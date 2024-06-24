# bad shape

    Code
      ggplot(mtcars, aes(wt, mpg)) + geom_casting(shape = "non-shape")
    Condition
      Error in `geom_casting()`:
      ! Problem while converting geom to grob.
      i Error occurred in the 1st layer.
      Caused by error in `FUN()`:
      ! `shape` is not a valid character string.
      i Is non-shape a typo? Or in the development version?

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
      39      leaf   hibiscus
      41      leaf        oak
      43   penguin     adelie
      45   penguin  chinstrap
      47   penguin     gentoo
      49   polygon   heptagon
      51   polygon    hexagon
      53   polygon    octagon
      55   polygon   pentagon

