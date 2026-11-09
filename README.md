# fayelhassan.github.io

Personal site of Fay Majid Elhassan, served by GitHub Pages as plain static files (`.nojekyll`, no build step).

- `index.html` contains all the content. To add a paper, copy one `<li class="pub">` block in the Publications section. Its `data-topic` can be `clinical`, `trust` or `sustain` (space-separated if it fits more than one).
- `assets/site.css` holds the design. Colours are defined as variables at the top, with dark-mode values just below them.
- `assets/site.js` runs the menu, the dark-mode toggle and the publication filters.
- `files/` holds the CV PDF and `images/` the photos.
- Old URLs (`/publications/`, `/talks/`, `/portfolio/`, `/cv/`) redirect to sections of the homepage.

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000

After editing `assets/site.css` or `assets/site.js`, bump the `?v=` number on their links in `index.html` so browsers fetch the new files.

## Arabic version (`/ar/`)

`ar/index.html` is generated from `index.html`; don't edit it by hand. After changing the English page, run:

```
python3 tools/build_ar.py
```

Translations live in `tools/build_ar.py`. Publication titles, authors and venues stay in English. The script lists any new English text that still needs an Arabic translation.

## Analytics

`assets/analytics.js` is switched on by two attributes on its `<script>` tag in `index.html`:

- `data-goatcounter="your-code"`: cookie-free visit counts (always on), plus a "section/…" event the first time a visitor reaches each section.
- `data-clarity="project-id"`: Microsoft Clarity heatmaps and session replays, loaded only after the visitor accepts the cookie banner. The footer's "Cookie settings" link reopens the banner.

Leave an attribute empty to switch that service off. Nothing is tracked on localhost. After changing them, run `python3 tools/build_ar.py` so the Arabic page gets the same IDs.
