from collections.abc import Iterator
from contextlib import contextmanager

import torch
from torch import nn
from transformers import PreTrainedModel

from qwen_compression.metrics import kl_and_loss_change, reference_log_probabilities
from qwen_compression.model_parts import (
    down_projection,
    final_hidden_states,
    hidden_states_before_layer,
    intermediate_size,
)


def neuron_scale_matrix(neuron_indices: torch.Tensor, scales: torch.Tensor, width: int) -> torch.Tensor:
    matrix = torch.ones(neuron_indices.shape[0], width, dtype=scales.dtype, device=scales.device)
    matrix[torch.arange(neuron_indices.shape[0], device=scales.device), neuron_indices] = scales
    return matrix


@contextmanager
def scaled_neurons(
    model: PreTrainedModel, layer_index: int, neuron_indices: torch.Tensor, scales: torch.Tensor
) -> Iterator[None]:
    projection = down_projection(model, layer_index)
    scale_matrix = neuron_scale_matrix(neuron_indices, scales, intermediate_size(model)).unsqueeze(1)

    def scale_input(module: nn.Module, arguments: tuple[torch.Tensor, ...]) -> tuple[torch.Tensor, ...]:
        activations = arguments[0]
        return (activations * scale_matrix.to(activations.dtype),)

    handle = projection.register_forward_pre_hook(scale_input)
    try:
        yield
    finally:
        handle.remove()


@torch.no_grad()
def measure_perturbations(
    model: PreTrainedModel,
    token_ids: torch.Tensor,
    layer_index: int,
    neuron_indices: torch.Tensor,
    scales: torch.Tensor,
    batch_size: int,
    chunk_length: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    perturbation_count = neuron_indices.shape[0]
    kl = torch.zeros(perturbation_count, token_ids.shape[0], dtype=torch.float64)
    loss_change = torch.zeros(perturbation_count, token_ids.shape[0], dtype=torch.float64)
    for sequence_index, sequence in enumerate(token_ids):
        sequence = sequence.to(model.device)
        layer_input = hidden_states_before_layer(model, sequence.unsqueeze(0), layer_index)
        reference = reference_log_probabilities(
            model, final_hidden_states(model, layer_input, layer_index), chunk_length
        )
        for start in range(0, perturbation_count, batch_size):
            batch_neurons = neuron_indices[start : start + batch_size].to(model.device)
            batch_scales = scales[start : start + batch_size].to(model.device)
            with scaled_neurons(model, layer_index, batch_neurons, batch_scales):
                perturbed_hidden = final_hidden_states(
                    model, layer_input.expand(batch_neurons.shape[0], -1, -1), layer_index
                )
            batch_kl, batch_loss_change = kl_and_loss_change(model, perturbed_hidden, reference, sequence, chunk_length)
            kl[start : start + batch_size, sequence_index] = batch_kl.double().cpu()
            loss_change[start : start + batch_size, sequence_index] = batch_loss_change.double().cpu()
    return kl, loss_change


def perturbation_grid(neurons: torch.Tensor, deltas: tuple[float, ...]) -> tuple[torch.Tensor, torch.Tensor]:
    return neurons.repeat_interleave(len(deltas)), (1 + torch.tensor(deltas)).repeat(neurons.numel())
