#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

MODULES=("room","breakfast","facilities","city","wifi","stay","contact")

ap=argparse.ArgumentParser()
ap.add_argument("--config",required=True,type=Path)
ap.add_argument("--html",required=True,type=Path)
args=ap.parse_args()

cfg=json.loads(args.config.read_text(encoding="utf-8"))
s=args.html.read_text(encoding="utf-8")

checks={
    "core title":"Hospitality Core v2" in s,
    "brand":cfg["property"]["name"] in s,
    "no RIVER":"RIVER HOTEL" not in s
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

ids=re.findall(r'\sid="([^"]+)"',s)
checks["duplicate ids"]=len(ids)==len(set(ids))

for k,v in checks.items():
    print(("PASS" if v else "FAIL"),k)

if not all(checks.values()):
    raise SystemExit(1)
