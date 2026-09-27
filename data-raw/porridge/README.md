# Redrawn porridge bowl artwork

Original editable vector geometry constructed for Carl Goodwin's ggfoundry
package. This revision follows the supplied bowl reference with a wavering
tilted rim, uneven porridge mound, loose texture marks and small foot.

The generator writes exactly these six runtime assets, preserving their names:

```text
inst/extdata/container-bowl0_col-cairo.svg
inst/extdata/container-bowl0_fill-cairo.svg
inst/extdata/container-bowl1_col-cairo.svg
inst/extdata/container-bowl1_fill-cairo.svg
inst/extdata/container-bowl2_col-cairo.svg
inst/extdata/container-bowl2_fill-cairo.svg
```

Run from the package root:

```sh
python3 data-raw/porridge/make_shapes.py
```

The developer needs `rsvg-convert` on PATH, or can provide its path explicitly:

```sh
python3 data-raw/porridge/make_shapes.py --rsvg-convert /opt/local/bin/rsvg-convert
```

The existing `--output-dir` option is supported. An optional `--preview-dir`
writes coloured standalone SVGs for review. Neither Python nor librsvg is an
additional package runtime dependency; the six converted SVGs are supplied.

`source-svg/` retains the editable black vector paths. The Cairo output keeps
the neutral `surface1` group used by grImport2's format detector. Each outline
is identical; the first fill path contains the common bowl, rim and foot, and
0, 1 or 2 additional fill paths add the steam. The porridge interior remains
transparent, with texture marks in the outline layer.

All layers retain a 200 x 200 canvas. Do not crop individual files independently.
The rim stays near y = 100, keeping the existing plot anchor. The deeper body,
higher mound and small foot deliberately change the visible silhouette.

Keep this generator and the matching source files together with the six
runtime replacements, so future regeneration preserves the revised artwork.
