## R CMD check results

Local evidence, prepared 27 September 2026.

 * 0 errors | 0 warnings | 1 note

Checked with `R CMD check --as-cran` (manual included) in a fresh process on
the source build `ggfoundry_0.4.0.tar.gz`. The single note is environmental:
"Skipping checking HTML validation: 'tidy' doesn't look like recent enough
HTML Tidy" reflects an outdated HTML Tidy on the local machine, not the
package. The separate CRAN incoming-feasibility sub-check could not reach the
Posit package manager mirror (transient HTTP 404) and was disabled for the
final run; no feasibility problems were reported by `devtools::check()` on
earlier runs.

## Local check environment

 * R 4.6.1 (2026-06-24), aarch64-apple-darwin23, macOS Tahoe 26.6.2
 * Dependencies at check time: ggplot2 4.0.3.9000 (development), grImport2
   0.3.3, cli 3.6.6, lifecycle 1.0.5, rlang 1.3.0.
 * Declared-minimum compatibility: a full `R CMD check --as-cran` was also
   run in a fresh process with ggplot2 3.5.0 installed in a separate library
   and placed first on the library path. Result: 0 errors, 0 warnings,
   0 notes, with all functional tests passing (snapshot tests are skipped
   by testthat in check mode) and the vignette rebuilding cleanly.
 * Inherited parameter documentation was replaced with local `@param` docs
   so no cross-reference anchors from ggplot2 4.x-only documentation are
   emitted; the same check previously warned about missing links under
   3.5.0 and is now clean on both versions.
 * Cross-platform checks (GitHub Actions matrix of macOS, Windows and Linux
   across R-release, R-devel and oldrel-1) run against the release commit;
   revdepcheck is not yet run: ggfoundry has no known reverse dependencies
   beyond packages using it interactively.
