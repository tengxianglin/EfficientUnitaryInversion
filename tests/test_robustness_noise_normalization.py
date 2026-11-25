"""Regression tests for Appendix B's per-instance L1 noise convention."""

import unittest
from pathlib import Path

import torch

from utils.noise_scaling import scale_out_of_support_coefficients


class RobustnessNoiseNormalizationTests(unittest.TestCase):
    def test_requested_l1_ratio_for_all_five_protocol_support_sizes(self):
        torch.manual_seed(20261125)
        support_sizes = {
            "1-slot, 3 qubits": (32, 31),
            "3-slot A, 3 qubits": (6, 57),
            "3-slot B, 3 qubits": (6, 57),
            "7-slot, 3 qubits": (7, 56),
            "15-slot, 4 qubits": (15, 240),
        }
        deltas = (0.0, 0.001, 0.01, 0.1)
        for name, (m_in, m_out) in support_sizes.items():
            in_support = torch.randn(10000, m_in, dtype=torch.float64)
            raw_out = torch.randn(10000, m_out, dtype=torch.float64)
            in_l1 = in_support.abs().sum(dim=1)
            for delta in deltas:
                scaled = scale_out_of_support_coefficients(in_support, raw_out, delta)
                ratio = scaled.abs().sum(dim=1) / in_l1
                expected = torch.full_like(ratio, delta)
                max_error = (ratio - expected).abs().max().item()
                self.assertLessEqual(max_error, 1e-14, msg=f"{name}, delta={delta}")

    def test_all_five_production_routines_use_the_shared_normalizer(self):
        source_path = Path(__file__).resolve().parents[1] / "robustness_analysis.py"
        source = source_path.read_text(encoding="utf-8")
        self.assertEqual(source.count("scale_out_of_support_coefficients("), 5)
        self.assertNotIn("sum_Sp = params_Sp.abs().sum", source)

    def test_zero_rows_are_rejected(self):
        in_support = torch.tensor([[1.0, 2.0], [0.0, 0.0]], dtype=torch.float64)
        raw_out = torch.tensor([[3.0, 4.0], [1.0, 2.0]], dtype=torch.float64)
        with self.assertRaises(ValueError):
            scale_out_of_support_coefficients(in_support, raw_out, 0.1)
        in_support = torch.tensor([[1.0, 2.0]], dtype=torch.float64)
        raw_out = torch.tensor([[0.0, 0.0]], dtype=torch.float64)
        with self.assertRaises(ValueError):
            scale_out_of_support_coefficients(in_support, raw_out, 0.1)

    def test_invalid_delta_and_shapes_are_rejected(self):
        in_support = torch.ones((2, 2), dtype=torch.float64)
        raw_out = torch.ones((2, 3), dtype=torch.float64)
        for delta in (-0.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                scale_out_of_support_coefficients(in_support, raw_out, delta)
        with self.assertRaises(ValueError):
            scale_out_of_support_coefficients(
                in_support, torch.ones((1, 3), dtype=torch.float64), 0.1
            )


if __name__ == "__main__":
    unittest.main()
