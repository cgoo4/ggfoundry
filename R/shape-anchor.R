# Intrinsic plotting anchors, in the expanded picture viewport's coordinates.
# grImport2 uses 5% padding: a 200 x 200 source has ranges -10..210.
# SVG y increases downward. The quill's ink contact is source (44,166).
# All other shapes keep their existing central anchor.
shape_anchor <- function(shape) {
  if (identical(shape, "quill")) {
    c((44 + 10) / 220, (200 - 166 + 10) / 220)
  } else {
    c(0.5, 0.5)
  }
}

# A square picture is centred inside a potentially rectangular viewport.
# snpc measures the shorter physical panel dimension; npc offsets would
# miss the point on rectangular panels. Rotate the physical displacement
# with the artwork so the ink contact stays at the plotting coordinate.
anchor_viewport <- function(vp, size, angle, anchor) {
  delta <- 0.5 - anchor
  theta <- angle * pi / 180
  dx <- size * (delta[1] * cos(theta) - delta[2] * sin(theta))
  dy <- size * (delta[1] * sin(theta) + delta[2] * cos(theta))
  vp$x <- vp$x + unit(dx, "snpc")
  vp$y <- vp$y + unit(dy, "snpc")
  vp
}
