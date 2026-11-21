# 08 · Internal SCCAF — special characteristics

Internal version of the **Special Characteristics Communication and Agreement Form** (SCCAF; Ford form FAF03-111-2
under procedure FAP-03-111), adapted to an academic prototype. Purpose: every characteristic that can hurt someone,
break a regulation or make a metric fail is identified in the DFMEA, gets an agreed control before build, and is
traced to its validation evidence.

Register: `risk/sccaf.csv` (one row per characteristic). Check: `python tools/fmea.py risk/dfmea.csv` computes the
class of every DFMEA row and fails if a YC/YS row has no register entry or a different class. It runs in CI.

## Classification by severity (DFMEA → agreed control)

| DFMEA severity (S) | Occurrence (O) | Design class (DFMEA) | Agreed class after PFMEA / control plan | Typical control |
|---|---|---|---|---|
| 9–10 (safety, regulation) | any | **YC** — potential critical characteristic | **CC** — critical characteristic | Error-proofing or 100 % check, re-verified after any change |
| 5–8 | 4–10 | **YS** — potential significant characteristic | **SC** — significant characteristic | Measured check per build/batch with recorded results |
| 5–8 | 1–3 | none | none | Normal design and build controls |
| 1–4 | any | none | none | Normal design and build controls |

`tools/fmea.py::special_class()` implements exactly this table. Adapted from Ford FMEA practice; if the course or a
customer requires the official handbook rule, confirm it there before changing the table (to verify).

## When the SCCAF applies

- At least one YC or YS row exists in the DFMEA (new row or severity/occurrence change).
- A part changes source or build location even with the same design: new supplier, another 3D printer or filament,
  another workshop. Each build site signs off separately (`site` column).
- A control changes before validation (new, removed or replaced control method).

## Workflow

1. DFMEA row written (`/fmea`) → `tools/fmea.py` prints its class (YC / YS / none).
2. YC/YS → add a row in `risk/sccaf.csv`: characteristic, specification (measured, not from CAD alone), proposed
   control method, owners, `agreed_class` = TBD.
3. Process step defined → PFMEA rows (`risk/pfmea.csv`) and control method; set `agreed_class` to CC or SC.
4. Agreement: design owner, build owner, validation owner and advisor sign (`advisor_signoff` = date). Record the
   decision in the engineering log.
5. Validation evidence: test report in `docs/test-reports/` referencing the SR; `status` = closed only then.

## Role mapping (Ford → this project)

| Ford role | This project |
|---|---|
| Product Development | Design owner: module team (A/B/C/D) |
| Supplier Technical Assistance (STA) | Purchasing / supplier lead of the module team |
| Manufacturing | Build owner: team that assembles the module |
| Supplier and sub-tier | Vendors and print services (record their controls in `control_method`) |
| PPAP submission | Test report + measured parts before integration (no formal PPAP for the prototype) |
| Approval | Advisor sign-off (Dr. Hiram Eredín Ponce Espinosa) |

## Register columns (`risk/sccaf.csv`)

`id` SC-NNN · `dfmea_id` F-NNN · `class` YC/YS (must match the DFMEA) · `characteristic` · `specification` ·
`agreed_class` CC/SC/TBD · `control_method` · `design_owner` · `build_owner` · `validation_owner` ·
`advisor_signoff` (date or pending) · `site` · `status` open/agreed/closed · `req` SR-NNN.
