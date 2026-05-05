---
name: tax-filing-individual
description: |
  Walks an Estonian resident or citizen through filing the annual personal
  income tax declaration (tuludeklaratsioon) via e-MTA. Use when the user
  mentions: "tax return", "tuludeklaratsioon", "annual taxes", "MTA", "EMTA",
  "tax filing for individuals", "how much do I owe in taxes", or "when am I
  getting my tax refund". Always re-fetches current tax-year rates and
  deadlines from emta.ee — never quotes cached numbers.
license: MIT
allowed-tools: WebFetch(domain:emta.ee) WebFetch(domain:www.emta.ee) WebFetch(domain:maasikas.emta.ee)
metadata:
  audience: "citizen,resident"
  life_event: "meta"
  service_domain: "tax"
  cadence: "annual"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.emta.ee/eraklient/tulu-deklareerimine|https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Tax filing for individuals

## Disclaimer

This is AI-generated procedural guidance, not tax advice. Always verify against the authoritative emta.ee pages linked below. This repository is not affiliated with the Republic of Estonia or Maksu- ja Tolliamet.

## Freshness obligation

**Before quoting any tax rate, threshold, deadline, or fee, fetch the current pages at:**

- `https://www.emta.ee/eraklient/tulu-deklareerimine`
- `https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad`

**Do not quote any number or date from this skill body.** Numbers below (if any) are illustrative only — always replace them with what the live pages currently say.

## Step 1 — Disambiguate the user's situation

Ask the minimum necessary, in this order:

1. **Tax year.** "Which tax year are you filing for?" (Default: the previous calendar year. The Estonian tax year runs January 1 – December 31; declarations open in February.)
2. **Tax residency.** "Are you a tax resident of Estonia for that year?" (Tax residency is distinct from residence permit or citizenship — it usually means the person spent ≥183 days in Estonia in a 12-month period or has a permanent home there. If the user is unsure, point them at the residency-test section on emta.ee.)
3. **Income types.** "What kinds of income did you receive that year?" (Employment salary, business income/FIE, dividends, rental, capital gains, foreign income, etc.) Different income types route to different sections of the e-MTA pre-filled return.

## Step 2 — Walk through the e-MTA flow

1. Fetch the live emta.ee page above and identify the current section titled (in Estonian) "Kuidas deklaratsiooni esitada" or (in English) "How to file the declaration." Summarise the steps from that page in 6–10 bullets, in the user's chosen language.
2. Mention the current filing window (open and close dates) — fetched from the live page, not memorised.
3. Mention the current tax-rate table from the `maksumaarad` page (basic exemption, income tax rate, etc.) — again, fetched, not memorised.

Frame each step in terms the user can act on. Where possible, link to the specific gov page that explains the step in detail.

## Step 3 — Auth seam (where the skill ends)

End the procedural guidance with:

> Now log in to **e-MTA** at `https://maasikas.emta.ee/oma_ee/login` (or via `https://www.emta.ee/`) using your Smart-ID, Mobile-ID, or ID-card. Most income data will already be pre-filled. Review each section, add anything missing (foreign income, rental income, FIE income), confirm your bank account for any refund, and submit.

After this point, do not narrate the in-portal experience — the user is authenticated and the page itself guides them.

## Step 4 — Common pitfalls to flag

After the procedural walkthrough, surface these (verify each against the live page):

- Foreign income from EU and non-EU sources is treated differently — a treaty may apply.
- Cryptocurrency gains are declarable; the rules are on a separate emta.ee page (link it).
- If the user owes tax (rather than getting a refund), the payment deadline differs from the filing deadline.
- The basic exemption phases out above a certain income threshold — the live page has the current threshold.

## Sources

See `references/sources.md`.
