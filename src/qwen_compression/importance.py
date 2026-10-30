from typing import cast

import torch
from torch import nn
from transformers import PreTrainedModel

from qwen_compression.model_parts import at_least_float32, decoder_layers, down_projection, intermediate_size


def sampled_hidden_gradients(
    output_weight: torch.Tensor,
    final_hidden: torch.Tensor,
    samples_per_sequence: int,
    generator: torch.Generator,
    chunk_length: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    expected_rows = []
    sampled_tokens = []
    for start in range(0, final_hidden.shape[0], chunk_length):
        logits = at_least_float32(final_hidden[start : start + chunk_length] @ output_weight.T)
        probabilities = torch.softmax(logits, dim=-1)
        sampled_tokens.append(
            torch.multinomial(probabilities, num_samples=samples_per_sequence, replacement=True, generator=generator)
        )
        expected_rows.append(probabilities @ at_least_float32(output_weight))
    return torch.cat(expected_rows), torch.cat(sampled_tokens)


def fisher_kl_coefficients(
    model: PreTrainedModel,
    token_ids: torch.Tensor,
    samples_per_sequence: int,
    generator: torch.Generator,
    chunk_length: int = 256,
) -> torch.Tensor:
    layer_count = len(decoder_layers(model))
    squared_score_sum = torch.zeros(layer_count, intermediate_size(model), dtype=torch.float64)
    output_weight = cast(nn.Linear, model.get_submodule("lm_head")).weight
    captured: dict[int, torch.Tensor] = {}
    handles = []
    for layer_index in range(layer_count):

        def capture(module: nn.Module, arguments: tuple[torch.Tensor, ...], layer_index: int = layer_index) -> None:
            captured[layer_index] = arguments[0]

        handles.append(down_projection(model, layer_index).register_forward_pre_hook(capture))
    token_total = 0
    try:
        for sequence in token_ids:
            input_ids = sequence.unsqueeze(0).to(model.device)
            embeddings = model.get_input_embeddings()(input_ids).detach().requires_grad_(True)
            final_hidden = model.base_model(inputs_embeds=embeddings, use_cache=False).last_hidden_state[0]
            with torch.no_grad():
                expected_rows, sampled_tokens = sampled_hidden_gradients(
                    output_weight, final_hidden.detach(), samples_per_sequence, generator, chunk_length
                )
            for sample_index in range(samples_per_sequence):
                hidden_gradient = at_least_float32(output_weight[sampled_tokens[:, sample_index]]) - expected_rows
                gradients = torch.autograd.grad(
                    final_hidden,
                    list(captured.values()),
                    grad_outputs=hidden_gradient.to(final_hidden.dtype),
                    retain_graph=sample_index < samples_per_sequence - 1,
                )
                for (layer_index, activation), gradient in zip(captured.items(), gradients, strict=True):
                    score = (at_least_float32(gradient) * at_least_float32(activation.detach())).sum(dim=(0, 1))
                    squared_score_sum[layer_index] += score.double().square().cpu()
            token_total += sequence.numel()
            captured.clear()
    finally:
        for handle in handles:
            handle.remove()
    return squared_score_sum / (2 * samples_per_sequence * token_total)
