# Tools — checkers and calculators

Plain Python, no network. `python tools/check_all.py` runs every blocking check (also in CI and before each PR).

| Script | What it does |
|---|---|
| `check_all.py` | Branch name, traceability, DFMEA, WCCA, ruff lint + format, pytest |
| `check_branch.py` | Branch name follows `CONTRIBUTING.md` (`<type>/<issue>-<desc>`, `claude/…`, `release/…`) |
| `check_commit_msg.py` | Conventional Commit message or PR title (`type(scope): subject`) |
| `check_traceability.py` | `requirements.yaml` structure and R → SR → test links |
| `fmea.py` | DFMEA/PFMEA ranking (RPN), mandatory actions for S ≥ 9, YC/YS classes vs SCCAF register |
| `wcca.py` | Worst-case dividers (EVA + RSS), logic levels, fuse/wire per branch, runtime |
| `dfma.py` | Design efficiency DE = 3 · N_min / Σ assembly time |
| `econ.py` | Economics of one robot: net benefit, payback, NPV, scenarios and sensitivity (Activity 06) |

Unit tests: [`tests/test_tools.py`](../tests/test_tools.py).
