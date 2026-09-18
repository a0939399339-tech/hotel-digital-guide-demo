#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
import qrcode
from qrcode.image.svg import SvgPathImage

MODULES=("room","breakfast","facilities","city","wifi","stay","contact")

def esc_wifi(v):
    for ch in ("\\",";",",",":",'"'):
        v=v.replace(ch,"\\"+ch)
    return v

def wifi_payload(w):
    sec=w.get("security","WPA")
    hidden="true" if w.get("hidden") else "false"
    ssid=esc_wifi(w["ssid"])
    if sec=="nopass":
        return f"WIFI:T:nopass;S:{ssid};H:{hidden};;"
    return f"WIFI:T:{sec};S:{ssid};P:{esc_wifi(w.get('password',''))};H:{hidden};;"

def set_i18n(el, zh, en):
    if el is None:
        return
    el["data-zh"]=zh
    el["data-en"]=en
    el.string=zh

def remove_module(soup, module):
    sec=soup.find(id=module)
    if sec:
        sec.decompose()
    home=soup.find(id="home")
    if home:
        for a in home.select(f'a[href="#{module}"]'):
            a.decompose()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True,type=Path)
    ap.add_argument("--html",required=True,type=Path)
    ap.add_argument("--css",type=Path)
    args=ap.parse_args()

    cfg=json.loads(args.config.read_text(encoding="utf-8"))
    if cfg.get("schema_version")!="2.0":
        raise SystemExit("schema_version must be 2.0")

    soup=BeautifulSoup(args.html.read_text(encoding="utf-8"),"html.parser")

    # Property identity + theme tokens.
    name=cfg["property"]["name"]
    if soup.title:
        soup.title.string=f"{name} — Hospitality Core v2"
    for el in soup.select(".brand"):
        if el.get_text(strip=True)=="LUME HOTEL":
            el.string=name
    hero=soup.find(id="landing")
    if hero:
        eyebrow=hero.select_one(".eyebrow")
        if eyebrow:
            eyebrow.string=cfg["property"].get("hero_eyebrow","CITY STAY")
        h1=hero.find("h1")
        if h1:
            h1.string=name
    footer=soup.select_one(".footer")
    if footer:
        footer.string=cfg["property"].get("footer",footer.get_text(strip=True))

    # Theme tokens are applied to the extracted stylesheet. Keep the inline
    # fallback for older templates during migration.
    t=cfg.get("theme",{})
    if args.css:
        css=args.css.read_text(encoding="utf-8")
        for token,value in (
            ("bg",t.get("bg","#fffaf6")),
            ("accent",t.get("accent","#c97a3d")),
            ("accent-soft",t.get("accent_soft","#fff1e6"))
        ):
            pattern=rf"(--{re.escape(token)}\s*:\s*)[^;}}]+"
            css,count=re.subn(pattern,lambda m:m.group(1)+value,css,count=1)
            if count!=1:
                raise SystemExit(f"theme token --{token} not found in {args.css}")
        args.css.write_text(css,encoding="utf-8")
    else:
        style=soup.find("style")
        if style:
            style.append(
                f":root{{--bg:{t.get('bg','#fffaf6')};"
                f"--accent:{t.get('accent','#c97a3d')};"
                f"--accent-soft:{t.get('accent_soft','#fff1e6')}}}"
            )

    # Module switches: false removes both homepage entry and section.
    mods=cfg["modules"]
    if mods.get("facilities") and not cfg.get("facilities"):
        mods["facilities"]=False
    for m in MODULES:
        if not mods.get(m,False):
            remove_module(soup,m)

    # Wi-Fi: QR is generated from config, never hand-authored.
    if mods.get("wifi"):
        w=cfg["wifi"]
        wifi=soup.find(id="wifi")
        if wifi:
            ssid=wifi.find(id="wifi-ssid")
            pwd=wifi.find(id="wifi-pass")
            if ssid:
                ssid.string=w["ssid"]
            if pwd:
                pwd.string=w.get("password","—") if w.get("security")!="nopass" else "—"

            qr=wifi.select_one(".wifi-qr-card img")
            if qr:
                qr["src"]=w["qr_asset"]
                qr["alt"]=f"{name} Guest Wi-Fi QR Code"
            cap=wifi.select_one(".wifi-qr-card figcaption")
            set_i18n(cap,f"掃描直接連線 · {w['ssid']}",f"Scan to join {w['ssid']}")

            buttons=wifi.select(".wifi-actions [data-copy]")
            if len(buttons)>0:
                buttons[0]["data-copy"]=w["ssid"]
            if len(buttons)>1:
                buttons[1]["data-copy"]=w.get("password","")

        qr_path=args.html.parent / w["qr_asset"]
        qr_path.parent.mkdir(parents=True,exist_ok=True)
        q=qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            border=4,
            box_size=10
        )
        q.add_data(wifi_payload(w))
        q.make(fit=True)
        q.make_image(image_factory=SvgPathImage).save(str(qr_path))

    # Breakfast operating data.
    if mods.get("breakfast"):
        b=soup.find(id="breakfast")
        data=cfg.get("breakfast",{})
        if b:
            infos=b.select(".info")
            if len(infos)>0:
                infos[0].find("span").string=data.get("hours","")
            if len(infos)>1:
                infos[1].find("span").string=data.get("last_entry","")
            if len(infos)>2:
                set_i18n(
                    infos[2].find("span"),
                    data.get("location_zh",""),
                    data.get("location_en","")
                )

    # Facilities: Phase 1 keeps the LUME focused single-facility layout.
    if mods.get("facilities") and cfg.get("facilities"):
        f=soup.find(id="facilities")
        item=cfg["facilities"][0]
        if f:
            set_i18n(f.find("h2"),item["name_zh"],item["name_en"])
            infos=f.select(".info")
            vals=[
                ("hours_zh","hours_en"),
                ("location_zh","location_en"),
                ("equipment_zh","equipment_en")
            ]
            for info,(zk,ek) in zip(infos,vals):
                set_i18n(info.find("span"),item.get(zk,""),item.get(ek,""))

    # Nearby cards are rebuilt from config.
    if mods.get("city"):
        city=soup.find(id="city")
        grid=city.select_one(".city-grid") if city else None
        if grid:
            grid.clear()
            for p in cfg.get("nearby",[]):
                card=soup.new_tag("div",attrs={"class":"city-card"})
                sm=soup.new_tag("small")
                sm.string=p.get("category","LOCAL")
                card.append(sm)

                h3=soup.new_tag("h3")
                set_i18n(h3,p["name_zh"],p["name_en"])
                card.append(h3)

                desc=soup.new_tag("p")
                set_i18n(desc,"可直接開啟地圖查看路線。","Open the map for directions.")
                card.append(desc)

                a=soup.new_tag(
                    "a",
                    attrs={
                        "class":"action-btn",
                        "data-zh":"開啟地圖",
                        "data-en":"Open map",
                        "target":"_blank",
                        "rel":"noopener",
                        "href":"https://www.google.com/maps/search/?api=1&query="+quote_plus(p["map_query"])
                    }
                )
                a.string="開啟地圖"
                card.append(a)
                grid.append(card)

    # Stay basics.
    if mods.get("stay"):
        stay=soup.find(id="stay")
        rows=stay.select(".row") if stay else []
        s=cfg.get("stay",{})
        vals=[
            ("check_in_zh","check_in_en"),
            ("check_out_zh","check_out_en"),
            ("front_desk_zh","front_desk_en")
        ]
        for row,(zk,ek) in zip(rows,vals):
            set_i18n(row.find("span"),s.get(zk,""),s.get(ek,""))

    # Front-desk extension.
    if mods.get("contact"):
        ext=str(cfg.get("contact",{}).get("front_desk_extension","9"))
        c=soup.find(id="contact")
        if c:
            lead=c.select_one(".lead")
            set_i18n(
                lead,
                f"入住期間若需要協助，請撥館內分機 {ext} 聯繫櫃檯。",
                f"If you need assistance during your stay, dial extension {ext} to reach the front desk."
            )
            btn=c.select_one("[data-copy]")
            if btn:
                btn["data-copy"]=ext
                btn["data-zh"]=f"複製櫃檯分機 {ext}"
                btn["data-en"]=f"Copy front-desk ext. {ext}"
                btn.string=f"複製櫃檯分機 {ext}"

    args.html.write_text(str(soup),encoding="utf-8")
    print("Hospitality Core v2 config applied:",args.config)

if __name__=="__main__":
    main()
