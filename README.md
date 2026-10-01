# adamwstauffer.github.io

Adam W. Stauffer's personal portfolio site: teaching, applied AI work, writing and builds.

Live at **https://adamwstauffer.github.io/**. Plain static HTML, no build step; `.nojekyll` tells GitHub Pages to serve files as-is.

Merging to `main` publishes the site, so changes land through pull requests.

## Resume, CV and bio

The master copies are the Markdown files in `content/` (`resume.md`, `cv.md`, `bio.md`). Edit those, then run `python build.py` (needs `pip install markdown`, plus Chromium or Chrome for the PDF). It regenerates `resume.html`, `cv.html`, `bio.html` and `resume.pdf`. Commit all of them together.
