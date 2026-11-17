# Asset attribution

## de_dust2.obj

- **Title:** de_dust2 (CS map) — low-poly recreation
- **Author:** vrchris
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Source (Sketchfab):** https://sketchfab.com/3d-models/de-dust2-cs-map-056008d59eb849a29c0ab6884c0c3d87
- **Mirror used for download:** https://github.com/AlexanderMladenov/EmbreeRT/blob/master/resources/de_dust2.obj

### Cook notes (JogEngine)

Host cook (Fedora): triangulated OBJ with parallel `v`/`vt`/`vn` and `f i/i/i`; Y-up → engine Z-up (`(x,y,z) → (x,z,y)`); uniform scale `0.5`; recenter into the positive octant (engine milli SoA). Source `vt` ignored — atlas UVs from face-normal dominant axis into 4 flat-color quadrants (see `tools/gen_atlas.py`). Sync load only for now; dynamic mesh streaming deferred.

License text: https://creativecommons.org/licenses/by/4.0/
