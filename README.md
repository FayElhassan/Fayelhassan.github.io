# fayelhassan.github.io

Personal site of Fay Majid Elhassan, served by GitHub Pages as plain static files (`.nojekyll`, no build step).

- `index.html` contains all the content. To add a paper, copy one `<li class="pub">` block in the Publications section. Its `data-topic` can be `clinical`, `trust` or `sustain` (space-separated if it fits more than one).
- `assets/site.css` holds the design. Colours are defined as variables at the top, with dark-mode values just below them.
- `assets/site.js` runs the menu, the dark-mode toggle and the publication filters.
- `files/` holds the CV PDF and `images/` the photos.
- Old URLs (`/publications/`, `/talks/`, `/portfolio/`, `/cv/`) redirect to sections of the homepage.

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000
