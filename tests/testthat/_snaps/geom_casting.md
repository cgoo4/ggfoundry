# bad shape

    Code
      ggplot2::ggplot(mtcars, ggplot2::aes(wt, mpg)) + geom_casting(shape = "non-shape")
    Condition
      Error in `geom_casting()`:
      ! Problem while converting geom to grob.
      i Error occurred in the 1st layer.
      Caused by error in `FUN()`:
      ! non-shape may be a typo or currently in the development version?

# available sets & shapes

    Code
      shapes_cast()
    Output
               set    shape
      1     circle  circleF
      3     circle  circleL
      5     circle  circleR
      7  container      jar
      9  container     tube
      11     cross   cross1
      13     cross   cross2
      15      geom      box
      17      geom   dendro
      19      geom   ribbon
      21      geom   violin
      23   polygon heptagon
      25   polygon  hexagon
      27   polygon  octagon
      29   polygon pentagon

