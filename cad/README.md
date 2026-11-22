# CAD — parametric OpenSCAD

**Status (Nov 2026):** one draft part; most CAD waits for the suction-rig decision (ADR-0004) and for measured
parts (rule 8: measure before modeling).

Why OpenSCAD: text-based (diff-able in Git), fully parametric, light on CPU/RAM, renders headless in CI.

```
cad/
  lib/common.scad      shared modules (hex prism, D-bore, holes, captive nuts, fn helper)
  parts/<part>.scad    one part per file, parameters at the top
  params/<part>.json   OpenSCAD customizer parameter sets (variants without code edits)
  tools/render.sh      headless render → cad/out/<part>[-<set>].stl
```

Rules (see `.claude/agents/cad-parametric.md`): measure real parts first and record value/date/instrument; `$fn`
low in preview, high in render; avoid `minkowski`; PETG for anything in the oil path; n ≥ 2 (n ≥ 3 bump mounts).

Render: `bash cad/tools/render.sh cad/parts/wheel_hub_hex.scad [paramset]`

## Parts

| Part | Module | Status |
|---|---|---|
| `wheel_hub_hex` | M2 — adapts JGB37-3530 D-shaft to Talon 12 mm hex wheel | draft; shaft and wheel dims TO MEASURE |
