"""Exact commutant obstruction for one perfect-matching atom of the SO(42) ensemble."""
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/perfect_matching_atom_cycle_unreachable_n21.json"
PRIME = 65521
MATCHING_42 = [
    (0, 11), (1, 38), (2, 8), (3, 13), (4, 30), (5, 25), (6, 21),
    (7, 14), (9, 41), (10, 36), (12, 37), (15, 18), (16, 28),
    (17, 40), (19, 22), (20, 27), (23, 29), (24, 31), (26, 32),
    (33, 35), (34, 39),
]
PIVOT_ROWS_42 = [
    38, 50, 97, 156, 193, 231, 266, 91, 93, 414, 10, 12, 138, 140,
    309, 658, 712, 647, 649, 825, 272, 274, 821, 997, 234, 236,
    866, 699, 701, 197, 199, 1040, 1125, 1425, 1420, 455, 457, 79,
    81, 753, 418, 378,
]


def enumerate_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in enumerate_matchings(rest):
            yield ((first, second),) + tail


def commutator_matrix(n, matching):
    N = 2 * n
    partner = {}
    for left, right in matching:
        partner[left] = right
        partner[right] = left
    signs = [(-1) ** index for index in range(N)]
    R = [[0] * N for _ in range(N)]
    for index in range(N):
        R[partner[index]][index] = signs[index]

    columns = []
    for edge in range(N):
        neighbor = (edge + 1) % N
        B = [[0] * N for _ in range(N)]
        B[edge][neighbor] = 1
        B[neighbor][edge] = -1
        comm = [[0] * N for _ in range(N)]
        for row in range(N):
            for col in range(N):
                left = sum(B[row][k] * R[k][col] for k in range(N))
                right = sum(R[row][k] * B[k][col] for k in range(N))
                comm[row][col] = left - right
        columns.append([comm[row][col] for row in range(N) for col in range(N)])
    matrix = [[columns[col][row] for col in range(N)] for row in range(N * N)]
    return matrix, R


def exact_rank(matrix):
    A = [[Fraction(value) for value in row] for row in matrix]
    rows = len(A)
    cols = len(A[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if A[r][col]), None)
        if pivot is None:
            continue
        A[pivot_row], A[pivot] = A[pivot], A[pivot_row]
        value = A[pivot_row][col]
        A[pivot_row] = [entry / value for entry in A[pivot_row]]
        for r in range(rows):
            if r != pivot_row and A[r][col]:
                factor = A[r][col]
                A[r] = [A[r][j] - factor * A[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def exact_small_n_audit(n):
    N = 2 * n
    histogram = Counter()
    matching_count = 0
    for matching in enumerate_matchings(list(range(N))):
        matrix, _ = commutator_matrix(n, matching)
        rank = exact_rank(matrix)
        histogram[N - rank] += 1
        matching_count += 1
    return {
        "n": n,
        "dimension": N,
        "matching_count": matching_count,
        "commutant_nullity_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "atoms_excluded_by_zero_commutant": histogram[0],
        "interpretation": "Nullity zero proves non-reachability; positive nullity is only a necessary-condition pass, not a reachability proof.",
    }


def rank_pivot_rows_mod(matrix, prime):
    A = [[value % prime for value in row] for row in matrix]
    original_rows = list(range(len(A)))
    row = 0
    pivots = []
    for col in range(len(A[0])):
        pivot = next((r for r in range(row, len(A)) if A[r][col] % prime), None)
        if pivot is None:
            continue
        A[row], A[pivot] = A[pivot], A[row]
        original_rows[row], original_rows[pivot] = original_rows[pivot], original_rows[row]
        value = A[row][col] % prime
        inverse = pow(value, -1, prime)
        A[row] = [(entry * inverse) % prime for entry in A[row]]
        for r in range(row + 1, len(A)):
            factor = A[r][col] % prime
            if factor:
                A[r] = [(A[r][j] - factor * A[row][j]) % prime for j in range(len(A[0]))]
        pivots.append(original_rows[row])
        row += 1
        if row == len(A[0]):
            break
    return row, pivots


def determinant_mod(matrix, prime):
    A = [[value % prime for value in row] for row in matrix]
    n = len(A)
    determinant = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if A[r][col] % prime), None)
        if pivot is None:
            return 0
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            determinant = (-determinant) % prime
        value = A[col][col] % prime
        determinant = determinant * value % prime
        inverse = pow(value, -1, prime)
        for r in range(col + 1, n):
            factor = A[r][col] * inverse % prime
            if factor:
                for j in range(col, n):
                    A[r][j] = (A[r][j] - factor * A[col][j]) % prime
    return determinant


def main():
    small = [exact_small_n_audit(n) for n in (2, 3, 4)]
    matrix, R = commutator_matrix(21, MATCHING_42)
    rank, pivots = rank_pivot_rows_mod(matrix, PRIME)
    if rank != 42 or pivots != PIVOT_ROWS_42:
        raise RuntimeError("frozen 42-site modular pivot-row certificate mismatch")
    square = [matrix[row] for row in pivots]
    determinant = determinant_mod(square, PRIME)
    if determinant != 1:
        raise RuntimeError(f"expected determinant 1 modulo {PRIME}, got {determinant}")
    if len(MATCHING_42) != 21 or len({x for pair in MATCHING_42 for x in pair}) != 42:
        raise RuntimeError("frozen 42-site matching is not a perfect matching")
    if R == [[int(i == j) for j in range(42)] for i in range(42)]:
        raise RuntimeError("matching atom unexpectedly equals identity")

    result = {
        "status": "certified_perfect_matching_atom_unreachable_by_cycle_exponential",
        "complete": True,
        "dimension": 42,
        "prime": PRIME,
        "matching": [list(pair) for pair in MATCHING_42],
        "commutator_matrix_shape": [42 * 42, 42],
        "flattening": "row_index = a*42+b for commutator entry (a,b)",
        "cycle_generator_basis": "B_j[j,(j+1)%42]=+1, B_j[(j+1)%42,j]=-1; A(c)=2*sum_j c_j B_j",
        "pivot_rows_zero_based": pivots,
        "pivot_minor_determinant_mod_prime": determinant,
        "rank_mod_prime": rank,
        "full_column_rank_over_Q": True,
        "commutant_kernel_over_R": "only c=0",
        "nonidentity_matching_atom": True,
        "proof": (
            "If R_M=exp(A(c)), then A(c) commutes with R_M. The integer commutator matrix "
            "C has a 42x42 minor with determinant 1 modulo 65521, hence this minor is "
            "nonzero over Q and C has full column rank over R. Thus c=0, which would give "
            "exp(A)=I, contradicting R_M!=I."
        ),
        "small_n_exact_commutant_audits": small,
        "scope": (
            "This proves that the frozen matching atom is not in the fixed cyclic "
            "nearest-neighbour exponential family for any real coupling vector. It does "
            "not prove that the balanced-slice target is outside the convex hull of that "
            "family; another physical positive ensemble may exist."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "rank_mod_prime": rank,
        "pivot_minor_determinant_mod_prime": determinant,
        "small_n": small,
        "output": str(OUTPUT.relative_to(ROOT)),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
