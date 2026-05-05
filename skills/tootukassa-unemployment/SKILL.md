---
name: tootukassa-unemployment
description: |
  Walks an Estonian resident or citizen who has lost or is losing
  employment through registration with Eesti Töötukassa, eligibility
  for unemployment-insurance benefit vs. unemployment allowance, and
  job-search obligations. Use when the user mentions: "Töötukassa",
  "unemployed Estonia", "register as unemployed", "unemployment benefit
  Estonia", "lost my job Estonia", "töötukassa registration".
  Determines eligibility live from tootukassa.ee rules, computes a
  benefit-amount estimate from the user's prior gross salary, and
  surfaces the obligations that come with registration. Never asks
  for the user's isikukood or account number.
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
  life_event: "employment"
  service_domain: "social"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.tootukassa.ee/en/job-seekers/registration-unemployed|https://www.tootukassa.ee/en/services/unemployment-insurance-benefit|https://www.tootukassa.ee/en/services/unemployment-allowance"
  last_verified: "2026-05-05"
  version: "0.1.0"
---

# Töötukassa unemployment registration

## Disclaimer

This is AI-generated procedural guidance, not legal or financial advice. Eligibility, benefit amounts, waiting periods, and durations are determined authoritatively by Eesti Töötukassa during the registration process — the estimates this skill produces are illustrative. For complex situations (collective dismissal, partial unemployment, EU citizens claiming aggregation of work history from another member state via a U1 form, freelance / FIE income earned alongside benefit, ongoing disputes over the reason for termination, or simultaneous applications for sickness/parental benefit), consult Töötukassa directly via their helpline or in-person service. This repository is not affiliated with the Republic of Estonia or Eesti Töötukassa.

## Freshness obligation

**Before computing or quoting any benefit rate, daily floor or cap, percentage, work-history threshold, waiting-period length, or maximum benefit duration, fetch the current pages at:**

- `https://www.tootukassa.ee/en/job-seekers/registration-unemployed`
- `https://www.tootukassa.ee/en/services/unemployment-insurance-benefit`
- `https://www.tootukassa.ee/en/services/unemployment-allowance`

**Do not use any number from this skill body.** Numbers below are illustrative only. Always replace them with what the live pages currently say. Estonian unemployment law has been amended repeatedly in recent years (waiting-period reforms, percentage step-down points, work-while-registered rules, allowance income threshold), so cached numbers age fast.

## Step 1 — Disambiguate

Ask the minimum needed, in this order:

1. **How did the employment end?** "Was it: (a) your own resignation, (b) mutual agreement with the employer, (c) employer-initiated termination — redundancy / liquidation / end-of-fixed-term, or (d) a fixed-term contract that simply expired?" The reason determines whether a longer waiting period applies before benefit payment starts, and influences whether unemployment-insurance benefit is available at all.
2. **Total work history.** "Roughly how many full months of insured employment have you had in the last 36 months? (Estonian employment counts; EU/EEA work counts too if you can produce a U1 form from the other country.)" The unemployment-insurance benefit requires a minimum insured-work threshold over the last 36 months — the live page has the current number (historically 12 months); confirm it.
3. **Recent shorter employment.** "If your work history in the last 36 months is below the insurance threshold, what about the last 12 months? Did you work or study at least 180 days during that window?" This routes to the unemployment allowance branch.
4. **Current status.** "Are you still employed (last working day approaching) or has employment already ended? If approaching, what is the last day?" Registration cannot be filed before the last working day; the user wants to register from day one of unemployment to maximise the benefit window.

**Never ask for the user's isikukood, account number, passport number, or salary slips.** They volunteer a gross-salary figure if they want a benefit calculation; that gross figure is the only personal financial input this skill ever requests.

## Step 2 — Eligibility decision tree

Apply the answers from Step 1 against the live thresholds (re-fetch them — do not rely on the illustrative numbers below):

**Branch A — Unemployment-insurance benefit (töötuskindlustushüvitis):**
- Work history meets or exceeds the live insured-work threshold (illustratively ≥12 months in the last 36), AND
- Reason for ending is employer-initiated, mutual agreement, or end of fixed-term contract → **likely eligible** for the insurance benefit. The waiting period before payments start is shorter for these reasons; verify on the live page.
- If reason is the user's own resignation but the work-history threshold is still met → **likely eligible** with a longer waiting period (historically several months from registration before payments begin); verify the current waiting-period length live.

**Branch B — Unemployment allowance (töötutoetus):**
- Insurance benefit not available (work history below the insurance threshold, or insurance benefit already exhausted), AND
- The user worked or studied at least 180 days in the 12 months before registration, AND
- The user's current net income falls below the live monthly threshold → **likely eligible** for the flat-rate allowance, paid daily up to the live maximum duration.

**Branch C — Registration only (no monetary benefit):**
- Neither branch's work-history condition is met → the user can still **register as unemployed** to access job-search support, training programmes, career counselling, and continued state health insurance coverage during the registration period. No cash benefit, but the non-cash entitlements are substantial.

State the result back explicitly: "Based on what you've described, you appear eligible for **[benefit type]**. Note this is an estimate — Töötukassa makes the actual eligibility decision during registration after they verify your insured-work history from tax and social-tax records."

## Step 3 — Compute benefit estimate

Once a branch is identified, walk the user through a numerical estimate. Always re-fetch rules from the live page first.

**For Branch A (unemployment-insurance benefit):**

1. **Fetch the calculation page.** WebFetch `https://www.tootukassa.ee/en/services/unemployment-insurance-benefit` (and follow links to "Calculation and payment of unemployment insurance benefit" if present) and extract:
   - the **average-daily-wage formula** (typically computed from a defined recent reference window — historically the last 9 months, but verify),
   - the **percentage of average daily wage** paid as benefit, and the **step-down**: a higher percentage for the first N days, a lower percentage thereafter (historically 60% / 40% with the step at day 100 — verify),
   - the **daily floor** (minimum daily benefit) and **daily cap** (maximum daily benefit),
   - the **maximum duration** in calendar days, which depends on insured-work history (historically 180 / 270 / 360 days bands — verify the bands and the boundaries).

2. **Walk through the calculation.** Ask:

   > "What was your gross monthly salary in your last job? (Or daily, if that's easier.)"

   Then show every step:

   > "Your gross monthly was €X. Average daily wage = €X × 12 / 365 = €D/day. The benefit rate is P1% of €D for the first N1 days = €B1/day, then P2% of €D for the rest = €B2/day. The current daily floor is €F and the daily cap is €C, so per-day benefit is min(max(B, F), C)."

   Don't hide any computation. If the user gives an annual figure, show the division explicitly.

3. **Project the total.** Based on the user's work-history band, identify the maximum duration D (days) on the live page. Show:

   > "At your insured-work band, the maximum duration is D days. Indicative total: N1 days × €B1 + (D − N1) days × €B2 = €T (before tax — the benefit is taxable income; Töötukassa withholds income tax at source)."

   Flag the **waiting period** before payments start (longer if the reason was the user's own resignation; verify the current value live).

**For Branch B (unemployment allowance):**

1. Fetch `https://www.tootukassa.ee/en/services/unemployment-allowance` and extract the current **flat daily rate**, the **maximum number of days** of payment, and the **net monthly income threshold** above which eligibility is lost.
2. Multiply: `daily rate × max duration days = indicative total`. Show the arithmetic.
3. Note that the allowance is also taxable in principle but small; confirm tax treatment from the live page.

**Always close with this caveat** (verbatim or close paraphrase):

> These are estimates based on the rates I just fetched. The authoritative figures are computed in the Töötukassa self-service portal from your tax and social-tax history; the portal value wins. Confirm everything there before you rely on it for budgeting.

## Step 4 — Document checklist

Pull from the live registration page; the typical items are:

```
Documents you'll need to register as unemployed:

ALWAYS:
- ID document (Estonian ID-card, EU/EEA ID, or passport).
- Information about your most recent employment: employer name, last day,
  reason for ending. The actual termination order / contract may not be
  required — Töötukassa pulls employment data from the tax register —
  but bring a copy in case the consultant needs to clarify.

IF YOU'RE APPLYING FOR THE UNEMPLOYMENT-INSURANCE BENEFIT:
- The employer's termination order (lõpetamise käskkiri) or equivalent —
  helps confirm the reason for ending if the tax-register entry is
  ambiguous about who initiated the termination.
- Your last employment contract (helps confirm full-time / part-time
  status if relevant for the calculation).

IF SOME OF YOUR WORK HISTORY IS FROM ANOTHER EU/EEA COUNTRY:
- A U1 form (Statement Concerning Periods to be Taken Into Account for the
  Granting of Unemployment Benefits) issued by that country's social-
  security office. Without U1, foreign work cannot be aggregated against
  the Estonian work-history threshold.

IF YOU'RE A THIRD-COUNTRY NATIONAL WITH A VALID ESTONIAN RESIDENCE PERMIT:
- Copy of the residence permit (most permit categories permit registration
  as unemployed; some — e.g., student permits — do not. Verify on the
  live registration page).
```

Tailor the list to the user's specific branch (don't list U1 if all work was in Estonia; don't list employer termination order if Branch B / C).

## Step 5 — Post-registration obligations summary

Registration creates ongoing obligations. Surface them clearly so the user understands the trade — benefit and services in exchange for active job search:

- **Regular contact with the consultant.** Frequency varies; verify on the live page (historically every 30 days, with at least one in-person or video meeting per cycle). Missing a contact without a valid reason terminates the benefit and can end the registration.
- **Apply for jobs the consultant suggests** and report back on the outcome. The portal shows the assigned vacancies; the user is expected to engage with them in good faith.
- **Attend training programmes** the consultant assigns (e.g., career counselling, language courses, vocational retraining). Refusal without valid reason has the same consequence as missing contact.
- **Notify Töötukassa promptly** of any short-term work, freelance income, illness, or travel abroad — these affect benefit eligibility and amount.
- **Continued state health insurance.** While registered as unemployed, the user retains public health-insurance coverage at no cost via Tervisekassa, even with no benefit payment in Branch C. This is often the single most valuable feature of registration for those without a cash benefit.

If the user is on Branch A (insurance benefit), flag explicitly that **the benefit is suspended or terminated** if obligations are missed, and that re-registration after termination is constrained — better to maintain compliance than to recover after a stop.

## Step 6 — Auth seam

> Now register at the Töötukassa self-service portal at **https://www.tootukassa.ee/iseteenindus** using your **Smart-ID, Mobile-ID, or ID-card**. Submit the registration application; attach the documents from Step 4 if requested. A consultant will be assigned within a working day and will contact you to schedule the first counselling session. The benefit calculation in the portal is authoritative and pulls your real tax-paid wage history; the estimate above is for planning only — verify the portal numbers before relying on them.

After login, do not narrate the in-portal experience — the user is authenticated and the portal itself guides them.

## Sources

See `references/sources.md`.
