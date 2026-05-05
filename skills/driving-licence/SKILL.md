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
  freshness_sources: "https://www.transpordiamet.ee/juhiluba|https://www.transpordiamet.ee/valisriigi-juhiluba"
  last_verified: "2026-05-05"
  version: "0.1.0"
---

# Driving licence

## Disclaimer

This is AI-generated procedural guidance, not driving instruction or legal advice. The Estonian Transport Administration (Transpordiamet) is the authoritative decision-maker for driving-licence eligibility, exam content and pass criteria, document requirements, and acceptance of foreign licences — this skill helps you prepare your application and surfaces the live procedure, but does not substitute for Transpordiamet's review or for accredited driving instruction. For non-routine cases (medical exemptions, restricted right to drive after revocation, professional categories C/D/E, internationally adopted minors, drivers with foreign licences from countries not mapped to a recognised treaty list), follow Transpordiamet's specific procedure for that path or contact their helpline. This repository is not affiliated with the Republic of Estonia or Transpordiamet.

## Freshness obligation

**Before quoting any fee, eligibility threshold, age limit, exam pass criterion, document requirement, residency-day count, or grace period, fetch the current pages at:**

- `https://www.transpordiamet.ee/juhiluba` (Estonian first-time issuance, renewal, replacement, validity, medical certificate)
- `https://www.transpordiamet.ee/valisriigi-juhiluba` (foreign-licence exchange — EU/EEA/Switzerland, 1968 Vienna Convention countries, 1949 Geneva Convention countries, other countries; Ukrainian temporary-protection special provisions)

**Do not quote any number from this skill body.** Numbers, treaty-country lists, and rule descriptions below are illustrative only — always replace them with what the live Transpordiamet pages currently say. State fees, exam fees, validity windows, the list of countries on each treaty branch, the residency-day threshold, and the post-expiry re-test cut-off all change. Re-fetch each time.

When the user is exchanging a non-EU foreign licence, also fetch the current treaty-country lists from the live page (the page lists Vienna Convention countries and Geneva Convention countries inline, and the lists change when treaties are updated). When the user wants to pick a driving school, also fetch `https://www.transpordiamet.ee/autokoolide-statistika` (approved schools and exam pass-rate statistics).

## Step 1 — Disambiguate via decision tree

Walk the user through the minimum questions in this order:

**Q1: What's your situation?**
- **First-time applicant in Estonia** (you've never held a driving licence anywhere) → go to Step 2A (Section 4).
- **Renewing an Estonian driving licence** (you currently hold or recently held an Estonian licence) → go to Step 2B (Section 5).
- **Exchanging a foreign driving licence** (you hold a valid licence issued by another country) → go to Q2.

**Q2 (foreign-licence exchange): Where was your foreign licence issued?**
- **EU / EEA member state, or Switzerland** → typically a swap without theory or practical test, provided the licence is still valid (or hasn't been expired beyond the live cut-off) and you meet the Estonian residency requirement. Verify the current rule, the validity-of-expired-licence window, and any category-specific exceptions on the live page.
- **A country signed up to the 1968 Vienna Convention on Road Traffic, or to the 1949 Geneva Convention on Road Traffic** → exchange procedure with documentary translation requirements; categories A/B are commonly exchanged without a practical exam, with theory required for some sub-cases. Other categories require testing. The live page lists the countries on each branch and the per-category rules — verify, the lists do change.
- **Any other country** (no recognised treaty) → exchange requires both theory and practical exams; until the exchange is complete, the foreign licence is recognised for driving in Estonia for a limited window after you establish residency (verify the current window).
- **Special case: Ukrainian licence under temporary-protection status** → re-fetch the special provisions on the live page; Ukrainian licences under TP have historically been recognised without exchange or translation for the duration of the protection. Do not assume — verify.

**Q3: Are you a resident in Estonia (registered place of residence)?**
- Foreign-licence exchange typically requires you to be a permanent resident in Estonia, often with at least the live page's required number of residency days per year. Verify on the live page.
- If the user has not yet registered their place of residence in the population register → route them to the `residence-registration` skill first; the exchange application cannot be filed without residence on file.

State the result back to the user explicitly: "Based on what you've described, your path is **[Step 2A first-time / Step 2B renewal / Step 2C exchange — EU branch / Vienna branch / Geneva branch / other branch]**. Here's what that path looks like next." Then proceed.

## Step 2A — First-time applicant flow

For someone who has never held a driving licence, the Estonian process is sequential and gated by exams and the medical certificate. Walk the user through:

1. **Driving school enrolment.** Fetch `https://www.transpordiamet.ee/autokoolide-statistika` for the official list of driving schools (autokoolid) holding a current operating licence, plus the exam-pass-rate statistics for each. If the user names their city, surface 2–3 schools nearby with their pass-rate ranking. Self-study with a private instructor is permitted for some categories (verify the per-category rules and the requirements for the supervising-driver) — but most first-time B-category applicants go through an autokool because the sequence of theory, traffic-safety, and behind-the-wheel hours is mandated.
2. **Theory exam at Transpordiamet.** Booked online via the Transpordiamet e-service after the driving school confirms the user has completed the required theory hours. Verify the current pass criteria, allowed re-take cadence, and the language options (Estonian / Russian / English — the language list shifts).
3. **Practical (driving) exam at Transpordiamet.** Booked after passing theory and completing the driving school's practical hours. Verify the current pass criteria and re-take rules.
4. **Medical certificate (tervisetõend).** Issued by the user's family doctor (perearst) — covers eyesight, general fitness to drive, and any category-specific medical conditions. Some pharmacies and private clinics also issue the certificate; verify which on the live page. The certificate is uploaded to the population-register / health-data system; Transpordiamet pulls it from there at application time. The user does not bring a paper certificate to the appointment in most cases — verify.
5. **State fee for the driving licence.** Paid online or at the service point; verify the current rate on the live page.
6. **Document collection.** After both exams are passed and the application is approved, the licence is issued. Verify whether the current default is in-person collection at a Transpordiamet service point, postal delivery, or both, and whether there is a delivery-method differential in the fee.

Surface the sequence so the user understands they cannot skip steps — the exam booking is gated by the school's confirmation, the practical exam is gated by passing theory, and issuance is gated by the medical certificate being on file.

## Step 2B — Renewal flow

For someone whose Estonian licence is approaching expiry or has recently expired:

- **Standard renewal before expiry.** Filed online via the Transpordiamet e-service. The user authenticates with eID (Smart-ID, Mobile-ID, or ID-card), confirms data, uploads a current document photo if required, and pays the state fee. A new card is issued and delivered. Verify the current self-service eligibility window (some categories or older drivers may be excluded from the simplified flow).
- **Late renewal (after expiry).** Whether re-testing is required depends on how long the licence has been expired. The live page defines the cut-off — re-fetch. Below the cut-off the renewal proceeds as a standard renewal with a possible surcharge; above the cut-off the user may need to re-take theory and/or practical exams.
- **Health certificate at renewal.** A medical certificate may be required — universally for some categories (e.g. professional C/D/E), and from a specific age threshold for B-category. The age threshold and the recurrence interval (e.g. every 5 years from age X) change — verify. The certificate routing is the same as in Step 2A: family doctor (or pharmacy / clinic alternative if surfaced on the live page), uploaded to the health-data / population-register system, pulled by Transpordiamet at application time.
- **Photo.** Verify whether the live page requires a fresh document photo at renewal or accepts the existing one on file. Photo specs follow the Estonian biometric-document standard; pharmacies and photo studios in Estonia provide compliant photos.
- **State fee.** Verify the current rate on the live page.

## Step 2C — Foreign-licence exchange flow

The exchange flow varies by the Q2 branch. Common sub-flow:

**Documents typically required (verify per branch on the live page):**
- The original foreign driving licence.
- Proof of identity (Estonian ID-card or passport; foreign passport for newcomers).
- Proof of registered place of residence in Estonia (pulled from the population register at application time).
- A current document photo.
- Application state fee (verify the current rate).
- For non-Latin-script licences (e.g. issued in Cyrillic, Arabic, or Asian scripts): an **official translation** of the licence into Estonian or English, often by a sworn translator. Some branches additionally require an apostille or consular legalisation of the original licence — verify per source country on the live page.
- Medical certificate (same channel as Step 2A — family doctor, uploaded to the system).

**Exam requirements by Q2 branch (verify on the live page; rules drift):**
- **EU / EEA / Switzerland branch:** typically no theory and no practical exam.
- **1968 Vienna Convention branch:** exchange usually with no exam for A/B categories, but some sub-cases require a theory exam. Higher categories require testing.
- **1949 Geneva Convention branch:** similar to Vienna in structure but with stricter conditions on some categories — verify.
- **Other countries (no treaty):** both theory and practical exams required, equivalent to Step 2A from the exam-booking step onward.

**Application channel:** the exchange application is filed at a Transpordiamet service point (in person) or via the e-service if the live page allows it for the user's branch — verify. Booking is via the Transpordiamet booking system.

**Grace period for driving while exchange is pending:** the foreign licence is recognised for driving in Estonia for a limited window after the user establishes residency. The window length differs by Q2 branch (typically longer for EU/EEA/Switzerland, shorter for non-treaty countries). Verify the current window before quoting it to the user.

## Step 3 — Generate document checklist

Output a checklist tailored to the user's path. Examples — adapt to the user's branch and omit items that don't apply:

```
Documents and items you'll need:

ALWAYS:
1. Estonian ID-card or passport (proof of identity).
2. Means to pay the state fee (card payment in person, or online via the
   Transpordiamet e-service).
3. A current document photo per the Estonian biometric standard
   (verify on the live page; pharmacies and photo studios provide compliant
   photos). Some flows let the photo be uploaded in advance via the e-service.

IF FIRST-TIME APPLICANT (Step 2A):
4. Driving school enrolment confirmation (the school files the
   completion record electronically with Transpordiamet — bring the
   reference if asked).
5. Medical certificate (issued by your family doctor, uploaded to the
   health-data system; not a paper document in most cases — verify).

IF RENEWAL (Step 2B):
6. The expiring or recently-expired Estonian driving licence.
7. Medical certificate if required for your age and category (verify on
   the live page).

IF EXCHANGING A FOREIGN LICENCE (Step 2C):
8. The original foreign driving licence.
9. Proof of registered place of residence in Estonia (pulled
   automatically from the population register; if not yet registered,
   complete residence registration first).
10. For non-Latin-script licences: an official translation of the
    licence into Estonian or English (sworn translator).
11. For some non-EU branches: an apostille or consular legalisation
    of the original licence — verify per source country.
12. Medical certificate (same channel as Step 2A).

IF YOU DON'T HAVE A FAMILY DOCTOR YET:
- Estonian residents are entitled to register with a family doctor (perearst)
  via Tervisekassa. The medical certificate can also be issued by some
  pharmacies and private clinics — verify on the live page which channels
  are accepted by Transpordiamet for driving-licence purposes.
```

Tailor the output: don't list driving-school enrolment for a renewal; don't list a translation requirement for an EU licence; don't list an expiring Estonian licence for a first-time applicant.

## Step 4 — Fee summary

Fetch the relevant Transpordiamet pages and extract the current published rates for:

- **Theory exam fee** (per attempt; re-take fee may differ).
- **Practical (driving) exam fee** (per attempt; re-take fee may differ).
- **Driving-licence state fee** (issuance / renewal — may differ by speed of issuance and delivery method).
- **Licence card fee** (sometimes bundled into the state fee, sometimes separate — verify).
- **Driving-school course fee** (set by the school, not by Transpordiamet — typical range varies widely; surface that this is school-set, not state-set, and direct the user to the autokool's price list).
- **Medical-certificate fee** (set by the issuing doctor / clinic / pharmacy, not by Transpordiamet).

Compute a personalised expected total based on the user's path:

> "Your situation: **[first-time B-category / renewal / EU exchange / Vienna exchange / Geneva exchange / other exchange]**.
>
> - Theory exam: €X (per attempt)
> - Practical exam: €Y (per attempt; only if your branch requires it)
> - Driving-licence state fee: €Z
> - **Subtotal of state fees: €T**
> - Plus driving school: €S (school-set; verify with your chosen autokool)
> - Plus medical certificate: €M (clinic-set)
> - **Estimated grand total: €(T + S + M)**, assuming you pass both exams on the first attempt."

Surface that re-take fees apply if the user fails an exam; the all-in cost grows fast on multiple re-takes.

## Step 5 — Auth seam

> Now book your exam slots and submit the application via the Transpordiamet e-service at `https://www.transpordiamet.ee` using your **Smart-ID**, **Mobile-ID**, or **ID-card**. The e-service routes you to the relevant flow:
>
> - **First-time applicant:** book the theory exam after your driving school marks your theory hours complete; book the practical exam after passing theory.
> - **Renewal:** the e-service pre-fills your data from the population register and the renewal is filed entirely online for most categories.
> - **Foreign-licence exchange:** the e-service collects the application; depending on your branch you may also need to attend a Transpordiamet service point with the original foreign licence and any translation / apostille documents.
>
> After you pass the exams (where applicable) and the application is approved, collect your driving licence at the Transpordiamet service point you selected, or via mail if your branch supports postal delivery. Verify the current delivery options on the live page.

After login, do not narrate the in-portal experience — the user is in a controlled flow with Transpordiamet, and that flow is authoritative.

Note on auth: ID-card with valid certificates, Mobile-ID, and Smart-ID are all generally accepted for Transpordiamet e-services; verify on the login page before promising the user any specific method will work for their flow.

## Sources

See `references/sources.md`.
