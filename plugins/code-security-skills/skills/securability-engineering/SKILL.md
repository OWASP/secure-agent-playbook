---
name: securability-engineering
description: Generate, scaffold, or refactor code so it embodies FIASSE v1.0.4 SSEM qualities by default — 10 attributes, Transparency and Least-Astonishment principles, ASVS-aligned controls, defensive boundary handling. Trigger on "secure/securable/FIASSE-compliant code", "harden", "secure-by-default", "audit-ready", or security-sensitive components (auth, file upload, password reset, input validation, API endpoints, queries) — even when those words are not explicit. For requirements use prd-securability-enhancement; for review use securability-engineering-review. The full PRD→generate→review→enhance loop is opt-in via "--full-loop" or "end-to-end securable".
license: CC-BY-4.0
---

# Securability Engineering — Code Generation Wrapper

This skill augments the built-in code generation capability by applying FIASSE v1.0.4 SSEM principles as engineering constraints. It does **not** perform full SSEM scoring (use `securability-engineering-review` for that).

The end-to-end PRD-enhance → generate → review → enhance → report loop is **opt-in**, not the default. See "Full Loop Mode" below.

Reference data: `data/fiasse/` (especially S2.1–S2.6 foundational principles, S3.2.1–S3.2.3 SSEM attributes including S3.2.1.4 Observability, S2.5 Transparency, S4.3 Boundary Control, S4.4 Resilient Coding, S4.4.1 Canonical Input Handling, S4.6 Dependency Stewardship) and `data/asvs/` for feature-level requirements.

## When to Invoke

Trigger this skill when the user asks to:

- Generate new code (functions, modules, services, APIs, scripts)
- Scaffold a project, feature, or component
- Refactor existing code for security or maintainability
- Implement security-sensitive functionality: authentication, authorization, input handling, file upload/download, data access, cryptography, logging, error handling, session management
- Write code that crosses a trust boundary (any user/external input, any storage I/O, any network egress, any cross-service call)

Watch for adjacent phrasings: "make this safe", "harden this endpoint", "I'm exposing this to the internet, can you...", "write the production version of...", "audit-ready", "production-grade".

## Modes of Operation

### Default Mode (single-shot generation)

Produce securable code from the user's request directly, applying SSEM constraints. Most invocations land here. The output is code + a Securability Notes block.

### Full Loop Mode (opt-in, end-to-end)

Run the full PRD-enhance → generate → review → enhance → report workflow. **Activate only when** the user:

- Passes the `--full-loop` flag or argument
- Says "end-to-end securable" or "full securability loop"
- Explicitly references the play (e.g., "follow the securable-generation play")

Otherwise stay in Default Mode. Do not invent a PRD for a small one-shot generation request.

When Full Loop Mode is active, follow [plays/securable-generation.md](../../plays/securable-generation.md). When Default Mode is active, follow this file alone.

## Foundational Constraints

Before generating any code, apply these FIASSE v1.0.4 principles:

1. **The Securable Paradigm** (FIASSE v1.0.4 S2.1) — There is no static "secure" state. Generate code with qualities that let it adapt to evolving threats, not code that is merely "secure right now".
2. **Resiliently Add Computing Value** (FIASSE v1.0.4 S2.2) — Code must withstand change, stress, and attack while delivering business value. Security qualities are engineering requirements, not afterthoughts.
3. **Reducing Material Impact** (FIASSE v1.0.4 S2.3) — Favor pragmatic controls aligned with the code's context and exposure, not theoretical completeness.
4. **Derived Integrity** (FIASSE v1.0.4 S4.4.1.2) — Never implicitly trust client-supplied values for server-owned state. Explicitly extract only expected values from requests.
5. **Transparency & Observability** (FIASSE v1.0.4 S2.5, S3.2.1.4) — Code must be observable from its own outputs: meaningful naming, structured logging at trust boundaries, audit trails, and instrumentation built in — not bolted on externally.
6. **Least Astonishment** (FIASSE v1.0.4 S2.6) — Behavior and side-effects must match what the name and signature suggest. No hidden mutation, no implicit network/filesystem effects, no surprising error paths.
7. **Boundary Control** (FIASSE v1.0.4 S4.3) — Flexibility belongs in the interior; control belongs at every trust boundary. Treat boundaries as the hard shell; keep the interior loose enough to evolve.
8. **Dependency Hygiene & Stewardship** (FIASSE v1.0.4 S4.5, S4.6) — Default to the latest stable release compatible with the runtime. Prefer packages with low CVE/CWE exposure, active maintenance, and strong release signals. Treat each dependency as an ongoing relationship.
9. **Canonical Input Handling** (FIASSE v1.0.4 S4.4.1) — Apply canonicalize → sanitize → validate at every trust boundary. Prefer specific types and constrained enums. Apply Request Surface Minimization (FIASSE v1.0.4 S4.4.1.1) — process only the specific named values you expect.

## SSEM Attribute Enforcement

Every code generation output must satisfy these ten attributes. Read `data/fiasse/` sections for definitions when context is needed.

### Maintainability

| Attribute | Enforcement |
|-----------|-------------|
| **Analyzability** (FIASSE v1.0.4 S3.2.1.1) | Methods ≤ 30 LoC. Cyclomatic complexity < 10. Clear, descriptive naming. No dead code. Comments only at trust boundaries and complex logic, explaining *why* — not *what*. |
| **Modifiability** (FIASSE v1.0.4 S3.2.1.2) | Loose coupling via interfaces / dependency injection. No static mutable state. Security-sensitive logic (auth, crypto, validation) centralized in dedicated modules, not scattered across call sites. Configuration externalized. |
| **Testability** (FIASSE v1.0.4 S3.2.1.3) | All public interfaces testable without modifying code under test. Dependencies injectable / mockable. Security controls isolated for dedicated test suites. |
| **Observability** (FIASSE v1.0.4 S3.2.1.4) | Code-level instrumentation, not external tooling alone. Structured logs with sufficient context (who/what/where/when/outcome) at trust boundaries and security-sensitive operations. Health and performance metrics exposed through a standardized API. Failure paths produce observable signals; no silent exception swallowing. UI/operator feedback surfaces meaningful state without leaking internals. |

### Trustworthiness

| Attribute | Enforcement |
|-----------|-------------|
| **Confidentiality** (FIASSE v1.0.4 S3.2.2.1) | Sensitive data classified at the type level. Least-privilege data access. No secrets in code, logs, or error messages. Encryption at rest and in transit where applicable. Data minimization. |
| **Accountability** (FIASSE v1.0.4 S3.2.2.2) | Security-sensitive actions logged with structured data (who, what, where, when). Audit trails append-only. Auth events (login, logout, failure) and authz decisions (grant, deny) recorded. No sensitive data in logs. |
| **Authenticity** (FIASSE v1.0.4 S3.2.2.3) | Use established authentication mechanisms. Verify token/session integrity (signed JWTs with pinned algorithm, secure cookies). Mutually authenticate service-to-service calls. Support non-repudiation. |

### Reliability

| Attribute | Enforcement |
|-----------|-------------|
| **Availability** (FIASSE v1.0.4 S3.2.3.1) | Enforce resource limits (memory, connections, file handles). Configure timeouts for all external calls. Rate-limit where appropriate. Thread-safe design for concurrent code. Graceful degradation for non-critical failures. |
| **Integrity** (FIASSE v1.0.4 S3.2.3.2) | Validate input at every trust boundary: canonicalize → sanitize → validate (FIASSE v1.0.4 S4.4.1). Output-encode when crossing trust boundaries. Use parameterized queries exclusively. Apply Derived Integrity (FIASSE v1.0.4 S4.4.1.2) and Request Surface Minimization (FIASSE v1.0.4 S4.4.1.1). |
| **Resilience** (FIASSE v1.0.4 S3.2.3.3) | Defensive coding: anticipate out-of-bounds input. Specific exception handling — no bare catch-all. Sandbox null checks to input/DB boundaries. Use immutable data structures in concurrent code. Deterministic disposal patterns (`with`, `using`, RAII). Graceful and **secure** failure: error messages don't leak internals. |

## Trust Boundary Handling (FIASSE v1.0.4 S4.3)

Apply the **Boundary Control Principle** (the "turtle analogy"): hard shell at trust boundaries, flexible interior.

- Identify trust boundaries: user input, API calls, DB queries, file I/O, service-to-service.
- Apply strict input handling (canonicalization → sanitization → validation) at every boundary entry point.
- Log boundary crossings with validation outcomes.
- Keep interior logic flexible — strict control belongs at the boundary, not everywhere.

### Defensive Boundary Parsing

Boundary input is hostile until proven otherwise — and "hostile" includes *well-meaning but unusual*, not just attacker-crafted. Real protocols and formats have edge cases that naive parsers fail on. Before writing any boundary-parsing code, think through these classes of variation explicitly:

- **HTTP headers** — case-insensitive names; scheme tokens whose RFC behavior is case-insensitive (`Bearer`, `bearer`, `BEARER` per RFC 6750/7235); leading/trailing whitespace; multiple values; comma-separated lists; non-ASCII; missing entirely.
- **URLs and query strings** — percent-encoding variants, normalization (`/a/./b` → `/a/b`), traversal (`..`), trailing slash, mixed-case schemes, IDN/punycode, repeated query keys.
- **Filenames and paths** — Unicode normalization forms (NFC/NFD), case sensitivity differences across filesystems, embedded null bytes, reserved names (`CON`, `PRN` on Windows), traversal segments.
- **Numeric and boolean inputs** — leading zeros, signed forms, scientific notation, `Infinity`/`NaN`, locale-specific separators, "yes"/"true"/"1"/"on" boolean variants.
- **Content types and MIME** — case-insensitive names, optional parameters (`; charset=utf-8`), spoofed declared type vs sniffed type.
- **JSON and structured payloads** — duplicate keys, depth bombs, integer overflow, type confusion (`"123"` vs `123`).
- **Tokens and credentials** — leading/trailing whitespace, base64url vs base64, padding variants, leading `Bearer ` already stripped or not.

Don't enumerate all of these in code — pick the ones that *matter for this boundary* and handle them deliberately. The default for any RFC-defined token is **"follow the RFC, don't reject the spec-compliant variant just because your prototype only saw one shape."**

## Steps (Default Mode)

1. **Identify Context** — Language, framework, system type, data sensitivity, exposure level, trust boundaries, feature category.
2. **Map Feature Requirements to ASVS** — Use `data/asvs/README.md` and the relevant `data/asvs/V*.md` chapters to identify the security requirements applying to the feature being generated.
3. **Apply SSEM Constraints** — Enforce the attribute rules in the tables above. Consult `data/fiasse/S3.2.1.md`–`S3.2.3.md` for umbrella definitions.
4. **Handle Trust Boundaries** — Identify where generated code crosses trust boundaries. Apply FIASSE v1.0.4 S4.3 (Boundary Control) and S4.4 (Resilient Coding).
5. **Select Dependencies Deliberately** (FIASSE v1.0.4 S4.5, S4.6):
   - Latest stable versions unless a compatibility constraint is known
   - Low known CVE/CWE exposure
   - Mature, actively maintained projects
   - Minimize footprint; avoid libraries when standard library suffices
   - Pin versions; include lockfile guidance
   - Treat the dependency as an ongoing relationship (Stewardship)
6. **Instrument Transparency & Observability** — Add structured logging at security-sensitive points (FIASSE v1.0.4 S2.5). Include audit-trail hooks for auth/authz events. Build observability into the code itself (FIASSE v1.0.4 S3.2.1.4).
7. **Generate Code** — Produce the code with all SSEM constraints applied. Code should be:
   - Small, single-purpose functions with clear names (Analyzability)
   - Loosely coupled with injectable dependencies (Modifiability, Testability)
   - Defensive at trust boundaries, flexible inside (Integrity, Resilience)
   - Observable via structured logging and audit trails (Observability, Accountability)
8. **Self-Check** — Verify against the Generation Checklist below before returning.

## Output Format

The code itself is the primary deliverable. After the code, append a short **Securability Notes** block:

```markdown
## Securability Notes

- **SSEM attributes enforced**: [the 2–4 that actually shape this code, named briefly]
- **ASVS references**: [V-chapter.section IDs that apply]
- **Trust boundaries**: [where input is canonicalized/validated]
- **Dependencies**: [package@version — only when something non-trivial was introduced]
- **Trade-offs**: [decisions a reviewer needs to know — e.g., "in-process rate limit; switch to shared store for multi-instance"]
```

Skip bullets that have nothing material to say. For tiny edits with no boundary crossing, a single sentence is enough. The point of this block is to make review faster, not to perform thoroughness.

## Worked Example (Mini)

**User request**: "Write a Python FastAPI endpoint that lets a logged-in user fetch one of their own orders by ID."

**Sloppy default (what to avoid)**:

```python
@app.get("/orders/{order_id}")
def get_order(order_id: str, current_user=Depends(get_user)):
    order = db.query("SELECT * FROM orders WHERE id = '" + order_id + "'")
    return order
```

Issues: SQL injection (string concatenation), missing ownership check (any user can read any order — IDOR), broad return shape leaks fields, no logging, no input validation, no error handling.

**Securable version**:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
import structlog

router = APIRouter()
log = structlog.get_logger()

class OrderView(BaseModel):
    id: UUID
    placed_at: str
    status: str
    total_cents: int

@router.get("/orders/{order_id}", response_model=OrderView)
def get_order(
    order_id: UUID,                                  # canonicalized: must parse as UUID or 422
    current_user = Depends(get_authenticated_user),  # auth at the boundary
    orders = Depends(get_orders_repo),               # injectable for tests
):
    order = orders.find_owned_by(order_id, current_user.id)  # ownership enforced server-side
    if order is None:
        log.info("order_lookup.denied",
                 user_id=current_user.id, order_id=str(order_id), reason="not_found_or_not_owned")
        raise HTTPException(status_code=404, detail="Order not found")
    log.info("order_lookup.granted",
             user_id=current_user.id, order_id=str(order_id))
    return OrderView.model_validate(order)
```

What changed and why:

- `order_id: UUID` canonicalizes input at the boundary (Integrity, FIASSE v1.0.4 S4.4.1).
- `find_owned_by(order_id, user_id)` enforces ownership server-side — `current_user.id` is server-owned state, never trusted from the client (Derived Integrity, FIASSE v1.0.4 S4.4.1.2).
- `OrderView` projection limits the response to expected fields (Confidentiality; Request Surface Minimization, FIASSE v1.0.4 S4.4.1.1).
- Structured logs at boundary outcomes give the audit pipeline what it needs (Accountability, Observability — FIASSE v1.0.4 S2.5, S3.2.1.4).
- `Depends(get_orders_repo)` is injectable, so tests can run without a real DB (Testability, Modifiability).
- 404 returned for both "not found" and "not owned" — avoids signalling existence to non-owners (Confidentiality).

## Anti-Pattern Tag Reference (avoid while writing)

These are the patterns to **not** emit during generation. Each row pairs the bad shape with the principle it would violate, so when you find yourself about to write one, you know what's going wrong and what the correct shape looks like.

| Pattern to avoid emitting | Principle / attribute violated | Tag | Correct shape instead |
|---|---|---|---|
| String-built SQL / shell / format strings touching user input | Integrity — input handling at boundary (FIASSE v1.0.4 S4.4.1, S4.3) | "Trust boundary input handling" | Parameterized query / `subprocess` arg list / format with placeholders |
| Trusting `req.body.user_id`, `X-Tenant-ID`, JWT claims for authorization decisions | Integrity — Derived Integrity (FIASSE v1.0.4 S4.4.1.2) | "Derived Integrity violation" | Look up user/tenant from authenticated session; never client-asserted |
| Spreading `req.body` / `**request.json` directly into ORM update | Integrity — Request Surface Minimization (FIASSE v1.0.4 S4.4.1.1) | "Mass assignment" | Explicit allow-list of named fields → typed DTO → mapped update |
| `os.path.join(base, user_input)` / template path concatenation | Integrity — boundary canonicalization (FIASSE v1.0.4 S4.4.1) | "Path canonicalization gap" | Resolve absolute path, assert it's under `base`, reject otherwise |
| `jwt.decode(token)` with default algorithms / no `aud` / no `iss` | Authenticity (FIASSE v1.0.4 S3.2.2.3) | "Token verification under-specified" | `jwt.decode(token, key, algorithms=['RS256'], audience=..., issuer=...)` |
| `print(...)` / `console.log(...)` / `fmt.Println(...)` for security events | Accountability + Observability (FIASSE v1.0.4 S2.5, S3.2.1.4) | "Unstructured audit trail" | Structured logger emitting `{event, actor, target, outcome, request_id}` |
| `try: ... except: pass` / silent failure paths | Observability (FIASSE v1.0.4 S3.2.1.4); Resilience (FIASSE v1.0.4 S3.2.3.3) | "Silent failure" | Specific exception types; log with context; re-raise or return typed error |
| Bare `except:` / `catch (e)` returning raw exception text | Resilience; Confidentiality (FIASSE v1.0.4 S3.2.3.3, S3.2.2.1) | "Specific exception handling missing" | Named exception types, generic public message, internal log with detail |
| Module-level globals (DB connection, app, config) created at import | Modifiability + Testability (FIASSE v1.0.4 S3.2.1.2, S3.2.1.3) | "Import-time side effects" | Factory function / DI container / fixture-injected dependencies |
| `request.body.read()` / `ioutil.ReadAll(r.Body)` with no size cap | Availability + Resilience (FIASSE v1.0.4 S3.2.3.1, S3.2.3.3) | "Unbounded resource consumption" | Bounded reader; explicit `max_size`; 413 on overflow |
| `password == request.password` / non-constant-time secret comparison | Authenticity; Confidentiality | "Timing-side-channel comparison" | `hmac.compare_digest` / language equivalent |
| Hardcoded secrets, connection strings, or API keys | Confidentiality (FIASSE v1.0.4 S3.2.2.1) | "Secret in code" | Env var / secret manager; pass via injected config |
| `any` / `interface{}` / `dynamic` on the trust-boundary surface | Analyzability + Integrity | "Trust-boundary type erasure" | Concrete typed DTO / Pydantic model / typed struct |
| `setTimeout` / `time.sleep` as a substitute for actual rate limiting | Availability (FIASSE v1.0.4 S3.2.3.1) | "Sleep-based throttling" | Real rate limiter (token bucket / fixed window) keyed by actor |
| External call without timeout (`requests.get(url)`, `http.Client{}`) | Availability + Resilience | "Unbounded external call" | Explicit `timeout=` / configured `Client` with timeouts |
| Logging the full request body / response body / token by default | Confidentiality + Accountability (sensitive data in audit) | "PII in audit log" | Log structured event with IDs only; redact body and credential fields |

If you catch yourself emitting one of these, stop and rewrite.

## Generation Checklist

**Maintainability**:
- [ ] Functions ≤ 30 LoC, cyclomatic complexity < 10
- [ ] No static mutable state; dependencies injected
- [ ] Security logic centralized, not duplicated
- [ ] Testable without modifying code under test
- [ ] Observability built into the code: structured logs at boundaries with sufficient context; failure paths are observable; instrumentation does not depend on external tooling alone

**Trustworthiness**:
- [ ] No secrets, PII, or tokens in code, logs, or error output
- [ ] Auth/authz events logged with structured data
- [ ] Authentication uses established mechanisms
- [ ] Data access follows least privilege

**ASVS feature requirements**:
- [ ] Relevant ASVS chapter(s) identified for the feature
- [ ] Applicable ASVS requirements translated into implementation constraints
- [ ] Generated code satisfies the requirement intent, not just the happy path

**Reliability**:
- [ ] Input validated at every trust boundary (canonicalize → sanitize → validate)
- [ ] Derived Integrity applied (server-owned state not client-supplied)
- [ ] Request Surface Minimization applied (only expected values extracted)
- [ ] Specific exception handling with meaningful messages; no bare catch-all
- [ ] Resource limits, timeouts, and disposal patterns in place

**Dependency hygiene**:
- [ ] External libraries are necessary (no avoidable dependency added)
- [ ] Selected versions are latest stable compatible releases
- [ ] Selected packages have low known CVE/CWE exposure
- [ ] Active-maintenance signals checked
- [ ] Versions pinned; lockfile guidance included

**Transparency**:
- [ ] Meaningful naming; self-documenting code
- [ ] Structured logging at trust boundaries and security events
- [ ] Audit-trail hooks for security-sensitive actions

**Anti-patterns avoided**:
- [ ] None of the rows in the Anti-Pattern Tag Reference are present in the generated code

**Output format**:
- [ ] Securability Notes block included after the code (lean — only material points)
- [ ] Notes name the 2–4 SSEM attributes that actually shaped the code (not all ten)
- [ ] Trade-offs section calls out anything a reviewer would want to revisit

## When in Doubt

- Prefer a small, sharp piece of code with a clear Securability Notes block over a large, comprehensive one with implicit assumptions.
- Prefer flagging a missing requirement explicitly (in trade-offs) over silently introducing a default behavior.
- Prefer the standard library / framework primitive over a new dependency unless the dependency materially improves correctness.
- Prefer named exception types and explicit error responses over generic `try/except`.

## FIASSE References

- [FIASSE Framework v1.0.4](https://github.com/OWASP/FIASSE/blob/v1.0.4/docs/securable_framework.md)
- `data/asvs/README.md` — ASVS chapter index
- `data/asvs/V*.md` — ASVS 5.0 feature requirements by chapter
- `data/fiasse/S2.1.md`–`S2.6.md` — Foundational Principles (incl. Transparency S2.5 and Least Astonishment S2.6)
- `data/fiasse/S3.2.1.md`–`S3.2.3.md` — SSEM attribute umbrellas (Maintainability, Trustworthiness, Reliability)
- `data/fiasse/S3.2.1.4.md` — Observability
- `data/fiasse/S4.3.md` — Boundary Control Principle
- `data/fiasse/S4.4.md` — Resilient Coding
- `data/fiasse/S4.4.1.md` — Canonical Input Handling
- `data/fiasse/S4.4.1.1.md` — Request Surface Minimization Principle
- `data/fiasse/S4.4.1.2.md` — Derived Integrity Principle
- `data/fiasse/S4.5.md` / `S4.6.md` — Dependency Management and Stewardship
- Full Loop Mode runbook: [plays/securable-generation.md](../../plays/securable-generation.md)
- ISO/IEC 25010:2011 — Software quality models
- RFC 4949 — Internet Security Glossary
