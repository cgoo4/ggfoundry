# Writing and Halloween artwork

Original vector artwork for eleven ggfoundry development shapes. The writing set contains `bookfront`, `bookopen`, `nib`, `fountainpen`, `inkpot` and `quill`. The Halloween set contains `skeleton`, `ghost`, `spiderweb`, `grimreaper` and `gravestone`.

`make_shapes.py` is the editable source of truth. `source-svg/` contains 22 black SVGs, with separate colour and fill layers. `preview-svg/` contains coloured and outline-only standalone previews. The generator writes the 22 matching Cairo SVGs to the package's `inst/extdata/`. All layers share a 200 by 200 canvas; never crop an outline or fill independently.

Run from the package root:

```sh
python3 data-raw/writing-halloween/make_shapes.py
```

Use `--rsvg-convert /path/to/rsvg-convert` if necessary. `--output-dir` and `--preview-dir` allow alternative destinations. Regeneration requires Python's standard library and librsvg's `rsvg-convert`; neither is a package runtime dependency. The Cairo output retains the neutral `surface1` wrapper used by grImport2's format detector.

Outlines and interior details use variable-width filled paths. Interior details are cut out of the fill so they survive the package's outline-then-fill drawing order. No downloaded artwork, raster images, masks, gradients or runtime fonts are used.

The quill's ink contact is source coordinate `(44, 166)`. Its feather and ink mark remain on this canvas, while the renderer places the ink contact at the plotted point. Preserve this coordinate or update `R/shape-anchor.R` and the corresponding tests with any artwork change. Its ink mark uses `colour`, independent of `fill`. Legends centre the complete quill.
