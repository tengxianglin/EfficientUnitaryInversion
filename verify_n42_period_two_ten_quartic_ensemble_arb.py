"""256-bit Arb certificate for the N=42 period-two ten-quartic partial design.

The frozen 41 base atoms are symmetrized with their one-site translates.  The
verifier reconstructs the exact-real weights from exact-rational decimal
couplings, checks all 861 pair minors, and checks every distinct translate of
ten specified fourth-order witnesses.  It does not claim a full quartic design.
"""
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

from flint import arb, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/n42_period_two_ten_quartic_atoms.json"
OUTPUT = ROOT / "evidence/n42_period_two_ten_quartic_ensemble_arb.json"


def rational(value):
    q = Fraction(value)
    return arb(fmpq(q.numerator, q.denominator))


def build_tables(n):
    two_pi = 2 * arb.pi()
    cosine, sine = [], []
    for k in range(n):
        rc, rs = [], []
        for d in range(n):
            angle = two_pi * (k * d) / n
            rc.append(angle.cos())
            rs.append(angle.sin())
        cosine.append(rc)
        sine.append(rs)
    return cosine, sine


def build_atom(atom, n, cosine, sine):
    a, b = rational(atom["a"]), rational(atom["b"])
    if not (a > 0 and b > 0):
        raise AssertionError("all cycle couplings must be strictly positive")

    c_symbol, sinc_symbol = [], []
    for k in range(n):
        ck, sk = cosine[k][1], sine[k][1]
        mu_sq = 4 * (a * a + b * b - 2 * a * b * ck)
        if not (mu_sq > 0):
            raise AssertionError(f"nonpositive Fourier singular value at mode {k}")
        mu = mu_sq.sqrt()
        cm, sm = mu.cos(), mu.sin()
        if not (cm * cm + sm * sm).contains(1):
            raise AssertionError("Fourier-mode trigonometric identity failed")
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

    x = C[0]
    same = [x * x - C[d] * C[d] for d in range(1, n // 2 + 1)]
    cross = [-x * x - S[d] * S[d] for d in range(n)]
    row_norm = x * x + 2 * sum((C[d] * C[d] for d in range(1, n // 2 + 1)), arb(0))
    row_norm += sum((S[d] * S[d] for d in range(n)), arb(0))
    if not (row_norm - 1).contains(0):
        raise AssertionError("period-two Fourier blocks failed the row-norm identity")
    identity = 2 * sum(same, arb(0)) + sum(cross, arb(0))
    if not (identity + 1).contains(0):
        raise AssertionError("pair-feature identity failed")

    return {"C": C, "S": S, "features": same + cross}


def q_entry(i, j, item, n):
    C, S = item["C"], item["S"]
    if i % 2 == 0 and j % 2 == 0:
        return C[(j // 2 - i // 2) % n]
    if i % 2 == 1 and j % 2 == 1:
        return -C[(j // 2 - i // 2) % n]
    if i % 2 == 0 and j % 2 == 1:
        return -S[(j // 2 - i // 2) % n]
    return -S[(i // 2 - j // 2) % n]


def principal_minor(indices, item, n):
    M = arb_mat([
        [q_entry(i, j, item, n) for j in indices]
        for i in indices
    ])
    return M.det()


def pair_feature_index(i, j, n):
    if i % 2 == j % 2:
        d = (j // 2 - i // 2) % n
        d = min(d, n - d)
        if not (1 <= d <= n // 2):
            raise AssertionError("bad same-parity displacement")
        return d - 1
    even = i if i % 2 == 0 else j
    odd = j if i % 2 == 0 else i
    return n // 2 + ((odd // 2 - even // 2) % n)


def symmetrized_quartic_moment(indices, base, shifted, weights, n):
    total = arb(0)
    for j in range(len(base)):
        v0 = principal_minor(indices, base[j], n)
        v1 = principal_minor(indices, shifted[j], n)
        total += weights[j, 0] * (v0 + v1) / 2
    return total


def symmetrized_pair_moment(indices, base, shifted, weights, n):
    total = arb(0)
    for j in range(len(base)):
        v0 = principal_minor(indices, base[j], n)
        v1 = principal_minor(indices, shifted[j], n)
        total += weights[j, 0] * (v0 + v1) / 2
    return total


def verify():
    data = json.loads(INPUT.read_text())
    n, N = data["n"], data["N"]
    ctx.prec = data["precision_bits"]
    assert (n, N) == (21, 42)

    atoms = data["atoms"]
    m = len(atoms)
    assert m == 41
    assert len({(a["a"], a["b"]) for a in atoms}) == m
    assert all(Fraction(a["a"]) > 0 and Fraction(a["b"]) > 0 for a in atoms)

    cosine, sine = build_tables(n)
    base = [build_atom(atom, n, cosine, sine) for atom in atoms]
    shifted_atoms = [{"a": atom["b"], "b": atom["a"]} for atom in atoms]
    shifted = [build_atom(atom, n, cosine, sine) for atom in shifted_atoms]

    pair_target = rational("-1/41")
    quartic_target = rational(Fraction(comb(n, 2), comb(N, 4)))
    if not (quartic_target - rational("1/533")).contains(0):
        raise AssertionError("balanced quartic target is not 1/533")

    # Thirty independent pair equations: ten same-parity and twenty cross-parity.
    # The omitted 21st cross equation follows from the exact row-norm identity.
    selected_pair_features = list(range(30))
    matched = [list(map(int, I)) for I in data["matched_quartic_witnesses"]]
    assert len(matched) == 10

    matrix_rows = [
        [base[j]["features"][i] for j in range(m)]
        for i in selected_pair_features
    ]
    for I in matched:
        matrix_rows.append([
            (
                principal_minor(I, base[j], n)
                + principal_minor(I, shifted[j], n)
            ) / 2
            for j in range(m)
        ])
    matrix_rows.append([arb(1) for _ in range(m)])

    A = arb_mat(matrix_rows)
    rhs = arb_mat(
        [[pair_target] for _ in selected_pair_features]
        + [[quartic_target] for _ in matched]
        + [[arb(1)]]
    )
    determinant = A.det()
    if determinant.contains(0):
        raise AssertionError("41x41 moment matrix is not certified invertible")

    weights = A.solve(rhs)
    floor = rational(data["weight_floor"])
    if not all(weights[j, 0] > floor for j in range(m)):
        raise AssertionError("strict positive weight floor was not certified")
    weight_sum = sum((weights[j, 0] for j in range(m)), arb(0))
    if not weight_sum.contains(1):
        raise AssertionError("weights do not sum to one")
    residual = A * weights - rhs
    if not all(residual[i, 0].contains(0) for i in range(m)):
        raise AssertionError("selected exact-real moment equations failed")

    # Verify every unordered pair in the explicit 50/50 one-site symmetrization.
    pair_count = 0
    for i, j in combinations(range(N), 2):
        value = symmetrized_pair_moment([i, j], base, shifted, weights, n)
        if not (value - pair_target).contains(0):
            raise AssertionError(f"symmetrized pair ({i},{j}) misses target: {value}")
        pair_count += 1
    assert pair_count == comb(N, 2) == 861

    # The one-site symmetrization joins the two parity-related translation orbits.
    # Check every distinct translate, not just the ten representatives.
    all_quartets = set()
    orbit_records = []
    quartic_checks = 0
    for I in matched:
        orbit = {
            tuple(sorted((i + shift) % N for i in I))
            for shift in range(N)
        }
        all_quartets.update(orbit)
        values = []
        for J in sorted(orbit):
            value = symmetrized_quartic_moment(list(J), base, shifted, weights, n)
            if not (value - quartic_target).contains(0):
                raise AssertionError(f"quartic translate {J} misses target: {value}")
            values.append(value)
            quartic_checks += 1
        orbit_records.append({
            "representative": I,
            "distinct_full_translation_count": len(orbit),
            "first_moment": str(values[0]),
            "last_moment": str(values[-1]),
        })

    assert quartic_checks == len(all_quartets) == 399

    # Candidate-specific eleventh-orbit miss: this does not exclude other
    # period-two mixtures or the full continuous physical family.
    unmatched_witness = [0, 6, 15, 21]
    unmatched_orbit = sorted({
        tuple(sorted((i + shift) % N for i in unmatched_witness))
        for shift in range(N)
    })
    if len(unmatched_orbit) != 42:
        raise AssertionError("unexpected orbit size for the next unmatched witness")
    if not set(unmatched_orbit).isdisjoint(all_quartets):
        raise AssertionError("unmatched witness overlaps a matched quartic orbit")
    unmatched_floor = rational("1/250")
    unmatched_values = []
    for J in unmatched_orbit:
        value = symmetrized_quartic_moment(list(J), base, shifted, weights, n)
        if not (value - quartic_target > unmatched_floor):
            raise AssertionError(
                f"candidate-specific unmatched quartic residual is not >1/250: {J}: {value}"
            )
        unmatched_values.append(value)

    min_index = min(range(m), key=lambda j: float(weights[j, 0]))
    max_index = max(range(m), key=lambda j: float(weights[j, 0]))
    min_coupling = min(
        Fraction(atom[key])
        for atom in atoms
        for key in ("a", "b")
    )

    result = {
        "status": "certified_N42_period_two_ten_quartic_orbit_ensemble",
        "complete": False,
        "certificate_complete": True,
        "design_complete": False,
        "N": N,
        "base_atom_count": m,
        "expanded_atom_count_after_one_site_symmetrization": 2 * m,
        "all_42_couplings_strictly_positive": True,
        "minimum_exact_coupling": str(min_coupling),
        "precision_bits": ctx.prec,
        "moment_matrix_determinant": str(determinant),
        "weight_floor_exact": data["weight_floor"],
        "minimum_weight": str(weights[min_index, 0]),
        "minimum_weight_atom_index": min_index,
        "maximum_weight": str(weights[max_index, 0]),
        "weight_sum": str(weight_sum),
        "weights": [str(weights[j, 0]) for j in range(m)],
        "pair_target_Q": "-1/41",
        "all_unordered_pair_coordinates_certified": pair_count,
        "quartic_target": str(quartic_target),
        "matched_quartic_orbits": orbit_records,
        "distinct_matched_quartic_coordinates": quartic_checks,
        "next_unmatched_quartic_witness": {
            "representative": unmatched_witness,
            "distinct_full_translation_count": len(unmatched_orbit),
            "translation_checks": len(unmatched_values),
            "target": str(quartic_target),
            "strict_residual_lower_bound": "1/250",
            "first_moment": str(unmatched_values[0]),
            "last_moment": str(unmatched_values[-1]),
            "scope": "This frozen 41-base-atom ensemble fails this additional orbit; it does not exclude other physical ensembles."
        },
        "one_site_symmetrization": "Each base atom (a,b) and its translate (b,a) receive equal half weight.",
        "scope": (
            "Exact positive ensemble for all 861 pair coordinates and 399 distinct "
            "fourth-order principal-minor coordinates belonging to ten specified "
            "full translation orbits. This is not a full fourth-order or all-even-moment design."
        ),
        "discovery": data["discovery"],
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "base_atoms": m,
        "expanded_atoms": 2 * m,
        "determinant": result["moment_matrix_determinant"],
        "minimum_weight": result["minimum_weight"],
        "weight_floor": result["weight_floor_exact"],
        "minimum_coupling": result["minimum_exact_coupling"],
        "pair_coordinates": pair_count,
        "quartic_coordinates": quartic_checks,
        "unmatched_witness_translates": len(unmatched_values),
        "unmatched_witness_strict_lower_bound": "1/250",
        "quartic_target": result["quartic_target"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    verify()
