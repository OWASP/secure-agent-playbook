# Play: Agent Security Audit

Evaluate AI agent implementations for security risks including excessive permissions, prompt injection surfaces, data exfiltration paths, and unsafe tool usage.

## Trigger Conditions

Use this skill when:
- Reviewing an AI agent's configuration, tool definitions, or system prompts
- Auditing MCP server setups, Claude Code CLAUDE.md files, or agent orchestration code
- Assessing whether an agent has appropriate guardrails before deployment
- A user asks "is this agent safe?" or "review my agent setup"

## Inputs

- Agent configuration files (CLAUDE.md, MCP configs, tool definitions, system prompts)
- Source code for custom tools or MCP servers the agent can invoke
- Description of what the agent is intended to do (scope of authorized behavior)

## Procedure

### 1. Permission Inventory

Enumerate every tool and capability the agent has access to:
- List all MCP servers and their exposed tools
- List all shell/bash capabilities and whether they are sandboxed
- List all file system access (read/write paths)
- List all network access (APIs, webhooks, external services)
- List all credential access (env vars, secret stores, OAuth tokens)

Flag: Does the agent have capabilities beyond what its stated purpose requires?

### 2. Prompt Injection Surface Analysis

> For technique-level injection testing (18 attack techniques, 20 evasion methods), see [`prompt-injection-testing.md`](prompt-injection-testing.md).

For each input path to the agent, assess injection risk:

| Input Path | Risk Level | Injection Vector |
|------------|-----------|-----------------|
| User messages | Medium | Direct prompt injection |
| Tool outputs (API responses, file contents, web fetches) | High | Indirect prompt injection |
| MCP resource content | High | Indirect prompt injection via resource data |
| Retrieved documents (RAG) | High | Indirect prompt injection via poisoned documents |
| Environment variables | Low | Supply chain / config injection |

For each HIGH risk path, check:
- Is the input sanitized or validated before the agent processes it?
- Can the input cause the agent to invoke tools it shouldn't?
- Can the input override system prompt instructions?
- Can the input exfiltrate data through tool calls (e.g., encoding secrets in URLs)?

### 3. Excessive Agency Assessment (OWASP LLM06)

Check whether the agent can:
- **Execute without confirmation**: Are destructive or irreversible actions gated behind user approval?
- **Access beyond need**: Does the agent have read/write access to files or systems it doesn't need?
- **Escalate privileges**: Can the agent modify its own permissions, install packages, or change configs?
- **Act on external systems**: Can the agent push code, send messages, create issues, or modify infrastructure without explicit authorization?
- **Chain actions dangerously**: Can a sequence of individually-safe tool calls combine into a harmful outcome?

### 4. Data Exfiltration Path Analysis

Map how sensitive data could leave the agent's boundary:
- Can the agent read secrets/credentials and pass them to external tools?
- Can the agent include file contents in web requests, API calls, or messages?
- Can tool outputs from one MCP server be forwarded to another?
- Are there logging mechanisms that might capture sensitive data?

### 5. Tool-Call Injection Assessment

For each tool the agent can invoke:
- Can user-controlled input be passed unsanitized into tool parameters?
- For shell/bash tools: is command injection possible?
- For file tools: is path traversal possible?
- For API tools: can parameters be manipulated to hit unintended endpoints?
- For database tools: is SQL injection possible through agent-constructed queries?

### 6. Guardrail Evaluation

Check for presence and effectiveness of:
- System prompt safety instructions (and whether they can be overridden)
- Tool call confirmation requirements for sensitive operations
- Output filtering (PII, credentials, internal paths)
- Rate limiting or action budgets
- Audit logging of agent actions
- Sandboxing (filesystem, network, process isolation)

## Output Format

```markdown
## Agent Security Audit: [Agent Name/Description]

### Permission Summary
| Category | Access Level | Justified? |
|----------|-------------|-----------|
| File System | Read/Write to /path | Yes/No — reason |
| Network | External API access | Yes/No — reason |
| Shell | Sandboxed/Unsandboxed | Yes/No — reason |
| Credentials | [list] | Yes/No — reason |

### Risk Findings
[Use standard finding template for each issue found]

### Injection Surface Map
[Table of input paths with risk ratings]

### Recommendations
[Prioritized list: reduce permissions, add confirmations, sandbox, etc.]
```

## OWASP References

- **LLM01**: Prompt Injection
- **LLM02**: Insecure Output Handling
- **LLM06**: Excessive Agency
- **LLM07**: System Prompt Leakage
- **LLM08**: Vector and Embedding Weaknesses (for RAG agents)
- **LLM09**: Misinformation
- OWASP AI Exchange: Agent Security Controls
- OWASP Cheat Sheet: AI Agent Security
