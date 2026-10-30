import copy
import itertools

import pytest
import torch
from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM

from qwen_compression.activations import collect_neuron_statistics
from qwen_compression.analysis import spearman, top_overlap
from qwen_compression.code_metrics import pass_at_k
from qwen_compression.data import interleave_evenly, interleave_sources, pack_sequences
from qwen_compression.importance import fisher_kl_coefficients
from qwen_compression.metrics import kl_and_loss_change, reference_log_probabilities
from qwen_compression.model_parts import (
    decoder_layers,
    down_projection,
    final_hidden_states,
    hidden_states_before_layer,
    mlp_of,
    replaced_mlp,
    run_layer_window,
)
from qwen_compression.perturbation import measure_perturbations, scaled_neurons
from qwen_compression.reconstruction import (
    LeastSquaresStatistics,
    merged_mlp,
    mlp_activations,
    neuron_clusters,
    pruned_mlp,
)
from qwen_compression.training import output_kl

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
    correlation = spearman(predicted, exact)
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


def test_interleave_evenly_keeps_proportions() -> None:
    code_rows, text_rows = torch.arange(6).view(6, 1), torch.arange(100, 102).view(2, 1)
    interleaved, sources = interleave_evenly({"code": code_rows, "c4": text_rows})
    assert sources == ["code", "c4", "code", "code", "code", "c4", "code", "code"]
    assert interleaved.flatten().tolist() == [0, 100, 1, 2, 3, 101, 4, 5]


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


def test_spearman_and_top_overlap() -> None:
    values = torch.tensor([3.0, 1.0, 4.0, 1.5, 9.0, 2.6])
    assert abs(spearman(values, values * 2 + 1) - 1) < 1e-12
    assert abs(spearman(values, -values) + 1) < 1e-12
    assert abs(spearman(torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0]), torch.tensor([2.0, 1.0, 4.0, 3.0, 5.0])) - 0.8) < 1e-12
    assert top_overlap(values, values, 0.5) == 1.0


def test_layer_window_reproduces_hidden_states(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    with torch.no_grad():
        hidden = model.model(input_ids=token_ids, output_hidden_states=True, use_cache=False).hidden_states
        layers = list(decoder_layers(model))
        output = run_layer_window(model, hidden[1], layers[1:3])
    torch.testing.assert_close(output, hidden[3])
    assert len(model.model.layers) == 4


def test_pruned_mlp_keeping_all_neurons_is_identical(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    mlp = mlp_of(model, 1)
    with replaced_mlp(model, 1, pruned_mlp(mlp, torch.arange(48))):
        pruned_logits = full_logits(model, token_ids)
    torch.testing.assert_close(pruned_logits, full_logits(model, token_ids))


def test_pruned_mlp_matches_zeroed_neurons(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    keep = torch.tensor([index for index in range(48) if index % 3 != 0])
    removed = torch.tensor([index for index in range(48) if index % 3 == 0])
    with replaced_mlp(model, 2, pruned_mlp(mlp_of(model, 2), keep)):
        pruned_logits = full_logits(model, token_ids)
    zeroed_model = copy.deepcopy(model)
    down_projection(zeroed_model, 2).weight[:, removed] = 0
    torch.testing.assert_close(pruned_logits, full_logits(zeroed_model, token_ids))


def test_least_squares_recovers_down_projection_when_keeping_all(
    model: Qwen3ForCausalLM, token_ids: torch.Tensor
) -> None:
    double_model = copy.deepcopy(model).double()
    statistics = LeastSquaresStatistics(48, 32)
    projection = down_projection(double_model, 1)

    def record(module: torch.nn.Module, arguments: tuple[torch.Tensor, ...], output: torch.Tensor) -> None:
        statistics.add(arguments[0], output)

    handle = projection.register_forward_hook(record)
    full_logits(double_model, torch.randint(0, 64, (10, SEQUENCE_LENGTH), generator=torch.Generator().manual_seed(3)))
    handle.remove()
    torch.testing.assert_close(statistics.down_weight(torch.arange(48), 1e-12), projection.weight, atol=1e-6, rtol=1e-6)


def test_least_squares_beats_plain_pruning(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    double_model = copy.deepcopy(model).double()
    statistics = LeastSquaresStatistics(48, 32)
    captured: list[tuple[torch.Tensor, torch.Tensor]] = []

    def record(module: torch.nn.Module, arguments: tuple[torch.Tensor, ...], output: torch.Tensor) -> None:
        statistics.add(arguments[0], output)
        captured.append((arguments[0].reshape(-1, 48), output.reshape(-1, 32)))

    projection = down_projection(double_model, 1)
    handle = projection.register_forward_hook(record)
    full_logits(double_model, token_ids)
    handle.remove()
    activations, targets = captured[0]
    keep = torch.arange(0, 48, 2)
    plain_error = (activations[:, keep] @ projection.weight[:, keep].T - targets).square().sum()
    fitted_error = (activations[:, keep] @ statistics.down_weight(keep, 1e-9).T - targets).square().sum()
    assert fitted_error < plain_error


def test_merged_mlp_with_one_neuron_per_cluster_is_identical(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    with replaced_mlp(model, 1, merged_mlp(mlp_of(model, 1), torch.arange(48))):
        merged_logits = full_logits(model, token_ids)
    torch.testing.assert_close(merged_logits, full_logits(model, token_ids))


def test_merging_identical_neurons_keeps_output(model: Qwen3ForCausalLM) -> None:
    mlp = copy.deepcopy(mlp_of(model, 1)).double()
    mlp.gate_proj.weight[1] = mlp.gate_proj.weight[0]
    mlp.up_proj.weight[1] = mlp.up_proj.weight[0]
    assignment = torch.tensor([0, *range(47)])
    mlp_input = torch.randn(7, 32, dtype=torch.float64, generator=torch.Generator().manual_seed(4))
    merged = merged_mlp(mlp, assignment)
    assert merged.down_proj.weight.shape == (32, 47)
    torch.testing.assert_close(merged(mlp_input), mlp(mlp_input))
    torch.testing.assert_close(
        mlp_activations(mlp, mlp_input), mlp.act_fn(mlp.gate_proj(mlp_input)) * mlp.up_proj(mlp_input)
    )


def test_neuron_clusters_group_duplicates_and_number_clusters_contiguously() -> None:
    base = torch.randn(5, 6, generator=torch.Generator().manual_seed(5)) * 10
    features = torch.cat([base, base + 1e-3])
    assignment = neuron_clusters(features, torch.arange(5), 10)
    assert torch.equal(assignment[:5], assignment[5:])
    assert torch.equal(torch.unique(assignment), torch.arange(5))


def test_output_kl_matches_direct_computation_and_gradient(model: Qwen3ForCausalLM, token_ids: torch.Tensor) -> None:
    double_model = copy.deepcopy(model).double()
    layer_input = hidden_states_before_layer(double_model, token_ids[:1], 2)
    student = pruned_mlp(mlp_of(double_model, 2), torch.arange(0, 48, 2))
    direct_student = copy.deepcopy(student)
    student.requires_grad_(True)
    direct_student.requires_grad_(True)
    value = output_kl(double_model, 2, student, layer_input, CHUNK_LENGTH, gradient_scale=0.5)
    with torch.no_grad():
        reference = torch.log_softmax(double_model.lm_head(final_hidden_states(double_model, layer_input, 2)), dim=-1)
    with replaced_mlp(double_model, 2, direct_student):
        perturbed = torch.log_softmax(double_model.lm_head(final_hidden_states(double_model, layer_input, 2)), dim=-1)
    direct = (reference.exp() * (reference - perturbed)).sum(dim=-1).mean()
    (0.5 * direct).backward()
    assert value == pytest.approx(direct.item(), rel=1e-9)
    for parameter, direct_parameter in zip(student.parameters(), direct_student.parameters(), strict=True):
        torch.testing.assert_close(parameter.grad, direct_parameter.grad)
    assert output_kl(double_model, 2, student, layer_input, CHUNK_LENGTH) == pytest.approx(direct.item(), rel=1e-9)


def test_pass_at_k_matches_enumeration() -> None:
    sample_count, correct_count = 6, 2
    outcomes = [True] * correct_count + [False] * (sample_count - correct_count)
    for k in (1, 2, 3):
        subsets = list(itertools.combinations(outcomes, k))
        expected = sum(any(subset) for subset in subsets) / len(subsets)
        assert pass_at_k(sample_count, correct_count, k) == pytest.approx(expected)
    assert pass_at_k(10, 0, 3) == 0.0
    assert pass_at_k(10, 8, 3) == 1.0
    assert pass_at_k(1, 1, 1) == 1.0
