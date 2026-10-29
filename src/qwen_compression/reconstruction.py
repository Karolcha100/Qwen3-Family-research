import copy
from dataclasses import dataclass, field

import torch
from torch import nn
from transformers.models.qwen3.modeling_qwen3 import Qwen3MLP


def linear_from_weight(weight: torch.Tensor) -> nn.Linear:
    layer = nn.Linear(weight.shape[1], weight.shape[0], bias=False, device=weight.device, dtype=weight.dtype)
    layer.weight = nn.Parameter(weight.detach().clone())
    return layer


def pruned_mlp(mlp: Qwen3MLP, keep: torch.Tensor, down_weight: torch.Tensor | None = None) -> Qwen3MLP:
    keep = keep.to(mlp.gate_proj.weight.device)
    pruned = copy.deepcopy(mlp)
    pruned.gate_proj = linear_from_weight(mlp.gate_proj.weight[keep])
    pruned.up_proj = linear_from_weight(mlp.up_proj.weight[keep])
    pruned.down_proj = linear_from_weight(
        mlp.down_proj.weight[:, keep] if down_weight is None else down_weight.to(mlp.down_proj.weight)
    )
    pruned.intermediate_size = keep.numel()
    return pruned


@dataclass
class LeastSquaresStatistics:
    width: int
    output_size: int
    token_count: int = 0
    gram: torch.Tensor = field(init=False)
    cross: torch.Tensor = field(init=False)

    def __post_init__(self) -> None:
        self.gram = torch.zeros(self.width, self.width, dtype=torch.float64)
        self.cross = torch.zeros(self.width, self.output_size, dtype=torch.float64)

    def add(self, activations: torch.Tensor, targets: torch.Tensor) -> None:
        flat_activations = activations.reshape(-1, self.width).double()
        flat_targets = targets.reshape(-1, self.output_size).double()
        self.gram += (flat_activations.T @ flat_activations).cpu()
        self.cross += (flat_activations.T @ flat_targets).cpu()
        self.token_count += flat_activations.shape[0]

    def down_weight(self, keep: torch.Tensor, relative_ridge: float) -> torch.Tensor:
        gram = self.gram[keep][:, keep]
        ridge = relative_ridge * gram.diagonal().mean()
        regularized = gram + ridge * torch.eye(keep.numel(), dtype=torch.float64)
        return torch.linalg.solve(regularized, self.cross[keep]).T
