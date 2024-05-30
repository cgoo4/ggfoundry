test_that("fills & manual shapes", {
  file <- tempfile(fileext = ".png")

  p <- ggplot2::ggplot(mtcars, ggplot2::aes(wt, mpg, fill = factor(cyl))) +
    geom_casting(ggplot2::aes(shape = factor(cyl))) +
    ggplot2::scale_shape_manual(values = c("violin", "box", "dendro"))

  ggplot2::ggsave(file, p, "png")

  expect_snapshot_file(file)

  unlink(file)
})

test_that("bad shape", {
  expect_snapshot(
    ggplot2::ggplot(mtcars, ggplot2::aes(wt, mpg)) +
      geom_casting(shape = "non-shape"),
    error = TRUE
  )
})

test_that("available sets & shapes", {
  expect_snapshot(
    shapes_cast()
  )
})

