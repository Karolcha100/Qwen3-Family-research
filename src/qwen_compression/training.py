import torch
from torch import nn
from transformers import PreTrainedModel

from qwen_compression.metrics import log_probabilities
from qwen_compression.model_parts import final_hidden_states, replaced_mlp


def output_kl(
    model: PreTrainedModel,
    layer_index: int,
    student_mlp: nn.Module,
    layer_input: torch.Tensor,
    chunk_length: int,
    gradient_scale: float | None = None,
) -> float:
    with torch.no_grad():
        teacher_final = final_hidden_states(model, layer_input, layer_index)
    with torch.set_grad_enabled(gradient_scale is not None), replaced_mlp(model, layer_index, student_mlp):
        student_final = final_hidden_states(model, layer_input, layer_index)
    detached_final = student_final.detach().requires_grad_(gradient_scale is not None)
    token_count = layer_input.shape[0] * layer_input.shape[1]
    total = 0.0
    for start in range(0, layer_input.shape[1], chunk_length):
        with torch.no_grad():
            reference = log_probabilities(model, teacher_final[:, start : start + chunk_length])
        with torch.set_grad_enabled(gradient_scale is not None):
            student = log_probabilities(model, detached_final[:, start : start + chunk_length])
            chunk_kl = (reference.exp() * (reference - student)).sum() / token_count
        if gradient_scale is not None:
            (chunk_kl * gradient_scale).backward()
        total += chunk_kl.item()
    if gradient_scale is not None:
        student_final.backward(detached_final.grad)
    return total
