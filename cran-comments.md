## R CMD check results

Local evidence, prepared 26 September 2026. Not yet a submission.

 * 0 errors | 0 warnings | 1 note

The note reports that the suggested package `ggimage` was not available for
checking in the local environment (its CRAN lookup could not be reached from
this machine). No code change results from this.

## Local check environment

 * R 4.6.1 (2026-06-24), aarch64-apple-darwin23, macOS Tahoe 26.6.2
 * Checked with `R CMD check --as-cran` in a fresh process on the source
   build `ggfoundry_0.3.1.9000.tar.gz` (development version; a release would
   be re-checked at its final version).
 * The package was also built and installed into a temporary library, where
   the new shapes and examples were verified.
 * Dependencies at check time: ggplot2 4.0.3.9000 (development; declared
   minimum 3.5.0), grImport2 0.3.3, cli 3.6.6, lifecycle 1.0.5, rlang 1.3.0.
 * Cross-platform checks (GitHub Actions matrix of macOS, Windows and Linux
   across R-release, R-devel and oldrel-1) and revdepcheck results are
   pending; they require the authorised release stage and are not claimed
   here.
