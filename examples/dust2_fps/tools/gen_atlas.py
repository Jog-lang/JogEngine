#!/usr/bin/env python3
"""Write a 64x64 flat-color quadrant atlas as binary P6 PPM.

Matches engine/assets/assets.jog tex_decode_ppm (magic P6, maxval 255).

Usage:
  python3 gen_atlas.py
  python3 gen_atlas.py --out ../assets/atlas.ppm
"""

from __future__ import annotations

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE.parent / "assets" / "atlas.ppm"
SIZE = 64

# Quadrants (R, G, B): TL warm sand, TR muted teal, BL brick, BR stone grey.
QUAD = {
    (0, 0): (210, 170, 110),
    (1, 0): (70, 140, 130),
    (0, 1): (160, 70, 50),
    (1, 1): (120, 120, 125),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--size", type=int, default=SIZE)
    args = ap.parse_args()

    w = h = args.size
    half = w // 2
    pixels = bytearray(w * h * 3)
    for y in range(h):
        for x in range(w):
            qx = 0 if x < half else 1
            qy = 0 if y < half else 1
            r, g, b = QUAD[(qx, qy)]
            i = (y * w + x) * 3
            pixels[i] = r
            pixels[i + 1] = g
            pixels[i + 2] = b

    args.out.parent.mkdir(parents=True, exist_ok=True)
    # Header must end with a single whitespace before binary payload (tex_decode_ppm).
    header = f"P6\n{w} {h}\n255\n".encode("ascii")
    args.out.write_bytes(header + pixels)
    print(f"wrote {args.out} {w}x{h} P6 ({len(header) + len(pixels)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
