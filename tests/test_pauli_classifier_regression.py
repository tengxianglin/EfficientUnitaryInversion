"""Dependency-light regression tests for the Pauli Hamiltonian taxonomy."""

import ast
import itertools
import pathlib
import unittest
from typing import List


def load_classifier_namespace():
    source_path = pathlib.Path(__file__).parents[1] / "utils" / "hamiltonian_utils.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    wanted = {
        "multiply_paulis",
        "_pauli_y_parity",
        "is_commuting",
        "is_type_1",
        "is_type_1_2",
        "is_type_2_1",
        "is_type_2_2",
        "is_type_2_2_1",
        "H_type",
        "certify_one_slot_pauli_dagger",
        "certify_one_slot_pauli_transpose",
        "certify_one_slot_pauli_conj",
        "certify_uniform_pauli_word_dagger",
    }
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    namespace = {"itertools": itertools, "List": List}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source_path), "exec"), namespace)
    return namespace


class PauliClassifierRegressionTest(unittest.TestCase):
    def test_type_1_2_identity_product(self):
        ns = load_classifier_namespace()
        support = ["X0", "Z0", "X1", "Z1", "Y0,Y1"]
        self.assertTrue(ns["is_type_1"](support))
        self.assertTrue(ns["is_type_1_2"](support))
        self.assertEqual(ns["H_type"](support), "1.2")

    def test_one_slot_target_certificates(self):
        ns = load_classifier_namespace()
        support = ["X0", "Y0"]
        self.assertTrue(ns["certify_one_slot_pauli_dagger"](
            support, "Z0"
        ))
        self.assertTrue(ns["certify_one_slot_pauli_transpose"](
            support, "X0"
        ))
        self.assertTrue(ns["certify_one_slot_pauli_conj"](
            support, "Y0"
        ))
        self.assertFalse(ns["certify_one_slot_pauli_transpose"](
            support, "Z0"
        ))

    def test_uniform_character_multi_slot_certificate(self):
        ns = load_classifier_namespace()
        self.assertTrue(ns["certify_uniform_pauli_word_dagger"](
            ["X0"], ["X0", "Z0", "X0", "Z0"]
        ))

    def test_type_1_without_odd_identity_product(self):
        ns = load_classifier_namespace()
        support = ["X0", "Z0", "X1", "Z1", "X0,Y1"]
        self.assertTrue(ns["is_type_1"](support))
        self.assertFalse(ns["is_type_1_2"](support))
        self.assertEqual(ns["H_type"](support), "1")


if __name__ == "__main__":
    unittest.main()
