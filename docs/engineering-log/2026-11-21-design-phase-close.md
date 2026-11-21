# Engineering log — 2026-11-21 Design phase close (semester 1)

- **Problem:** Plants accumulate oil and metal chips on floors; no system found that cleans and separates both streams autonomously.
- **Hypothesis:** Brush + vacuum + sealed separation chamber + separate tank on a diff-drive UNO Q robot can meet M1–M3.
- **Change:** Requirements R1–R10, two selection methods (agreement 0.26 → 0.83 after correction), conceptual design,
  9 modules, priced BOM (MXN 15,849.50), scenario analysis, economics, standards, final presentation.
- **Evidence:** Calculations and simulations only (coverage 96 %, 25.6 min, 167 m²/h; payback 6.6 months). No physical tests.
- **Reasoning:** Suction is the critical risk → suction-first plan; option B as backup (ADR-0004).
- **Result:** Design complete; build starts next semester.
- **Commits:** repository created after this stage (deduced).
