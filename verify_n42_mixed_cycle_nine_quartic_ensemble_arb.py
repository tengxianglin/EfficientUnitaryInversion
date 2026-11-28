#!/usr/bin/env python3
"""256-bit Arb certificate for a mixed period-two / fully nonperiodic N=42 ensemble.

Each seed is averaged over its 42 cyclic translates.  The verifier reconstructs
30 exact-real weights from 21 pair-distance moments and nine quartic-orbit
moments.  Four seeds have primitive period 42 and all 42 couplings positive.
"""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from flint import arb, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_mixed_cycle_nine_quartic_atoms.json"
OUTPUT = ROOT / "evidence/n42_mixed_cycle_nine_quartic_ensemble_arb.json"
N = 42
n = 21


def rational(value):
    q = Fraction(str(value))
    return arb(fmpq(q.numerator, q.denominator))


def exact_fraction(value):
    return Fraction(str(value))


def build_tables(size):
    two_pi = 2 * arb.pi()
    cosine, sine = [], []
    for k in range(size):
        row_c, row_s = [], []
        for d in range(size):
            angle = two_pi * (k * d) / size
            row_c.append(angle.cos())
            row_s.append(angle.sin())
        cosine.append(row_c)
        sine.append(row_s)
    return cosine, sine


def build_period_two_atom(atom, cosine, sine):
    a = rational(atom["a"])
    b = rational(atom["b"])
    if not (a > 0 and b > 0):
        raise AssertionError("period-two seed couplings must be strictly positive")

    c_symbol, sinc_symbol = [], []
    for k in range(n):
        ck, sk = cosine[k][1], sine[k][1]
        mu_sq = 4 * (a * a + b * b - 2 * a * b * ck)
        if not (mu_sq > 0):
            raise AssertionError("period-two Fourier singular value is not positive")
        mu = mu_sq.sqrt()
        cm, sm = mu.cos(), mu.sin()
        if not (cm * cm + sm * sm).contains(1):
            raise AssertionError("Fourier trigonometric identity failed")
        c_symbol.append(cm)
        sinc_symbol.append(sm / mu)

    C, S = [], []
    for d in range(n):
        cd, sd = arb(0), arb(0)
        for k in range(n):
            co, si = cosine[k][d], sine[k][d]
            cd += c_symbol[k] * co
            sd += 2 * sinc_symbol[k] * (
                (a - b * cosine[k][1]) * co + b * sine[k][1] * si
            )
        C.append(cd / n)
        S.append(sd / n)

    return {"kind": "period-two", "C": C, "S": S, "a": a, "b": b}


def build_general_atom(atom):
    couplings = [exact_fraction(x) for x in atom["couplings"]]
    if len(couplings) != N or any(x <= 0 for x in couplings):
        raise AssertionError("each nonperiodic seed needs 42 strictly positive couplings")

    A = arb_mat(N, N)
    for j, coupling in enumerate(couplings):
        k = (j + 1) % N
        edge = rational(str(2 * coupling))
        A[j, k] = edge
        A[k, j] = -edge

    R = A.exp()
    signs = [1 if j % 2 == 0 else -1 for j in range(N)]
    Q = arb_mat(N, N)
    for i in range(N):
        for j in range(N):
            Q[i, j] = R[i, j] * signs[j]

    # D A D = -A implies Q = exp(A)D is a symmetric involution.
    for i in range(N):
        for j in range(N):
            if not (Q[i, j] - Q[j, i]).contains(0):
                raise AssertionError(f"Q symmetry failed at ({i},{j})")
    Q2 = Q * Q
    for i in range(N):
        for j in range(N):
            target = arb(1 if i == j else 0)
            if not (Q2[i, j] - target).contains(0):
                raise AssertionError(f"Q involution failed at ({i},{j})")
    trace = sum((Q[i, i] for i in range(N)), arb(0))
    if not trace.contains(0):
        raise AssertionError("Q trace is not certified to be zero")

    return {"kind": "general", "Q": Q, "couplings": couplings}


def entry(atom, i, j):
    if atom["kind"] == "general":
        return atom["Q"][i, j]
    C, S = atom["C"], atom["S"]
    if i % 2 == 0 and j % 2 == 0:
        return C[(j // 2 - i // 2) % n]
    if i % 2 == 1 and j % 2 == 1:
        return -C[(j // 2 - i // 2) % n]
    if i % 2 == 0 and j % 2 == 1:
        return -S[(j // 2 - i // 2) % n]
    return -S[(i // 2 - j // 2) % n]


def pair_minor(atom, i, j):
    return entry(atom, i, i) * entry(atom, j, j) - entry(atom, i, j) * entry(atom, j, i)


def pair_distance_orbit(atom, distance):
    # There are 42 unordered pairs at distances 1,...,20 and 21 opposite pairs.
    shifts = range(21) if distance == 21 else range(42)
    total = sum((pair_minor(atom, s, (s + distance) % N) for s in shifts), arb(0))
    return total / len(shifts)


def principal_minor(atom, indices):
    return arb_mat([
        [entry(atom, i, j) for j in indices]
        for i in indices
    ]).det()


def quartic_translation_orbit(atom, indices):
    total = arb(0)
    for shift in range(N):
        translated = [((i + shift) % N) for i in indices]
        total += principal_minor(atom, translated)
    return total / N


def cyclic_orbit(values):
    values = [exact_fraction(x) for x in values]
    return {
        tuple(values[(j + shift) % N] for j in range(N))
        for shift in range(N)
    }


def minimal_period(values):
    values = [exact_fraction(x) for x in values]
    for period in range(1, N + 1):
        if N % period == 0 and all(
            values[j] == values[(j + period) % N] for j in range(N)
        ):
            return period
    raise AssertionError("a 42-cycle vector has no period dividing 42")


def translation_orbit(indices):
    return {
        tuple(sorted((i + shift) % N for i in indices))
        for shift in range(N)
    }


def verify():
    data = json.loads(INPUT.read_text())
    ctx.prec = data["precision_bits"]
    assert data["N"] == N and data["n"] == n

    old_seeds = data["old_period_two_atoms"]
    new_seeds = data["nonperiodic_atoms"]
    matched = [list(map(int, x)) for x in data["matched_quartic_witnesses"]]
    extras = [list(map(int, x)) for x in data["extra_quartic_witnesses"]]
    assert len(old_seeds) == 26 and len(new_seeds) == 4 and len(matched) == 9
    assert len(extras) == 2

    cosine, sine = build_tables(n)
    atoms = [build_period_two_atom(x, cosine, sine) for x in old_seeds]
    atoms += [build_general_atom(x) for x in new_seeds]

    # The 26 old seeds have two distinct cyclic translates; each new seed has 42.
    all_orbits = []
    periods = []
    minimum_coupling = None
    for seed in old_seeds:
        c = [seed["a"], seed["b"]] * n
        period = minimal_period(c)
        if period != 2:
            raise AssertionError("an old seed is not genuinely period two")
        periods.append(period)
        minimum_coupling = min(
            [exact_fraction(seed["a"]), exact_fraction(seed["b"])]
            if minimum_coupling is None
            else [minimum_coupling, exact_fraction(seed["a"]), exact_fraction(seed["b"])]
        )
        orbit = cyclic_orbit(c)
        if len(orbit) != 2:
            raise AssertionError("a period-two seed must have exactly two translates")
        all_orbits.append(orbit)

    for seed in new_seeds:
        c = seed["couplings"]
        period = minimal_period(c)
        if period != 42:
            raise AssertionError("a new seed is not primitive period 42")
        periods.append(period)
        minimum_coupling = min(
            [minimum_coupling] + [exact_fraction(x) for x in c]
        )
        orbit = cyclic_orbit(c)
        if len(orbit) != 42:
            raise AssertionError("a nonperiodic seed must have 42 distinct translates")
        all_orbits.append(orbit)

    seen = set()
    for orbit in all_orbits:
        if seen.intersection(orbit):
            raise AssertionError("two frozen seed orbits contain the same physical coupling")
        seen.update(orbit)
    unique_atom_count = len(seen)
    if unique_atom_count != 26 * 2 + 4 * 42:
        raise AssertionError("unexpected number of distinct physical atoms")
    if not (minimum_coupling > 0):
        raise AssertionError("the ensemble contains a nonpositive coupling")

    pair_columns = []
    quartic_columns = []
    extra_columns = []
    for atom in atoms:
        pair_values = [pair_distance_orbit(atom, d) for d in range(1, N // 2 + 1)]
        pair_identity = 2 * sum(pair_values[:20], arb(0)) + pair_values[20]
        if not (pair_identity + 1).contains(0):
            raise AssertionError("cyclic pair-orbit identity failed")
        pair_columns.append(pair_values)
        quartic_columns.append([quartic_translation_orbit(atom, I) for I in matched])
        extra_columns.append([quartic_translation_orbit(atom, I) for I in extras])

    # A 30x30 exact-real system: 21 cyclic pair-distance orbits + 9 quartic orbits.
    rows = []
    for d in range(21):
        rows.append([pair_columns[j][d] for j in range(len(atoms))])
    for r in range(9):
        rows.append([quartic_columns[j][r] for j in range(len(atoms))])
    M = arb_mat(rows)
    rhs = arb_mat(
        [[rational("-1/41")] for _ in range(21)]
        + [[rational("1/533")] for _ in range(9)]
    )
    determinant = M.det()
    if determinant.contains(0):
        raise AssertionError("the 30x30 mixed physical moment matrix is not certified invertible")
    weights = M.solve(rhs)

    floor = rational(data["weight_floor"])
    if not all(weights[j, 0] > floor for j in range(len(atoms))):
        raise AssertionError("a reconstructed exact-real weight is not above the strict floor")
    weight_sum = sum((weights[j, 0] for j in range(len(atoms))), arb(0))
    if not weight_sum.contains(1):
        raise AssertionError("pair identity did not certify normalized probability weights")

    pair_residuals = []
    for d in range(21):
        value = sum(
            (weights[j, 0] * pair_columns[j][d] for j in range(len(atoms))),
            arb(0),
        )
        residual = value - rational("-1/41")
        if not residual.contains(0):
            raise AssertionError(f"pair-distance orbit {d + 1} misses the target: {residual}")
        pair_residuals.append(str(residual))

    quartic_residuals = []
    for r in range(9):
        value = sum(
            (weights[j, 0] * quartic_columns[j][r] for j in range(len(atoms))),
            arb(0),
        )
        residual = value - rational("1/533")
        if not residual.contains(0):
            raise AssertionError(f"matched quartic orbit {matched[r]} misses the target: {residual}")
        quartic_residuals.append(str(residual))

    extra_records = []
    threshold_strings = ["1/500", "1/250"]
    thresholds = [rational(x) for x in threshold_strings]
    for r, witness in enumerate(extras):
        value = sum(
            (weights[j, 0] * extra_columns[j][r] for j in range(len(atoms))),
            arb(0),
        )
        residual = value - rational("1/533")
        if not (residual > thresholds[r]):
            raise AssertionError(
                f"extra quartic witness {witness} is not strictly above its claimed floor: {residual}"
            )
        extra_records.append({
            "representative": witness,
            "orbit_size": len(translation_orbit(witness)),
            "moment": str(value),
            "target": "1/533",
            "residual": str(residual),
            "strict_floor": threshold_strings[r],
        })

    matched_orbits = [translation_orbit(I) for I in matched]
    if len(set().union(*matched_orbits)) != 357:
        raise AssertionError("the nine matched quartic orbits do not cover 357 distinct subsets")
    if sum(len(x) for x in matched_orbits) != 357:
        raise AssertionError("matched quartic translation orbits overlap")
    if any(set(matched_orbits[i]).intersection(matched_orbits[j])
           for i in range(9) for j in range(i)):
        raise AssertionError("two matched quartic orbits overlap")

    nonperiodic_mass = sum(
        (weights[j, 0] for j in range(26, 30)), arb(0)
    )
    if not (nonperiodic_mass > rational(data["nonperiodic_mass_floor"])):
        raise AssertionError("the strictly nonperiodic mass is below its required floor")

    result = {
        "N": N,
        "status": "certified_positive_mixed_cycle_nine_quartic_partial_ensemble",
        "precision_bits": data["precision_bits"],
        "seed_count": len(atoms),
        "old_period_two_seed_count": 26,
        "new_primitive_period_42_seed_count": 4,
        "unique_physical_atom_count": unique_atom_count,
        "all_physical_cycle_couplings_strictly_positive": True,
        "minimum_coupling_exact": str(minimum_coupling),
        "minimum_weight": str(weights[min(range(len(atoms)), key=lambda j: float(weights[j, 0])), 0]),
        "weight_floor_exact": data["weight_floor"],
        "weight_sum": str(weight_sum),
        "nonperiodic_mass": str(nonperiodic_mass),
        "nonperiodic_mass_floor_exact": data["nonperiodic_mass_floor"],
        "pair_distance_orbits_certified": 21,
        "pair_coordinates_covered": 861,
        "pair_target_Q": "-1/41",
        "pair_residuals": pair_residuals,
        "matched_quartic_translation_orbits": 9,
        "matched_quartic_coordinates": 357,
        "quartic_target_Q": "1/533",
        "matched_quartic_residuals": quartic_residuals,
        "extra_quartic_witnesses": extra_records,
        "moment_matrix_determinant": str(determinant),
        "weights": [str(weights[j, 0]) for j in range(len(atoms))],
        "discovery": data["discovery"],
        "scope": (
            "Exact-real positive ensemble over 220 distinct strictly-positive cycle atoms. "
            "It matches all 861 pair coordinates and 357 quartic coordinates in nine "
            "specified cyclic translation orbits. The two additional quartic witnesses "
            "are strictly mismatched; no complete fourth-order or all-even-moment claim follows."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "determinant": result["moment_matrix_determinant"],
        "minimum_weight": result["minimum_weight"],
        "weight_sum": result["weight_sum"],
        "nonperiodic_mass": result["nonperiodic_mass"],
        "pair_coordinates": result["pair_coordinates_covered"],
        "quartic_coordinates": result["matched_quartic_coordinates"],
        "extra_witnesses": extra_records,
        "unique_physical_atoms": unique_atom_count,
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
