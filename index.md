# ggfoundry

Arbitrary hand-crafted fillable shapes for ggplot2.

New shapes may be feature requested via a [Github
issue](https://github.com/cgoo4/ggfoundry/issues).

## Installation

``` r

install.packages("ggfoundry")
```

## Development version

To get a bug fix, or to use a feature from the development version, you
can install ggfoundry from GitHub.

``` r

# install.packages("pak")
pak::pak("cgoo4/ggfoundry")
```

## Basic example

See the [get
started](https://cgoo4.github.io/ggfoundry/articles/ggfoundry.html)
vignette and supporting package-website articles for more details,
including available shapes, a showcase of examples and how ggfoundry
contrasts with alternative strategies.

``` r

library(ggfoundry)
#> Loading required package: ggplot2

ggplot(mtcars, aes(wt, mpg, fill = factor(cyl))) +
  geom_casting(aes(shape = factor(cyl))) +
  scale_fill_manual(values = c("skyblue", "lightgreen", "pink")) +
  scale_shape_manual(values = c("violin", "dendro", "box")) +
  theme_bw()
```

![Scatter plot of car weight against fuel economy for 32 cars, with
fillable violin, box and dendrogram shapes cast in sky blue, light green
and pink according to the number of
cylinders.](reference/figures/README-example-1.png)

plot of chunk example
