# Get the names of available shapes

**\[experimental\]**

Create a data frame of available shapes and associated sets. This may be
filtered and used as a vector of strings in
[`scale_shape_manual()`](https://ggplot2.tidyverse.org/reference/scale_manual.html).

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
#>          set      shape
#> 1     circle    circleF
#> 3     circle    circleL
#> 5     circle    circleR
#> 7  container      bowl0
#> 9  container      bowl1
#> 11 container      bowl2
#> 13 container        jar
#> 15 container       tube
#> 17     cross     cross1
#> 19     cross     cross2
#> 21    flower sunflower1
#> 23    flower sunflower2
#> 25    flower sunflower3
#> 27    flower sunflower4
#> 29    flower sunflower5
#> 31    flower sunflower6
#> 33    flower sunflower7
#> 35    flower sunflower8
#> 37      geom        box
#> 39      geom     dendro
#> 41      geom     ribbon
#> 43      geom     violin
#> 45      leaf   hibiscus
#> 47      leaf        oak
#> 49   penguin     adelie
#> 51   penguin  chinstrap
#> 53   penguin     gentoo
#> 55   polygon   heptagon
#> 57   polygon    hexagon
#> 59   polygon    octagon
#> 61   polygon   pentagon
```
