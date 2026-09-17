# Security Policy

This repository is a public, sanitized demonstration project. It must not contain production secrets, private customer information, guest data, internal hotel operating records, or credentials.

## What must never be committed

- API keys, OAuth client secrets, access tokens, private keys, or service-account files
- `.env` files containing secrets
- Real guest names, reservation details, contact information, IDs, payment data, or other personal data
- Real hotel Wi-Fi passwords unless they are intentionally public demo values
- Internal SOPs, staff-only documents, non-public business data, or customer/client source materials without authorization
- Credentials for GitHub, Google, Cloudflare, Vercel, PMS, booking engines, or other services

## Reporting a security issue

Do not post secrets, credentials, exploit details, or sensitive screenshots in a public GitHub issue.

If GitHub private vulnerability reporting / Security Advisories are available for this repository, use that channel. Otherwise, contact the repository owner through GitHub and request a private channel before sharing sensitive details.

If a secret is ever committed, deleting the file is not sufficient. The affected credential should be revoked or rotated immediately, and the Git history should be cleaned if necessary.

## Public demo boundary

Only sanitized, non-sensitive, client-safe static demo material belongs in this repository. The Hospitality Core, Control Center, generator, Auto QA tooling, customer intake source data, and private client projects should remain in private repositories or local/private storage.
