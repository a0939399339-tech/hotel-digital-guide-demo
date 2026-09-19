# LUME Theme

Reusable presentation layer for Hospitality Core v2.

## Files

- `index.html` — LUME page structure, bilingual UI and lightweight browser interactions.
- `styles.css` — complete LUME visual system, responsive rules, selected demo imagery and Wi-Fi QR layout.

## Rendering contract

The deployment pipeline copies these two files into the client staging directory, then `core-v2/apply_config.py` applies hotel-specific data from `clients/<client>/hotel-config.json`.

Theme files own presentation and structure. Client config owns property identity, operating data, module switches, Wi-Fi data and theme tokens.

The legacy `.v23/.v25` payloads under staging are no longer part of the active render path.

## Theme freeze

The approved LUME visual system is considered **LOCKED** by default.

Without an explicitly approved THEME change, do not alter:

- typography hierarchy
- layout grid
- spacing rhythm
- navigation structure
- card/button treatment
- icon style
- responsive behavior
- baseline component geometry
- brand-placement rules

Client onboarding and routine content maintenance must not trigger a visual redesign.

## Brand boundary

LUME Hospitality is the studio/creator brand.

LUME HOTEL is the fictional demo property.

Client builds use the client's own property brand.

The studio logo must not be inserted into the guest-facing UI by default. Any attribution must be explicitly approved and should remain subtle.

## Required governance

Before changing the theme, review:

- `docs/LUME_GOVERNANCE.md`
- `docs/CHANGE_REQUEST_TEMPLATE.md`
- `docs/RELEASE_CHECKLIST.md`
- `AGENTS.md`
