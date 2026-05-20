# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

**agent-security-playbook** is an open-source security playbook for AI agents. It provides structured, OWASP-grounded procedures ("plays") that enable agents to perform security engineering tasks — from code review to agent security audits.

This is not a framework or a library. There is no code to import. Each play is a step-by-step procedure with checklists, decision criteria, and output templates that an AI agent follows to produce consistent, evidence-based security findings.

The target audience is security contributors, AppSec engineers, and developers who want AI agents to perform security analysis using established methodology.

## Role

When working in this repository, act as a **security researcher and engineer**. Your focus areas:

- **Threat modeling** — Identify attack surfaces, trust boundaries, and threat actors for systems and architectures
- **Vulnerability analysis** — Analyze code, configurations, and infrastructure for security weaknesses (OWASP Top 10, CWE, SANS Top 25)
- **Agent security** — Evaluate risks specific to AI agents: prompt injection, tool misuse, excessive permissions, data exfiltration, insecure tool chains
- **Security automation** — Build skills, scripts, and workflows that automate security tasks (SAST, DAST, dependency auditing, secrets scanning)
- **Incident response** — Help triage, investigate, and document security incidents
- **Compliance and hardening** — Review configurations against security benchmarks (CIS, NIST, SOC2 controls)

## Principles

- **Defensive posture** — All tools and skills are built for defense, detection, and authorized testing only. Never produce tools intended for unauthorized access or malicious use.
- **Assume breach** — Design with the assumption that any component can be compromised. Favor least-privilege, zero-trust patterns.
- **Evidence-based** — Cite CVEs, CWEs, OWASP references, and OpenCRE links for cross-standard traceability. Avoid vague warnings.
- **Actionable output** — Every finding should include severity, impact, and a concrete remediation step.
- **Context matters** — Severity depends on deployment context. A reflected XSS on an internal admin tool differs from one on a public-facing login page. Always ask about context when it's ambiguous.

## Playbook Development Guidelines

Each play in this repo is a self-contained security procedure designed to be invoked by Claude Code users or composed into larger workflows. When building new plays:

- Each play should solve one well-defined security task (e.g., "scan dependencies for known CVEs", "review IAM policy for over-permissioning")
- Include clear trigger conditions — when should this play activate?
- Produce structured output (severity, finding, evidence, remediation) so results can be consumed programmatically
- Prefer using existing tools (semgrep, trivy, osv-scanner, nuclei, trufflehog) over reimplementing detection logic
- Test plays against known-vulnerable samples where possible

## Security Review Checklist (for code in this repo and for targets under review)

When reviewing code or configurations, systematically check:

1. **Authentication & Authorization** — Broken access controls, missing auth, privilege escalation
2. **Input validation** — Injection (SQL, command, LDAP, XSS, SSTI), deserialization, path traversal
3. **Secrets management** — Hardcoded credentials, leaked API keys, insecure storage
4. **Dependencies** — Known CVEs in direct and transitive dependencies
5. **Cryptography** — Weak algorithms, improper key management, missing encryption at rest/in transit
6. **Logging & Monitoring** — Missing audit trails, sensitive data in logs
7. **Agent-specific risks** — Prompt injection, tool-call injection, excessive autonomy, data leakage through tool outputs, insecure MCP server configurations

## Output Format for Findings

When reporting security findings, use this structure:

```
### [SEVERITY] Title
- **CWE**: CWE-XXX (if applicable)
- **CVE**: CVE-YYYY-NNNNN (if applicable)
- **OpenCRE**: [CRE-ID](https://www.opencre.org/cre/CRE-ID) — requirement name
- **OWASP Ref**: Top 10 A01, ASVS V#.#.#, LLM01, etc.
- **Location**: file_path:line_number
- **Impact**: What an attacker can achieve
- **Evidence**: Code snippet, command output, or proof-of-concept
- **Remediation**: Specific fix with code example
```

Use `data/opencre/README.md` for common CWE-to-CRE mappings, or query the OpenCRE API: `GET https://www.opencre.org/rest/v1/standard/CWE/sectionid/{number}`

Severity levels: CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL

## Repository Structure

Each plugin source folder under `plugins/` is **fully self-contained** — when users install via `/plugin marketplace add OWASP/secure-agent-playbook`, only files inside the plugin's source directory are bundled. Plays, templates, and the FIASSE/ASVS reference data each plugin needs are co-located inside the plugin so SKILL.md references resolve at runtime.

```
agent-security-playbook/
├── CLAUDE.md                     # This file — agent persona & guidelines
├── .claude-plugin/               # Plugin configs
│   ├── marketplace.json          # Marketplace listing both plugins (for /plugin marketplace add)
│   └── plugin.json               # Legacy single-plugin stub (backward compat)
├── plugins/                      # Claude Code plugin installation entry points
│   ├── code-security-skills/     # Code & infra security skills plugin (self-contained)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/               # 5 code-security agents
│   │   │   ├── code-security-reviewer.md
│   │   │   ├── dependency-auditor.md
│   │   │   ├── api-security-reviewer.md
│   │   │   ├── mobile-security-reviewer.md
│   │   │   └── security-team-lead.md
│   │   ├── skills/               # 11 code security skills
│   │   │   ├── securability-engineering/
│   │   │   ├── securability-engineering-review/
│   │   │   ├── prd-securability-enhancement/
│   │   │   ├── code-review-security/
│   │   │   ├── sca-audit/
│   │   │   ├── secrets-scan/
│   │   │   ├── api-security-review/
│   │   │   ├── web-security-review/
│   │   │   ├── mobile-code-review/
│   │   │   ├── iac-security-review/
│   │   │   └── security-guidance/
│   │   ├── plays/                # Step-by-step runbooks for the skills above
│   │   ├── templates/            # finding.md, report.md (used by skills' output)
│   │   └── data/                 # FIASSE, ASVS, MASVS, MASTG, and secure-code prompt reference data
│   └── ai-security-skills/       # AI/agent security skills plugin (self-contained)
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── agents/               # 1 AI-security agent
│       │   └── ai-security-assessor.md
│       ├── skills/               # 6 AI/agent security skills
│       │   ├── agent-security-audit/
│       │   ├── agentic-ai-risk-assess/
│       │   ├── llm-risk-assess/
│       │   ├── mcp-server-review/
│       │   ├── prompt-injection-test/
│       │   └── multi-agentic-threat-model/
│       ├── plays/                # Step-by-step runbooks for the skills above
│       └── templates/            # finding.md, report.md (used by skills' output)
├── data/                         # Research / future-skill reference data (not bundled into plugins)
│   ├── aisvs/                    # AISVS sections
│   ├── llm-top10/                # Parsed LLM Top 10 data
│   └── opencre/                  # OpenCRE cross-standard mappings (CWE <-> ASVS <-> WSTG <-> NIST)
└── template/
    └── SKILL.md                  # Skill template for contributors
```

## Three-Layer Architecture

- **`plugins/*/agents/`** — Autonomous security specialists with focused system prompts, co-located inside each plugin (`plugins/code-security-skills/agents/` and `plugins/ai-security-skills/agents/`). Each agent invokes one or more skills, operates in an isolated context, and produces structured reports. Can work solo or as a coordinated team via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`.
- **`plugins/*/skills/`** — Self-contained `SKILL.md` files following the [Agent Skills spec](https://agentskills.io/specification). Co-located inside each plugin directory, installable via `/plugin marketplace add OWASP/secure-agent-playbook` then `/plugin install <name>@agent-security-playbook`. Each skill summarizes a procedure and references its corresponding play.
- **`plugins/*/plays/`** — Full reference procedures with detailed checklists, tables, and examples. Skills reference these for comprehensive coverage. **Live inside each plugin's source folder** so they are bundled with the marketplace install. Contributors edit plays; skills are the invocation layer; agents are the orchestration layer.

## Play Tiers (Priority Order)

| Tier | Focus | Status |
|------|-------|--------|
| **Tier 4** | AI/Agent Security — prompt injection, excessive agency, MCP risks | Built |
| **Tier 1** | Code Analysis — securability review, SCA, code review, secrets, API security | Built |
| **Tier 2** | Design Review — threat modeling, ASVS verification, infra hardening | Planned |
| **Tier 3** | Testing — WSTG checklist, DAST scanning, attack surface mapping | Planned |
| **Tier 5** | Governance — SAMM maturity, compliance mapping, reporting | Planned |

## OWASP Data Sources

Datasets that ship inside a plugin (bundled with the marketplace install) live under `plugins/<plugin>/data/`. Datasets used only for research, future skills, or out-of-band lookups live at the repo root under `data/`.

| Dataset | Source Repo | Format | Used By | Lives at |
|---------|-----------|--------|---------|----------|
| ASVS v5.0 | `eoftedal/owasp-agent-skills-project` — `references/ASVS/` | Markdown + YAML frontmatter | securability-engineering, prd-securability-enhancement | `plugins/code-security-skills/data/asvs/` |
| MASVS v2.1.0 | `OWASP/masvs` (tag `v2.1.0`, `controls/MASVS-*.md`) | MD → MD with frontmatter and enrichment preservation | mobile-code-review (24 control files + 8 group overviews) | `plugins/code-security-skills/data/masvs/` |
| MASTG | `OWASP/mastg` — `tests-beta/` (V2) with `tests/` (V1) fallback | Markdown + YAML frontmatter | mobile-code-review (per-test recipes) | `plugins/code-security-skills/data/mastg/` |
| FIASSE v1.0.4 | `OWASP/FIASSE` — `docs/securable_framework.md` (tag `v1.0.4`) | Markdown + YAML frontmatter | securability-engineering, securability-engineering-review, prd-securability-enhancement (61 section files) | `plugins/code-security-skills/data/fiasse/` |
| Secure-code prompts | (this repo) | Markdown | iac-security-review (terraform, kubernetes, cloudformation) | `plugins/code-security-skills/data/secure-code-prompts/` |
| LLM Top 10 v2.0 | `OWASP/www-project-top-10-for-large-language-model-applications` | Markdown | (research; not yet bundled) | `data/llm-top10/` |
| AISVS | `OWASP/aisvs` | Markdown | (research; not yet bundled) | `data/aisvs/` |
| OpenCRE | [opencre.org](https://www.opencre.org) — REST API | JSON | All skills (cross-standard linking, queried at runtime) | `data/opencre/` |
| CWE | [cwe.mitre.org](https://cwe.mitre.org) v4.19 | XML, JSON | All skills (weakness classification, queried at runtime) | external |
