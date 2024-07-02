# File conversion at package build time
# Intent is to minimise the size of the shipped package

# Get path to Cairo SVG files
svg_names <- list.files("inst/extdata/")
svg_paths <- paste0("inst/extdata/", svg_names)

# Convert smaller SVG files to larger Picture objects
picture_lst <- lapply(svg_paths, \(x){
  assign(x, grImport2::readPicture(x))
}) |>
  rlang::set_names(gsub(svg_names, pattern = ".svg$", replacement = ""))
