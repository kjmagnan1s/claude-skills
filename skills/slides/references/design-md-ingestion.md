# Deriving a Theme from a design.md

A `design.md` (or `DESIGN.md`) is a design-system spec: palette, typography,
spacing, radii, shadows. This skill turns one into a deck theme so a deck can be
generated on-brand — your personal projects, a Slalom client brand, or any of the
54 systems in the local library.

## Where design.md files come from

1. **Project root** — if the current repo has a `design.md`/`DESIGN.md`, use it.
2. **The awesome-design-md library** — `~/.claude/awesome-design-md/design-md/`
   has 54 systems (Airbnb, Apple, Stripe, Vercel, Linear, Notion, Figma, Cursor…).
   Each folder holds `DESIGN.md` + `preview.html`. List with
   `ls ~/.claude/awesome-design-md/design-md/`.
3. **A path the user gives** — e.g. a Slalom brand `design.md` they drop in.
4. **The `design-md` skill** — invoke it to generate or normalize a design.md
   first if the brand only has scattered brand guidelines.

## Mapping design.md → token contract

Read the design.md and fill the token table from `templates.md`. Map by role,
not by name:

| design.md concept | → token |
|-------------------|---------|
| page / canvas background | `--bg` (light) and `--bg-i` (dark variant) |
| card / panel / elevated surface | `--surface`, `--surface-2` |
| primary text / foreground | `--ink` (and `--ink-i` on dark) |
| muted / secondary text | `--ink-soft` (and `--ink-soft-i`) |
| primary brand / CTA color | `--accent` |
| secondary brand or a lighter brand tint | `--accent-2` |
| brand color at ~10–15% alpha | `--accent-soft` |
| text that sits on the brand color | `--accent-ink` (usually white or near-black) |
| divider / border color | `--border` |
| heading / display typeface | `--font-display` (+ `--display-weight`, `--display-tracking`) |
| body typeface | `--font-body` |
| mono / code typeface | `--font-mono` |
| corner radius scale | `--radius`, `--radius-sm` |
| elevation / shadow | `--shadow`, `--shadow-soft` |

Rules when mapping:
- **Pick ONE accent.** If the brand has many colors, choose the primary CTA color.
  Use neutrals for everything else. Decks die when every brand color competes.
- **Contrast first.** Ensure `--ink` on `--bg` and `--accent-ink` on `--accent`
  both clear WCAG AA (≥ 4.5:1 for body). If the brand accent is light, set
  `--accent-ink` to a dark ink.
- **Always produce the `*-i` invert set** so cover/quote/closing have a dark
  counterpart. If the brand has a documented dark mode, use it; otherwise derive
  a deep neutral from the brand's darkest text color.
- If `preview.html` exists in the library folder, open it to confirm the look.

## Fonts

- If the brand fonts are on Google Fonts, add them to the deck's `<link>`.
- If they're **licensed/custom** (common for corporate brands like Slalom),
  reference local files via `@font-face` inside the deck's `<style>` and tell the
  user which font files the deck expects in the same folder. Never silently
  substitute a corporate font without flagging it.
- No brand font available → use the closest Google Fonts pairing and say so.

## Output

Produce a `body.theme-<brand>` block (copy an existing one in the scaffold, swap
tokens), wire up the fonts, set `<body class="theme-<brand>">`, then build and QA
the deck under it. Offer to save the theme block back into the scaffold so the
brand becomes a permanent built-in theme.

## Slalom workflow (the recurring professional use case)

1. Get Slalom's `design.md` (or run the `design-md` skill on Slalom brand
   guidelines to create one). Keep it somewhere stable, e.g.
   `~/.claude/skills/slides/assets/brands/slalom/design.md` plus its font files.
2. Derive `body.theme-slalom` per the mapping above; save it into the scaffold so
   it's a one-word theme from then on.
3. New client deck → outline → `theme-slalom` → generate → QA → deliver. On-brand
   in minutes, every time.
