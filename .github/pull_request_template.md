## What and why
<!-- One paragraph. Link the issue: Closes #NN -->

## Requirements
<!-- SR-xxx IDs implemented or verified, or "N/A (tooling)" -->

## Evidence
<!-- Test / simulation / measurement with date and conditions. Never present simulation as physical evidence. -->
- [ ] Unit tests
- [ ] Simulation (seeds, scenarios, success rate)
- [ ] Bench / floor test (date, conditions, log file)

## Risk
- [ ] DFMA worksheet (parts/assemblies) or N/A with reason
- [ ] DFMEA/PFMEA updated (or not affected)
- [ ] WCCA updated (electrical changes)
- [ ] Safety functions unchanged or re-verified (e-stop, watchdog, limits)

## Lessons-learned check
- [ ] Thresholds from measured readings (midpoint)
- [ ] Single bad reading cannot change state
- [ ] MCU stops by itself if Linux is late
- [ ] Removed dead code where possible

## Docs
- [ ] requirements.yaml / docs / ADR / engineering log updated
