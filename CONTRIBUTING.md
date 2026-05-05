# Contributing to estonia-skills

Thanks for considering a contribution. This repo aims to cover Estonian bureaucratic procedures comprehensively, accurately, and freshly. Pull requests welcome — especially new skills covering procedures not yet in v1.

## What makes a good skill

- **Procedural, not advisory.** Walks a user through "how to do X with the Estonian state." Avoids individualised legal/tax/medical opinions.
- **Audience-aware.** Tagged with one or more of `citizen`, `resident`, `e-resident`, `non-resident-founder`, `expat-newcomer`.
- **Freshness-correct.** Body never quotes specific numbers (rates, fees, deadlines) — those are always re-fetched from the URLs in `freshness_sources` at runtime.
- **Authentication-respecting.** Ends at the Estonian eID auth seam — does not transact on the user's behalf, does not request PII.

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
| `allowed-tools` | Space-separated list of tools the skill is permitted to use. For skills that fetch live data, list each WebFetch domain explicitly: `WebFetch(domain:emta.ee) WebFetch(domain:www.emta.ee) ...`. Without this, every fetch prompts the user for permission. List **every** domain that appears in `freshness_sources` plus any used in the body's procedural prose. |

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
