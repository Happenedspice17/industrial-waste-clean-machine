---
description: Create or modify a parametric OpenSCAD part
argument-hint: <part name and function, measured dimensions if available>
---
Use the `cad-parametric` subagent: $ARGUMENTS
Create `cad/parts/<part>.scad` + `cad/params/<part>.json`, render with `bash cad/tools/render.sh`, list dimensions
still to measure, print settings and n (safety factor) estimate.
