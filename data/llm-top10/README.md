# OWASP Top 10 for LLM Applications — Reference Data

10 structured risk files sourced from the [OWASP Top 10 for Large Language Model Applications v2.0](https://genai.owasp.org) (2025 edition).

## Source & License

Content is derived from the [OWASP www-project-top-10-for-large-language-model-applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications) repository. OWASP materials are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "LLM01 Prompt Injection"
owasp_llm_id: "LLM01"
when_to_use:                          # Task-matching triggers
  - reviewing LLM applications that accept user input
  - assessing chatbots for injection risks
threats:                              # Relevant threat categories
  - direct prompt injection via user input
  - indirect prompt injection via external content
summary: "Brief description of the risk."
---
```

Followed by the risk description, common examples, prevention/mitigation table, attack scenarios, related frameworks, and references.

## Usage in Skills

### LLM Risk Assessment (`/llm-risk-assess`)

When assessing an LLM application, reference specific risk IDs:

```markdown
- **OWASP Ref**: LLM01 Prompt Injection
```

### Task-Based Lookup

Use the `when_to_use` frontmatter to match tasks to relevant LLM risks. For example, if reviewing code that renders LLM output in a web page, check:
- `LLM05` — Improper Output Handling
- `LLM01` — Prompt Injection (indirect injection via output)

### Agent Security Audit

Cross-reference with the agent security audit skill:
- `LLM06` — Excessive Agency (tool overpermissioning)
- `LLM01` — Prompt Injection (via tool outputs and MCP resources)
- `LLM07` — System Prompt Leakage (CLAUDE.md and system prompt review)

## Risk Index

| ID | Risk | Key Concern |
|----|------|-------------|
| [LLM01](LLM01.md) | Prompt Injection | Direct and indirect manipulation of LLM behavior |
| [LLM02](LLM02.md) | Sensitive Information Disclosure | PII, credentials, or proprietary data in outputs |
| [LLM03](LLM03.md) | Supply Chain | Poisoned models, vulnerable dependencies, LoRA adapters |
| [LLM04](LLM04.md) | Data and Model Poisoning | Training data manipulation, backdoors, sleeper agents |
| [LLM05](LLM05.md) | Improper Output Handling | XSS, SQLi, RCE via unsanitized LLM output |
| [LLM06](LLM06.md) | Excessive Agency | Overpermissioned tools, missing human-in-the-loop |
| [LLM07](LLM07.md) | System Prompt Leakage | Credentials or business logic in extractable prompts |
| [LLM08](LLM08.md) | Vector and Embedding Weaknesses | RAG poisoning, tenant isolation, embedding inversion |
| [LLM09](LLM09.md) | Misinformation | Hallucination, fabricated references, package squatting |
| [LLM10](LLM10.md) | Unbounded Consumption | DoS, denial of wallet, model extraction |

## Updating

To refresh from upstream:

```bash
# Check for updates to the OWASP LLM Top 10 source
cd /tmp && git clone --depth 1 https://github.com/OWASP/www-project-top-10-for-large-language-model-applications.git
ls /tmp/www-project-top-10-for-large-language-model-applications/2_0_vulns/
```

Then update individual files as needed, preserving the YAML frontmatter format.
