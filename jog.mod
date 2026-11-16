# JogEngine — reusable CPU-3D packages (kind library).
# Demos path-require this tree; optional `jog-build pack` later.
module jog_engine
version 0.1.0
kind library

source engine

export engine.math
export engine.time
export engine.core
export engine.jobs
export engine.assets

# timing uses jog_sdl.sdl GetTicks/Delay.
require jog_sdl ./deps/jog_sdl-0.1.0.jogz

link.linux SDL3
link.emscripten SDL3
libdir.linux ./prefix/lib64
libdir.linux ./prefix/lib
libdir.emscripten ./prefix-emscripten/lib
