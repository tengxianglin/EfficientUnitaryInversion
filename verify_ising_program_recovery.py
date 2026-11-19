"""Check physical syndrome recovery in a valid three-site coherent encoder.

p=0.6 is a valid encoder mixture at this size. Its linear drift need not
vanish. The check verifies that the added recovery preserves that derivative
and compares full correction with the optional selective correction rule.
"""

import argparse
from itertools import product

import numpy as np
from scipy.linalg import expm

D = 4
IDENTITY = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])
PAULIS = [np.kron(a, b) for a, b in product((IDENTITY, X, Y, Z), repeat=2)]
PARITY_BASIS = (0, 3, 5, 6)
MIXTURE = 0.6


def projector():
    majoranas = []
    for site in range(3):
        for local in (X, -Y):
            matrix = np.ones((1, 1))
            for j in range(3):
                factor = Z if j < site else local if j == site else IDENTITY
                matrix = np.kron(matrix, factor)
            majoranas.append(matrix)
    charge_conjugation = majoranas[1] @ majoranas[3] @ majoranas[5]
    sector = np.ix_(PARITY_BASIS, PARITY_BASIS)
    columns = np.column_stack([
        (g @ charge_conjugation)[sector].conj().reshape(-1)/np.sqrt(D)
        for g in majoranas
    ])
    return columns @ columns.conj().T


Q = projector()
PROTECTED = {
    i for i, pauli in enumerate(PAULIS) if np.array_equal(pauli, pauli.T)
}
BELL = [pauli.reshape(D, D)/np.sqrt(D) for pauli in PAULIS]


def kraus(hamiltonian, epsilon, corrected, selective=False):
    target = expm(1j*hamiltonian)
    a = np.exp(-6j*epsilon)
    b = np.exp(2j*epsilon)-a
    amplitudes = (
        a*np.eye(D*D)+MIXTURE*b*Q,
        np.sqrt(MIXTURE*(1-MIXTURE))*b*Q,
    )
    result = []
    for flag, amplitude in enumerate(amplitudes):
        joint = (np.kron(target, target) @ amplitude).reshape(D, D, D, D)
        for label, pauli in enumerate(PAULIS):
            matrix = np.einsum("er,aeir->ai", BELL[label].conj(), joint)/np.sqrt(D)
            if corrected and (
                (flag == 0 and label not in PROTECTED)
                or (flag == 1 and not selective)
            ):
                matrix = pauli.conj().T @ matrix
            result.append(matrix)
    return result


def choi(hamiltonian, epsilon, corrected, selective=False):
    return sum(
        np.outer(matrix.reshape(-1), matrix.reshape(-1).conj())/D
        for matrix in kraus(hamiltonian, epsilon, corrected, selective)
    )


def verify(selective=False):
    rng = np.random.default_rng(20261119)
    ratios = []
    for sample in range(10):
        fields, edges = rng.normal(size=(2, 3))
        hamiltonian = np.diag([
            sum(fields[k]*(-1)**((row >> k) & 1) for k in range(3))
            for row in PARITY_BASIS
        ]).astype(complex)
        for column, row in enumerate(PARITY_BASIS):
            for k in range(3):
                flipped = row ^ (1 << k) ^ (1 << ((k+1) % 3))
                hamiltonian[PARITY_BASIS.index(flipped), column] += edges[k]
        for corrected in (False, True):
            operators = kraus(hamiltonian, 0.013, corrected, selective)
            np.testing.assert_allclose(
                sum(k.conj().T @ k for k in operators), np.eye(D), atol=1e-12
            )
        np.testing.assert_allclose(
            choi(hamiltonian, 0, False, selective), choi(hamiltonian, 0, True, selective), atol=1e-12
        )
        step = 1e-5
        derivative_change = (
            choi(hamiltonian, step, True, selective)-choi(hamiltonian, -step, True, selective)
            -choi(hamiltonian, step, False)+choi(hamiltonian, -step, False)
        )/(2*step)
        assert np.linalg.norm(derivative_change) < 1e-7
        target = expm(1j*hamiltonian).reshape(-1)/np.sqrt(D)
        infidelities = []
        for corrected in (False, True):
            infidelity = 1-np.vdot(
                target, choi(hamiltonian, 0.001, corrected, selective) @ target
            ).real
            infidelities.append(infidelity)
        ratio = infidelities[1]/infidelities[0]
        ratios.append(ratio)
        print(sample, "new/old entanglement infidelity", f"{ratio:.9f}")
    if selective:
        assert max(ratios) <= 1+1e-8
        print("Selective correction passed exactness and derivative checks; sampled infidelity decreased.")
    else:
        assert min(ratios) > 1
        print("All ideal and derivative checks passed; nonzero-H infidelity can increase.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selective", action="store_true",
                        help="correct only ideal-flag syndromes outside the physical program span")
    args = parser.parse_args()
    verify(args.selective)
