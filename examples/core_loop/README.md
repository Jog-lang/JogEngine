# core_loop

Headless smoke for the first engine core slice: `Clock` / `System` / `PhaseQueue` / `World` / `App`.

```bash
export JOG=~/.local/bin/jog-v2
export JOG_BUILD=~/.local/bin/jog-build
export JOG_ROOT=~/Documents/Projects/Jog/JogCompiler   # if jog roots miss std/core

cd examples/core_loop
# Host stub required while engine.render3d.gpu_present references jog_f32_bits:
cc -shared -fPIC -O2 -o libf32bits.so f32bits.S
"$JOG_BUILD" build -o out/core_loop
JOGENGINE_CORE_SMOKE=1 ./out/core_loop
```

Expect: `core_loop smoke ok`.
