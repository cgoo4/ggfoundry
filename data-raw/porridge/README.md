# Porridge vector source

Original path geometry constructed for Carl Goodwin's ggfoundry package with
Codex assistance, September 2026. This folder retains the editable source and
generator; no external clip-art assets were used.

The shipped Cairo SVGs live in `inst/extdata/`. Normal installation, checking and
use of ggfoundry do not run this generator or require Python or librsvg.

To revise the artwork, edit `make_shapes.py` and run from the package root:

```sh
python3 data-raw/porridge/make_shapes.py
```

The developer needs `rsvg-convert` on PATH, or can supply its path explicitly:

```sh
python3 data-raw/porridge/make_shapes.py --rsvg-convert /opt/local/bin/rsvg-convert
```

The generator updates only its six source SVGs and six converted SVGs. A
`--output-dir` argument can redirect converted files for inspection. Different
librsvg versions may produce different serialisations; recheck rendering after
regeneration. A neutral `surface1` group makes modern Cairo output recognisable
to grImport2's older format detector without changing the geometry.

The outline is identical across variants. Fill contains the bowl body and zero,
one or two steam paths. All layers retain the same 200 × 200 canvas. Transparent
fill intentionally hides steam. Do not crop individual files independently.
