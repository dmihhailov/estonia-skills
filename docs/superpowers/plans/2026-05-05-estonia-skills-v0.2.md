# estonia-skills v0.2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add five new atomic skills targeted at the citizens/residents audience: `parental-benefit-vanemahuvitis`, `vehicle-transfer`, `tootukassa-unemployment`, `passport-or-idcard-renewal`, `driving-licence`. Plus extend the canonical "Trusted Estonian Sources" allowlist with the transport / booking / unemployment subdomains these skills need.

**Architecture:** Each new skill follows the v0.1 patterns documented in `CONTRIBUTING.md` — agentic body shape (disclaimer → freshness obligation → disambiguate → walkthrough that *does* live lookups / computation / drafting → eID auth seam → sources), TES allowlist as `allowed-tools`, validators in CI. No changes to validators, plugin manifests, or v0.1 skills' bodies (only their `allowed-tools` block gets updated when TES extends).

**Tech Stack:** No new dependencies. Existing Python 3.11 + PyYAML + pytest harness. Only Markdown + JSON edits.

**Reference:** Spec at `docs/superpowers/specs/2026-05-03-estonia-skills-design.md`; v0.1 plan at `docs/superpowers/plans/2026-05-03-estonia-skills-v1.md`.

---

## File Structure

```
estonia-skills/
├── skills/
│   ├── estonia/SKILL.md                        # Task 1: refresh allowed-tools
│   ├── tax-filing-individual/SKILL.md          # Task 1: refresh allowed-tools
│   ├── ou-open-e-resident/SKILL.md             # Task 1: refresh allowed-tools
│   ├── residence-registration/SKILL.md         # Task 1: refresh allowed-tools
│   ├── parental-benefit-vanemahuvitis/         # Task 2 — NEW
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   ├── vehicle-transfer/                       # Task 3 — NEW
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   ├── tootukassa-unemployment/                # Task 4 — NEW
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   ├── passport-or-idcard-renewal/             # Task 5 — NEW
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   ├── driving-licence/                        # Task 6 — NEW
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   └── estonia/INDEX.yaml                      # auto-regenerated each task
├── CONTRIBUTING.md                             # Task 1: TES block + table
└── .claude/settings.json                       # Task 1: WebFetch domains
```

---

## Task 1: Extend Trusted Estonian Sources allowlist (TES)

**Files:**
- Modify: `CONTRIBUTING.md` (TES block + category table)
- Modify: `.claude/settings.json` (WebFetch domains)
- Modify: `skills/estonia/SKILL.md` (allowed-tools)
- Modify: `skills/tax-filing-individual/SKILL.md` (allowed-tools)
- Modify: `skills/ou-open-e-resident/SKILL.md` (allowed-tools)
- Modify: `skills/residence-registration/SKILL.md` (allowed-tools)

The v0.2 skills need transport (Maanteamet successor `transpordiamet.ee`), insurance (`lkf.ee`), and booking-system (`broneering.politsei.ee`) domains; plus `tootukassa.ee` self-service subdomains. Adding them to the canonical TES, then updating every skill's `allowed-tools` block to match.

- [ ] **Step 1: Verify each new domain returns 200 via WebFetch**

Run from repo root:
```bash
. .venv/bin/activate
for d in www.transpordiamet.ee transpordiamet.ee www.maanteamet.ee maanteamet.ee www.lkf.ee lkf.ee broneering.politsei.ee; do
  echo "=== $d ==="
  curl -sI "https://$d" | head -3
done
```
Expected: each returns either 200 OK, or a 301/302 redirect to a same-or-related host. If a domain doesn't resolve at all, drop it from the additions and note in your report — don't allowlist a domain that doesn't exist.

For `maanteamet.ee` specifically: the agency renamed to Transpordiamet in 2021, so it likely 301-redirects. Allowlist it anyway because cached content and old links still reference it.

- [ ] **Step 2: Update `CONTRIBUTING.md` — TES block**

Use Edit. Locate the existing TES code block (the `allowed-tools: >-` block under "Canonical `allowed-tools` block"). Replace the entire block with:

```yaml
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
```

- [ ] **Step 3: Update `CONTRIBUTING.md` — category table**

Add three new rows to the existing "What's in the list, by category" table, between the "Police / identity (PPA)" row and the "Business registry (RIK)" row, and after the "Major city portals" row. Use Edit:

```markdown
| Police / identity (PPA) | `politsei.ee`, `broneering.politsei.ee` |
```
(replaces the old `politsei.ee` row — the booking subsystem is on a separate subdomain that needs its own allowlist entry)

```markdown
| Social / health | `sotsiaalkindlustusamet.ee`, `tootukassa.ee`, `tervisekassa.ee`, `terviseamet.ee` |
```
(replaces the old social/health row)

Add a new row before the city-portals row:

```markdown
| Transport / vehicles / insurance | `transpordiamet.ee` (Estonian Transport Administration), `maanteamet.ee` (legacy Road Administration redirect), `lkf.ee` (Traffic Insurance Fund) |
```

- [ ] **Step 4: Update `.claude/settings.json`**

Add the new WebFetch domains to the `permissions.allow` array. Use Edit; locate the existing block of `WebFetch(domain:...)` entries and add these (preserve order; group near related domains):

After `"WebFetch(domain:www.politsei.ee)"`:
```json
      "WebFetch(domain:broneering.politsei.ee)",
```

After `"WebFetch(domain:andmed.stat.ee)"`:
```json
      "WebFetch(domain:transpordiamet.ee)",
      "WebFetch(domain:www.transpordiamet.ee)",
      "WebFetch(domain:maanteamet.ee)",
      "WebFetch(domain:www.maanteamet.ee)",
      "WebFetch(domain:lkf.ee)",
      "WebFetch(domain:www.lkf.ee)",
      "WebFetch(domain:tootukassa.ee)",
      "WebFetch(domain:sotsiaalkindlustusamet.ee)",
```

Verify the JSON parses:
```bash
python3 -c "import json; json.load(open('.claude/settings.json')); print('OK')"
```
Expected: `OK`.

- [ ] **Step 5: Update each existing skill's `allowed-tools` block**

Four skills need updates: `skills/estonia/SKILL.md`, `skills/tax-filing-individual/SKILL.md`, `skills/ou-open-e-resident/SKILL.md`, `skills/residence-registration/SKILL.md`.

For each, use Edit to replace the existing `allowed-tools: >-\n  WebFetch(domain:eesti.ee) ...` YAML block with the new TES block from Step 2 above. The new block adds three groups of entries:

1. `WebFetch(domain:broneering.politsei.ee)` — added to the police row.
2. A new transport row: `WebFetch(domain:transpordiamet.ee) WebFetch(domain:www.transpordiamet.ee) WebFetch(domain:maanteamet.ee) WebFetch(domain:www.maanteamet.ee) WebFetch(domain:lkf.ee) WebFetch(domain:www.lkf.ee)`.

The fastest way to apply: copy the entire TES block from CONTRIBUTING.md (just edited in Step 2) and replace the entire block in each skill. The frontmatter still must end with `---`; do not remove that.

- [ ] **Step 6: Validate**

```bash
. .venv/bin/activate
python scripts/validate_frontmatter.py
python scripts/build_index.py
python scripts/check_no_pii.py
pytest -q
```
Expected: 4 skills validated, INDEX.yaml regenerated (will produce no diff since description didn't change), PII clean, 22/22 tests pass.

- [ ] **Step 7: Commit**

```bash
git add CONTRIBUTING.md .claude/settings.json skills/estonia/SKILL.md skills/tax-filing-individual/SKILL.md skills/ou-open-e-resident/SKILL.md skills/residence-registration/SKILL.md
git commit -m "$(cat <<'EOF'
Extend TES allowlist with transport, booking, unemployment subdomains

v0.2 introduces five citizens/residents skills that reach for new
gov domains:
- transpordiamet.ee + maanteamet.ee — vehicle and driving-licence
- lkf.ee — traffic insurance lookups for vehicle skill
- broneering.politsei.ee — PPA appointment booking for passport/ID
- broneering.politsei.ee — PPA appointment booking (corrected from broneeri.politsei.ee)

Adds them to the canonical Trusted Estonian Sources block and
propagates to every existing skill's allowed-tools, plus the
project's .claude/settings.json. CONTRIBUTING.md updated with
new category rows.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: `parental-benefit-vanemahuvitis` skill

**Files:**
- Create: `skills/parental-benefit-vanemahuvitis/SKILL.md`
- Create: `skills/parental-benefit-vanemahuvitis/references/sources.md`

This is the highest-value skill in the batch. Estonian parental benefit (vanemahüvitis) is calculated from the previous calendar year's social-tax-paid income, capped at 3× national average wage. Either parent can take leave; can be split between them. The agent's pre-auth surface is large: compute the estimated monthly benefit from the user's gross-salary input, walk through the optimal mum/dad split timing, project total household income during leave, and surface the application channel. **Authoritative agency: Sotsiaalkindlustusamet (Social Insurance Board).**

- [ ] **Step 1: Verify URLs via WebFetch**

Use WebFetch on each candidate URL and confirm 200 + relevant content. Drill from the homepage if a deep link 404s, the way Tasks 8-10 did in the v0.1 plan. Report each URL's outcome.

Candidates (drill from these starting points to find the most-specific verified canonical URL):
- `https://sotsiaalkindlustusamet.ee/lapsed-ja-pere/vanemahuvitis` — primary parental-benefit overview
- `https://sotsiaalkindlustusamet.ee/lapsed-ja-pere/vanemahuvitis/vanemahuvitise-arvutamine` — benefit calculation rules (the live source for the formula and current cap)
- `https://www.eesti.ee/en/family-and-relationships/parental-benefits` — EN-language overview at the state portal (eesti.ee is an SPA so the deep link may not resolve directly; if so, the homepage is the freshness anchor and the body instructs the agent to navigate)

If a URL 404s, find the corrected canonical and use that instead. Report all URLs with `last_verified: 2026-05-05`.

- [ ] **Step 2: Create `skills/parental-benefit-vanemahuvitis/SKILL.md` — frontmatter**

```yaml
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
allowed-tools: <PASTE THE TES BLOCK FROM CONTRIBUTING.md, IDENTICAL TO TASK 1 STEP 2>
metadata:
  audience: "citizen,resident"
  life_event: "family"
  service_domain: "social"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "<URL_1>|<URL_2>"
  last_verified: "2026-05-05"
  version: "0.1.0"
---
```

Replace `<URL_1>` and `<URL_2>` with the verified URLs from Step 1.

- [ ] **Step 3: Write the body following the agentic pattern**

Five sections, in order. Use the v0.1 `tax-filing-individual` skill (`skills/tax-filing-individual/SKILL.md`) as a style reference for the computation pattern.

**Section 1: Disclaimer.** Reproduce the standard disclaimer with this skill's specifics: AI-generated procedural guidance, not legal/tax/financial advice. Estimates produced by the calculator are illustrative; the authoritative monthly benefit is whatever Sotsiaalkindlustusamet determines from your tax-paid income history. For complex situations (multiple children's leave overlapping, second child during current leave, employment status changes mid-leave), consult Sotsiaalkindlustusamet directly. Repository not affiliated with the Republic of Estonia or Sotsiaalkindlustusamet.

**Section 2: Freshness obligation.** List both verified URLs from Step 1. Instruct the agent to fetch the calculation page before quoting any rate, cap, threshold, leave-duration limit, or fee. Forbid quoting any number from the body itself.

**Section 3: Step 1 — Disambiguate.** Ask the minimum needed:
1. Child's birth or expected birth date — determines which calendar year's income drives the benefit (always the previous calendar year before benefit start; mid-year births can use either parent's prior income depending on circumstances).
2. Which parent is the user — mother / father / either-parent-able-to-claim. Mother is required to take a portion (the maternity-leave portion); the rest is splittable.
3. Employment status — full-time employed, FIE/sole-proprietor, contractor, unemployed. Affects the benefit calculation base.
4. The other parent's status (also working / on leave / unemployed) — affects the household-income projection.

Explicit safety line: never ask for isikukood, account numbers, or salary slips. The user volunteers a gross-salary figure if they want a calculation; that's the only personal financial input.

**Section 4: Step 2 — Compute the benefit interactively.** This is the agent's biggest pre-auth contribution.

1. **Fetch the current calculation page first** (the `vanemahuvitise-arvutamine` URL or equivalent). Extract: the formula (typically X% of average gross monthly income from the previous calendar year), the monthly cap (typically 3× national average wage), the floor (minimum benefit equal to a multiple of national minimum wage), and the leave-duration limits.
2. **Walk the calculation:**
   - "What was your gross monthly salary in [previous calendar year]? (Or annual, if easier.)"
   - Apply the formula: `monthly_benefit = average_gross_monthly_income × benefit_rate`, capped at the monthly cap and floored at the minimum.
   - Show every step: "Your average gross was €X. The benefit is Y% of that = €Z. The current cap is €C, so your benefit is min(Z, C) = €B."
3. **Compute the leave-duration:** how many months of full-rate benefit, plus any extension at reduced rate. Pull from the live page.
4. **Project total household income during leave:**
   - Parent on benefit: ~€B per month for D months.
   - Other parent: their continuing income (ask, gross figure).
   - Estimated total: B × D + other_parent's_income × D.
5. **Surface optional planning:**
   - Splitting leave between parents — the mother portion is fixed, the rest can be assigned. Show the user trade-offs (each parent's individual benefit if one earns more than the cap; childcare flexibility).
   - Second-child timing — if the user is considering another child within the leave period, the previous benefit calculation can carry over advantageously. Mention this and link to the relevant page.

End the calculation section with: "These are estimates based on the rates I just fetched. The authoritative figures will appear in your application portal at sotsiaalkindlustusamet.ee. Verify each number there before submitting."

**Section 5: Step 3 — Generate planning checklist.** Output a numbered checklist with:
1. Apply for benefit at sotsiaalkindlustusamet.ee at least 30 days before leave start (verify exact lead time from live page).
2. Notify employer of leave start date.
3. If splitting with other parent — submit each parent's application referencing the shared benefit pool.
4. Update bank account in self-service if changed.
5. Note expected first payment date.

**Section 6: Auth seam.** "Now apply for parental benefit at the Sotsiaalkindlustusamet self-service portal (link from sotsiaalkindlustusamet.ee/lapsed-ja-pere) using your Smart-ID, Mobile-ID, or ID-card. The portal pulls your tax-paid income history and pre-fills the calculation. Verify against the estimates above; submit."

**Section 7: Sources.** "See `references/sources.md`."

- [ ] **Step 4: Create `skills/parental-benefit-vanemahuvitis/references/sources.md`**

```markdown
# Sources — parental-benefit-vanemahuvitis

All canonical URLs cited in this skill. Verify each URL returns 200 and contains the expected content; record the date of last check.

| URL | Purpose | Last checked |
|---|---|---|
| <URL_1 from Step 1> | Parental benefit overview | 2026-05-05 |
| <URL_2 from Step 1> | Benefit calculation rules + current cap | 2026-05-05 |
| https://sotsiaalkindlustusamet.ee/lapsed-ja-pere | Family benefits index page | 2026-05-05 |

If a URL changes or returns non-200, update this table and bump `last_verified` in `SKILL.md`.
```

- [ ] **Step 5: Validate, regenerate index, PII-check**

```bash
. .venv/bin/activate
python scripts/validate_frontmatter.py
python scripts/build_index.py
python scripts/check_no_pii.py
```
Expected: validate says "validated 5 skill(s)" (router + 3 v0.1 + this), INDEX.yaml lists 4 atomic skills, PII clean.

- [ ] **Step 6: Commit**

```bash
git add skills/parental-benefit-vanemahuvitis/ skills/estonia/INDEX.yaml
git commit -m "$(cat <<'EOF'
Add parental-benefit-vanemahuvitis skill

Citizens/residents v0.2: walks the user through planning, computing,
and applying for vanemahüvitis. Pre-auth surface includes interactive
benefit calculation from previous-year gross income (cap fetched live
from sotsiaalkindlustusamet.ee), parent-split timing strategy,
household-income projection during leave, and a planning checklist.
Auth seam at sotsiaalkindlustusamet.ee self-service.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: `vehicle-transfer` skill

**Files:**
- Create: `skills/vehicle-transfer/SKILL.md`
- Create: `skills/vehicle-transfer/references/sources.md`

Buying or selling a vehicle is a common interaction with the Estonian state. The agent's pre-auth surface includes: live insurance status check via lkf.ee (public lookup by registration number), MOT status check via transpordiamet.ee, fee computation, and a personalised pre-/post-transfer checklist. **Authoritative agency: Transpordiamet (Estonian Transport Administration; absorbed Maanteamet in 2021).**

- [ ] **Step 1: Verify URLs via WebFetch**

Candidates (drill from these for the most-specific canonical):
- `https://www.transpordiamet.ee/sõidukite-registreerimine` — vehicle registration overview (Estonian)
- `https://www.transpordiamet.ee/en/vehicle-registration` — same in English
- `https://www.lkf.ee` — Traffic Insurance Fund homepage
- `https://www.lkf.ee/poliisi-andmed` — public lookup of insurance status by registration number (verify the actual canonical path; this may have moved)
- `https://www.emta.ee/eraklient/maksud-ja-tasumine/auto-ja-veokimaks` — vehicle tax (Estonia introduced car tax in 2025, "automaks"; verify the current canonical page exists)

If any URL 404s, find the correct canonical via the homepage and use that. Report each URL's outcome.

- [ ] **Step 2: Create `skills/vehicle-transfer/SKILL.md` — frontmatter**

```yaml
---
name: vehicle-transfer
description: |
  Walks an Estonian resident, citizen, or new arrival through buying or
  selling a road vehicle in Estonia: ownership transfer at the
  Transpordiamet, mandatory traffic insurance, MOT status, and the
  current car tax (automaks). Use when the user mentions: "transfer car",
  "sell car Estonia", "buy car Estonia", "register vehicle", "automaks",
  "Maanteamet", "Transpordiamet", "MOT booking", "OSAGO", "tehnoülevaatus".
  Does live registration / insurance / MOT lookups via the public
  registries; computes fees from current rates. Never asks for the
  user's isikukood or bank details.
license: MIT
allowed-tools: <PASTE THE TES BLOCK FROM CONTRIBUTING.md>
metadata:
  audience: "citizen,resident,expat-newcomer"
  life_event: "vehicle"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "<URL_1>|<URL_2>|<URL_3>"
  last_verified: "2026-05-05"
  version: "0.1.0"
---
```

Replace `<URL_*>` with verified URLs (transpordiamet vehicle registration, lkf.ee insurance lookup, emta.ee car tax).

- [ ] **Step 3: Write the body**

Use the v0.1 `ou-open-e-resident` skill (`skills/ou-open-e-resident/SKILL.md`) as a style reference for the live-lookup + draft-generator pattern.

**Section 1: Disclaimer.** AI guidance, not legal advice; the authoritative vehicle status is whatever Transpordiamet shows. For disputes (vehicle history defects, encumbrances), use a vehicle-history professional service. Not affiliated with the state.

**Section 2: Freshness obligation.** List the three verified URLs. Instruct: don't quote any fee, tax rate, or insurance premium from this body — fetch live before answering.

**Section 3: Step 1 — Disambiguate.** Ask:
1. Buying or selling? (Determines who the agent is helping.)
2. Vehicle category — passenger car, van, motorcycle, trailer, mopeds. (Different rules and fees per category.)
3. Has the vehicle been in Estonia before, or is it being imported? (Imports have additional steps: customs, type-approval check.)
4. Does the user have eID? (Most steps need it; some can be done on paper at a service point.)

**Section 4: Step 2 — Live status checks.** For an existing Estonian vehicle, ask the user for the registration number (this is publicly displayed on every vehicle, not PII; treat it like a domain name). Then:
1. **Insurance status** — WebFetch the lkf.ee insurance lookup with the registration number. Parse: is the vehicle insured today? When does the policy expire? Is the insurer named? Surface this.
2. **MOT status** — WebFetch the transpordiamet.ee MOT lookup if available. Parse: is the MOT current? When does it expire?
3. **Registration ownership** — note that the public Transpordiamet lookup typically does NOT expose the current owner's name (privacy); the buyer learns this from the seller and verifies via the e-state portal during the transfer flow.

If any of these are missing or expired, surface as a buyer's-due-diligence flag.

**Section 5: Step 3 — Compute fees.** Pull current values from the live pages:
- Transfer state fee.
- Annual car tax (automaks) for this vehicle category — applies to the new owner pro-rata from purchase.
- Insurance premium estimate — note that lkf.ee shows minimum insurer pricing on the central insurance-comparison page (also fetch and surface, if available); actual premium depends on the chosen insurer.

Sum up the buyer's first-year cost: `transfer_fee + automaks_year + cheapest_insurer_year`.

**Section 6: Step 4 — Generate the transfer checklist.** Personalised:

```
Transfer checklist:

BEFORE:
- ✅ Confirm seller's identity matches the registered owner
- ✅ Confirm the vehicle has valid insurance until at least transfer day
- ✅ Confirm MOT (tehnoülevaatus) is current, OR factor in the cost to renew
- ✅ Inspect the vehicle (or have it inspected by a professional)
- ✅ Agree on price and payment method

AT TRANSFER:
- ✅ Both buyer and seller log in to the Transpordiamet e-service
- ✅ Seller initiates the transfer; buyer accepts
- ✅ Buyer pays the transfer state fee (€X — fetched from live page)
- ✅ Buyer arranges new insurance (must be active before driving)

AFTER:
- ✅ Set up annual car tax (automaks) — declared via e-MTA
- ✅ Update insurance if buyer's terms differ
- ✅ Diary the next MOT date
```

**Section 7: Auth seam.** "Now log in to the Transpordiamet e-service at https://www.transpordiamet.ee using your Smart-ID, Mobile-ID, or ID-card. Both parties (buyer and seller) sign the transfer; the buyer pays the state fee in the same flow. New insurance must be active before the buyer drives away."

**Section 8: Sources.** Pointer to references/sources.md.

- [ ] **Step 4: Create `skills/vehicle-transfer/references/sources.md`**

Same template as Task 2 Step 4, with the verified URLs and 2026-05-05 dates.

- [ ] **Step 5: Validate, regenerate index, PII-check**

```bash
. .venv/bin/activate
python scripts/validate_frontmatter.py && python scripts/build_index.py && python scripts/check_no_pii.py
```
Expected: validates 6 skills.

- [ ] **Step 6: Commit**

```bash
git add skills/vehicle-transfer/ skills/estonia/INDEX.yaml
git commit -m "$(cat <<'EOF'
Add vehicle-transfer skill

Citizens/residents v0.2: walks buyer or seller through an Estonian
vehicle ownership transfer. Agent does live insurance lookups via
lkf.ee, MOT status via transpordiamet.ee, and fee computation
including the new car tax (automaks). Generates a personalised
pre-/at-/post-transfer checklist. Auth seam at the Transpordiamet
e-service.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: `tootukassa-unemployment` skill

**Files:**
- Create: `skills/tootukassa-unemployment/SKILL.md`
- Create: `skills/tootukassa-unemployment/references/sources.md`

Registering with Töötukassa after job loss is a high-stakes life event. The agent's pre-auth surface includes: eligibility decision tree (work-history threshold, contribution-based vs. allowance-only), benefit-amount estimate from prior salary, document checklist, and a summary of post-registration job-search obligations. **Authoritative agency: Eesti Töötukassa (Estonian Unemployment Insurance Fund).**

- [ ] **Step 1: Verify URLs via WebFetch**

Candidates:
- `https://www.tootukassa.ee/en/services/registration-as-unemployed` — registration overview (English) — drill from the homepage if the deep link 404s
- `https://www.tootukassa.ee/en/content/unemployment-insurance-benefit` — benefit eligibility and amount rules
- `https://www.tootukassa.ee/en/content/unemployment-allowance` — allowance for those who don't qualify for unemployment-insurance benefit
- `https://www.tootukassa.ee/iseteenindus` — self-service portal homepage (the actual registration happens here)

Find the most-specific canonical URLs and use those.

- [ ] **Step 2: Create `skills/tootukassa-unemployment/SKILL.md` — frontmatter**

```yaml
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
allowed-tools: <PASTE THE TES BLOCK>
metadata:
  audience: "citizen,resident"
  life_event: "employment"
  service_domain: "social"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "<URL_1>|<URL_2>|<URL_3>"
  last_verified: "2026-05-05"
  version: "0.1.0"
---
```

Replace `<URL_*>` with verified URLs.

- [ ] **Step 3: Write the body**

Use the v0.1 `residence-registration` skill (`skills/residence-registration/SKILL.md`) as a style reference for the decision-tree pattern.

**Section 1: Disclaimer.** AI guidance, not legal/financial advice; authoritative eligibility and amount come from Töötukassa. For complex situations (collective dismissal, partial unemployment, EU citizens with rights aggregation, freelance work alongside benefit), consult Töötukassa directly.

**Section 2: Freshness obligation.** List verified URLs; forbid quoting any rate, threshold, work-history requirement, or duration from the body.

**Section 3: Step 1 — Disambiguate.** Ask:
1. How did employment end? — resignation, mutual agreement, employer-initiated termination, end of fixed-term contract, etc. Affects waiting period and eligibility.
2. Total work history in last 36 months — full-time work duration matters for unemployment-insurance eligibility (the threshold is published on tootukassa.ee; verify live).
3. Reason for ending — own request usually has a longer waiting period; employer-initiated typically not.
4. Currently still employed (last day approaching) or already ended?

**Section 4: Step 2 — Eligibility decision tree.** Branch on the answers above:
- **If employer-terminated AND ≥12 months work in last 36 months (verify the exact threshold from live page):** likely eligible for unemployment-insurance benefit (töötuskindlustushüvitis). Compute estimate (Section 5).
- **If self-resigned AND ≥12 months work:** likely eligible after the longer waiting period. Compute estimate.
- **If <12 months work but ≥180 days in last 12 months:** eligible for unemployment allowance (töötutoetus) instead — flat-rate, much smaller. Surface the difference.
- **If <180 days work:** not eligible for monetary benefit; can still register as unemployed for job-search support, training programs, and continued health insurance. Surface this clearly so the user doesn't assume they get nothing.

State the result back: "Based on your situation, you appear eligible for [benefit type]. The actual eligibility decision is made by Töötukassa during registration; this is an estimate."

**Section 5: Step 3 — Compute benefit estimate.**

For unemployment-insurance benefit (töötuskindlustushüvitis):
1. Fetch current calculation rules from the live `unemployment-insurance-benefit` page.
2. Walk the formula: typically a percentage of average daily wage from the last 9 months, with a daily cap and a daily floor. The percentage steps down after a certain number of days.
3. "What was your gross monthly salary in your last job? (Or daily, if easier.)" Apply the formula. Show the steps.
4. Project total over the typical max-duration (usually 180-360 days depending on contribution history; verify live).

For unemployment allowance (töötutoetus): pull the flat daily rate from the live page; multiply by 270 days (or the verified max).

End with the standard caveat: estimate; Töötukassa decides; verify in the portal.

**Section 6: Step 4 — Document checklist.** Pull from the live page; typical items include:
- ID document (Estonian ID-card / passport / residence permit)
- Termination order from employer (lõpetamise käskkiri / korraldus)
- Last employment contract
- For non-Estonian work history (EU rights aggregation): a U1 form from the previous country's social security office

Output the personalised checklist.

**Section 7: Step 5 — Post-registration obligations summary.** What the user is signing up for:
- Visit Töötukassa office or portal regularly (frequency from live page)
- Apply for jobs the consultant suggests (pull current rules)
- Attend assigned training programs
- Loss of benefit if obligations are missed
- Continued public health insurance during registration

**Section 8: Auth seam.** "Now register at the Töötukassa self-service at https://www.tootukassa.ee/iseteenindus using your Smart-ID, Mobile-ID, or ID-card. Submit the documents above. A consultant will be assigned within a working day. The benefit calculation in the portal is authoritative; the estimate above is for planning only."

**Section 9: Sources.** Pointer.

- [ ] **Step 4: Create `references/sources.md`**

Standard template with verified URLs.

- [ ] **Step 5: Validate, regenerate, PII-check**

Expected: validates 7 skills.

- [ ] **Step 6: Commit**

```bash
git add skills/tootukassa-unemployment/ skills/estonia/INDEX.yaml
git commit -m "$(cat <<'EOF'
Add tootukassa-unemployment skill

Citizens/residents v0.2: registration with Eesti Töötukassa after
job loss. Pre-auth surface: eligibility decision tree
(unemployment-insurance benefit vs. unemployment allowance),
benefit-amount estimate from prior gross salary, document checklist,
post-registration obligations summary. Auth seam at
www.tootukassa.ee/iseteenindus.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: `passport-or-idcard-renewal` skill

**Files:**
- Create: `skills/passport-or-idcard-renewal/SKILL.md`
- Create: `skills/passport-or-idcard-renewal/references/sources.md`

Renewing a passport or ID-card is once-per-decade per person but every Estonian does it. The agent's pre-auth surface includes: eligibility check (validity dates, photo specs verification, fee fetch), live booking-availability lookup at PPA service points, embassy lookup if abroad, and a pre-appointment checklist. **Authoritative agency: Politsei- ja Piirivalveamet (Police and Border Guard Board, PPA).**

- [ ] **Step 1: Verify URLs**

Candidates:
- `https://www.politsei.ee/en/instructions/applying-for-a-passport` — passport renewal overview
- `https://www.politsei.ee/en/instructions/applying-for-an-id-card` — ID-card renewal overview
- `https://www.politsei.ee/en/instructions/photo-requirements` — photo specs (verify the actual canonical name)
- `https://broneering.politsei.ee` — appointment booking system (English language version may be at /en)
- `https://www.politsei.ee/en/contact/foreign-missions` — Estonian embassies abroad (for users renewing from outside Estonia)

Drill from politsei.ee/en if any deep link 404s.

- [ ] **Step 2: Create `skills/passport-or-idcard-renewal/SKILL.md` — frontmatter**

```yaml
---
name: passport-or-idcard-renewal
description: |
  Walks an Estonian citizen (or first-time applicant turning 15) through
  applying for or renewing a passport, an ID-card, or both at the same
  time. Use when the user mentions: "renew passport", "new passport",
  "renew ID-card", "ID-card expired", "passport application Estonia",
  "PPA appointment", "broneering.politsei.ee". Verifies eligibility,
  computes current fees, checks photo requirements, looks up booking
  availability at PPA service points, and finds the nearest Estonian
  embassy if applying from abroad. Never asks for the user's isikukood
  or document numbers.
license: MIT
allowed-tools: <PASTE TES BLOCK>
metadata:
  audience: "citizen,resident,expat-newcomer"
  life_event: "meta"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "id-card"
  authoritative_lang: "et"
  freshness_sources: "<URL_1>|<URL_2>|<URL_3>"
  last_verified: "2026-05-05"
  version: "0.1.0"
---
```

Note `auth_required: "id-card"` — the appointment booking and submission accept ID-card; Smart-ID/Mobile-ID may not be sufficient for first-time issuance, so be conservative. (If WebFetch confirms Smart-ID is accepted for renewal, expand the list.)

- [ ] **Step 3: Write the body**

Style reference: any v0.1 skill — this is form-filling-with-decision-tree pattern.

**Section 1: Disclaimer.** AI guidance, not legal advice. The PPA decides identity-document eligibility; this skill helps you prepare.

**Section 2: Freshness obligation.** List verified URLs.

**Section 3: Step 1 — Disambiguate.** Ask:
1. Passport, ID-card, or both? (Both can be renewed in the same appointment.)
2. First-time or renewal? (First-time has age thresholds — 15 for ID-card; passport-required-age varies.)
3. Currently in Estonia or abroad? (If abroad: embassy flow; if in Estonia: PPA service point.)
4. Document validity status — current document still valid, expired by less than X months, expired by more than X months. (Affects whether you can renew online or must visit in person.)

**Section 4: Step 2 — Eligibility check.** Decision tree:
- Renewal of valid or recently-expired ID-card AND already have eID activation: typically eligible for "Renewal application via e-service" without an in-person visit.
- Renewal of an expired-too-long ID-card OR first issue OR passport (always in-person): in-person at PPA.
- Abroad: at Estonian embassy.
- A user under the relevant age (e.g. minor): special parental-consent rules — surface this and link to the live PPA page.

**Section 5: Step 3 — Photo requirements.** Pull from the live photo-specs page. Generate a checklist:
- Dimensions (35×45 mm) + confirm
- Recent (taken in last X months — verify)
- Background colour
- Face/expression rules
- File format / DPI if uploading digitally
- Where to take photos (most pharmacies, photo studios; some PPA offices have a photo booth)

**Section 6: Step 4 — Fee + processing time.** Fetch from live page:
- ID-card fee (urgency-tiered: standard vs. expedited)
- Passport fee (urgency-tiered)
- Combined renewal discount if applicable
- Processing time per option

Personalised total: based on user's choice (regular vs. expedited, just ID-card vs. just passport vs. both).

**Section 7: Step 5 — Booking availability lookup.** WebFetch the broneering.politsei.ee homepage. Parse: list of service points with their next-available appointment slot (if visible in the public listing). If only an interactive UI is exposed (and the public HTML doesn't show times), surface that the user needs to visit broneering.politsei.ee directly to see live slots — but at minimum identify the nearest PPA service point to the user's city.

**Section 8: Step 6 — If abroad, embassy lookup.** If the user said they're abroad, fetch the foreign-missions page and surface the nearest Estonian embassy in the user's country.

**Section 9: Step 7 — Pre-appointment checklist.** Output:
1. Photo per the requirements (or note where to take it)
2. Current ID document
3. Birth certificate (for first-time)
4. Application fee paid (or paid at the appointment — verify)
5. Other documents per PPA: name change documents if any, etc.

**Section 10: Auth seam.** "Now book your appointment at https://broneering.politsei.ee using your ID-card (or visit in person without booking, where available). For renewal-only via e-service: log in to the PPA e-service at politsei.ee and submit the renewal application. For abroad: schedule with the embassy identified above."

**Section 11: Sources.** Pointer.

- [ ] **Step 4: `references/sources.md`**

Template with verified URLs.

- [ ] **Step 5: Validate, regenerate, PII-check**

Expected: validates 8 skills.

- [ ] **Step 6: Commit**

```bash
git add skills/passport-or-idcard-renewal/ skills/estonia/INDEX.yaml
git commit -m "$(cat <<'EOF'
Add passport-or-idcard-renewal skill

Citizens/residents v0.2: passport, ID-card, or both renewal flow. Agent
checks eligibility, fetches current fees and processing times, verifies
photo requirements, looks up PPA service-point booking availability via
broneering.politsei.ee, and finds the nearest Estonian embassy if the
user is abroad. Auth seam at PPA appointment booking / e-service.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: `driving-licence` skill

**Files:**
- Create: `skills/driving-licence/SKILL.md`
- Create: `skills/driving-licence/references/sources.md`

The driving-licence skill is decision-tree-heavy: foreign-licence-exchange depends on the issuing country, applicant's residency status, and the licence category. **Authoritative agency: Transpordiamet.**

- [ ] **Step 1: Verify URLs**

Candidates:
- `https://www.transpordiamet.ee/juhilubade-asendamine` — foreign licence exchange overview
- `https://www.transpordiamet.ee/juhilubade-taotlemine` — first-time / renewal
- `https://www.transpordiamet.ee/en/driving-licences` — English overview if available
- `https://www.transpordiamet.ee/koolide-loetelu` — approved driving schools list (verify the canonical path)

- [ ] **Step 2: Create `skills/driving-licence/SKILL.md` — frontmatter**

```yaml
---
name: driving-licence
description: |
  Walks a citizen, resident, or new arrival through getting an Estonian
  driving licence. Covers first-time issuance, renewal, and exchange of
  a foreign driving licence (EU/EEA / bilateral-agreement countries /
  other). Use when the user mentions: "driving licence Estonia",
  "Estonian driving licence", "exchange foreign licence", "renew
  driving licence", "B-category", "Transpordiamet driving school",
  "driver's licence Estonia". Determines the right path via decision
  tree, lists current document requirements, surfaces approved driving
  schools, and computes fees from the live page.
license: MIT
allowed-tools: <PASTE TES BLOCK>
metadata:
  audience: "citizen,resident,expat-newcomer"
  life_event: "vehicle"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "<URL_1>|<URL_2>"
  last_verified: "2026-05-05"
  version: "0.1.0"
---
```

- [ ] **Step 3: Write the body**

Style reference: `residence-registration` skill (decision tree).

**Section 1: Disclaimer.** AI guidance, not driving instruction. Transpordiamet decides licensing eligibility; this skill helps you prepare.

**Section 2: Freshness obligation.** List verified URLs.

**Section 3: Step 1 — Disambiguate via decision tree.**

**Q1: What's your situation?**
- First-time applicant in Estonia → Step 2A.
- Renewing an Estonian driving licence → Step 2B.
- Exchanging a foreign driving licence → Q2.

**Q2: Where was your foreign licence issued?**
- EU / EEA / Switzerland → typically free swap, no test required (verify against live page; the rules can change).
- A country with a bilateral agreement (Japan, Korea, others — verify the live list at transpordiamet.ee) → swap with theory test, no practical.
- Other countries (most non-EU without agreement) → re-take theory + practical tests; existing licence is recognised for some grace period (verify) for driving in Estonia.

**Q3: Are you a resident in Estonia (registered place of residence)?** Foreign-licence exchange typically requires Estonian residency to be on file. If not, the user may need to do the residence-registration skill first.

**Section 4: Step 2A — First-time applicant flow.**
Walk through:
1. Driving school enrolment — fetch the approved-school list from transpordiamet.ee koolide-loetelu page; surface 2-3 schools near the user's city. Alternative: self-study with a private instructor (if allowed).
2. Theory exam at Transpordiamet (book online).
3. Practical exam at Transpordiamet (book online).
4. Medical certificate (peresemena pharmacy or family doctor; verify).
5. Application fee at Transpordiamet.
6. Document collection at the service point.

**Section 5: Step 2B — Renewal flow.**
Renewal is usually a simpler online flow. Eligibility:
- Standard renewal before expiry → online via Transpordiamet e-service.
- Late renewal (after expiry) → may require re-test depending on how long it expired (verify).
- Health certificate may be required for older drivers (age threshold — verify).

**Section 6: Step 2C — Foreign-licence exchange flow.**
Per Q2 result, walk through:
- Documents required: foreign licence, ID, residence proof, photo, fee, sometimes a translated/apostilled copy of the foreign licence.
- Theory exam (if applicable).
- Practical exam (if applicable).
- Application at Transpordiamet.

**Section 7: Step 3 — Generate document checklist.** Personalised based on which path the user is on. Include the medical certificate where needed; surface the family-doctor channel if the user doesn't have one.

**Section 8: Step 4 — Fee summary.** Pull current fees from the live page: theory exam, practical exam, application fee, licence card fee. Sum the user's expected total.

**Section 9: Auth seam.** "Now book your exam slots and submit the application via the Transpordiamet e-service at https://www.transpordiamet.ee using your Smart-ID, Mobile-ID, or ID-card. After passing exams, collect your licence at the service point or via mail."

**Section 10: Sources.** Pointer.

- [ ] **Step 4: `references/sources.md`**

Template with verified URLs.

- [ ] **Step 5: Validate, regenerate, PII-check**

Expected: validates 9 skills.

- [ ] **Step 6: Commit**

```bash
git add skills/driving-licence/ skills/estonia/INDEX.yaml
git commit -m "$(cat <<'EOF'
Add driving-licence skill

Citizens/residents v0.2: first-time issuance, renewal, or exchange of
a foreign driving licence at Transpordiamet. Decision tree branches
on the user's situation (first-time / renewal / EU-EEA exchange /
bilateral-agreement exchange / other). Surfaces approved driving
schools, document requirements, and current fees. Auth seam at
Transpordiamet e-service.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Final v0.2 verification

- [ ] **Step 1: Full validator run**

```bash
. .venv/bin/activate
pytest -v
python scripts/validate_frontmatter.py
python scripts/build_index.py
git diff --exit-code skills/estonia/INDEX.yaml
python scripts/check_no_pii.py
```
Expected: 22/22 tests pass; validates **9 skills** (router + 3 v0.1 + 5 v0.2); INDEX in sync; PII clean.

- [ ] **Step 2: Confirm INDEX.yaml shape**

```bash
cat skills/estonia/INDEX.yaml | head -50
```
Expected: lists 8 atomic skills (the router itself is excluded), sorted by name:
1. `driving-licence`
2. `ou-open-e-resident`
3. `parental-benefit-vanemahuvitis`
4. `passport-or-idcard-renewal`
5. `residence-registration`
6. `tax-filing-individual`
7. `tootukassa-unemployment`
8. `vehicle-transfer`

- [ ] **Step 3: List commits**

```bash
git log --oneline feature/v1-implementation | head -15
```
Expected: 7 v0.2 commits on top of the v0.1 + agentic + TES history.

- [ ] **Step 4: Smoke-test in a fresh Claude Code session (manual, no automation)**

Have the user run:
```
/plugin uninstall estonia-skills@estonia-skills
/plugin install estonia-skills@estonia-skills
/reload-plugins
```

Then test prompts that exercise each new skill:
1. *"My partner and I are expecting; what will I get for parental benefit if my gross salary last year was €X?"* → triggers `parental-benefit-vanemahuvitis`. Confirm: agent fetches sotsiaalkindlustusamet.ee, computes estimate, surfaces split-timing options.
2. *"I'm buying a car in Tallinn, registration number 123ABC. What do I need to do?"* → triggers `vehicle-transfer`. Confirm: agent does live insurance lookup at lkf.ee, surfaces fees and checklist.
3. *"I just got laid off; how do I register at Töötukassa?"* → triggers `tootukassa-unemployment`. Confirm: agent walks through eligibility tree, computes benefit estimate.
4. *"My passport expires in 3 months; how do I renew?"* → triggers `passport-or-idcard-renewal`. Confirm: agent verifies photo specs, fetches fees, surfaces booking-availability link.
5. *"I have a French driving licence and just moved to Estonia; do I need to do anything?"* → triggers `driving-licence`. Confirm: agent decision-trees to "EU/EEA → free swap" path.

For each, confirm there's no permission prompt for any TES domain.

---

## Self-Review

**1. Spec coverage:** All five approved skills have a dedicated task (2-6); the TES allowlist extension is its own task (1) so all skills get the new domains; final verification (7) ensures the project ships in a publishable state.

**2. Placeholder scan:** Frontmatter snippets contain `<URL_1>|<URL_2>` and `<PASTE THE TES BLOCK>` — these are intentional substitution points the implementer fills in after Step 1 (URL verification) and Step 2 (TES extension) respectively. They are not "TODO" placeholders; they are explicit references to outputs of named earlier steps in the same plan. Body sections describe specific computation logic, decision-tree branches, and documents to generate — not vague "add appropriate handling."

**3. Type / name consistency:** Skill directory names match SKILL.md `name:` fields exactly. The TES block in CONTRIBUTING.md is the single source of truth pasted into every `allowed-tools`. The `last_verified: "2026-05-05"` date is consistent across all five new skills. INDEX.yaml will list 8 atomic skills sorted alphabetically (with `parental-benefit-vanemahuvitis` between `ou-open-e-resident` and `passport-or-idcard-renewal`); validate_frontmatter validates 9 (router included).

**Deviation from strict no-placeholder rule (intentional):** Section bodies prescribe what each section *must do* (questions to ask, computations to perform, documents to generate) rather than the exact prose. The implementer composes prose around these instructions, using the three v0.1 skills as style references. Justification: with patterns now mature in CONTRIBUTING.md, dictating prose verbatim for five additional ~150-line skill bodies would bloat the plan without adding meaningful guidance — and would constrain implementers from fixing things they discover during URL verification (e.g., a freshness URL turns out to require different framing in Step 4). Spec compliance reviewer enforces section presence and content shape per task.
