# Contributing to agent-security-playbook

Thanks for your interest in contributing to the OWASP Secure Agent Playbook. This guide covers how to add new plays, skills, and reference data.

## Ways to Contribute

- **New plays** — Add security procedures for uncovered vulnerability classes or standards
- **New skills** — Create the invocation layer for existing or new plays
- **New agents** — Add autonomous specialists that orchestrate skills for focused assessments
- **Reference data** — Add or update OWASP datasets in `data/`
- **Improvements** — Enhance existing plays with better checklists, examples, or tool coverage
- **Bug reports** — File issues for inaccurate findings, broken references, or missing coverage

## Adding a New Play

Plays live in `plays/` organized by tier:

| Tier | Focus |
|------|-------|
| `tier1-code-analysis/` | Code review, dependency audit, secrets, API security |
| `tier2-design-review/` | Threat modeling, ASVS verification, infrastructure hardening |
| `tier3-testing/` | WSTG checklist, DAST, attack surface mapping |
| `tier4-ai-security/` | Agent security, LLM risks, prompt injection, MCP review |
| `tier5-governance/` | SAMM maturity, compliance mapping, reporting |

A good play should:

1. **Solve one well-defined security task** — "Scan dependencies for CVEs" not "do a full security audit"
2. **Include trigger conditions** — When should this play run? What inputs does it need?
3. **Follow a structured procedure** — Numbered steps with clear decision criteria
4. **Produce findings using the standard format** — See `templates/finding.md`
5. **Reference OWASP standards** — Map findings to CWE, ASVS, WSTG, or relevant Top 10
6. **Prefer existing tools** — Use semgrep, trivy, osv-scanner, trufflehog, etc. over reimplementing detection logic

## Adding a New Skill

Skills are the invocation layer that wraps plays for Claude Code plugin installation.

1. Create a new directory under `skills/` with your skill name
2. Add a `SKILL.md` file following the template in `template/SKILL.md`
3. Reference the corresponding play in your skill
4. Add the skill path to the appropriate plugin group in `.claude-plugin/marketplace.json`

**Plugin groups:**
- `code-security-skills` — Code, infrastructure, and dependency analysis
- `ai-security-skills` — AI/agent-specific security assessment

## Adding a New Agent

Agents are autonomous specialists that invoke one or more skills to perform focused security assessments.

1. Create a new `.md` file in `agents/` named after your agent (e.g., `agents/my-agent.md`)
2. Use YAML frontmatter with required fields: `name`, `description`, `tools`, `model`, `skills`
3. Optionally add `isolation: worktree` so the agent works on an isolated copy of the repo (recommended for agents that may run in parallel as part of a team)
4. The system prompt should describe the agent's approach, which skills to invoke and when, and the expected output format
5. Add the agent path to the `agents` array in `.claude-plugin/marketplace.json`

**Note:** Plugin agents cannot use `hooks`, `mcpServers`, or `permissionMode` fields for security reasons.

See existing agents in `agents/` for examples.

## Finding Format

All findings must use the structure defined in `templates/finding.md`:

```markdown
### [SEVERITY] Title

- **CWE**: CWE-XXX
- **CVE**: CVE-YYYY-NNNNN (if applicable)
- **OpenCRE**: [CRE-ID](https://www.opencre.org/cre/CRE-ID) — requirement name
- **OWASP Ref**: Top 10 A01, ASVS V#.#.#, LLM01, etc.
- **Location**: file_path:line_number
- **Impact**: What an attacker can achieve
- **Evidence**: Code snippet, command output, or proof-of-concept
- **Remediation**: Specific fix with code example
- **Confidence**: HIGH | MEDIUM | LOW
```

Resolve OpenCRE links via the API: `GET https://www.opencre.org/rest/v1/standard/CWE/sectionid/{cwe-number}`

Common mappings are pre-populated in `data/opencre/README.md`.

## Pull Request Guidelines

- One play or skill per PR (unless tightly coupled)
- Include a clear description of what the play/skill covers and why it's needed
- If adding a skill, ensure it's added to `marketplace.json`
- Test your play against a real or deliberately-vulnerable target where possible

## License

By contributing, you agree that your contributions will be licensed under the same [CC-BY-4.0](LICENSE.md) license as the rest of the project.
