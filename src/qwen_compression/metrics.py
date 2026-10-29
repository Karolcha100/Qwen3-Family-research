import torch
from transformers import PreTrainedModel

from qwen_compression.model_parts import at_least_float32


def log_probabilities(model: PreTrainedModel, final_hidden: torch.Tensor) -> torch.Tensor:
    return torch.log_softmax(at_least_float32(model.lm_head(final_hidden)), dim=-1)


@torch.no_grad()
def reference_log_probabilities(
    model: PreTrainedModel, final_hidden: torch.Tensor, chunk_length: int
) -> list[torch.Tensor]:
    return [
        log_probabilities(model, final_hidden[:, start : start + chunk_length])
        for start in range(0, final_hidden.shape[1], chunk_length)
    ]


@torch.no_grad()
def kl_and_loss_change(
    model: PreTrainedModel,
    perturbed_final_hidden: torch.Tensor,
    reference_chunks: list[torch.Tensor],
    token_ids: torch.Tensor,
    chunk_length: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    batch_size, sequence_length = perturbed_final_hidden.shape[:2]
    accumulator_dtype = at_least_float32(perturbed_final_hidden).dtype
    kl_sum = torch.zeros(batch_size, device=perturbed_final_hidden.device, dtype=accumulator_dtype)
    loss_change_sum = torch.zeros(batch_size, device=perturbed_final_hidden.device, dtype=accumulator_dtype)
    targets = token_ids[1:]
    for chunk_index, start in enumerate(range(0, sequence_length, chunk_length)):
        reference = reference_chunks[chunk_index]
        perturbed = log_probabilities(model, perturbed_final_hidden[:, start : start + chunk_length])
        kl_sum += (reference.exp() * (reference - perturbed)).sum(dim=-1).sum(dim=-1)
        positions = torch.arange(start, min(start + chunk_length, sequence_length - 1), device=targets.device)
        if positions.numel() > 0:
            local = positions - start
            chosen = targets[positions]
            loss_change_sum += (reference[0, local, chosen] - perturbed[:, local, chosen]).sum(dim=-1)
    return kl_sum / sequence_length, loss_change_sum / (sequence_length - 1)
