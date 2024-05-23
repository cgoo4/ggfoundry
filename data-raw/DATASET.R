# Move raw svg files to project
file.copy(
  from = "~/Library/Mobile Documents/com~apple~CloudDocs/extdata",
  to = "inst/",
  overwrite = TRUE, recursive = TRUE
)

# Path to raw svg files
svg_names <- grep(
  list.files("inst/extdata/"),
  pattern = "-cairo", invert = TRUE, value = TRUE
)

svg_paths <- paste0("inst/extdata/", svg_names)

# Convert raw svg to cairo
# Keep commented out as grConvert not on CRAN

for (i in svg_paths) {
  s <- sub(".svg", "-cairo.svg", i)
  if (!file.exists(s)) {
    grConvert::convertPicture(i, s)
  }
}

# Remove raw svg
file.remove(svg_paths)


