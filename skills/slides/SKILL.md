---
name: slides
description: Create a beautiful, animated HTML slide deck. Use when the user wants to make a presentation, pitch deck, talk slides, board deck, conference talk, client deck, or any "slides" — or invokes /slides. Guides them through content and brand style, generates one self-contained HTML file with 16 slide formats and 5 themes, runs a visual QA pass, and can theme to any design.md (personal, Slalom, or the awesome-design-md library).
---

# Slides

Turn a rough outline into a polished, animated, on-brand HTML deck — one
self-contained file that opens in any browser. No PowerPoint, no build step, no
framework. From nothing to first draft in minutes, then iterate.

**Credit:** Adapted from Peter Yang's `/slides` skill
([@petergyang](https://x.com/petergyang/status/2059801947503530365)), extended here
with 16 formats, a 5-theme + design.md theming system, and a self-running visual-QA loop.

**Why HTML decks:** zero-to-draft in minutes, live interactive charts, drop-in
images, subtle animations on every reveal, brand-locked typography, and a visual
QA loop the agent runs on itself. The whole deck is one shareable `.html` file.

## What ships with this skill

- `assets/deck-scaffold.html` — the engine + full CSS framework + **a live gallery
  of all 16 formats** under the default theme. Copy this and trim it down.
- `references/slide-formats.md` — the 16 formats, content limits, image rules.
- `references/templates.md` — the 5 themes + the token "format contract."
- `references/animations.md` — the motion toolkit and per-format cheat sheet.
- `references/design-md-ingestion.md` — derive a theme from any design.md (Slalom etc.).
- `scripts/render_slides.py` — the visual-QA renderer (Playwright).

Read `references/*` as needed during the relevant step — don't preload everything.

---

## Step 1 — Ask the user these questions (one AskUserQuestion call)

Use the AskUserQuestion tool. Ask questions 1–3 always, then pick ONE more from
the pool. Do not start building until answered.

### Required
1. **Content** — "Do you have content ready, or just a topic?"
   Options: *I have content to paste* · *Just a topic — help me outline it*
2. **Length** — "How many slides?"
   Options: *Short (5–8)* · *Medium (10–15)* · *Long (20+)*
3. **Theme** — "Which look?"
   Options: *Default (warm editorial)* · *Dark* · *Light* · *Kevin (personal brand)*
   · *Anthropic* · *From a design.md / brand*
   (If they pick a design.md/brand, ask for the path or brand name and follow
   `design-md-ingestion.md`.)

### Pick ONE more (by context)
4. One of: "Will this be screen-shared on video/Zoom?" (if yes, keep slides sparse,
   bump font sizes) · "Who's the audience?" · "What's the goal — pitch, teach,
   inform, inspire?" · "What's the one takeaway they should remember?" · "Any images
   or assets to include?"

If they chose **"I have content to paste,"** wait for the paste before continuing.

If they ask to **see the themes first**, generate one-slide preview files (one per
candidate theme) in `output/slide-previews/`, open them, and let them pick before
building the full deck.

### Derived from answers (decide yourself, do NOT ask)
- **Which formats to use** and their order — map the content to the format menu in
  `slide-formats.md`. Lead with a cover, close with a CTA.
- **Which slides invert** (dark) for rhythm — cover, dividers, quote, code, closing.
- **Deck length → format mix** (short = cover + 4–6 content + close).
- **Accent usage, motion choices, icon designs, chart types, copy tightening.**
- **Filename** (short kebab-case).

---

## Step 2 — Offer light research

Ask once (AskUserQuestion): "Want me to research the topic first?"
Options: *Yes, research it* · *Yes, here's what to search* · *No, just build it*.

If yes, **dispatch a subagent to do the searching** (Agent tool, `general-purpose`)
rather than searching inline — web research is noisy and bloats the deck-building
context. Tell the agent exactly what to find (facts, figures, dates, names, prices)
and to return a tight 3–6 bullet brief with **sources, numbers quoted verbatim, and
an explicit note on anything it could NOT verify**. Fold the verified findings into
the outline. Never put an unconfirmed figure on a slide — use a clearly-labeled
placeholder and tell the user it needs a real number.

---

## Step 3 — Generate the deck (one HTML file)

1. Copy `assets/deck-scaffold.html` to `output/slides/<deck-name>.html`.
2. Keep its `<head>` (fonts, CSS framework, all theme tokens) and `<script>`
   (engine) intact. Set `<body class="theme-…">` to the chosen theme.
3. Replace the gallery slides in `<main>` with this deck's slides, pulling each
   format's markup from the gallery (or `slide-formats.md`) and filling real
   content. Delete formats you don't use.
4. Follow the format contract: **only use tokens, never hardcode a color or font.**
5. Add motion per `animations.md` — one hero motion per slide, the rest fade.

### Architecture (the output is ONE file)
```
<deck>.html
├── <head>
│   ├── Google Fonts <link>  +  Chart.js (with SRI) — the only external deps
│   └── <style>: tokens (:root) · 5 themes · .slide.invert · layout · 16 format
│       component blocks · reveal/stagger/draw-line/float animations · nav chrome
├── <body class="theme-X">
│   ├── .deck-progress · .deck-dots · .deck-hint   (nav UI)
│   └── <main class="deck"> → <section class="slide [invert]" data-n="NN"> × N
└── <script>: nav (keys/scroll/dots) · IntersectionObserver → .is-active ·
    count-up (0→target or data-from→target) · progress-fill · Chart.js init ·
    grid overview (G) · fullscreen (F)
```
Single file. No routing, no extra assets except images the user supplies.

### Strong opinions (these override generic defaults)
- **Every slide needs a visual element.** Text-only slides are forgettable. Reach
  for a card, stat, chart, icon grid, or illustration.
- **One idea per slide.** Never two features joined by "and."
- **Left-align body copy. Center only titles and short hero lines.**
- **Pick ONE accent and one visual motif; carry it across every slide.**
- **Charts use a monochrome tint ramp of the accent — never rainbow.**
- **Hand-built inline-SVG icons, not emoji,** as the visual system. (A few emoji as
  recap-grid icons is fine; never emoji on every bullet.)
- **≤ 6 bullet-list slides per deck.** The rest use the visual formats.

### Responsive
All font sizes use `clamp(min, preferred, max)`; spacing uses `clamp()`/viewport
units. The scaffold already handles height breakpoints — keep them.

---

## Step 4 — Save (do NOT open yet)

Save to `output/slides/<deck-name>.html`. Do not open it for the user yet — run
Visual QA first.

---

## Step 5 — Visual QA (REQUIRED — never skip, even for one slide)

You cannot tell whether a deck looks right by reading the HTML. Rendered slides
routinely have problems the code doesn't reveal: images cropped by the viewport,
text overflow, overlapping elements, low contrast, captions caught mid-animation.

1. **Render every slide to a PNG:**
   ```bash
   python3 ~/.claude/skills/slides/scripts/render_slides.py --html output/slides/<deck-name>.html
   ```
   It isolates each slide, disables scroll-snap, and freezes animations to their
   final state. Prints one `output/slides/qa/slide-NN.png` per line. (First run:
   `pip install playwright && python3 -m playwright install chromium`.)

2. **Inspect with a fresh-eyes subagent — do NOT inspect them yourself.** You've
   been staring at the code and will see what you expect, not what's there. Spawn a
   subagent (Agent tool, `general-purpose`), pass the image paths plus a one-line
   "expected" note per slide, and this instruction:
   > Visually inspect these slide images. Assume there ARE issues — find them. For
   > each slide list every problem: overlapping elements, text overflow or cut off
   > at edges, images cropped or partly hidden, low-contrast or washed-out text,
   > mid-animation/half-faded captures, content colliding, columns misaligned,
   > insufficient margin from slide edges, leftover placeholder text. Report ALL
   > issues by slide number. If a slide is clean, say so explicitly.

3. **Fix every real issue, then re-render the affected slides and re-inspect** — one
   fix often creates another (enlarging an image re-crops it).

4. Repeat until a full pass finds nothing new. **Do not declare done until at least
   one fix-and-verify cycle has run.** If the first pass "finds nothing," look again
   more critically — a first draft almost always has something.

---

## Step 6 — Deliver (only after QA passes)

- `open output/slides/<deck-name>.html` so the user can view it.
- One-line QA summary ("rendered 12 slides, fixed 3 overflow + 1 contrast issue,
  re-verified clean").
- Mention: customize colors by editing the `:root` / `body.theme-*` tokens at the
  top; navigate with arrows / space / scroll, `G` for grid overview, `F` fullscreen.
- Delete `output/slides/qa/` images if no longer needed.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Static accent bar/line under a title | Use `.draw-line` (animates) or nothing — static bars read as AI-generated |
| Centering all body text | Left-align body; center only titles + short hero lines |
| Default-blue accent on everything | Use the theme's accent; pick ONE accent total |
| Generic gradient / glassmorphism with no purpose | Remove it; use flat surfaces + the token shadows |
| Emoji as the icon system | Hand-built inline SVG icons; emoji only as occasional recap-grid accents |
| Rainbow chart series | Monochrome tint ramp of the accent |
| Full-bleed image cropped / washed out | Cap `max-height:74vh; object-fit:contain`; no reveal-anim on slide-filling images |
| Three same-background slides in a row | Alternate `invert` slides for rhythm |
| Two ideas crammed on one slide | Split into two; one idea per slide |
| Hardcoded color/font in a format | Use a token so it themes automatically |
| Declaring done without rendering | Step 5 is mandatory — render + fresh-eyes inspect every time |
| Opening the deck before QA | Save → QA → fix → only then open (Steps 4–6) |

## Anthropic theme

The `anthropic` theme is mapped from the canonical Claude design system. Hard rules
if you edit it: Parchment `#F5F4ED` is the page canvas (Ivory `#FAF9F5` is the card
surface, never the background); terracotta `#C96442` is CTA/accent only; every gray
stays warm-toned (no cool blue-grays); serif headlines are weight **500 only**
(never bold); use whisper shadows, not hard drop shadows.
