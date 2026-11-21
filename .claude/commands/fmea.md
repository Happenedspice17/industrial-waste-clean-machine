---
description: Add DFMEA or PFMEA rows for a part, module or process step
argument-hint: <part/module/process> [dfmea|pfmea]
---
Use the `dfma-fmea-engineer` subagent. Target: $ARGUMENTS
Follow the AIAG-VDA seven steps, append rows to `risk/dfmea.csv` (or `risk/pfmea.csv`) using the templates, run
`python tools/fmea.py risk/dfmea.csv`, and list mandatory actions (any S ≥ 9) and new requirements needed. For every row the tool classes YC/YS, add or
update the entry in `risk/sccaf.csv` (`docs/08-sccaf.md`).
