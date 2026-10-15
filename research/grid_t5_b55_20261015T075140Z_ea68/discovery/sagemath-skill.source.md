---
name: sagemath-skill
description: Use SageMath as a Python package for exact symbolic and mathematical computation, with a bundled full-text SageMath reference manual and search workflow.
Use when a task needs SageMath APIs for algebra, number theory, combinatorics, polynomial rings, matrices, calculus, graphs, topology, geometry, coding theory, cryptography, manifolds, modular forms, or any nontrivial exact mathematical computation where the agent must look up correct SageMath constructors, methods, examples, or calling conventions before writing and validating code.
---
# SageMath Skill
## Core Rules

Always treat SageMath as a Python package. This preserves the original SageMath skill contract. Prefer the Sage Python namespace; most reference examples use:

```python
from sage.all import *
```

If the active environment exposes `sageall` instead of `sage.all`, use `from sageall import *` and keep the rest of the workflow unchanged.

Do not write code that depends on Sage notebook/preparser-only syntax. Use Python examples from the reference files, for example:
```python
R = PolynomialRing(QQ, names=("x",))
(x,) = R._first_ngens(1)
```

Never invent SageMath APIs from memory. Locate the relevant reference file first, read the exact constructor or method signature, adapt the documented Python example, then execute the code.
## Reference Layout

The full SageMath text reference is bundled in `references/api/`, preserving every `.txt` file from the source reference tree. The files are organized by top-level domain such as `rings`, `groups`, `polynomial_rings`, `matrices`, `number_fields`, `graphs`, `manifolds`, and `calculus`.

Use these generated navigation files:
- `references/domain_index.md`: generated compact domain catalog.
- `references/domain_index.json`: machine-readable domain catalog.
- `references/reference_manifest.jsonl`: one metadata record per bundled reference file.
## Lookup Workflow

1. Analyze the user's mathematical content and decide what mathematical objects, algorithms, and operations are needed. Do this reasoning yourself; do not use a static task-to-domain routing table.
2. Turn that analysis into one or more concise English search queries using mathematical nouns, SageMath-style object names when known, and operation names. Search the bundled reference with `scripts/sage_ref_search.py`:
```bash
python3 scripts/sage_ref_search.py "multivariate polynomial ideal groebner basis quotient" --examples
```

3. If the first query is too broad or misses the right API, refine the English query from the result titles, symbols, methods, and error terms. Prefer a new global query over a hand-picked domain filter.
4. Open the returned `references/api/...` file and inspect the exact constructor, method, input parameters, warnings, and Python examples:
```bash
python3 scripts/sage_ref_search.py --show references/api/polynomial_rings/rings/polynomial/multi_polynomial_ideal.txt --pattern groebner
```

If the exact returned path differs, use that returned path. Many files end in `.txt`; do not assume a path by memory.
5. Write SageMath-enabled Python code using the documented Python calling convention. Use explicit constructors and parent rings/fields rather than relying on hidden coercions.
6. Execute and verify the code with the runner that matches the operating system.

On macOS or Linux, use the local SageMath runner:

```python
python3 scripts/sagemath_runner.py /path/to/your_script.py
```

On Windows OpenCode Desktop, enter WSL first and use the WSL runner from the WSL shell:
```bash
python3 scripts/sagemath_runner_wsl.py /path/to/your_script.py
```

If execution fails, search the error terms together with the constructor or method name, reread the reference, and revise the code.
## Local SageMath Access

On macOS or Linux, run SageMath-enabled Python through:

```bash
python3 scripts/sagemath_runner.py /path/to/script.py
```

This runner first checks `SAGE_PYTHON`, `sage -python`, `/usr/local/bin/sage`, and common conda environments including `sagemath-env`, `sage_env`, `sage`, and `sagemath`.

On Windows OpenCode Desktop, install SageMath inside WSL, enter the WSL shell, then run:
```bash
python3 scripts/sagemath_runner_wsl.py /path/to/script.py
```

The WSL runner must be run inside WSL. It uses Linux conda inside WSL and runs `conda run -n sagemath-env python`; it refuses Windows conda exposed under `/mnt/c/...`. Override the conda environment with `SAGE_CONDA_ENV` or `--conda-env`.

If SageMath is not available, use `references/install_sagemath.md`; choose the install path by operating system before running commands. The macOS / Linux fallback conda-forge target is SageMath 10.9, while Windows uses the WSL install flow.
## Search Tactics

Use English queries that describe the mathematical tool you need, not the user's whole problem statement. Good query ingredients are object names, constructor names, method names, algorithms, invariants, and algebraic structures.

When search is broad, rewrite the query with more specific operation names or inspected result terms. When a file is promising but long, inspect only a method or term:
```bash
python3 scripts/sage_ref_search.py --show references/api/graphs/graphs/graph.txt --pattern chromatic_polynomial --context 5
```

Read `index.txt` when an API area is unfamiliar, `constructor.txt` for public factories, `all.txt` for exposed names, `*_element.txt` for element methods, and `*_morphism.txt` or `homset.txt` for maps and homomorphisms.
## Output Standards

When answering the user:

- State which SageMath API or reference file you relied on when it matters.
- Provide executable Python code, not Sage prompt transcripts.
- Include the verified output or clearly say if execution was not possible.
- Translate results into mathematical language after the computation.
## Prohibited Behavior

- Do not load large unrelated reference files. Use focused English searches and `--show --pattern` inspection first.
- Do not cross domains without evidence from the docs; for example, do not solve a ring-theory task using calculus APIs because a name happens to match.
- Do not silently fall back to pure Python approximations for exact SageMath tasks. If SageMath is unavailable, say so and ask before installation.
- Do not trust a failed or partial computation. Rerun after fixing the code and report the final verified result.
