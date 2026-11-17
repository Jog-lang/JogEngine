#!/usr/bin/env python3
"""Cook a Wavefront OBJ for JogEngine dust2_fps.

Y-up → Z-up ((x,y,z)->(x,z,y)), uniform scale 0.5, recenter +octant.
Expands corners to unique pos+uv+normal verts with atlas UVs (ignore source vt).
Caps via quantized weld when over MESH_VERT_CAP.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

MESH_VERT_CAP = 20000
MESH_TRI_CAP = 10000

# Atlas quadrant bases: planar micro-UV lives in [0.05, 0.45] within each.
QUAD_BASE = (
    (0.0, 0.0),  # 0 floor/ceil (|nz|)
    (0.5, 0.0),  # 1 |nx|
    (0.0, 0.5),  # 2 |ny|
    (0.5, 0.5),  # 3 else
)


def _parse_face_corner(tok: str) -> tuple[int, int | None, int | None]:
    parts = tok.split("/")
    vi = int(parts[0])
    vti = int(parts[1]) if len(parts) > 1 and parts[1] else None
    vni = int(parts[2]) if len(parts) > 2 and parts[2] else None
    return vi, vti, vni


def _normalize(n: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = n
    L = math.sqrt(x * x + y * y + z * z)
    if L < 1e-12:
        return (0.0, 0.0, 1.0)
    return (x / L, y / L, z / L)


def _face_normal(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    c: tuple[float, float, float],
) -> tuple[float, float, float]:
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    return _normalize((uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx))


def _dominant_quadrant(n: tuple[float, float, float]) -> int:
    ax, ay, az = abs(n[0]), abs(n[1]), abs(n[2])
    if az >= ax and az >= ay:
        return 0
    if ax >= ay and ax >= az:
        return 1
    if ay >= ax and ay >= az:
        return 2
    return 3


def _frac01(x: float) -> float:
    return x - math.floor(x)


def _atlas_uv(
    pos: tuple[float, float, float],
    face_n: tuple[float, float, float],
) -> tuple[float, float]:
    q = _dominant_quadrant(face_n)
    bx, by = QUAD_BASE[q]
    # Planar axes orthogonal to dominant direction.
    if q == 0:  # |nz| — use x,y
        s, t = pos[0], pos[1]
    elif q == 1:  # |nx| — use y,z
        s, t = pos[1], pos[2]
    elif q == 2:  # |ny| — use x,z
        s, t = pos[0], pos[2]
    else:  # mixed — use x,y
        s, t = pos[0], pos[1]
    # Tiny planar UV: mod position into 0.05..0.45
    u = bx + 0.05 + _frac01(s * 0.25) * 0.40
    v = by + 0.05 + _frac01(t * 0.25) * 0.40
    return (u, v)


def _qkey(
    p: tuple[float, float, float],
    uv: tuple[float, float],
    n: tuple[float, float, float],
) -> tuple[int, ...]:
    return (
        int(round(p[0] * 1000.0)),
        int(round(p[1] * 1000.0)),
        int(round(p[2] * 1000.0)),
        int(round(uv[0] * 1000.0)),
        int(round(uv[1] * 1000.0)),
        int(round(n[0] * 1000.0)),
        int(round(n[1] * 1000.0)),
        int(round(n[2] * 1000.0)),
    )


def cook(src: Path, dst: Path, scale: float = 0.5) -> None:
    raw_v: list[tuple[float, float, float]] = []
    raw_vt: list[tuple[float, float]] = []
    raw_vn: list[tuple[float, float, float]] = []
    raw_faces: list[list[tuple[int, int | None, int | None]]] = []

    with src.open() as f:
        for line in f:
            if line.startswith("v "):
                _, xs, ys, zs = line.split()[:4]
                x, y, z = float(xs), float(ys), float(zs)
                # Y-up → Z-up, then scale
                raw_v.append((x * scale, z * scale, y * scale))
            elif line.startswith("vt "):
                parts = line.split()
                raw_vt.append((float(parts[1]), float(parts[2])))
            elif line.startswith("vn "):
                parts = line.split()
                nx, ny, nz = float(parts[1]), float(parts[2]), float(parts[3])
                # Same axis swap as positions; normalize
                raw_vn.append(_normalize((nx, nz, ny)))
            elif line.startswith("f "):
                parts = line.split()[1:]
                corners = [_parse_face_corner(p) for p in parts]
                # Triangulate polygon fan
                for i in range(1, len(corners) - 1):
                    raw_faces.append([corners[0], corners[i], corners[i + 1]])

    if not raw_v or not raw_faces:
        raise SystemExit(f"no verts/faces in {src}")

    minx = min(v[0] for v in raw_v)
    miny = min(v[1] for v in raw_v)
    minz = min(v[2] for v in raw_v)
    # +octant pad — engine milli SoA poke64 is unsigned-safe for non-negative coords.
    ox, oy, oz = minx - 1.0, miny - 1.0, minz - 1.0
    pos = [(x - ox, y - oy, z - oz) for x, y, z in raw_v]

    out_v: list[tuple[float, float, float]] = []
    out_vt: list[tuple[float, float]] = []
    out_vn: list[tuple[float, float, float]] = []
    out_f: list[tuple[int, int, int]] = []
    weld: dict[tuple[int, ...], int] = {}

    def emit_corner(
        vi: int,
        vni: int | None,
        face_n: tuple[float, float, float],
    ) -> int:
        p = pos[vi - 1]
        if vni is not None and 1 <= vni <= len(raw_vn):
            n = raw_vn[vni - 1]
        else:
            n = face_n
        uv = _atlas_uv(p, face_n)
        key = _qkey(p, uv, n)
        idx = weld.get(key)
        if idx is not None:
            return idx
        idx = len(out_v) + 1  # 1-based OBJ
        weld[key] = idx
        out_v.append(p)
        out_vt.append(uv)
        out_vn.append(n)
        return idx

    for tri in raw_faces:
        (a_vi, _a_vt, a_vn), (b_vi, _b_vt, b_vn), (c_vi, _c_vt, c_vn) = tri
        pa, pb, pc = pos[a_vi - 1], pos[b_vi - 1], pos[c_vi - 1]
        face_n = _face_normal(pa, pb, pc)
        ia = emit_corner(a_vi, a_vn, face_n)
        ib = emit_corner(b_vi, b_vn, face_n)
        ic = emit_corner(c_vi, c_vn, face_n)
        out_f.append((ia, ib, ic))

    # If still over cap (unlikely after weld), drop excess tris that need new verts.
    if len(out_v) > MESH_VERT_CAP or len(out_f) > MESH_TRI_CAP:
        # Re-weld is already applied; truncate faces that reference >cap (should not happen
        # often). Prefer keeping first MESH_TRI_CAP tris whose indices stay in range.
        kept: list[tuple[int, int, int]] = []
        for a, b, c in out_f:
            if a <= MESH_VERT_CAP and b <= MESH_VERT_CAP and c <= MESH_VERT_CAP:
                kept.append((a, b, c))
            if len(kept) >= MESH_TRI_CAP:
                break
        out_f = kept
        if len(out_v) > MESH_VERT_CAP:
            out_v = out_v[:MESH_VERT_CAP]
            out_vt = out_vt[:MESH_VERT_CAP]
            out_vn = out_vn[:MESH_VERT_CAP]

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w") as out:
        out.write(
            "# Cooked for JogEngine dust2_fps: Y-up→Z-up, scale "
            f"{scale}, recenter +octant, atlas UV+normals, f i/i/i\n"
        )
        out.write(f"# verts={len(out_v)} tris={len(out_f)}\n")
        for x, y, z in out_v:
            out.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
        for u, v in out_vt:
            out.write(f"vt {u:.6f} {v:.6f}\n")
        for nx, ny, nz in out_vn:
            out.write(f"vn {nx:.6f} {ny:.6f} {nz:.6f}\n")
        for a, b, c in out_f:
            out.write(f"f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c}\n")
    print(f"wrote {dst} verts={len(out_v)} tris={len(out_f)}")
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
