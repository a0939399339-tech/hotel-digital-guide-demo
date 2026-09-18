# Hospitality Core v2

Config-driven migration layer for the hotel Digital Guest Guide.

## Current milestone

LUME is the first Core v2 client. The existing LUME theme is rendered first, then `apply_config.py` applies client data and module switches before deployment.

This means hotel-specific operating data is no longer meant to be hand-edited inside the page.

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

## Module rules

- `false` removes both the homepage entry and the section.
- Facilities with zero configured items are treated as disabled.
- Wi-Fi QR is generated from the config; the QR payload is not typed by hand.

## Security

Only guest-network credentials belong in a public guest guide. Never expose staff, POS, CCTV, office, or infrastructure network credentials.

## Direction

This is Phase 1 of the migration. The next Core milestone is to extract the full LUME HTML/CSS into a reusable theme renderer so future hotels can be generated without the legacy LUME build steps.
