#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

MODULES=("room","breakfast","facilities","city","wifi","stay","contact")
DEMO_PROPERTY="LUME HOTEL"
DEMO_ONLY_MARKERS=(
    "LUME HOTEL",
    "DEMO HOTEL",
    "FICTIONAL PROPERTY",
    "DEMO-ONLY-",
    "虛構示範旅宿",
    "示範站使用假帳密",
)

ap=argparse.ArgumentParser()
ap.add_argument("--config",required=True,type=Path)
ap.add_argument("--html",required=True,type=Path)
ap.add_argument("--css",type=Path)
args=ap.parse_args()

cfg=json.loads(args.config.read_text(encoding="utf-8"))
s=args.html.read_text(encoding="utf-8")
css=args.css.read_text(encoding="utf-8") if args.css else ""
compact_css=re.sub(r"\s+","",css)

checks={
    "core title":"Hospitality Core v2" in s,
    "brand":cfg["property"]["name"] in s,
    "no RIVER":"RIVER HOTEL" not in s,
    "external theme css":(not args.css) or ("styles.css" in s and bool(css)),
    "theme bg":(not args.css) or (f"--bg:{cfg.get('theme',{}).get('bg','#fffaf6')}" in compact_css),
    "theme accent":(not args.css) or (f"--accent:{cfg.get('theme',{}).get('accent','#c97a3d')}" in compact_css),
    "theme accent soft":(not args.css) or (f"--accent-soft:{cfg.get('theme',{}).get('accent_soft','#fff1e6')}" in compact_css)
}

for m in MODULES:
    expected=bool(cfg["modules"].get(m))
    if m=="facilities" and not cfg.get("facilities"):
        expected=False
    checks[f"module {m}"]=(f'id="{m}"' in s)==expected
    checks[f"nav {m}"]=(f'href="#{m}"' in s)==expected

if cfg["modules"].get("wifi"):
    checks["wifi ssid"]=cfg["wifi"]["ssid"] in s
    checks["wifi qr ref"]=cfg["wifi"]["qr_asset"] in s
    checks["wifi qr file"]=(args.html.parent/cfg["wifi"]["qr_asset"]).exists()

# Client builds must not inherit demo-only branding or fictional disclosure text.
# The public LUME HOTEL demo is intentionally exempt.
if cfg["property"]["name"].strip() != DEMO_PROPERTY:
    for marker in DEMO_ONLY_MARKERS:
        checks[f"no demo residue: {marker}"]=marker not in s

ids=re.findall(r'\sid="([^"]+)"',s)
checks["duplicate ids"]=len(ids)==len(set(ids))

for k,v in checks.items():
    print(("PASS" if v else "FAIL"),k)

if not all(checks.values()):
    raise SystemExit(1)
