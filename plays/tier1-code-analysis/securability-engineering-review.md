# Play: Securable Code Analysis (FIASSE v1.0.4 / SSEM)

Step-by-step runbook for executing an SSEM-scored review.

> **Source of truth**: [skills/securability-engineering-review/SKILL.md](../../skills/securability-engineering-review/SKILL.md) defines the rubric, equal-weight scoring (1/3 per pillar; 1/4 within Maintainability; 1/3 within Trustworthiness and Reliability), severity classification, output format, and 50-item checklist. This play does not redefine them — it sequences the work.

## Trigger Conditions

Run this play when:

- Performing a proactive security posture assessment of a codebase (beyond vulnerability scanning)
- Evaluating code quality attributes that directly impact security outcomes
- Reviewing merge requests through a securable engineering lens
- Establishing a baseline of securable attributes for a project
- A user asks to assess code securability, code quality for security, or FIASSE/SSEM compliance

## Inputs

- Code files, modules, or full codebase to analyze
- (Optional) Architecture documentation or data-flow diagrams
- (Optional) Target attribute focus areas
- (Optional) Prior static-analysis or quality reports
- (Optional) Dependency manifests

## Steps

### 1. Establish scope and context

Capture before scoring:

- Language / framework
- System type (web app, API, library, CLI, agent, microservice)
- Data sensitivity (PII, credentials, financial, health, regulated)
- Exposure (internet-facing, internal, local-only)
- Lifecycle stage (new, mature, legacy under maintenance)
- Team context (size, experience, velocity)

Without this, scores are guesses.

### 2. Apply triage and sampling (large codebases only)

For codebases beyond a few thousand LoC, follow the triage strategy in the skill: trust boundaries first, then security-sensitive modules, data-access layer, architectural seams, cross-cutting infrastructure, and a small spot-sample of business logic.

Mark every sampled path in the report. For un-sampled areas, cap scores at 6 and call out the gap in the assessment line. Do not extrapolate.

### 3. Inspect the code, not the docs

Open files. Trace flows. Sample tests. Rubric anchors are about what *is* there, not what is *claimed*.

### 4. Score Maintainability (4 attributes)

Score each on the skill's 0-10 anchor scale, citing file paths or patterns:

- **Analyzability** (FIASSE v1.0.4 S3.2.1.1) — clarity, complexity, naming, structure
- **Modifiability** (FIASSE v1.0.4 S3.2.1.2) — coupling, cohesion, separation of concerns, no static mutable state
- **Testability** (FIASSE v1.0.4 S3.2.1.3) — coverage of security-critical paths, mockability, independence
- **Observability** (FIASSE v1.0.4 S3.2.1.4) — log coverage at boundaries, code-level instrumentation, failure-path visibility

### 5. Score Trustworthiness (3 attributes)

- **Confidentiality** (FIASSE v1.0.4 S3.2.2.1) — secrets, PII handling, least privilege, encryption at rest/in transit
- **Accountability** (FIASSE v1.0.4 S3.2.2.2) — audit-trail completeness, structured logging, action traceability
- **Authenticity** (FIASSE v1.0.4 S3.2.2.3) — auth mechanisms, token integrity, non-repudiation

### 6. Score Reliability (3 attributes)

- **Availability** (FIASSE v1.0.4 S3.2.3.1) — resource limits, timeouts, rate limiting, graceful degradation
- **Integrity** (FIASSE v1.0.4 S3.2.3.2) — input handling, parameterized queries, Derived Integrity (FIASSE v1.0.4 S4.4.1.2), Request Surface Minimization (FIASSE v1.0.4 S4.4.1.1)
- **Resilience** (FIASSE v1.0.4 S3.2.3.3) — specific exception handling, defensive coding, deterministic disposal

### 7. Apply pattern tagging

For each weakness, name the principle violated using the **Pattern Tag Reference** in the skill. "Derived Integrity violation (FIASSE v1.0.4 S4.4.1.2)" is actionable; "the auth is sketchy" is not.

### 8. Apply the Four-Question Framework at the code level (FIASSE v1.0.4 S4.2.1)

Use static-analysis findings as starting points, then think deeper:

1. What are we building?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good job?

Map solutions back to SSEM attributes — prefer architectural fixes over line-level patches when the same root cause produces multiple findings.

### 9. Assess dependency stewardship

Per FIASSE v1.0.4 S4.5 (Management) and S4.6 (Stewardship), evaluate:

- Documented rationale for inclusion
- Pinned versions / lockfiles
- Known transitive dependencies
- Maintenance signals (release cadence, maintainer activity, CVE response)
- Whether the dependency would remain trustworthy a year from now (Stewardship)

### 10. Compute scores

- Pillar score = simple average of attribute scores
- Overall SSEM score = (Maintainability + Trustworthiness + Reliability) / 3

Show the math in the report.

### 11. Classify each finding's severity

Use the severity table in the skill — engineering-impact based, not CVSS. Severities are CRITICAL / HIGH / MEDIUM / LOW / INFO.

### 12. Assemble the three-part report

Use the output format and checklist defined in the skill:

- **Part 1**: SSEM Score Summary (overall, pillars, attribute breakdown tables, top 3 strengths, top 3 improvements)
- **Part 2**: Detailed Findings per pillar (use [templates/finding.md](../../templates/finding.md) for individual findings)
- **Part 3**: 50-item Evaluation Checklist (Maintainability 20, Trustworthiness 15, Reliability 15)

Use [templates/report.md](../../templates/report.md) as the assembly scaffold.

## Quality Gates

- [ ] Scope, language, and exposure captured before scoring
- [ ] Sampling discipline declared (file paths inspected; un-sampled areas capped at 6)
- [ ] Every one of the 10 attributes has a 0-10 score with code-anchored evidence
- [ ] Pillar arithmetic shown
- [ ] Every weakness tagged to a FIASSE v1.0.4 principle where applicable
- [ ] Severity assigned to every finding
- [ ] 50-item checklist completed with inline notes on failing items

## References

- [skills/securability-engineering-review/SKILL.md](../../skills/securability-engineering-review/SKILL.md) — rubric, weights, severity, output format, 50-item checklist, pattern tags, anti-patterns
- [templates/finding.md](../../templates/finding.md) — individual finding shape
- [templates/report.md](../../templates/report.md) — full-report scaffold
- [FIASSE Framework v1.0.4](https://github.com/OWASP/FIASSE/blob/v1.0.4/docs/securable_framework.md)
- ISO/IEC 25010:2011 — Software quality models
- RFC 4949 — Internet Security Glossary
