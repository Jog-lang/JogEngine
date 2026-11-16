# JogEngine

Reusable CPU-3D packages for Jog (`module jog_engine`, `kind library`) plus a Wolfenstein-style software raycaster demo (native and Emscripten).

| | |
|---|---|
| Repo | https://github.com/Jog-lang/JogEngine |
| Local path | `/home/plague_doc/Documents/Projects/Jog/JogEngine` |
| Toolchain | JogCompiler **v2** + JogBuild **v2** (pack / `.jogz`). Emscripten browser needs tip **v2** with [#39](https://github.com/Jog-lang/JogCompiler/pull/39) + [#40](https://github.com/Jog-lang/JogCompiler/pull/40) (fixes MainLoop `RuntimeError: unreachable`). |

## Layout

```
JogEngine/
  jog.mod                 # kind library; source engine; export math/time/core/jobs/assets
  engine/math/            # Vec2 / view basis (avoid struct returns on hot path)
  engine/time/            # timing_* (jog_sdl.sdl GetTicks/Delay)
  engine/core/            # phases, fixed timestep, pause
  engine/jobs/            # dispatcher_pool / go / coro_drain helpers
  engine/assets/          # bump-safe CPU tex_* helpers
  deps/jog_sdl-*.jogz     # packed JogSDL (gitignored; scripts/pack-deps.sh)
  examples/raycaster/     # native demo
  examples/raycaster-emscripten/
  scripts/                # pack-deps + SDL3 prefix helpers (from JogSDL)
  prefix/                 # local SDL3 3.4.18 (gitignored); symlink sibling JogSDL/prefix OK
```

Import engine packages as `jog_engine.engine.<pkg>` (directory `source engine` keeps the `engine.` segment, same pattern as `jog_sdl.sdl.window`).

## Setup

```bash
export JOG=~/.local/bin/jog-v2          # tip v2: #39 mangle + #40 extern emit for wasm browser
export JOG_BUILD=~/.local/bin/jog-build # must support `pack`

cd /home/plague_doc/Documents/Projects/Jog/JogEngine
./scripts/pack-deps.sh                  # → deps/jog_sdl-0.1.0.jogz from ../JogSDL

# SDL3 prefix (or: ln -s ../JogSDL/prefix prefix && ln -s ../JogSDL/prefix-emscripten prefix-emscripten)
./scripts/fetch-sdl3.sh
./scripts/build-sdl3.sh
# wasm:
./scripts/build-sdl3-emscripten.sh
```

## Native raycaster

```bash
export JOG JOG_BUILD
cd examples/raycaster
"$JOG_BUILD" build -o out/raycaster
JOGENGINE_RAYCASTER_SMOKE=1 "$JOG_BUILD" run -o out/raycaster
# or: JOGENGINE_RAYCASTER_SMOKE=1 ./out/raycaster
```

`JOGENGINE_RAYCASTER_SERIAL=1` forces serial column bands (no go pool).

## Emscripten raycaster

```bash
source ~/emsdk/emsdk_env.sh
cd examples/raycaster-emscripten
./start.sh --rebuild
# or: "$JOG_BUILD" build --target wasm32-emscripten -o out/raycaster.html
```

Browser smoke: `JOGENGINE_RAYCASTER_SMOKE=1` (Module env / start.sh notes).

## Library check

```bash
cd /home/plague_doc/Documents/Projects/Jog/JogEngine
"$JOG_BUILD" check .
```
