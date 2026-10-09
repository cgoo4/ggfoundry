# Get the names of available shapes

**\[experimental\]**

Create a data frame of available shapes and associated sets. This may be
filtered and used as a vector of strings in
[`scale_shape_manual()`](https://ggplot2.tidyverse.org/reference/scale_manual.html).

Shapes are nominal symbols, not an ordered scale. Note that the quill is
placed by its ink-contact point rather than its centre; see
[`geom_casting()`](https://cgoo4.github.io/ggfoundry/reference/geom_casting.md).

## Usage

``` r
shapes_cast()
```

## Value

A data frame of available sets and shapes.

## Examples

``` r
# Returns a data frame of available shapes
shapes_cast()
#>          set        shape
#> 1     circle      circleF
#> 3     circle      circleL
#> 5     circle      circleR
#> 7  container        bowl0
#> 9  container        bowl1
#> 11 container        bowl2
#> 13 container          cup
#> 15 container          jar
#> 17 container          mug
#> 19 container     takeaway
#> 21 container         tube
#> 23     cross       cross1
#> 25     cross       cross2
#> 27    flower   sunflower1
#> 29    flower   sunflower2
#> 31    flower   sunflower3
#> 33    flower   sunflower4
#> 35    flower   sunflower5
#> 37    flower   sunflower6
#> 39    flower   sunflower7
#> 41    flower   sunflower8
#> 43      food   coffeebean
#> 45      food jackolantern
#> 47      food      pumpkin
#> 49      geom          box
#> 51      geom       dendro
#> 53      geom       ribbon
#> 55      geom       violin
#> 57 halloween        ghost
#> 59 halloween   gravestone
#> 61 halloween   grimreaper
#> 63 halloween     skeleton
#> 65 halloween    spiderweb
#> 67      leaf     hibiscus
#> 69      leaf          oak
#> 71   penguin       adelie
#> 73   penguin    chinstrap
#> 75   penguin       gentoo
#> 77   polygon     heptagon
#> 79   polygon      hexagon
#> 81   polygon      octagon
#> 83   polygon     pentagon
#> 85   writing    bookfront
#> 87   writing     bookopen
#> 89   writing  fountainpen
#> 91   writing       inkpot
#> 93   writing          nib
#> 95   writing        quill
```
