---
name: security-architecture
description: Produces a factual, descriptive SECURITY_ARCHITECTURE.md mapping a system and the security mechanisms it relies on — authentication (inbound and outbound), authorization, session management, input/output handling, data protection, cryptography, logging, infrastructure, dependencies, integrations, tenancy, and any AI/agent components. Trigger on "describe/document the security architecture", "map the security controls", "as-built security design", or producing the descriptive baseline a threat model or ASVS review builds on. This skill describes the system as-is — it does NOT find vulnerabilities, rate controls, or recommend fixes.
license: CC-BY-4.0
---

# Security Architecture Description

Produce a descriptive map of how a system is built and what security mechanisms it relies
on. The deliverable is a populated `SECURITY_ARCHITECTURE.md`. Full procedure:
[plays/security-architecture.md](../../plays/security-architecture.md).

## Scope: Describe, Don't Assess

This skill is **purely descriptive**. It documents the *as-is* design and the controls that
exist. It does **not**:

- find or list vulnerabilities
- rate, score, or judge controls ("weak", "strong", "missing")
- assign severities or recommend remediations

When a control can't be found, record **UNKNOWN** — never infer one that the evidence
doesn't show. Assessment is a separate activity (threat modeling, ASVS verification, code
review) that *consumes* this document. The descriptive baseline this skill produces is the
input to those reviews, not a substitute for them.

## When to Invoke

- "Describe / document the security architecture of this system"
- "Map the security mechanisms / controls in this codebase"
- "Create a SECURITY_ARCHITECTURE.md / as-built security design doc"
- "I need the baseline before we threat-model this"
- Onboarding to an unfamiliar system to capture how its security works

## Working Principles

1. **Evidence over assumption** — anchor every claim to a `file:line`, config, or named
   source. No evidence → **UNKNOWN**.
2. **Find them all** — authentication, integrations, and entry points usually have several
   instances. Enumerate exhaustively rather than describing the first one found.
3. **Both directions** — capture inbound *and* outbound for authentication, integrations,
   and data flow. Outbound credentials and egress are the commonly-missed half.
4. **Describe, don't judge** — presence and mechanism only; no severity or remediation.

## Topics to Cover

Walk these in order, populating the matching section of `templates/SECURITY_ARCHITECTURE.md`:

1. **System overview** — purpose, deployment context, component inventory, tech stack, diagram.
2. **Trust boundaries & data flow** — where trust changes, entry points (attack surface,
   described not assessed), how sensitive data enters/processes/stores/leaves.
3. **Authentication — inbound** — *every* mechanism: end-user login, service-to-service,
   webhooks, admin, machine/CI. Protocol, credential, signing/issuer/audience, lifetime, MFA,
   verification point.
4. **Authentication — outbound** — credentials this system presents to DBs, third parties,
   internal services, and where they're stored.
5. **Authorization** — model (RBAC/ABAC/ReBAC/ACL/policy-as-code), enforcement point(s),
   roles/attributes/policies, ownership/tenancy scoping.
6. **Session management** — stateful/stateless, cookie attributes, store, timeouts,
   revocation, refresh/rotation.
7. **Secrets & credential management** — storage, injection, rotation, access.
8. **Data protection** — data classification inventory, encryption in transit / at rest,
   cryptography and key management.
9. **Input & output handling** — validation, output encoding, (de)serialization, file handling.
10. **Logging, monitoring & auditing** — security events logged, retention, redaction, alerting.
11. **Infrastructure & deployment** — cloud, network/VPC segmentation, IaC, compute/runtime,
    CI/CD, workload identity.
12. **Dependencies & supply chain** — footprint and management, base images, SBOM (inventory
    only; CVE analysis belongs to `sca-audit`).
13. **External integrations** — third parties, direction, data shared, auth, trust assumption.
14. **Tenancy & isolation** — isolation model and where the tenant id originates/enforces.
15. **AI / agent-specific** — only if LLMs/agents/MCP present: models, prompt boundaries,
    callable tools and privileges, untrusted-content paths, MCP scopes (describe only). Use
    the OWASP **AISVS v1.0** categories (`data/aisvs/`, C1–C12) as the checklist of what to
    describe.

## Steps

1. **Gather sources** — application code, IaC, gateway/mesh/CI config, API specs, existing
   docs/ADRs. Note what you have and what's missing.
2. **Walk the topics** — work through the list above following
   [plays/security-architecture.md](../../plays/security-architecture.md), anchoring each
   claim to a source and marking gaps **UNKNOWN**.
3. **Populate the template** — fill `templates/SECURITY_ARCHITECTURE.md` section by section.
4. **Synthesize** — complete the Security Controls Summary matrix (presence + location, no
   rating), the Assumptions & Open Questions, and optionally the ASVS cross-reference.

## Output

A complete `SECURITY_ARCHITECTURE.md` based on `templates/SECURITY_ARCHITECTURE.md`. Every
bracketed placeholder replaced with evidence-anchored content or the literal **UNKNOWN**.
No findings, severities, or recommendations — those are out of scope.

## OWASP References

- **OWASP ASVS v5.0** — chapter structure used for the application/infra cross-reference appendix (`data/asvs/`)
- **OWASP AISVS v1.0** — category structure (C1–C12) used to describe the AI/agent section (`data/aisvs/README.md` index, `data/aisvs/C*.md` requirements)
- **OWASP Threat Modeling** — this document is the descriptive input a threat model consumes
- **OWASP Cheat Sheets** — Authentication, Authorization, Session Management, Transport Layer
  Protection, Secrets Management — definitions for the described mechanisms
- Full procedure: [plays/security-architecture.md](../../plays/security-architecture.md)
- Output template: `templates/SECURITY_ARCHITECTURE.md`
