#' Arbitrary hand-crafted fillable shapes for ggplot2
#'
#' @description `r lifecycle::badge('experimental')`
#'
#' Arbitrary hand-crafted colourable and fillable shapes for ggplot2.
#'
#' New shapes may be feature requested via a Github issue.
#'
#' @details Behind the scenes, a pair of hand-drawn vector images (outline &
#'   fill) are converted into Cairo graphics library SVG files, then into grid
#'   graphical objects (grobs) for use in a ggplot2 layer.
#'
#'   By default, the "violin" shape is used.
#'
#'   If the shape is mapped to a variable, e.g. `aes(shape = factor(cyl))`, then
#'   [scale_shape_manual()] is also required to explicitly name the desired
#'   shapes as a character vector (see examples). This is because standard
#'   shapes are associated with a number, e.g. a circle is 19, whereas
#'   `geom_casting()` shapes are associated only with character strings.
#'
#'   In addition to the supported aesthetics below, `nudge_x` and `nudge_y` are
#'   also respected.
#'
#' @inheritParams ggplot2::geom_point
#'
#' @section Aesthetics:
#' \code{geom_casting()} understands the following aesthetics (required aesthetics are in bold):
#' \itemize{
#'  \item \strong{\code{x}}
#'  \item \strong{\code{y}}
#'  \item \code{alpha}
#'  \item \code{angle}
#'  \item \code{colour}
#'  \item \code{fill}
#'  \item \code{group}
#'  \item \code{shape}
#'  \item \code{size}
#' }
#' Learn more about setting these aesthetics
#' in \code{vignette("ggplot2-specs")}
#'
#' @export
#'
#' @return A geom layer that can be added to a ggplot.
#'
#' @examples
#' library(ggplot2)
#'
#' # "Baby violin" shape by default
#' p <- ggplot(mtcars, aes(wt, mpg))
#' p + geom_casting()
#'
#' # Change shape & fill
#' p + geom_casting(shape = "box", fill = "lightgreen")
#'
#' # Shapes mapped to a variable
#' ggplot(mtcars, aes(wt, mpg, fill = factor(cyl))) +
#'   geom_casting(aes(shape = factor(cyl))) +
#'   scale_shape_manual(values = c("violin", "dendro", "box"))
geom_casting <- \(mapping = NULL, data = NULL,
  stat = "identity", position = "identity",
  ...,
  na.rm = FALSE,
  show.legend = NA,
  inherit.aes = TRUE) {
  layer(
    data = data,
    mapping = mapping,
    stat = stat,
    geom = GeomCasting,
    position = position,
    show.legend = show.legend,
    inherit.aes = inherit.aes,
    params = list(
      na.rm = na.rm,
      ...
    )
  )
}

#' Get the names of available shapes
#'
#' @description `r lifecycle::badge('experimental')`
#'
#'   Create a data frame of available shapes and associated sets. This may be
#'   filtered and used as a vector of strings in `scale_shape_manual`.
#'
#' @export
#'
#' @return A data frame of available sets and shapes.
#'
#' @examples
#' # Returns a data frame of available shapes
#' shapes_cast()
shapes_cast <- \(){
  df <- data.frame(
    set = sub("(.*)-.*", "\\1", names(picture_lst)),
    shape = sub(".*-(.*)_.*", "\\1", names(picture_lst))
  )

  df[order(df$set, df$shape), ] |> unique()
}

#' Geom object for casting a shape (not used directly by end user)
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
#' @export
GeomCasting <- ggproto("GeomCasting", Geom,
  required_aes = c("x", "y"),
  non_missing_aes = c("size", "shape", "colour", "fill"),
  default_aes = aes(
    shape = "violin", size = 0.1, colour = "black",
    alpha = NA, angle = 0, fill = "pink"
  ),

  draw_panel = \(self, data, panel_params, coord,
    na.rm = FALSE, nudge_x = 0, nudge_y = 0) {
    coords <- coord$transform(data, panel_params)
    coords <- subset(coords, x >= 0 & x <= 1 & y >= 0 & y <= 1)

    lst <- split(coords, coords$group)

    grobs <- lapply(lst, \(df) {

      valid_shapes <- shapes_cast()$shape

      if (is_empty(which(df$shape[1] %in% valid_shapes))) {
        msg <- paste0(
          df$shape[1],
          " may be a typo or currently in the development version?"
          )
        abort(msg)
      }

      cast_shape(
        shape = df$shape[1],
        colour = alpha(df$colour[1], df$alpha[1]),
        fill = fill_alpha(df$fill[1], df$alpha[1]),
        size = df$size[1],
        angle = df$angle[1],
        x = df$x + nudge_x,
        y = df$y + nudge_y
      )
    })

    gTree("geom_casting", children = do.call(gList, grobs))
  },

  draw_key = \(data, params, size) {
    if (is.null(data$shape)) {
      data$shape <- "violin"
    }

    cast_shape(
      shape = data$shape,
      colour = alpha(data$colour, data$alpha),
      fill = fill_alpha(data$fill, data$alpha),
      size = 1,
      angle = 0,
      x = 0.5,
      y = 0.5
    )
  }
)
