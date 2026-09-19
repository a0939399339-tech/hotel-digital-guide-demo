#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

MODULES = ("room", "breakfast", "facilities", "city", "wifi", "stay", "contact")
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
ALLOWED_WIFI_SECURITY = {"WPA", "WEP", "nopass"}

def require(condition, message, errors):
    if not condition:
        errors.append(message)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, type=Path)
    args = ap.parse_args()

    errors = []

    try:
        cfg = json.loads(args.config.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Config not found: {args.config}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")

    require(isinstance(cfg, dict), "config root must be an object", errors)
    if not isinstance(cfg, dict):
        for msg in errors:
            print("FAIL", msg)
        raise SystemExit(1)

    require(cfg.get("schema_version") == "2.0", "schema_version must be 2.0", errors)

    prop = cfg.get("property")
    require(isinstance(prop, dict), "property must be an object", errors)
    if isinstance(prop, dict):
        require(nonempty(prop.get("name")), "property.name is required", errors)
        require(nonempty(prop.get("footer")), "property.footer is required", errors)

    modules = cfg.get("modules")
    require(isinstance(modules, dict), "modules must be an object", errors)
    if isinstance(modules, dict):
        for module in MODULES:
            require(module in modules, f"modules.{module} is required", errors)
            if module in modules:
                require(isinstance(modules[module], bool), f"modules.{module} must be boolean", errors)

    theme = cfg.get("theme", {})
    require(isinstance(theme, dict), "theme must be an object", errors)
    if isinstance(theme, dict):
        for key in ("accent", "accent_soft", "bg"):
            value = theme.get(key)
            require(nonempty(value), f"theme.{key} is required", errors)
            if nonempty(value):
                require(bool(HEX_COLOR.fullmatch(value)), f"theme.{key} must be a 6-digit hex color", errors)

    if isinstance(modules, dict) and modules.get("wifi"):
        wifi = cfg.get("wifi")
        require(isinstance(wifi, dict), "wifi must be an object when Wi-Fi module is enabled", errors)
        if isinstance(wifi, dict):
            require(nonempty(wifi.get("ssid")), "wifi.ssid is required", errors)
            security = wifi.get("security")
            require(security in ALLOWED_WIFI_SECURITY, "wifi.security must be WPA, WEP, or nopass", errors)
            require(isinstance(wifi.get("hidden"), bool), "wifi.hidden must be boolean", errors)
            require(nonempty(wifi.get("qr_asset")), "wifi.qr_asset is required", errors)
            qr_asset = wifi.get("qr_asset", "")
            if isinstance(qr_asset, str):
                require(not qr_asset.startswith("/") and ".." not in Path(qr_asset).parts,
                        "wifi.qr_asset must be a safe relative path", errors)
            if security != "nopass":
                require(nonempty(wifi.get("password")), "wifi.password is required for secured networks", errors)

    if isinstance(modules, dict) and modules.get("breakfast"):
        breakfast = cfg.get("breakfast")
        require(isinstance(breakfast, dict), "breakfast must be an object when breakfast module is enabled", errors)
        if isinstance(breakfast, dict):
            for key in ("hours", "last_entry", "location_zh", "location_en"):
                require(nonempty(breakfast.get(key)), f"breakfast.{key} is required", errors)

    if isinstance(modules, dict) and modules.get("facilities"):
        facilities = cfg.get("facilities")
        require(isinstance(facilities, list) and len(facilities) > 0,
                "facilities must contain at least one item when facilities module is enabled", errors)
        if isinstance(facilities, list):
            for i, item in enumerate(facilities):
                require(isinstance(item, dict), f"facilities[{i}] must be an object", errors)
                if isinstance(item, dict):
                    for key in ("id", "name_zh", "name_en", "hours_zh", "hours_en",
                                "location_zh", "location_en", "equipment_zh", "equipment_en"):
                        require(nonempty(item.get(key)), f"facilities[{i}].{key} is required", errors)

    if isinstance(modules, dict) and modules.get("city"):
        nearby = cfg.get("nearby")
        require(isinstance(nearby, list) and len(nearby) > 0,
                "nearby must contain at least one item when city module is enabled", errors)
        if isinstance(nearby, list):
            for i, item in enumerate(nearby):
                require(isinstance(item, dict), f"nearby[{i}] must be an object", errors)
                if isinstance(item, dict):
                    for key in ("category", "name_zh", "name_en", "map_query"):
                        require(nonempty(item.get(key)), f"nearby[{i}].{key} is required", errors)

    if isinstance(modules, dict) and modules.get("stay"):
        stay = cfg.get("stay")
        require(isinstance(stay, dict), "stay must be an object when stay module is enabled", errors)
        if isinstance(stay, dict):
            for key in ("check_in_zh", "check_in_en", "check_out_zh", "check_out_en",
                        "front_desk_zh", "front_desk_en"):
                require(nonempty(stay.get(key)), f"stay.{key} is required", errors)

    if isinstance(modules, dict) and modules.get("contact"):
        contact = cfg.get("contact")
        require(isinstance(contact, dict), "contact must be an object when contact module is enabled", errors)
        if isinstance(contact, dict):
            require(nonempty(str(contact.get("front_desk_extension", "")).strip()),
                    "contact.front_desk_extension is required", errors)

    if errors:
        for msg in errors:
            print("FAIL", msg)
        raise SystemExit(1)

    print("PASS config preflight", args.config)

if __name__ == "__main__":
    main()
