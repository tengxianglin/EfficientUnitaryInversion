"""Freeze the platform-sensitive binary64 seed pool after hash verification.

The random seed alone is not a portable specification: libm/CPU differences can
change the last bits of exp/log/normal outputs. This script only freezes a
generated pool when it exactly matches the previously certified SHA256.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np

from ising_fourth_moments import seed_pool

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "evidence/full_low_moment_certificate_input_n21.json"
OUTPUT = ROOT / "evidence/seed_pool_n21_frozen.npy"
METADATA = ROOT / "evidence/seed_pool_n21_frozen.json"


def main():
    cfg = json.loads(INPUT.read_text())
    expected = cfg["pool_couplings_sha256_le_f64"]
    rows = np.asarray(seed_pool(), dtype="<f8")
    actual = hashlib.sha256(rows.tobytes()).hexdigest()
    if rows.shape != (1600, 42):
        raise RuntimeError(f"unexpected seed-pool shape: {rows.shape}")
    if actual != expected:
        raise RuntimeError(
            "this runner does not reproduce the frozen binary64 seed-pool "
            f"fingerprint: expected {expected}, got {actual}; do not overwrite it"
        )
    np.save(OUTPUT, rows, allow_pickle=False)
    metadata = {
        "sha256_le_f64": actual,
        "shape": list(rows.shape),
        "dtype": "<f8",
        "numpy_version": np.__version__,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "generator_seed": 202611210435,
        "generation_note": "Frozen exact binary64 output; seed-only regeneration is not assumed cross-platform.",
    }
    METADATA.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
