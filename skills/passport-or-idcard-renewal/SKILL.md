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
  life_event: "meta"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.politsei.ee/en/instructions/estonian-passport-for-an-adult|https://www.politsei.ee/en/instructions/applying-for-an-id-card-for-an-adult|https://www.politsei.ee/en/requirement-and-instructions-for-the-document-photo"
  last_verified: "2026-05-05"
  version: "0.1.0"
---

# Passport or ID-card renewal

## Disclaimer

This is AI-generated procedural guidance, not legal advice. The Estonian Police and Border Guard Board (Politsei- ja Piirivalveamet, PPA) is the authoritative decision-maker for identity-document eligibility, fees, processing times, and acceptance of supporting documents — this skill helps you prepare your application and surfaces the live procedure, but does not substitute for the PPA's review. For non-routine cases (name change tied to civil-status events still pending in another jurisdiction, lost-document reports, dual citizenship questions, applications under emergency travel-document procedures, applications for an alien's passport rather than an Estonian citizen's passport, or applicants with disabilities entitled to a state-fee discount), follow the PPA's procedure for that specific path or contact the PPA helpline. This repository is not affiliated with the Republic of Estonia or the PPA.

## Freshness obligation

**Before quoting any fee, processing time, photo dimension, age threshold, or eligibility cut-off, fetch the current pages at:**

- `https://www.politsei.ee/en/instructions/estonian-passport-for-an-adult`
- `https://www.politsei.ee/en/instructions/applying-for-an-id-card-for-an-adult`
- `https://www.politsei.ee/en/requirement-and-instructions-for-the-document-photo`

**Do not quote any number from this skill body.** Numbers below are illustrative only. Always replace them with what the live PPA pages currently say. Document fees, expedited-procedure surcharges, photo dimensions, and processing-time SLAs change repeatedly: the state-fee schedule was last revised on 1 January 2025, and the photo-specs page is under separate version control from the document-application pages. Re-fetch each time.

When the user is applying for a child's document or under a discounted category, also fetch the relevant variant page (`/instructions/estonian-passport-for-a-child`, `/instructions/applying-for-an-id-card-for-a-child`, or the disability-discount section of the state-fee page).

## Step 1 — Disambiguate

Ask the minimum needed, in this order:

1. **Which document?** "Are you applying for a passport, an ID-card, or both at the same appointment?" Both can be applied for or renewed in a single appointment; the PPA will accept one set of biometrics for both. Note that for some flows (e.g. ID-card-only renewal via the self-service portal), in-person attendance is not required at all.
2. **First-time or renewal?** "Is this your first ever Estonian passport / ID-card, or a renewal of one you've held before?" First-time applications have age thresholds (an ID-card is compulsory for Estonian citizens residing in Estonia from a specific age — verify the current threshold live; passport-required age varies). Renewals of recently-expired or still-valid documents may qualify for the self-service renewal route.
3. **Currently in Estonia or abroad?** "Are you in Estonia, or outside Estonia for the application?" Inside Estonia → PPA service office or self-service portal. Abroad → Estonian foreign representation (embassy or consulate that issues documents). Honorary consuls accept some passport categories but not always ID-card / digital ID applications — verify per-country.
4. **Document validity status.** "What's the status of your current document — still valid, expired recently, expired some time ago, lost, or stolen?" Lost / stolen documents have a separate reporting flow (declare invalid first); long-expired documents may not qualify for the simplified self-service renewal route.

**Never ask for the user's isikukood, current document number, or biometric data.** They volunteer their city / country if they want a service-point lookup or embassy pointer; they volunteer document type and renewal-vs-first if they want a personalised fee estimate. Nothing else is required.

## Step 2 — Eligibility decision tree

Apply the answers from Step 1 against the live procedure (re-fetch — the simplified renewal path is governed by parameters that have shifted as the eID stack matured):

**Branch A — ID-card renewal via the self-service portal (no in-person visit):**
- The applicant is renewing an ID-card (not a passport, and not a first-time ID-card), AND
- The current or recently-expired ID-card is on file at the PPA, AND
- The applicant has working eID authentication (a valid certificate on a current ID-card, Mobile-ID, or — verify acceptance — Smart-ID), AND
- The previous fingerprints are still valid (historically the PPA reuses fingerprints captured within a defined window — verify the current validity window on the live page; persons over a certain age are exempt from the fingerprint requirement entirely).
- → **Likely eligible** for self-service renewal. The application is filed at the PPA self-service portal; the new card is delivered by post or to a chosen pickup point (PPA office or — as of January 2025 — selected Selver stores at a lower pickup fee).

**Branch B — In-person at a PPA service office:**
- Passport applications (always require in-person attendance for fingerprints, unless fingerprints on file are still valid and the live page explicitly allows portal-only passport renewal — verify), OR
- First-time ID-card applications, OR
- ID-card renewal where the current ID-card has been expired beyond the simplified-renewal window, OR
- The applicant lacks working eID authentication, OR
- Reporting and replacing a lost / stolen / damaged document.
- → **Apply at a PPA client service office.** Booking strongly recommended (use `https://broneering.politsei.ee/`); some offices also serve walk-ins on a queue-ticket basis (`https://mobiilnepilet.politsei.ee/`).

**Branch C — From abroad, at an Estonian foreign representation:**
- The applicant is currently outside Estonia.
- → **Apply at the nearest Estonian embassy / consulate that issues documents.** See Step 6 for the lookup. Note: honorary consuls handle some passport applications but not all document types; verify per-country.

**Branch D — Minor (under 18) applying:**
- Parental-consent rules apply. Both legal representatives must consent unless one has sole custody. The parental signature is captured at the appointment. Surface this explicitly so the parent doesn't show up alone with the child and get sent home.

State the result back: "Based on what you've described, you qualify for **[Branch X]**. Here's what that path looks like next." Then proceed to Steps 3–7 with the appropriate variant.

## Step 3 — Photo requirements

Fetch `https://www.politsei.ee/en/requirement-and-instructions-for-the-document-photo` and produce a checklist tailored to the user's situation. The page distinguishes adult requirements from young-children (0–7) requirements — pull the right section.

```
Document-photo checklist (re-verify each item from the live page):

DIMENSIONS
- Minimum pixel dimensions (live page; historically a few-megapixel requirement)
- Physical dimensions when printed (commonly 35 × 45 mm — verify)
- File size range (commonly 1–5 MB — verify)
- File format (commonly JPG; uneditied original — verify)

RECENCY
- Self-taken photos no older than the live limit (historically 6 months)
- Booth photos valid within the booth-imposed limit (historically 183 days)

BACKGROUND
- Light and uniform, single colour, no extraneous objects

FACE / EXPRESSION
- Looking straight into the camera
- Eyes level, both visible, no obstruction (glasses with reflections / heavy frames are problematic)
- Mouth closed (children especially)
- No headwear except for verified religious / medical reasons documented separately

WHAT'S NOT ACCEPTED
- Scanned photographs
- Screenshots
- Edited / retouched / filtered images
```

**Where to take the photo:**
- Most pharmacies and photo studios in Estonia provide compliant photo booths; they print and provide the digital file matching PPA specs.
- Some PPA service offices have an on-site photo booth (verify per office on the live page).
- For abroad: most countries have photo studios that can produce ICAO-compliant biometric photos meeting Estonian PPA specs — the photo specs are an international standard; the dimensions and file-size are the only Estonian-specific aspects to confirm.

If the user is filing the self-service renewal, the photo is uploaded as a file. If filing in person, they can either upload the file in advance via the portal or bring a printed photo to the appointment.

## Step 4 — Fee + processing time

Fetch the relevant document page(s) and the state-fee page (`https://www.politsei.ee/en/instructions/state-fee-amounts`) and extract:

- **ID-card state fee — standard procedure** (current published rate)
- **ID-card state fee — expedited procedure** (substantially higher than standard — verify)
- **Passport state fee — standard procedure** (current published rate; differs from ID-card)
- **Passport state fee — expedited procedure**
- **Discount categories** (e.g., persons with a moderate / severe / profound disability; pensioners on certain pages — verify)
- **Foreign-representation surcharge** (applying abroad typically costs more than in Estonia — verify)
- **Self-service portal vs. service-office state-fee differential** (the portal is sometimes discounted — verify)
- **Pickup fee** (delivery method affects total: PPA office pickup, postal delivery, Selver-store pickup as of 2025 — verify which is cheapest)
- **Processing time per option** (standard vs. expedited, in working days)

Compute a personalised total based on the user's choices:

> "Your situation: **renewal of [ID-card / passport / both], applying [in person / via self-service portal / abroad], [standard / expedited] procedure, pickup at [PPA office / by post / Selver store]**.
>
> - State fee for [document]: €X
> - Plus state fee for [second document, if both]: €Y
> - Plus [foreign-rep / expedited / pickup-method] surcharge: €Z
> - **Total: €T**
> - Expected ready: within W working days from acceptance."

If the user is applying for both a passport and ID-card in the same visit, surface that the photo, fingerprints, and signature are captured once for both — but each document has its own state fee; there is no automatic combined-renewal discount unless the live page now offers one (verify).

## Step 5 — Booking availability lookup

Fetch `https://broneering.politsei.ee/` to check what the booking system surfaces. The PPA appointment system is interactive (a Qmatic widget); the public HTML may not expose specific time slots without running its JavaScript. If the WebFetch returns a near-empty shell:

- Confirm the booking page is reachable.
- Tell the user the URL and explain that they must pick the slot interactively.
- Identify the nearest PPA client service office to the user's city. Common offices include Tallinn (multiple), Tartu, Narva, Pärnu, Jõhvi, Rakvere, Viljandi, Valga, Kuressaare — verify the current list at `https://www.politsei.ee/en/services/services/` and don't quote opening hours from cache.

If the user prefers a walk-in queue ticket (some offices), surface `https://mobiilnepilet.politsei.ee/` as the alternative.

> "Open `https://broneering.politsei.ee/` in your browser, choose **service: passport / ID-card application**, choose **office: [nearest to your city]**, and pick a slot. Bring everything from the Step 7 checklist below."

## Step 6 — If abroad, embassy lookup

If the user said they're outside Estonia, fetch `https://www.politsei.ee/en/estonian-foreign-representations-that-issue-documents` and surface the relevant Estonian foreign representation in the user's country. Notes:

- Career embassies and consulates accept all document categories (passport, ID-card, digital ID), subject to current local availability — verify on the live page.
- **Honorary consuls** issue Estonian citizen's passports but not always ID-cards / digital IDs. The Ministry of Foreign Affairs maintains a list of honorary consuls authorised for ID-card / digital-ID issuance — link the user there if no career embassy is in their country.
- Foreign-representation state fees are higher than Estonia-side fees; the surcharge varies. Re-fetch the current rate.
- Application abroad still requires fingerprints (subject to the same age and validity exemptions). Plan for two visits if the local representation requires the original fingerprinting and the new-document collection in separate trips.

If the user names their country or city, identify the closest representation and report its address, contact, and (if surfaced) appointment-booking method.

## Step 7 — Pre-appointment checklist

Output a checklist tailored to the user's branch:

```
What to bring to your PPA appointment:

ALWAYS:
1. A document photo per the requirements in Step 3 (digital file uploaded
   in advance, OR a printed copy if your service office accepts that).
2. Your current ID document — even an expired Estonian ID-card or
   passport is useful to bring as proof of identity continuity.
3. Means to pay the state fee. Verify whether the fee can be paid:
   - Online in advance via the PPA self-service portal (often the
     cheapest path; confirm), OR
   - At the appointment by card (most offices accept card, no cash), OR
   - By bank transfer in advance with a payment reference.

IF FIRST-TIME APPLICANT (no prior Estonian document):
4. Birth certificate or equivalent proof of citizenship.
5. If the applicant is a minor: parental-consent presence (both legal
   representatives unless one has sole custody, as confirmed by court /
   civil-registry document).

IF YOUR NAME OR LEGAL DETAILS HAVE CHANGED SINCE THE PREVIOUS DOCUMENT:
6. The civil-registry document confirming the change (marriage / divorce
   / name-change certificate). The PPA pulls many of these from the
   population register automatically, but bring originals for clarity.

IF REPLACING A LOST / STOLEN DOCUMENT:
7. The reference number from the lost-document declaration filed in
   advance with the PPA. The previous document must be declared invalid
   before the replacement is issued.

IF APPLYING ABROAD:
8. Whatever the foreign representation specifies in its booking
   confirmation — requirements vary per representation.
```

Don't list items the user's branch doesn't need (don't ask for a birth certificate on a renewal; don't ask for parental consent for an adult).

## Step 8 — Auth seam

> Now you're ready to file the application:
>
> - **Self-service renewal (Branch A — ID-card renewal only):** log in to the PPA self-service portal at `https://www.politsei.ee/en` (the "Apply" entry point will route to `https://etaotlus.politsei.ee/`) using your **current ID-card** with the eID software, or your **Mobile-ID** (if accepted by the renewal flow — verify). Upload the photo, confirm the data prefilled from the population register, pay the state fee, and submit. The new ID-card will be sent to your chosen pickup point.
>
> - **In person (Branch B):** book at `https://broneering.politsei.ee/` (or visit a service office that accepts walk-in queue tickets via `https://mobiilnepilet.politsei.ee/`). Bring the checklist from Step 7. The appointment captures fingerprints, signature, and photo (if you didn't upload in advance). The new document is ready within the live SLA you computed in Step 4.
>
> - **Abroad (Branch C):** schedule with the foreign representation identified in Step 6 according to its own booking method.

After submission / appointment, do not narrate the post-auth experience — the user is in a controlled flow with the PPA or its representation, and that flow is authoritative.

Note on auth: a physical ID-card with valid certificates is the most reliable authentication method for the PPA self-service portal, since the certificate authority chain is the PPA itself. Mobile-ID is generally accepted; Smart-ID acceptance for PPA flows has historically lagged Mobile-ID — verify the current acceptance on the live login page before promising the user Smart-ID will work.

## Sources

See `references/sources.md`.
