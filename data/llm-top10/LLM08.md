---
title: "LLM08 Hidden Context Exposure"
owasp_llm_id: "LLM08"
owasp_llm_version: "2026"
when_to_use:
  - reviewing system prompts for embedded secrets or credentials
  - assessing whether hidden-context disclosure reveals exploitable information
  - evaluating guardrail configurations that rely on prompt secrecy
  - reviewing tool and function schemas exposed to the model
  - auditing LLM apps for prompt extraction vulnerabilities
  - assessing whether authorization is delegated to the system prompt
threats:
  - exposure of tool and function schemas, API keys, or database credentials
  - disclosure of behavioral control logic and internal decision-making
  - reverse engineering of safety and refusal mechanisms
  - disclosure of permissions and user roles
  - exposure of output structure and formatting rules
  - reliance on hidden context as a security boundary
summary: "Unauthorized extraction, inference, or reconstruction of hidden, non-user-facing system instructions or operational context. Security-relevant when that context contains secrets, policy logic, tool schemas, or trust boundaries that materially increase attacker capability."
aisvs_mappings:
  - section: "C2.1"
    title: "Prompt Injection Defenses"
    requirements: ["2.1.3", "2.1.6"]
  - section: "C5.2"
    title: "AI Resource Authorization & Classification"
    requirements: ["5.2.1", "5.2.4", "5.2.5"]
  - section: "C7.1"
    title: "Output Format Enforcement"
    requirements: ["7.1.1"]
  - section: "C7.3"
    title: "Output Safety"
    requirements: ["7.3.2", "7.3.4"]
  - section: "C9.3"
    title: "Component Isolation and Tool Authorization"
    requirements: ["9.3.3", "9.3.4"]
  - section: "C9.5"
    title: "Agent Authorization, Delegation, and Continuous Enforcement"
    requirements: ["9.5.1", "9.5.3", "9.5.4"]
  - section: "C10.2"
    title: "Authentication & Authorization"
    requirements: ["10.2.4", "10.2.5"]
  - section: "C11.1"
    title: "Model Alignment, Safety, and Robustness Testing and Training"
    requirements: ["11.1.1", "11.1.3"]
  - section: "C12.2"
    title: "Detection and Alerting"
    requirements: ["12.2.3"]
---

# LLM08:2026 Hidden Context Exposure

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM08:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM08_HiddenContextExposure.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

> **Renamed in 2026.** This entry supersedes LLM07:2025 System Prompt Leakage, broadening it from the system prompt alone to all hidden, non-user-facing context the application assembles into the model's context window.

## Description

Hidden Context Exposure is the unauthorized extraction, inference, or reconstruction of hidden, non-user-facing system instructions or operational context placed in a model's context. It becomes security-relevant when that hidden context contains or reveals secrets, policy logic, tools, trust boundaries, workflow criteria, proprietary behavior, or other sensitive implementation details that materially increase attacker capability.

Hidden context typically includes the system prompt, developer instructions, retrieved policy text (from RAG knowledge bases, configuration stores, or user-profile services), the schemas of tools and functions the application exposes, and other rules and directives assembled into the context window. **The common thread is that this context is not intended to be visible to end users but is accessible to the model.**

**Design under the assumption that hidden context is discoverable** and that nothing in the context should be considered a secret. Ensure disclosure of hidden context has little or no direct security impact. Sensitive data such as credentials, connection strings, and tokens should not be embedded in it, nor should hidden context be relied on as a security boundary for authorization, privilege separation, policy enforcement, or content filtering.

### Severity

Severity tracks what is placed in hidden context and how the application relies on it:

| Level | Condition |
|-------|-----------|
| **Informational** | No secrets, no security-relevant logic, no reliance on confidentiality |
| **Medium** | Internal rules, filtering criteria, role descriptions, or workflow logic that meaningfully aids an attacker but does not gate critical decisions |
| **High** | Embedded credentials or tokens, or reliance on hidden-context secrecy for authorization or content policy |
| **Critical** | Disclosure chains to remote code execution, broad data exfiltration, or privilege escalation in a connected system |

### Amplification of adjacent risks

- Disclosed rules or logic enable more targeted prompt injection ([LLM01](LLM01.md))
- Embedded credentials constitute sensitive information disclosure ([LLM02](LLM02.md))
- Revealed tool permissions and schemas expand the surface for excessive agency ([LLM03](LLM03.md))
- Leaked output-formatting rules can facilitate improper output handling ([LLM10](LLM10.md))

**Out of scope**: leakage of regulated user or training data ([LLM02](LLM02.md)); agentic amplifications such as persistent memory, inter-agent channels, and multi-step agent compromise (OWASP Top 10 for Agentic Applications); generic application-security concerns such as server-side log leakage and client-side bundle inspection.

## Common Examples of Risk

1. **Exposure of sensitive functionality, tool and function schemas** — system architecture, available tools, API keys, database credentials, or user tokens. **The real risk is that sensitive credentials are placed in hidden context in the first place.**
2. **Exposure of behavioral control logic** — internal decision-making processes that let attackers understand how to exploit weaknesses or bypass controls.
3. **Reverse engineering of safety and refusal mechanisms** — leakage reveals the underlying triggers, conditions, and exceptions behind a refusal, letting attackers craft inputs that avoid known patterns or exploit enforcement gaps.
4. **Disclosure of permissions and user roles** — a tool description on an internal MCP server may indicate that a user needs the developer role, inviting directed probing.
5. **Exposure of output structure and formatting rules** — knowledge of required JSON schemas, templates, or validation constraints lets attackers generate conforming responses embedding manipulated values, leading to incorrect parsing or unintended downstream behavior.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Do not put sensitive data in hidden context | Never embed credentials, secrets, or security-critical configuration in system prompts or hidden context. **Assume all context available to the LLM is available to users.** Externalize to systems the model does not directly access. |
| 2 | Use deterministic methods and guardrails for validation and behavior control | Hidden context must not be the primary mechanism for controlling behavior. Fine-tuning may reduce disclosure risk but provides no guarantee. Enforce critical behaviors through independent deterministic systems outside the model — harmful-content detection belongs in external safeguards, not prompt instructions. |
| 3 | Enforce authorization and access control independently from the LLM | Privilege separation and authorization bounds checks must not be delegated to the LLM through any mechanism. Enforce deterministically and auditably. Where tasks require different access levels, separate them by authorization context and grant each only the privileges it requires. |

## Example Attack Scenarios

1. **Credential leakage via system prompt** — a system prompt contains credentials for a tool the LLM can access. The prompt leaks, and the attacker uses those credentials elsewhere.
2. **Tool schema via context extraction** — an attacker extracts the tool list and parameter schemas through conversational probing and crafts inputs steering the application toward specific tool calls. No credential is disclosed and no policy is overtly bypassed, but the attacker now has concrete targets for subsequent injection and reconnaissance for downstream action chaining.
3. **Bypassing restrictions via guardrail disclosure** — an attacker extracts a system prompt prohibiting offensive content, external links, and code execution, then uses the disclosed restrictions to craft an injection that bypasses them.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C2.1 Prompt Injection Defenses | Injection screening with blocking; instruction hierarchy so system messages override user input | 2.1.3, 2.1.6 |
| C5.2 AI Resource Authorization & Classification | Default-deny access control, post-inference filtering, **policy decision point isolated from the agent's execution environment** | 5.2.1, 5.2.4, 5.2.5 |
| C7.1 Output Format Enforcement | Schema validation with rejection on mismatch | 7.1.1 |
| C7.3 Output Safety | **Block responses disclosing system prompt content or backend data**; detect hidden or encoded output | 7.3.2, 7.3.4 |
| C9.3 Component Isolation and Tool Authorization | Tool manifests declaring required privileges, enforced by the runtime rather than described in the prompt | 9.3.3, 9.3.4 |
| C9.5 Agent Authorization & Delegation | Runtime-enforced fine-grained authorization, **access decisions never made by the model**, **secrets kept out of the context window, system prompts, and tool arguments** | 9.5.1, 9.5.3, 9.5.4 |
| C10.2 MCP Authentication & Authorization | Scope-filtered tools/list so unauthorized tool schemas are never exposed; per-invocation authorization | 10.2.4, 10.2.5 |
| C11.1 Alignment, Safety & Robustness Testing | Alignment training against disallowed disclosure; adversarial evaluation for extraction | 11.1.1, 11.1.3 |
| C12.2 Detection and Alerting | Custom rules detecting system-prompt extraction attempts | 12.2.3 |

## Related Frameworks

- AML.T0056 — LLM Meta Prompt Extraction (MITRE ATLAS)
- ASI06 — Memory and Context Poisoning (OWASP Top 10 for Agentic Applications)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
