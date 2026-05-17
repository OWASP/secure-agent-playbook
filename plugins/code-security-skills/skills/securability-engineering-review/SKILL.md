---
name: securability-engineering-review
description: Score a codebase, file, or merge request against the FIASSE v1.0.4 SSEM model — 0-10 per attribute, equal-weighted pillars, evidence-backed strengths and weaknesses, prioritized recommendations, 50-item checklist appendix. Trigger on "review/score/audit securability", "SSEM scorecard", "FIASSE/SSEM compliance", "where would I start hardening this?", "is this audit-ready?", "security posture baseline" — including phrasings that don't say SSEM explicitly. For requirements use prd-securability-enhancement; for new code use securability-engineering.
license: CC-BY-4.0
---

# SSEM Evaluation (Scoring and Reporting)

Analyze code for securable engineering qualities and produce a structured SSEM scorecard. This file is **authoritative** for the rubric, weights, severity classification, and report shape. The play at [plays/securability-engineering-review.md](../../plays/securability-engineering-review.md) is the step-by-step runbook; consult it for *when* to do each step, not for *what* the rubric says.

Aligned with [FIASSE v1.0.4](https://github.com/OWASP/FIASSE/blob/v1.0.4/docs/securable_framework.md). Per-attribute measurement guidance in `data/fiasse/SA.*.md` (Appendix A).

## When to Invoke

Trigger this skill when the user asks to:

- Assess, audit, score, rate, or evaluate the **securability** of code
- Produce an **SSEM scorecard** or SSEM evaluation report
- Review a merge request / pull request through a **securable engineering** lens
- Establish a **security posture baseline** for a project
- Identify **engineering quality** issues that affect security (not vulnerability-centric)
- Answer "where would I start hardening this codebase?"
- Check **FIASSE/SSEM compliance**

Adjacent phrasings: "rate this code for security", "is this audit-ready?", "what's the security health of X?", "how securable is this?", "do a sec-engineering review", "give me a posture report".

## Scoring Framework

Each attribute is scored **0-10**. Pillar scores are simple averages of their attribute scores. The overall SSEM score is the simple average of the three pillar scores.

### Pillars and Attributes (FIASSE v1.0.4 — 10 attributes, equal weights)

| Pillar | Pillar Weight | Attributes | Per-Attribute Weight |
|--------|---------------|------------|----------------------|
| **Maintainability** | 1/3 | Analyzability, Modifiability, Testability, Observability | 1/4 each |
| **Trustworthiness** | 1/3 | Confidentiality, Accountability, Authenticity | 1/3 each |
| **Reliability** | 1/3 | Availability, Integrity, Resilience | 1/3 each |

**Pillar score** = average of its attribute scores.
**Overall SSEM score** = (Maintainability + Trustworthiness + Reliability) / 3.

Equal weighting reflects FIASSE v1.0.4's stance that no SSEM attribute is intrinsically more important than another — context-specific severity is captured in *findings*, not in the rubric.

### Scoring Rubric (Anchor Points)

| Score | Anchor |
|-------|--------|
| **10** | Exemplary implementation |
| **8**  | Strong implementation with minor issues |
| **6**  | Adequate implementation with notable gaps |
| **4**  | Weak implementation with significant issues |
| **2**  | Minimal or poor implementation |

Interpolation between anchors is allowed when justified by evidence. Stay consistent with the rubric language.

### Attribute Inventory (the 10 scored items)

Every report MUST produce a numeric 0-10 score for each of these:

**Maintainability**
1. **Analyzability** (FIASSE v1.0.4 S3.2.1.1) — clarity, complexity, naming, structure
2. **Modifiability** (FIASSE v1.0.4 S3.2.1.2) — coupling, cohesion, separation of concerns
3. **Testability** (FIASSE v1.0.4 S3.2.1.3) — coverage, mockability, independence
4. **Observability** (FIASSE v1.0.4 S3.2.1.4) — log coverage, instrumentation, failure-path visibility

**Trustworthiness**
5. **Confidentiality** (FIASSE v1.0.4 S3.2.2.1) — sensitive-data handling, least privilege, encryption
6. **Accountability** (FIASSE v1.0.4 S3.2.2.2) — audit trails, action traceability
7. **Authenticity** (FIASSE v1.0.4 S3.2.2.3) — identity verification, token integrity, non-repudiation

**Reliability**
8. **Availability** (FIASSE v1.0.4 S3.2.3.1) — resource limits, timeouts, graceful degradation
9. **Integrity** (FIASSE v1.0.4 S3.2.3.2) — input handling, parameterized queries, derived state
10. **Resilience** (FIASSE v1.0.4 S3.2.3.3) — error handling, recovery, defensive coding

### Grading Scale

| Score Range | Grade | Description |
|-------------|-------|-------------|
| 9.0–10.0 | **Excellent** | Exemplary implementation, minimal improvement needed |
| 8.0–8.9 | **Good** | Strong implementation, minor improvements beneficial |
| 7.0–7.9 | **Adequate** | Functional but notable improvement opportunities exist |
| 6.0–6.9 | **Fair** | Basic requirements met, significant improvements needed |
| < 6.0 | **Poor** | Critical deficiencies requiring immediate attention |

### Severity Classification (for individual findings)

Severity is an **engineering-impact** judgment, not a CVSS or CWE score. FIASSE does not borrow assurance-tool severity scales. Classify each finding by its effect on SSEM scores and on the system's ability to remain securable.

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | A pillar score is held ≤4 because of this finding *alone*; or an attribute scores ≤2 due to systemic absence (e.g., no input validation anywhere, no audit trail, ambient client-trust). Remediation requires architectural change. |
| **HIGH** | A single attribute scores ≤4 due to this finding; or the finding reduces a pillar score by ≥1.5 points. Localized but pervasive (e.g., string-built SQL across one service). |
| **MEDIUM** | Reduces a single attribute by ~1 point; specific module or pattern. Remediation contained to one module. |
| **LOW** | Localized engineering improvement; ≤0.5 score impact. |
| **INFO** | Best-practice observation; no measurable score impact. |

## Required Inputs

If the repository or input is incomplete, ask for these before scoring:

- Project name and short description
- Programming language(s) and framework(s)
- Architecture overview (one paragraph is enough)
- Repository URL or codebase access (or pasted code)
- Any existing documentation, test posture, or prior assessments worth incorporating

If essential context is missing, **score conservatively and state the limitation explicitly**. Do not invent coverage, architecture, or operational controls.

## Triage and Sampling Strategy (for codebases > a few thousand LoC)

Full read-through is impossible at scale. Sample deliberately and **declare what was sampled**. The report's credibility rests on the sampling discipline, not on claimed totality.

Inspection priority order:

1. **Trust boundaries** — every entry point: HTTP handlers, queue consumers, RPC servers, file ingestors, CLI flag parsers. Boundaries are where Integrity, Authenticity, and Confidentiality scores are won or lost.
2. **Security-sensitive modules** — auth, authz, crypto, session, secrets handling, audit logging, error/logging glue.
3. **Data-access layer** — query construction, ORM usage, file-path joining, deserialization.
4. **Architectural seams** — public interfaces, dependency-injection wiring, configuration loaders, feature-flag plumbing.
5. **Cross-cutting infrastructure** — health endpoints, metrics, tracing, scheduled jobs.
6. **Spot-sample of business logic** — pick 2–3 representative modules; do not exhaustively grade what you didn't read.

For each sampled area, mark the report with the file paths actually inspected. For un-sampled areas, **score conservatively (cap at 6) and call out the gap in the assessment line**. Do not extrapolate from sampled to un-sampled with confidence.

For very large repos, scope the review to a single service / package / module and say so in the scope statement. A focused scorecard is worth more than a vague one covering everything.

## Procedure

The full step-by-step runbook lives in [plays/securability-engineering-review.md](../../plays/securability-engineering-review.md). The high-level shape:

1. **Scope and context** — language, framework, system type, data sensitivity, exposure, lifecycle, team context.
2. **Inspect the code, not the docs** — open files; trace flows; sample tests. Anchors are about what *is* there, not what is *claimed*.
3. **Score each pillar** — Maintainability (4 attributes), Trustworthiness (3), Reliability (3). Cite specific file paths or patterns, not generalities.
4. **Compute scores** — attribute → pillar (simple average) → overall (simple average). Show the math.
5. **Assemble the report** — three-part structure below, exactly.

## Output Format

The report must contain exactly these three parts in order. Do not skip parts even on small reviews.

### Part 1: SSEM Score Summary

A compact summary block. The exact ASCII shape can flex (Markdown tables are also acceptable when the review is short), but it must include:

- Project name and date
- Overall SSEM score, grade, and a one-line status assessment
- Pillar summary (Maintainability / Trustworthiness / Reliability) — each with score, grade, and a one-line key finding
- Maintainability breakdown table — 4 attributes (Analyzability, Modifiability, Testability, Observability), each with weight (25%), score, and short assessment
- Trustworthiness breakdown table — 3 attributes (Confidentiality, Accountability, Authenticity), each with weight (33.3%), score, and assessment
- Reliability breakdown table — 3 attributes (Availability, Integrity, Resilience), each with weight (33.3%), score, and assessment
- **Top 3 strengths** with concrete evidence (file path, pattern name, or short quote)
- **Top 3 improvement opportunities** with concrete recommendations

### Part 2: Detailed Findings

Per pillar, write:

- Pillar name, score, grade
- **Strengths**: bullets with specific evidence (file:line, pattern, observation)
- **Weaknesses**: bullets with concrete examples or locations and an impact note
- **Recommendations**: numbered list using this shape:
  ```
  1. **[Title]** (Severity: CRITICAL/HIGH/MEDIUM/LOW/INFO)
     - Issue:    [Specific problem]
     - Impact:   [Effect on the pillar score and on the system]
     - Solution: [Actionable steps]
     - Expected Improvement: +[X.X] points
  ```

For per-finding format, use [templates/finding.md](../../templates/finding.md).
For full-report scaffold, use [templates/report.md](../../templates/report.md).

### Part 3: Appendix A — Evaluation Checklist (50 items)

The official checklist:

- **Maintainability (20 items)**: Analyzability (5), Modifiability (5), Testability (5), Observability (5)
- **Trustworthiness (15 items)**: Confidentiality (5), Accountability (5), Authenticity (5)
- **Reliability (15 items)**: Availability (5), Integrity (5), Resilience (5)

Mark each `[x]` (passing) or `[ ]` (failing) with a brief inline note when failing.

End with a checklist summary:

- Maintainability: N/20 passing (NN%)
- Trustworthiness: N/15 passing (NN%)
- Reliability: N/15 passing (NN%)
- **Overall: N/50 passing (NN%)**

## Worked Example (Mini)

**Snippet under review** (Python, ~12 lines):

```python
@app.post("/notes/{note_id}")
def update_note(note_id, body):
    sql = f"UPDATE notes SET body = '{body}' WHERE id = {note_id}"
    db.execute(sql)
    print("note updated " + note_id)
    return {"ok": True}
```

**Analyzability** — `4/10` (weak). Single-purpose handler but unsafe string formatting; no input typing; no early returns; conflates parsing, persistence, and response shaping.
*Evidence*: `f"UPDATE notes SET body = '{body}' WHERE id = {note_id}"`.

**Observability** — `2/10` (minimal). `print(...)` is not structured output. No correlation ID, no actor, no outcome field. Failure paths are silent.
*Evidence*: `print("note updated " + note_id)`.

**Integrity** — `2/10` (minimal). SQL injection via string interpolation; no parameterized queries; no ownership check (any caller can update any note ID — Derived Integrity violation per FIASSE v1.0.4 S4.4.1.2).
*Evidence*: same line as above; no `current_user` derivation.

**Accountability** — `3/10` (weak). `print` is not an audit log; missing actor, action verb, target ID type-tagged, and outcome.
*Evidence*: `print("note updated " + note_id)`.

**Recommendation (HIGH)** — Replace the f-string with a parameterized query that scopes by owner, and emit a structured `note.update` log with `{actor, note_id, outcome}`. Expected improvement: Integrity +5, Accountability +3, Observability +4, Analyzability +2.

This is the level of specificity the report should hit at scale — every score paired with a code-anchored observation, every weakness with a remediation that names the change.

## Pattern Tag Reference

When you find one of these patterns, tag the finding with the FIASSE/SSEM principle it violates. Specific named tagging is what makes a report actionable — saying "the code mishandles auth" is weak; saying "this is a Derived Integrity violation (FIASSE v1.0.4 S4.4.1.2) — the server's authorization decision rests on a client-asserted JWT claim" is strong.

| Pattern observed in code | Principle / attribute violated | Tag in finding |
|---|---|---|
| Server decides who-can-do-what based on a client-asserted claim (`req.user.email`, `request.body.user_id`, `X-Tenant-ID` header) | Integrity — **Derived Integrity Principle** (FIASSE v1.0.4 S4.4.1.2) | "Derived Integrity violation" |
| Spread of `req.body` / `**kwargs` directly into a database update or model field-set | Integrity — **Request Surface Minimization** (FIASSE v1.0.4 S4.4.1.1) | "Request Surface Minimization violation; mass assignment" |
| String-built SQL or shell commands; format strings with user input | Integrity — input handling at trust boundary (FIASSE v1.0.4 S4.4.1, S4.3) | "Trust boundary input handling" |
| Path joined with user-controlled segment without `..`/separator validation | Integrity — trust boundary; canonicalize → sanitize → validate (FIASSE v1.0.4 S4.4.1) | "Path canonicalization gap" |
| `jwt.verify` with no pinned algorithms / no audience / no issuer; or using a default-allow algorithm list | Authenticity (token integrity) | "Token verification under-specified" |
| `console.log` / `print` / `fmt.Println` standing in for an audit trail; missing actor, target, outcome, request id | Accountability + Observability (FIASSE v1.0.4 S2.5, S3.2.1.4) | "Unstructured audit trail" |
| Bare `except:` / `catch (e)` returning raw exception text to the client | Resilience (graceful degradation); Confidentiality (info leakage) | "Specific exception handling missing" |
| Module-level globals (DB connection, app, config) created at import time | Modifiability (loose coupling); Testability (mockability) | "Import-time side effects" |
| `ioutil.ReadAll(r.Body)` / unlimited request body buffer | Availability + Resilience (resource limits) | "Unbounded resource consumption" |
| Pervasive `any` typing on the trust-boundary surface (TypeScript / dynamic langs) | Analyzability; Integrity (validation) | "Trust-boundary type erasure" |
| Silent `try { … } catch {}` / failure paths that emit no log or metric | Observability (failure-path visibility) (FIASSE v1.0.4 S3.2.1.4) | "Silent failure" |
| Health/metrics endpoints absent; readiness/liveness derived from external probes only | Observability (instrumentation built into code, not bolted on externally) (FIASSE v1.0.4 S3.2.1.4) | "External-only instrumentation" |

You don't need this whole table inline in every report. But when one of these patterns is *present*, the finding should name the principle by tag — not just describe the symptom.

## Anti-Patterns (Things That Make a Report Useless)

- **Fabricated evidence**: don't cite line numbers or function names you didn't actually read. If something is unverified, mark the score as conservative and call out the gap explicitly.
- **All-7s scoring**: if every attribute lands at the same number, you haven't actually evaluated. Some attributes will be stronger than others; the report should reflect that.
- **Vulnerability-centric drift**: this is *not* a CWE pentest report. SSEM scores engineering attributes (analyzability, modifiability, etc.). A finding's value is in the *engineering improvement*, not the exploit recipe.
- **Generic recommendations**: "improve error handling" is not actionable. "Replace bare `except:` at app/handlers.py:42 with `except (ValidationError, NotFound) as e:`" is.
- **Score without code access**: if you can't see the code, say so and refuse to score that pillar — don't extrapolate.
- **Missing the math**: pillar scores must show how they were derived from attribute scores. Don't leave the reader guessing.
- **Claiming totality on a sample**: if you sampled 5 of 50 modules, do not score as if you read all 50. Mark sampled paths and cap un-sampled scores at 6.

## Required Evaluation Criteria

Always:

- Be specific. Reference observable code or architecture evidence by file path or function name.
- Apply equal weights (1/3 per pillar; 1/4 within Maintainability; 1/3 within Trustworthiness and Reliability).
- Keep recommendations actionable — the reader should be able to open a PR from your text.
- Consider project size, domain, architecture, and intended use when scoring against rubric anchors.
- If evidence is insufficient, score conservatively and **state the limitation in the assessment line for that attribute**.

## Invocation Behavior

When invoked:

1. Ask for missing project information if context is incomplete.
2. Apply the triage strategy if the codebase is large; otherwise inspect comprehensively.
3. Score against the rubric using the procedure above.
4. Produce the three-part report exactly as specified.
5. Use repository evidence over assumptions; declare gaps where evidence is missing.

## FIASSE & OWASP References

- [FIASSE Framework v1.0.4](https://github.com/OWASP/FIASSE/blob/v1.0.4/docs/securable_framework.md)
- FIASSE v1.0.4 SA.* — Appendix A (per-attribute measurement guidance) in `data/fiasse/SA.*.md`
- ISO/IEC 25010:2011 — Software quality models
- RFC 4949 — Internet Security Glossary
- OWASP Code Review Guide
- OWASP ASVS v5.0 — `data/asvs/`
- Step-by-step runbook: [plays/securability-engineering-review.md](../../plays/securability-engineering-review.md)
- Finding format: [templates/finding.md](../../templates/finding.md)
- Report scaffold: [templates/report.md](../../templates/report.md)
