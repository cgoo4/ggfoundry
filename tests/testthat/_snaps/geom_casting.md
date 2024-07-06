# fills & manual shapes

    Code
      layer_data(p, 1)
    Output
          shape    fill     x    y PANEL group size colour alpha angle
      1     box #00BA38 2.620 21.0     1     2  0.1  black    NA     0
      2     box #00BA38 2.875 21.0     1     2  0.1  black    NA     0
      3  violin #F8766D 2.320 22.8     1     1  0.1  black    NA     0
      4     box #00BA38 3.215 21.4     1     2  0.1  black    NA     0
      5  dendro #619CFF 3.440 18.7     1     3  0.1  black    NA     0
      6     box #00BA38 3.460 18.1     1     2  0.1  black    NA     0
      7  dendro #619CFF 3.570 14.3     1     3  0.1  black    NA     0
      8  violin #F8766D 3.190 24.4     1     1  0.1  black    NA     0
      9  violin #F8766D 3.150 22.8     1     1  0.1  black    NA     0
      10    box #00BA38 3.440 19.2     1     2  0.1  black    NA     0
      11    box #00BA38 3.440 17.8     1     2  0.1  black    NA     0
      12 dendro #619CFF 4.070 16.4     1     3  0.1  black    NA     0
      13 dendro #619CFF 3.730 17.3     1     3  0.1  black    NA     0
      14 dendro #619CFF 3.780 15.2     1     3  0.1  black    NA     0
      15 dendro #619CFF 5.250 10.4     1     3  0.1  black    NA     0
      16 dendro #619CFF 5.424 10.4     1     3  0.1  black    NA     0
      17 dendro #619CFF 5.345 14.7     1     3  0.1  black    NA     0
      18 violin #F8766D 2.200 32.4     1     1  0.1  black    NA     0
      19 violin #F8766D 1.615 30.4     1     1  0.1  black    NA     0
      20 violin #F8766D 1.835 33.9     1     1  0.1  black    NA     0
      21 violin #F8766D 2.465 21.5     1     1  0.1  black    NA     0
      22 dendro #619CFF 3.520 15.5     1     3  0.1  black    NA     0
      23 dendro #619CFF 3.435 15.2     1     3  0.1  black    NA     0
      24 dendro #619CFF 3.840 13.3     1     3  0.1  black    NA     0
      25 dendro #619CFF 3.845 19.2     1     3  0.1  black    NA     0
      26 violin #F8766D 1.935 27.3     1     1  0.1  black    NA     0
      27 violin #F8766D 2.140 26.0     1     1  0.1  black    NA     0
      28 violin #F8766D 1.513 30.4     1     1  0.1  black    NA     0
      29 dendro #619CFF 3.170 15.8     1     3  0.1  black    NA     0
      30    box #00BA38 2.770 19.7     1     2  0.1  black    NA     0
      31 dendro #619CFF 3.570 15.0     1     3  0.1  black    NA     0
      32 violin #F8766D 2.780 21.4     1     1  0.1  black    NA     0

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

# shapes clipped when zooming

    Code
      p[["coordinates"]][["limits"]][["x"]]
    Output
      [1] 1 4

# display a palette

    Code
      layer_data(p, 1)
    Output
        fill x y PANEL group shape size colour alpha angle
      1  red 1 1     1     1   jar  0.5   grey    NA     0
      2 blue 2 1     1     2   jar  0.5   grey    NA     0

---

    Code
      layer_data(p, 2)
    Output
        label x y PANEL group colour      fill size angle hjust vjust alpha family
      1   red 1 1     1    -1  black #FFFFFFB2 3.88     0   0.5     2    NA       
      2  blue 2 1     1    -1  black #FFFFFFB2 3.88     0   0.5     2    NA       
        fontface lineheight
      1        1        1.2
      2        1        1.2

