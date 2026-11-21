---
name: mcp-server-review
description: Security review of MCP (Model Context Protocol) server implementations and configurations. Use when auditing MCP server source code, evaluating third-party MCP servers before installation, or reviewing Claude Code MCP integrations for overpermissioning, injection risks, data exposure, and tool definitions that change after approval (rug pulls).
license: CC-BY-4.0
---

# MCP Server Security Review

Audit an MCP server by following the full procedure in `plays/mcp-server-review.md`.

## Steps

1. **Transport & Authentication** — Check transport type (stdio vs HTTP/SSE), authentication on network transports, TLS enforcement, CORS policy, origin validation.

2. **Tool Permission Audit** — For each exposed tool: document what it claims to do vs what it actually does (read source). Classify as READ-ONLY, MUTATION, DESTRUCTIVE, NETWORK, or CREDENTIAL-ACCESS. Flag tools with broader capabilities than descriptions suggest, free-form inputs, or credential access.

3. **Input Validation & Injection** — For each tool parameter: check for command injection (shell interpolation), path traversal (../ in file paths), SQL injection (unparameterized queries), SSRF (user-supplied URLs hitting internal services), and template injection.

4. **Data Exposure** — Assess MCP resources for secrets/PII leakage, tool outputs for excessive data, error messages for internal paths/stack traces, and logging for sensitive data capture.

5. **Scope & Sandboxing** — Check file system restrictions, network scope (can it reach cloud metadata 169.254.169.254?), process permissions, resource limits, and dependency surface.

6. **Supply Chain** — Verify source trustworthiness, run SCA on dependencies, check for lockfiles and reproducible builds, assess update mechanism.

7. **Client Configuration** — Review MCP client config for absolute/specific server paths, minimized env var passthrough, and command injection safety in args.

8. **Tool Definition Integrity (Rug Pull)** — Check that the client pins what the user approved (each tool's complete definition including annotations, the server instructions, and the server entry), re-checks it every time it fetches `tools/list` (startup, new session, cache expiry, `notifications/tools/list_changed`), and on any change blocks the tool, shows the user the old and new values, and requires human re-approval (no change is accepted automatically). A changed `serverInfo.version` is not a pin. Confirm with a test server built on the official MCP SDK and before/after `tools/list` snapshots from the MCP Inspector CLI.

## Output

Server overview, tool risk matrix, tool definition integrity summary, findings using `templates/finding.md`, and specific configuration recommendations.

## OWASP References

- LLM01: Prompt Injection (via tool descriptions and outputs)
- LLM02: Sensitive Information Disclosure
- LLM05: Improper Output Handling
- LLM06: Excessive Agency (overpermissioned tools)
- LLM07: System Prompt Leakage
- A01: Broken Access Control
- A03: Injection
- MCP03:2025: Tool Poisoning (includes rug pulls)
- OWASP Cheat Sheet: MCP Security
