#!/usr/bin/env python3
"""
Render fixed-canvas HTML pages into a crisp, design-faithful PDF.

Each "page" is one HTML element matching --selector (default `.page`), with a
fixed pixel size (e.g. 1080x1350 for a 4:5 carousel). The script screenshots
each page at high DPI via headless Chromium (pixel-perfect CSS fidelity:
gradients, flexbox, web fonts, SVG) and assembles them into a multi-page PDF.

It also writes a CONTACT SHEET (all pages tiled into one PNG) so you can review
the whole deck at a glance and critique it before finalizing — this review loop
is the difference between "fine" and "good".

Usage:
    python render_pdf.py --html deck.html --out final.pdf
    python render_pdf.py --html deck.html --out final.pdf \
        --selector .page --width 1080 --height 1350 --scale 2

Notes:
- Loads the HTML via file:// so relative url('fonts/..') in @font-face resolve.
  Keep your font files reachable from the HTML's folder (or use absolute paths).
- Pages are screenshotted in document order. Size each page element to exactly
  --width x --height (px) in your CSS, or pass the size you used.
- Output PDF is raster at --scale x; at scale 2 text is sharp on screen/print
  for shareable docs. Use a higher scale for print-grade output.
"""
import argparse, os, sys, tempfile

def main():
    ap = argparse.ArgumentParser(description="Render HTML pages to a crisp PDF.")
    ap.add_argument("--html", required=True, help="Path to the HTML file.")
    ap.add_argument("--out", required=True, help="Output PDF path.")
    ap.add_argument("--selector", default=".page", help="CSS selector for each page element.")
    ap.add_argument("--width", type=int, default=1080, help="Page width in px.")
    ap.add_argument("--height", type=int, default=1350, help="Page height in px.")
    ap.add_argument("--scale", type=float, default=2.0, help="Device scale factor (DPI multiplier).")
    ap.add_argument("--dpi", type=float, default=144.0, help="PDF resolution metadata.")
    ap.add_argument("--no-contact-sheet", action="store_true", help="Skip the review contact sheet.")
    ap.add_argument("--wait", type=int, default=500, help="ms to wait for fonts/layout before shooting.")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright not installed. Run: pip install playwright --break-system-packages")
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow not installed. Run: pip install pillow --break-system-packages")

    html_path = os.path.abspath(args.html)
    if not os.path.exists(html_path):
        sys.exit(f"HTML not found: {html_path}")
    workdir = os.path.dirname(args.out) or "."
    os.makedirs(workdir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="render_pages_")

    png_paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page.goto("file://" + html_path)
        page.wait_for_timeout(args.wait)
        try:
            page.evaluate("document.fonts && document.fonts.ready")
        except Exception:
            pass
        els = page.query_selector_all(args.selector)
        if not els:
            browser.close()
            sys.exit(f"No elements match selector '{args.selector}'. "
                     f"Wrap each page in an element with that class.")
        for i, el in enumerate(els, 1):
            out = os.path.join(tmp, f"page_{i:02d}.png")
            el.screenshot(path=out)
            png_paths.append(out)
        browser.close()

    imgs = [Image.open(p).convert("RGB") for p in png_paths]
    imgs[0].save(args.out, "PDF", resolution=args.dpi, save_all=True,
                 append_images=imgs[1:])
    print(f"PDF written: {args.out}  ({len(imgs)} pages @ {imgs[0].size})")

    if not args.no_contact_sheet:
        sheet_path = os.path.splitext(args.out)[0] + "_contact_sheet.png"
        n = len(imgs)
        cols = min(4, n)
        rows = (n + cols - 1) // cols
        sc = 0.40
        tw, th = int(imgs[0].width * sc), int(imgs[0].height * sc)
        sheet = Image.new("RGB", (tw * cols, th * rows), "#cfcfcf")
        for i, im in enumerate(imgs):
            sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
        sheet.save(sheet_path)
        print(f"Contact sheet: {sheet_path}  (view it, critique, then iterate)")

if __name__ == "__main__":
    main()
