---
title: "LLM03 Excessive Agency"
owasp_llm_id: "LLM03"
owasp_llm_version: "2026"
when_to_use:
  - reviewing AI agents with tool-calling or function-calling capabilities
  - auditing MCP server configurations for overpermissioning
  - evaluating autonomous agent workflows for safety controls
  - assessing human-in-the-loop requirements for destructive actions
  - reviewing delegated or multi-agent workflows for authorization propagation
  - checking downstream system permissions granted to LLM tool identities
threats:
  - excessive functionality beyond intended scope
  - deprecated or trial tools remaining available to the agent
  - open-ended tools (shell, URL fetch) with insufficient input filtering
  - overpermissioned tool access (write when read-only needed)
  - generic high-privileged identity instead of per-user context
  - autonomous execution of high-impact actions without confirmation
  - authorization decisions delegated to the model rather than to code
  - tool chaining enabling unintended destructive outcomes
summary: "Damaging actions performed in response to unexpected, ambiguous, or manipulated LLM output. Root causes are excessive functionality, excessive permissions, and excessive autonomy — independent of what made the model malfunction."
aisvs_mappings:
  - section: "C5.1"
    title: "Authentication"
    requirements: ["5.1.1", "5.1.2"]
  - section: "C5.2"
    title: "AI Resource Authorization & Classification"
    requirements: ["5.2.1", "5.2.5"]
  - section: "C9.1"
    title: "Execution Budgets, Loop Control, and Circuit Breakers"
    requirements: ["9.1.1", "9.1.2", "9.1.3"]
  - section: "C9.2"
    title: "High-Impact Action Approval and Irreversibility Controls"
    requirements: ["9.2.1", "9.2.2", "9.2.3", "9.2.4", "9.2.5", "9.2.8", "9.2.10"]
  - section: "C9.3"
    title: "Component Isolation and Tool Authorization"
    requirements: ["9.3.1", "9.3.2", "9.3.3", "9.3.4", "9.3.7", "9.3.8"]
  - section: "C9.4"
    title: "Agent and Orchestrator Identity"
    requirements: ["9.4.1", "9.4.2"]
  - section: "C9.5"
    title: "Agent Authorization, Delegation, and Continuous Enforcement"
    requirements: ["9.5.1", "9.5.2", "9.5.3", "9.5.5", "9.5.6"]
  - section: "C9.6"
    title: "Shutdown and Graceful Degradation"
    requirements: ["9.6.1", "9.6.2", "9.6.3"]
  - section: "C10.2"
    title: "Authentication & Authorization"
    requirements: ["10.2.4", "10.2.5", "10.2.7"]
  - section: "C12.4"
    title: "Proactive Security Behavior Monitoring"
    requirements: ["12.4.1", "12.4.2", "12.4.3"]
---

# LLM03:2026 Excessive Agency

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM03:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM03_ExcessiveAgency.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

An LLM-based system is often granted agency by its developer: the ability to call functions or interface with other systems via tools (also called extensions, plugins, or skills) to undertake actions in response to a prompt. An LLM agent may also select which tool to invoke dynamically, and agent-based systems typically make repeated calls using output from previous invocations to direct subsequent ones.

**Excessive Agency is the vulnerability that enables damaging actions to be performed in response to unexpected, ambiguous, or manipulated outputs from an LLM — regardless of what is causing the LLM to malfunction.** Common triggers:

- hallucination/confabulation from poorly-engineered benign prompts, or a poorly-performing/misaligned model
- direct or indirect prompt injection from a malicious user, a compromised tool, or (in multi-agent systems) a compromised peer agent

The root cause is typically one or more of **excessive functionality**, **excessive permissions**, or **excessive autonomy**.

Excessive Agency differs from [LLM10 Improper Output Handling](LLM10.md), which concerns insufficient scrutiny of LLM outputs. Sanitization of model inputs and outputs is **not a root control** for Excessive Agency — inputs are covered by [LLM01](LLM01.md), outputs by [LLM10](LLM10.md).

## Potential Impacts

Impacts span the full confidentiality, integrity, and availability spectrum, bounded by which systems the app can interact with. In agentic systems this manifests as ASI02 Tool Misuse & Exploitation, ASI03 Identity & Privilege Abuse, and ASI08 Cascading Failures.

## Common Examples of Risk

### Excessive Functionality

1. The agent has access to tools including functions not needed for intended operation — e.g. a document-read requirement satisfied with a third-party tool that also modifies and deletes.
2. A tool trialed during development and dropped in favor of an alternative remains available to the agent.
3. An open-ended tool fails to filter input instructions — e.g. a tool meant to run one specific shell command fails to prevent other commands.

### Excessive Permissions

4. A tool has downstream permissions beyond what is needed — e.g. a read-only tool connecting with an identity holding UPDATE, INSERT, and DELETE.
5. A tool designed to operate in an individual user's context accesses downstream systems with a generic high-privileged identity — e.g. reading the current user's documents with an account that can reach all users' files.

### Excessive Autonomy

6. The application fails to independently verify and approve high-impact actions — e.g. deleting user documents without confirmation.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Minimize tools | Limit callable tools to the minimum necessary. If URL fetching is not required, do not offer the tool. |
| 2 | Minimize tool functionality | A mailbox-summarizing tool needs read only — it should not also delete or send. |
| 3 | Avoid open-ended tools | Prefer a specific file-writing tool over "run a shell command". Define a strict input schema and validate before use. |
| 4 | Minimize tool permissions | Enforce least privilege at the downstream identity — read access to one table, not the database. |
| 5 | Execute tools in the user's context | Track user authorization and scope; require OAuth with minimum scope. **In delegated or multi-agent workflows, preserve the original user context across chained calls** rather than relying on the calling agent's identity. |
| 6 | Require user approval | Human-in-the-loop for high-impact actions, implemented downstream or within the tool itself. |
| 7 | Complete mediation | Implement authorization **in logic, not by asking the LLM**. Validate every downstream request against policy at the tool, at an independent pre-execution policy decision point, or at the downstream system. A graduated policy (audit, warn, block, escalate) lets recoverable actions auto-approve while irreversible ones route to human review. |

These do not prevent Excessive Agency but limit damage:

| # | Strategy | Description |
|---|----------|-------------|
| 8 | Monitor tool use | Log and monitor tool and downstream activity to identify undesirable actions and respond. |
| 9 | Rate limiting | Thresholds on tool invocation with circuit breakers that halt, rate-limit, or escalate. Context-aware thresholds can key on the cumulative value of an input parameter. |

## Example Attack Scenarios

**Hijacked email assistant** — a personal-assistant app is granted mailbox access to summarize incoming email. The chosen tool also contains send functions. An indirect prompt injection in an incoming email tricks the LLM into scanning the inbox for sensitive information and forwarding it to the attacker. Avoidable by:

- eliminating excessive functionality — use a read-only mail tool
- eliminating excessive permissions — authenticate via OAuth with a read-only scope
- eliminating excessive autonomy — require the user to review and send every drafted mail

Damage could alternatively be reduced by rate-limiting the mail-sending interface.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C5.1 Authentication | Step-up authentication for high-risk AI operations; short-lived minimal-scope agent tokens | 5.1.1, 5.1.2 |
| C5.2 AI Resource Authorization & Classification | Default-deny on AI resources; policy decision point isolated from the agent runtime | 5.2.1, 5.2.5 |
| C9.1 Execution Budgets & Circuit Breakers | Per-tool quotas and timeouts, per-execution budgets, swarm-level kill-switch | 9.1.1, 9.1.2, 9.1.3 |
| C9.2 High-Impact Action Approval | Deterministic approval gate, canonicalized parameters, reversibility classification and enforcement, self-modification bounds, cryptographically bound approvals, chain-level gating | 9.2.1–9.2.5, 9.2.8, 9.2.10 |
| C9.3 Component Isolation and Tool Authorization | Least-privilege sandbox, schema-validated tool output, manifest declaration and runtime enforcement, external-resource allow-list, automated containment | 9.3.1–9.3.4, 9.3.7, 9.3.8 |
| C9.4 Agent and Orchestrator Identity | Unique cryptographic agent identity; actions bound to each execution-chain step | 9.4.1, 9.4.2 |
| C9.5 Agent Authorization & Delegation | Fine-grained tool *and parameter-value* authorization, scope-limited delegated user context, policy-engine (never model) access decisions, delegation policy, continuous re-evaluation | 9.5.1–9.5.3, 9.5.5, 9.5.6 |
| C9.6 Shutdown and Graceful Degradation | Manual kill-switch, fail-closed approval timeout, out-of-band shutdown channel | 9.6.1, 9.6.2, 9.6.3 |
| C10.2 MCP Authentication & Authorization | Scope-filtered tools/list, per-invocation authorization down to argument values, no token pass-through | 10.2.4, 10.2.5, 10.2.7 |
| C12.4 Proactive Security Behavior Monitoring | Pre-execution evaluation of autonomous triggers, approval audit trail, kill-switch logging | 12.4.1, 12.4.2, 12.4.3 |

## Related Frameworks

- ASI02 — Tool Misuse & Exploitation (OWASP Top 10 for Agentic Applications)
- ASI03 — Identity & Privilege Abuse (OWASP Top 10 for Agentic Applications)
- ASI08 — Cascading Failures (OWASP Top 10 for Agentic Applications)
- AML.T0053 — LLM Plugin Compromise (MITRE ATLAS)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
