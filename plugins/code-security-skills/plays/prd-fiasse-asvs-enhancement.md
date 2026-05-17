# PRD FIASSE / ASVS Enhancement — Step-by-Step Runbook

> **Status:** Stub. This play is referenced by the `prd-securability-enhancement` skill as the detailed runbook. Real content is deferred to a follow-up PR; the SKILL.md itself currently carries the full procedure inline.

## Intent

Enhance PRDs, feature specs, user stories, or product briefs with explicit OWASP ASVS v5.0 coverage and FIASSE v1.0.4 / SSEM implementation guidance — **before** code is written.

The goal is to upgrade the requirements artifact so delivery teams build securable capabilities by design rather than retrofitting controls during/after implementation.

## Procedure

TODO — extract the step-by-step procedure currently embedded in the `prd-securability-enhancement` SKILL.md into this file. High-level shape:

1. **Parse features** — normalize each feature with actor, data sensitivity, trust boundaries, and existing acceptance criteria.
2. **Choose ASVS level** — recommend or accept Level 1/2/3 per feature based on data sensitivity and exposure.
3. **Map features to ASVS chapters** — use `data/asvs/README.md` and the `when_to_use` frontmatter in `data/asvs/V*.md`.
4. **Apply FIASSE principles** — overlay SSEM attribute coverage (Maintainability, Trustworthiness, Reliability umbrellas plus Observability and Transparency).
5. **Add securability acceptance criteria** — testable, traceable to ASVS requirement IDs.
6. **Emit enhanced PRD** — preserve original structure; add a per-feature "Security Requirements" block.

## Output

TODO — define the enhanced PRD artifact shape.

## References

- Triggering skill: [`plugins/code-security-skills/skills/prd-securability-enhancement/SKILL.md`](../skills/prd-securability-enhancement/SKILL.md)
- OWASP ASVS v5.0 chapter index: `data/asvs/README.md`
- OWASP ASVS v5.0 chapters: `data/asvs/V*.md`
- FIASSE v1.0.4 foundational principles: `data/fiasse/S2.1.md`–`S2.6.md`
- FIASSE v1.0.4 SSEM attribute umbrellas: `data/fiasse/S3.2.1.md`–`S3.2.3.md`
