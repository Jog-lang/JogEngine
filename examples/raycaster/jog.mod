# Proto-3D raycaster demo: engine math/time + JogSDL via .jogz.
module raycaster
version 0.1.0
root main.jog
require jog_engine ../..
require jog_sdl ../../deps/jog_sdl-0.1.3.jogz
source world.jog
source texture.jog
source mesh.jog
source parallel.jog
link.linux SDL3
link.emscripten SDL3
libdir.linux ../../prefix/lib64
libdir.linux ../../prefix/lib
libdir.emscripten ../../prefix-emscripten/lib
