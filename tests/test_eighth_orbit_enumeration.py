import unittest

from eighth_orbit_enumeration import (
    burnside_even,
    enumeration_summary,
    orbit_size_from_gaps,
    task_keys,
    task_specs,
)


class EighthOrbitEnumerationTests(unittest.TestCase):
    def test_burnside_reference_counts(self):
        self.assertEqual(burnside_even(10, 4)["orbit_count"], 16)
        self.assertEqual(burnside_even(14, 6)["orbit_count"], 126)
        self.assertEqual(burnside_even(42, 8)["orbit_count"], 1408185)
        result = burnside_even(42, 8)
        self.assertEqual(result["rotation_fixed_sum"], 118036170)
        self.assertEqual(result["vertex_reflection_fixed"], 5985)
        self.assertEqual(result["edge_reflection_fixed"], 5985)

    def test_small_canonical_enumerations(self):
        for N, k, expected_orbits, expected_sets in (
            (10, 4, 16, 210),
            (14, 6, 126, 3003),
        ):
            summary, _ = enumeration_summary(N, k)
            self.assertEqual(summary["canonical_orbits"], expected_orbits)
            self.assertEqual(summary["orbit_size_sum"], expected_sets)
            self.assertEqual(summary["all_k_subsets"], expected_sets)

    def test_task_partition_is_disjoint(self):
        N, k = 14, 6
        keys = []
        for spec in task_specs(N, k):
            keys.extend(task_keys(N, k, spec))
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(keys), 126)
        self.assertEqual(sum(orbit_size_from_gaps(g, N) for g in keys), 3003)


if __name__ == "__main__":
    unittest.main()
