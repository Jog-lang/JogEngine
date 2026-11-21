# JogEngine — reusable CPU-3D packages (kind library).
# Demos path-require this tree; optional `jog-build pack` later.
module jog_engine
version 0.1.0
kind library

source engine

export engine.math
export engine.time
export engine.core
export engine.world
export engine.app
export engine.jobs
export engine.assets
export engine.msg
export engine.collision
export engine.render2d
export engine.render3d
export engine.audio

# timing uses jog_sdl.sdl GetTicks/Delay.
require jog_sdl ./deps/jog_sdl-0.1.2.jogz

link.linux SDL3
link.emscripten SDL3
libdir.linux ./prefix/lib64
libdir.linux ./prefix/lib
libdir.emscripten ./prefix-emscripten/lib
