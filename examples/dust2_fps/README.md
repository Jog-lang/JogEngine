# dust2_fps

First-person walk of a CC-BY low-poly **de_dust2** mesh on JogEngine’s CPU soft-raster path.

## Controls

| Input | Action |
|---|---|
| WASD | Move / strafe |
| Mouse / arrows | Look (yaw + horizon pitch) |
| Space | Jump (when grounded) |
| Esc | Quit |

## Run

```bash
export JOG=~/.local/bin/jog-v2
export JOG_BUILD=~/.local/bin/jog-build
cd examples/dust2_fps
"$JOG_BUILD" build -o out/dust2_fps
./out/dust2_fps
# smoke (walls + jump):
JOGENGINE_DUST2_SMOKE=1 ./out/dust2_fps
```

Framebuffer is **320×180** (window scaled). Present stays on the CPU streaming-texture path; GPU `PresentBackend` is not used.

## Assets

See [`assets/ATTRIBUTION.md`](assets/ATTRIBUTION.md). Cooked OBJ: Y-up → Z-up, scale `0.5`, recenter into the **positive octant** (engine milli SoA), positions + triangles only (flat normal shading; no MTL textures in v1).

Rebuild cook (Fedora host):

```bash
python3 tools/cook_obj.py /path/to/de_dust2.obj assets/de_dust2.obj
```

## Notes

- Wall collision: near-vertical tris → `engine.collision` AABB3 grid; resolution is demo-local (axis slide).
- Floor: upward faces stamped into a height grid; gravity + Space jump.
- Soft-mesh uses a full per-pixel Z-buffer and distance cull (`DRAW_DIST`).
