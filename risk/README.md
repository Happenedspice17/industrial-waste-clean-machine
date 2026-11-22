# Risk — DFMEA, SCCAF, WCCA, DFMA

Data files read by the checkers in [`tools/`](../tools/); CI fails if they are inconsistent.

| File | Method | Today (Nov 2026) | Check |
|---|---|---|---|
| `dfmea.csv` | DFMEA: RPN = S × O × D; any S ≥ 9 needs an action | 9 failure modes; 4 YC (S ≥ 9), 3 YS; top RPN F-001 vacuum vs steel chips (168) | `python tools/fmea.py risk/dfmea.csv` |
| `sccaf.csv` | Internal SCCAF ([`docs/08-sccaf.md`](../docs/08-sccaf.md)): YC/YS → agreed CC/SC + control | 7 special characteristics (SC-001–SC-007), all open | `tools/fmea.py` (class computed from DFMEA) |
| `wcca.yaml` | Worst-case circuit analysis: dividers, logic levels, power branches, runtime | 8 checks: 7 OK, 1 warning (battery-sense divider margin 4.1 %) | `python tools/wcca.py risk/wcca.yaml` |
| `dfma/` | Boothroyd-Dewhurst design efficiency | M4 separation first pass: DE 11.3 % → simplify | `python tools/dfma.py risk/dfma/m4_separation_example.csv` |

Add rows with `/fmea`, `/wcca`, `/dfma`. A DFMEA row classed YC/YS needs its SCCAF entry in the same PR.
Values are design estimates until replaced by measured data (rule 5).
