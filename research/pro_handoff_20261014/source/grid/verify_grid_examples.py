#!/usr/bin/env python3
"""Exact, CPU-only checks for a small set of 3-qubit Pauli grids.

The grid rule is checked in the phase-free Pauli group (bitwise XOR).  The
envelope calculation keeps Gaussian-integer coefficients, so cancellations in
H(alpha)^k are not hidden by numerical sampling.  The transpose lambda values
are exact for the examples included here: saturated envelopes use Walsh
inversion; a partial envelope is accepted only when an explicit one-Pauli
transpose witness is found.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence


N = 3
MASK = (1 << N) - 1
PAULI_BITS = {"I": (0, 0), "X": (1, 0), "Y": (1, 1), "Z": (0, 1)}
BITS_PAULI = {value: key for key, value in PAULI_BITS.items()}
ALL_VECTORS = tuple(range(1 << (2 * N)))


EXAMPLES = (
    {
        "name": "custom_S1",
        "role": "target_grid",
        "notes": "Historical custom support used with the original 4U^T formula; that formula is not admitted.",
        "grid": [
            ["XXI", "IYX", "XZX"],
            ["ZZI", "YII", "XZI"],
            ["YYI", "YYX", "IIX"],
        ],
    },
    {
        "name": "new_structure_grid",
        "role": "target_grid",
        "notes": "Later structure-preserving grid; its separate 16-term transpose identity was independently checked.",
        "grid": [
            ["XXI", "IYX", "XZX"],
            ["ZZZ", "XXY", "YYX"],
            ["YYZ", "XZZ", "ZXI"],
        ],
    },
    {
        "name": "S2_frozen",
        "role": "target_grid",
        "notes": "Formal frozen S2; official project target is dagger, while transpose is a control here.",
        "grid": [
            ["XXI", "YYI", "ZZI"],
            ["IXX", "IYY", "IZZ"],
            ["XIX", "YIY", "ZIZ"],
        ],
    },
    {
        "name": "S2_same_W_saturated",
        "role": "target_grid",
        "notes": "Matched grid in the same phase-free W as S2_frozen, but with a saturated transpose envelope.",
        "grid": [
            ["XXI", "YYI", "ZZI"],
            ["ZIZ", "XIX", "YIY"],
            ["YXZ", "ZYX", "XZY"],
        ],
    },
    {
        "name": "same_W_q4_partial",
        "role": "matched_pair",
        "notes": "Same W and coarse q/commutation counts as same_W_q4_saturated; partial envelope with a one-Pauli witness.",
        "grid": [
            ["ZIZ", "ZZI", "IZZ"],
            ["XIX", "YXZ", "ZXY"],
            ["YIY", "XYZ", "ZYX"],
        ],
    },
    {
        "name": "same_W_q4_saturated",
        "role": "matched_pair",
        "notes": "Matched to same_W_q4_partial: same W, m, symplectic rank, q-odd count, and anti-edge count, but saturated envelope.",
        "grid": [
            ["ZIZ", "ZZI", "IZZ"],
            ["YZX", "ZYX", "XXI"],
            ["XZY", "IXX", "XYZ"],
        ],
    },
    {
        "name": "frozen_S1_control",
        "role": "control_not_full_grid",
        "notes": "The current configs/s1_transpose.json support; its three rows satisfy the rule, but not all columns.",
        "grid": [
            ["XXI", "IYX", "XZX"],
            ["ZZI", "IIZ", "ZZZ"],
            ["XYI", "IYY", "XIY"],
        ],
    },
    {
        "name": "row_only_full_M8",
        "role": "control_not_full_grid",
        "notes": "Row-only full-M8 counterexample; included to show why the column condition matters.",
        "grid": [
            ["IXZ", "YZI", "YYZ"],
            ["YYI", "IZY", "YXY"],
            ["XXI", "IXX", "XIX"],
        ],
    },
)


def tag_to_vector(tag: str) -> int:
    if len(tag) != N or any(char not in PAULI_BITS for char in tag):
        raise ValueError(f"expected a {N}-qubit I/X/Y/Z tag, got {tag!r}")
    x = sum(PAULI_BITS[char][0] << i for i, char in enumerate(tag))
    z = sum(PAULI_BITS[char][1] << i for i, char in enumerate(tag))
    return x | (z << N)


def vector_to_tag(value: int) -> str:
    x, z = value & MASK, (value >> N) & MASK
    return "".join(BITS_PAULI[((x >> i) & 1, (z >> i) & 1)] for i in range(N))


def gf2_basis(vectors: Iterable[int]) -> tuple[int, ...]:
    pivots: dict[int, int] = {}
    for value in vectors:
        reduced = value
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))


def gf2_span(basis: Sequence[int]) -> list[int]:
    out = [0]
    for value in basis:
        out += [item ^ value for item in out]
    return out


def coordinate(value: int, basis: Sequence[int]) -> int:
    for mask in range(1 << len(basis)):
        candidate = 0
        for index, vector in enumerate(basis):
            if (mask >> index) & 1:
                candidate ^= vector
        if candidate == value:
            return mask
    raise ValueError(f"vector {value} is outside the supplied basis span")


def symplectic(left: int, right: int) -> int:
    lx, lz = left & MASK, (left >> N) & MASK
    rx, rz = right & MASK, (right >> N) & MASK
    return ((lx & rz).bit_count() + (lz & rx).bit_count()) & 1


def qform(value: int) -> int:
    x, z = value & MASK, (value >> N) & MASK
    return (x & z).bit_count() & 1


def rank_of_rows(rows: Iterable[int]) -> int:
    return len(gf2_basis(rows))


def gram_rows(basis: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        sum(symplectic(left, right) << index for index, right in enumerate(basis))
        for left in basis
    )


def phase_free_product(left: int, right: int) -> int:
    return left ^ right


def pauli_product_phase(left: int, right: int) -> tuple[int, int]:
    """Return e,w with P(left)P(right)=i**e P(w), e in Z4."""
    lx, lz = left & MASK, (left >> N) & MASK
    rx, rz = right & MASK, (right >> N) & MASK
    w = left ^ right
    wx, wz = w & MASK, (w >> N) & MASK
    exponent = (
        (lx & lz).bit_count()
        + (rx & rz).bit_count()
        + 2 * (lz & rx).bit_count()
        - (wx & wz).bit_count()
    ) % 4
    return exponent, w


def add_gaussian(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def multiply_by_i(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    a, b = value
    return ((a, b), (-b, a), (-a, -b), (b, -a))[exponent % 4]


def envelope_support(generators: Sequence[int]) -> tuple[set[int], list[int]]:
    """Compute exact coordinate support of powers H^k, cumulatively."""
    number = len(generators)
    polynomial: dict[tuple[int, ...], dict[int, tuple[int, int]]] = {
        (0,) * number: {0: (1, 0)}
    }
    support: set[int] = set()
    counts: list[int] = []
    for degree in range(1 << N):
        for terms in polynomial.values():
            support.update(label for label, coefficient in terms.items() if coefficient != (0, 0))
        counts.append(len(support))
        if degree == (1 << N) - 1:
            break
        next_polynomial: dict[tuple[int, ...], dict[int, tuple[int, int]]] = {}
        for exponents, terms in polynomial.items():
            for index, generator in enumerate(generators):
                next_exponents = list(exponents)
                next_exponents[index] += 1
                output = next_polynomial.setdefault(tuple(next_exponents), {})
                for label, coefficient in terms.items():
                    phase, product = pauli_product_phase(label, generator)
                    contribution = multiply_by_i(coefficient, phase)
                    output[product] = add_gaussian(output.get(product, (0, 0)), contribution)
        polynomial = {
            exponents: {
                label: coefficient
                for label, coefficient in terms.items()
                if coefficient != (0, 0)
            }
            for exponents, terms in next_polynomial.items()
        }
    return support, counts


def line_checks(tags: Sequence[str]) -> tuple[list[dict], list[dict]]:
    vectors = [tag_to_vector(tag) for tag in tags]

    def check(left_index: int, right_index: int, target_index: int) -> dict:
        phase, product = pauli_product_phase(vectors[left_index], vectors[right_index])
        return {
            "left": tags[left_index],
            "right": tags[right_index],
            "third": tags[target_index],
            "phase_free_product": vector_to_tag(product),
            "phase_exponent_i": phase,
            "pass": product == vectors[target_index],
        }

    rows = [check(i, i + 1, i + 2) for i in (0, 3, 6)]
    columns = [check(j, 3 + j, 6 + j) for j in range(3)]
    return rows, columns


def all_pair_checks(tags: Sequence[str]) -> list[dict]:
    """Check all three unordered pairs in every row and column."""
    vectors = [tag_to_vector(tag) for tag in tags]
    lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
    ]
    checks = []
    for line in lines:
        for left, right, target in (
            (line[0], line[1], line[2]),
            (line[0], line[2], line[1]),
            (line[1], line[2], line[0]),
        ):
            _, product = pauli_product_phase(vectors[left], vectors[right])
            checks.append(
                {
                    "left": tags[left],
                    "right": tags[right],
                    "third": tags[target],
                    "phase_free_product": vector_to_tag(product),
                    "pass": product == vectors[target],
                }
            )
    return checks


def transpose_data(generators: Sequence[int], support: set[int]) -> dict:
    basis = gf2_basis(generators)
    span = gf2_span(basis)
    m = len(basis)
    target_values = {
        coordinate(value, basis): (1 if qform(value) == 0 else -1)
        for value in support
    }

    if len(support) == len(span):
        numerators = []
        for ell in range(1 << m):
            numerator = sum(
                (1 if qform(value) == 0 else -1)
                * (-1 if (ell & coordinate(value, basis)).bit_count() & 1 else 1)
                for value in span
            )
            numerators.append(numerator)
        nonzero = [value for value in numerators if value]
        denominator = 1 << m
        l1_numerator = sum(abs(value) for value in numerators)
        if l1_numerator % denominator:
            raise AssertionError("Walsh L1 norm was not integral for a saturated example")
        lam = l1_numerator // denominator
        return {
            "method": "exact Walsh inversion on saturated envelope",
            "lambda": lam,
            "branch_count": len(nonzero),
            "coefficient_numerators_over_2^m": numerators,
            "postselection_probability": f"1/{lam * lam}",
        }

    witnesses = []
    for sigma in ALL_VECTORS:
        if all(
            (-1 if symplectic(sigma, value) else 1) == target
            for value, target in ((value, target_values[coordinate(value, basis)]) for value in support)
        ):
            witnesses.append(vector_to_tag(sigma))
    if not witnesses:
        return {"method": "no exact small-scope certificate in this script", "lambda": None}
    return {
        "method": "explicit one-Pauli transpose witness on partial envelope",
        "lambda": 1,
        "branch_count": 1,
        "witnesses": witnesses,
        "postselection_probability": "1",
    }


def analyze(example: dict) -> dict:
    grid = example["grid"]
    if len(grid) != 3 or any(len(row) != 3 for row in grid):
        raise ValueError(f"{example['name']} is not a 3x3 grid")
    tags = [tag for row in grid for tag in row]
    vectors = [tag_to_vector(tag) for tag in tags]
    basis = gf2_basis(vectors)
    span = set(gf2_span(basis))
    rows, columns = line_checks(tags)
    pair_checks = all_pair_checks(tags)
    envelope, envelope_counts = envelope_support(vectors)
    gram = gram_rows(basis)
    radical = [
        value
        for value in span
        if all(symplectic(value, basis_vector) == 0 for basis_vector in basis)
    ]
    result = {
        "name": example["name"],
        "role": example["role"],
        "notes": example["notes"],
        "grid": grid,
        "ordered_tags": tags,
        "support_hash": hashlib.sha256(
            json.dumps(tags, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "all_nine_distinct_nonidentity": len(set(vectors)) == 9 and 0 not in vectors,
        "row_checks": rows,
        "column_checks": columns,
        "all_three_pairs_per_line_pass": all(item["pass"] for item in pair_checks),
        "full_row_column_rule": all(item["pass"] for item in pair_checks),
        "gf2_rank": len(basis),
        "symplectic_rank": rank_of_rows(gram),
        "radical_dimension": len(radical),
        "radical": sorted(vector_to_tag(value) for value in radical),
        "commutant_phase_free_size": 1 << (2 * N - len(basis)),
        "pairwise_anticommuting_pairs": sum(
            symplectic(left, right)
            for index, left in enumerate(vectors)
            for right in vectors[index + 1 :]
        ),
        "odd_y_count": sum(qform(value) for value in vectors),
        "envelope_coordinate_support_size": len(envelope),
        "envelope_coordinate_support_counts_by_degree": envelope_counts,
        "envelope_saturated": len(envelope) == len(span),
    }
    result["transpose_lcu"] = transpose_data(vectors, envelope)
    return result


def verify(results: Sequence[dict]) -> dict:
    by_name = {item["name"]: item for item in results}
    checks = {
        "four_target_grids_satisfy_all_six_line_checks": all(
            by_name[name]["full_row_column_rule"]
            for name in ("custom_S1", "new_structure_grid", "S2_frozen", "S2_same_W_saturated")
        ),
        "controls_do_not_claim_full_grid": all(
            not by_name[name]["all_three_pairs_per_line_pass"]
            for name in ("frozen_S1_control", "row_only_full_M8")
        ),
        "custom_has_rank_two_symplectic_form": (
            by_name["custom_S1"]["gf2_rank"] == 4
            and by_name["custom_S1"]["symplectic_rank"] == 2
        ),
        "new_grid_has_rank_four_symplectic_form": (
            by_name["new_structure_grid"]["gf2_rank"] == 4
            and by_name["new_structure_grid"]["symplectic_rank"] == 4
        ),
        "same_W_matched_pair": set(
            gf2_span(
                gf2_basis(
                    tag_to_vector(tag)
                    for tag in by_name["S2_frozen"]["ordered_tags"]
                )
            )
        )
        == set(
            gf2_span(
                gf2_basis(
                    tag_to_vector(tag)
                    for tag in by_name["S2_same_W_saturated"]["ordered_tags"]
                )
            )
        ),
        "matched_pair_has_different_envelopes": (
            by_name["S2_frozen"]["envelope_coordinate_support_size"] == 10
            and by_name["S2_same_W_saturated"]["envelope_coordinate_support_size"] == 16
        ),
        "matched_pair_has_different_exact_lambdas": (
            by_name["S2_frozen"]["transpose_lcu"]["lambda"] == 1
            and by_name["S2_same_W_saturated"]["transpose_lcu"]["lambda"] == 4
        ),
        "matched_q4_pair_has_same_coarse_counts": (
            set(
                gf2_span(
                    gf2_basis(
                        tag_to_vector(tag)
                        for tag in by_name["same_W_q4_partial"]["ordered_tags"]
                    )
                )
            )
            == set(
                gf2_span(
                    gf2_basis(
                        tag_to_vector(tag)
                        for tag in by_name["same_W_q4_saturated"]["ordered_tags"]
                    )
                )
            )
            and
            by_name["same_W_q4_partial"]["gf2_rank"]
            == by_name["same_W_q4_saturated"]["gf2_rank"] == 4
            and by_name["same_W_q4_partial"]["symplectic_rank"]
            == by_name["same_W_q4_saturated"]["symplectic_rank"] == 4
            and by_name["same_W_q4_partial"]["odd_y_count"]
            == by_name["same_W_q4_saturated"]["odd_y_count"] == 4
            and by_name["same_W_q4_partial"]["pairwise_anticommuting_pairs"]
            == by_name["same_W_q4_saturated"]["pairwise_anticommuting_pairs"] == 18
        ),
        "matched_q4_pair_has_different_envelope_and_lambda": (
            by_name["same_W_q4_partial"]["envelope_coordinate_support_size"] == 10
            and by_name["same_W_q4_saturated"]["envelope_coordinate_support_size"] == 16
            and by_name["same_W_q4_partial"]["transpose_lcu"]["lambda"] == 1
            and by_name["same_W_q4_saturated"]["transpose_lcu"]["lambda"] == 4
        ),
        "rank_two_and_rank_four_examples_have_expected_lambdas": (
            by_name["custom_S1"]["transpose_lcu"]["lambda"] == 2
            and by_name["new_structure_grid"]["transpose_lcu"]["lambda"] == 4
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError("failed checks: " + ", ".join(failed))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = [analyze(example) for example in EXAMPLES]
    checks = verify(results)
    payload = {
        "title": "Exact phase-free 3-qubit Pauli grid examples",
        "arithmetic": "GF(2) labels and Gaussian-integer polynomial coefficients; no random sampling",
        "scope": "eight hand-picked supports, including matched pairs inside one fixed W; not a full n=3 classification",
        "grid_rule": "P[i,0] XOR P[i,1] = P[i,2] and P[0,j] XOR P[1,j] = P[2,j]",
        "transpose_lcu_scope": "normalized Pauli-conjugation LCU only; lambda is not an arbitrary-comb lower bound",
        "verification": checks,
        "examples": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in results:
        lcu = item["transpose_lcu"]
        print(
            f"{item['name']}: grid={item['full_row_column_rule']} "
            f"m={item['gf2_rank']} srank={item['symplectic_rank']} "
            f"env={item['envelope_coordinate_support_size']} "
            f"lambda={lcu['lambda']}"
        )
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
