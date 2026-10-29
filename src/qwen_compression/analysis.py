import torch


def ranks(values: torch.Tensor) -> torch.Tensor:
    order = values.argsort()
    result = torch.empty_like(order, dtype=torch.float64)
    result[order] = torch.arange(values.numel(), dtype=torch.float64)
    return result


def spearman(first: torch.Tensor, second: torch.Tensor) -> float:
    first_ranks = ranks(first.flatten()) - (first.numel() - 1) / 2
    second_ranks = ranks(second.flatten()) - (second.numel() - 1) / 2
    return float((first_ranks * second_ranks).sum() / (first_ranks.norm() * second_ranks.norm()))


def top_overlap(first: torch.Tensor, second: torch.Tensor, fraction: float) -> float:
    count = max(1, int(fraction * first.numel()))
    first_top = set(first.topk(count).indices.tolist())
    second_top = set(second.topk(count).indices.tolist())
    return len(first_top & second_top) / count
