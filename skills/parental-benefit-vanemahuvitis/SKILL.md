---
name: parental-benefit-vanemahuvitis
description: |
  Walks an Estonian resident or citizen through planning, calculating, and
  applying for parental benefit (vanemahüvitis) — the income-based benefit
  paid by the Social Insurance Board to one parent on leave with a new child.
  Use when the user mentions: "vanemahüvitis", "parental benefit", "parental
  leave Estonia", "maternity benefit", "paternity benefit", "how much will
  I get on parental leave", "split parental leave between parents". Always
  re-fetches current rates and caps from sotsiaalkindlustusamet.ee — never
  quotes cached numbers. Computes interactively from the user's gross
  salary; never asks for the user's isikukood, account number, or salary
  slips.
license: MIT
allowed-tools: >-
  WebFetch(domain:eesti.ee) WebFetch(domain:www.eesti.ee)
  WebFetch(domain:riigiteataja.ee) WebFetch(domain:www.riigiteataja.ee)
  WebFetch(domain:emta.ee) WebFetch(domain:www.emta.ee) WebFetch(domain:maasikas.emta.ee)
  WebFetch(domain:politsei.ee) WebFetch(domain:www.politsei.ee) WebFetch(domain:broneering.politsei.ee)
  WebFetch(domain:ariregister.rik.ee) WebFetch(domain:ettevotjaportaal.rik.ee) WebFetch(domain:avaandmed.ariregister.rik.ee)
  WebFetch(domain:e-resident.gov.ee) WebFetch(domain:www.e-resident.gov.ee) WebFetch(domain:marketplace.e-resident.gov.ee)
  WebFetch(domain:sotsiaalkindlustusamet.ee) WebFetch(domain:tootukassa.ee) WebFetch(domain:tervisekassa.ee) WebFetch(domain:terviseamet.ee)
  WebFetch(domain:transpordiamet.ee) WebFetch(domain:www.transpordiamet.ee) WebFetch(domain:maanteamet.ee) WebFetch(domain:www.maanteamet.ee) WebFetch(domain:lkf.ee) WebFetch(domain:www.lkf.ee)
  WebFetch(domain:tallinn.ee) WebFetch(domain:www.tallinn.ee) WebFetch(domain:tartu.ee) WebFetch(domain:www.tartu.ee) WebFetch(domain:parnu.ee) WebFetch(domain:www.parnu.ee) WebFetch(domain:narva.ee) WebFetch(domain:www.narva.ee)
  WebFetch(domain:id.ee) WebFetch(domain:www.id.ee) WebFetch(domain:smart-id.com) WebFetch(domain:www.smart-id.com) WebFetch(domain:sk.ee) WebFetch(domain:www.sk.ee)
  WebFetch(domain:andmed.stat.ee) WebFetch(domain:avaandmed.eesti.ee) WebFetch(domain:stat.ee) WebFetch(domain:www.stat.ee)
  WebFetch(domain:maaamet.ee) WebFetch(domain:www.maaamet.ee) WebFetch(domain:geoportaal.maaamet.ee)
  WebFetch(domain:teatmik.ee) WebFetch(domain:www.teatmik.ee) WebFetch(domain:inforegister.ee) WebFetch(domain:www.inforegister.ee) WebFetch(domain:e-krediidiinfo.ee) WebFetch(domain:www.e-krediidiinfo.ee) WebFetch(domain:krediidiinfo.ee) WebFetch(domain:creditinfo.ee)
  WebSearch
metadata:
  audience: "citizen,resident"
  life_event: "family"
  service_domain: "social"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://sotsiaalkindlustusamet.ee/perehuvitised-ja-muud-toetused/perehuvitiste-ulevaade|https://sotsiaalkindlustusamet.ee/perehuvitised-ja-muud-toetused/perehuvitiste-ulevaade/vanemahuvitise-kalkulaator"
  last_verified: "2026-05-05"
  version: "0.1.0"
---

# Parental benefit (vanemahüvitis)

## Disclaimer

This is AI-generated procedural guidance, not legal, tax, or financial advice. The estimates this skill produces are illustrative — the authoritative monthly benefit is whatever Sotsiaalkindlustusamet (the Social Insurance Board) determines from your tax-paid income history. For complex situations (multiple children's leave overlapping, a second child arriving during the current leave, employment-status changes mid-leave, adoption, foster care, or self-employment income mixed with wage income), consult Sotsiaalkindlustusamet directly. This repository is not affiliated with the Republic of Estonia or Sotsiaalkindlustusamet.

## Freshness obligation

**Before computing or quoting any benefit rate, monthly cap, floor, leave-duration limit, application lead time, or fee, fetch the current pages at:**

- `https://sotsiaalkindlustusamet.ee/perehuvitised-ja-muud-toetused/perehuvitiste-ulevaade`
- `https://sotsiaalkindlustusamet.ee/perehuvitised-ja-muud-toetused/perehuvitiste-ulevaade/vanemahuvitise-kalkulaator`

**Do not use any number from this skill body.** Numbers below are illustrative only. Always replace them with what the live pages currently say. Parental-benefit law in Estonia has changed materially in recent years (caps, sharing rules, work-while-on-leave provisions), so cached numbers age fast.

## Step 1 — Disambiguate

Ask the minimum needed, in this order:

1. **Child's birth date or expected due date.** "When was the child born, or when is the due date?" The birth date determines which calendar year's income drives the benefit calculation — typically the calendar year before benefit start. For mid-year births, either parent's prior-year income may be usable; the live page describes the current rule.
2. **Which parent is the user.** "Are you the mother, the father, or either parent for the purpose of this question?" The mother's portion of the leave is reserved by law; the rest can be split between the parents in any combination.
3. **Employment status.** "Are you currently full-time employed, self-employed (FIE), a contractor, or unemployed?" This affects the calculation base — wage income is read from tax records; FIE income comes from the social-tax declarations.
4. **The other parent's status.** "Is the other parent working, on leave, or unemployed?" This affects household-income projection during leave but does not change the benefit calculation for the parent on leave.

**Never ask for the user's isikukood, account number, passport number, or salary slips.** They volunteer a gross-salary figure if they want a calculation; that gross figure is the only personal financial input this skill ever requests.

## Step 2 — Compute the benefit interactively

Once the basic situation is clear:

1. **Fetch the calculator/calculation page first.** WebFetch `https://sotsiaalkindlustusamet.ee/perehuvitised-ja-muud-toetused/perehuvitiste-ulevaade/vanemahuvitise-kalkulaator` and extract:
   - the formula (typically a percentage of average gross monthly income from the previous calendar year — confirm the exact percentage on the live page),
   - the current monthly **cap** (historically tied to a multiple of the national average wage),
   - the current monthly **floor** (a minimum benefit, historically tied to the national minimum wage),
   - the **leave-duration limits** — how many days/months at full rate, and any extension at a reduced rate,
   - the **mother's reserved portion** and the **shared portion** that parents can divide.

2. **Walk through the calculation.** Ask:

   > "What was your gross monthly salary in [previous calendar year]? (Or annual, if that's easier — I'll divide by 12.)"

   Then apply the formula and show every step:

   > "Your average gross was €X per month. The benefit is Y% of that = €Z. The current monthly cap is €C and the floor is €F, so your benefit is min(max(Z, F), C) = €B per month."

   Don't hide any computation. If the user gives an annual figure, show the division explicitly.

3. **Compute the leave duration.** From the live page, extract the total days at full rate plus any reduced-rate extension. Translate into months for the user. Show:

   > "At your benefit rate, you get €B per month for D months at full rate, then optionally €B' per month for D' more months at the reduced rate."

4. **Project household income during leave.** Ask the other parent's gross monthly figure (only if the user wants the projection). Then:

   > "Parent on leave: ~€B × D months = ~€(B × D) total benefit.
   > Other parent (continuing to work): ~€G × D months = ~€(G × D) gross.
   > Estimated household gross during the leave: ~€(B × D + G × D)."

   Flag that the other parent's wage continues to be subject to ordinary income tax and social tax, while parental benefit is also taxed but withheld at source by Sotsiaalkindlustusamet.

5. **Surface optional planning.** Two big levers:

   - **Splitting leave between parents.** The mother's reserved portion is fixed; the shared portion can go entirely to either parent or be split. Walk through trade-offs: if both parents earn similar amounts, splitting equally maximizes flexibility; if one earns much more, having the lower earner take more of the shared portion may preserve more household income (since each parent's benefit is capped by their own prior earnings).
   - **Second-child timing.** If a second child arrives within a defined window after the first, the previous benefit calculation can carry over advantageously rather than being recomputed against (potentially lower) recent income. The live page has the current rule and the window length — fetch and quote it.

**Always close the calculation with this caveat** (verbatim or close paraphrase):

> These are estimates based on the rates I just fetched. The authoritative figures will appear in your application portal at sotsiaalkindlustusamet.ee — the portal pulls your actual tax-paid income history. Verify each number there before submitting; if anything diverges meaningfully, the portal value wins.

## Step 3 — Generate planning checklist

Output a numbered checklist for the user. Format:

```
Parental-benefit planning checklist:

APPLICATION:
1. Apply at sotsiaalkindlustusamet.ee at least [N] days before your intended
   leave start (verify the exact lead time on the live page — historically
   ~30 days; do not trust cached numbers).
2. Notify your employer of the leave start date in writing, per the notice
   period in your employment contract.
3. If splitting leave with the other parent — each parent submits their
   own application that references the shared benefit pool. Coordinate the
   split before applying.

ADMIN:
4. In the self-service portal, confirm or update the bank account where the
   benefit will be paid.
5. Note the expected first-payment date so you can plan cash flow during the
   gap between last salary and first benefit payment.
6. If you plan to work part-time during leave (now allowed under recent
   reforms — check the live page for current rules), record the planned
   hours and earnings for transparency.

REVIEW:
7. After Sotsiaalkindlustusamet computes the official benefit, compare it
   against the estimate from Step 2. If the difference is large, the cause
   is usually a data discrepancy in your tax record — contact
   Sotsiaalkindlustusamet to reconcile.
```

This checklist is the tangible artifact the user takes into the self-service portal.

## Step 4 — Auth seam

> Now apply for parental benefit at the **Sotsiaalkindlustusamet self-service portal** (link from `https://sotsiaalkindlustusamet.ee/perehuvitised-ja-muud-toetused/perehuvitiste-ulevaade`) using your **Smart-ID, Mobile-ID, or ID-card**. The portal pulls your tax-paid income history and pre-fills the calculation. Verify against the estimates above; adjust the leave start date and split arrangement; submit.

After login, do not narrate the in-portal experience — the user is authenticated and the portal itself guides them.

## Sources

See `references/sources.md`.
