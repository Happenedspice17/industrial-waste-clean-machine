# Engineering log — 2026-11-25 Handheld suction pre-test (TP-S01) and presentation v4

- **Problem:** The collection concept (ADR-0004) is the main open risk (F-001) and had no physical evidence.
- **Hypothesis:** Suction alone cannot lift an oily film or heavy chips; agitation (brush) is needed.
- **Change:** María Ruiz Mejía ran four exploratory tests on 2026-11-24 with a handheld dry vacuum (Fanttik X200,
  16 kPa / 40 AW per seller), no brush, no squeegee: oil; oil + dust; oil + dust + 5 coins; same with a water + dish
  soap + baking soda solution. Added her log (photos re-encoded, SHA-256 of the original recorded), the extracted
  photos and report `docs/test-reports/TP-S01-handheld-suction-pretest.md`; "Evidence so far" in ADR-0004; deck
  `Final_Presentation_Waste_Robot_v4.pptx/.pdf` = v3 + slide 10 "First suction test" (photos, 0 % / 2 of 5 / 30 %),
  slide 9 notes shortened, next-steps note says the rig now uses the brush and the robot's vacuum.
- **Evidence:** Measured 2026-11-24, home setup, visual before/after comparison; coin masses are official values,
  not weighed; vacuum rating is seller data. Dry: no visible change, 0 of 5 coins. Degreaser: film mostly gone
  (visual estimate 85–90 %), 2 of 5 coins = 7.053 / 23.263 g = 30.3 % by mass.
- **Reasoning:** Supports the brush already in M3; does not test the brush + squeegee concept nor the BOM vacuum, so
  ADR-0004 stays open. The degreaser conflicts with the "no water or chemicals" principle (third stream, emulsion,
  foam toward the vacuum, F-002) → needs its own ADR with rig data; not adopted. The source log numbers tests
  inconsistently; renumbered T1–T4 in the report.
- **Result:** Hypothesis supported (exploratory). SR-001 not evaluated (no mass). Deck validator passes, slide 10
  rendered and checked; talk ≈ 10.5 min with the new slide (deduced from the notes' time marks).
- **Commits:** this branch.
