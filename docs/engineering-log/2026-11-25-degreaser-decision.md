# Engineering log — 2026-11-25 Degreaser adopted (ADR-0008) and suction rig with wet trap (TP-S02)

- **Problem:** TP-S01 showed suction alone does not detach the oil film; the team decided to use a cleaning agent.
  The repo still said "no water or chemicals" in the context, business, SDG docs and the presentation.
- **Hypothesis:** A low-dose (≈ 20 mL/m², estimate), low-foam, quick-break degreaser sprayed ahead of the brush breaks
  the film while keeping two waste streams.
- **Change:** ADR-0008 (accepted). SR-022 dose and pump interlock, SR-023 foam, SR-024 floor slip after the pass,
  SR-025 product (water-based, low-foam, quick-break, silicone-free, SDS). DFMEA F-010–F-014 + F-004 updated; PFMEA
  `risk/pfmea.csv` P-001–P-003 (now checked by `tools/fmea.py` and `check_all.py`); SCCAF SC-008–SC-011; WCCA dosing
  pump branch, 165 W → 52 min. `tools/econ.py`: scenario `activity06` keeps the old numbers, `base` adds the
  degreaser. Protocol TP-S02 with the wet trap (sealed jar between nozzle and vacuum) so the vacuum never sucks
  liquid. Context, architecture, standards (NOM-018-STPS added), business, SDG, glossary, README, CLAUDE.md key
  numbers and presentation v4 updated.
- **Evidence:** TP-S01 (measured 2026-11-24, exploratory). Dose, concentrate price (MXN 65/L), dosing hardware
  (≈ MXN 1,000), pump power (≈ 5 W) are estimates, not quotes or measurements.
- **Reasoning:** Quick-break lets the oil float and be decanted, so the liquid stream stays one stream and the
  solution tank is a supply, not a third waste stream. Low dose keeps tank, mass and oily-water disposal small.
  Economics (estimates): base net 56,968 → 46,731/yr, payback 6.6 → 8.4 months, NPV 105,269 → 79,529; pessimistic
  NPV 7,928 → −10,926 (not viable); customer payback 1.3 → 1.7 yr; margin 47 → 45 %. The dose is the second most
  sensitive input, so TP-S02 must measure it. Semester-1 archive files (brief, v1–v3 decks) stay frozen; the context
  file wins where they disagree.
- **Result:** `python tools/check_all.py` passes (25 SR, DFMEA, PFMEA, WCCA, pytest). Deck validator passes; slides 5,
  7, 8, 10, 11, 12 rendered and checked.
- **Commits:** this branch.
