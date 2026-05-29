# Templates (Themes)

**Themes and formats are orthogonal.** A *theme* sets palette, fonts, and mood.
A *format* is a slide layout. Every format works under every theme because
formats only ever read shared **design tokens** — never a hardcoded color or
font. This is the format contract. Honor it and any deck re-skins by changing
one class.

## Switching theme

Set the body class. That's the entire switch:

```html
<body class="theme-default">   <!-- default·dark·light·kevin·anthropic·midnight·mono·sage·plum, or a design.md theme -->
```

## The token contract

Every format is built from these CSS variables (defined in `:root` and each
`body.theme-*` block in `assets/deck-scaffold.html`). Never hardcode — reach for
a token so the deck themes automatically.

| Token | Role |
|-------|------|
| `--bg` / `--bg-grad` | slide background + optional glow |
| `--surface` / `--surface-2` | card / secondary surfaces |
| `--ink` / `--ink-soft` | primary / secondary text |
| `--accent` / `--accent-2` | brand accent + secondary (chart ramp, gradients) |
| `--accent-soft` | low-opacity accent fill (tints, highlights) |
| `--accent-ink` | text on an accent fill |
| `--border` | hairlines |
| `--font-display` / `--font-body` / `--font-mono` | type |
| `--display-weight` / `--display-tracking` | heading weight + tracking |
| `--radius` / `--shadow` / `--stage-w` | shape + content width |
| `--bg-i`, `--surface-i`, `--ink-i`, … (`*-i`) | the **invert** palette for `.slide.invert` |

`.slide.invert` swaps the live tokens for the `*-i` set, so cover/quote/code/
closing render on the theme's dark (or contrasting) palette. Every component
re-themes for free.

## The 9 built-in themes

| Theme | Mood | Bg | Accent | Display font |
|-------|------|----|--------|--------------|
| `default` | Warm editorial (Peter's brand feel) | cream `#F4EAD0` | brick red `#BE3A1E` | Fraunces (serif) |
| `dark` | Bold tech-talk | near-black `#0C0C0D` | gold `#F2C14E` | Inter (sans, 800) |
| `light` | Apple-clean, minimal | white | blue `#2D6CDF` | Inter (sans, 800) |
| `kevin` | Kevin's personal brand | ink `#0E0D0C` | signal orange `#FF5A1F` | Fraunces 900 (serif) |
| `anthropic` | Parchment + terracotta, warm-neutral, editorial | parchment `#F5F4ED` | terracotta `#C96442` | Newsreader (serif, wt 500) |
| `midnight` | Product/tech keynote | deep navy `#0B1020` | electric cyan `#5BC8FF` | Inter (sans, 800) |
| `mono` | Swiss, minimal, high-contrast | white | signal red `#E5482A` | Inter (sans, 800) |
| `sage` | Calm, natural, editorial | oat `#F2F1E7` | forest green `#4F7A4D` | Fraunces (serif) |
| `plum` | Creative, bold, launch | dark plum `#15101D` | violet `#B57BFF` | Inter (sans, 800) |

## Theme picker — by intent

Use this to auto-suggest 3–4 best-fit themes in the Step 1 question (don't list all 9).
Map the deck's topic, audience, and desired tone:

| If the deck is… | Reach for |
|-----------------|-----------|
| Editorial / thought-leadership / warm | `default`, `sage`, `anthropic` |
| Developer / product / tech keynote | `midnight`, `dark`, `mono` |
| Executive / board / corporate | `light`, `mono`, `anthropic` |
| Anthropic / Claude subject matter | `anthropic` |
| Creative / launch / high-energy | `plum`, `kevin`, `dark` |
| Minimal / data-forward / no-frills | `mono`, `light` |
| Kevin's personal byline | `kevin` |
| A specific company brand | a `design.md` (see `design-md-ingestion.md`) |

**Base (light vs dark):** light-bg themes (`default`, `light`, `anthropic`, `mono`,
`sage`) invert their cover/quote/code/closing to a dark slide; dark-bg themes
(`dark`, `kevin`, `midnight`, `plum`) invert to a light slide. Either way the deck
gets light/dark rhythm for free.

Notes:
- **Serif** display: `default`, `kevin`, `anthropic`, `sage`. **Sans**: `dark`,
  `light`, `midnight`, `mono`, `plum`.
- **`anthropic`** is mapped from the canonical Claude design system
  (`awesome-design-md/claude/DESIGN.md` + Anthropic brand specs): Parchment canvas
  `#F5F4ED`, Ivory cards `#FAF9F5`, terracotta brand `#C96442` (CTA/accent only),
  exclusively warm neutrals, serif headlines at **weight 500 only** (never bold),
  whisper shadows. Newsreader substitutes for the custom Anthropic Serif.
- **Fonts faithful to Peter's original:** Crimson Pro (display) + Manrope (body).
  Swap `--font-display`/`--font-body` and the Google Fonts `<link>` if an exact
  match to his deck is wanted; Fraunces + Inter is the chosen house default here.

## Adding a custom theme

1. Copy a `body.theme-*` block in the scaffold's `<style>`, rename the class.
2. Set every token in the table above (include the `*-i` invert set).
3. Add the brand's fonts to the Google Fonts `<link>` (or `@font-face` for local/
   licensed fonts — required for corporate brands like Slalom that don't ship on
   Google Fonts).
4. Set `<body class="theme-yourbrand">`.
5. Render and QA under that theme — verify all formats used in the deck.

To derive a theme from a `design.md` (yours, Slalom's, or the awesome-design-md
library), see `design-md-ingestion.md`.
