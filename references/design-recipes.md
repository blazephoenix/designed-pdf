# Design recipes

Concrete starting points so the design plan isn't a blank page. These are
*ingredients*, not a fixed look. Always tune them to the specific subject — a
fintech security one-pager and a kids' summer-camp flyer should not share a
palette. The `frontend-design` skill's warning applies: don't default to the
three generic AI looks (cream+serif+terracotta; near-black+one-acid-accent;
broadsheet hairlines). Pick deliberately.

## Page dimensions (px, before scale)

| Format | Size | Ratio | Notes |
|---|---|---|---|
| LinkedIn / IG carousel (portrait) | 1080 × 1350 | 4:5 | best feed real estate |
| Square carousel | 1080 × 1080 | 1:1 | safe everywhere |
| Story / vertical | 1080 × 1920 | 9:16 | full-screen mobile |
| One-pager / flyer (A4 portrait) | 1240 × 1754 | √2 | ~150dpi A4 |
| US Letter portrait | 1275 × 1650 | ~3:4 | ~150dpi Letter |
| Slide deck (landscape) | 1920 × 1080 | 16:9 | presentation |
| Pitch one-sheet (landscape) | 1754 × 1240 | √2 | A4 landscape |

Pick the format from how it will be *used* (scrolled feed → portrait carousel;
printed/emailed → A4/Letter; presented → 16:9). When unsure, ask or default to
4:5 carousel for social, A4 portrait for a document.

## Color token systems (4–6 named hex each)

Define exactly these roles every time: a base/background, a deep ink for text,
1 accent (used with restraint), 1 soft accent-wash for highlight panels, plus
muted text tints for each background. Examples:

- **Ink + signal mint** (technical/compliance/SaaS): base `#0A1826`, panel
  `#0F2236`, accent `#1FE3A4`, wash `#E6FAF2`, paper `#F4F7F5`, muted-on-dark
  `#8A9DAD`. (This is the Konfirmity family.)
- **Warm editorial** (lifestyle/wellness/food): paper `#F3EDE3`, ink `#241C16`,
  accent `#C8553D`, wash `#EFD9C6`, muted `#7A6E62`.
- **Cobalt corporate** (finance/legal/B2B): paper `#F5F7FB`, ink `#0C1B3A`,
  accent `#2F6BFF`, wash `#E4ECFF`, muted `#5A6B8C`.
- **Botanical** (sustainability/health): paper `#F4F6F1`, ink `#1B2A1E`,
  accent `#3F7D52`, wash `#E2EFE2`, muted `#5F6F60`.
- **Plum dusk** (creative/events/beauty): base `#1A1326`, ink-text `#F2ECF7`,
  accent `#E5A3FF`, second `#FFC76B`, muted `#9A8AB0`.

Rule of thumb: dark backgrounds for statement/hero/CTA pages; light for
evidence/detail/list pages; one fully-saturated accent page reserved for the
single most important line (a punchline or key stat) to break the rhythm.

## Type pairings (display / body / utility-mono)

Bundled in `assets/fonts/`: **Space Grotesk** (display), **Inter** (body),
**Space Mono** (utility). They cover most briefs. Alternatives (all OFL, fetch
from github.com/google/fonts raw if network allows): Fraunces / Bricolage
Grotesque / Clash-like grotesques for display; Source Serif, Newsreader,
IBM Plex Sans for body; IBM Plex Mono, JetBrains Mono, Space Mono for utility.

Use the mono face as *texture*, not body copy: eyebrows, labels, data, dates,
page numbers, clause/reference codes. It reads as "technical/edited" and is a
cheap way to make a layout feel intentional. Set a real type scale — e.g.
display 56–80px, section 34–44px, body 22–28px, mono labels 16–19px with wide
letter-spacing (.16–.32em) and uppercase.

## Layout & structure patterns

- **Consistent margins + a repeating footer** (wordmark left, page index
  `01 / 08` right, hairline divider) makes a set of pages feel like one
  artifact. A thin accent progress bar along the bottom edge is a strong, quiet
  unifier for carousels.
- **Eyebrow → headline → rule → subhead** is a reliable page header stack.
- **Center content vertically** in the free space (`margin: auto 0`) rather than
  pinning to the top — top-pinned content with an empty bottom third is the
  most common "unfinished" tell.
- **Turn lists into devices**: a 3-item comparison becomes two contrasting
  columns with a `vs` node; a before/after becomes faded vs. saturated; a
  timeline becomes a real horizontal track with labelled nodes; a big number
  becomes a dominant numeral, not a small centered figure.
- **Numbering (01/02/03) only when order is real** (a process, ranked list,
  timeline). Don't decorate with it otherwise.

## Signature element (the one memorable thing)

Every good piece has one. Spend boldness here and keep everything else quiet.
Ground it in the subject's own world:
- a compliance deck → a faint procurement-checklist motif with one item ticked;
- a recipe card → a hand-numbered ingredient ledger;
- a finance one-pager → a ghosted ticker/series line behind the hero number;
- an events flyer → an oversized date as the hero.
Reuse it lightly across pages (e.g. on cover + closing) to bind the set.

## Iconography

Draw small icons as inline SVG (checks, arrows, clocks, dots). Avoid relying on
emoji or font glyphs for symbols — glyph coverage in bundled fonts is partial
and missing glyphs render as boxes. Inline SVG always renders and inherits the
accent color via `stroke`/`fill`.
