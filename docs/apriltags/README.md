# AprilTags for localization (ADR-0007, SR-018)

`apriltags_36h11_160mm_LETTER.pdf`: IDs 0–25 (13 stations of two tags), family tag36h11, black square 160 mm
nominal, one per letter page (216 × 279 mm). `apriltags_36h11_home_160mm_LETTER.pdf`: home pair IDs 100–101.
Regenerate or make other sizes: `python tools/gen_apriltags.py --ids 0-19 --size-mm 160 --paper LETTER --out docs/apriltags`
(home: `--ids 100-101 --label HOME`)
(A4: `--size-mm 150 --paper A4`; add `--png` for one image per tag).

## Print and mount
1. Print at **100 % / actual size** (never "fit to page"), matte paper, laser printer.
2. Measure the black square with a steel rule; reject a sheet more than 1 mm off. Write the measured size in the map.
3. Glue on rigid flat board (foam board or acrylic, matte). Keep the white border; do not trim into it.
4. Mount vertical, "TOP" up, centre 0.9 m above the floor, facing the work area, out of oil splash and forklift paths.
5. Mount tags in **stations of two**: same height, same facing, centres 0.60 m apart (ADR-0008). Example layout
   (`linux/vision/config/tag_map.example.json`, 12 × 8 m cell): one station every 3 m along each wall, IDs
   counter-clockwise from the (0, 0) corner. **Home:** tags 100 (left) and 101 (right) seen from the room, centres
   0.40 m apart on the y = 0 wall at x = 1.5 m; keep 1 m in front clear (dock pose) and 1 m more (approach). Add tags on interior columns or machine sides where the robot drives
   long stretches without seeing one (`python sim/tag_visibility.py <your_map.json>`).
6. Survey each tag (x, y, z, facing direction in degrees: 0 = faces +x, 90 = faces +y) from two cell corners; keep
   every ID unique. Re-survey after any tag is moved.

Expected accuracy (simulation, `sim/tag_accuracy.py`, 0.3 px corner noise): p95 ≈ 0.03 m at 1.5 m, 0.09 m at 2.5 m,
0.17 m at 3.5 m (160 mm tag). Real values come from TP-V02.
