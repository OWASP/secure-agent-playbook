# Contributing to agent-security-playbook

Thanks for your interest in contributing to the OWASP Secure Agent Playbook. This guide covers how to add new plays, skills, and reference data.

## Ways to Contribute

- **New plays** — Add security procedures for uncovered vulnerability classes or standards
- **New skills** — Create the invocation layer for existing or new plays
- **New agents** — Add autonomous specialists that orchestrate skills for focused assessments
- **Reference data** — Add or update OWASP datasets in `plugins/<group>/data/` (bundled with a plugin) or `data/` (research datasets no skill uses yet)
- **Improvements** — Enhance existing plays with better checklists, examples, or tool coverage
- **Bug reports** — File issues for inaccurate findings, broken references, or missing coverage

## Adding a New Play

Plays live in the `plays/` folder of the plugin whose skills use them, so they ship with the marketplace install:

| Plugin | Plays folder | Focus |
|--------|--------------|-------|
| `code-security-skills` | `plugins/code-security-skills/plays/` | Code review, dependency audit, secrets, API, web, mobile, IaC, securability |
| `ai-security-skills` | `plugins/ai-security-skills/plays/` | Agent security, LLM risks, prompt injection, MCP review, AISVS verification, threat modeling |

Name the play after its task (e.g. `mcp-server-review.md`). Every template or data file a play or skill cites must live inside the same plugin folder, because files outside it are not installed.

A good play should:

1. **Solve one well-defined security task** — "Scan dependencies for CVEs" not "do a full security audit"
2. **Include trigger conditions** — When should this play run? What inputs does it need?
3. **Follow a structured procedure** — Numbered steps with clear decision criteria
4. **Produce findings using the standard format** — See `plugins/<group>/templates/finding.md`
5. **Reference OWASP standards** — Map findings to CWE, ASVS, WSTG, or relevant Top 10
6. **Prefer existing tools** — Use semgrep, trivy, osv-scanner, trufflehog, etc. over reimplementing detection logic

## Adding a New Skill

Skills are the invocation layer that wraps plays for Claude Code plugin installation.

1. Decide which plugin group your skill belongs to (see groups below)
2. Create a new directory under `plugins/<group>/skills/` with your skill name
3. Add a `SKILL.md` file following the template in `template/SKILL.md`. Its frontmatter needs a `name`, a `description` that says when to use the skill, and `license: CC-BY-4.0`
4. Reference the corresponding play in your skill (`plays/<play>.md`)
5. Don't add an `allowed-tools` line that pre-approves `Bash`, `WebFetch`, or `Agent`. These skills read untrusted code and content, and pre-approval removes the permission prompt that would catch an injected command

Skills are auto-discovered from `plugins/<group>/skills/` — no manifest registration step needed.

**Plugin groups:**
- `code-security-skills` — Code, infrastructure, and dependency analysis
- `ai-security-skills` — AI/agent-specific security assessment

## Adding a New Agent

Agents are autonomous specialists that invoke one or more skills to perform focused security assessments.

1. Decide which plugin the agent belongs to based on the skills it invokes
2. Create a new `.md` file in `plugins/<group>/agents/` named after your agent (e.g., `plugins/code-security-skills/agents/my-agent.md`)
3. Use YAML frontmatter with required fields: `name`, `description`, `tools`, `model`, `skills`
4. Optionally add `isolation: worktree` so the agent works on an isolated copy of the repo (recommended for agents that may run in parallel as part of a team)
5. The system prompt should describe the agent's approach, which skills to invoke and when, and the expected output format

Agents are auto-discovered from `plugins/<group>/agents/` — no manifest registration step needed.

**Note:** Plugin agents cannot use `hooks`, `mcpServers`, or `permissionMode` fields for security reasons.

See existing agents in `plugins/code-security-skills/agents/` and `plugins/ai-security-skills/agents/` for examples.

## Finding Format

All findings must use the structure defined in `plugins/<group>/templates/finding.md`:

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
- If adding a skill, ensure it lives under the correct `plugins/<group>/skills/` directory, and update the README skills table and skill count
- Test your play against a real or deliberately-vulnerable target where possible

## License

By contributing, you agree that your contributions will be licensed under the same [CC-BY-4.0](LICENSE.md) license as the rest of the project.
