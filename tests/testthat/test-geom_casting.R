test_that("fills & manual shapes", {
  p <- ggplot(mtcars, aes(wt, mpg, fill = factor(cyl))) +
    geom_casting(aes(shape = factor(cyl))) +
    scale_shape_manual(values = c("violin", "box", "dendro"))

  expect_snapshot(layer_data(p, 1))
})

test_that("bad shape", {
  expect_snapshot(
    ggplot(mtcars, aes(wt, mpg)) +
      geom_casting(shape = "non-shape"),
    error = TRUE
  )
})

test_that("available sets & shapes", {
  expect_snapshot(
    shapes_cast()
  )
})

test_that("shapes clipped when zooming", {
  p <- ggplot(mtcars, aes(wt, mpg)) +
    geom_casting(size = 0.1, shape = "violin") +
    geom_point() +
    coord_cartesian(xlim = c(1, 4))

  expect_snapshot(p[["coordinates"]][["limits"]][["x"]])
})

test_that("display a palette", {
  p <- display_palette(
    c("red", "blue"),
    "Example",
    colour = "grey",
    shape = "jar"
  )

  expect_snapshot(layer_data(p, 1))
  expect_snapshot(layer_data(p, 2))
})

# Drawing-path regression: aesthetics must be honoured per observation,
# not taken from the first row of a group. Helpers inspect the grobs
# actually produced by GeomCasting$draw_panel().

collect_gp_fills <- function(grob) {
  fills <- character(0)
  if (!is.null(grob$gp$fill)) {
    fills <- grob$gp$fill
  }
  if (!is.null(grob$children)) {
    fills <- c(fills, unlist(lapply(grob$children, collect_gp_fills)))
  }
  unique(fills)
}

per_row_fills <- function(grob) {
  # Row grobs: children 1 & 2 are the outline & fill picture layers
  lapply(grob$children, \(row) collect_gp_fills(row$children[[2]]))
}

shape_viewports <- function(x) {
  if (is.null(x)) {
    return(list())
  }
  if (identical(x$name, "picture.shape")) {
    return(list(x))
  }
  found <- list()
  if (!is.null(x$children)) {
    found <- c(
      found,
      unlist(lapply(x$children, shape_viewports), recursive = FALSE)
    )
  }
  if (inherits(x, "vpStack")) {
    found <- c(found, unlist(lapply(x, shape_viewports), recursive = FALSE))
  }
  if (!is.null(x$vp)) {
    found <- c(found, shape_viewports(x$vp))
  }
  found
}

built_layer_grob <- function(p, i = 1) {
  layer_grob(p, i)[[1]]
}

drawn_rows <- function(data, shape = "jar", base = data.frame(x = 1, y = 1)) {
  p <- ggplot(base, aes(x, y)) +
    geom_casting(shape = shape)

  b <- ggplot_build(p)
  built <- b$data[[1]][rep(1, nrow(data)), ]
  rownames(built) <- NULL
  # Only aesthetics are varied; built coordinates stay inside the panel
  aes_cols <- intersect(names(data), names(built))
  built[aes_cols] <- data[aes_cols]
  built$group <- 1L
  built$PANEL <- 1L

  GeomCasting$draw_panel(
    built,
    b$layout$panel_params[[1]],
    b$layout$coord
  )
}

test_that("continuous fill is drawn per observation", {
  # Implicit grouping
  df <- data.frame(x = 1:7, temp = c(5, 18, 32, 47, 63, 81, 96))
  p <- ggplot(df, aes(x, 1, fill = temp)) +
    geom_casting(shape = "bowl2", colour = "black") +
    scale_fill_viridis_c(limits = c(0, 100))

  fills <- per_row_fills(built_layer_grob(p))
  expect_length(fills, 7)
  expect_length(unique(unlist(fills)), 7)

  # Explicit shared group must not collapse the fills
  p_grouped <- p + aes(group = 1)
  fills_grouped <- per_row_fills(built_layer_grob(p_grouped))
  expect_length(unique(unlist(fills_grouped)), 7)
})

test_that("existing shape honours varied alpha, size & angle per observation", {
  df <- data.frame(
    alpha = c(0.3, 0.6, 1),
    size = c(0.05, 0.1, 0.2),
    angle = c(0, 30, 60)
  )

  grob <- drawn_rows(df, shape = "jar")
  expect_length(grob$children, 3)

  # Alpha varies the drawn colour of each row
  cols <- vapply(
    grob$children,
    \(row) unique(collect_gp_fills(row$children[[1]])),
    character(1)
  )
  expect_length(unique(cols), 3)

  # Size & angle vary the shape viewport of each row
  dims <- vapply(
    grob$children,
    \(row) {
      vp <- shape_viewports(row)[[1]]
      paste(vp$width, vp$angle)
    },
    character(1)
  )
  expect_length(unique(dims), 3)
  expect_match(dims[3], "60")
})

test_that("shared aesthetics across a group still render together", {
  df <- data.frame(
    fill = "skyblue",
    size = c(0.05, 0.1, 0.15),
    angle = c(0, 20, 40)
  )

  grob <- drawn_rows(df)
  cols <- vapply(
    grob$children,
    \(row) unique(collect_gp_fills(row$children[[2]])),
    character(1)
  )
  expect_length(cols, 3)
  expect_true(all(cols == "#87CEEBFF"))

  # Each row keeps its own placement from the shared template
  dims <- vapply(
    grob$children,
    \(row) {
      vp <- shape_viewports(row)[[1]]
      paste(vp$width, vp$angle)
    },
    character(1)
  )
  expect_length(unique(dims), 3)
})

test_that("display_palette accepts repeated colours", {
  p <- display_palette(c("red", "red", "blue"), "Repeated")
  expect_snapshot(layer_data(p, 1))
})

test_that("display_palette rejects an empty palette", {
  expect_snapshot(display_palette(character(0), "Empty"), error = TRUE)
})

test_that("outline-only fill = NA retains the outline", {
  df <- data.frame(x = 1, y = 1, fill = NA)

  grob <- drawn_rows(df, shape = "bowl2")
  expect_length(grob$children, 1)

  # Outline layer keeps its colour; fill layer (bowl body & steam) is NA
  outline_fills <- collect_gp_fills(grob$children[[1]]$children[[1]])
  expect_false(any(outline_fills == "transparent" | is.na(outline_fills)))

  fill_fills <- collect_gp_fills(grob$children[[1]]$children[[2]])
  expect_true(all(is.na(fill_fills)))
})

test_that("repeated styles reuse a template but keep per-row placement", {
  df <- data.frame(
    x = c(0.9, 1.1, 0.9, 1.1),
    y = c(0.9, 0.9, 1.1, 1.1),
    fill = "pink",
    colour = "black",
    size = 0.1,
    angle = 15
  )

  grob <- drawn_rows(
    df,
    shape = "jar",
    base = data.frame(x = c(0.9, 1.1), y = c(0.9, 1.1))
  )
  expect_length(grob$children, 4)

  placements <- vapply(
    grob$children,
    \(row) {
      vp <- shape_viewports(row)[[1]]
      paste(vp$x, vp$y, vp$angle)
    },
    character(1)
  )
  expect_length(unique(placements), 4)
})
