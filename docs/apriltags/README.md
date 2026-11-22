# AprilTags for localization (ADR-0007, SR-018)

`apriltags_36h11_220mm_A3.pdf`: IDs 0–19, family tag36h11, black square 220 mm nominal, one per A3 page.
Regenerate or make other sizes: `python tools/gen_apriltags.py --ids 0-19 --size-mm 220 --paper A3 --out docs/apriltags`
(A4: `--size-mm 150 --paper A4`; add `--png` for one image per tag).

## Print and mount
1. Print at **100 % / actual size** (never "fit to page"), matte paper, laser printer.
2. Measure the black square with a steel rule; reject a sheet more than 1 mm off. Write the measured size in the map.
3. Glue on rigid flat board (foam board or acrylic, matte). Keep the white border; do not trim into it.
4. Mount vertical, "TOP" up, centre 0.9 m above the floor, facing the work area, out of oil splash and forklift paths.
5. Example layout (`linux/vision/config/tag_map.example.json`, 12 × 8 m cell): one tag every 2 m along each wall,
   IDs counter-clockwise from the (0, 0) corner. Add tags on interior columns or machine sides where the robot drives
   long stretches without seeing one (`python sim/tag_visibility.py <your_map.json>`).
6. Survey each tag (x, y, z, facing direction in degrees: 0 = faces +x, 90 = faces +y) from two cell corners; keep
   every ID unique. Re-survey after any tag is moved.

Expected accuracy (simulation, `sim/tag_accuracy.py`, 0.3 px corner noise): p95 ≈ 0.02 m at 1.5 m, 0.07 m at 2.5 m,
0.16 m at 3.5 m. Real values come from TP-V02.
