# Secure Agent Playbook

An open-source security playbook for AI agents. Structured, OWASP-grounded procedures that enable agents to perform security engineering tasks — from code review to AI agent security audits.

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

| Plugin | Skills Included |
|--------|----------------|
| `code-security-skills` | securability-engineering, securability-engineering-review, code-review-security, sca-audit, secrets-scan, api-security-review, web-security-review |
| `ai-security-skills` | agent-security-audit, llm-risk-assess, agentic-ai-risk-assess, mcp-server-review, prompt-injection-test |

**Step 3** — Use the skills by mentioning the task in conversation:

```
"Review this code for security issues"
"Scan my dependencies for CVEs"
"Audit this MCP server configuration"
"Test this chatbot for prompt injection"
```

Claude will automatically activate the relevant skill based on context.

**Local development** — To test from a local clone instead of GitHub:
```
/plugin install /path/to/agent-security-playbook
```

**Without Claude Code:**

Reference plays directly as procedures for any AI agent or manual use:
- Point your agent at a play: *"Follow the procedure in `plays/tier4-ai-security/agent-security-audit.md`"*
- Or use the plays as checklists for manual security reviews

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

Two-layer design:

- **`skills/`** — Self-contained `SKILL.md` files following the [Agent Skills spec](https://agentskills.io/specification). Installable as a Claude Code plugin via `.claude-plugin/marketplace.json`. Each skill summarizes a procedure and references its corresponding play.
- **`plays/`** — Full reference procedures with detailed checklists, tables, decision criteria, and examples. Skills reference these for comprehensive coverage.

Contributors edit plays. Skills are the thin invocation layer. This means the playbook works with any AI agent (just point it at a play), while Claude Code users get plugin-based installation.

## OWASP Foundation

All plays reference OWASP standards and datasets:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Web application risks
- [OWASP API Security Top 10](https://owasp.org/API-Security/) — API-specific risks
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org) — AI/LLM risks
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) — Security verification requirements
- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) — Testing methodology
- [OWASP SAMM](https://owaspsamm.org) — Security program maturity model
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org) — Developer security guidance

## Related Projects

| Project | Relationship |
|---------|-------------|
| [OWASP Agent Skills Project](https://github.com/eoftedal/owasp-agent-skills-project) | Proactive ASVS 5.0 guidance for AI coding agents — helps agents **write** secure code. We use their ASVS reference data in `data/asvs/`. Complementary: they guide code generation, we find vulnerabilities in existing code. |
| [Arcanum PI Taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) | Prompt injection attack classification by Jason Haddix. Our `prompt-injection-testing` play is built on this taxonomy. CC BY 4.0. |
| [OpenCRE](https://www.opencre.org) | Cross-standard requirement mappings (CWE, ASVS, WSTG, NIST 800-53). We use OpenCRE links in findings for multi-framework traceability. |

## Contributing

New plays should:
- Solve one well-defined security task
- Include clear trigger conditions (when should this play run?)
- Follow a structured procedure with checkpoints
- Produce findings using `templates/finding.md` format
- Reference OWASP standards where applicable
- Prefer existing tools (semgrep, trivy, osv-scanner, trufflehog) over reimplementing detection

## License

This project is open source. See LICENSE for details.
