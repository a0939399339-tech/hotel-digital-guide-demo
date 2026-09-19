#!/usr/bin/env python3
"""
Create truthful, high-resolution portfolio captures from the real assembled LUME site.

This script does NOT redraw or reinterpret the guest UI. It opens the exact staging
HTML in headless Chromium and screenshots the actual DOM sections used by the site.
"""
import argparse
import shutil
import subprocess
import time
from pathlib import Path

SECTIONS = [
    ("room", "02-room.png"),
    ("breakfast", "03-breakfast.png"),
    ("city", "04-city.png"),
    ("wifi", "05-wifi.png"),
    ("stay", "06-stay.png"),
]

def chrome_binary():
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Chromium/Chrome not found. Install chromium before capture.")

def capture(chrome, html, selector, output):
    # Chromium headless supports element screenshots only through DevTools; use a
    # temporary print-friendly capture page that contains the original DOM section
    # unchanged and hides every other section.
    wrapper = html.parent / f".capture-{selector}.html"
    original = html.read_text(encoding="utf-8")
    injection = f"""
<style id="portfolio-capture-guard">
html,body{{margin:0!important;padding:0!important;background:#fffaf6!important;}}
body>section{{display:none!important;}}
body>section#{selector}{{display:block!important;}}
body>nav.lang-float{{display:none!important;}}
body>section#{selector} .wrap{{max-width:430px!important;margin:0 auto!important;}}
body>section#{selector} .back{{visibility:hidden!important;}}
</style>
"""
    wrapper.write_text(original.replace("</head>", injection + "</head>"), encoding="utf-8")
    try:
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=2",
            "--window-size=430,5000",
            "--virtual-time-budget=2000",
            f"--screenshot={output.resolve()}",
            wrapper.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
        wrapper.unlink(missing_ok=True)

def trim_bottom(path):
    # Keep the full real section but remove the unused browser canvas below it.
    from PIL import Image, ImageChops
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((0, im.height - 1)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        bottom = min(im.height, bbox[3] + 48)
        im.crop((0, 0, im.width, bottom)).save(path, quality=95)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    if not args.html.exists():
        raise SystemExit(f"HTML not found: {args.html}")

    chrome = chrome_binary()
    args.output.mkdir(parents=True, exist_ok=True)

    for section, filename in SECTIONS:
        output = args.output / filename
        capture(chrome, args.html, section, output)
        trim_bottom(output)
        print("PASS real UI capture", section, output)

if __name__ == "__main__":
    main()
