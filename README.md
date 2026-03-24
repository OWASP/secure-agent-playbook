# Secure Agent Playbook

An open-source security playbook for AI agents. Structured, OWASP-grounded procedures that enable agents to perform security engineering tasks — from code review to AI agent security audits.

## Table of Contents

- [Why Use This?](#why-use-this)
- [What This Is](#what-this-is)
- [Quick Start](#quick-start)
- [Skills Catalog](#skills-catalog)
- [Agents](#agents)
- [Example Output](#example-output)
- [Plays](#plays)
- [Architecture](#architecture)
- [OWASP Foundation](#owasp-foundation)
- [Related Projects](#related-projects)
- [Contributing](#contributing)

## Why Use This?

Without a playbook, asking an AI agent to "review my code for security" gives you a surface-level checklist. With these plays, the agent follows a structured OWASP-grounded procedure — systematically testing every vulnerability class, producing findings with CWE mappings, OpenCRE cross-references, evidence snippets, and specific remediation code.

- **Consistent methodology** — Every assessment follows a documented procedure, not ad-hoc prompting. Results are reproducible across runs and reviewers.
- **Structured, actionable output** — Findings include severity, CWE, evidence, and remediation steps with code examples. No vague warnings.
- **Cross-standard traceability** — Findings link to CWE, ASVS, WSTG, and NIST 800-53 via [OpenCRE](https://www.opencre.org) for compliance mapping.
- **15 security skills** — From dependency CVE scanning to prompt injection testing to multi-agent threat modeling. Install as a Claude Code plugin or use standalone.
- **Works beyond Claude Code** — Skills are Claude Code plugins; plays are standalone procedures any AI agent can follow.

## What This Is

This is not a framework or a library. There is no code to import.

Each **play** is a step-by-step security procedure with checklists, decision criteria, and output templates. An AI agent follows the procedure to produce consistent, evidence-based findings. Think of it like a SOC analyst's playbook — but written for AI agents to execute.

## Quick Start

**With Claude Code (recommended):**

**Step 1** — Register the plugin marketplace:
```
/plugin marketplace add OWASP/secure-agent-playbook
```

**Step 2** — Install a skill set:
```
/plugin install code-security-skills@agent-security-playbook
/plugin install ai-security-skills@agent-security-playbook
```

**Step 3** — Use the skills by mentioning the task in conversation:

```
"Review this code for security issues"
"Scan my dependencies for CVEs"
"Audit this MCP server configuration"
"Test this chatbot for prompt injection"
```

Claude will automatically activate the relevant skill based on context. See [Skills Catalog](#skills-catalog) for all available skills and [Example Output](#example-output) for what the results look like.

**Local development** — To test from a local clone instead of GitHub:
```
/plugin install /path/to/agent-security-playbook
```

**Without Claude Code:**

Reference plays directly as procedures for any AI agent or manual use:
- Point your agent at a play: *"Follow the procedure in `plays/tier4-ai-security/agent-security-audit.md`"*
- Or use the plays as checklists for manual security reviews

## Skills Catalog

### Code & Infrastructure Security (`code-security-skills`)

| Skill | What It Does | Say This | OWASP Ref |
|-------|-------------|----------|-----------|
| `code-review-security` | Security code review mapped to Top 10 + ASVS | "Review this code for security issues" | Top 10, ASVS |
| `sca-audit` | Dependency CVE scanning with reachability analysis | "Scan my dependencies for CVEs" | A06:2021 |
| `secrets-scan` | Detect hardcoded credentials and API keys | "Scan for hardcoded secrets" | CWE-798 |
| `api-security-review` | API review against OWASP API Top 10 (2023) | "Review this API for security" | API Top 10 |
| `web-security-review` | Web app review against OWASP Top 10 (2021) | "Review this web app for OWASP Top 10" | Top 10 |
| `iac-security-review` | IaC security (Terraform, K8s, CloudFormation) | "Review this Terraform for security" | CIS Benchmarks |
| `securability-engineering` | Generate inherently securable code (FIASSE) | "Generate secure code for..." | FIASSE |
| `securability-engineering-review` | Assess code securability (0-10 SSEM scoring) | "Assess the securability of this code" | FIASSE/SSEM |
| `security-guidance` | Auto-triggered ASVS guidance for security-sensitive code | *(auto-triggered)* | ASVS 5.0 |

### AI & Agent Security (`ai-security-skills`)

| Skill | What It Does | Say This | OWASP Ref |
|-------|-------------|----------|-----------|
| `agent-security-audit` | Audit agent permissions, injection surfaces, data exfil paths | "Audit this agent's security" | LLM Top 10 |
| `llm-risk-assess` | LLM app assessment against LLM Top 10 2025 | "Assess LLM risks for this app" | LLM Top 10 |
| `agentic-ai-risk-assess` | Agentic app assessment against Top 10 Agentic 2026 | "Assess agentic AI risks" | Agentic Top 10 |
| `mcp-server-review` | MCP server security review | "Review this MCP server" | LLM Top 10 |
| `prompt-injection-test` | Prompt injection testing (Arcanum PI Taxonomy) | "Test for prompt injection" | LLM01 |
| `multi-agentic-threat-model` | CSA MAESTRO 7-layer threat modeling | "Model threats for this multi-agent system" | CSA MAESTRO |

## Agents

Agents are autonomous security specialists that invoke skills and produce structured reports. Each agent has a focused system prompt, scoped tool access, and preloaded skills. Use them individually or as a coordinated team.

| Agent | Focus | Skills Invoked |
|-------|-------|---------------|
| `code-security-reviewer` | Code vulnerabilities, secrets, web security | code-review-security, secrets-scan, web-security-review |
| `dependency-auditor` | Supply chain and dependency CVE risks | sca-audit |
| `api-security-reviewer` | API security against OWASP API Top 10 | api-security-review |
| `ai-security-assessor` | Agent configs, MCP servers, LLM app risks | agent-security-audit, mcp-server-review, llm-risk-assess, prompt-injection-test |
| `security-team-lead` | Coordinates specialists, consolidates report | securability-engineering-review |

**Standalone usage** — invoke any agent directly:
```
"Use code-security-reviewer to review src/"
"Use dependency-auditor to scan this project"
```

**Team assessment** — with agent teams enabled, the team lead dispatches specialists in parallel and consolidates findings into a single report:
```
"Run a full security assessment of this project"
```

The team lead scopes the target, dispatches relevant specialists (skipping those whose focus area isn't present), deduplicates findings, identifies cross-domain risk chains, and produces a unified report using `templates/report.md`.

> Agent teams requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. See [Claude Code docs](https://code.claude.com/docs/en/agent-teams) for setup. Individual agents work without this flag.

## Example Output

Running `"Review src/auth/ for security issues"` on a Node.js/Express codebase produces findings like this:

```
Security Code Review — src/auth/
Scope: Node.js/Express, server-side, processes user credentials
Findings: CRITICAL 1 | HIGH 2 | MEDIUM 1 | LOW 0
```

### [CRITICAL] SQL Injection in User Lookup

- **CWE**: [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- **OpenCRE**: [CRE-764-507](https://www.opencre.org/cre/764-507) — Injection Prevention
- **OWASP Ref**: A03:2021 Injection
- **Location**: `src/auth/login.js:42`
- **Impact**: Attacker can extract the entire users table, bypass authentication, or execute arbitrary SQL via crafted `id` parameter
- **Evidence**:
  ```js
  // src/auth/login.js:42
  const user = await db.query("SELECT * FROM users WHERE id=" + req.params.id);
  ```
- **Remediation**: Use parameterized queries:
  ```js
  const user = await db.query("SELECT * FROM users WHERE id = $1", [req.params.id]);
  ```
- **Confidence**: HIGH

> Every skill produces structured findings with severity, CWE, evidence, and remediation code.
> See [`examples/`](examples/) for complete sample assessment reports.

## Plays

### Tier 4: AI/Agent Security

The differentiator — security procedures purpose-built for the AI agent era.

| Play | What It Does |
|------|-------------|
| [agent-security-audit](plays/tier4-ai-security/agent-security-audit.md) | Audit agent permissions, prompt injection surfaces, data exfiltration paths, guardrails |
| [llm-risk-assess](plays/tier4-ai-security/llm-risk-assess.md) | Assess LLM applications against OWASP Top 10 for LLM Applications |
| [mcp-server-review](plays/tier4-ai-security/mcp-server-review.md) | Review MCP server implementations for overpermissioning, injection, data exposure |
| [prompt-injection-testing](plays/tier4-ai-security/prompt-injection-testing.md) | Test LLM apps against 18 attack techniques, 20 evasions, 13 intents |


### Tier 1: Code & Dependency Analysis

Immediate, practical value for any codebase.

| Play | What It Does |
|------|-------------|
| [sca-audit](plays/tier1-code-analysis/sca-audit.md) | Scan dependencies for known CVEs with reachability analysis |
| [code-review-security](plays/tier1-code-analysis/code-review-security.md) | Systematic security code review mapped to OWASP Top 10 and ASVS |
| [secrets-scan](plays/tier1-code-analysis/secrets-scan.md) | Detect hardcoded credentials, API keys, and tokens |
| [api-security-review](plays/tier1-code-analysis/api-security-review.md) | Review APIs against OWASP API Security Top 10 |
| [securability-engineering-review](plays/tier1-code-analysis/securability-engineering-review.md) | Assess code against FIASSE/SSEM securable attributes: Maintainability, Trustworthiness, Reliability, and Transparency |

### Planned

- **Tier 2**: Threat modeling, ASVS verification, infrastructure hardening
- **Tier 3**: WSTG testing checklist, DAST orchestration, attack surface mapping
- **Tier 5**: SAMM maturity assessment, compliance mapping, aggregate reporting

## Architecture

Three-layer design:

- **`agents/`** — Autonomous security specialists with focused system prompts. Each agent invokes one or more skills, operates in an isolated context, and produces structured reports. Can work solo or as a coordinated team.
- **`skills/`** — Self-contained `SKILL.md` files following the [Agent Skills spec](https://agentskills.io/specification). Installable as a Claude Code plugin via `.claude-plugin/marketplace.json`. Each skill summarizes a procedure and references its corresponding play.
- **`plays/`** — Full reference procedures with detailed checklists, tables, decision criteria, and examples. Skills reference these for comprehensive coverage.

Agents orchestrate, skills execute, plays provide the full procedure. Contributors edit plays. This means the playbook works with any AI agent (just point it at a play), while Claude Code users get plugin-based installation with agents and skills.

## OWASP Foundation

All plays reference OWASP standards and datasets:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Web application risks
- [OWASP API Security Top 10](https://owasp.org/API-Security/) — API-specific risks
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org) — AI/LLM risks
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) — Security verification requirements
- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) — Testing methodology
- [OWASP SAMM](https://owaspsamm.org) — Security program maturity model
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org) — Developer security guidance
- [OWASP FIASSE](https://owasp.org/www-project-fiasse/) — securable attributes and secure coding principles

## Related Projects

| Project | Relationship |
|---------|-------------|
| [OWASP Agent Skills Project](https://github.com/eoftedal/owasp-agent-skills-project) | Proactive ASVS 5.0 guidance for AI coding agents — helps agents **write** secure code. We use their ASVS reference data in `data/asvs/`. Complementary: they guide code generation, we find vulnerabilities in existing code. |
| [Arcanum PI Taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) | Prompt injection attack classification by Jason Haddix. Our `prompt-injection-testing` play is built on this taxonomy. CC BY 4.0. |
| [OpenCRE](https://www.opencre.org) | Cross-standard requirement mappings (CWE, ASVS, WSTG, NIST 800-53). We use OpenCRE links in findings for multi-framework traceability. |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

New plays should:
- Solve one well-defined security task
- Include clear trigger conditions (when should this play run?)
- Follow a structured procedure with checkpoints
- Produce findings using `templates/finding.md` format
- Reference OWASP standards where applicable
- Prefer existing tools (semgrep, trivy, osv-scanner, trufflehog) over reimplementing detection

## License

This project is open source. See LICENSE for details.
