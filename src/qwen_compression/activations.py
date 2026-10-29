from dataclasses import dataclass, field

import torch
from torch import nn
from transformers import PreTrainedModel

from qwen_compression.model_parts import decoder_layers, down_projection, intermediate_size


@dataclass
class NeuronStatistics:
    layer_count: int
    width: int
    active_threshold: float
    token_count: int = 0
    activation_sum: torch.Tensor = field(init=False)
    squared_sum: torch.Tensor = field(init=False)
    absolute_sum: torch.Tensor = field(init=False)
    absolute_max: torch.Tensor = field(init=False)
    active_count: torch.Tensor = field(init=False)

    def __post_init__(self) -> None:
        shape = (self.layer_count, self.width)
        self.activation_sum = torch.zeros(shape, dtype=torch.float64)
        self.squared_sum = torch.zeros(shape, dtype=torch.float64)
        self.absolute_sum = torch.zeros(shape, dtype=torch.float64)
        self.absolute_max = torch.zeros(shape, dtype=torch.float64)
        self.active_count = torch.zeros(shape, dtype=torch.float64)

    def add(self, layer_index: int, activations: torch.Tensor) -> None:
        flat = activations.reshape(-1, self.width).double()
        absolute = flat.abs()
        self.activation_sum[layer_index] += flat.sum(dim=0).cpu()
        self.squared_sum[layer_index] += flat.square().sum(dim=0).cpu()
        self.absolute_sum[layer_index] += absolute.sum(dim=0).cpu()
        self.absolute_max[layer_index] = torch.maximum(self.absolute_max[layer_index], absolute.max(dim=0).values.cpu())
        self.active_count[layer_index] += (absolute > self.active_threshold).sum(dim=0).cpu().double()

    def summary(self) -> dict[str, torch.Tensor]:
        mean = self.activation_sum / self.token_count
        return {
            "mean": mean,
            "standard_deviation": (self.squared_sum / self.token_count - mean.square()).clamp_min(0).sqrt(),
            "mean_absolute": self.absolute_sum / self.token_count,
            "max_absolute": self.absolute_max,
            "active_fraction": self.active_count / self.token_count,
        }


@torch.no_grad()
def collect_neuron_statistics(
    model: PreTrainedModel, token_ids: torch.Tensor, active_threshold: float
) -> dict[str, torch.Tensor]:
    layer_count = len(decoder_layers(model))
    statistics = NeuronStatistics(layer_count, intermediate_size(model), active_threshold)
    handles = []
    for layer_index in range(layer_count):

        def record(module: nn.Module, arguments: tuple[torch.Tensor, ...], layer_index: int = layer_index) -> None:
            statistics.add(layer_index, arguments[0])

        handles.append(down_projection(model, layer_index).register_forward_pre_hook(record))
    try:
        for sequence in token_ids:
            model.model(input_ids=sequence.unsqueeze(0).to(model.device), use_cache=False)
            statistics.token_count += sequence.numel()
    finally:
        for handle in handles:
            handle.remove()
    return statistics.summary()
