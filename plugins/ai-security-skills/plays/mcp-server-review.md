# Play: MCP Server Security Review

Audit Model Context Protocol (MCP) server configurations and implementations for security vulnerabilities including overpermissioning, injection risks, data exposure, and tool definitions that change after approval (rug pulls).

## Trigger Conditions

Use this skill when:
- Reviewing MCP server source code or configuration
- Auditing a Claude Code setup's MCP integrations
- Evaluating third-party MCP servers before installation
- A user asks "is this MCP server safe to use?"

## Inputs

- MCP server source code (especially tool handler implementations)
- MCP client configuration (e.g., Claude Code settings, `mcp_servers` config)
- MCP client name and version, plus its source code or a build you can run (for §8)
- Server manifest / tool definitions (names, descriptions, parameter schemas)
- Network configuration (stdio vs SSE/HTTP transport, authentication)

## Procedure

### 1. Transport & Authentication Review

| Check | Risk | What to Look For |
|-------|------|-----------------|
| Transport type | Varies | stdio (local) vs HTTP/SSE (network). Network transports need auth. |
| Authentication | HIGH if missing | Is there auth on HTTP/SSE endpoints? Token-based? mTLS? |
| TLS | HIGH if missing | Is HTTPS enforced for network transports? |
| CORS | MEDIUM | For HTTP transports, are CORS headers restrictive? |
| Origin validation | HIGH | Does the server validate the client's origin? |

### 2. Tool Permission Audit

For each tool the MCP server exposes:

```
Tool: [name]
Description: [what it claims to do]
Parameters: [schema]
Actual capability: [what it ACTUALLY does — read source code]
Risk level: [READ-ONLY | MUTATION | DESTRUCTIVE | NETWORK | CREDENTIAL-ACCESS]
Least privilege: [Does the tool do more than its description suggests?]
```

Flag:
- Tools with broader capabilities than their descriptions indicate
- Tools that accept free-form input (shell commands, SQL, file paths, URLs)
- Tools that can read/write credentials, environment variables, or secrets
- Tools that can make arbitrary network requests
- Tools with no input validation on parameters

### 3. Input Validation & Injection Analysis

For each tool's parameters:
- **Command injection**: Does any parameter get interpolated into shell commands?
- **Path traversal**: Do file path parameters allow `../` or absolute paths outside intended scope?
- **SQL injection**: Are parameters used in database queries without parameterization?
- **SSRF**: Can URL parameters be used to hit internal services?
- **Template injection**: Are parameters inserted into templates that get evaluated?

Check the parameter schema:
- Are types enforced (string, number, enum)?
- Are there format constraints (regex, max length, allowed characters)?
- Are enum values used where possible instead of free-form strings?

### 4. Data Exposure Assessment

- **Resource endpoints**: What data do MCP resources expose? Can they leak secrets, PII, or internal configs?
- **Tool outputs**: Do tool responses include more data than the client needs?
- **Error messages**: Do errors leak internal paths, stack traces, or credentials?
- **Logging**: Does the server log sensitive inputs or outputs?
- **Prompt context**: Tool descriptions and resource content become part of the LLM's context — do they contain sensitive info?

### 5. Scope & Sandboxing

- **File system scope**: Is file access restricted to specific directories?
- **Network scope**: Can the server reach internal services, cloud metadata endpoints (169.254.169.254)?
- **Process scope**: Does the server run with minimal OS permissions?
- **Resource limits**: Are there timeouts, rate limits, or output size limits?
- **Dependency surface**: What packages does the server depend on? Are they audited?

### 6. Supply Chain Assessment

- **Source**: Is the MCP server from a trusted source? Is the repo verified?
- **Dependencies**: Run SCA against the server's dependencies
- **Build integrity**: Is there a lockfile? Are builds reproducible?
- **Update mechanism**: How is the server updated? Can updates be tampered with?
- **Code review**: Has the implementation been reviewed by someone other than the author?

### 7. Configuration Review

Check the client-side MCP configuration:
- Are server paths absolute and specific (not user-controlled)?
- Are environment variables passed to the server minimized?
- Are sensitive env vars (API keys, tokens) only passed to servers that need them?
- Is the server command safe from injection (no shell expansion in args)?

### 8. Tool Definition Integrity (Rug Pull)

A server can change a tool's definition after the user approved it, and a remote server can do so at any time without a package update, so §6 does not cover it. Like §7, this step checks the client. If the client is out of scope, record the step as not assessed and note whether the server is remote or third-party.

CVE-2025-54136 shows the same flaw on the configuration side: Cursor 1.2.4 and earlier did not re-prompt when an approved MCP server entry was changed to run a different command (fixed in 1.3).

Check that the client:

1. **Pins what the user approved**: each tool's complete definition from `tools/list` (`name`, `title`, `description`, `inputSchema`, `outputSchema`, `annotations`), the server `instructions` if the client passes them to the model, and the server entry (command, args or URL). The client must keep the approved definition itself, not only a hash, so it can show what changed. A hash over a canonical serialisation (e.g. RFC 8785 JCS with SHA-256) can detect a change but cannot show it.
2. **Re-checks before use**: compares against the pin every time it fetches `tools/list`: at startup or on a new session, when a cached list expires (`ttlMs` in spec 2026-07-28), and when `notifications/tools/list_changed` arrives (in spec 2026-07-28 the client only receives it if it opened a `subscriptions/listen` stream). Re-checking before each call is better, but its absence is not a finding. A changed `serverInfo.version` is not a pin: the version is self-reported, and the MCP spec (2026-07-28, `server/discover`) says clients should not rely on it for security decisions.
3. **Blocks and requires human review on change**: stops using the changed tool, shows the user the old and new value of every changed field (including a flipped `readOnlyHint` or `destructiveHint`), and requires explicit re-approval before the next call. No change is accepted automatically, whatever its size or the part it touches.

Confirm with the client's code and a test server you control. Build the test server with the official MCP SDK, and capture `tools/list` before and after each change with the MCP Inspector CLI (`npx @modelcontextprotocol/inspector --cli <server command> --method tools/list`); the two snapshots are the Evidence. [`examples/mcp-rugpull-fixture`](https://github.com/OWASP/secure-agent-playbook/tree/main/examples/mcp-rugpull-fixture) is such a server. Approve one tool that has `readOnlyHint: true`, then run each test, restoring the approved definition between tests. In tests 1 and 3, have the server change the definition when the first call arrives, and make the second call depend on the first call's result; otherwise the model can send both calls before the notification arrives.

1. Change one word of the description and send `notifications/tools/list_changed`. Tests `list_changed` handling.
2. Change one word of the description without a notification, then restart the client or start a new session. Tests the re-check on fetch.
3. Flip `readOnlyHint` from `true` to `false` without changing `serverInfo.version`, then send `notifications/tools/list_changed`. Tests whether the pin covers `annotations` and whether re-approval depends on the version.
4. Change the server entry's command, args or URL in the client configuration. Tests whether the pin covers the server entry.
5. For every change the client detects, check whether it blocks the tool and whether the re-approval prompt shows the old and new values.

Record what the client does each time: blocks and asks, warns only, accepts silently, or does not notice.

A pin detects changed definitions, not changed server code behind an unchanged definition. Annotations are hints: the MCP spec says clients must treat them as untrusted unless the server is trusted.

Report each missing control with `templates/finding.md`. If the client pins nothing, report only the "No pin" row and, if it applies, the server entry row: the other rows assume a pin exists. OWASP Ref: MCP03:2025 and LLM06, plus LLM01 when the changed part reaches the model (`description`, `instructions`). Confidence: HIGH if the test server reproduces it, MEDIUM from code alone.

| Missing control | Severity | CWE | OpenCRE |
|-----------------|----------|-----|---------|
| No pin: approval is not bound to the definition | HIGH | CWE-353 | [307-507](https://www.opencre.org/cre/307-507) |
| Pin leaves out `description` or `inputSchema` | HIGH | CWE-353 | [307-507](https://www.opencre.org/cre/307-507) |
| Server entry (command, args or URL) not pinned | HIGH | CWE-353 | [307-507](https://www.opencre.org/cre/307-507) |
| Pin leaves out `title`, `annotations`, `outputSchema` or `instructions` | MEDIUM (HIGH if the client skips confirmation on `readOnlyHint`) | CWE-353 | [307-507](https://www.opencre.org/cre/307-507) |
| Pin not checked when `tools/list` is fetched (startup, new session, cache expiry) | HIGH | CWE-354 | — |
| `notifications/tools/list_changed` not handled | MEDIUM | CWE-354 | — |
| Re-approval triggered only by a new `serverInfo.version` | HIGH | CWE-807 | — |
| Change detected, but the tool is not blocked, or is re-approved without the user (e.g. small description edits accepted automatically) | HIGH | CWE-356 | — |
| Re-approval prompt that does not show the old and new values | MEDIUM | CWE-357 | — |

`—`: the OpenCRE API (`GET /rest/v1/standard/CWE/sectionid/{id}`) returns no CRE for this CWE (CWE-356, CWE-357, CWE-807), or none that fits this control (CWE-354).

## Output Format

```markdown
## MCP Server Security Review: [Server Name]

### Server Overview
- **Transport**: stdio | HTTP/SSE
- **Tools exposed**: [count]
- **Resources exposed**: [count]
- **Language/Runtime**: [Node.js, Python, etc.]
- **Source**: [repo URL or "local/custom"]

### Tool Risk Matrix
| Tool | Capability Type | Input Validation | Risk Level |
|------|----------------|-----------------|------------|
| tool_name | READ-ONLY | Schema-validated | LOW |
| tool_name | MUTATION | Free-form string | HIGH |

### Tool Definition Integrity (client: [name and version])
- **Pinned**: [fields covered, or "none"]
- **Re-checked**: before each call | on every `tools/list` fetch + `list_changed` | on fetch only | on `list_changed` only | on version change only | never
- **On change**: blocks + old/new diff + human re-approval | auto-accepts some changes | warns only | nothing

### Findings
[Standard finding template for each issue]

### Configuration Recommendations
[Specific config changes to reduce risk]
```

## OWASP References

- **LLM01**: Prompt Injection (via tool descriptions and outputs)
- **LLM02**: Sensitive Information Disclosure (secrets/PII in resources and tool outputs)
- **LLM05**: Improper Output Handling (tool output rendering)
- **LLM06**: Excessive Agency (overpermissioned tools)
- **LLM07**: System Prompt Leakage (sensitive data in tool descriptions)
- OWASP Top 10: A01 Broken Access Control, A03 Injection
- OWASP MCP Top 10 (2025): MCP03 Tool Poisoning (includes rug pulls)
- OWASP Cheat Sheet: MCP Security (Tool Description & Schema Integrity)
