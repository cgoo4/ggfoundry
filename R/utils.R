
#' Cast a shape from a pair of SVG files
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_shape <- \(shape, colour, fill, size, angle, x, y, hjust, vjust) {
  col_grob <- picture_lst[grepl(paste0(shape, "_col"), names(picture_lst))][[1]]
  fill_grob <- picture_lst[grepl(paste0(shape, "_fill"), names(picture_lst))][[1]]

  gTree(
    children = gList(
      cast_layers(col_grob, colour, size, angle, x, y, hjust, vjust),
      cast_layers(fill_grob, fill, size, angle, x, y, hjust, vjust)
    )
  )
}

#' Used by cast_shape to process each layer
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_layers <- \(picture, col, size, angle, x, y, hjust, vjust) {
  picture |>
    symbolsGrob(
      x = x, y = y, size = size, angle = angle,
      just = c(hjust, vjust), default.units = "npc"
      ) |>
    removeGrob("Poly", grep = TRUE, global = TRUE) |>
    editGrob(
      "Path",
      gp = gpar(col = col, fill = col),
      grep = TRUE, global = TRUE, warn = FALSE
    )
}
