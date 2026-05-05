---
name: ou-open-e-resident
description: |
  Walks an e-Resident through opening a private limited company (osaühing, OÜ)
  remotely using the e-Residency digital ID. Use when the user mentions:
  "open OÜ", "open Estonian company", "register OÜ", "e-Residency company",
  "ariregister", "Company Registration Portal", "start a business in Estonia
  as a non-resident". Always re-fetches the current procedure from
  e-resident.gov.ee — never quotes cached fees or share-capital minimums.
license: MIT
allowed-tools: WebFetch(domain:e-resident.gov.ee) WebFetch(domain:www.e-resident.gov.ee) WebFetch(domain:marketplace.e-resident.gov.ee) WebFetch(domain:ariregister.rik.ee)
metadata:
  audience: "e-resident,non-resident-founder"
  life_event: "starting-business"
  service_domain: "business"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "e-residency-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.e-resident.gov.ee/start-a-company/|https://ariregister.rik.ee/eng/application/start"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Open an OÜ as an e-Resident

## Disclaimer

This is AI-generated procedural guidance, not legal, tax, or accounting advice. Always verify against the authoritative pages linked below. This repository is not affiliated with the Republic of Estonia, the e-Residency programme, or Centre of Registers and Information Systems (RIK).

## Freshness obligation

**Before quoting any state fee, share capital minimum, processing time, or step, fetch the current pages at:**

- `https://www.e-resident.gov.ee/start-a-company/`
- `https://ariregister.rik.ee/eng/application/start`

**Numbers and procedural steps in this skill body are illustrative — always replace them with what the live pages currently say.**

## Step 1 — Confirm prerequisites

Ask the user, in order:

1. **Do you already hold an active e-Residency digital ID card?** If no, route them to the e-Residency application flow first — this skill assumes the card is in hand.
2. **Do you have a card reader and the latest DigiDoc4 client installed?** Smart-ID and Mobile-ID are not options here; OÜ registration requires the e-Residency ID-card and a hardware reader.
3. **Have you chosen a contact person and legal address in Estonia?** Most e-Residents use a third-party service provider for both. Mention that this is a service marketplace topic, not a state matter — the user picks a provider from `https://marketplace.e-resident.gov.ee/`.
4. **What's the company's intended name?** Mention that name availability can be checked at `https://ariregister.rik.ee/eng/name_query`.

## Step 2 — Walk through the Company Registration Portal procedure

1. Fetch `https://www.e-resident.gov.ee/start-a-company/` and summarise the current procedure in 6–10 numbered steps, in the user's chosen language. Pay particular attention to the contributed share capital question (some founders defer payment, others pay up front), and the differences for sole vs. multiple founders.
2. Fetch the relevant section on `https://ariregister.rik.ee/eng/application/start` and confirm the in-portal flow matches the description above.
3. State the current state fee (from the live page, not memorised).
4. State current processing time (from the live page).

## Step 3 — Auth seam

End procedural guidance with:

> Now sign in to the **e-Business Register (e-Äriregister)** at `https://ariregister.rik.ee/eng/application/start` with your e-Residency ID-card via the DigiDoc4 client. Fill in the application, sign, and pay the state fee. RIK will email you when the company is approved (typically within a business day).

## Step 4 — After registration

Surface these post-registration tasks (verify against the live page):

- Open a business bank account (Wise, LHV, and various fintechs are common; the e-Residency marketplace lists options).
- Register for VAT if anticipated turnover exceeds the current threshold (fetch the threshold from emta.ee).
- File the annual report after the first financial year ends.
- Set up accounting; many founders use service providers from the marketplace.

## Sources

See `references/sources.md`.
