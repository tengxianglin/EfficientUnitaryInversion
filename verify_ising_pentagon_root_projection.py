"""Exact certificate for the 21-basis pentagon coefficient projection."""

from fractions import Fraction
from itertools import combinations, product
from math import prod

import numpy as np
from sympy import prevprime


def projector_grams():
    """Return exact Gram matrices with common denominator 5**8."""
    weights = tuple(w for w in product((1, -1), repeat=5) if prod(w) == 1)
    dim = len(weights)
    weights_index = {w: i for i, w in enumerate(weights)}
    pair_sums = [tuple(a + b for a, b in zip(w, v))
                 for w in weights for v in weights]
    characters = sorted(set(pair_sums) | {tuple(-a for a in w) for w in pair_sums})
    char_index = {w: i for i, w in enumerate(characters)}
    indices = np.array([char_index[w] for w in pair_sums])
    inverse_char = [char_index[tuple(-a for a in w)] for w in characters]

    # Every matrix stored here is five times its spinor basis rotation.
    bases = [5 * np.eye(dim, dtype=np.int64)]
    for i, j in combinations(range(5), 2):
        for occupation_type in (-1, 1):
            basis = bases[0].copy()
            for p, w in enumerate(weights):
                if w[i] != 1 or w[j] != occupation_type:
                    continue
                partner = tuple(-a if k in (i, j) else a for k, a in enumerate(w))
                q = weights_index[partner]
                sign = prod(w[i + 1:j])
                basis[p, p] = basis[q, q] = 3
                basis[q, p] = 4 * sign
                basis[p, q] = -4 * sign
            assert np.array_equal(basis.T @ basis, 25 * np.eye(dim, dtype=np.int64))
            bases.append(basis)

    width = len(characters)
    gram = np.zeros((width * len(bases),) * 2, dtype=np.int64)
    for i, basis in enumerate(bases):
        for j, other in enumerate(bases[:i + 1]):
            overlap = (basis.T @ other)**2
            block = np.zeros((width, width), dtype=np.int64)
            np.add.at(block, (indices[:, None], indices[None, :]),
                      np.kron(overlap, overlap))
            gram[i*width:(i+1)*width, j*width:(j+1)*width] = block
            gram[j*width:(j+1)*width, i*width:(i+1)*width] = block.T

    negate = [i * width + k for i in range(len(bases)) for k in inverse_char]
    target = gram[np.ix_(negate, negate)]
    assert gram.shape == (2562, 2562)
    assert int(np.trace(target)) == int(np.trace(gram)) == 21 * 16**2 * 5**8
    return gram, target


def exact_moments(gram, target, highest_power):
    """Compute Tr(gram**k @ target), k=1,...,highest_power, by CRT."""
    row_sum = int(gram.sum(axis=1).max())
    trace = int(np.trace(target))
    bound = row_sum**highest_power * trace
    nonzero = gram.any(axis=1)
    gram = gram[np.ix_(nonzero, nonzero)]
    target = target[np.ix_(nonzero, nonzero)]
    rows, cols = target.nonzero()
    h = target[rows, cols]

    modulus = 1
    moments = [0] * highest_power
    prime = 2**20
    while modulus <= bound:
        prime = int(prevprime(prime))
        # Nonnegative integer dot products fit in the exact binary64 range.
        assert len(gram) * (prime - 1)**2 < 2**53
        assert len(h) * (prime - 1)**2 < 2**63
        base = (gram % prime).astype(np.float64)
        power = base
        h_mod = h % prime
        inverse = pow(modulus, -1, prime)
        for k in range(highest_power):
            entries = power[rows, cols].astype(np.int64)
            residue = int(entries @ h_mod) % prime
            moments[k] += modulus * ((residue - moments[k]) * inverse % prime)
            if k + 1 < highest_power:
                power = (base @ power) % prime
        modulus *= prime
    assert all(0 <= value <= row_sum**k * trace for k, value in enumerate(moments, 1))
    return [Fraction(value, row_sum**k * trace) for k, value in enumerate(moments, 1)]


def certificate():
    gram, target = projector_grams()
    coefficients = (34, -244, 506, -316)
    moments = exact_moments(gram, target, 2 * len(coefficients))
    linear = 2 * sum(a * moments[i] for i, a in enumerate(coefficients))
    quadratic = sum(a*b*moments[i+j+1] for i, a in enumerate(coefficients)
                    for j, b in enumerate(coefficients))
    witness = linear - quadratic
    assert witness > Fraction(19, 25) > Fraction(3, 4)
    print("Exact lower bound on projected alternate fraction:", witness)
    print("Decimal display:", f"{float(witness):.12f}")


if __name__ == "__main__":
    certificate()
