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
  audience: "citizen,resident,expat-newcomer"
  life_event: "vehicle"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://transpordiamet.ee/en/vehicle-ship-airplane/vehicle/registration-vehicle|https://www.lkf.ee/et/kindlustusekehtivus|https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud/mootorsoidukimaks"
  last_verified: "2026-05-05"
  version: "0.1.0"
---

# Vehicle transfer (buying or selling a vehicle in Estonia)

## Disclaimer

This is AI-generated procedural guidance, not legal advice. The estimates this skill produces (fees, taxes, insurance) are illustrative — the authoritative state of the vehicle (its registered owner, its outstanding tax, its insurance, its MOT validity) is whatever Transpordiamet, the Liikluskindlustuse Fond (LKF), and Maksu- ja Tolliamet (EMTA) currently show in their registries. For disputes about a vehicle's history (undisclosed damage, encumbrances, leasing claims, odometer fraud), use a vehicle-history professional service or a lawyer; this skill cannot substitute for a paid background check. This repository is not affiliated with the Republic of Estonia, the Transport Administration, the Traffic Insurance Fund, or the Tax and Customs Board.

## Freshness obligation

**Before quoting any state fee, tax rate, insurance premium, or processing time, fetch the current pages at:**

- `https://transpordiamet.ee/en/vehicle-ship-airplane/vehicle/registration-vehicle` — Transpordiamet vehicle-registration overview (links into the e-service for transfers and MOT lookups)
- `https://www.lkf.ee/et/kindlustusekehtivus` — Liikluskindlustuse Fond (LKF) public lookup of traffic-insurance validity by registration number, VIN, or policy number
- `https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud/mootorsoidukimaks` — EMTA motor vehicle tax (mootorsõidukimaks / automaks), in force since 1 January 2025

**Do not quote any fee, tax rate, or insurance premium from this skill body.** Numbers below are illustrative only — always replace them with what the live pages currently say. Estonia introduced the motor vehicle tax (`automaks`) on 1 January 2025; rates and the registration-fee schedule have been revised more than once since, so cached numbers age fast.

## Step 1 — Disambiguate

Ask the minimum needed, in this order. Don't skip any of these — each answer changes which sub-flow runs.

1. **Buying or selling?** "Are you the buyer or the seller in this transaction?" The buyer pays the transfer fee, arranges new insurance, and inherits the automaks obligation; the seller's job is mostly to confirm identity and sign the transfer. The checklist in Step 4 differs.
2. **Vehicle category.** "What kind of vehicle — passenger car (M1), van or light truck (N1), motorcycle, moped, trailer, or something else?" Different categories have different MOT cadences, insurance pricing bands, and (since 2025) different automaks formulas. Some categories — e.g. mopeds and certain trailers — are registered but exempt from automaks; check the current EMTA page.
3. **Has the vehicle been registered in Estonia before, or is it being imported?** "Is this a vehicle already in the Estonian traffic register, or is it being brought in from abroad (EU or outside EU)?" Imports add steps: customs clearance (only for non-EU imports), type-approval / EU conformity check, possibly a one-off Estonian roadworthiness inspection before first registration.
4. **Does the user have an Estonian eID?** "Do you have a Smart-ID, Mobile-ID, or ID-card?" Most of the transfer flow runs through the Transpordiamet e-service and requires eID. If not, the same actions can be done in person at a Transpordiamet service bureau on paper, but the user has to physically attend; surface that as a fallback.

**Never ask for the user's isikukood, bank account, IBAN, passport number, or driving-licence number.** The registration number of the vehicle is fine — it's publicly displayed on the plate and treat it like a domain name, not personal data.

## Step 2 — Live status checks

Once the vehicle category is known and the vehicle is already in the Estonian register, ask the user for the registration number (e.g. `123ABC`). Then run these lookups in parallel:

1. **Insurance status (LKF).** WebFetch `https://www.lkf.ee/et/kindlustusekehtivus` and submit the registration number (or VIN, if the user has it). Parse the response:
   - **Insured today?** Yes / No.
   - **Policy expiry date.**
   - **Insurer name** (if surfaced).
   Surface all three to the user. If the policy expires within 14 days, flag it; if it has already lapsed, flag that loudly — driving an uninsured vehicle on Estonian roads carries fines and the buyer cannot drive it home until a new policy is bound.

2. **MOT (tehnoülevaatus) status.** WebFetch the Transpordiamet vehicle history / MOT lookup. The entry-point is via the e-service from `https://transpordiamet.ee/en/vehicle-ship-airplane/vehicle/registration-vehicle`; if the page links to a vehicle-history check (`soidukTaustakontroll`), use that. Parse:
   - **MOT current?** Yes / No.
   - **MOT expiry date.**
   - **Next-due date.**
   If MOT is expired, the buyer cannot legally drive the vehicle on public roads until it passes a new inspection — surface the cost of the inspection (fetch the current fee from the Transpordiamet page) as part of the buyer's first-year cost.

3. **Registration ownership.** Note explicitly: the public Transpordiamet lookup does **not** typically expose the current owner's name (that's privacy-protected). The buyer learns the seller's identity from the seller and verifies it at the moment of transfer — the seller logs into the Transpordiamet e-service with their own eID and initiates the transfer; the registry confirms identity by the eID, not by manually-entered name. Don't try to scrape an owner name out of the public registry.

If any of insurance, MOT, or seller-side eID is missing or expired, surface as a **buyer's-due-diligence flag** before proceeding to fees:

> Flagging for the buyer: [vehicle] currently has [insurance lapsed / MOT expired on Y / seller does not have eID]. This doesn't block the sale, but it changes the cost structure and the timing — see Step 3.

## Step 3 — Compute fees

Pull current values from the live pages — never quote any cached number from this body.

1. **Transfer state fee.** Fetch the current transfer / re-registration fee from the Transpordiamet page. Different categories pay different fees; the e-service usually shows the exact fee at the moment of transfer.
2. **Annual motor vehicle tax (automaks / mootorsõidukimaks).** Fetch the formula from the EMTA page. The tax depends on the vehicle's CO₂ emissions, mass, age, and category. Apply the formula to the user's vehicle and surface the annual amount. **Pro-rata note:** automaks applies to whoever is the registered owner on the assessment date(s) — confirm the current EMTA rule for mid-year transfers (typically the new owner pays from the first full month of ownership; verify on the live page).
3. **Insurance premium estimate.** The LKF lookup may show an indicative minimum premium; the actual premium depends on the chosen insurer, the buyer's no-claims history, the vehicle, and any optional kasko add-ons. Surface the LKF indicative figure as a *floor*, not a binding quote, and tell the user to compare 2–3 insurers before binding.

**Sum up the buyer's first-year cost** (illustrative formula — substitute live numbers):

```
First-year buyer cost ≈ transfer_fee + automaks_for_full_year + cheapest_traffic_insurance_for_full_year
                         (+ MOT inspection fee, if MOT has expired)
                         (+ customs and type-approval, if imported from outside the EU)
```

Show the breakdown explicitly so the user sees each component, then the total.

## Step 4 — Generate the transfer checklist

Output a personalised checklist. Adjust the items that depend on Step 1 answers (buyer vs. seller, eID vs. paper, domestic vs. import) — don't ship a generic boilerplate. Format:

```
Transfer checklist for [buyer / seller] of [vehicle category, reg. NNN]:

BEFORE TRANSFER:
- [ ] Confirm the seller's identity matches the registered owner (the e-service does this automatically when the seller logs in)
- [ ] Confirm the vehicle has valid traffic insurance through at least the transfer day
- [ ] Confirm MOT (tehnoülevaatus) is current — or factor in the cost to renew (€[from live page])
- [ ] Inspect the vehicle in person (or have it inspected by a professional service)
- [ ] Agree on price and payment method in writing (a short bill-of-sale protects both parties even though the registry transfer is the legally operative step)

AT TRANSFER:
- [ ] Both buyer and seller log in to the Transpordiamet e-service
- [ ] Seller initiates the transfer in the e-service; buyer accepts
- [ ] Buyer pays the transfer state fee (€[from live page]) inside the same flow
- [ ] Buyer arranges new traffic insurance — the policy must be active before the buyer drives the vehicle away

AFTER TRANSFER:
- [ ] Confirm the new automaks (motor vehicle tax) registration in e-MTA — EMTA picks up the change from the traffic register, but verify the tax notice arrives correctly
- [ ] Update or replace the insurance policy if the buyer's insurer or terms differ from the prior policy
- [ ] Diary the next MOT (tehnoülevaatus) date so it doesn't lapse
- [ ] (If imported from outside the EU) confirm customs clearance is complete and the vehicle has Estonian-issued plates
```

This checklist is the tangible artifact the user takes into the e-service. Each item should be one action the user can complete or verify in a single sitting.

## Step 5 — Auth seam

> Now log in to the **Transpordiamet e-service** (entry point at `https://transpordiamet.ee/en/vehicle-ship-airplane/vehicle/registration-vehicle`) using your **Smart-ID, Mobile-ID, or ID-card**. Both parties — the buyer and the seller — sign the transfer in the e-service; the buyer pays the state fee in the same flow. Before the buyer drives the vehicle away, a new traffic-insurance policy must be active (any Estonian insurer can bind one online). After the transfer is registered, EMTA will update the automaks record automatically and the next tax notice will be issued to the new owner.

After login, do not narrate the in-portal experience — the user is authenticated and the e-service itself guides them through identity confirmation, signature, and payment.

## Sources

See `references/sources.md`.
