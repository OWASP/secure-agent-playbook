---
name: prd-securability-enhancement
description: Enhance PRDs, feature specs, user stories, or product briefs with explicit OWASP ASVS coverage and FIASSE v1.0.4 SSEM implementation guidance — before code is written. Trigger on "harden the PRD/spec", "choose ASVS level", "map features to ASVS", "find missing security requirements", "add NFRs for security", "make these requirements securable", "security-review my product brief". For code review use securability-engineering-review; for code generation use securability-engineering.
license: CC-BY-4.0
---

# PRD Securability Enhancement (FIASSE/SSEM + ASVS)

Enhance PRD content so each feature has explicit, testable securability requirements aligned to OWASP ASVS and shaped by FIASSE v1.0.4 / SSEM. The goal is to upgrade the requirements artifact *before* implementation, so delivery teams build securable capabilities by design rather than retrofitting controls later.

This skill is requirements-centric. It does not review or write code. If the user wants code review, redirect to `securability-engineering-review`. If they want code generation, redirect to `securability-engineering`.

## When to Invoke

Trigger this skill when the user asks to:

- Strengthen or harden a PRD, spec, user-story set, or product brief with security requirements
- Choose an ASVS assurance level (Level 1, 2, or 3) for a product or feature
- Map features to ASVS controls or check ASVS coverage of a requirements doc
- Find missing security requirements before development starts
- Annotate features with SSEM attributes or FIASSE tenets
- Add testable security acceptance criteria to existing functional requirements

Adjacent phrasings: "security-review this spec", "what's missing security-wise from this feature list", "add NFRs for security to my PRD", "make these requirements securable".

## Inputs

Ask the user for whatever is missing before starting:

- The PRD, spec, or feature list (markdown, prose, ticket export, etc.)
- System context: user types, deployment model, data sensitivity, integration surfaces
- Compliance or risk context, if any (HIPAA, PCI, SOC 2, regulated industry)
- Whether they have an ASVS level preference, or want this skill to recommend one

If the artifact is large, parse the features inline; do not require the user to pre-extract them.

## Procedure

### Step 1 — Parse features

Extract each feature into a normalized record. Capture for each:

- Feature ID and title (assign IDs like `F-01` if absent)
- Actor (user role, system, external service)
- Data touched and sensitivity class
- Trust boundaries crossed (browser↔server, service↔service, server↔storage, internal↔external)
- Existing acceptance criteria (verbatim, even if weak)

If the source PRD lumps several capabilities into one bullet, split them so each feature is independently testable.

### Step 2 — Choose the ASVS level *first*

Selecting the level before mapping requirements prevents both under-scoping and over-scoping. Use this rubric:

| Level | Use when |
|-------|----------|
| **1** | Internal tooling, prototypes, low-sensitivity data, no regulatory pressure, limited blast radius if compromised |
| **2** | Typical production web/API systems with authenticated users, business-critical behavior, customer data, or moderate regulatory exposure (most products land here) |
| **3** | High-assurance contexts: payments, health records, government, identity providers, anything where compromise causes severe material impact or where attackers are well-resourced |

Default to Level 2 unless evidence pushes lower or higher. Document:

- Chosen level
- Why lower levels are insufficient (when level > 1)
- Any specific features that should escalate above the baseline (e.g., a payments endpoint inside a Level-2 product gets Level-3 treatment)

### Step 3 — Map each feature to ASVS

For every feature, use `data/asvs/README.md` (chapter index) and the `when_to_use` frontmatter in `data/asvs/V*.md` to identify applicable chapters. Common mappings:

- Auth flows → V2 (Authentication), V3 (Session Management)
- Authorization, ownership, multi-tenant scoping → V4 (Access Control)
- File upload/download → V5 (File Handling)
- Crypto, password storage, tokens → V6 (Cryptography)
- Logging, error handling, observability → V7 (Error/Logging)
- PII, data at rest/in transit → V8 (Data Protection), V14 (Secure Communication)
- Public APIs → V9 (API/Web Services)
- Config, secrets, deployment → V10 (Configuration)
- Workflow rules, anti-automation → V11 (Business Logic)
- Any user/external input → V12 (Input Validation)
- Anything rendered or returned to a client → V13 (Output Encoding)
- Sensitive data lifecycle → V16 (Sensitive Data)

Filter requirements by the chosen ASVS level. For each requirement, classify coverage:

- **Covered** — the PRD already satisfies the intent
- **Partial** — partly covered; clarify or strengthen acceptance criteria
- **Missing** — requirement absent and must be added
- **N/A** — justified with a one-line rationale

Use the **ASVS Coverage Gap Pattern Table** below to spot the gaps that PRDs reliably miss.

### Step 4 — Add Securability Notes per feature

Write a *short* paragraph per feature surfacing only the SSEM and FIASSE points that materially shape implementation. Do not enumerate all ten SSEM attributes or all FIASSE tenets — that produces noise.

Useful lenses (mention only when relevant):

- Trust-boundary handling and input canonicalization (FIASSE v1.0.4 S4.3, S4.4.1)
- Derived Integrity — never trust client-supplied values for server-owned state (FIASSE v1.0.4 S4.4.1.2)
- Request Surface Minimization — process only the named values you expect (FIASSE v1.0.4 S4.4.1.1)
- Observability: what must be logged or auditable (FIASSE v1.0.4 S3.2.1.4 + Accountability; Transparency S2.5)
- Least Astonishment — predictable behavior at trust boundaries and error paths (FIASSE v1.0.4 S2.6)
- Resilience or availability drivers (rate limits, timeouts, graceful and **secure** failure)
- Testability or modifiability mandates (e.g., centralizing crypto/auth in a dedicated module)
- Dependency stewardship — ongoing relationship with third-party code (FIASSE v1.0.4 S4.6)

### Step 5 — Convert into testable acceptance criteria

For each added or strengthened requirement, write at least one acceptance criterion that is:

- Behaviorally observable (a test or audit can confirm pass/fail)
- Specific about boundary conditions (failure modes, unauthorized actors, malformed input)
- Tied to a verifiable artifact (log line, response code, denied action)

Ambiguous "secure" or "robust" language is not acceptable here.

### Step 6 — Emit the enhanced PRD artifact

Produce these sections in order, using the exact templates below.

## ASVS Coverage Gap Pattern Table

These are the gaps PRDs reliably miss. When you see one of the trigger phrasings on the left, add the named requirements on the right — they are almost always missing in the source artifact.

| PRD trigger phrasing (what the feature *says*) | Almost-always-missing requirements | ASVS section | Tag |
|---|---|---|---|
| "User logs in with email and password" | Account-enumeration parity (same response/timing for valid vs invalid email); password-screen against breached-password list; auth-event audit log; per-account brute-force rate limit | V6.3.8, V2.1, V2.4, V16.3 | "Auth surface gaps" |
| "User resets/forgets password" | Account-enumeration parity on the request endpoint; single-use token; short expiry (≤15 min); token-hash-at-rest; rate-limit per email and per IP; audit log of issuance/redemption | V6.3.8, V6.2, V2.4, V16.3 | "Reset flow gaps" |
| "User uploads a file" | Type allow-list (not deny-list); content-sniffing vs declared type; max size; antivirus/safe-storage path; filename canonicalization; storage outside web root; URL non-guessability | V5.1, V5.2, V12.1 | "Upload gaps" |
| "User can edit their profile" / "update settings" | Allow-listed mutable fields (no `email`/`role`/`is_admin` from request body); ownership check on the resource; audit log of changes; old-vs-new value capture | V4.1, V4.2, V16.2, V16.3 | "Mass-assignment gaps" |
| "Admin can do X" / "role-based access" | Authorization decision logged with grant/deny; centralized authz module (not scattered checks); deny-by-default at boundary; ownership scoping on every record fetch | V4.1, V4.2, V16.2, V16.3 | "Authz gap" |
| "Public API endpoint" / "third-party integration" | Per-key/per-client rate limits; auth for every call (not first-call only); request-id propagation; response field allow-list (no leaking internal fields); contract validation | V2.4, V9.1, V13.1, V16.2 | "API gaps" |
| "Send email/SMS to user" | Templated payload with no user-controlled subject/body injection; rate-limit per recipient and per actor; bounce/abuse-loop handling; opt-out and audit log | V2.4, V12.1, V13.1, V16.3 | "Outbound-message gaps" |
| "Search / filter / list with user-supplied parameters" | Parameter allow-list; ordering/pagination caps; query timeout; result count cap; tenant/owner scoping enforced server-side | V4.1, V12.1, V13.1 | "Query-surface gaps" |
| "Webhook receiver" / "callback URL" | Source verification (signature, mTLS, IP allow-list); replay protection (timestamp + nonce); idempotency key; rate-limit; audit log of received events | V2.4, V2.5, V9.1, V16.3 | "Webhook gaps" |
| "Save user file/document/note" | Owner identifier never client-supplied; size and content caps; rich-text/HTML sanitization on read or write; audit log of writes | V4.1, V5.1, V12.1, V16.3 | "Server-owned state gaps (Derived Integrity)" |
| "Export data" / "download report" | Authorization re-checked on export (not just on UI route); rate-limit; audit log including row count; PII-scrub policy if applicable | V4.1, V7.1.1, V8.1 | "Export gaps" |
| "Background job processes user-submitted data" | Same boundary discipline as the synchronous path (validation, surface minimization, owner scoping); job-level audit log; poison-message handling and DLQ | V11.1, V12.1, V7.1.1 | "Async-path boundary gaps" |
| "Configuration / feature flag / admin setting" | Change requires authenticated actor and audit record; cannot be set via product API without admin role; secret values never echoed back; defaults are safe | V7.1.1, V10.1, V14.2 | "Config-surface gaps" |
| "PII/PHI/financial data" mentioned anywhere | Field-level classification; encryption at rest and in transit; retention/disposal policy; access-log requirement; export/erasure (right-to-be-forgotten) flows | V8.1, V14.1 | "Sensitive-data lifecycle gaps" |
| "Real-time" / "websocket" / "streaming" feature | Per-connection auth (not just first message); per-connection resource caps; back-pressure / max-queue; idle timeout; audit of connection lifecycle | V3.1, V9.1, V11.1.4 | "Streaming gaps" |
| "AI/LLM-backed feature" | Prompt-injection handling at trust boundary; output validation before downstream side effects; per-actor rate limit and cost cap; audit log of prompts and tool calls; PII redaction policy | V11.1, V12.1, V8.1 | "LLM boundary gaps" |

When a feature triggers one of these patterns, prefill the corresponding requirements as **Missing** in the coverage matrix unless the PRD explicitly addresses them — most of the time it doesn't.

## Output Templates

### A. ASVS Level Decision

```markdown
## ASVS Level Decision

**Chosen Level**: [1 | 2 | 3]

**Rationale**: [2–4 sentences. Cover data sensitivity, user population, regulatory context, and material-impact reasoning. Note why lower levels are insufficient if Level > 1.]

**Feature-Level Escalations**: [List any features that need a higher level than baseline, with one-line justification, or "None".]
```

### B. Coverage Matrix

```markdown
## Feature ↔ ASVS Coverage Matrix

| Feature | ASVS Section | Requirement ID | Level | Coverage | PRD Change Needed |
|---------|--------------|----------------|-------|----------|-------------------|
| F-01    | V2.2         | 2.2.1          | 2     | Missing  | Add MFA requirement for high-risk actions |
| F-01    | V7.1         | 7.1.1          | 2     | Partial  | Specify which auth events are logged |
| F-02    | V12.1        | 12.1.1         | 2     | Covered  | — |
```

Aim for completeness over brevity here — every feature × every applicable requirement gets a row. Where the gap pattern table applies, include the named requirements it surfaces.

### C. Enhanced Feature Specifications

For each feature, emit exactly this shape:

```markdown
### Feature F-01: [Title]

**Actor**: [user role / system]
**Data**: [data classes touched]
**Trust Boundaries**: [boundaries crossed]

**ASVS Mapping**: V2.2.1, V7.1.1, ...

**Updated Requirements**:
- [Original requirement, kept or rewritten]
- [Newly added requirement from ASVS mapping]
- [Newly added requirement from ASVS mapping]

**Acceptance Criteria**:
- [Testable criterion tied to a requirement above]
- [Testable criterion tied to a requirement above]

**Securability Notes**: [Short paragraph — only material SSEM/FIASSE points for this feature. Do not enumerate all attributes.]
```

### D. Cross-Cutting Securability Requirements

Controls that span multiple features (centralized logging, secrets management, dependency policy, baseline TLS, error-handling standards). One bullet each, with the ASVS reference.

### E. Open Gaps and Assumptions

Anything you could not resolve from the input: missing system context, unclear data sensitivity, unstated user populations, deferred decisions. Be explicit so the team can close these before implementation.

## Worked Example (Mini)

**Input feature (from a PRD):**

> F-03: Users can reset their password by clicking "Forgot Password" and entering their email. The system emails a reset link.

This trips the "Reset flow gaps" pattern in the gap table — so the missing requirements are predictable.

**Enhanced output:**

```markdown
### Feature F-03: Password Reset via Email

**Actor**: Unauthenticated user (claiming an account)
**Data**: Email address (PII), password (credential), reset token
**Trust Boundaries**: browser → public API; API → email provider; API → credential store

**ASVS Mapping**: V2.2.2, V6.2.1, V6.2.2, V7.1.1, V11.1.4, V12.1.1

**Updated Requirements**:
- User can request a password reset by entering an account email at `/reset`.
- The system always returns the same success response whether or not the email matches an account (prevents account enumeration, V2.2.2).
- Reset tokens are single-use, expire within 15 minutes, and are stored only as a salted hash (V6.2).
- New passwords are validated against a minimum policy and screened against a known-breached-password list (V6.2.1).
- All reset requests, token issuances, token redemptions, and password changes are logged with user ID, source IP, user agent, and outcome (V7.1.1).
- Reset requests are rate-limited per email and per source IP (V11.1.4).
- The email input is canonicalized and validated against a strict format (V12.1.1).

**Acceptance Criteria**:
- Submitting a non-existent email returns the same response body, status code, and timing characteristics as a valid email (within tolerance).
- A reset token cannot be redeemed after 15 minutes or after first successful use; both cases produce a generic failure response and a logged `reset_token_invalid` event.
- More than 5 reset requests for the same email within 10 minutes are rejected with HTTP 429 and logged.
- Audit log lines for reset events are queryable by user ID and contain the fields above.

**Securability Notes**: This feature crosses an unauthenticated trust boundary (FIASSE v1.0.4 S4.3), so input handling and rate limiting are the load-bearing concerns. The reset token is server-owned state; never accept client-supplied token attributes beyond the opaque token itself (Derived Integrity, FIASSE v1.0.4 S4.4.1.2). Centralize token generation, hashing, and verification in a single module so the policy can evolve without touching call sites (Modifiability). All reset events must be observable in the audit pipeline so abuse patterns can be detected (Accountability + Observability, FIASSE v1.0.4 S3.2.1.4; Transparency S2.5).
```

This is the level of specificity the output should hit — concrete, testable, and traceable back to ASVS.

## Quality Checklist (run before emitting)

**Coverage**
- [ ] Every feature has an ID, actor, data classification, and trust-boundary list
- [ ] ASVS level is chosen and justified before per-feature mapping
- [ ] Every feature mapped against all applicable ASVS chapters at the chosen level
- [ ] Gap patterns from the table above were applied to every relevant feature
- [ ] Every Missing/Partial item produced a concrete PRD change

**Output discipline**
- [ ] Coverage matrix is present and includes change-needed column
- [ ] Each feature follows the exact output shape (Actor / Data / Trust Boundaries / ASVS Mapping / Updated Requirements / Acceptance Criteria / Securability Notes)
- [ ] Acceptance criteria are behaviorally testable, not aspirational
- [ ] Securability Notes are surgical — only material SSEM/FIASSE points, not exhaustive enumeration

**Traceability**
- [ ] Every added requirement cites its ASVS reference
- [ ] Cross-cutting requirements section captures shared controls
- [ ] Open gaps and assumptions are listed explicitly

## When in doubt

- Prefer adding a missing requirement over assuming coverage; mark it explicitly so reviewers see it.
- Prefer fewer, sharper ASVS references per feature over a long list that nobody will action.
- Prefer plain language in Securability Notes — these are read by product managers, not just security engineers.

## Reference Material

- Step-by-step runbook: [plays/requirements-analysis/prd-fiasse-asvs-enhancement.md](../../plays/requirements-analysis/prd-fiasse-asvs-enhancement.md)
- ASVS chapter index: `data/asvs/README.md`
- ASVS requirements (per chapter): `data/asvs/V*.md`
- FIASSE v1.0.4 foundational principles: `data/fiasse/S2.1.md`–`S2.6.md` (Transparency S2.5, Least Astonishment S2.6)
- FIASSE v1.0.4 SSEM attribute umbrellas: `data/fiasse/S3.2.1.md`–`S3.2.3.md`; leaf files (e.g. `S3.2.1.4.md` Observability) for attribute-specific guidance
- FIASSE v1.0.4 Boundary Control and Resilient Coding: `data/fiasse/S4.3.md`, `S4.4.md`, and the canonical-input-handling leaves `S4.4.1.md`, `S4.4.1.1.md`, `S4.4.1.2.md`
- FIASSE v1.0.4 Dependency Management and Stewardship: `data/fiasse/S4.5.md`, `S4.6.md`
