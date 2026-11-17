# Phase 4: IO Dispatcher asset load + audio mixer stub (no hitching CPU pool).
module streaming
version 0.1.0
root main.jog
require jog_engine ../..
require jog_sdl ../../deps/jog_sdl-0.1.2.jogz
link.linux SDL3
libdir.linux ../../prefix/lib64
libdir.linux ../../prefix/lib
