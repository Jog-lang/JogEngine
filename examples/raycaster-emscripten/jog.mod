# Full CPU-3D raycaster for --target wasm32-emscripten.
# Shares world/texture/mesh/parallel with native; math/time from jog_engine; tick via jog_host_run_loop.
# go bands: run-to-completion under emscripten (JogCompiler RTC); yield still unsupported.
module raycaster_emscripten
version 0.1.0
root main.jog
require jog_engine ../..
require jog_sdl ../../deps/jog_sdl-0.1.0.jogz
source ../raycaster/world.jog
source ../raycaster/texture.jog
source ../raycaster/mesh.jog
source ../raycaster/parallel.jog
link.emscripten SDL3
libdir.emscripten ../../prefix-emscripten/lib
