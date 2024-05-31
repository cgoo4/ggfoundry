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
               set      shape
      1     circle    circleF
      3     circle    circleL
      5     circle    circleR
      7  container        jar
      9  container       tube
      11     cross     cross1
      13     cross     cross2
      15    flower sunflower1
      17    flower sunflower2
      19    flower sunflower3
      21    flower sunflower4
      23    flower sunflower5
      25    flower sunflower6
      27    flower sunflower7
      29    flower sunflower8
      31      geom        box
      33      geom     dendro
      35      geom     ribbon
      37      geom     violin
      39   polygon   heptagon
      41   polygon    hexagon
      43   polygon    octagon
      45   polygon   pentagon

