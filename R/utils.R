#' Cast a shape from a pair of SVG files
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_shape <- \(shape, colour, fill, size, angle, x, y, hjust, vjust, anchor = TRUE) {
  col_grob <- picture_lst[grepl(paste0(shape, "_col"), names(picture_lst))][[1]]
  fill_grob <- picture_lst[grepl(paste0(shape, "_fill"), names(picture_lst))][[
    1
  ]]

  grob <- gTree(
    children = gList(
      cast_layers(col_grob, colour, size, angle, x, y, hjust, vjust),
      cast_layers(fill_grob, fill, size, angle, x, y, hjust, vjust)
    )
  )

  if (anchor && identical(shape, "quill")) {
    grob <- place_template(grob, size, angle, x, y, hjust, vjust,
                           anchor = shape_anchor(shape))
  }
  grob
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

  place_template(template, size, angle, x, y, hjust, vjust,
                 anchor = shape_anchor(shape))
}

#' Re-place a styled template for one observation
#'
#' Copies the grob tree, editing only the placement viewports; the styled
#' picture grobs are shared with the template and left untouched.
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
place_template <- \(grob, size, angle, x, y, hjust, vjust, anchor = c(0.5, 0.5)) {
  grob$vp <- place_viewports(grob$vp, size, angle, x, y, hjust, vjust, anchor)

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
        vjust = vjust,
        anchor = anchor
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
place_viewports <- \(vp, size, angle, x, y, hjust, vjust, anchor = c(0.5, 0.5)) {
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
      vjust = vjust,
      anchor = anchor
    )
    return(vp)
  }

  if (identical(vp$name, "picture.scale") && !identical(anchor, c(0.5, 0.5))) {
    # Quill geometry stays within its canvas; the enclosing plot clips it.
    # Inner clipping cannot be resolved by grid after rotation.
    vp$clip <- FALSE
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
    if (!identical(anchor, c(0.5, 0.5))) {
      vp <- anchor_viewport(vp, size, angle, anchor)
    }
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
      default.units = "npc",
      expansion = 0.05
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
