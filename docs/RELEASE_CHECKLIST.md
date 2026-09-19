# LUME Release Checklist v1.0

> Required release gate for LUME demo and client deployments.

Mark each required item PASS before production release.

## A. Release identity

- [ ] Release version identified
- [ ] Candidate commit SHA recorded
- [ ] Correct client/property config selected
- [ ] Correct theme version selected
- [ ] Staging build created from source
- [ ] No direct production-only edits

## B. Brand integrity

- [ ] Property name is correct
- [ ] Property logo is correct
- [ ] Studio logo is not inserted into guest UI unless explicitly approved
- [ ] Approved typography hierarchy unchanged
- [ ] Approved colors unchanged except approved client tokens
- [ ] Navigation/component visual system has no unexplained drift
- [ ] Mobile and desktop layout match the approved baseline

## C. Content accuracy

- [ ] Check-in time verified
- [ ] Check-out time verified
- [ ] Breakfast hours verified
- [ ] Breakfast location verified
- [ ] Facility hours/locations verified
- [ ] Contact information verified
- [ ] Front-desk extension/phone verified
- [ ] Smoking/house rules verified
- [ ] Room information verified
- [ ] Nearby recommendations verified
- [ ] No placeholder or invented client facts remain

## D. Wi-Fi / QR

- [ ] Correct guest SSID
- [ ] Correct guest password
- [ ] Correct security mode
- [ ] QR generated from config, not typed manually
- [ ] QR scan tested on a physical/mobile device where practical
- [ ] Same-phone fallback instructions visible
- [ ] Copy SSID control works
- [ ] Copy password control works
- [ ] No staff/POS/CCTV/back-office credentials exposed

## E. Navigation and interaction

- [ ] Home/landing works
- [ ] Room module works
- [ ] Breakfast module works
- [ ] Facilities module works
- [ ] Nearby/city module works
- [ ] Wi-Fi module works
- [ ] Stay info works
- [ ] Contact module works
- [ ] Back links work
- [ ] Language switch works
- [ ] External map links open correctly
- [ ] Disabled modules do not leave orphan links

## F. Responsive QA

Test at minimum:
- [ ] narrow mobile
- [ ] standard mobile
- [ ] tablet
- [ ] desktop

For each:
- [ ] no horizontal overflow
- [ ] no clipped text
- [ ] touch targets remain usable
- [ ] images preserve intended crop
- [ ] headings do not collide
- [ ] fixed/floating controls do not cover content

## G. Asset QA

- [ ] No broken images
- [ ] No missing fonts/icons
- [ ] No legacy/demo asset accidentally used in a client build
- [ ] Image files are reasonably optimized
- [ ] Alt text present where appropriate
- [ ] Asset filenames follow semantic naming rules

## H. Portfolio truth check

Only required when preparing portfolio/case-study material.

- [ ] Product UI shown is a real implemented screenshot
- [ ] Mockup framing does not alter the product screenshot
- [ ] No nonexistent features are shown as implemented
- [ ] Property identity inside screenshot is authentic to that build
- [ ] Studio branding remains outside the product UI unless implemented
- [ ] Concept visuals are labeled Concept / Visual Exploration

## I. Security / privacy

- [ ] No API keys or secrets
- [ ] No guest personal data
- [ ] No internal hotel records
- [ ] No private staff network data
- [ ] Public demo uses fake/nonfunctional credentials
- [ ] Public repo contains only sanitized material

## J. Visual regression

Compare against approved baseline:

- [ ] home
- [ ] room
- [ ] breakfast
- [ ] facilities
- [ ] nearby/city
- [ ] Wi-Fi
- [ ] stay info
- [ ] contact

Any unexplained difference must be resolved or explicitly approved.

## K. Final release decision

- [ ] Core/automated QA passes
- [ ] Static QA passes
- [ ] Required manual checks pass
- [ ] Known exceptions documented
- [ ] Rollback commit identified
- [ ] RELEASE APPROVED

If any required item fails, do not mark the release approved.
