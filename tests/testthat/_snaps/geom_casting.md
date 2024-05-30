# bad shape

    Code
      ggplot2::ggplot(mtcars, ggplot2::aes(wt, mpg)) + geom_casting(shape = "non-shape")
    Condition
      Error in `geom_casting()`:
      ! Problem while converting geom to grob.
      i Error occurred in the 1st layer.
      Caused by error in `FUN()`:
      ! non-shape may be a typo or currently in the development version?

