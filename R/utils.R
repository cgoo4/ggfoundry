
#' Cast a shape from a pair of SVG files
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_shape <- \(shape, colour, fill, size, angle, x, y) {
  col_grob <- ggfoundry:::picture_lst[[paste0(shape, "_col")]]
  fill_grob <- ggfoundry:::picture_lst[[paste0(shape, "_fill")]]

  gTree(
    children = gList(
      cast_layers(col_grob, colour, size, angle, x, y),
      cast_layers(fill_grob, fill, size, angle, x, y)
    )
  )
}

#' Used by cast_shape to process each layer
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
cast_layers <- \(picture, col, size, angle, x, y) {
  picture |>
    symbolsGrob(x = x, y = y, size = size, angle = angle) |>
    removeGrob("Poly", grep = TRUE, global = TRUE) |>
    editGrob(
      "Path",
      gp = gpar(col = col, fill = col),
      grep = TRUE, global = TRUE, warn = FALSE
    )
}

#' Documentation helper
#' Simple lowercase converter
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
as_lower <- \(x) {

  chartr("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", x)
}

#' Documentation helper
#' Simple uppercase converter
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
as_upper <- \(x) {

  chartr("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", x)
}

#' Helper function
#' Convert snake_case to CamelCase
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
camelize <- \(x, first = FALSE) {

  x <- gsub("_(.)", "\\U\\1", x, perl = TRUE)
  if (first) {
    x <- paste0(as_upper(substring(x, 1, 1)), substring(x, 2))
  }
  x
}

#' Helper function
#' Find object in given environment with fallback to package namespace
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
find_global <- \(name, env, mode = "any") {

  if (exists(name, envir = env, mode = mode)) {
    return(get(name, envir = env, mode = mode))
  }
  nsenv <- asNamespace("geomtextpath")
  if (exists(name, envir = nsenv, mode = mode)) {
    return(get(name, envir = nsenv, mode = mode))
  }
  NULL
}

#' Helper function
#' Check subclass
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
check_subclass <- \(
    x,
    subclass,
    argname = as_lower(subclass),
    env     = parent.frame()
) {

  if (inherits(x, subclass)) {
    x
  }
  else if (is.character(x) && length(x) == 1) {
    name <- paste0(subclass, camelize(x, first = TRUE))
    obj  <- find_global(name, env = env)
    if (is.null(obj) || !inherits(obj, subclass)) {
      abort(paste0("Can't find `", argname, "` called '", x, "'"))
    } else {
      obj
    }
  }
  else {
    abort(paste0("`", argname, "` must be either a string or a ",
                 subclass, " object"))
  }
}

#' Helper function
#' Adds each aesthetic to output in rd_aesthetics
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
rd_aesthetics_item <- \(x) {

  req          <- x$required_aes
  req          <- sub("|", "} \\emph{or} \\code{", req, fixed = TRUE)
  req_aes      <- unlist(strsplit(x$required_aes, "|", fixed = TRUE))
  optional_aes <- setdiff(x$aesthetics(), req_aes)
  all          <- union(req, sort(optional_aes))

  ifelse(test = all %in% req,
         yes  = paste0("\\strong{\\code{", all, "}}"),
         no   = paste0("\\code{", all, "}"))
}

#' Helper function Calculate aesthetics and produce documentation item for given
#' function / topic
#'
#' @rdname geom_casting
#' @format NULL
#' @usage NULL
rd_aesthetics <- \(type, name, check_label_variant = TRUE) {

  obj <- switch(type,
                geom = check_subclass(name, "Geom", env = globalenv()),
                stat = check_subclass(name, "Stat", env = globalenv()))
  aes <- rd_aesthetics_item(obj)
  txt <- "@section Aesthetics:"
  txt <- c(txt,
           paste0("\\code{", type,
                  "_", name, "()} ",
                  "understands the following aesthetics ",
                  "(required aesthetics are in bold):"))
  txt <- c(txt, "\\itemize{", paste0("  \\item ", aes), "}")

  lab_aes <- NULL
  if (check_label_variant) {
    # Check if there is 'text' to be substituted by 'label'
    lab_name <- gsub("^text", "label", name)
    if (!(lab_name == name)) {
      # Check if label variant exists
      lab_obj <- tryCatch(
        {
          switch(type,
                 geom = check_subclass(lab_name, "Geom", env = globalenv()),
                 stat = check_subclass(lab_name, "Stat", env = globalenv()))
        },
        error   = \(cond) {return(NULL)}
      )
      if (!is.null(lab_obj)) {
        lab_aes <- rd_aesthetics_item(lab_obj)
        lab_aes <- setdiff(lab_aes, aes)
      }
      if (length(lab_aes)) {
        txt <- c(txt,
                 paste0("In addition to aforementioned aesthetics,",
                        " \\code{", type, "_", lab_name, "()} ",
                        "also understands:"))
        txt <- c(txt, "\\itemize{", paste0("  \\item ", lab_aes), "}")
      }
    }
  }

  if (any(grepl("spacing", aes))) {
    txt <- c(txt,
             "The \\code{spacing} aesthetic allows fine control of spacing",
             " of text, which is called 'tracking' in typography.",
             "The default is 0 and units are measured in 1/1000 em.",
             "Numbers greater than zero increase the spacing,",
             "whereas negative numbers decrease the spacing.")
  }

  txt <- c(txt,
           "\n\nLearn more about setting these aesthetics ",
           "in \\code{vignette(\"ggplot2-specs\")}.")
  txt
}
