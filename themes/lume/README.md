# LUME Theme

Reusable presentation layer for Hospitality Core v2.

## Files

- `index.html` — LUME page structure, bilingual UI and lightweight browser interactions.
- `styles.css` — complete LUME visual system, responsive rules, selected demo imagery and Wi-Fi QR layout.

## Rendering contract

The deployment pipeline copies these two files into the client staging directory, then `core-v2/apply_config.py` applies hotel-specific data from `clients/<client>/hotel-config.json`.

Theme files own presentation and structure. Client config owns property identity, operating data, module switches, Wi-Fi data and theme tokens.

The legacy `.v23/.v25` payloads under staging are no longer part of the active render path.
