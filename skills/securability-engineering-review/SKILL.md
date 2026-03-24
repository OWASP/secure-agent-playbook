---
name: securability-engineering-review
description: Analyze code for securable qualities using the OWASP FIASSE/SSEM framework. Use when assessing code securability, evaluating engineering attributes that impact security (analyzability, modifiability, testability, confidentiality, accountability, authenticity, availability, integrity, resilience), reviewing merge requests through a securable engineering lens, or establishing a security posture baseline. Complements vulnerability-centric reviews by focusing on whether code is able to accommodate fixes for security findings and is engineered to remain securable over time.
license: CC-BY-4.0
---

# Securable Code Analysis (OWASP FIASSE/SSEM)

Analyze code for securable engineering qualities by following the full procedure in `plays/tier1-code-analysis/securability-engineering-review.md`.

## Scoring Framework

Each SSEM attribute is scored **0–10**. Pillar scores are calculated using weighted sub-attribute scores. The overall SSEM score is the weighted average of the three pillar scores.

### Pillar Weights

| Pillar | Weight | Sub-Attributes (Weight) |
|--------|--------|------------------------|
| **Maintainability** | 33% | Analyzability (40%), Modifiability (30%), Testability (30%) |
| **Trustworthiness** | 34% | Confidentiality (35%), Accountability (30%), Authenticity (35%) |
| **Reliability** | 33% | Availability (25%), Integrity (35%), Resilience (40%) |

**Overall SSEM Score** = (Maintainability × 0.33) + (Trustworthiness × 0.34) + (Reliability × 0.33)

### Grading Scale

| Score Range | Grade | Description |
|-------------|-------|-------------|
| 9.0 – 10.0 | **Excellent** | Exemplary implementation, minimal improvement needed |
| 8.0 – 8.9 | **Good** | Strong implementation, minor improvements beneficial |
| 7.0 – 7.9 | **Adequate** | Functional but notable improvement opportunities exist |
| 6.0 – 6.9 | **Fair** | Basic requirements met, significant improvements needed |
| < 6.0 | **Poor** | Critical deficiencies requiring immediate attention |

### Severity Classification for SSEM Deficits

| Severity | Criteria |
|----------|---------|
| CRITICAL | Attribute deficit directly enables exploitation or prevents incident response |
| HIGH | Attribute deficit significantly increases probability of material impact |
| MEDIUM | Attribute deficit degrades securability but does not directly enable attack |
| LOW | Attribute deficit is a code quality concern with indirect security implications |
| INFORMATIONAL | Positive observation or minor improvement opportunity |

## Steps

1. **Scope & Context** — Establish language/framework, system type, data sensitivity, exposure, lifecycle stage, and team context.

2. **SSEM Attribute Assessment — Maintainability**:
   - **Analyzability** — Volume, duplication, unit size, cyclomatic complexity, comment density, time-to-understand
   - **Modifiability** — Module coupling, change impact size, regression rate, centralized security code
   - **Testability** — Code coverage, unit test density, mocking complexity, component independence

3. **SSEM Attribute Assessment — Trustworthiness**:
   - **Confidentiality** — Data classification, least privilege, encryption at rest/in transit, no sensitive data in logs
   - **Accountability** — Structured audit logging, immutable trails, entity traceability
   - **Authenticity** — Strong authentication, token integrity, mutual service auth, non-repudiation

4. **SSEM Attribute Assessment — Reliability**:
   - **Availability** — Redundancy, resource limits, rate limiting, timeouts, health checks
   - **Integrity** — Input validation at trust boundaries, output encoding, Derived Integrity Principle, Request Surface Minimization
   - **Resilience** — Defensive coding, predictable execution, strong trust boundaries, fault tolerance, error handling

5. **Transparency Assessment** — Self-documenting code, structured logging, audit trails, instrumentation, trust boundary logging.

6. **Code-Level Threat Identification** — Apply "What can go wrong?" using the Four Question Framework; map solutions to SSEM attributes.

7. **Dependency Securability** — Evaluate dependencies against SSEM attributes (analyzability, modifiability, testability, trustworthiness, reliability).

8. **Produce Findings** — Score each sub-attribute 0–10 using rubrics, calculate weighted pillar scores and overall SSEM score, assign grade (Excellent/Good/Adequate/Fair/Poor), generate SSEM Score Summary, detailed findings per pillar with expected improvement estimates, and 45-item evaluation checklist.

## Output

Part 1: SSEM Score Summary (overall score, grade, pillar breakdown with weights, top strengths, top improvement opportunities). Part 2: Detailed Findings per pillar (strengths with evidence, weaknesses with examples, recommendations with priority and expected point improvement). Part 3: Appendix A — 45-item Evaluation Checklist (15 per pillar) with pass/fail summary percentages. Severity count table.

## OWASP References

- [OWASP FIASSE Project](https://owasp.org/www-project-fiasse/) — Tools and resources for FIASSE/SSEM
- [FIASSE](https://github.com/Xcaciv/securable_software_engineering/blob/main/docs/secureable_framework.md) — Framework for Integrating Application Security into Software Engineering
- ISO/IEC 25010:2011 — Software quality models (Maintainability, Reliability definitions)
- RFC 4949 — Internet Security Glossary (Trustworthiness, Integrity, Availability definitions)
- OWASP Code Review Guide
- OWASP Proactive Controls
- OWASP Top 10 (2021)
- OWASP ASVS v5.0
