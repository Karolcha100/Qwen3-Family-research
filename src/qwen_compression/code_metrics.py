import math


def pass_at_k(sample_count: int, correct_count: int, k: int) -> float:
    if sample_count - correct_count < k:
        return 1.0
    return 1.0 - math.comb(sample_count - correct_count, k) / math.comb(sample_count, k)
