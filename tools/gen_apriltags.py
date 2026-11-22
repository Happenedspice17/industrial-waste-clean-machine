#!/usr/bin/env python3
"""Generate printable AprilTag 36h11 sheets at true scale (SR-018).

Usage: python tools/gen_apriltags.py --ids 0-19 --size-mm 160 --paper LETTER --out build/apriltags
Print at 100 % ("actual size", no fit-to-page), then MEASURE the black square and write it in the tag map (rule 8).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFont

PAPER_MM = {"A4": (210.0, 297.0), "A3": (297.0, 420.0), "LETTER": (215.9, 279.4)}
CELLS = 8
MARGIN_MM = 6.0


def parse_ids(text: str) -> list[int]:
    ids: list[int] = []
    for part in text.split(","):
        a, _, b = part.partition("-")
        ids += range(int(a), int(b or a) + 1)
    if any(i < 0 or i > 586 for i in ids):
        raise ValueError("tag36h11 IDs are 0-586")
    return ids


def page(tag_id: int, size_mm: float, paper: str, dpi: int) -> tuple[Image.Image, float]:
    w_mm, h_mm = PAPER_MM[paper]
    cell_px = round(size_mm / CELLS / 25.4 * dpi)
    side_px = cell_px * CELLS
    real_mm = side_px / dpi * 25.4
    quiet_px = cell_px
    if side_px + 2 * quiet_px > (w_mm - 2 * MARGIN_MM) / 25.4 * dpi:
        raise ValueError(f"{size_mm} mm tag + white border does not fit on {paper}")
    dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    tag = Image.fromarray(cv2.aruco.generateImageMarker(dic, tag_id, CELLS, borderBits=1))
    tag = tag.resize((side_px, side_px), Image.Resampling.NEAREST)
    pw, ph = round(w_mm / 25.4 * dpi), round(h_mm / 25.4 * dpi)
    img = Image.new("L", (pw, ph), 255)
    x0 = (pw - side_px) // 2
    y0 = round(MARGIN_MM / 25.4 * dpi) + quiet_px + round(15 / 25.4 * dpi)
    img.paste(tag, (x0, y0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=round(dpi * 0.22))
    small = ImageFont.load_default(size=round(dpi * 0.11))
    draw.text((pw // 2, round(MARGIN_MM / 25.4 * dpi)), "TOP", fill=0, font=small, anchor="mt")
    y = y0 + side_px + quiet_px + round(5 / 25.4 * dpi)
    draw.text((pw // 2, y), f"ID {tag_id}", fill=0, font=font, anchor="mt")
    lines = [
        f"AprilTag tag36h11 - black square {real_mm:.1f} mm (nominal)",
        "Print at 100 % / actual size. Measure the black square and enter it in tag_map.json.",
        "Mount flat, vertical, TOP up, matte surface, centre height as in tag_map.json.",
    ]
    for i, line in enumerate(lines):
        draw.text((pw // 2, y + round(dpi * (0.4 + 0.18 * i))), line, fill=0, font=small, anchor="mt")
    return img.convert("1"), real_mm


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ids", default="0-19")
    ap.add_argument("--size-mm", type=float, default=160.0)
    ap.add_argument("--paper", default="LETTER", choices=sorted(PAPER_MM))
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--out", type=Path, default=Path("build/apriltags"))
    ap.add_argument("--png", action="store_true", help="also write one PNG per tag")
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    pages = []
    for tid in parse_ids(a.ids):
        img, real = page(tid, a.size_mm, a.paper, a.dpi)
        pages.append(img)
        if a.png:
            img.save(a.out / f"tag36h11_{tid:03d}.png", dpi=(a.dpi, a.dpi))
    pdf = a.out / f"apriltags_36h11_{a.size_mm:.0f}mm_{a.paper}.pdf"
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=a.dpi)
    print(f"{len(pages)} tags -> {pdf} (black square {real:.1f} mm at {a.dpi} dpi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
