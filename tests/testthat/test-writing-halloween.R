writing_halloween_stack <- function(grob) {
  if (inherits(grob$vp, "vpStack") &&
      identical(grob$vp[[1]]$name, "picture.shape")) {
    return(grob$vp)
  }
  if (!is.null(grob$children)) {
    for (child in grob$children) {
      found <- writing_halloween_stack(child)
      if (!is.null(found)) return(found)
    }
  }
  NULL
}

writing_halloween_location <- function(grob, point) {
  vp <- writing_halloween_stack(grob)
  # Clipping is irrelevant to a coordinate measurement. grid cannot
  # resolve rotated clip boxes for the existing ordinary shapes.
  vp[[2]]$clip <- FALSE
  grid::pushViewport(vp)
  on.exit(grid::popViewport(2))
  unlist(grid::deviceLoc(grid::unit(point[1], "native"),
                         grid::unit(point[2], "native"), valueOnly = TRUE))
}

test_that("writing and Halloween assets register as two complete sets", {
  shapes <- shapes_cast()
  expect_setequal(shapes$shape[shapes$set == "writing"],
                  c("bookfront", "bookopen", "nib", "fountainpen", "inkpot", "quill"))
  expect_setequal(shapes$shape[shapes$set == "halloween"],
                  c("skeleton", "ghost", "spiderweb", "grimreaper", "gravestone"))
})

test_that("quill ink contact stays at the point after rotation and cache reuse", {
  for (dims in list(c(900, 600), c(600, 900), c(700, 700))) {
    file <- tempfile(fileext = ".png")
    grDevices::png(file, width = dims[1], height = dims[2], res = 100)
    tryCatch({
      cache <- new.env(parent = emptyenv())
      target <- unlist(grid::deviceLoc(grid::unit(0.42, "npc"),
                                        grid::unit(0.46, "npc"), valueOnly = TRUE))
      for (size in c(0.12, 0.32)) {
        for (angle in c(0, 29, 90, 173, 270)) {
          direct <- cast_shape("quill", "black", "tan", size, angle,
                               0.42, 0.46, 0.5, 0.5)
          reused <- cast_style("quill", "black", "tan", size, angle,
                               0.42, 0.46, 0.5, 0.5, cache)
          expect_equal(writing_halloween_location(direct, c(44, 166)),
                       target, tolerance = 1e-9)
          expect_equal(writing_halloween_location(reused, c(44, 166)),
                       target, tolerance = 1e-9)
        }
      }
    }, finally = {
      grDevices::dev.off()
      unlink(file)
    })
  }
})

test_that("legends centre quills and ordinary shapes retain their placement", {
  file <- tempfile(fileext = ".png")
  grDevices::png(file, width = 900, height = 600, res = 100)
  on.exit({grDevices::dev.off(); unlink(file)})
  target <- unlist(grid::deviceLoc(grid::unit(0.5, "npc"),
                                    grid::unit(0.5, "npc"), valueOnly = TRUE))
  legend <- GeomCasting$draw_key(
    list(shape = "quill", colour = "black", fill = "tan", alpha = 1),
    list(), 1
  )
  expect_equal(writing_halloween_location(legend, c(100, 100)),
               target, tolerance = 1e-9)
  for (angle in c(0, 45, 90)) {
    ordinary <- cast_shape("mug", "black", "tan", 0.2, angle,
                           0.5, 0.5, 0.5, 0.5)
    expect_equal(writing_halloween_location(ordinary, c(100, 100)),
                 target, tolerance = 1e-9)
  }
})

test_that("quill anchor preserves the existing justification adjustments", {
  file <- tempfile(fileext = ".png")
  grDevices::png(file, width = 900, height = 600, res = 100)
  on.exit({grDevices::dev.off(); unlink(file)})
  for (angle in c(0, 45, 90)) {
    for (just in list(c(0, 0), c(1, 1), c(0.2, 0.7))) {
      quill <- cast_shape("quill", "black", "tan", 0.2, angle,
                          0.5, 0.5, just[1], just[2])
      centred <- cast_shape("mug", "black", "tan", 0.2, angle,
                            0.5, 0.5, just[1], just[2])
      expect_equal(writing_halloween_location(quill, c(44, 166)),
                   writing_halloween_location(centred, c(100, 100)),
                   tolerance = 1e-9)
    }
  }
})
