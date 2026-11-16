# Agents (JogEngine)

## Jog knowledge

- Jog language notes, plans, checklists and the friction log live in JogDocs:
  Fedora `~/Documents/Projects/Jog/JogDocs` (or `/home/plague_doc/Documents/Projects/Jog/JogDocs`);
  Windows `D:/Projects/Jog/JogDocs`
  (https://github.com/Jog-lang/JogDocs).
- Read JogDocs `AGENTS.md` first, then `guide/JogQuickRef.md` before writing or reviewing Jog.
- Agent skills canon: JogDocs `.agents/skills/` (pointer: `.agents/skills/README.md` here when present). See `guide/UsingJogDocs.md`.
- Log rough edges in JogDocs `bootstrap/Friction.md`. Prefer the Fedora tree for SDL / engine smoke.

## This repo

- `kind library` module `jog_engine` plus raycaster demos (native + emscripten).
- Fedora path: `~/Documents/Projects/Jog/JogEngine`.
- **Toolchain: JogCompiler v2 + JogBuild v2** (`JOG=~/.local/bin/jog-v2`, pack-capable `jog-build`). SDL via packed `deps/jog_sdl-*.jogz` (see `scripts/pack-deps.sh`), not a path into JogSDL sources. Emscripten browser: tip with JogCompiler #39 + #40.
- Ivan writes Jog engine/demo logic. Move/adapt existing sources; do not invent new engine gameplay APIs.
- Friction-first: if the compiler / JogBuild / docs block a correct layout, fix those and log Friction — do not invent JogEngine workarounds.
- Build/smoke: see `README.md`.
