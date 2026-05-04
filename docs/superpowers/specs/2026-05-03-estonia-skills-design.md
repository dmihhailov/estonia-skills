# estonia-skills — design

**Status:** draft
**Date:** 2026-05-03
**Owner:** dmitri.mihhailov@gmail.com

## Summary

A public, MIT-licensed Claude Code plugin that bundles modular skills for navigating Estonian bureaucracy. Skills are written for three audiences (Estonian citizens/residents, e-Residents, expat newcomers), conform to the agentskills.io v1 spec, and never hardcode legal or financial information — they always re-fetch from authoritative government sources at runtime.

V1 ships three atomic skills (annual personal income tax filing, opening an OÜ as an e-Resident, residence registration for newcomers) plus a router skill that disambiguates the user's intent and dispatches to the right one.

## Goals

1. Make it materially easier for anyone interacting with Estonian government procedures to use Claude as a guide, with answers grounded in current authoritative sources.
2. Establish patterns (router + atomic skills + freshness model + tag schema) that scale cleanly from 3 skills to ~30 over time.
3. Be the first published civic-tech Claude skill repo, written in a way that other countries can fork and adapt.
4. Stay legally and ethically defensible: AI Act-compliant disclaimer, GDPR-clean (no PII collection), explicit non-affiliation with the Republic of Estonia.

## Non-goals (v1)

- RU translations of skill bodies. (Runtime rendering by Claude is enough; community-contributed RU summaries can land in v2.)
- A companion MCP server. (Plain WebFetch covers everything we need; MCP comes only if specific skills demonstrably need it.)
- Authenticated transactional skills. Skills end at the Estonian eID auth seam ("now log in to e-MTA with your Smart-ID and click X"). Skills do not impersonate the user.
- Skills wrapping Bürokratt. Bürokratt is the Estonian government's official assistant mesh; this repo is positioned as a Claude-native complement, not a replacement or integration target.
- Anything requiring X-Road membership.

## Architecture

A single Claude Code plugin, distributed via `/plugin marketplace add`. Internally:

- One **router skill** (`estonia/`) that owns a generated `INDEX.yaml` and is the natural-language entry point.
- N **atomic skills** (3 in v1), each one self-contained, conforming to the agentskills.io v1 SKILL.md spec.
- A **shared references library** inside the router (`disclaimer.md`, `eid-primer.md`, `glossary.md`) that atomic skills cite by relative path.

Skills are auto-discovered: pointing `plugin.json`'s `skills` field at `./skills/` causes Claude Code to register every `*/SKILL.md` underneath. Adding a new skill is "create a new directory, drop in `SKILL.md`" — no manifest edits.

Skills are slash-invocable for free: each skill registers as `/estonia-skills:<skill-name>`, so power users can bypass the router. The router remains the friendly natural-language entry point.

## Repo layout

```
estonia-skills/
├── README.md                           # intro, install, Bürokratt acknowledgement, demo
├── LICENSE                             # MIT (covers code + content)
├── PRIVACY.md                          # GDPR rules for contributors
├── CONTRIBUTING.md                     # how to add a skill
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── estonia/                        # router skill
│   │   ├── SKILL.md
│   │   ├── INDEX.yaml                  # generated from sub-skill metadata
│   │   └── references/
│   │       ├── disclaimer.md           # AI Act + no-legal-advice boilerplate
│   │       ├── eid-primer.md           # Smart-ID / Mobile-ID / ID-card explainer
│   │       └── glossary.md             # isikukood, OÜ, EMTA, e-MTA, etc.
│   ├── tax-filing-individual/
│   │   ├── SKILL.md
│   │   └── references/sources.md       # canonical URL list with last-checked dates
│   ├── ou-open-e-resident/
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   └── residence-registration/
│       ├── SKILL.md
│       └── references/sources.md
├── scripts/
│   └── build-index.py                  # regenerates skills/estonia/INDEX.yaml from frontmatter
└── .github/
    └── workflows/
        └── validate.yml                # frontmatter schema check + Markdown lint
```

## Plugin manifest files

`.claude-plugin/plugin.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "estonia-skills",
  "version": "0.1.0",
  "description": "Modular Claude skills for Estonian bureaucracy — taxes, OÜ, residence, identity",
  "license": "MIT",
  "homepage": "https://github.com/<owner>/estonia-skills",
  "repository": "https://github.com/<owner>/estonia-skills",
  "keywords": ["estonia", "civic", "bureaucracy", "tax", "e-residency"],
  "skills": "./skills/"
}
```

Pointing `skills` at the directory means contributors never edit `plugin.json` to register a new skill — they just create a new directory.

`.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-marketplace.json",
  "name": "estonia-skills",
  "owner": { "name": "<owner-name>" },
  "plugins": [
    {
      "name": "estonia-skills",
      "source": "./",
      "description": "Modular Claude skills for Estonian bureaucracy",
      "version": "0.1.0",
      "license": "MIT",
      "category": "productivity",
      "keywords": ["estonia", "civic", "tax", "e-residency"]
    }
  ]
}
```

## Skill anatomy

### Frontmatter schema

The agentskills.io v1 spec gives us `name`, `description`, `license`, `metadata` (string-string map), `compatibility`, and the experimental `allowed-tools`. Our index lives inside `metadata`. Because spec restricts metadata values to strings, list-typed fields are pipe- or comma-separated and parsed by `build-index.py`:

| Field | Required | Values | Notes |
|---|---|---|---|
| `audience` | yes | comma-list of `citizen`, `resident`, `e-resident`, `non-resident-founder`, `expat-newcomer` | Orthogonal flags; multiple may apply. |
| `life_event` | yes | one of `arriving`, `starting-business`, `employment`, `family`, `housing`, `vehicle`, `education`, `healthcare`, `retirement`, `leaving`, `death`, `meta` | `meta` for skills that don't fit a phase. |
| `service_domain` | yes | one of `tax`, `identity`, `business`, `social`, `health`, `justice`, `property` | |
| `cadence` | yes | one of `one-off`, `annual`, `monthly`, `on-demand` | |
| `difficulty` | yes | one of `self-serve`, `accountant-recommended`, `lawyer-recommended` | |
| `auth_required` | yes | comma-list of `none`, `smart-id`, `mobile-id`, `id-card`, `e-residency-card` | |
| `authoritative_lang` | yes | `et`, `en`, or `ru` | Almost always `et`. |
| `freshness_sources` | yes | pipe-separated URL list | URLs the skill body must re-fetch before quoting numbers/dates/fees. |
| `last_verified` | yes | `YYYY-MM-DD` | Updated by the contributor when re-checking the skill. Router warns if >90 days. |
| `version` | yes | semver string | |

### Body conventions

Every atomic skill body follows the same shape:

1. **Disclaimer reference.** Link to `references/disclaimer.md` from the router and reproduce its key line ("AI-generated procedural guidance, not legal/tax/medical advice; verify against the source").
2. **Freshness obligation.** Explicit instruction: "Before quoting any number, fee, or deadline, fetch the current page at <URL>. Never quote cached numbers."
3. **Disambiguation.** The minimum question(s) needed to scope the procedure to the user's situation (e.g., "Are you a tax resident in 2025?").
4. **Walkthrough.** Step-by-step prose. End at the Estonian eID auth seam — the skill instructs the user to log in to a gov portal and click X; it does not transact on their behalf.
5. **Sources.** Reference `references/sources.md` for the canonical URL list with last-checked dates.

### Example frontmatter

```yaml
---
name: tax-filing-individual
description: |
  Walks an Estonian resident or citizen through filing the annual personal
  income tax declaration via e-MTA. Trigger on: "tax return", "tuludeklaratsioon",
  "annual taxes", "MTA", "tax filing for individuals", or "how much do I owe / will I get back".
  Always re-fetches current tax-year rates and deadlines from emta.ee — never quotes cached numbers.
license: MIT
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
  version: "1.0.0"
---
```

## Router skill

`skills/estonia/SKILL.md` description (what triggers it):

> Use whenever the user asks about Estonian bureaucracy, government procedures, taxes, business registration, residence, identity documents, e-Residency, or anything involving an Estonian government service. Routes to the appropriate sub-skill based on audience and intent.

Body logic:

1. Load `INDEX.yaml`.
2. If audience is unclear from the user's message, ask **one** disambiguating question: "Are you (a) an Estonian citizen or resident, (b) an e-Resident running an Estonian company, or (c) newly arrived or arriving in Estonia?"
3. Filter `INDEX` by audience + intent keywords from the user's message.
4. Branching:
   - **One match** → suggest activating that skill.
   - **Multiple matches** → present them, let the user choose.
   - **Composite life event** (e.g., "I'm relocating to Estonia") → propose an ordered chain of skills sharing context.
5. Before activating any skill, check `last_verified`. If >90 days, warn the user that the skill may need verification against current gov sources.

`INDEX.yaml` is regenerated from sub-skills' frontmatter by `scripts/build-index.py`. CI runs the script on PR and fails if the committed `INDEX.yaml` is stale, so the skills' own frontmatter remains the source of truth.

## v1 skills

The URLs below are illustrative starting points, not verified canonical paths. The implementation plan will verify each URL against the live site, choose the most stable available, and record any redirects.

| Skill directory | Audience tags | `freshness_sources` (illustrative) | Auth seam |
|---|---|---|---|
| `tax-filing-individual` | `citizen,resident` | `emta.ee/eraklient/tulu-deklareerimine`, `emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad` | "Now log in to e-MTA with your Smart-ID / Mobile-ID / ID-card and review the pre-filled return." |
| `ou-open-e-resident` | `e-resident,non-resident-founder` | `e-resident.gov.ee/start-a-company`, `ariregister.rik.ee/eng/company-registration-portal` | "Now sign in to the Company Registration Portal with your e-Residency card to file the application." |
| `residence-registration` | `expat-newcomer,resident` | `eesti.ee/en/family-and-relationships/registering-residence`, relevant subset of `politsei.ee/en/instructions` for residence permits | "Submit at rahvastikuregister.ee with your eID, or visit your local council in person." |

Each ships with `references/sources.md` listing every URL referenced in the body, with a "last checked: YYYY-MM-DD" stamp per URL.

## Freshness model

### Runtime freshness (every invocation)

The skill body always instructs Claude:

> Before quoting any number, fee, deadline, or specific procedural step, fetch the current page at the URL listed in `metadata.freshness_sources`. Do not quote any number from this skill body itself — they are illustrative only.

Numbers (tax rates, fees) are re-fetched per session. Text-heavy guidance is fetched once per session and cached in conversation context.

### Meta-freshness (skill rot over project lifetime)

Three layers, shipped progressively:

- **v1 — `last_verified` timestamp.** Every skill carries `last_verified: YYYY-MM-DD`. The router warns the user when activating a skill verified more than 90 days ago. Contributors update the field when they re-check the skill.
- **v2 — automated link checking.** A nightly GitHub Action does HEAD checks against every URL in `freshness_sources` across all skills, opens an issue on 404 / 410 / 5xx.
- **v3 — AI freshness bot.** A scheduled Action runs Claude over each skill's `freshness_sources`, diffs current content against the last verified snapshot, opens a PR flagging material changes (rate changes, restructured pages, new procedures).

V1 ships only the timestamp. v2 and v3 are roadmap, not blocking.

## Distribution and install

Public GitHub repo. Users install via:

```
/plugin marketplace add <github-owner>/estonia-skills
/plugin install estonia-skills@estonia-skills
/reload-plugins
```

Skills are also portable to claude.ai (manual upload) and the Claude API (Skills parameter) since they're stock SKILL.md format.

There is no central plugin registry; discoverability comes from the README, word of mouth, and external lists like `awesome-claude` repos. The README must therefore work hard — install instructions, demo transcript, contribution guide all reachable from the top.

## Legal and contributor model

### License

MIT for everything. Code and content under one short permissive license. Maximum compatibility, minimum contributor friction. The patent grant from Apache-2.0 is unnecessary for a project that's almost entirely Markdown procedural guidance, and procedures themselves are not subject to patent or copyright. Allows commercial use; the project explicitly has no monetization plans, so others' use is fine.

### Disclaimer (AI Act Art. 50 + liability)

Every skill body opens with a reference to `skills/estonia/references/disclaimer.md`, which contains:

- "This is AI-generated procedural guidance, not legal, tax, or medical advice."
- "Always verify against the authoritative Estonian government source linked below."
- "This repository is not affiliated with the Republic of Estonia, Maksu- ja Tolliamet, Politsei- ja Piirivalveamet, the e-Residency programme, or any other state authority."
- "When in doubt, consult a qualified accountant, lawyer, or notary."

### Privacy (`PRIVACY.md`)

Two non-negotiable rules for contributors:

1. **Never embed example PII.** No real `isikukood`, no real account numbers, no real names. Synthetic examples only. Validators in CI grep for `isikukood` patterns and fail the build if any found.
2. **Skills must never request PII into the conversation.** Phrase prompts as "you will need your isikukood for this step" — never "paste your isikukood here." Skills walk users to the gov portal where authentication happens; they don't intermediate it.

### Bürokratt acknowledgement

The README opens with a note acknowledging Bürokratt as the Estonian government's official assistant mesh, and positions estonia-skills as a Claude-native complement intended for users who already work in Claude or want a different interface. Not a competitor, not an integrator (no Bürokratt API calls in v1).

### Contributing flow

1. Fork the repo.
2. Create `skills/<new-skill-name>/SKILL.md` following the frontmatter schema and body conventions.
3. Add `skills/<new-skill-name>/references/sources.md`.
4. Run `python scripts/build-index.py` to regenerate `skills/estonia/INDEX.yaml`.
5. Set `last_verified` to today.
6. Open PR. CI validates frontmatter, lints Markdown, checks for accidental PII, and verifies the index is in sync.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Estonian gov site URL changes break skills | `freshness_sources` is per-skill; v2 link-check Action surfaces breakage within 24 h; users see `last_verified` warning. |
| EN translations of Estonian law lag ET | Skills mark `authoritative_lang: et` and the body instructs Claude to flag this when citing translated content. |
| Skill descriptions collide as catalog grows | Router uses `audience` + `service_domain` filters before description matching; INDEX.yaml is queryable by tag. |
| Contributor accidentally embeds real PII | CI greps for known PII patterns; PRIVACY.md spells out the rule; reviewer required. |
| Procedure changes faster than re-verification | `last_verified` warning at >90 days; v3 AI freshness bot eventually closes this gap. |
| Liability from incorrect guidance | Per-skill disclaimer; explicit non-affiliation; MIT "no warranty" clause; skills never collect PII or transact. |
| User mistakes the project for an official Estonian service | README and disclaimer are explicit; "estonia-skills" name doesn't impersonate any state body. |

## Open questions (deferred to implementation plan)

- Exact wording of `disclaimer.md` (legal review desirable but not blocking v1).
- Whether `validate.yml` should run a real WebFetch against `freshness_sources` URLs or rely on schema validation only (cost vs. coverage).
- Naming: `estonia-skills` vs. `claude-skills-estonia` vs. `eesti-skills` — pick one before publishing.
- Verifying the actual canonical URLs for each v1 skill's `freshness_sources` against the live Estonian gov sites (research session was blocked from those domains).
