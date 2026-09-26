# Changelog

## ggfoundry (development version)

- 3 shapes (“bowl0”, “bowl1” & “bowl2”) added to a “container” set. Bowl
  body & steam share the `fill`; bowl & porridge outline use the
  `colour`; a transparent `fill` hides the steam while retaining the
  outline.
- Aesthetics varying per observation, e.g. a continuous `fill`, are now
  respected for every shape, without requiring a `group = id`
  workaround, including when a shared group is explicit.

## ggfoundry 0.3.1

CRAN release: 2024-07-06

- 2 shapes (“oak” & “hibiscus”) added to a “leaf” set
  ([\#10](https://github.com/cgoo4/ggfoundry/issues/10)).
- Added support for `hjust` and `vjust` arguments to
  [`geom_casting()`](https://cgoo4.github.io/ggfoundry/reference/geom_casting.md)
  ([\#14](https://github.com/cgoo4/ggfoundry/issues/14)).
- Added a radial dendrogram with rotated leaves to the showcase article
  ([\#14](https://github.com/cgoo4/ggfoundry/issues/14)).
- New
  [`display_palette()`](https://cgoo4.github.io/ggfoundry/reference/display_palette.md)
  uses a fillable shape for palette & hex codes
  ([\#9](https://github.com/cgoo4/ggfoundry/issues/9)).
- Uses `cli_abort`, instead of `abort`, for error message handling.
- Refactor snapshot tests to use layer data rather than `png` files
  ([\#15](https://github.com/cgoo4/ggfoundry/issues/15)).
- Converted showcase vignette to article
  ([\#11](https://github.com/cgoo4/ggfoundry/issues/11)).
- Moved contrast section of get started vignette to article
  ([\#12](https://github.com/cgoo4/ggfoundry/issues/12)).
- File conversion from `SVG` to `Picture` objects now at build time
  ([\#13](https://github.com/cgoo4/ggfoundry/issues/13)).
- Added use of `use_spell_check()`.

## ggfoundry 0.2.0

CRAN release: 2024-06-09

- 2 shapes (“jar” & “tube”) added to a “container” set
  ([\#1](https://github.com/cgoo4/ggfoundry/issues/1)).
- 8 shapes (“sunflower1” to “sunflower8”) added to a “flower” set
  ([\#4](https://github.com/cgoo4/ggfoundry/issues/4)).
- 3 shapes (“gentoo”, “chinstrap” & “adelie”) added to a “penguin” set
  ([\#5](https://github.com/cgoo4/ggfoundry/issues/5)).
- Invalid-shape error message notes shape may be in development version
  ([\#2](https://github.com/cgoo4/ggfoundry/issues/2)).
- New
  [`shapes_cast()`](https://cgoo4.github.io/ggfoundry/reference/shapes_cast.md)
  creates a data frame of available sets & shapes
  ([\#3](https://github.com/cgoo4/ggfoundry/issues/3)).
- Reduced `sysdata.rda` size by 23% switching from “bkzip2” to “xz”
  ([\#6](https://github.com/cgoo4/ggfoundry/issues/6)).
- Fixed shapes outside plotting area when zooming
  ([\#7](https://github.com/cgoo4/ggfoundry/issues/7)).
- Showcase vignette added.

## ggfoundry 0.1.1

CRAN release: 2024-05-28

- Initial CRAN submission.
