# Conclusions

## What has been demonstrated, and how

**By analysis and simulation, plus one exploratory pre-test:**

1. **The need is real and measurable.** Same-level falls cost U.S. manufacturing USD 1.20 billion a year; Mexico
   recorded 290,527 work accidents in 2023; metalworking fluids harm health; mixed oil, chips and absorbent become one
   hazardous waste. NOM-001-STPS-2008 asks for floors free of liquids that cause slips.
2. **There is a gap.** In the literature and five patents reviewed, and among commercial autonomous scrubbers, no
   system collects oil and chips autonomously and stores them as two separate streams.
3. **One integrated concept covers all ten requirements.** Every requirement maps to at least one of nine modules; 25
   system requirements carry acceptance criteria fixed before testing; three ethical value requirements protect
   worker safety, the environment and privacy.
4. **It is buildable in Mexico** for about MXN 17,500 including tooling (≈ MXN 20,160 with contingency, ≈ MXN 21,310 with the
   dosing system), with parts
   priced at local suppliers.
5. **A cleaning cycle fits the shift change and the battery:** 96 % coverage of a 12 × 8 m cell in 25.6 min at
   167 m²/h, 68 Wh per cycle, ≈ 2 cycles per charge (simulation).
6. **Suction alone is not enough, and the concept was corrected.** The first physical pre-test (TP-S01, 24 Nov 2026)
   showed no visible effect of dry suction and 85–90 % film removal (visual) with a degreaser; the team adopted a
   low-dose, low-foam degreaser ahead of the brush (ADR-0008) and kept two waste streams.
7. **It is safe by design:** speed ≤ 0.38 m/s, ≤ 7.4 cm braking on oil (calculation), hardware e-stop, float shut-off,
   force limit, watchdog; safety never depends on software.
8. **It is economically attractive in the base case:** 6.6-month payback for the dry concept and 8.4 months with the
   degreaser; the pessimistic case with degreaser is negative, so the dose must be measured (estimates).
9. **The engineering record is complete and checked:** 25 system requirements, DFMEA (14 failure modes), PFMEA (3),
   SCCAF (11 special characteristics), WCCA (9 checks), DFMA, threat model (6 threats), 8 ADRs, 1 test report and 3
   test protocols, all in a public repository whose CI
   enforces traceability and risk rules on every change.

## What has not been demonstrated yet

- Physical collection and separation performance (metrics M1–M3) with the robot's own vacuum, brush and squeegee.
- Whether the vacuum can lift steel chips (option A vs B) and the right degreaser dose, foam and slip — **the design
  gate (TP-S02).**
- LiDAR navigation in reflective, oily surroundings.
- Every safety function on real hardware (e-stop timing, heartbeat loss, float shut-off, compactor limit).
- The AprilTag bench app's physical accuracy (simulation is borderline).

## Hypothesis status

The hypothesis (Section 1.5) is **neither accepted nor rejected**: it can only be tested on the prototype. The
pre-test already refined it (degreaser ahead of the brush). What this semester achieved is to make it testable, with metrics, thresholds, protocols and a test order that attacks the
largest risk first.

## Final reflection

The most valuable result of this semester is not a number but a method: requirements before features, evidence
before claims, safety in hardware, risks in files that a machine checks, and decisions written down with their
reasons. The next semester will tell whether the concept works; this report makes sure that, whatever the suction rig
says, the team will know what to change, why, and how to prove it.
