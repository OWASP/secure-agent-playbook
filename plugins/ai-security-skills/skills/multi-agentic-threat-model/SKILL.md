---
name: multi-agentic-threat-model
description: "Threat model multi-agent AI systems using the CSA MAESTRO 7-layer framework and OWASP Multi-Agentic System Threat Modeling Guide v1.0. Maps agent architectures, identifies cross-layer attack chains, assesses extended multi-agent threats like goal drift and reasoning collapse, and produces a prioritized risk matrix with layered mitigations. Use when performing threat modeling on multi-agent AI systems, reviewing agentic architectures for security risks, assessing LLM-based agent pipelines, or evaluating trust boundaries between cooperating agents."
license: CC-BY-4.0
---

# Multi-Agentic System Threat Modeling

Conduct threat modeling for multi-agent systems using the CSA MAESTRO 7-layer architecture and OWASP Multi-Agentic System Threat Modeling Guide v1.0.

## Steps

1. **MAESTRO 7-Layer Architecture Mapping** — Decompose the target system into CSA's layered reference architecture:

   | Layer | Name | Scope |
   |-------|------|-------|
   | 7 | Agent Ecosystem | User-facing apps, agent marketplace, business integrations |
   | 6 | Security & Compliance | Cross-cutting controls, compliance frameworks |
   | 5 | Evaluation & Observability | Monitoring, metrics, anomaly detection |
   | 4 | Deployment & Infrastructure | Containers, orchestration, cloud/on-prem |
   | 3 | Agent Frameworks | Orchestration logic, tool bindings, routing |
   | 2 | Data Operations | Memory stores, vector DBs, RAG pipelines |
   | 1 | Foundation Models | LLMs, model APIs, inference engines |

   **Checkpoint**: Confirm every agent, tool, data store, and external integration is placed in at least one layer before proceeding.

2. **Layer-Specific Threat Analysis** — For each MAESTRO layer, identify threats using the CSA taxonomy. Focus on:
   - Layer 1: model poisoning, adversarial inputs, inference-time attacks
   - Layer 2: RAG injection, context window manipulation, memory corruption
   - Layer 3: tool-call injection, routing hijack, agent impersonation
   - Layer 7: marketplace supply chain, business logic abuse

3. **Cross-Layer Threat Assessment** — Map attack chains that span multiple layers. Example: a prompt injection at Layer 1 escalates through tool misuse at Layer 3 to exfiltrate data via a compromised RAG pipeline at Layer 2.

   **Checkpoint**: Verify each cross-layer chain has a defined entry point, pivot, and impact target.

4. **Extended Multi-Agent Threats** — Assess MAESTRO framework extensions for complex multi-agent scenarios:
   - **Reasoning Collapse** — Chain-of-thought breakdowns across agent delegation
   - **Goal Drift in Delegated Chains** — Intent mutation through agent handoffs
   - **Trust Misuse Between Legitimate Agents** — Strategic misreporting within valid roles
   - **Emergent Covert Coordination** — Autonomous symbolic protocol development
   - **Heterogeneous Multi-Agent Exploits** — Coordinated attacks using diverse agent capabilities

5. **Architecture Pattern Risk Assessment** — Evaluate the system's multi-agent pattern against known risks:

   | Pattern | Key Risk |
   |---------|----------|
   | Supervisor-agent | Single point of compromise at supervisor |
   | Hierarchical | Privilege escalation through delegation depth |
   | Distributed ecosystem | Lack of centralized trust arbitration |
   | Human-in-the-loop | Approval fatigue bypassing safety checks |

6. **Mitigation Strategy Development** — For each identified threat, recommend layer-specific and cross-layer controls. Prioritize mitigations by risk score (likelihood x impact).

## Example Finding

```markdown
### [HIGH] Goal Drift via Delegated Task Chain

- **CWE**: CWE-285 (Improper Authorization)
- **OWASP Ref**: Agentic Top 10 — A05 Inadequate Agent Authorization
- **Location**: Agent orchestration layer (MAESTRO Layer 3)
- **Impact**: A sub-agent reinterprets a delegated task, expanding its scope
  beyond the original intent — e.g., a "summarize financials" task mutates
  into "export all financial records to an external endpoint."
- **Evidence**: No intent-preservation constraint on delegated task objects;
  sub-agents receive free-text instructions without structured goal boundaries.
- **Remediation**: Enforce structured task schemas with immutable goal fields.
  Add an intent-verification step where the delegating agent confirms the
  sub-agent's planned actions before execution.
- **Confidence**: MEDIUM
```

## Output

Use the finding format from `templates/finding.md`. Produce:
- **MAESTRO 7-Layer Architecture Map** — System decomposition across all layers
- **Layer-Specific Threat Assessment** — Threats per MAESTRO layer with severity
- **Cross-Layer Attack Chain Analysis** — Multi-layer threat scenarios with entry/pivot/impact
- **Extended Multi-Agent Threat Analysis** — Assessment of MAESTRO framework extensions
- **Risk Prioritization Matrix** — Likelihood vs. impact for all identified threats
- **Layered Mitigation Strategy** — Defense-in-depth recommendations per layer

## OWASP References

- CSA MAESTRO Framework — 7-Layer Agentic AI Reference Architecture
- OWASP Multi-Agentic System Threat Modeling Guide v1.0
- OWASP Top 10 for Agentic Applications 2026