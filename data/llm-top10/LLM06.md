---
title: "LLM06 Excessive Agency"
owasp_llm_id: "LLM06"
when_to_use:
  - reviewing AI agents with tool-calling or function-calling capabilities
  - auditing MCP server configurations for overpermissioning
  - evaluating autonomous agent workflows for safety controls
  - assessing human-in-the-loop requirements for destructive actions
threats:
  - excessive functionality beyond intended scope
  - overpermissioned tool access (write when read-only needed)
  - autonomous execution of high-impact actions without confirmation
  - tool chaining enabling unintended destructive outcomes
  - deprecated plugins remaining accessible to agents
summary: "Excessive agency occurs when LLM-based systems are granted overpermissioned tools, excessive functionality, or autonomous execution of high-impact actions without adequate human oversight or privilege constraints."
---

# LLM06:2025 Excessive Agency

## Description

LLM-based systems granted agency to invoke functions or extensions may suffer from excessive agency vulnerabilities. This occurs when damaging actions result from unexpected or manipulated LLM outputs, triggered by hallucination, prompt injection, or compromised agents. Root causes include excessive functionality, excessive permissions, and excessive autonomy. Impacts span confidentiality, integrity, and availability.

## Common Examples

**Excessive Functionality:**
1. LLM agents accessing extensions with unneeded capabilities beyond intended scope
2. Deprecated development plugins remaining accessible to agents
3. Extensions that run specific commands failing to prevent other commands from executing

**Excessive Permissions:**
4. Extensions possessing database permissions beyond operational needs (UPDATE/DELETE when only SELECT required)
5. Extensions connecting to document repositories with privileged accounts

**Excessive Autonomy:**
6. High-impact actions lacking independent verification or user approval before execution

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Minimize extensions | Limit available extensions to essential functions only. |
| 2 | Limit functionality | Restrict extension functionality to minimum necessary operations. |
| 3 | Avoid open-ended extensions | Avoid unrestricted tools like generic shell command or URL fetch. |
| 4 | Minimize permissions | Restrict extension permissions to minimum required levels. |
| 5 | User-context execution | Execute extensions within individual user contexts with minimal privileges. |
| 6 | Human-in-the-loop | Implement approval for significant or destructive actions. |
| 7 | Downstream authorization | Enforce authorization in downstream systems rather than relying on LLM decisions. |
| 8 | Input/output sanitization | Sanitize inputs and outputs following OWASP ASVS standards. |
| 9 | Rate limiting | Monitor extension activity and implement rate-limiting for undesirable actions. |

## Example Attack Scenarios

1. **Email exfiltration** — A personal assistant app with mailbox access is exploited via malicious incoming email. Hidden instructions trick the LLM into scanning the inbox for sensitive information and forwarding it to the attacker.
2. **Tool chaining** — Individually safe tool calls are chained together to achieve a harmful outcome that no single tool would permit.

## Related Frameworks

- CWE-250 — Execution with Unnecessary Privileges
- CWE-732 — Incorrect Permission Assignment for Critical Resource

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [Slack AI Data Exfil from Private Channels — PromptArmor](https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via)
- [Embrace the Red: Confused Deputy Problem](https://embracethered.com/blog/posts/2023/chatgpt-cross-plugin-request-forgery-and-prompt-injection/)
