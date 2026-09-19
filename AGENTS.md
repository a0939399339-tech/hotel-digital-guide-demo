# AGENTS.md — LUME Repository Rules

These rules apply to humans and automated coding agents working in this repository.

## Non-negotiable rules

1. **No requirement, no change.** Do not perform unsolicited redesign or cleanup.
2. `themes/lume/` is the canonical LUME presentation source.
3. Hotel-specific operating data belongs in `clients/<client>/hotel-config.json`, not hard-coded into the theme.
4. Treat approved layout, typography, spacing, component style and responsive behavior as LOCKED.
5. A content update must not change design.
6. Do not invent hotel facts, room details, operating hours, Wi-Fi data, facilities, contact data or features.
7. LUME Hospitality (studio), LUME HOTEL (fictional demo), and client brands are separate identities.
8. Do not insert the LUME Hospitality studio logo into guest UI unless explicitly approved.
9. Portfolio product screens must be real implemented screenshots. Do not use generatively redrawn UI as implementation evidence.
10. Do not expose secrets, private data, staff networks or production credentials.
11. Build and test in staging before production.
12. Run the applicable checks in `docs/RELEASE_CHECKLIST.md` before release.
13. Classify non-trivial changes using `docs/CHANGE_REQUEST_TEMPLATE.md`.
14. If scope is ambiguous, preserve the approved baseline and request clarification.

Full policy: `docs/LUME_GOVERNANCE.md`
