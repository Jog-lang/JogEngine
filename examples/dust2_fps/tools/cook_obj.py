#!/usr/bin/env python3
"""Cook a Wavefront OBJ for JogEngine dust2_fps.

Y-up → Z-up ((x,y,z)->(x,z,y)), uniform scale 0.5, positions + triangulated faces only.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def cook(src: Path, dst: Path, scale: float = 0.5) -> None:
    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []
    with src.open() as f:
        for line in f:
            if line.startswith("v "):
                _, xs, ys, zs = line.split()[:4]
                x, y, z = float(xs), float(ys), float(zs)
                # Y-up → Z-up
                verts.append((x * scale, z * scale, y * scale))
            elif line.startswith("f "):
                parts = line.split()[1:]
                idx = [int(p.split("/")[0]) for p in parts]
                for i in range(1, len(idx) - 1):
                    faces.append((idx[0], idx[i], idx[i + 1]))
    minx = min(v[0] for v in verts)
    miny = min(v[1] for v in verts)
    minz = min(v[2] for v in verts)
    # +octant pad — engine milli SoA poke64 is unsigned-safe for non-negative coords.
    ox, oy, oz = minx - 1.0, miny - 1.0, minz - 1.0
    verts = [(x - ox, y - oy, z - oz) for x, y, z in verts]
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w") as out:
        out.write(
            "# Cooked for JogEngine dust2_fps: Y-up→Z-up, scale "
            f"{scale}, recenter +octant, positions+tris only\n"
        )
        out.write(f"# verts={len(verts)} tris={len(faces)}\n")
        for x, y, z in verts:
            out.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
        for a, b, c in faces:
            out.write(f"f {a} {b} {c}\n")
    print(f"wrote {dst} verts={len(verts)} tris={len(faces)}")
    print(f"offset ({-ox}, {-oy}, {-oz})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--scale", type=float, default=0.5)
    args = ap.parse_args()
    cook(Path(args.src), Path(args.dst), args.scale)


if __name__ == "__main__":
    main()
