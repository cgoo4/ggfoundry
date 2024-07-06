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
    c("red", "blue"), "Example", colour = "grey", shape = "jar"
  )

  expect_snapshot(layer_data(p, 1))
  expect_snapshot(layer_data(p, 2))
})

