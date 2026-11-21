# dust2_fps

First-person walk of a CC-BY low-poly **de_dust2** mesh on JogEngine.

Default present is the **CPU soft-mesh** oracle. Optional **SDL_GPU + Vulkan + SPIR-V** PresentBackend:

```bash
JOGENGINE_PRESENT=gpu ./out/dust2_fps
# alias:
JOGENGINE_PRESENT=vulkan ./out/dust2_fps
```

## Controls

| Input | Action |
|---|---|
| WASD | Move / strafe |
| Mouse / arrows | Look (yaw + pitch) |
| Space | Jump (when grounded) |
| Esc | Quit |

## Run

```bash
export JOG=~/.local/bin/jog-v2
export JOG_BUILD=~/.local/bin/jog-build
cd examples/dust2_fps
"$JOG_BUILD" build -o out/dust2_fps
./out/dust2_fps
# smoke (walls + jump; GPU line when PRESENT=gpu):
JOGENGINE_DUST2_SMOKE=1 ./out/dust2_fps
JOGENGINE_PRESENT=gpu JOGENGINE_DUST2_SMOKE=1 ./out/dust2_fps
```

`jog_f32_bits` is linked from the JogCompiler runtime (no host `libf32bits`).


CPU framebuffer is **320×180** (window scaled). GPU path presents the **960×540** swapchain with Lambert SPIR-V + atlas.

## Assets

See [`assets/ATTRIBUTION.md`](assets/ATTRIBUTION.md).

- `de_dust2.obj` — cooked Z-up mesh (CPU SoA path)
- `de_dust2.meshbin` — interleaved f32 POS/UV/NRM + u32 indices (GPU upload)
- `atlas.ppm` — 64×64 albedo
- `mesh.vert.spv` / `mesh.frag.spv` — Vulkan SPIR-V (from `engine/render3d/shaders`)

Rebuild cook / atlas / meshbin:

```bash
python3 tools/cook_obj.py /path/to/de_dust2.obj assets/de_dust2.obj
python3 tools/gen_atlas.py --out assets/atlas.ppm
# meshbin: see tools/cook notes in cook_obj.py (--meshbin if present)
```

## Notes

- Wall collision: near-vertical tris → `engine.collision` AABB3; CPU soft-mesh stays the oracle.
- SysV 7th stack-arg alignment fixed in JogCompiler #43 (≤6-arg workaround dropped).
- `jog_sdl` **0.1.3** createinfo pack plane required.
