# Engineering log — 2026-11-21 Glossary and internal SCCAF

- **Problem:** Team lingo (M1 module vs M1 metric, DoD battery vs definition of done, Spanish terms) was undefined;
  no process to identify and agree controls for safety-critical characteristics.
- **Hypothesis:** A glossary plus an automated YC/YS classification tied to the DFMEA keeps critical characteristics
  from being missed.
- **Change:** `docs/07-glossary.md`; `docs/08-sccaf.md` (Ford SCCAF adapted); `risk/sccaf.csv` with SC-001–SC-007;
  `tools/fmea.py` classes rows (YC: S 9–10; YS: S 5–8 and O 4–10), checks the register and rejects duplicate IDs.
  Fixed duplicate DFMEA IDs from the bootstrap PR (vision rows renumbered F-007–F-009).
- **Evidence:** `python tools/check_all.py` passes; unit tests cover the class boundaries and register check.
- **Reasoning:** Class is computed, not typed, so it cannot drift from S/O; CI fails if a YC/YS row has no agreement.
- **Result:** 7 characteristics open (4 YC, 3 YS), all `agreed_class` TBD until PFMEA and advisor sign-off.
- **Commits:** branch `docs/glossary-scaf` (deduced: merged by PR into `develop`).
