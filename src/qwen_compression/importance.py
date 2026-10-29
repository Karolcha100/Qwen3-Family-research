import torch
from torch import nn
from transformers import PreTrainedModel

from qwen_compression.model_parts import at_least_float32, decoder_layers, down_projection, intermediate_size


def fisher_kl_coefficients(
    model: PreTrainedModel, token_ids: torch.Tensor, samples_per_sequence: int, generator: torch.Generator
) -> torch.Tensor:
    layer_count = len(decoder_layers(model))
    squared_score_sum = torch.zeros(layer_count, intermediate_size(model), dtype=torch.float64)
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
            logits = at_least_float32(model(inputs_embeds=embeddings, use_cache=False).logits)
            log_probabilities = torch.log_softmax(logits[0], dim=-1)
            probabilities = log_probabilities.detach().exp()
            for sample_index in range(samples_per_sequence):
                sampled_tokens = torch.multinomial(probabilities, num_samples=1, generator=generator)
                sampled_log_likelihood = log_probabilities.gather(1, sampled_tokens).sum()
                gradients = torch.autograd.grad(
                    sampled_log_likelihood,
                    list(captured.values()),
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
