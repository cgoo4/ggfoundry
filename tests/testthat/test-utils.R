test_that("available sets & shapes", {
  x <- cast_shape("oak", "black", "red", 0.2, 90, 5, 5, 1, 1)

  expect_snapshot(typeof(x))
  expect_snapshot(class(x))
  expect_snapshot(length(x))
})
