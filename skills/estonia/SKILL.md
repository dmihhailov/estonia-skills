---
name: estonia
description: |
  Router for Estonian bureaucracy questions. Use whenever the user asks about
  Estonian government procedures, taxes, business registration, residence,
  identity documents, e-Residency, passports, kindergarten enrolment, vehicle
  registration, healthcare, social benefits, or any other interaction with an
  Estonian state authority. Routes to the appropriate sub-skill based on
  audience and intent. Trigger words: "Estonia", "Eesti", "OÜ", "MTA", "EMTA",
  "e-Residency", "isikukood", "tuludeklaratsioon", "Töötukassa", "PPA", "Smart-ID".
license: MIT
metadata:
  audience: "citizen,resident,e-resident,non-resident-founder,expat-newcomer"
  life_event: "meta"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "none"
  authoritative_lang: "et"
  freshness_sources: ""
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Estonia — bureaucracy router

This skill is the entry point for Estonian government procedures. It does not give procedural advice itself; it routes to a sub-skill that does.

## Disclaimer

Before any procedural guidance, reproduce the key line from `references/disclaimer.md`:

> This is AI-generated procedural guidance, not legal, tax, or medical advice. Always verify against the authoritative Estonian government source. This repository is not affiliated with the Republic of Estonia.

## Routing logic

1. **Load the catalog.** Read `INDEX.yaml` (in this same skill directory). It lists every other skill in this repository with full metadata.

2. **Identify audience.** If the user's message does not make their audience clear, ask exactly one question:
   > Are you (a) an Estonian citizen or resident, (b) an e-Resident running an Estonian company, or (c) newly arrived or arriving in Estonia?

   If the user replies with their situation in plain language, infer the audience tag(s) and proceed.

3. **Filter the catalog.** Narrow `INDEX.yaml` entries to those whose `audience` overlaps with the user's audience and whose `service_domain` or trigger keywords match the user's intent.

4. **Branch on match count:**
   - **One match** — name the skill, summarize what it covers in one sentence, and ask: "Want me to walk you through it?" Do not auto-load.
   - **Multiple matches** — present a numbered list (max 5) with one-line descriptions. Let the user pick.
   - **Composite life event** (e.g., "I'm relocating to Estonia") — propose an ordered chain of skills with shared context. Confirm before chaining.

5. **Freshness check.** Before activating any sub-skill, look at its `last_verified` date. If it is more than 90 days before today, warn the user:
   > This skill was last verified on YYYY-MM-DD. Estonian government procedures can change; if anything below seems out of date, double-check against the authoritative source linked at the bottom of the skill.

6. **No PII into chat.** Never ask the user to paste their isikukood, account numbers, or any other personal identifier into the conversation. If a procedural step requires personal data, instruct the user to enter it directly into the relevant gov portal at the time of authentication.

## Reference material

- `references/disclaimer.md` — full disclaimer text and AI Act compliance language.
- `references/eid-primer.md` — Smart-ID, Mobile-ID, ID-card, e-Residency card explained.
- `references/glossary.md` — definitions of `isikukood`, `OÜ`, `MTA`, and other terms used across skills.

## Sub-skills available in v1

See `INDEX.yaml`. v1 ships:
- `tax-filing-individual` — annual personal income tax declaration via e-MTA.
- `ou-open-e-resident` — opening a private limited company (OÜ) as an e-Resident.
- `residence-registration` — registering one's place of residence as a newcomer.
