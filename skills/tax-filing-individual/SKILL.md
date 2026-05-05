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

This is AI-generated procedural guidance, not tax advice. The estimates this skill produces are illustrative — your authoritative tax position is whatever e-MTA shows in your pre-filled declaration. For complex situations (foreign income with treaty implications, FIE accounting, large capital gains), consult a qualified accountant. This repository is not affiliated with the Republic of Estonia or Maksu- ja Tolliamet.

## Freshness obligation

**Before computing or quoting any tax rate, threshold, deadline, or fee, fetch the current pages at:**

- `https://www.emta.ee/eraklient/tulu-deklareerimine`
- `https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad`

**Do not use any number from this skill body.** Numbers below are illustrative. Always replace them with what the live pages currently say.

## Step 1 — Disambiguate

Ask the minimum needed, in this order:

1. **Tax year.** "Which tax year are you filing for?" (Default: the previous calendar year. The Estonian tax year runs Jan 1 – Dec 31; declarations open in February.)
2. **Tax residency.** "Are you a tax resident of Estonia for that year?" (Tax residency: roughly ≥183 days in a 12-month period, or a permanent home in Estonia. If unsure, fetch the residency-test section on emta.ee and walk through it.)
3. **Income mix.** "What kinds of income did you receive that year?" (Employment salary, FIE / sole-proprietor, dividends, rental, capital gains, crypto, foreign income.)

**Never ask for the user's isikukood, account number, passport number, or salary slip data.** They tell you a gross figure if they want a calculation; that is the only personal financial input.

## Step 2 — Compute the tax interactively

Once you know the user's situation:

1. **Fetch current rates first.** WebFetch `https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad` and extract: basic exemption, basic-exemption phase-out threshold, headline income tax rate, and any special rates relevant to the income types the user has.

2. **Walk through each income type they have, in order.** For each, ask the gross figure, apply the live rate, show the math:

   - **Employment salary** — "What was your gross salary for [year]?" → Compute: `taxable = gross − exemption_for_this_income_level; tax = taxable × headline_rate`. Show every intermediate value.
   - **FIE / sole-proprietor** — Tax math is genuinely involved (gross revenue, deductible expenses, social tax). Offer to give a rough number with their estimate, but flag explicitly that an accountant is usually worth it for FIE.
   - **Capital gains** — "What was the sale price minus the cost basis?" → Apply the headline rate. Note that securities held in an investment account may get tax-deferred treatment.
   - **Crypto gains** — Same as capital gains; cite the dedicated emta.ee crypto subpage if you can find one.
   - **Rental income** — "What was your gross rental income?" → 20% of gross is deductible as flat-rate expense; tax the remainder.
   - **Foreign income** — "Which country, and what kind of income?" → Fetch treaty info from emta.ee if available. Note that foreign tax already paid usually credits against Estonian tax.

3. **Show your math at every step.** "Gross salary €X. Basic exemption €Y (current rate from emta.ee). Taxable €(X−Y). Tax at 22% = €Z." Don't hide any computation.

4. **Sum to a total**, then subtract tax already withheld (from employment) to estimate refund or amount owed:
   - "Your total tax liability: ~€A. Withholding already applied: ~€B. Expected refund: ~€(B−A)" (or amount due if A > B).

5. **Surface deductions** the user is likely eligible for: children, mortgage interest, voluntary pension contributions, education expenses, charitable donations. Pull the current deduction caps from emta.ee. For each, ask "do you have this?" and apply if yes.

**Always close the calculation with this caveat** (verbatim or close paraphrase):

> These are estimates based on the rates I just fetched. The authoritative figures will appear in your pre-filled e-MTA declaration. Verify each number there before submitting; if anything diverges meaningfully, the e-MTA value wins.

## Step 3 — Generate verification checklist

Output a numbered checklist for the user to take into e-MTA after login. Format:

```
Tax declaration checklist for [year]:

PRE-FILLED FIELDS TO VERIFY:
1. Employment income: should be ~€[gross] (your computation: €[X])
2. Income tax withheld: should be ~€[withholding] (your computation: €[B])
3. [other pre-filled items based on their situation]

FIELDS TO ADD MANUALLY:
4. Foreign income from [country]: €[amount] (treaty status: [...])
5. Rental income: €[gross]; minus 20% flat expenses
6. Capital gains from [security]: €[gain]
[etc.]

DEDUCTIONS TO CLAIM:
7. Children: [count] — apply the per-child deduction
8. Mortgage interest paid: €[amount]
9. Voluntary pension contributions: €[amount]
[etc.]

EXPECTED OUTCOME:
- Total tax: ~€[A]
- Refund / amount owed: ~€[B−A] refund / €[A−B] owed
```

This checklist is the tangible artifact the user takes to e-MTA. They walk through their declaration screen by screen and tick off each item.

## Step 4 — Auth seam

> Now log in to **e-MTA** at `https://maasikas.emta.ee/oma_ee/login` (or via `https://www.emta.ee/`) using your Smart-ID, Mobile-ID, or ID-card. Walk through the checklist above. Most fields will be pre-filled; verify and adjust where needed. Add any items in the "manual" section. Confirm your bank account for any refund. Submit.

After login, do not narrate the in-portal experience — the user is authenticated and the page itself guides them.

## Step 5 — Common pitfalls

- **Foreign income from EU and non-EU sources is treated differently** — a tax treaty may apply. If your computation looked off, this is a likely cause; consult an accountant for treaty-specific cases.
- **Cryptocurrency gains are declarable.** The rules are on a separate emta.ee page; fetch and cite if the user has crypto.
- **If you owe tax (rather than getting a refund), the payment deadline differs from the filing deadline.** e-MTA will show both.
- **The basic exemption phases out above an income threshold.** The live page has the current threshold; this is one of the most common sources of confusion when the math doesn't match expectations.
- **FIE accounting is genuinely complex.** If the user runs a sole proprietorship, recommend an accountant unless their income is small and simple.

## Sources

See `references/sources.md`.
