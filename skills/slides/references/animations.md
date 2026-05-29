# Animation Toolkit

Motion is the signature of a good HTML deck — it makes the deck feel alive. But
it must be subtle. The rule: **give each slide ONE hero motion; everything else
just fades in.** Subtle = 8–24px travel, 450–700ms, ease-out. Never distracting.

All motion fires when a slide becomes active. The engine adds `.is-active` to the
slide that's centered in the viewport (IntersectionObserver) and runs counters +
charts then. Everything degrades to instant under `prefers-reduced-motion`.

## Entrance reveals

Put `data-reveal` on an element to fade+rise it in. Stagger a group by setting
`style="--i:N"` (N = 0,1,2,… → each waits `N×80ms`).

```html
<h2 class="display" data-reveal>Headline</h2>
<p class="lead"    data-reveal style="--i:1">Subhead.</p>
<div class="card"  data-reveal style="--i:2">…</div>
```

Direction variants (add as a class on the same element):

| Class | Motion | Good for |
|-------|--------|----------|
| `data-reveal` (alone) | fade + 18px rise | default, most things |
| `.from-left` / `.from-right` | slide in horizontally | two-column halves |
| `.from-scale` | scale up from 93% | hero cards, stats |
| `.from-blur` | de-blur in | cover headlines, big moments |
| `.fade-only` | opacity only, no move | images, dense layouts |

## Counters (KPI tick-up)

`<span data-count="900">0</span>` ticks from 0 to the target (easeOutCubic, 1.1s)
when the slide activates. Use on stat-grid numbers. Decimals supported
(`data-count="3.5"`). Pair with a unit span: `<span class="unit">M</span>`.

**Start from a baseline** with `data-from` — the number animates from that value
to the target instead of from zero (e.g. a score climbing 61 → 92):

```html
<span data-count="92" data-from="61">61</span><span class="unit">%</span>
```

Set the element's initial text to the `data-from` value so it reads correctly
before the reveal fires.

## Progress bars

`.bar > span` fills to `--fill` on activate:
`<div class="bar" style="--fill:82%"><span></span></div>`.

## Charts

Charts (`<canvas data-chart>`) draw in over ~900ms on activate, themed to the
accent ramp. No extra markup needed.

## Annotations (the "brand mark" move)

- **Cover/closing lasso (the signature):** wrap the italic highlight phrase in
  `.circle-word` containing an inline `<svg class="circle-mark">` whose `<path>`
  is the lasso loop. The stroke draws on like a marker, a soft accent glow
  breathes behind the phrase (`wordGlow`), and a drifting `.aura` floats behind
  the whole headline. **Keep the lasso path identical on the cover and the
  closing** — matching bookends are the brand mark. See slides 1 and 16 in the
  scaffold. The phrase text stays the headline color; only the lasso is accent.
- **Inline ellipse** mid-slide: wrap a phrase in `.anno` with a rough-ellipse
  `<svg>` path — same draw-on, for highlighting a word inside body content.
- **Draw-on underline**: wrap a word in `.uline` — an accent underline wipes in.
- **`.draw-line`**: an accent rule that scales in from the left. Use this INSTEAD
  of a static bar under a title (static accent bars are an AI-slide tell).

## Code / CLI motion

- **Blinking cursor**: append `<span class="cursor"></span>` after a prompt line
  in `.code-body`, or inside a `.cmd-frame`. Blinks on a 1.1s step loop.
- **Scan sweep**: drop `<div class="scan"></div>` inside `.code-window` — a faint
  accent band sweeps top-to-bottom every 5s. Use on ONE code slide, not every one.
- **CLI command frame** (`.cmd-frame`): one prominent command shown large (`>`
  sign + `<code>` + cursor). Best for showing a single Claude Code / CLI invocation
  efficiently, paired with a terminal window or on its own.

## Ambient motion (use sparingly)

`.float` (gentle bob) and `.pulse` (soft scale/opacity) loop forever. Apply to ONE
small decorative element per slide — never to text. For process/concept slides,
the strongest move is a hand-built inline-SVG illustration with one looping
ambient detail (a breathing glow, a self-drawing line, a drifting dot).

## Per-format cheat sheet

| Format | Hero motion | Rest |
|--------|-------------|------|
| Cover | `.from-blur` headline + `.circle-word` lasso draw-on + drifting `.aura` | breathing word-glow loops |
| Agenda | active row's filled disc + stagger rows | — |
| Two-column | `.from-left` text, `.from-right` visual | bullets stagger |
| Stat grid | `data-count` counters (+`data-from` baseline) | labels fade |
| Bento | stagger cards (`--i:1..6`) | — |
| Comparison | table fades; highlight column has `--accent-soft` | — |
| Steps | stagger discs + flowing dashed arrows + breathing accent rings | — |
| Timeline | sequential node reveal (`--i`); `.tl-fill` connector fills to "now"; "now" dot pulses | — |
| Chart | chart draw-in | — |
| Code / CLI | window fades + blinking `.cursor` + optional `.scan` sweep; `.cmd-frame` for one CLI command | — |
| Quote | quote staggers; portrait `.from-scale` | — |
| Divider | big number `.from-scale` | title fades |
| Full-bleed | image static (no reveal), text `.from-left` | — |
| People | stagger faces | — |
| Pricing | stagger tiers, featured `.from-scale` | — |
| Closing | same `.circle-word` lasso as cover (bookend) | CTA fades |

## QA note

`render_slides.py` emulates `prefers-reduced-motion`, so QA screenshots show every
animation FROZEN at its final state (counters on final value, reveals fully shown,
charts drawn). Verify the motion itself separately by opening the deck in a browser.
