
<!-- README.md is generated from README.Rmd. Please edit that file -->

# ggfoundry

<!-- badges: start -->
<!-- badges: end -->

The goal of ggfoundry is to offer arbitrary hand-crafted fillable shapes
for ggplot2.

New shapes may be feature requested via a Github issue.

## Installation

Install the development version of ggfoundry from
[GitHub](https://github.com/):

``` r
# install.packages("pak")
pak::pak("cgoo4/ggfoundry")
```

## Example

This is a basic example. See [get
started](https://cgoo4.github.io/ggfoundry/) for more details.

``` r
library(ggfoundry)
#> Loading required package: ggplot2
```

``` r

ggplot(mtcars, aes(wt, mpg, fill = factor(cyl))) +
  geom_casting(aes(shape = factor(cyl))) +
  scale_fill_manual(values = c("skyblue", "lightgreen", "pink")) +
  scale_shape_manual(values = c("violin", "dendro", "box")) +
  theme_bw()
```

<img src="man/figures/README-example-1.png" width="100%" />