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


def mlp_activations(mlp: Qwen3MLP, mlp_input: torch.Tensor) -> torch.Tensor:
    return mlp.act_fn(mlp.gate_proj(mlp_input)) * mlp.up_proj(mlp_input)


def neuron_clusters(features: torch.Tensor, initial_centers: torch.Tensor, iterations: int) -> torch.Tensor:
    centers = features[initial_centers].clone()
    for _ in range(iterations):
        assignment = torch.cdist(features, centers).argmin(dim=1)
        sums = torch.zeros_like(centers).index_add_(0, assignment, features)
        counts = torch.bincount(assignment, minlength=centers.shape[0])
        occupied = counts > 0
        centers[occupied] = sums[occupied] / counts[occupied, None].to(sums.dtype)
    assignment = torch.cdist(features, centers).argmin(dim=1)
    return torch.unique(assignment, return_inverse=True)[1]


def merged_mlp(mlp: Qwen3MLP, assignment: torch.Tensor) -> Qwen3MLP:
    assignment = assignment.to(mlp.gate_proj.weight.device)
    cluster_count = int(assignment.max().item()) + 1
    gate_weight, up_weight, down_weight = mlp.gate_proj.weight, mlp.up_proj.weight, mlp.down_proj.weight
    counts = torch.bincount(assignment, minlength=cluster_count).to(gate_weight.dtype)[:, None]
    merged = copy.deepcopy(mlp)
    merged.gate_proj = linear_from_weight(
        torch.zeros(cluster_count, gate_weight.shape[1], dtype=gate_weight.dtype, device=gate_weight.device)
        .index_add_(0, assignment, gate_weight)
        .div_(counts)
    )
    merged.up_proj = linear_from_weight(
        torch.zeros(cluster_count, up_weight.shape[1], dtype=up_weight.dtype, device=up_weight.device)
        .index_add_(0, assignment, up_weight)
        .div_(counts)
    )
    merged.down_proj = linear_from_weight(
        torch.zeros(down_weight.shape[0], cluster_count, dtype=down_weight.dtype, device=down_weight.device).index_add_(
            1, assignment, down_weight
        )
    )
    merged.intermediate_size = cluster_count
    return merged
