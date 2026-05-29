# Slide Formats

The 16 built-in formats. Exact, working markup for every one lives in
`assets/deck-scaffold.html` (it is a live gallery — one slide per format under
the default theme). To build a deck: copy the scaffold's `<head>` (fonts + full
CSS framework + theme tokens) and `<script>` (the engine), then assemble `<main>`
from only the formats this deck needs, editing the copy.

**Each slide is `<section class="slide" data-n="NN">` wrapping a `.stage`.** Add
`invert` (`class="slide invert"`) to flip a slide to its theme's dark palette —
use it for cover, section dividers, quote, code, and closing to give the deck
rhythm. Never run three identical-background slides in a row.

## The format menu

| # | Format | Use it when | Key classes / hooks |
|---|--------|-------------|---------------------|
| 1 | **Cover** | Deck opener. Every deck starts here. | `.cover`, `.anno` (lasso/ellipse draw-on), `.uline` |
| 2 | **Agenda** | 3–5 sections up front. | `.agenda-list`, `.agenda-row[data-on]` marks the active item |
| 3 | **Two-column** | One sentence + one real visual (mock, chart, card). | `.two-col`, `.mock`, `.progress-card` |
| 4 | **Stat grid** | 2–3 KPIs / big numbers. | `.stat-grid`, `.stat .num`, `data-count="900"` counts up (`data-from` for a baseline) |
| 5 | **Feature bento** | 4–6 features as an icon-card grid. | `.bento`, `.bento-card`, hand-built SVG in `.bento-ico` |
| 6 | **Comparison** | Contrast two options / before-after / us-vs-them. | `.cmp` table, `.hl` highlights the winning column |
| 7 | **Steps / Process** | A 3–4 stage workflow with arrows. | `.steps`, `.step-ico`, `.step-arrow` |
| 8 | **Timeline / Roadmap** | Milestones across quarters; past→now→next. | `.timeline`, `.tl-node[data-done]`/`[data-now]` |
| 9 | **Chart** | Quantitative substance. | `.chart-card`, `<canvas data-chart='{...}'>` (Chart.js) |
| 10 | **Code / CLI** | Tutorials / technical; the command or snippet is the visual. | `.code-window` + `.cursor`/`.scan`; `.cmd-frame` for one big CLI command; tokens `.c-com/.c-ok/.c-acc` |
| 11 | **Quote** | Anchor with a testimonial or pull-quote. | `.quote-slide`, `.quote-text em`, optional `.quote-portrait` (swap placeholder for an `<img>` face) |
| 12 | **Section divider** | Chapter break between deck sections. | `.divider`, `.big-n` |
| 13 | **Full-bleed image** | One image carries the moment. | `.slide.fullbleed`, `.bg-img`, `.scrim`, `.fb-text` |
| 14 | **People / team** | Headshots + names + roles. | `.people`, `.person .face` (swap placeholder for img) |
| 15 | **Pricing / tiers** | 2–3 plans with feature lists. | `.pricing`, `.tier.featured` = recommended |
| 16 | **Closing** | Memorable last line + one clear next action. | `.cover`, `.uline` |

## Content limits (hard)

- **One idea per slide.** Never join two ideas with "and."
- **≤ 6 bullet-list slides per deck.** Everything else uses a visual format above.
- Stat grid: 2–3 stats, never 4+. Bento: 3 or 6 cards. Steps: 3–4. Timeline: 3–5 nodes.
- Comparison table: ≤ 6 rows. Pricing: 3 tiers max.
- Body copy left-aligned. Center only titles and short hero lines.
- Headlines ≤ 7 words. Use a serif-italic accent word (`.accent-i`) for emphasis on serif themes.

## Charts (format 9)

`<canvas data-chart='{...}'>` reads a JSON config. Supported `type`: `bar`
(add `"stacked":true`), `line`, `pie`, `doughnut`. Series colors come from a
**monochrome tint ramp of the deck accent** — never rainbow. Example:

```html
<canvas data-chart='{"type":"bar","stacked":true,
  "labels":["Q1","Q2","Q3","Q4"],
  "datasets":[{"label":"Product","data":[12,18,24,32]},
              {"label":"Marketing","data":[8,11,14,17]}]}'></canvas>
```

Keep ≤ 3 series and ≤ 6 categories or the chart turns to noise.

## Image-slide rules (non-obvious — these prevent the two classic failures)

1. **Constrain images by height, not just width.** A `width:100%` image on a tall
   screenshot overflows a 100vh slide and gets cropped. Always:
   `max-height:74vh; max-width:100%; width:auto; height:auto; object-fit:contain;`
   and let the wrapping `<figure>` use `flex:0 1 auto; min-height:0;`. The whole
   image must be visible without scrolling.
2. **Do not reveal-animate an image that fills the slide.** A mid-transition
   screenshot looks washed-out / semi-transparent in QA captures. Render
   slide-filling images at full opacity — omit `data-reveal` on the `<figure>`.
3. For a screenshot that has its own light background (e.g. a white UI), give it a
   subtle border/shadow card so it doesn't float on the slide.

To add a local image: drop the file next to the deck HTML and reference it
relatively (`<img src="diagram.png">`), or paste it into chat and let the deck
embed it. For full-bleed, set `background-image:url('photo.jpg')` on `.bg-img`.

## Variation rules

- Alternate light and `invert` slides for rhythm; aim for 2–4 inverted slides in a deck.
- Never repeat the same format on consecutive slides.
- Commit to ONE visual motif (accent-colored bullets, card style, heading treatment)
  and carry it across every slide.
- Give most slides ONE hero motion; everything else just fades in. See `animations.md`.
