"""Per-instance L1 normalization for support-mismatch Hamiltonian noise."""

import math


def scale_out_of_support_coefficients(in_support, raw_out_support, delta: float):
    """Scale each batch row to the requested relative L1 noise strength.

    raw_out_support is an iid-Gaussian direction. The returned tensor
    satisfies, row by row, ||scaled_out_support||_1 = delta * ||in_support||_1.
    """
    if not math.isfinite(float(delta)) or delta < 0:
        raise ValueError("delta must be a finite nonnegative scalar")
    if getattr(in_support, "ndim", None) != 2 or getattr(raw_out_support, "ndim", None) != 2:
        raise ValueError("coefficient batches must be rank-2 tensors")
    if in_support.shape[0] != raw_out_support.shape[0]:
        raise ValueError("in-support and out-support batch sizes must match")
    if in_support.shape[1] == 0 or raw_out_support.shape[1] == 0:
        raise ValueError("both support batches must contain at least one coefficient")
    if getattr(in_support, "device", None) != getattr(raw_out_support, "device", None):
        raise ValueError("coefficient batches must be on the same device")
    if getattr(in_support, "dtype", None) != getattr(raw_out_support, "dtype", None):
        raise ValueError("coefficient batches must have the same dtype")

    in_l1 = in_support.abs().sum(dim=1, keepdim=True)
    raw_out_l1 = raw_out_support.abs().sum(dim=1, keepdim=True)
    if bool((in_l1 == 0).any().item()):
        raise ValueError("each in-support row must have nonzero L1 norm")
    if bool((raw_out_l1 == 0).any().item()):
        raise ValueError("each raw out-support row must have nonzero L1 norm")
    return raw_out_support * (float(delta) * in_l1 / raw_out_l1)
