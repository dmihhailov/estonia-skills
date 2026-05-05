---
name: residence-registration
description: |
  Walks a newcomer to Estonia (EU/EEA citizen, third-country national, or
  returning resident) through registering their place of residence in the
  rahvastikuregister (population register). Use when the user mentions:
  "register address Estonia", "rahvastikuregister", "kohalik omavalitsus",
  "moving to Estonia", "place of residence", "elukoharegistreerimine".
  Distinguishes between place-of-residence registration (for everyone) and
  residence permits (for non-EU nationals). Always re-fetches current procedure
  from eesti.ee and politsei.ee.
license: MIT
allowed-tools: WebFetch(domain:eesti.ee) WebFetch(domain:www.eesti.ee) WebFetch(domain:politsei.ee) WebFetch(domain:www.politsei.ee)
metadata:
  audience: "expat-newcomer,resident"
  life_event: "arriving"
  service_domain: "identity"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.eesti.ee/en|https://www.politsei.ee/en/instructions/applying-for-a-residence-permit"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Residence registration

## Disclaimer

This is AI-generated procedural guidance, not legal advice. Always verify against the authoritative eesti.ee and politsei.ee pages linked below. This repository is not affiliated with the Republic of Estonia, Politsei- ja Piirivalveamet, or any local government.

## Freshness obligation

**Before quoting any deadline, fee, document list, or processing time, fetch the current pages at:**

- `https://www.eesti.ee/en`
- `https://www.politsei.ee/en/instructions/applying-for-a-residence-permit`

The eesti.ee state portal is a single-page application whose specific paths cannot be verified server-side; from the homepage, navigate to "Family and relationships" / "Registering place of residence" (Estonian: `elukoha registreerimine`) and use the live page content. If the politsei.ee URL above returns non-200 because the gov sites have restructured, fetch `https://www.politsei.ee/en` and find the current path under "Migration and citizenship" / "Residence permits".

## Step 1 — Two procedures, often confused

Clarify with the user which they need:

1. **Place-of-residence registration** (`elukoharegistreerimine`) — recording the user's address in the population register. Required for everyone living in Estonia for >3 months, regardless of citizenship. Typically free; verify the current fee on the live eesti.ee page. Self-service.
2. **Residence permit** — only for non-EU/non-EEA nationals who need legal authorisation to reside. Issued by PPA. Has fees, document requirements, and processing time. Different procedure entirely.

EU/EEA citizens need #1 only (plus a "right of residence" registration at PPA after 3 months — fetch the current details from politsei.ee).

Non-EU/non-EEA citizens need both #2 (first) and then #1 (after arrival).

## Step 2 — Place-of-residence registration walkthrough

1. Fetch the live eesti.ee page and summarise the current registration procedure in 6–10 numbered steps, in the user's chosen language. Cover: who must register, document requirements, and the two channels (online vs. in-person at the local council).
2. Note that only the property owner (or someone with the owner's written consent) can register an address there — many newcomers forget this and assume a tenancy agreement is enough.

## Step 3 — Residence permit walkthrough (only if needed)

If the user is non-EU/non-EEA and needs a permit:

1. Fetch the live politsei.ee page and identify the relevant permit type (work, study, family reunification, long-term resident, etc.).
2. Summarise the application steps, document list, and current state fee in 6–10 bullets.
3. Note that most third-country applications must be filed at an Estonian embassy abroad **before** travel, not after arrival.

## Step 4 — Auth seam

For place-of-residence registration:

> Submit your registration online at the eesti.ee residence-registration page using your Smart-ID, Mobile-ID, or ID-card; or visit your local government office (`kohalik omavalitsus`) in person with your passport / ID and proof of right to use the address.

For residence permits:

> Apply at the relevant Estonian embassy abroad (or, if eligible, in person at a PPA service point in Estonia). The application flow itself is on the politsei.ee page; this skill ends at the start of that flow.

## Sources

See `references/sources.md`.
