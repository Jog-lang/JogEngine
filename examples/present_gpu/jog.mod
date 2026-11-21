# Phase 5: PresentBackend GPU/Vulkan smoke (CPU remains default oracle).
module present_gpu
version 0.1.0
root main.jog
require jog_engine ../..
require jog_sdl ../../deps/jog_sdl-0.1.3.jogz
link.linux SDL3
libdir.linux ../../prefix/lib64
libdir.linux ../../prefix/lib
