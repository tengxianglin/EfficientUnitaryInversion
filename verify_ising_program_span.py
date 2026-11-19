"""Exact modular ranks for the physical Ising program span, n=3,5,7."""

import argparse
from math import comb
from random import Random

import numpy as np


def inverse_mod(matrix, prime):
    dim = len(matrix)
    work = np.concatenate(
        (matrix % prime, np.eye(dim, dtype=np.int64)), axis=1
    )
    for col in range(dim):
        pivot = next((i for i in range(col, dim) if work[i, col]), None)
        if pivot is None:
            return None
        work[[col, pivot]] = work[[pivot, col]]
        work[col] = work[col] * pow(int(work[col, col]), -1, prime) % prime
        factors = work[:, col].copy()
        factors[col] = 0
        work = (work - factors[:, None] * work[col]) % prime
    return work[:, dim:]


def verify(n):
    prime = 65521
    rng = Random(20261119 + n)
    basis = [x for x in range(2**n) if x.bit_count() % 2 == 0]
    dim = len(basis)
    lookup = {x: i for i, x in enumerate(basis)}
    signs = np.array(
        [[(-1)**((x >> i) & 1) for i in range(n)] for x in basis],
        dtype=np.int64,
    )
    edge_rows = [
        [lookup[x ^ (1 << i) ^ (1 << ((i + 1) % n))] for x in basis]
        for i in range(n)
    ]
    triangular = np.triu_indices(dim)
    ceiling = comb(2*n, n) // 2
    pivots = {}
    attempts = 0
    limit = 3 * dim * (dim + 1) // 2
    while len(pivots) < ceiling and attempts < limit:
        attempts += 1
        fields = [rng.randint(-19, 19) for _ in range(n)]
        edges = [rng.randint(-19, 19) for _ in range(n)]
        z = rng.randint(37, 96)
        hamiltonian = np.diag(signs @ fields)
        for i in range(n):
            hamiltonian[edge_rows[i], np.arange(dim)] += edges[i]
        inverse = inverse_mod(z*np.eye(dim, dtype=np.int64)-hamiltonian, prime)
        if inverse is None:
            continue
        np.testing.assert_array_equal(inverse, inverse.T)
        row = inverse[triangular]
        for col, previous in pivots.items():
            row = (row - int(row[col])*previous) % prime
        remaining = np.flatnonzero(row)
        if not len(remaining):
            continue
        col = int(remaining[0])
        pivots[col] = row * pow(int(row[col]), -1, prime) % prime

    assert len(pivots) == ceiling
    print(f"n={n}: exact rank {len(pivots)}, symmetric dimension "
          f"{dim*(dim+1)//2}, rational resolvent samples {attempts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, choices=(3, 5, 7), default=(3, 5))
    args = parser.parse_args()
    for size in args.sizes:
        verify(size)
