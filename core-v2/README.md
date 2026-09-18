# Hospitality Core v2

Config-driven rendering layer for the hotel Digital Guest Guide.

## Current milestone

LUME is the first Core v2 client, and its presentation layer now lives in `themes/lume/`.

The active render flow is:

1. Copy `themes/lume/index.html` and `themes/lume/styles.css` into the client staging directory.
2. Apply `clients/lume/hotel-config.json` with `apply_config.py`.
3. Generate the guest Wi-Fi QR asset from config.
4. Run Core v2 QA and static QA.
5. Deploy the assembled staging directory.

Hotel-specific operating data is not hand-edited inside the theme.

## Config controls

- Property name and hero label
- Theme accent/background tokens
- Module visibility
- Wi-Fi SSID/password/security and QR generation
- Breakfast operating data
- Facility data
- Nearby map destinations
- Stay basics
- Front-desk extension

## Theme boundary

- `themes/lume/index.html`: page structure, bilingual labels and lightweight browser interactions.
- `themes/lume/styles.css`: complete visual system and responsive behavior.
- `clients/lume/hotel-config.json`: property-specific identity and operating data.
- `staging/river-hotel/assets/`: deploy-time image assets and generated Wi-Fi QR.

The legacy `.v23/.v25` payloads remain only as historical artifacts and are no longer used by the active render path.

## Module rules

- `false` removes both the homepage entry and the section.
- Facilities with zero configured items are treated as disabled.
- Wi-Fi QR is generated from config; the QR payload is not typed by hand.

## Security

Only guest-network credentials belong in a public guest guide. Never expose staff, POS, CCTV, office, or infrastructure network credentials.
