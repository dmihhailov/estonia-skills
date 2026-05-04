# Privacy rules for contributors

These are **non-negotiable**. CI enforces them where possible; reviewers enforce them where it can't.

## 1. Never embed real personally identifiable information

Skill bodies, examples, tests, fixtures, and documentation must never contain real:

- Estonian personal identification codes (`isikukood`)
- Bank account numbers (Estonian `EE...` IBANs or any other)
- Passport numbers, ID-card numbers, residence permit numbers
- Real names of real private individuals
- Real home addresses
- Real phone numbers
- Real email addresses (other than well-known role addresses like `info@example.gov`)

Use synthetic examples. The CI script `scripts/check_no_pii.py` greps for personal-code and IBAN patterns; if you have a clearly-synthetic placeholder (like `12345678901`) that the regex flags, add it to `.pii-allowlist`.

## 2. Skills must never request PII into the conversation

Skill bodies must phrase prompts like:

- ✅ "You'll need your isikukood for this step. Have it ready."
- ❌ "Paste your isikukood here so I can check the format."

The Estonian eID flow handles authentication directly between the user and the gov portal. Skills walk the user up to the auth seam and hand off — they do not intermediate identification, ever.

## 3. The repository is GDPR-clean

Skill bodies and code in this repository do not collect, store, or transmit personal data. Users running these skills locally inside Claude do not send personal data through this repository — Claude itself runs in their own client; this repo just provides instructions.

If a contributor has a use case that involves any kind of PII handling, the answer is: **don't build it as a skill in this repo.** Open an issue first.

## 4. Reporting

If you spot a privacy violation in this repository, open an issue tagged `privacy`. For sensitive disclosures, use GitHub's [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) on this repo. PRs that remove violations will be merged immediately.
