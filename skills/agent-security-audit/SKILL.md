---
name: agent-security-audit
description: Audit AI agent configurations for security risks — excessive permissions, prompt injection surfaces, data exfiltration paths, and missing guardrails. Use when reviewing CLAUDE.md files, MCP configs, agent orchestration code, or any AI agent setup.
license: CC-BY-4.0
---

# Agent Security Audit

Evaluate an AI agent's security posture by following the full procedure in `plays/tier4-ai-security/agent-security-audit.md`.

## Steps

1. **Permission Inventory** — Enumerate every tool, MCP server, file system path, network access, and credential the agent has. Flag capabilities beyond what its stated purpose requires.

2. **Prompt Injection Surface Analysis** — For each input path (user messages, tool outputs, MCP resources, RAG documents), assess whether crafted input could cause the agent to invoke unintended tools, override instructions, or exfiltrate data.

3. **Excessive Agency Assessment (OWASP LLM06)** — Check whether destructive/irreversible actions require confirmation, whether access exceeds need, whether the agent can escalate its own privileges, and whether individually-safe tool calls can chain into harmful outcomes.

4. **Data Exfiltration Path Analysis** — Map how sensitive data could leave the agent boundary: secrets passed to external tools, file contents in web requests, cross-MCP-server data forwarding, sensitive data in logs.

5. **Tool-Call Injection Assessment** — For each tool: can user-controlled input reach tool parameters unsanitized? Check for command injection, path traversal, SSRF, and SQL injection through agent-constructed calls.

6. **Guardrail Evaluation** — Check for system prompt safety instructions, tool call confirmations, output filtering, rate limiting, audit logging, and sandboxing.

## Output

Use the finding format from `templates/finding.md`. Produce a Permission Summary table, Risk Findings, Injection Surface Map, and prioritized Recommendations.

## OWASP References

- LLM01: Prompt Injection
- LLM02: Insecure Output Handling
- LLM06: Excessive Agency
- LLM07: System Prompt Leakage
- LLM08: Vector and Embedding Weaknesses
