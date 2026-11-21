# Dust2 FPS demo: OBJ soft-mesh + AABB3 walk/jump; optional SDL_GPU present.
module dust2_fps
version 0.1.0
root main.jog
require jog_engine ../..
require jog_sdl ../../deps/jog_sdl-0.1.3.jogz
source bake.jog
source player.jog
link.linux SDL3
libdir.linux .
libdir.linux ../../prefix/lib64
libdir.linux ../../prefix/lib
