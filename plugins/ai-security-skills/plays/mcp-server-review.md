# Play: MCP Server Security Review

Audit Model Context Protocol (MCP) server configurations and implementations for security vulnerabilities including overpermissioning, injection risks, and data exposure.

## Trigger Conditions

Use this skill when:
- Reviewing MCP server source code or configuration
- Auditing a Claude Code setup's MCP integrations
- Evaluating third-party MCP servers before installation
- A user asks "is this MCP server safe to use?"

## Inputs

- MCP server source code (especially tool handler implementations)
- MCP client configuration (e.g., Claude Code settings, `mcp_servers` config)
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

### Findings
[Standard finding template for each issue]

### Configuration Recommendations
[Specific config changes to reduce risk]
```

## OWASP References

- **LLM01**: Prompt Injection (via tool descriptions and outputs)
- **LLM02**: Insecure Output Handling (tool output rendering)
- **LLM06**: Excessive Agency (overpermissioned tools)
- **LLM07**: System Prompt Leakage (sensitive data in tool descriptions)
- OWASP Top 10: A01 Broken Access Control, A03 Injection
