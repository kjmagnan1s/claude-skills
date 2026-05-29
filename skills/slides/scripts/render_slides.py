#!/usr/bin/env python3
"""
render_slides.py — Visual-QA renderer for /slides decks.

Renders every slide of a self-contained deck HTML to a PNG so a fresh-eyes
reviewer can inspect layout. It isolates each slide, disables scroll-snap,
and emulates prefers-reduced-motion so the deck engine FREEZES every animation
to its final state (counters land on their end value, reveals are fully shown,
charts draw instantly). What you screenshot is what the audience ends on.

Usage:
    python3 render_slides.py --html output/slides/my-deck.html
    python3 render_slides.py --html my-deck.html --out output/slides/qa --scale 2
    python3 render_slides.py --html my-deck.html --pdf      # export a shareable PDF

Prints one output path per line. Requires Playwright:
    pip install playwright && python3 -m playwright install chromium
"""
import argparse, os, sys, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, help="path to the deck .html file")
    ap.add_argument("--out", default=None, help="output dir (default: <deck-dir>/qa)")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=int, default=2, help="device scale factor (2 = retina)")
    ap.add_argument("--settle", type=int, default=450, help="ms to wait after each slide before shooting")
    ap.add_argument("--pdf", action="store_true", help="export one landscape PDF (a page per slide) instead of PNGs")
    args = ap.parse_args()

    html_path = pathlib.Path(args.html).expanduser().resolve()
    if not html_path.exists():
        sys.exit(f"ERROR: file not found: {html_path}")

    out_dir = pathlib.Path(args.out).expanduser().resolve() if args.out \
        else html_path.parent / "qa"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("ERROR: Playwright not installed. Run:\n"
                 "  pip install playwright && python3 -m playwright install chromium")

    # CSS injected before paint: kill snap, freeze reveals/bars to final, hide chrome.
    freeze_css = """
      html,.deck{scroll-behavior:auto!important;scroll-snap-type:none!important}
      [data-reveal]{opacity:1!important;transform:none!important;filter:none!important;transition:none!important}
      .draw-line,.is-active .draw-line{transform:none!important}
      .bar>span{transition:none!important}
      .anno svg path{stroke-dashoffset:0!important;transition:none!important}
      .uline::after{transform:scaleX(1)!important;transition:none!important}
      .float,.pulse{animation:none!important}
      .deck-dots,.deck-progress,.deck-hint{display:none!important}
    """

    # ---- PDF export: one landscape page per slide, charts/counters at final state ----
    if args.pdf:
        pdf_path = html_path.parent / (html_path.stem + ".pdf")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_context(reduced_motion="reduce").new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")
            n = page.eval_on_selector_all(".slide", "els => els.length")
            if not n:
                sys.exit("ERROR: no .slide elements found — is this a /slides deck?")
            # scroll through so each slide's IntersectionObserver fires charts + counters
            for i in range(n):
                page.evaluate("(i)=>document.querySelectorAll('.slide')[i].scrollIntoView()", i)
                page.wait_for_timeout(140)
            page.add_style_tag(content=freeze_css + """
              @page{size:1280px 720px;margin:0}
              html,body{height:auto!important;overflow:visible!important;background:#fff!important}
              .deck{height:auto!important;overflow:visible!important;display:block!important;scroll-snap-type:none!important}
              .slide{height:720px!important;width:1280px!important;break-after:page;page-break-after:always}
              .slide:last-child{break-after:auto;page-break-after:auto}
            """)
            page.evaluate("""() => {
                document.querySelectorAll('.slide').forEach(s=>s.classList.add('is-active'));
                document.querySelectorAll('.bar>span').forEach(s=>{
                  const f=getComputedStyle(s.closest('.bar')).getPropertyValue('--fill')||'70%';
                  s.style.width=f;
                });
            }""")
            page.wait_for_timeout(args.settle)
            page.pdf(path=str(pdf_path), width="1280px", height="720px",
                     print_background=True, prefer_css_page_size=True)
            browser.close()
        print(pdf_path)
        return [pdf_path]

    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
            reduced_motion="reduce",   # makes the deck engine jump to final state
        )
        page = ctx.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.add_style_tag(content=freeze_css)
        # force the fill bars to their target width now that transitions are off
        page.evaluate("""() => {
            document.querySelectorAll('.bar>span').forEach(s=>{
              const f=getComputedStyle(s.closest('.bar')).getPropertyValue('--fill')||'70%';
              s.style.width=f;
            });
            document.querySelectorAll('.slide').forEach(s=>s.classList.add('is-active'));
        }""")
        n = page.eval_on_selector_all(".slide", "els => els.length")
        if not n:
            sys.exit("ERROR: no .slide elements found — is this a /slides deck?")

        for i in range(n):
            # scroll slide i into view; its IntersectionObserver fires count-up + charts
            page.evaluate("(i)=>document.querySelectorAll('.slide')[i].scrollIntoView()", i)
            page.wait_for_timeout(args.settle)
            out = out_dir / f"slide-{i+1:02d}.png"
            page.screenshot(path=str(out))
            print(out)
            paths.append(out)

        browser.close()

    return paths

if __name__ == "__main__":
    main()
