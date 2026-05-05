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
allowed-tools: >-
  WebFetch(domain:eesti.ee) WebFetch(domain:www.eesti.ee)
  WebFetch(domain:riigiteataja.ee) WebFetch(domain:www.riigiteataja.ee)
  WebFetch(domain:emta.ee) WebFetch(domain:www.emta.ee) WebFetch(domain:maasikas.emta.ee)
  WebFetch(domain:politsei.ee) WebFetch(domain:www.politsei.ee) WebFetch(domain:broneering.politsei.ee)
  WebFetch(domain:ariregister.rik.ee) WebFetch(domain:ettevotjaportaal.rik.ee) WebFetch(domain:avaandmed.ariregister.rik.ee)
  WebFetch(domain:e-resident.gov.ee) WebFetch(domain:www.e-resident.gov.ee) WebFetch(domain:marketplace.e-resident.gov.ee)
  WebFetch(domain:sotsiaalkindlustusamet.ee) WebFetch(domain:tootukassa.ee) WebFetch(domain:tervisekassa.ee) WebFetch(domain:terviseamet.ee)
  WebFetch(domain:transpordiamet.ee) WebFetch(domain:www.transpordiamet.ee) WebFetch(domain:maanteamet.ee) WebFetch(domain:www.maanteamet.ee) WebFetch(domain:lkf.ee) WebFetch(domain:www.lkf.ee) WebFetch(domain:eteenindus.mnt.ee)
  WebFetch(domain:tallinn.ee) WebFetch(domain:www.tallinn.ee) WebFetch(domain:tartu.ee) WebFetch(domain:www.tartu.ee) WebFetch(domain:parnu.ee) WebFetch(domain:www.parnu.ee) WebFetch(domain:narva.ee) WebFetch(domain:www.narva.ee)
  WebFetch(domain:id.ee) WebFetch(domain:www.id.ee) WebFetch(domain:smart-id.com) WebFetch(domain:www.smart-id.com) WebFetch(domain:sk.ee) WebFetch(domain:www.sk.ee)
  WebFetch(domain:andmed.stat.ee) WebFetch(domain:avaandmed.eesti.ee) WebFetch(domain:stat.ee) WebFetch(domain:www.stat.ee)
  WebFetch(domain:maaamet.ee) WebFetch(domain:www.maaamet.ee) WebFetch(domain:geoportaal.maaamet.ee)
  WebFetch(domain:teatmik.ee) WebFetch(domain:www.teatmik.ee) WebFetch(domain:inforegister.ee) WebFetch(domain:www.inforegister.ee) WebFetch(domain:e-krediidiinfo.ee) WebFetch(domain:www.e-krediidiinfo.ee) WebFetch(domain:krediidiinfo.ee) WebFetch(domain:creditinfo.ee)
  WebSearch
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

This is AI-generated procedural guidance, not legal, tax, or accounting advice. The drafts and scenarios this skill produces (articles of association, share-capital options, marketplace recommendations) are starting points; your authoritative state of affairs is what RIK confirms after registration. For complex setups (multiple jurisdictions, share structures with vesting, family-owned arrangements), consult a lawyer. This repository is not affiliated with the Republic of Estonia, the e-Residency programme, or Centre of Registers and Information Systems (RIK).

## Freshness obligation

**Before quoting any state fee, share-capital rule, processing time, or step, fetch the current pages at:**

- `https://www.e-resident.gov.ee/start-a-company/`
- `https://ariregister.rik.ee/eng/application/start`

**Do not use any number from this skill body.** Numbers below are illustrative — always replace them with what the live pages currently say.

## Step 1 — Confirm prerequisites

Ask the user, in order:

1. **Do you already hold an active e-Residency digital ID card?** If no, route them to the e-Residency application flow first — this skill assumes the card is in hand.
2. **Do you have a card reader and the latest DigiDoc4 client installed?** Smart-ID and Mobile-ID are not options here; OÜ registration requires the e-Residency ID-card and a hardware reader.
3. **Sole founder or multiple founders?** Affects the articles of association and the share-capital question (Step 3).
4. **Have you decided on a contact person and legal address in Estonia?** Most non-residents use a service provider for both. If they haven't, Step 4 helps them pick one.

## Step 2 — Live company name search

Once the user has a name in mind:

1. **Prefer WebFetch over WebSearch.** The e-Business Register exposes its name search via a public URL; query it directly rather than searching the wider web for the company name. Try `https://ariregister.rik.ee/eng/name_query?name=<URL-encoded-name>` first. If that doesn't return useful results, fetch `https://ariregister.rik.ee/eng/name_query` (the form page) and inspect the form to determine the correct GET parameters, then re-fetch with those.
2. Parse the result:
   - **Available** — confirm and move on.
   - **Conflict** (identical or confusingly-similar existing entity) — list the conflicting registrations and suggest variations: add `Eesti`, append `OÜ`/`Holdings`/`Group`, swap to a related word, etc. Re-check the variations until one is available.
   - **Restricted** (e.g., uses a reserved word like *bank*, *insurance*, *university*) — explain that names containing those words require additional approvals; suggest alternatives.
3. **Then a quick trademark check.** WebSearch the name to catch obvious red flags before they hit the registry: existing trademarks, too generic to be enforceable, or a name that's actively confusing with a well-known competitor in the same line of business. This is a *secondary* check after the registry; don't skip the registry just because the WebSearch came up empty.

The output of this step is a confirmed available name the user has greenlit.

## Step 3 — Choose share-capital approach

The Estonian OÜ has options for share capital. As of 2023 there's no formal minimum capital requirement at registration, but the chosen capital figure has legal-liability implications.

1. **Fetch the current rule** from `https://www.e-resident.gov.ee/start-a-company/` (look for "share capital" or "osakapital"). Confirm what's required *now*.
2. **Walk the user through the choice:**
   - **Pay up front** — full declared capital deposited at registration. Simplest path; no ongoing personal-liability exposure for unpaid capital. Recommended if the founder has the cash and wants minimum complexity.
   - **Defer payment** — declare the capital but pay later. No cash needed at registration, but founders are personally liable for unpaid capital if the company is dissolved or goes insolvent before the capital is paid in. Only sensible if the founder genuinely lacks the cash and accepts that liability.
3. **Ask the user about their situation** (sole founder, multi-founder, expected first-year revenue) and recommend an approach. Show the trade-off explicitly: "If you defer €2,500 and the OÜ becomes insolvent in year one, you personally owe €2,500 to creditors." Don't gloss this over.
4. **Compute the founder split** for multi-founder cases: who owns what percentage, what each contributes, voting rights default to ownership share.

The output is a share-capital plan: amount, payment timing, founder split.

## Step 4 — Pick service providers from the marketplace

Most non-residents need at least a contact person and a legal address. Many also want accounting and a banking-introduction service.

1. **WebFetch** `https://marketplace.e-resident.gov.ee/`. Parse the listing.
2. **Filter by the user's needs:**
   - Just contact person + legal address? (Cheapest tier.)
   - Full bookkeeping + tax filings? (Mid-tier.)
   - Banking intro, payment processing, ongoing legal support? (Top tier.)
3. **Surface 2–3 specific providers** that match the user's needs and budget signal. For each, list: name, listed services, price tier, language, link to the marketplace listing.
4. **Caveat the recommendation:** you're surfacing options, not endorsing any single provider. The user does the final pick after due diligence (read reviews, check provider's response time, etc.).

## Step 5 — Generate Articles of Association draft

Based on the answers from Steps 1–3, generate a draft Articles of Association in Estonian (canonical) plus an English working translation.

Use a standard OÜ template with placeholders filled in:
- Company name (verified from Step 2)
- Registered address (placeholder — to be filled by service provider from Step 4)
- Share capital amount and structure (from Step 3)
- Founder list with contributions (from Step 3)
- Board structure (single director — typical for sole-founder; or multi-director list)
- Financial year (default: calendar year, January 1 – December 31, unless the user has a reason to differ)
- Standard provisions: representation rights, profit distribution, dispute resolution

Output the draft inline as Markdown code blocks (Estonian first, English below). Note that the user will paste the Estonian version into the Company Registration Portal during application. The English version is a working aid for the founder; the Estonian text is legally canonical.

**Caveat the draft explicitly:** "This is a starting template — for complex structures (vesting schedules, multiple share classes, drag-along rights), have a lawyer review before submitting. Standard sole-founder and small multi-founder cases are usually fine with the template."

## Step 6 — Pre-flight checklist

Before the user signs:

```
OÜ registration pre-flight:
1. ✅ Company name confirmed available: [name]
2. ✅ Articles of Association drafted (ET + EN): both reviewed
3. ✅ Share-capital approach chosen: [amount, payment timing]
4. ✅ Service provider contracted: [provider name, what they cover]
5. ✅ State fee budget confirmed: €[from live page]
6. ✅ e-Residency card in hand
7. ✅ DigiDoc4 client installed and tested
8. ✅ Card reader connected and verified
```

The user ticks each item. Anything unchecked = don't sign yet.

## Step 7 — Auth seam

> Now sign in to the **e-Business Register** (`https://ariregister.rik.ee/eng/application/start`) with your e-Residency ID-card via the DigiDoc4 client. Fill in the application using the data from Steps 2–4 (you'll paste the Articles of Association from Step 5). Sign. Pay the state fee. RIK will email you when the company is approved (typically within a business day).

After login, do not narrate the in-portal experience — the user is authenticated and the page itself guides them.

## Step 8 — After registration

Surface these post-registration tasks (verify each against the current live page):

- **Open a business bank account.** Wise, LHV, and various fintechs are common; the marketplace lists provider options. Some banks won't open accounts for non-resident-owned OÜs; an Estonian fintech partner is the usual workaround.
- **Register for VAT** if anticipated turnover exceeds the current threshold. Fetch the current threshold from emta.ee; the application is via e-MTA after the company is registered.
- **File the annual report** after the first financial year ends (deadline depends on financial year end — usually 6 months after).
- **Set up accounting.** Many founders use the marketplace provider chosen in Step 4; the service provider typically handles VAT filings, monthly bookkeeping, and the annual report.

## Sources

See `references/sources.md`.
