# OWASP AISVS v1.0 — AI Security Verification Standard

Category index for the per-requirement files in this directory (`C<chapter>.<section>.md`).
Used by `security-architecture` (to describe AI/agent mechanisms) and the AI-focused skills.

Source: [OWASP AISVS](https://github.com/OWASP/AISVS) **v1.0 (June 2026)** — 12 chapters,
44 sections, 191 requirements.

**Fidelity:** each file carries its upstream section heading, intro paragraph, and
requirements table **byte-for-byte** from `1.0/en/0x10-C*.md`. Only the YAML frontmatter
(`when_to_use`, `threats`, `summary`) is authored by this repo. Requirement text can be
quoted directly in findings. The `Level` column is the AISVS verification level (1–3).

| Category | Title | Sections |
|----------|-------|----------|
| C1 | Training Data Integrity & Traceability | C1.1–C1.3 |
| C2 | Input Validation (incl. Prompt Injection Defenses) | C2.1–C2.2 |
| C3 | Model Lifecycle Management & Change Control | C3.1–C3.5 |
| C4 | Infrastructure, Configuration & Deployment Security | C4.1–C4.3 |
| C5 | Access Control & Identity for AI Components & Users | C5.1–C5.3 |
| C6 | Supply Chain Security for Models | C6.1–C6.2 |
| C7 | Model Behavior, Output Control & Safety Assurance | C7.1–C7.4 |
| C8 | Memory, Embeddings & Vector Database Security | C8.1–C8.3 |
| C9 | Orchestration & Agentic Security | C9.1–C9.6 |
| C10 | Model Context Protocol (MCP) Security | C10.1–C10.4 |
| C11 | Adversarial Robustness | C11.1–C11.4 |
| C12 | Monitoring, Logging & Anomaly Detection | C12.1–C12.5 |

## Section index

| Section | Title |
|---------|-------|
| C1.1 | Training Data Origin & Data Security |
| C1.2 | Data Labeling and Annotation Security |
| C1.3 | Training Data Quality and Security Assurance |
| C2.1 | Prompt Injection Defenses |
| C2.2 | Content & Policy Screening |
| C3.1 | Model Authorization & Integrity |
| C3.2 | Model Validation & Testing |
| C3.3 | Controlled Deployment & Rollback |
| C3.4 | Secure Development Practices |
| C3.5 | Pipeline Fine-Tuning |
| C4.1 | AI Workload Sandboxing & Validation |
| C4.2 | AI Hardware Security |
| C4.3 | Edge & Distributed AI Security |
| C5.1 | Authentication |
| C5.2 | AI Resource Authorization & Classification |
| C5.3 | Multi-Tenant Isolation |
| C6.1 | Model Artifact Integrity |
| C6.2 | AI BOM & Supply Chain Monitoring |
| C7.1 | Output Format Enforcement |
| C7.2 | Hallucination Detection & Mitigation |
| C7.3 | Output Safety |
| C7.4 | Source Attribution & Citation Integrity |
| C8.1 | Access Controls on Memory & RAG Indices |
| C8.2 | Embedding Sanitization & Validation |
| C8.3 | Memory Expiry & Revocation |
| C9.1 | Execution Budgets, Loop Control, and Circuit Breakers |
| C9.2 | High-Impact Action Approval and Irreversibility Controls |
| C9.3 | Component Isolation and Tool Authorization |
| C9.4 | Agent and Orchestrator Identity |
| C9.5 | Agent Authorization, Delegation, and Continuous Enforcement |
| C9.6 | Shutdown and Graceful Degradation |
| C10.1 | Component Integrity |
| C10.2 | Authentication & Authorization |
| C10.3 | Secure Transport |
| C10.4 | Schema, Message, and Input Validation |
| C11.1 | Model Alignment, Safety, and Robustness Testing and Training |
| C11.2 | Membership-Inference and Model-Inversion Mitigation |
| C11.3 | Model-Extraction Defense |
| C11.4 | Model Runtime Anomaly Detection |
| C12.1 | Request & Response Logging |
| C12.2 | Detection and Alerting |
| C12.3 | Model, Data, and Performance Drift Detection |
| C12.4 | Proactive Security Behavior Monitoring |
| C12.5 | Training Data & Model Lifecycle Audit |

## Changes from the pre-1.0 draft

The v1.0 release renumbered and restructured several chapters. When updating existing
references, note:

| Pre-1.0 draft | AISVS v1.0 |
|---------------|------------|
| C10 Adversarial Robustness & Attack Resistance | **C11** Adversarial Robustness |
| C11 Privacy Protection & PII Management | chapter removed — privacy controls folded into C1 (data minimization), C5.2 (classification & authorization), C8.2 (sensitive-field masking), C11.2 (inference/inversion) |
| C12 Monitoring, Logging & Anomaly Detection | C12 (unchanged number, resectioned) |
| C13 Human Oversight, Accountability & Governance | chapter removed — oversight controls folded into C9.2 (approval gates) and C9.6 (kill-switch, graceful degradation) |
| — | **C10** Model Context Protocol (MCP) Security (new chapter) |
