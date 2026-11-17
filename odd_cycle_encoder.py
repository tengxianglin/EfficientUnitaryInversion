"""Generate and verify the fixed three-register odd-cycle encoder.

Wire order is A, B, C, with n wires per register. The gate list uses the
Hadamard-rotated physical basis and accepts initial B=C=0. A Givens gate
acts on |10>,|01> by the real rotation with the listed cosine and sine.
"""

from collections import Counter, defaultdict
from math import sqrt


def encoder_gates(n):
    """Yield (name, wires, parameters) in execution order."""
    if n < 3 or n % 2 == 0:
        raise ValueError("n must be odd and at least three")

    a, b, c = [tuple(range(r * n, (r + 1) * n)) for r in range(3)]
    last = n - 1
    type_wire = c[last]
    scan = [("CX", (b[i + 1], b[i]), ()) for i in reversed(range(last))]

    def fixed_phase(target):
        # z_C is 1 on even sites. The scan gives the bits [i < j].
        for i in range(0, n, 2):
            yield "Z", (target[i],), ()
        yield from scan
        for i in range(last):
            yield "CZ", (b[i + 1], target[i]), ()
        yield from reversed(scan)

    yield "X", (b[0],), ()
    for j in range(last):
        remaining = n - j
        yield "GIVENS", (b[j], b[j + 1]), (
            1 / sqrt(remaining), sqrt((remaining - 1) / remaining)
        )

    yield "H", (type_wire,), ()
    yield "Z", (type_wire,), ()
    yield from fixed_phase(a)
    for j in range(n):
        yield "CCZ", (type_wire, b[j], a[j]), ()

    # The last-site Fourier character contributes (-1)^(type * parity).
    for i in range(last):
        yield "CX", (a[i], a[last]), ()
    yield "CCZ", (type_wire, b[last], a[last]), ()
    for i in reversed(range(last)):
        yield "CX", (a[i], a[last]), ()

    for j in range(n):
        yield "X", (a[j],), ()
        yield "CX", (b[j], a[j]), ()

    # Move the type bit to the Fourier label on C[:last] and erase it.
    for i in range(last):
        yield "CCX", (type_wire, b[i], c[i]), ()
        yield "CCX", (type_wire, b[last], c[i]), ()
    for i in range(last):
        yield "CCX", (b[i], c[i], type_wire), ()
    yield "CCX", (b[last], c[0], type_wire), ()

    for i in range(last):
        yield "H", (c[i],), ()
        yield "CX", (c[i], c[last]), ()
    for i in range(n):
        yield "CX", (a[i], c[last]), ()
    yield from fixed_phase(c)

    for i in range(n):
        yield "X", (b[i],), ()
        yield "CX", (c[i], b[i]), ()


def apply_gate(state, gate):
    """Apply one listed gate to a sparse basis-state dictionary."""
    name, wires, parameters = gate
    masks = tuple(1 << wire for wire in wires)
    out = defaultdict(complex)
    for index, amplitude in state.items():
        if name == "H":
            mask = masks[0]
            low = index & ~mask
            out[low] += amplitude / sqrt(2)
            out[low | mask] += amplitude * (-1 if index & mask else 1) / sqrt(2)
        elif name == "GIVENS":
            left, right = masks
            if bool(index & left) == bool(index & right):
                out[index] += amplitude
            else:
                cosine, sine = parameters
                out[index] += cosine * amplitude
                out[index ^ left ^ right] += sine * amplitude * (1 if index & left else -1)
        elif name in {"Z", "CZ", "CCZ"}:
            phase = -1 if all(index & mask for mask in masks) else 1
            out[index] += phase * amplitude
        elif all(index & mask for mask in masks[:-1]):
            out[index ^ masks[-1]] += amplitude
        else:
            out[index] += amplitude
    return out


def majorana(index, j, kind):
    """Action of a Majorana after the sitewise Hadamard change of basis."""
    phase = (-1) ** (index & ((1 << j) - 1)).bit_count()
    if kind:
        phase *= -1j if not index & (1 << j) else 1j  # -Y
    return index ^ (1 << j), phase


def direct_column(x, n):
    """Independently evaluate the sum of Majorana tensor products."""
    def transformed(index, j, kind):
        phase = 1
        # C is ordered b_0 ... b_(n-1), so the rightmost acts first.
        for k in reversed(range(n)):
            index, local = majorana(index, k, 1)
            phase *= local
        index, local = majorana(index, j, kind)
        return index, phase * local

    norm = sqrt(2 * n * 2 ** (n - 1))
    column = defaultdict(complex)
    for j in range(n):
        for kind in (0, 1):
            a, alpha = transformed(x, j, kind)
            for y in range(1 << n):
                if (x.bit_count() - y.bit_count()) % 2 == 0:
                    b, beta = transformed(y, j, kind)
                    index = a | (b << n) | (y << (2 * n))
                    column[index] -= alpha * beta / norm  # fixed global phase
    return column


def verify(n):
    gates = list(encoder_gates(n))
    counts = Counter(name for name, _, _ in gates)
    assert counts["CX"] == 10 * n - 7
    assert counts["CZ"] == 2 * n - 2
    assert counts["CCX"] == 3 * n - 2
    assert counts["CCZ"] == n + 1
    assert counts["GIVENS"] == n - 1
    for x in range(1 << n):
        actual = {x: 1}
        for gate in gates:
            actual = apply_gate(actual, gate)
        expected = direct_column(x, n)
        error = max(abs(actual.get(k, 0) - expected.get(k, 0)) for k in actual.keys() | expected.keys())
        assert error < 1e-12, (n, x, error)
    print(f"L={n}: all {1 << n} encoder columns verified, CNOT upper bound {40*n-19}")


if __name__ == "__main__":
    for size in (3, 5, 7):
        verify(size)
