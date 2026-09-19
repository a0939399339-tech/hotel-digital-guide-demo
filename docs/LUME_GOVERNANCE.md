# LUME Product Governance v1.0

> Status: ACTIVE  
> Scope: LUME Hospitality Digital Guest Guide product, demo, client builds, portfolio presentation, and release process.

## 1. Governing principle

**No requirement, no change.**

A content update is not permission to redesign the product.  
A new client is not permission to reinvent the theme.  
The same approved theme plus the same config must produce the same visual and functional result.

The product target is:

```text
Stable Theme + Client Config + QA + Controlled Release
```

not:

```text
New client = new design experiment
```

---

## 2. Three-layer change model

Every requested change must be classified before implementation.

| Level | Meaning | Examples | Default action |
|---|---|---|---|
| LOCKED | Product / brand system | layout, typography system, spacing, component style, responsive behavior, approved logo treatment | Do not change without explicit design approval |
| CONFIGURABLE | Client/property content | property name, client logo, brand token, breakfast, Wi-Fi, facilities, images, contact details, nearby places | May change through client config/content workflow |
| CUSTOM | New scope | new module, new interaction, API, PMS, booking, membership, payment, major UI redesign | Separate change request, estimate and approval required |

If a request is ambiguous, treat it as **LOCKED** until clarified.

---

## 3. Single Source of Truth

### Theme
`themes/lume/` is the canonical LUME presentation layer.

It owns:
- HTML structure
- typography hierarchy
- spacing system
- component design
- responsive behavior
- supported browser interactions

### Client data
`clients/<client>/hotel-config.json` owns property-specific operating content and configuration.

It may contain:
- property identity
- approved brand tokens
- module switches
- Wi-Fi guest-network data
- breakfast data
- facilities
- nearby places
- stay information
- contact information

### Build output
`staging/` is assembled output, not the design source.

Do not fix a canonical problem by hand-editing generated staging output.

---

## 4. Brand hierarchy

The following identities must never be mixed.

### LUME Hospitality
The studio / creator brand.

Use for:
- sales material
- proposal material
- portfolio framing
- case-study framing
- optional product attribution

### LUME HOTEL
The fictional demo property.

Use only inside the demo product where configured.

### Client property brand
The paying client's hotel identity.

It is the primary guest-facing brand in a client build.

### Rule
A client or demo interface must not automatically inherit the LUME Hospitality studio logo.

Optional attribution may appear only as a subtle footer such as:

`Powered by LUME Hospitality`

and only when the commercial plan permits it.

White-label delivery may remove the attribution entirely.

---

## 5. Brand Freeze

Once an interface baseline has been approved, the following are LOCKED unless a design change is explicitly approved:

- logo treatment and placement
- typography system
- headline/body hierarchy
- spacing rhythm
- navigation structure
- button styling
- card styling
- icon style
- border radius system
- responsive breakpoints/behavior
- layout grid
- default motion/interaction style
- portfolio master-template geometry

An operating-data update must not alter any of these.

---

## 6. Content Change != Design Change

Examples:

- Change breakfast from 06:30 to 07:00 -> CONTENT
- Change Wi-Fi password -> CONTENT
- Replace an approved hotel image -> CONTENT
- Add a new restaurant facility type already supported -> CONTENT/CONFIG
- Move navigation, change fonts, redesign cards -> THEME
- Add PMS / booking / payment / membership integration -> CUSTOM
- Add a new guest-facing module not supported by the theme -> CUSTOM

A CONTENT request must not be used as justification for unrelated design cleanup.

---

## 7. No Invented Client Content

Never invent or infer client operating facts.

Do not fabricate:
- room types
- room size
- bed type
- rates
- breakfast hours
- facilities
- Wi-Fi credentials
- phone numbers
- addresses
- check-in/out rules
- smoking policy
- nearby attractions
- booking functions
- service availability

If required information is missing, mark it as pending confirmation or keep the module disabled.

---

## 8. Demo Integrity

The public demo must remain clearly fictional and sanitized.

Current demo identity:
- Property: `LUME HOTEL`
- Demo data: non-production
- Guest Wi-Fi: demo credentials only
- Nearby information: feature demonstration only

Do not replace demo content with a real client's private or production information.

Do not present Yidear Hotel production information as part of the public LUME HOTEL demo.

---

## 9. Portfolio Truth Rule

Portfolio work must represent real implemented output.

Allowed:
- real product screenshots
- cropping
- device mockup framing
- background/layout presentation
- captions
- annotations
- case-study text
- approved studio branding outside the product screenshot

Not allowed:
- generatively redrawing the product UI and presenting it as implemented work
- adding nonexistent functionality to a screenshot
- changing property names inside a screenshot
- replacing real interface content with invented content
- inserting the LUME Hospitality logo inside the guest UI when it was not implemented
- presenting concept art as a production screenshot

Concept images must be explicitly labeled **Concept** or **Visual Exploration**.

---

## 10. AI Usage Boundary

AI may assist with:
- code drafting
- QA
- text drafting
- translation drafts
- visual concepts
- decorative assets
- image cleanup
- exploratory mockups

AI must not autonomously:
- redesign an approved theme
- alter approved brand identity
- invent property facts
- create fictitious implemented features
- replace real UI screenshots in the portfolio
- silently change scope
- publish production changes without required checks

Generated visual exploration is not implementation evidence.

---

## 11. Asset Governance

Approved assets must have stable filenames and predictable locations.

Avoid filenames such as:
- `final-final2.png`
- `new-logo-latest.png`
- `use-this-one-v3.png`

Use semantic names, for example:

```text
assets/
  brand/
    property-logo.svg
  rooms/
    deluxe-room-01.webp
  dining/
    breakfast-01.webp
  guide/
    wifi-qr.svg
```

Demo assets and production client assets must not be mixed.

---

## 12. Environment Separation

Preferred flow:

```text
development -> staging -> production
```

Rules:
- do not experiment directly in production
- staging must reflect the exact candidate release
- a production release must be reproducible from source
- generated staging output must not become a hidden second source of truth

---

## 13. Approved Baseline

After client/design approval, create an approved baseline.

The baseline should identify:
- version
- commit SHA
- approved property config
- approved theme version
- release date
- key reference screenshots where practical

Any later visual or functional difference must have an explicit change reason.

---

## 14. Versioning

Use semantic version intent:

- PATCH: content correction, safe bug fix, no intentional visual redesign
- MINOR: backward-compatible module/function enhancement
- MAJOR: intentional product/design architecture change

Example:

`v1.0.0 -> v1.0.1` for a safe fix  
`v1.0.0 -> v1.1.0` for a new supported module  
`v1.x -> v2.0.0` for an approved major redesign

---

## 15. Change Request Classification

Every non-trivial request must be labeled:

- CONTENT
- THEME
- FEATURE
- INTEGRATION

Use `docs/CHANGE_REQUEST_TEMPLATE.md`.

CONTENT may enter routine maintenance.

THEME / FEATURE / INTEGRATION require explicit scope confirmation before implementation.

---

## 16. Visual Regression Rule

Key product surfaces should have reference screenshots or equivalent visual checks.

At minimum:
- landing/home
- room
- breakfast
- facilities
- nearby/city
- Wi-Fi
- stay info
- contact

A release with unexplained visual drift must fail review.

---

## 17. Security and Privacy Boundary

Never commit:
- production secrets
- private API keys
- staff network credentials
- POS/CCTV/back-office Wi-Fi
- guest personal data
- internal hotel records
- private contracts or credentials

Only guest-facing data intentionally approved for publication belongs in a guest guide.

Public demo credentials must be fake/nonfunctional.

---

## 18. Release Gate

No production deployment may be considered approved until the release checklist passes.

See:

`docs/RELEASE_CHECKLIST.md`

A failed required check blocks release.

---

## 19. Rollback

Every production release must be traceable to a commit.

If a release introduces:
- incorrect hotel data
- broken navigation
- brand drift
- layout regression
- security/privacy issue
- incorrect QR/Wi-Fi behavior

prefer rollback to the last known-good release before attempting an uncontrolled hotfix.

---

## 20. Product rule of last resort

When uncertain:

> Preserve the approved product and ask for scope clarification.

Stability and trust take priority over unsolicited redesign.
