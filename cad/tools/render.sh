#!/usr/bin/env bash
# Usage: bash cad/tools/render.sh cad/parts/<part>.scad [paramset]
set -euo pipefail
part="$1"; set_name="${2:-default}"
name="$(basename "$part" .scad)"
params="$(dirname "$part")/../params/${name}.json"
mkdir -p cad/out
out="cad/out/${name}$([ "$set_name" = default ] || echo "-$set_name").stl"
if [ -f "$params" ]; then
  openscad --hardwarnings -o "$out" -p "$params" -P "$set_name" "$part"
else
  openscad --hardwarnings -o "$out" "$part"
fi
echo "rendered $out"
