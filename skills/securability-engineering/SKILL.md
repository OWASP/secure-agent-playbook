---
name: securability-engineering
description: >
  Meta-skill that wraps code generation to enforce OWASP FIASSE securable coding attributes and principles.
  Use when generating, scaffolding, or refactoring code so that the output is engineered to be inherently
  securable by default. Applies the nine SSEM attributes (Analyzability, Modifiability, Testability,
  Confidentiality, Accountability, Authenticity, Availability, Integrity, Resilience), the
  Transparency principle, and OWASP FIASSE defensive coding practices to every code generation task.
  Invoke this skill alongside or instead of raw code generation when the user asks for secure code,
  securable code, FIASSE-compliant code, or when generating security-sensitive components
  (auth, input handling, data access, API endpoints, trust boundaries).
license: CC-BY-4.0
---

# Securability Engineering — Code Generation Wrapper

This skill augments the built-in code generation capability by applying Securable Software Engineering principles as
engineering constraints. It does not perform analysis or review (see `securability-engineering-review`
for that). Instead, it ensures that **generated code embodies securable qualities from the start**.

> **Reference**: OWASP FIASSE data in `data/fiasse/` — especially S2.1–S2.6 (Foundational Principles),
> S3.2.1–S3.2.3 (SSEM Attributes), S3.3.1 (Transparency), S6.3–S6.4 (Practical Guidance).
> Use `data/asvs/` as the feature-requirements reference set for security controls and implementation
> expectations. Assume the application is L2.

## When to Use

- Generating new code (functions, modules, services, APIs)
- Scaffolding projects or features
- Refactoring existing code for securability
- User asks for "secure code", "securable code", "FIASSE-compliant code"
- Generating security-sensitive components: authentication, authorization, input handling, data access, cryptography, logging, error handling
- Writing code that crosses trust boundaries

## Foundational Constraints

Before generating any code, apply these FIASSE principles as engineering constraints:

1. **The Securable Paradigm (S2.1)** — There is no static "secure" state. Generate code with inherent qualities that enable it to adapt to evolving threats, not code that is merely "secure right now".

2. **Resiliently Add Computing Value (S2.2)** — Generated code must be robust enough to withstand change, stress, and attack while delivering business value. Security qualities are engineering requirements, not afterthoughts.

3. **Reducing Material Impact (S2.3)** — Aim to reduce the probability of material impact from cyber events. Favor pragmatic controls aligned with the code's context and exposure, not theoretical completeness.

4. **Engineer, Don't Hack (S2.4)** — Generate engineering solutions, not exploit-aware patches. Build securely through quality attributes, not through adversarial thinking.

5. **Transparency (S2.6, S3.3.1)** — Generated code must be observable: meaningful naming, structured logging at trust boundaries, audit trails for security-sensitive actions, and health/performance instrumentation.

6. **Dependency Hygiene for Trustworthiness and Reliability** — When selecting libraries, default to the latest stable release that is compatible with the target runtime and framework. Prefer packages with low known vulnerability exposure (CVEs/CWEs), active maintenance, and strong release quality signals. Minimize dependency count and transitive risk by avoiding unnecessary or abandoned packages.

## SSEM Attribute Enforcement

Every code generation output must satisfy these nine attributes. Read the corresponding `data/fiasse/` section for full definitions when context is needed.

### Maintainability (S3.2.1)

| Attribute | Enforcement Rule |
|-----------|-----------------|
| **Analyzability** | Methods ≤ 30 LoC. Cyclomatic complexity < 10. Clear, descriptive naming. No dead code. Comments at trust boundaries and complex logic explaining *why*. |
| **Modifiability** | Loose coupling via interfaces/dependency injection. No static mutable state. Security-sensitive logic (auth, crypto, validation) centralized in dedicated modules, not scattered. Configuration externalized. |
| **Testability** | All public interfaces testable without modifying the code under test. Dependencies injectable/mockable. Security controls (auth, validation, crypto) isolated for dedicated test suites. |

### Trustworthiness (S3.2.2)

| Attribute | Enforcement Rule |
|-----------|-----------------|
| **Confidentiality** | Sensitive data classified and handled at the type level. Least-privilege data access. No secrets in code, logs, or error messages. Encryption at rest and in transit where applicable. Data minimization — collect and retain only what is needed. |
| **Accountability** | Security-sensitive actions logged with structured data (who, what, where, when). Audit trails append-only. Auth events (login, logout, failure) and authz decisions (grant, deny) recorded. No sensitive data in logs. |
| **Authenticity** | Use established authentication mechanisms. Verify token/session integrity (signed JWTs, secure cookies). Mutually authenticate service-to-service calls. Support non-repudiation — link actions irrefutably to entities. |

### Reliability (S3.2.3)

| Attribute | Enforcement Rule |
|-----------|-----------------|
| **Availability** | Enforce resource limits (memory, connections, file handles). Configure timeouts for all external calls. Rate-limit where appropriate. Thread-safe design for concurrent code. Graceful degradation for non-critical failures. |
| **Integrity** | Validate input at every trust boundary: canonicalize → sanitize → validate (S6.4.1). Output-encode when crossing trust boundaries. Use parameterized queries exclusively. Apply the **Derived Integrity Principle** (S6.4.1.1): never accept client-supplied values for server-owned state. Apply **Request Surface Minimization** (S6.4.1.1): extract only specific expected values from requests. |
| **Resilience** | Defensive coding: anticipate out-of-bounds input and handle gracefully. Specific exception handling (no bare catch-all). Sandbox nulls to input checks and DB communication. Use immutable data structures in concurrent code. Ensure no resource leaks — proper disposal patterns. Graceful degradation under load. |

## Trust Boundary Handling (S6.3)

Apply the **Turtle Analogy**: hard shell at trust boundaries, flexible interior.

- Identify trust boundaries in the generated code (user input, API calls, DB queries, file I/O, service-to-service)
- Apply strict input handling (canonicalization → sanitization → validation) at every boundary entry point
- Log trust boundary crossings with validation outcomes
- Keep interior logic flexible — strict control belongs at the boundary, not everywhere

## Steps

When generating code, apply this sequence:

1. **Identify Context** — Determine language/framework, system type, data sensitivity, exposure level, trust boundaries, and feature category relevant to the generation request.

2. **Map Feature Requirements to ASVS** — Use `data/asvs/README.md` and the relevant `data/asvs/V*.md` chapters to identify the security requirements that apply to the feature being generated. Match the request to ASVS sections using chapter topic and `when_to_use` guidance, then use the applicable ASVS requirements as implementation constraints.

3. **Apply SSEM Constraints** — For each piece of generated code, enforce the attribute rules above. Consult `data/fiasse/S3.2.1.md`, `S3.2.2.md`, `S3.2.3.md` for definitions when needed.

4. **Handle Trust Boundaries** — Identify where generated code crosses trust boundaries. Apply S6.3 (Flexibility Principle) and S6.4 (defensive coding, canonical input handling, Derived Integrity Principle, Request Surface Minimization).

5. **Select Dependencies Deliberately** — For each external dependency used in generated code, apply this policy:
  - Prefer latest stable versions unless a compatibility constraint is explicitly known
  - Prefer libraries with low known CVE/CWE exposure and no unresolved critical/high issues in current releases
  - Prefer mature, actively maintained projects with recent releases and clear security response practices
  - Minimize dependency footprint; avoid adding libraries when standard library/framework capabilities are sufficient
  - Pin versions and include lockfile guidance to support reproducible and reviewable builds

6. **Instrument Transparency** — Add structured logging at security-sensitive points. Include audit trail hooks for auth/authz events. Expose health metrics where applicable. Follow S3.3.1 transparency tactics.

7. **Generate Code** — Produce the code using the built-in code generation capability, with all SSEM constraints applied. The code should be:
   - Small, single-purpose functions with clear names (Analyzability)
   - Loosely coupled with injectable dependencies (Modifiability, Testability)
   - Defensive at trust boundaries, flexible inside (Integrity, Resilience)
   - Aligned to applicable ASVS feature requirements for the capability being implemented
   - Observable via structured logging and audit trails (Transparency, Accountability)

8. **Self-Check** — Before returning, verify the generated code against this checklist:

### Generation Checklist

**Maintainability:**
- [ ] Functions ≤ 30 LoC, cyclomatic complexity < 10
- [ ] No static mutable state; dependencies injected
- [ ] Security logic centralized, not duplicated
- [ ] Testable without modifying code under test

**Trustworthiness:**
- [ ] No secrets, PII, or tokens in code, logs, or error output
- [ ] Auth/authz events logged with structured data
- [ ] Authentication uses established mechanisms
- [ ] Data access follows least privilege

**ASVS Feature Requirements:**
- [ ] Relevant ASVS chapter(s) in `data/asvs/` were identified for the feature
- [ ] Applicable ASVS requirements were translated into implementation constraints
- [ ] Generated code satisfies the relevant ASVS requirement intent, not just the happy path behavior

**Reliability:**
- [ ] Input validated at every trust boundary (canonicalize → sanitize → validate)
- [ ] Derived Integrity Principle applied (server-owned state not client-supplied)
- [ ] Request Surface Minimization applied (only expected values extracted)
- [ ] Specific exception handling with meaningful messages; no bare catch-all
- [ ] Resource limits, timeouts, and disposal patterns in place

**Dependency Choice (Supply Chain Hygiene):**
- [ ] External libraries are necessary (no avoidable dependency added)
- [ ] Selected versions are latest stable compatible releases
- [ ] Selected packages have low known CVE/CWE exposure and no unresolved critical/high issues
- [ ] Packages show active maintenance (recent releases/commits and issue responsiveness)
- [ ] Versions are pinned and lockfile usage is included in generated setup guidance

**Transparency:**
- [ ] Meaningful naming conventions; self-documenting code
- [ ] Structured logging at trust boundaries and security events
- [ ] Audit trail hooks for security-sensitive actions

## Output

Generated code that embodies FIASSE securable qualities. When the generation is non-trivial, include a brief **Securability Notes** section after the code listing which SSEM attributes were actively enforced, applicable ASVS chapter or requirement references, dependency-selection rationale (version and risk posture), and any trade-offs made.

## FIASSE References

- [OWASP FIASSE Website](https://fiasse.org) — Tools and resources for FIASSE/SSEM
- [OWASP FIASSE Project](https://owasp.org/www-project-fiasse/) — Tools and resources for FIASSE/SSEM
- [FIASSE](https://github.com/Xcaciv/securable_software_engineering/blob/main/docs/secureable_framework.md) — Framework for Integrating Application Security into Software Engineering
- `data/asvs/README.md` — ASVS usage guidance and chapter index for feature requirements
- `data/asvs/V*.md` — ASVS 5.0 feature-aligned security requirements by chapter
- `data/fiasse/S2.1.md` – S2.6.md — Foundational Principles
- `data/fiasse/S3.2.1.md` – S3.2.3.md — SSEM Core Attributes
- `data/fiasse/S3.3.1.md` — Transparency Strategy
- `data/fiasse/S6.3.md` — The Flexibility Principle (Trust Boundaries)
- `data/fiasse/S6.4.md` — Resilient Coding, Derived Integrity Principle, Request Surface Minimization
- ISO/IEC 25010:2011 — Software quality models
- RFC 4949 — Internet Security Glossary
