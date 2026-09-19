# Hotel Digital Guest Guide — DEMO

Reusable, sanitized hotel digital guest guide demo derived from the production architecture.

## Live staging

https://a0939399339-tech.github.io/hotel-digital-guide-demo/

## Active architecture

LUME is the first Hospitality Core v2 theme.

```text
themes/lume/
├─ index.html      # canonical LUME structure + bilingual browser interactions
├─ styles.css      # canonical LUME visual system + responsive rules
└─ README.md       # theme contract

clients/lume/
└─ hotel-config.json

core-v2/
├─ apply_config.py
└─ qa.py

staging/river-hotel/
└─ assets/         # deploy-time demo imagery + generated Wi-Fi QR

docs/
├─ LUME_GOVERNANCE.md
├─ RELEASE_CHECKLIST.md
└─ CHANGE_REQUEST_TEMPLATE.md

AGENTS.md           # concise guardrails for human / AI implementation work
```

The active build path is:

1. Copy `themes/lume/index.html` and `themes/lume/styles.css` into staging.
2. Apply `clients/lume/hotel-config.json` through Hospitality Core v2.
3. Generate deploy-time Wi-Fi QR content.
4. Run Core v2 QA and static QA.
5. Deploy the assembled staging directory to GitHub Pages.

**Do not hand-edit hotel-specific operating data inside `themes/lume/`.** Theme files own presentation and structure; client config owns property identity, operating data, module switches, Wi-Fi data, and configurable theme tokens.

The root-level `index.html`, `styles.css`, and `app.js` belong to the older generic demo and are not the canonical LUME render source. Legacy `staging/river-hotel/.v23` and `.v25` payloads are historical artifacts only.

## Product governance

LUME follows a strict product-governance model:

- **LOCKED** — approved theme/brand system. No unsolicited redesign.
- **CONFIGURABLE** — client/property content supplied through config.
- **CUSTOM** — new modules, major redesigns and integrations require explicit scope approval.

The governing rule is:

> **No requirement, no change.**

A content update is not permission to redesign the product.

Required references:

- [LUME Product Governance](docs/LUME_GOVERNANCE.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)
- [Change Request Template](docs/CHANGE_REQUEST_TEMPLATE.md)
- [Repository Agent Rules](AGENTS.md)

## Purpose
- Portfolio / product demonstration
- Reusable starter for future hotel projects
- No Yidear Hotel branding, official logo, real contact details, campaign assets, or operational data

## LUME demo features
- Traditional Chinese / English interface
- Mobile-first guest guide
- Room, breakfast, facilities, neighborhood, Wi-Fi, stay info, and front-desk modules
- Config-driven property data
- Generated guest Wi-Fi QR asset
- Generic sample data only

## Portfolio integrity

Product screenshots shown as implemented work must come from real implemented UI. Generated visual concepts may be used only when clearly labeled as concepts and must not be presented as production screenshots.

## Public repository boundary

This repository is intentionally public and should contain only sanitized demo material. Do not commit production credentials, private client source files, guest data, internal hotel records, or other non-public operational information.

The Hospitality Core, Control Center, Client Generator, Auto QA tooling, customer intake source data, and private client projects are maintained separately and should remain private.

## License

This repository is **not open source**. Public visibility is for demonstration and evaluation only. See [`LICENSE`](LICENSE) for the copyright and usage terms.

## Security

See [`SECURITY.md`](SECURITY.md). Never report credentials, secrets, exploit details, or sensitive screenshots in a public issue.

> This repository is a personal reusable DEMO template. The production Yidear Hotel guide is maintained separately under the Yidear-Hotel organization.
