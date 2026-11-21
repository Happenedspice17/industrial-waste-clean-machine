# DFMA worksheet — <assembly>

Date · author · revision · related SR/ADR

| # | Part | Qty | Moves relative to others? | Different material needed? | Separate for assembly/service? | Theoretical min (0/1) | Handling s | Insertion s | Merge / simplify idea |
|---|---|---|---|---|---|---|---|---|---|

Design efficiency `DE = 3·Nmin/Σt` → run `python tools/dfma.py <csv>` and paste result.
Checklist: one fastener size per module · self-locating features · top-down assembly · service access (tank, basket,
battery, brush) without tools where safe · printable without supports · oil-compatible materials · error-proofing
(poka-yoke) for connectors and parts that can be mounted reversed.
