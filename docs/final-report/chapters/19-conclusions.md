# Conclusions

## What has been demonstrated, and how

**By analysis and simulation (not by physical tests):**

1. **The need is real and measurable.** Same-level falls cost U.S. manufacturing USD 1.20 billion a year; Mexico
   recorded 290,527 work accidents in 2023; metalworking fluids harm health; mixed oil, chips and absorbent become one
   hazardous waste. NOM-001-STPS-2008 asks for floors free of liquids that cause slips.
2. **There is a gap.** In the literature and five patents reviewed, and among commercial autonomous scrubbers, no
   system collects oil and chips autonomously and stores them as two separate streams.
3. **One integrated concept covers all ten requirements.** Every requirement maps to at least one of nine modules; 21
   system requirements carry acceptance criteria fixed before testing; three ethical value requirements protect
   worker safety, the environment and privacy.
4. **It is buildable in Mexico** for about MXN 17,500 including tooling (≈ MXN 20,160 with contingency), with parts
   priced at local suppliers.
5. **A cleaning cycle fits the shift change and the battery:** 96 % coverage of a 12 × 8 m cell in 25.6 min at
   167 m²/h, 68 Wh per cycle, ≈ 2 cycles per charge (simulation).
6. **It is safe by design:** speed ≤ 0.38 m/s, ≤ 7.4 cm braking on oil (calculation), hardware e-stop, float shut-off,
   force limit, watchdog; safety never depends on software.
7. **It is economically viable:** 6.6-month payback in the base case; positive NPV even in the pessimistic case
   (estimates).
8. **The engineering record is complete and checked:** DFMEA (9 failure modes), SCCAF (7 special characteristics),
   WCCA (8 checks), DFMA, threat model (6 threats), 7 ADRs and 2 test protocols, all in a public repository whose CI
   enforces traceability and risk rules on every change.

## What has not been demonstrated yet

- Physical collection and separation performance (metrics M1–M3).
- Whether the 80 W vacuum can lift steel chips (option A vs B) — **the design gate.**
- LiDAR navigation in reflective, oily surroundings.
- Every safety function on real hardware (e-stop timing, heartbeat loss, float shut-off, compactor limit).
- The AprilTag bench app's physical accuracy (simulation is borderline).

## Hypothesis status

The hypothesis (Section 1.5) is **neither accepted nor rejected**: it can only be tested on the prototype. What this
semester achieved is to make it testable, with metrics, thresholds, protocols and a test order that attacks the
largest risk first.

## Final reflection

The most valuable result of this semester is not a number but a method: requirements before features, evidence
before claims, safety in hardware, risks in files that a machine checks, and decisions written down with their
reasons. The next semester will tell whether the concept works; this report makes sure that, whatever the suction rig
says, the team will know what to change, why, and how to prove it.
