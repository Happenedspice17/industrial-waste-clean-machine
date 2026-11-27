# ADR-0004: Collection architecture A (vacuum for all) vs B (front hopper for chips)

- Status: **proposed — decide with suction rig (next semester, weeks 1–3)** · Requirements: SR-001, SR-002

## Options
A: brush + vacuum carry liquid and chips into the sealed chamber (one intake, simplest).
B: brush throws chips into a front hopper with magnets; vacuum handles only liquid (chips never pass through the hose).
## Decision criteria (fix before the test)
Chip lift rate (g/s) for reference chips; liquid recovered per pass; clogging with long chips (count per 10 runs);
current/temperature of vacuum motor. Choose A only if chip pickup ≥ 85 % and no clogging in 10 runs.
## Context
Pickup velocity grows with density (steel ≈ 7,850 kg/m³); 80 W automotive vacuum is the main technical risk (F-001).
## Evidence so far
- [TP-S01](../test-reports/TP-S01-handheld-suction-pretest.md), measured 2026-11-24, exploratory: handheld dry vacuum
  (16 kPa / 40 AW, seller data), **no brush, no squeegee**. Dry: no visible change on oil or oil + dust, 0 of 5
  coins lifted. With water + dish soap + baking soda: film mostly removed (visual estimate 85–90 %), 2 of 5 coins
  (30 % by mass, only the two lightest). Suction alone fails the option-A criterion with this vacuum; the brush +
  squeegee concept and the BOM vacuum are still untested, so the decision stays open.
- Degreaser adopted by the team on 2026-11-25 ([ADR-0008](0008-cleaning-agent-dosing.md)). The A/B decision is
  taken on the rig with brush + degreaser + wet trap ([TP-S02](../test-reports/TP-S02-suction-rig-wet-trap.md)).
