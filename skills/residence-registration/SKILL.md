---
name: residence-registration
description: |
  Walks a newcomer to Estonia (EU/EEA citizen, third-country national, or
  returning resident) through registering their place of residence in the
  rahvastikuregister (population register). Use when the user mentions:
  "register address Estonia", "rahvastikuregister", "kohalik omavalitsus",
  "moving to Estonia", "place of residence", "elukoharegistreerimine".
  Distinguishes between place-of-residence registration (for everyone) and
  residence permits (for non-EU nationals). Always re-fetches current procedure
  from eesti.ee and politsei.ee.
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
  audience: "expat-newcomer,resident"
  life_event: "arriving"
  service_domain: "identity"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.eesti.ee/en|https://www.politsei.ee/en/instructions/applying-for-a-residence-permit"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Residence registration

## Disclaimer

This is AI-generated procedural guidance, not legal advice. The decision-tree outputs and document drafts this skill produces are starting points; your authoritative status is whatever the local council and PPA confirm. For complex situations (refugee/asylum, family reunification with disputed parentage, long-term resident transitions), consult a lawyer or the PPA directly. This repository is not affiliated with the Republic of Estonia, Politsei- ja Piirivalveamet, or any local government.

## Freshness obligation

**Before quoting any deadline, fee, document list, or processing time, fetch the current pages at:**

- `https://www.eesti.ee/en` (state portal — the residence-registration flow lives here; navigate to "Family and relationships" / "Registering place of residence" if a deep link doesn't resolve, since eesti.ee is a single-page application whose specific paths cannot be verified server-side)
- `https://www.politsei.ee/en/instructions/applying-for-a-residence-permit` (PPA — residence permits)

**Do not use any number or date from this skill body.** Numbers below are illustrative.

## Step 1 — Decision tree: which procedure(s) do you need?

Walk the user through this branch by asking only the questions needed:

**Q1: What's your citizenship?**
- **Estonian citizen returning to Estonia** → place-of-residence registration only.
- **EU/EEA/Swiss citizen** → continue to Q2.
- **Third-country national (non-EU/EEA/Swiss)** → continue to Q3.

**Q2 (EU/EEA/Swiss): Are you staying >3 months?**
- **No, short stay** → no registration needed.
- **Yes, >3 months** → place-of-residence registration AND right-of-residence registration with PPA.

**Q3 (third-country): Do you already hold a valid Estonian residence permit?**
- **Yes** → place-of-residence registration only (you've already got the permit).
- **No** → residence permit FIRST (Step 5 of this skill), then place-of-residence registration after arrival.

State the result back to the user explicitly: "Based on your answers, you need: [procedure list]." Then proceed through the relevant Steps below.

## Step 2 — Find the right local council (kohalik omavalitsus)

Place-of-residence registration is filed with the local government covering the user's address. The user provides their city and (for Tallinn / Tartu / Pärnu) the district / linnaosa.

1. **Ask for city + district** (not the street address — we don't need or want the specific address in chat).
2. **Look up the responsible local government** for that city/district. For Tallinn: 8 linnaosa (Haabersti, Kesklinn, Kristiine, Lasnamäe, Mustamäe, Nõmme, Pirita, Põhja-Tallinn) — each has its own service desk. For Tartu: city service centre. For other cities/parishes: the unitary municipality.
3. **Provide the name + the in-person service address** of the responsible council, plus a link to its online residence-registration page (most councils have one accessible via eesti.ee). For users who cannot use eID, this is where they go in person with paper documents.

The output is: "For your address in [city/district], the responsible local government is [name]. Online registration is via eesti.ee residence flow; in-person at [address]."

## Step 3 — Personalised document checklist

Build the checklist based on what we've established:

```
Documents you'll need:

ALWAYS:
- Passport (or Estonian ID-card if you have one)
- Proof of right to use the address — see Step 4 below

IF YOU'RE RENTING:
- Tenancy agreement, OR
- Property-owner consent letter (Step 4 generates a template)

IF YOU OWN THE PROPERTY:
- Title deed extract from the Land Register (kinnistu väljatrükk)

IF YOU HAVE FAMILY MEMBERS REGISTERING TOO:
- Children: birth certificates (apostilled / translated if foreign)
- Spouse: marriage certificate (apostilled / translated if foreign)

IF YOU'RE EU/EEA/SWISS REGISTERING RIGHT-OF-RESIDENCE WITH PPA:
- Proof of basis for stay: employment contract / university enrolment letter / proof of sufficient funds
- Application form for right-of-residence (the PPA online flow generates this)

IF YOU'RE A THIRD-COUNTRY NATIONAL WITH PERMIT:
- Copy of valid residence permit
```

Tailor the list to omit sections that don't apply to the user's situation. Output the result inline.

## Step 4 — Generate property-owner consent letter (if renting)

If the user is renting and the tenancy agreement isn't acceptable to the council (some councils require a separate consent), generate the consent letter template.

**Important:** the agent does NOT know the user's name, address, or the property owner's name. Generate the template with clearly-marked placeholders that the user fills in themselves before having the owner sign.

Output the template inline as a code block. Estonian first (legally canonical), English working translation below:

```
NÕUSOLEK ELUKOHA REGISTREERIMISEKS

Mina, [PROPERTY OWNER'S FULL NAME], elukoht [PROPERTY OWNER'S ADDRESS], olen kinnistu nr [LAND REGISTRY NUMBER] omanik (aadress: [PROPERTY ADDRESS]).

Annan käesolevaga oma nõusoleku, et [TENANT'S FULL NAME] võib registreerida oma elukoha aadressil [PROPERTY ADDRESS].

Käesolev nõusolek kehtib kuni selle kirjaliku tagasivõtmiseni.

[OMANIKU ALLKIRI / OWNER'S SIGNATURE]
[KUUPÄEV / DATE]
```

```
CONSENT FOR RESIDENCE REGISTRATION (working translation; Estonian text is legally canonical)

I, [PROPERTY OWNER'S FULL NAME], residing at [PROPERTY OWNER'S ADDRESS], am the owner of land registry property no. [LAND REGISTRY NUMBER] (address: [PROPERTY ADDRESS]).

I hereby give my consent for [TENANT'S FULL NAME] to register their place of residence at [PROPERTY ADDRESS].

This consent remains valid until withdrawn in writing.

[OWNER'S SIGNATURE]
[DATE]
```

The user fills in the placeholders and has the owner sign — either with eID (digital signature via DigiDoc4) or wet-ink. Either is accepted.

## Step 5 — Residence permit decision tree (only for third-country nationals without a permit)

If Step 1 routed here, walk through permit types:

**Q: What's your basis for being in Estonia?**
- **Employment contract with an Estonian employer** → temporary residence permit for employment. Application via politsei.ee, usually filed at an Estonian embassy abroad before travel.
- **University acceptance / study programme** → temporary residence permit for study.
- **Family member is an Estonian citizen or resident** → temporary residence permit for family reunification.
- **Running an Estonian business / self-employed** → temporary residence permit for enterprise (overlaps with the OÜ flow).
- **Living in Estonia legally for ≥5 years** → long-term resident permit.
- **Other / unsure** → fetch the politsei.ee permit-type overview and surface the options.

For the user's permit type, **fetch the relevant politsei.ee subpage** (`https://www.politsei.ee/en/instructions/applying-for-a-residence-permit/[type]` or whatever the canonical path turns out to be) and list the specific document requirements, application channels, current state fee, and processing time. Crucial procedural note: most third-country applications must be filed at an Estonian embassy abroad **before** travel, not after arrival. There are exceptions (e.g., if already in Estonia on certain visas) — confirm against the live page.

## Step 6 — Auth seam

**For place-of-residence registration:**

> Submit your registration online at the eesti.ee residence-flow page (under "Family and relationships" / "Registering place of residence") using your Smart-ID, Mobile-ID, or ID-card. Attach the documents from Step 3 (and the consent letter from Step 4 if renting). OR — visit the local council office identified in Step 2 in person with paper documents.

**For EU/EEA/Swiss right-of-residence registration:**

> File the right-of-residence application with PPA at https://www.politsei.ee/en (find the EU citizens' residence section under instructions) using your eID. Attach the documents from Step 3.

**For residence permits (third-country nationals):**

> Apply at the relevant Estonian embassy abroad (or, if eligible, in person at a PPA service point in Estonia). The application flow is on the politsei.ee page; this skill ends at the start of that flow.

After login, do not narrate the in-portal experience.

## Sources

See `references/sources.md`.
