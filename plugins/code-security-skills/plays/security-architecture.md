# Play: Security Architecture Description

Produce a factual, descriptive map of a system and the security mechanisms it relies on —
the *as-is* design. The deliverable is a populated `SECURITY_ARCHITECTURE.md`.

> **Scope discipline.** This play is **descriptive, not evaluative**. It documents what
> exists. It does **not** find vulnerabilities, rate controls, assign severities, or
> recommend fixes. When you notice a gap, record it as **UNKNOWN** or as an open question —
> do not editorialize. Assessment is a separate activity (threat modeling, ASVS
> verification, code review) that *consumes* this document.

## Trigger Conditions

Use this play when the user asks to:
- "Describe / document the security architecture of this system"
- "Map the security mechanisms / controls in this codebase"
- Produce a `SECURITY_ARCHITECTURE.md` or an as-built security design doc
- Create the descriptive baseline that a threat model or ASVS review will build on
- Onboard to an unfamiliar system and capture how its security works

## Inputs

- Source repositories (application code, middleware, auth logic)
- Infrastructure as Code (Terraform, CloudFormation, Pulumi, Helm, k8s manifests)
- Configuration (gateway/proxy config, service mesh, CI/CD pipelines, env templates)
- API specs (OpenAPI/GraphQL schema), architecture docs, ADRs, diagrams
- Any existing security/compliance documentation
- Optional: SME interviews to fill gaps the artifacts don't cover

## Principles

1. **Evidence over assumption** — anchor every claim to a file, config, or named source. If
   you cannot find evidence, write **UNKNOWN**; never infer a control that isn't shown.
2. **Find them all** — auth, integrations, and entry points usually have *several*
   instances (inbound and outbound, primary and edge-case). Enumerate exhaustively.
3. **Both directions** — for authentication, integrations, and data flow, capture inbound
   *and* outbound. Outbound credentials and egress are the commonly missed half.
4. **Describe, don't judge** — no severity, no "weak/strong", no remediation. Presence and
   mechanism only.

## Procedure

Work topic by topic, populating the corresponding section of `templates/SECURITY_ARCHITECTURE.md`.

### Phase 1: Orient — System Overview (§1)

1. Identify the system's purpose, primary users, and deployment context (internet-facing /
   internal / multi-tenant / regulated).
2. Build the **component inventory** by surveying the repo and IaC: services, datastores,
   caches, brokers, gateways. Record role, language/framework, exposure, and source path.
3. Capture the technology stack and managed cloud services.
4. Sketch an architecture diagram (`mermaid flowchart`) showing components and the calls
   between them.

### Phase 2: Trust Boundaries & Data Flow (§2)

5. Identify every point where the trust level of data or callers changes: internet edge,
   app↔data tier, service↔third-party, user↔admin plane, tenant↔tenant. Record what
   crosses and what control sits on the boundary.
6. Enumerate **entry points** (attack surface, descriptively): public endpoints, admin
   interfaces, webhooks, queue consumers, scheduled jobs, CLI/SSH, debug/metrics ports.
7. Trace how sensitive data enters, is processed, is stored, and leaves.

### Phase 3: Identity & Access (§3)

8. **Inbound authentication** — find *all* mechanisms. Look for: login/session middleware,
   JWT/OIDC validation, mTLS, API-key checks, webhook signature verification, basic auth,
   SSO/SAML. For each record protocol, credential type, signing/issuer/audience, lifetime,
   MFA, and the verification point. Search hints:
   - `grep` for `Authorization`, `Bearer`, `jwt`, `verify`, `passport`, `oidc`, `saml`,
     `mtls`, `client_cert`, `hmac`, `X-API-Key`, `Auth0`, `Cognito`, `Okta`.
9. **Outbound authentication** — credentials this system presents to others (DBs, third-party
   APIs, internal services). Record target, mechanism, credential, and where it is stored.
10. **Authorization** — determine the model (RBAC / ABAC / ReBAC / ACL / policy-as-code),
    the enforcement point(s), and enumerate roles/attributes/policies. Capture how
    ownership/tenancy scoping is applied per request. Search hints: `role`, `permission`,
    `policy`, `can(`, `authorize`, `@PreAuthorize`, `casbin`, `opa`, `cedar`, row-level security.
11. **Session management** — stateful vs stateless, cookie attributes, store, timeouts,
    logout/revocation, refresh/rotation.
12. **Secrets & credential management** — where secrets live, how injected, rotation, access.

### Phase 4: Data Protection (§4)

13. Build a **data classification inventory**: categories, sensitivity, storage, flow.
14. Document encryption **in transit** (TLS versions, termination, internal mTLS).
15. Document encryption **at rest** (DB/volume/bucket/backup, KMS keys).
16. Document cryptography in use: signing/hashing/encryption algorithms, password hashing,
    key storage and rotation.

### Phase 5: Input & Output Handling (§5)

17. Describe input validation (schema/type validation, canonicalization, parameterized
    queries/ORM), output encoding (template auto-escaping, DTO projection, security headers),
    serialization/deserialization formats and limits, and file/upload handling.

### Phase 6: Logging, Monitoring & Auditing (§6)

18. Document which security-relevant events are logged, destination and retention,
    audit-trail integrity, redaction of secrets/PII, and the monitoring/alerting stack.

### Phase 7: Infrastructure & Deployment (§7)

19. From IaC and pipeline config: hosting/cloud, network architecture (VPC, subnets,
    segmentation, security groups/network policies, egress), IaC tooling and scope,
    compute/runtime model and isolation, CI/CD flow and who can deploy, and workload
    identity (how compute authenticates to cloud services).

### Phase 8: Supply Chain, Integrations, Tenancy, AI (§8–§11)

20. **Dependencies & supply chain** (§8) — dependency footprint and management, base images,
    SBOM availability, registries. Inventory only; defer CVE analysis to `sca-audit`.
21. **External integrations** (§9) — every third party, direction, data shared, auth, and the
    trust assumption placed on it.
22. **Tenancy & isolation** (§10) — isolation model and where the tenant identifier originates
    and is enforced.
23. **AI / agent-specific** (§11) — only if LLMs/agents/MCP are present: models/providers,
    prompt boundaries, callable tools and their privileges, untrusted-content paths,
    human-in-the-loop points, MCP server scopes. Use the OWASP **AISVS** category structure
    (`data/aisvs/`, C1–C13) as the checklist of what to describe — training-data governance
    (C1), prompt-injection boundaries (C2), model provenance (C3/C6), runtime isolation (C4),
    agent identity & access (C5), output handling (C7), memory/RAG access (C8), autonomy &
    tool privileges (C9), safety guardrails (C10), privacy (C11), logging (C12), human
    oversight/kill-switch (C13). Describe only; assessment lives in the `ai-security-skills`
    plugin.

### Phase 9: Synthesize (§12–§13, Appendix)

24. Fill the **Security Controls Summary** matrix (presence + location, no rating).
25. Record **assumptions and open questions**, consolidating every **UNKNOWN**.
26. Optionally complete the **ASVS chapter cross-reference** appendix to hand off to a later
    verification pass.

## Output Format

Populate `templates/SECURITY_ARCHITECTURE.md` in full. Replace every bracketed placeholder
with evidence-anchored content or the literal token **UNKNOWN**. Keep tables; drop a
section only when it is genuinely **N/A** (and say so). Do not add severities, findings, or
recommendations — those are out of scope for this play.

## OWASP References

- **OWASP ASVS v5.0** — chapter structure used for the application/infra cross-reference appendix (`data/asvs/`)
- **OWASP AISVS** — category structure (C1–C13) used to describe the AI/agent section §11 (`data/aisvs/README.md` index, `data/aisvs/C*.md` requirements)
- **OWASP Threat Modeling** — this document is the descriptive input a threat model consumes
- **OWASP Cheat Sheets** — Authentication, Authorization, Session Management, Transport Layer
  Protection, Secrets Management (reference definitions for the mechanisms described)
