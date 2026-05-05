# Contributing to estonia-skills

Thanks for considering a contribution. This repo aims to cover Estonian bureaucratic procedures comprehensively, accurately, and freshly. Pull requests welcome — especially new skills covering procedures not yet in v1.

## What makes a good skill

- **Procedural, not advisory.** Walks a user through "how to do X with the Estonian state." Avoids individualised legal/tax/medical opinions.
- **Audience-aware.** Tagged with one or more of `citizen`, `resident`, `e-resident`, `non-resident-founder`, `expat-newcomer`.
- **Freshness-correct.** Body never quotes specific numbers (rates, fees, deadlines) — those are always re-fetched from the URLs in `freshness_sources` at runtime.
- **Authentication-respecting.** Ends at the Estonian eID auth seam — does not transact on the user's behalf, does not request PII.
- **Agentic.** *Does* as much as it can before the auth seam, instead of telling the user to go and do things manually. See the next section.

## Designing agentic skills

The default temptation when writing a skill is to tell the user "go visit X and click Y" for every step. That makes the skill a long instruction manual the user has to follow themselves. **Don't do that.** A good skill in this repo *takes the actions* it can take, and only hands off to the user for the parts that genuinely require it (eID authentication, signature, payment).

### What the agent CAN do (no auth needed)

| Capability | Examples |
|---|---|
| **Read public data** | WebFetch authoritative pages, parse the relevant section |
| **Use public APIs / queries** | `ariregister.rik.ee/eng/name_query`, `marketplace.e-resident.gov.ee`, municipality directories, Riigi Teataja API |
| **Compute** | Tax owed, share capital scenarios, eligibility decisions, deadline math |
| **Draft documents** | Letters, articles of association, consent forms, checklists, application data the user pastes |
| **Personalize** | Build a decision tree, surface only the subset relevant to *this* user's citizenship / residency / income mix |

### What the agent CAN'T do (still hits the seam)

- Authenticate to a gov portal as the user
- Submit signed filings, pay state fees
- Read the user's own data on a gov portal (their pre-filled tax return, their existing companies)
- Hold or transmit PII

### Hard constraints (preserved no matter how agentic the skill becomes)

1. **Never ask the user to paste PII into chat.** No isikukood, no account numbers, no passport numbers, no ID-card numbers. The agent works with non-identifying inputs the user volunteers (gross salary figure, citizenship, address city — never the identifier itself). Enforced by `scripts/check_no_pii.py` and reviewed in PRs.
2. **Submission stays user-side.** The agent prepares everything; the user clicks submit after eID authentication.
3. **Numbers always re-fetched live.** Even when computing (e.g. tax math), fetch the rate from the source page first. Never hardcode a fee.
4. **Disclaimer first.** Computed outputs ("you'll owe approximately €X") are estimates; the gov portal is authoritative. The disclaimer must say so.

### Pattern templates

If your skill involves… → consider…

| If your skill involves… | Replace with… |
|---|---|
| "Visit page X" | WebFetch page X, extract and summarise the relevant section |
| "Calculate Y" | Run the computation interactively; show your math step by step |
| "Decide which form / permit / option fits" | Build a decision tree — ask the minimum questions, branch to the right answer |
| "Write a letter from your landlord" | Generate the letter template inline (Estonian + EN), with placeholders filled from the user's answers |
| "Look up Z" (name available, council for an address, etc.) | Query the public source via WebFetch and present the answer |
| "Fill in the registration form" | Generate the form data the user pastes; don't make them re-derive each field |
| "Verify the pre-filled return" | Generate a personalised checklist they tick off after login |

### Anti-patterns to remove

- ❌ "Please calculate your expected tax based on the rates above."
  → ✅ "Tell me your income breakdown and I'll compute your expected tax."
- ❌ "Visit the marketplace and pick a contact-person provider."
  → ✅ "What kind of provider do you need? I'll surface 2–3 options that fit."
- ❌ "Write a consent letter from the property owner."
  → ✅ "Here's a consent letter template in Estonian and English; have the owner sign it."
- ❌ "Decide which residence permit applies to you."
  → ✅ "Three quick questions: are you here for work, study, or family? …"

### Author checklist before opening a PR

For every instruction in your skill body, ask:

1. **Could the agent do this instead of telling the user?** If yes, replace.
2. **If yes, can it be done without auth or PII?** If yes, do it. If no, the instruction stays — but make sure the agent has done everything possible up to that point.
3. **Does the instruction defer a decision the agent could make?** If yes, build the decision tree.
4. **Does the instruction defer a lookup the agent could do?** If yes, WebFetch.
5. **Does the instruction defer a draft the agent could write?** If yes, draft it inline.

A good v1 atomic skill in this repo has 60–80% of its body doing things, and 20–40% handing off at the auth seam. If your skill body is 90% "go do X yourself", it needs another pass.

### Real examples in this repo

- `tax-filing-individual` — interactive tax calculator + personalised verification checklist
- `ou-open-e-resident` — live company-name search, share-capital scenario advisor, articles of association template generator
- `residence-registration` — citizenship decision tree, local council finder, property-owner consent letter generator

## Adding a new skill (six steps)

### 1. Create the directory

```
skills/<your-skill-name>/
├── SKILL.md
└── references/
    └── sources.md
```

`<your-skill-name>` must be lowercase kebab-case (e.g., `kindergarten-queue-tallinn`).

### 2. Write `SKILL.md` with the full frontmatter

Copy the frontmatter shape from any existing skill (e.g. `skills/tax-filing-individual/SKILL.md`). The required `metadata` fields are:

| Field | Allowed values |
|---|---|
| `audience` | comma-list of `citizen`, `resident`, `e-resident`, `non-resident-founder`, `expat-newcomer` |
| `life_event` | one of `arriving`, `starting-business`, `employment`, `family`, `housing`, `vehicle`, `education`, `healthcare`, `retirement`, `leaving`, `death`, `meta` |
| `service_domain` | one of `tax`, `identity`, `business`, `social`, `health`, `justice`, `property` |
| `cadence` | one of `one-off`, `annual`, `monthly`, `on-demand` |
| `difficulty` | one of `self-serve`, `accountant-recommended`, `lawyer-recommended` |
| `auth_required` | comma-list of `none`, `smart-id`, `mobile-id`, `id-card`, `e-residency-card` |
| `authoritative_lang` | `et`, `en`, or `ru` (almost always `et`) |
| `freshness_sources` | pipe-separated URL list — the URLs the skill body must re-fetch before quoting |
| `last_verified` | `YYYY-MM-DD` — today's date |
| `version` | semver (start with `0.1.0`) |

Plus one **top-level** field (sibling of `name`/`description`/`license`/`metadata`):

| Field | Purpose |
|---|---|
| `allowed-tools` | Space-separated list of tools the skill is permitted to use. **Use the canonical "Trusted Estonian Sources" block below** — copy it verbatim into every new skill. It covers the realistic universe of sources an Estonian-bureaucracy skill will reach for; doing it once per skill avoids the prompt-treadmill where each new skill discovers a new domain mid-test. |

#### Canonical `allowed-tools` block — "Trusted Estonian Sources"

Copy this verbatim into the frontmatter of every new skill:

```yaml
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
```

**What's in the list, by category:**

| Category | Domains |
|---|---|
| State portals | `eesti.ee`, `riigiteataja.ee` |
| Tax (MTA) | `emta.ee`, `maasikas.emta.ee` |
| Police / identity (PPA) | `politsei.ee`, `broneering.politsei.ee` |
| Business registry (RIK) | `ariregister.rik.ee`, `ettevotjaportaal.rik.ee`, `avaandmed.ariregister.rik.ee` |
| e-Residency | `e-resident.gov.ee`, `marketplace.e-resident.gov.ee` |
| Social / health | `sotsiaalkindlustusamet.ee`, `tootukassa.ee`, `tervisekassa.ee`, `terviseamet.ee` |
| Transport / vehicles / insurance | `transpordiamet.ee` (Estonian Transport Administration), `maanteamet.ee` (legacy Road Administration redirect), `lkf.ee` (Traffic Insurance Fund), `eteenindus.mnt.ee` (Transport Administration e-services — MOT and vehicle history lookups) |
| Major city portals | `tallinn.ee`, `tartu.ee`, `parnu.ee`, `narva.ee` |
| eID infrastructure | `id.ee`, `smart-id.com`, `sk.ee` |
| Statistics + open data | `stat.ee`, `andmed.stat.ee`, `avaandmed.eesti.ee` |
| Land registry | `maaamet.ee`, `geoportaal.maaamet.ee` |
| Business directories (third-party trusted) | `teatmik.ee`, `inforegister.ee`, `e-krediidiinfo.ee`, `krediidiinfo.ee`, `creditinfo.ee` |
| Read-only web queries | `WebSearch` (unscoped) |

**When to extend this list:**

- A skill needs a domain not in the canonical list → propose adding it to TES rather than allowlisting it ad-hoc in one skill. The list grows monotonically and stays consistent across skills.
- The same domain appearing in the canonical list and freshness_sources is intentional — they serve different purposes (allowlist permits the fetch; freshness_sources tells the skill body where to fetch from).
- Don't add unrelated domains (e.g. random business websites, social media). The list is for governmental + civic-tech sources only.

### 3. Write the body

Follow the standard structure:

1. **Disclaimer** — reproduce the key line from `skills/estonia/references/disclaimer.md`.
2. **Freshness obligation** — instruct Claude to fetch `freshness_sources` URLs before quoting.
3. **Disambiguation questions** — the minimum to scope the procedure to the user.
4. **Walkthrough** — step-by-step prose, ending at the eID auth seam.
5. **Sources** — pointer to `references/sources.md`.

### 4. Run validators locally

```bash
. .venv/bin/activate
python scripts/validate_frontmatter.py
python scripts/build_index.py
python scripts/check_no_pii.py
```

All three must exit 0.

### 5. Set `last_verified` to today

This is the date you actually fetched and read the gov pages cited in `freshness_sources`. **Don't lie about this.** It's the signal users have for trusting the skill.

### 6. Open a PR

PR template includes a checklist. Reviewers look for:

- All validators pass.
- The skill body genuinely re-fetches sources rather than memorising numbers.
- No PII in examples.
- Disclaimer present.
- Auth seam respected.
- `INDEX.yaml` updated (regenerate with `build_index.py`).

## Verifying an existing skill

If you spot a skill whose `last_verified` is more than 90 days old, re-check it:

1. Fetch each URL in `freshness_sources`. Confirm 200 and current content.
2. Check the procedure described in the skill body still matches the live page.
3. Update `last_verified` to today.
4. Open a PR.

This is the single highest-leverage contribution to the repo's long-term usefulness.

## Style

- Write skill bodies in clear English. Claude renders to the user's chosen language at runtime.
- Use Estonian terms (`isikukood`, `OÜ`, `tuludeklaratsioon`) but gloss them on first use.
- Cite the Estonian-language gov page as authoritative; English translations are orientation only.

## Code of conduct

Be respectful. Estonian bureaucracy can frustrate; the repo's job is to demystify, not to vent. Keep PRs and issues focused on the procedural content.
