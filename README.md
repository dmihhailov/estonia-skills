# estonia-skills

Modular [Claude](https://claude.ai) skills for Estonian bureaucracy — taxes, OÜ company formation, residence registration, and more. Skills are written in the [agentskills.io v1](https://agentskills.io/specification) format and packaged as a Claude Code plugin.

> **Not affiliated with the Republic of Estonia.** For the official Estonian government assistant mesh, see [Bürokratt](https://burokratt.ee). This repo is a Claude-native complement, intended for users who already work in Claude.

## Install (Claude Code)

```
/plugin marketplace add dmitrim/estonia-skills
/plugin install estonia-skills@estonia-skills
/reload-plugins
```

(Replace `dmitrim` with the actual GitHub owner.)

After install, ask Claude things like:

- "How do I file my Estonian income tax return?"
- "I'm an e-Resident — how do I open an OÜ?"
- "I just moved to Estonia, do I need to register my address?"

The router skill `estonia` will pick up the question and route to the right sub-skill.

## What's in v1

| Skill | Audience | Covers |
|---|---|---|
| `tax-filing-individual` | citizens, residents | Annual personal income tax declaration via e-MTA |
| `ou-open-e-resident` | e-Residents, non-resident founders | Opening an OÜ remotely with e-Residency ID |
| `residence-registration` | expat newcomers, residents | Registering place of residence (and residence permits) |

Plus the `estonia` router skill that disambiguates the user's intent and dispatches.

## How freshness works

Every skill carries a `freshness_sources` list of authoritative gov URLs (emta.ee, e-resident.gov.ee, eesti.ee, politsei.ee, …). When activated, the skill instructs Claude to **re-fetch those pages before quoting any number, fee, or deadline**. Skill bodies do not hardcode tax rates, thresholds, or deadlines — those always come from the live page.

Each skill also carries a `last_verified` timestamp. The router warns the user when activating a skill that hasn't been verified in over 90 days.

## Authentication boundary

Skills walk the user up to the Estonian eID auth seam (Smart-ID, Mobile-ID, ID-card, or e-Residency card) and then hand off. Skills never request personal identifiers in chat, never store PII, and never transact on the user's behalf.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to add a skill. The short version:

1. Create `skills/<your-skill>/SKILL.md` with the standard frontmatter.
2. Add `skills/<your-skill>/references/sources.md` listing canonical URLs.
3. Run `python scripts/build_index.py` and `python scripts/validate_frontmatter.py`.
4. Open a PR.

Privacy rules in [`PRIVACY.md`](PRIVACY.md) are non-negotiable: no real PII in examples, no PII collection in skills.

## License

MIT — see [`LICENSE`](LICENSE).

## Design

Architecture and rationale: [`docs/superpowers/specs/2026-05-03-estonia-skills-design.md`](docs/superpowers/specs/2026-05-03-estonia-skills-design.md).
