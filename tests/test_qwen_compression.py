import copy

import pytest
import torch
from scipy.stats import spearmanr
from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM

from qwen_compression.activations import collect_neuron_statistics
from qwen_compression.data import interleave_sources, pack_sequences
from qwen_compression.importance import fisher_kl_coefficients
from qwen_compression.metrics import kl_and_loss_change, reference_log_probabilities
from qwen_compression.model_parts import down_projection, final_hidden_states, hidden_states_before_layer
from qwen_compression.perturbation import measure_perturbations, scaled_neurons

SEQUENCE_LENGTH = 16
CHUNK_LENGTH = 5


@pytest.fixture(scope="module")
def model() -> Qwen3ForCausalLM:
    torch.manual_seed(0)
    config = Qwen3Config(
        vocab_size=64,
        hidden_size=32,
        intermediate_size=48,
        num_hidden_layers=4,
        num_attention_heads=4,
        num_key_value_heads=2,
        head_dim=8,
        max_position_embeddings=64,
    )
    tiny_model = Qwen3ForCausalLM(config).eval()
    tiny_model.requires_grad_(False)
    return tiny_model


@pytest.fixture(scope="module")
def token_ids() -> torch.Tensor:
    return torch.randint(0, 64, (3, SEQUENCE_LENGTH), generator=torch.Generator().manual_seed(1))


def full_logits(model: Qwen3ForCausalLM, tokens: torch.Tensor) -> torch.Tensor:
    with torch.no_grad():
        return model(input_ids=tokens, use_cache=False).logits


def logits_from_layer(model: Qwen3ForCausalLM, tokens: torch.Tensor, layer_index: int) -> torch.Tensor:
    with torch.no_grad():
        layer_input = hidden_states_before_layer(model, tokens, layer_index)
        return model.lm_head(final_hidden_states(model, layer_input, layer_index))


@pytest.mark.parametrize("layer_index", [0, 2, 3])
def test_starting_from_layer_matches_full_forward(
    model: Qwen3ForCausalLM, token_ids: torch.Tensor, layer_index: int
) -> None:
    torch.testing.assert_close(logits_from_layer(model, token_ids, layer_index), full_logits(model, token_ids))
    assert len(model.model.layers) == 4


def test_unit_scale_changes_nothing(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    with scaled_neurons(model, 1, torch.tensor([5, 7, 9]), torch.ones(3)):
        perturbed = full_logits(model, token_ids)
    torch.testing.assert_close(perturbed, full_logits(model, token_ids))


def test_zero_scale_equals_removing_neuron(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    neuron_index = 11
    with scaled_neurons(model, 2, torch.tensor([neuron_index]), torch.zeros(1)):
        scaled = full_logits(model, token_ids[:1])
    projection = down_projection(model, 2)
    original_column = projection.weight[:, neuron_index].clone()
    projection.weight[:, neuron_index] = 0
    removed = full_logits(model, token_ids[:1])
    projection.weight[:, neuron_index] = original_column
    torch.testing.assert_close(scaled, removed)


def test_batched_perturbations_match_individual_runs(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    neuron_indices = torch.tensor([3, 3, 20, 47])
    scales = torch.tensor([0.0, 2.0, 0.5, 1.5])
    single_sequence = token_ids[:1]
    with scaled_neurons(model, 1, neuron_indices, scales):
        batched = full_logits(model, single_sequence.expand(4, -1))
    for row, (neuron_index, scale) in enumerate(zip(neuron_indices, scales, strict=True)):
        with scaled_neurons(model, 1, neuron_index.view(1), scale.view(1)):
            torch.testing.assert_close(batched[row : row + 1], full_logits(model, single_sequence))


def exact_kl_and_loss(
    model: Qwen3ForCausalLM,
    sequence: torch.Tensor,
    layer_index: int,
    neuron_indices: torch.Tensor,
    scales: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    with torch.no_grad():
        layer_input = hidden_states_before_layer(model, sequence.unsqueeze(0), layer_index)
        reference = reference_log_probabilities(
            model, final_hidden_states(model, layer_input, layer_index), CHUNK_LENGTH
        )
        with scaled_neurons(model, layer_index, neuron_indices, scales):
            perturbed_hidden = final_hidden_states(
                model, layer_input.expand(neuron_indices.shape[0], -1, -1), layer_index
            )
        return kl_and_loss_change(model, perturbed_hidden, reference, sequence, CHUNK_LENGTH)


def test_kl_and_loss_change_match_direct_computation(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    sequence = token_ids[0]
    kl, loss_change = exact_kl_and_loss(model, sequence, 1, torch.tensor([4, 4]), torch.tensor([1.0, 0.0]))
    reference = torch.log_softmax(full_logits(model, sequence.unsqueeze(0))[0], dim=-1)
    with scaled_neurons(model, 1, torch.tensor([4]), torch.zeros(1)):
        perturbed = torch.log_softmax(full_logits(model, sequence.unsqueeze(0))[0], dim=-1)
    expected_kl = (reference.exp() * (reference - perturbed)).sum(dim=-1).mean()
    targets = sequence[1:]
    expected_loss_change = (
        reference[:-1].gather(1, targets[:, None]) - perturbed[:-1].gather(1, targets[:, None])
    ).mean()
    torch.testing.assert_close(kl, torch.stack([torch.tensor(0.0), expected_kl]))
    torch.testing.assert_close(loss_change, torch.stack([torch.tensor(0.0), expected_loss_change]))


def test_fisher_coefficients_rank_neurons_like_exact_kl(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    delta = 0.05
    layer_index = 1
    double_model = copy.deepcopy(model).double()
    width = double_model.config.intermediate_size
    coefficients = fisher_kl_coefficients(double_model, token_ids, 400, torch.Generator().manual_seed(2))
    exact = torch.zeros(width, dtype=torch.float64)
    scales = torch.full((width,), 1 + delta, dtype=torch.float64)
    for sequence in token_ids:
        kl, _ = exact_kl_and_loss(double_model, sequence, layer_index, torch.arange(width), scales)
        exact += kl / token_ids.shape[0]
    predicted = coefficients[layer_index] * delta**2
    correlation = spearmanr(predicted.numpy(), exact.numpy()).statistic
    assert correlation > 0.9
    assert 0.5 < (predicted.sum() / exact.sum()).item() < 2.0


def test_neuron_statistics_match_manual_computation(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    statistics = collect_neuron_statistics(model, token_ids, active_threshold=0.01)
    captured: list[torch.Tensor] = []
    handle = down_projection(model, 3).register_forward_pre_hook(
        lambda module, arguments: captured.append(arguments[0])
    )
    full_logits(model, token_ids)
    handle.remove()
    activations = captured[0].reshape(-1, model.config.intermediate_size).double()
    torch.testing.assert_close(statistics["mean"][3], activations.mean(dim=0))
    torch.testing.assert_close(statistics["max_absolute"][3], activations.abs().max(dim=0).values)
    torch.testing.assert_close(statistics["active_fraction"][3], (activations.abs() > 0.01).double().mean(dim=0))


def test_measurement_set_packing_and_interleaving() -> None:
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B-Base")
    texts = [f"Sentence number {index} about compression of language models." for index in range(200)]
    sequences = pack_sequences(tokenizer, texts, sequence_length=32, sequence_count=6)
    assert sequences.shape == (6, 32)
    assert (sequences == tokenizer.eos_token_id).any()
    interleaved, sources = interleave_sources(sequences, sequences[:2] + 1, text_per_code=3)
    assert sources == ["c4", "c4", "c4", "code", "c4", "c4", "c4", "code"]
    torch.testing.assert_close(interleaved[3], sequences[0] + 1)


def test_measure_perturbations_matches_single_measurements(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    neuron_indices = torch.tensor([0, 5, 5, 30, 47])
    scales = torch.tensor([0.0, 0.5, 2.0, 1.5, 0.0])
    kl, loss_change = measure_perturbations(model, token_ids[:2], 2, neuron_indices, scales, 2, CHUNK_LENGTH)
    assert kl.shape == (5, 2)
    for row in range(5):
        for sequence_index in range(2):
            expected_kl, expected_loss = exact_kl_and_loss(
                model, token_ids[sequence_index], 2, neuron_indices[row : row + 1], scales[row : row + 1]
            )
            torch.testing.assert_close(kl[row, sequence_index], expected_kl[0].double())
            torch.testing.assert_close(loss_change[row, sequence_index], expected_loss[0].double())
