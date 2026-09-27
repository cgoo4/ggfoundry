#' Cast a shape from a pair of SVG files
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_shape <- \(shape, colour, fill, size, angle, x, y, hjust, vjust) {
  col_grob <- picture_lst[grepl(paste0(shape, "_col"), names(picture_lst))][[1]]
  fill_grob <- picture_lst[grepl(paste0(shape, "_fill"), names(picture_lst))][[
    1
  ]]

  gTree(
    children = gList(
      cast_layers(col_grob, colour, size, angle, x, y, hjust, vjust),
      cast_layers(fill_grob, fill, size, angle, x, y, hjust, vjust)
    )
  )
}

#' Cast a repeated style from a per-panel template cache
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_style <- \(shape, colour, fill, size, angle, x, y, hjust, vjust, cache) {
  key <- paste(shape, colour, fill)
  template <- cache[[key]]

  # Converting a picture to grobs is expensive: build the styled template
  # once per unique style, then re-place a copy for every observation.
  if (is.null(template)) {
    template <- cast_shape(shape, colour, fill, size, angle, x, y, hjust, vjust)
    cache[[key]] <- template
  }

  place_template(template, size, angle, x, y, hjust, vjust)
}

#' Re-place a styled template for one observation
#'
#' Copies the grob tree, editing only the placement viewports; the styled
#' picture grobs are shared with the template and left untouched.
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
place_template <- \(grob, size, angle, x, y, hjust, vjust) {
  grob$vp <- place_viewports(grob$vp, size, angle, x, y, hjust, vjust)

  if (inherits(grob, "gTree") && !is.null(grob$children)) {
    grob$children <- do.call(
      gList,
      lapply(
        grob$children,
        place_template,
        size = size,
        angle = angle,
        x = x,
        y = y,
        hjust = hjust,
        vjust = vjust
      )
    )
  }

  grob
}

#' Edit the placement of a "picture.shape" viewport
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
place_viewports <- \(vp, size, angle, x, y, hjust, vjust) {
  if (is.null(vp)) {
    return(NULL)
  }

  if (inherits(vp, "vpStack")) {
    vp[] <- lapply(
      vp,
      place_viewports,
      size = size,
      angle = angle,
      x = x,
      y = y,
      hjust = hjust,
      vjust = vjust
    )
    return(vp)
  }

  if (identical(vp$name, "picture.shape")) {
    # Mirror how viewport() stores a justification
    just <- viewport(just = c(hjust, vjust))$justification
    vp$x <- unit(x, "npc")
    vp$y <- unit(y, "npc")
    vp$width <- unit(size, "npc")
    vp$height <- unit(size, "npc")
    vp$angle <- angle
    vp$justification <- just
    vp$valid.just <- just
  }

  vp
}

#' Used by cast_shape to process each layer
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_layers <- \(picture, col, size, angle, x, y, hjust, vjust) {
  picture |>
    symbolsGrob(
      x = x,
      y = y,
      size = size,
      angle = angle,
      just = c(hjust, vjust),
      default.units = "npc"
    ) |>
    removeGrob("Poly", grep = TRUE, global = TRUE) |>
    editGrob(
      "Path",
      gp = gpar(col = col, fill = col),
      grep = TRUE,
      global = TRUE,
      warn = FALSE
    )
}
