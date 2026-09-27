# ggfoundry (development version)

-   3 shapes ("bowl0", "bowl1" & "bowl2") added to a "container" set. Bowl body & steam share the `fill`; bowl & porridge outline use the `colour`; a transparent `fill` hides the steam while retaining the outline.
-   Aesthetics varying per observation, e.g. a continuous `fill`, are now respected for every shape, without requiring a `group = id` workaround, including when a shared group is explicit.
-   Repeated shapes with the same appearance reuse a styled template rather than rebuilding the artwork, substantially reducing grob construction time and memory for dense layers.
-   A `fill` of `NA` now renders the outline only, instead of dropping the shape with a warning.
-   `display_palette()` accepts repeated colours, maps each swatch to the intended colour, and gives a clear error for an empty palette.

# ggfoundry 0.3.1

-   2 shapes ("oak" & "hibiscus") added to a "leaf" set (#10).
-   Added support for `hjust` and `vjust` arguments to `geom_casting()` (#14).
-   Added a radial dendrogram with rotated leaves to the showcase article (#14).
-   New `display_palette()` uses a fillable shape for palette & hex codes (#9).
-   Uses `cli_abort`, instead of `abort`, for error message handling.
-   Refactor snapshot tests to use layer data rather than `png` files (#15).
-   Converted showcase vignette to article (#11).
-   Moved contrast section of get started vignette to article (#12).
-   File conversion from `SVG` to `Picture` objects now at build time (#13).
-   Added use of `use_spell_check()`.

# ggfoundry 0.2.0

-   2 shapes ("jar" & "tube") added to a "container" set (#1).
-   8 shapes ("sunflower1" to "sunflower8") added to a "flower" set (#4).
-   3 shapes ("gentoo", "chinstrap" & "adelie") added to a "penguin" set (#5).
-   Invalid-shape error message notes shape may be in development version (#2).
-   New `shapes_cast()` creates a data frame of available sets & shapes (#3).
-   Reduced `sysdata.rda` size by 23% switching from "bkzip2" to "xz" (#6).
-   Fixed shapes outside plotting area when zooming (#7).
-   Showcase vignette added.

# ggfoundry 0.1.1

-   Initial CRAN submission.
