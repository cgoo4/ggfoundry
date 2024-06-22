test_that("fills & manual shapes", {
  file <- tempfile(fileext = ".png")

  p <- ggplot(mtcars, aes(wt, mpg, fill = factor(cyl))) +
    geom_casting(aes(shape = factor(cyl))) +
    scale_shape_manual(values = c("violin", "box", "dendro"))

  ggsave(file, p, "png")

  expect_snapshot_file(file)

  unlink(file)
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
  file <- tempfile(fileext = ".png")

  p <- ggplot(mtcars, aes(wt, mpg)) +
    geom_casting(size = 0.1, shape = "violin") +
    geom_point() +
    coord_cartesian(xlim = c(1, 4))

  ggsave(file, p, "png")

  expect_snapshot_file(file)

  unlink(file)
})

test_that("Display a palette", {
  file <- tempfile(fileext = ".png")

  p <- display_palette(
    c("red", "blue"), 2, "Example", colour = "grey", shape = "jar"
    )

  ggsave(file, p, "png")

  expect_snapshot_file(file)

  unlink(file)
})

