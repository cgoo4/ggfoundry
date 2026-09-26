## R CMD check results

Local evidence, prepared 26 September 2026. Not yet a submission.

 * 0 errors | 0 warnings | 0 notes

Checked with `R CMD check --as-cran --no-manual` in a fresh process on the
source build `ggfoundry_0.3.1.9000.tar.gz` (development version; a release
would be re-checked at its final version).

## Local check environment

 * R 4.6.1 (2026-06-24), aarch64-apple-darwin23, macOS Tahoe 26.6.2
 * The package was also built and installed into a temporary library, where
   the new shapes and examples were verified, and a local pkgdown preview
   rendered all articles.
 * Dependencies at check time: ggplot2 4.0.3.9000 (development), grImport2
   0.3.3, cli 3.6.6, lifecycle 1.0.5, rlang 1.3.0.
 * Declared-minimum compatibility: the full test suite was also run in a
   fresh process against ggplot2 3.5.0 installed in a separate library. All
   functional tests passed, including the drawing-path regressions and a
   rendered continuous-fill example with seven distinct fills. The only
   diffs were layer_data snapshot formatting (column order) caused by the
   newer ggplot2 used to generate the snapshots, not by the package code.
 * Cross-platform checks (GitHub Actions matrix of macOS, Windows and Linux
   across R-release, R-devel and oldrel-1) and revdepcheck results are
   pending; they require the authorised release stage and are not claimed
   here.
