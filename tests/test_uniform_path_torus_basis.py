"""Numerical regression for the explicit real canonical basis of the uniform path."""

import unittest

import numpy as np


def uniform_path_matrices():
    n = 42
    generator = np.zeros((n, n), dtype=np.float64)
    for j in range(n - 1):
        generator[j, j + 1] = 2.0
        generator[j + 1, j] = -2.0

    q = np.zeros((n, n), dtype=np.float64)
    frequencies = []
    for k in range(1, 22):
        frequencies.append(4.0 * np.cos(k * np.pi / 43.0))
        for j in range(n):
            sine = np.sin((j + 1) * k * np.pi / 43.0)
            q[j, 2 * k - 2] = np.sqrt(4.0 / 43.0) * sine * np.cos(j * np.pi / 2.0)
            q[j, 2 * k - 1] = np.sqrt(4.0 / 43.0) * sine * np.sin(j * np.pi / 2.0)

    canonical = np.zeros((n, n), dtype=np.float64)
    block_j = np.array([[0.0, 1.0], [-1.0, 0.0]])
    for k, omega in enumerate(frequencies):
        canonical[2 * k : 2 * k + 2, 2 * k : 2 * k + 2] = omega * block_j
    return generator, q, canonical


class UniformPathTorusBasisTests(unittest.TestCase):
    def test_explicit_basis_is_orthogonal(self):
        _, q, _ = uniform_path_matrices()
        defect = np.max(np.abs(q.T @ q - np.eye(42)))
        self.assertLess(defect, 1e-12)

    def test_explicit_basis_has_the_claimed_skew_canonical_form(self):
        generator, q, canonical = uniform_path_matrices()
        defect = np.max(np.abs(q.T @ generator @ q - canonical))
        self.assertLess(defect, 1e-12)

    def test_basis_orientation_is_special_orthogonal(self):
        _, q, _ = uniform_path_matrices()
        self.assertLess(abs(np.linalg.det(q) - 1.0), 1e-12)


if __name__ == "__main__":
    unittest.main()
