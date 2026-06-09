---
name: designed-pdf
description: >-
  Create polished, design-led PDFs FROM SCRATCH — starting from just a topic and
  optional content, not from an existing PDF. Produces visually distinctive
  multi-page PDFs such as LinkedIn/Instagram carousels, one-pagers, pitch
  one-sheets, explainer decks, leaflets/flyers, mini-reports, and branded
  handouts by designing fixed-canvas HTML pages and rendering them crisply via
  headless Chromium. Use this skill whenever the user wants a "nice"/"good
  looking"/"polished"/"designed" PDF, a carousel, a one-pager, a handout,
  leaflet, flyer, visual explainer, or wants to "make a PDF" that should look
  designed rather than a plain text document — even when they give only a topic
  and a little content. Do NOT use this for editing/reading an existing PDF, or
  for long plain-text documents (use the `pdf` skill for manipulation and the
  `docx`/`md` skills for text documents).
---

# Designed PDF (from scratch)

Build attractive, intentional PDFs from a topic and (optionally) some content.
The output is a fixed-canvas, multi-page visual document — the kind shared as a
carousel, sent as a one-pager, or handed out as a leaflet — not a wall of text.

This skill stands on two others. Read them, briefly, before designing:
- **`frontend-design`** — the design discipline (palette/type/layout/signature,
  the two-pass plan, and self-critique). This is where the *quality* comes from.
- **`pdf`** — awareness of the PDF toolchain. Note: that skill's reportlab
  recipes are for plain/programmatic PDFs; for *designed* output, render HTML
  instead (below). Reach for the `pdf` skill's tools only if you later need to
  merge, encrypt, or post-process the result.

## Why HTML -> Chromium -> image-PDF

Designed layout (gradients, flexbox, web fonts, SVG icons, precise spacing) is
far easier and more faithful in HTML/CSS than in reportlab, and headless
Chromium renders it pixel-perfectly. Screenshotting each page at 2x and
assembling a PDF gives crisp, shareable output with zero layout surprises. This
is the pipeline `scripts/render_pdf.py` implements.

## Workflow

### 1. Pin the brief (don't skip)
From the topic, name three things explicitly, in one line each: the **subject**
(what it's about), the **audience**, and the **format + dimensions** (see
`references/design-recipes.md` -> Page dimensions; default 4:5 carousel for
social, A4 portrait for a document). If the user gave content, list the pages
you'll make from it. If they gave only a topic, draft the page list and the copy
yourself — thin copy makes a design feel as templated as a generic layout, so
write real, specific lines. Keep any factual claims defensible; don't invent
statistics or attribute quotes.

### 2. Make a design plan (one short pass, mostly in your head)
Following `frontend-design`, decide a compact token system specific to this
brief: **color** (4-6 named hex with explicit roles), **type** (display / body /
utility-mono pairing), **layout** concept, and the one **signature** element the
piece will be remembered by. `references/design-recipes.md` has ready-to-tune
palettes, type pairings, layout devices, and signature ideas. Then critique the
plan: if any part reads like the generic default you'd produce for any similar
topic, change it and note why. Spend boldness in one place; keep the rest quiet.

### 3. Build the HTML
Copy `assets/page-skeleton.html` as a starting point. Rules that keep it clean:
- **One element per page** with a shared class (default `.page`), each sized to
  exactly the chosen width x height in px. Render order = document order.
- Put all colors/spacing in CSS variables; derive every value from the plan.
- Use the bundled fonts in `assets/fonts/` via `@font-face`. Make the paths
  resolve: either copy `assets/fonts/` next to your HTML and use relative
  `url('fonts/Inter.ttf')`, or use absolute paths to the skill's font files.
- **Vertically center content blocks** in their free space (`margin:auto 0`),
  rather than pinning to the top and leaving an empty bottom — that empty
  bottom is the #1 "unfinished" tell.
- **Turn lists into devices** (comparison columns with a `vs` node, a real
  timeline, a dominant stat, faded-vs-saturated before/after). Draw symbols as
  inline **SVG**, never emoji/font glyphs (missing glyphs render as boxes).
- A repeating footer (wordmark + `01 / N` page index + hairline) and a thin
  accent progress bar bind a multi-page set together.

### 4. Render and CRITIQUE (this loop is what makes it good)
Install deps once if needed, then render:
```bash
pip install playwright pillow --break-system-packages   # if not present
python scripts/render_pdf.py --html deck.html --out out/deck.pdf \
    --selector .page --width 1080 --height 1350 --scale 2
```
The script writes the PDF **and** `..._contact_sheet.png` (all pages tiled).
**View the contact sheet.** Look hard for: dead space / top-pinned content,
weak hierarchy, tiny floating elements, clipped or overflowing text, misaligned
baselines, inconsistent margins, and whether the signature actually lands. Fix
the HTML and re-render. Do at least one critique pass — usually two. Spot-check
any complex page at full resolution (open its PNG) to catch glyph boxes or
overflow the thumbnail hides.

### 5. Deliver
Write the final PDF to `/mnt/user-data/outputs/` and present it with
`present_files`. Offer obvious follow-ups (export pages as PNGs for direct
carousel posting, change the accent, tweak one page). Keep the summary short:
say what you designed and the few deliberate choices you made.

## Boundaries
- Fixed-canvas designed documents only. For continuous, reflowing long-form text
  (multi-page essays/reports), prefer `docx`/`md`; for manipulating an existing
  PDF, use `pdf`.
- Output is raster at the chosen scale. 2x is sharp for screen and normal print;
  bump `--scale` for print-grade. Selectable text is not preserved — that's the
  trade for exact visual fidelity.

## Files
- `scripts/render_pdf.py` — HTML pages -> crisp PDF + review contact sheet (CLI).
- `references/design-recipes.md` — palettes, type pairings, layout devices,
  signature ideas, page dimensions. Read when planning the design.
- `assets/page-skeleton.html` — minimal starting HTML (tokens, page, footer,
  progress bar).
- `assets/fonts/` — bundled OFL typefaces (Space Grotesk, Inter, Space Mono) so
  the skill works offline; see `NOTICE.txt`.
