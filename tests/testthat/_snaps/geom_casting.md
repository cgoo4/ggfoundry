# fills & manual shapes

    Code
      layer_data(p, 1)
    Output
          shape     x    y    fill PANEL group size colour alpha angle
      1     box 2.620 21.0 #00BA38     1     2  0.1  black    NA     0
      2     box 2.875 21.0 #00BA38     1     2  0.1  black    NA     0
      3  violin 2.320 22.8 #F8766D     1     1  0.1  black    NA     0
      4     box 3.215 21.4 #00BA38     1     2  0.1  black    NA     0
      5  dendro 3.440 18.7 #619CFF     1     3  0.1  black    NA     0
      6     box 3.460 18.1 #00BA38     1     2  0.1  black    NA     0
      7  dendro 3.570 14.3 #619CFF     1     3  0.1  black    NA     0
      8  violin 3.190 24.4 #F8766D     1     1  0.1  black    NA     0
      9  violin 3.150 22.8 #F8766D     1     1  0.1  black    NA     0
      10    box 3.440 19.2 #00BA38     1     2  0.1  black    NA     0
      11    box 3.440 17.8 #00BA38     1     2  0.1  black    NA     0
      12 dendro 4.070 16.4 #619CFF     1     3  0.1  black    NA     0
      13 dendro 3.730 17.3 #619CFF     1     3  0.1  black    NA     0
      14 dendro 3.780 15.2 #619CFF     1     3  0.1  black    NA     0
      15 dendro 5.250 10.4 #619CFF     1     3  0.1  black    NA     0
      16 dendro 5.424 10.4 #619CFF     1     3  0.1  black    NA     0
      17 dendro 5.345 14.7 #619CFF     1     3  0.1  black    NA     0
      18 violin 2.200 32.4 #F8766D     1     1  0.1  black    NA     0
      19 violin 1.615 30.4 #F8766D     1     1  0.1  black    NA     0
      20 violin 1.835 33.9 #F8766D     1     1  0.1  black    NA     0
      21 violin 2.465 21.5 #F8766D     1     1  0.1  black    NA     0
      22 dendro 3.520 15.5 #619CFF     1     3  0.1  black    NA     0
      23 dendro 3.435 15.2 #619CFF     1     3  0.1  black    NA     0
      24 dendro 3.840 13.3 #619CFF     1     3  0.1  black    NA     0
      25 dendro 3.845 19.2 #619CFF     1     3  0.1  black    NA     0
      26 violin 1.935 27.3 #F8766D     1     1  0.1  black    NA     0
      27 violin 2.140 26.0 #F8766D     1     1  0.1  black    NA     0
      28 violin 1.513 30.4 #F8766D     1     1  0.1  black    NA     0
      29 dendro 3.170 15.8 #619CFF     1     3  0.1  black    NA     0
      30    box 2.770 19.7 #00BA38     1     2  0.1  black    NA     0
      31 dendro 3.570 15.0 #619CFF     1     3  0.1  black    NA     0
      32 violin 2.780 21.4 #F8766D     1     1  0.1  black    NA     0

# bad shape

    Code
      ggplot(mtcars, aes(wt, mpg)) + geom_casting(shape = "non-shape")
    Condition
      Error in `geom_casting()`:
      ! Problem while converting geom to grob.
      i Error occurred in the 1st layer.
      Caused by error in `draw_panel()`:
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
      7  container      bowl0
      9  container      bowl1
      11 container      bowl2
      13 container        jar
      15 container       tube
      17     cross     cross1
      19     cross     cross2
      21    flower sunflower1
      23    flower sunflower2
      25    flower sunflower3
      27    flower sunflower4
      29    flower sunflower5
      31    flower sunflower6
      33    flower sunflower7
      35    flower sunflower8
      37      geom        box
      39      geom     dendro
      41      geom     ribbon
      43      geom     violin
      45      leaf   hibiscus
      47      leaf        oak
      49   penguin     adelie
      51   penguin  chinstrap
      53   penguin     gentoo
      55   polygon   heptagon
      57   polygon    hexagon
      59   polygon    octagon
      61   polygon   pentagon

# shapes clipped when zooming

    Code
      p[["coordinates"]][["limits"]][["x"]]
    Output
      [1] 1 4

# display a palette

    Code
      layer_data(p, 1)
    Output
        x y fill PANEL group shape size colour alpha angle
      1 1 1  red     1     1   jar  0.5   grey    NA     0
      2 2 1 blue     1     2   jar  0.5   grey    NA     0

---

    Code
      layer_data(p, 2)
    Output
        label x y PANEL group nudge_x nudge_y colour      fill family     size angle
      1   red 1 1     1    -1       0       0  black #FFFFFFB2        3.866058     0
      2  blue 2 1     1    -1       0       0  black #FFFFFFB2        3.866058     0
        hjust vjust alpha fontface lineheight linewidth linetype
      1   0.5     2    NA        1        1.2      0.25        1
      2   0.5     2    NA        1        1.2      0.25        1

# display_palette accepts repeated colours

    Code
      layer_data(p, 1)
    Output
        x y fill PANEL group shape size colour alpha angle
      1 1 1  red     1     1   jar  0.5 grey50    NA     0
      2 2 1  red     1     1   jar  0.5 grey50    NA     0
      3 3 1 blue     1     2   jar  0.5 grey50    NA     0

# display_palette rejects an empty palette

    Code
      display_palette(character(0), "Empty")
    Condition
      Error in `display_palette()`:
      ! `fill` must contain at least one colour.

