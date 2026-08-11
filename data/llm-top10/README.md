# OWASP GenAI LLM Top 10 2026 — Reference Data

10 structured risk files sourced from the [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/), published 4 August 2026.

## Source & License

Content is derived from [`GenAI-Security-Project/GenAI-LLM-Top10`](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) (`2026/final`). OWASP materials are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The former repository, [`OWASP/www-project-top-10-for-large-language-model-applications`](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications), is now a legacy entry point and historical archive; active development has moved to the repo above.

## Fidelity and Provenance

**These files are condensed summaries, not OWASP's verbatim text.** Each risk entry restates
its upstream chapter in compressed form so an agent can load all ten cheaply. Facts, figures,
scope boundaries, and cross-references to sibling risks are preserved; OWASP's wording is not.
Roughly 7% of sentences are verbatim.

Authored by this repo rather than derived from upstream prose:

- the YAML frontmatter (`when_to_use`, `threats`, `summary`)
- the **Potential Impacts** section (upstream carries an equivalent list only for LLM01)
- the **AISVS Controls** table and `aisvs_mappings` (see the cross-reference section below)
- the tabular restructuring of **Prevention and Mitigation**

When a finding needs to quote the standard, quote the [upstream
source](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/tree/main/2026/final), not
these files. Cite risks by ID and year (`LLM01:2026`) and let the reader resolve the wording.

By contrast, the sibling [`data/aisvs/`](../aisvs/) dataset **is** verbatim: each file carries
its upstream section heading, intro paragraph, and requirements table byte-for-byte, with only
frontmatter added. Requirement text there can be quoted directly.

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "LLM01 Prompt Injection"
owasp_llm_id: "LLM01"
owasp_llm_version: "2026"
when_to_use:                          # Task-matching triggers
  - reviewing LLM applications that accept user input
  - assessing chatbots for injection risks
threats:                              # Relevant threat categories
  - direct prompt injection via user input
  - indirect prompt injection via external content
summary: "Brief description of the risk."
aisvs_mappings:                       # OWASP AISVS v1.0 controls
  - section: "C2.1"
    title: "Prompt Injection Defenses"
    requirements: ["2.1.1", "2.1.2", "2.1.3"]
---
```

Followed by the risk description, potential impacts, common examples of risk, prevention/mitigation table, example attack scenarios, AISVS controls table, related frameworks, and references.

## Risk Index

| ID | Risk | Key Concern |
|----|------|-------------|
| [LLM01](LLM01.md) | Prompt Injection | Direct, indirect, multimodal, and cross-session manipulation of LLM behavior |
| [LLM02](LLM02.md) | Sensitive Information Disclosure | PII, credentials, traces, embeddings, and side-channel leakage |
| [LLM03](LLM03.md) | Excessive Agency | Excessive functionality, permissions, and autonomy in tool-calling agents |
| [LLM04](LLM04.md) | Supply Chain | Tampered models, weak provenance, adapters, conversion and build pipelines |
| [LLM05](LLM05.md) | Data and Model Poisoning | Training, fine-tuning, embedding, and memory poisoning; sleeper agents |
| [LLM06](LLM06.md) | Unbounded Consumption | DoS, denial of wallet, reasoning-loop exhaustion, model extraction |
| [LLM07](LLM07.md) | Misinformation | Hallucination, fabricated evidence, incorrect state driving agent action |
| [LLM08](LLM08.md) | Hidden Context Exposure | System prompts, tool schemas, and control logic extracted from context |
| [LLM09](LLM09.md) | Vector and Embedding Weaknesses | RAG poisoning, embedding inversion, cross-tenant leakage, cache poisoning |
| [LLM10](LLM10.md) | Improper Output Handling | XSS, SQLi, RCE, ANSI injection, renderer-triggered exfiltration |

## Changes from the 2025 Edition

Every risk except LLM01 and LLM02 was renumbered. Update any citation of a 2025 ID:

| 2025 ID | 2026 ID | Note |
|---------|---------|------|
| LLM01 Prompt Injection | **LLM01** | held first place |
| LLM02 Sensitive Information Disclosure | **LLM02** | held second place |
| LLM03 Supply Chain | **LLM04** | |
| LLM04 Data and Model Poisoning | **LLM05** | |
| LLM05 Improper Output Handling | **LLM10** | largest fall, fifth to tenth |
| LLM06 Excessive Agency | **LLM03** | largest rise; agentic deployments are where damage is landing |
| LLM07 System Prompt Leakage | **LLM08 Hidden Context Exposure** | renamed and broadened beyond the system prompt |
| LLM08 Vector and Embedding Weaknesses | **LLM09** | |
| LLM09 Misinformation | **LLM07** | |
| LLM10 Unbounded Consumption | **LLM06** | rose four places |

## Usage in Skills

### LLM Risk Assessment (`/llm-risk-assess`)

When assessing an LLM application, reference specific risk IDs:

```markdown
- **OWASP Ref**: LLM01:2026 Prompt Injection
```

Include the year — a bare `LLM06` is ambiguous between the 2025 and 2026 lists.

### Task-Based Lookup

Use the `when_to_use` frontmatter to match tasks to relevant risks. For example, if reviewing code that renders LLM output in a web page, check:
- `LLM10` — Improper Output Handling
- `LLM01` — Prompt Injection (indirect injection reaching the renderer)

### Agent Security Audit

Cross-reference with the agent security audit skill:
- `LLM03` — Excessive Agency (tool overpermissioning)
- `LLM01` — Prompt Injection (via tool outputs and MCP resources)
- `LLM08` — Hidden Context Exposure (CLAUDE.md and system prompt review)

## OWASP AISVS Cross-Reference

Each risk file includes `aisvs_mappings` in the YAML frontmatter linking to specific [OWASP AISVS](https://github.com/OWASP/AISVS) **v1.0** requirements, plus an `AISVS Controls` table in the body.

The 2026 release ships an official [AISVS mapping appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) that maps at **chapter** granularity. The mappings in these files cover every chapter that appendix marks as a primary defense, refined down to individual sections and requirements, and occasionally extend to a supporting chapter the appendix leaves unmarked. Per the appendix's own caveat, mappings are directional guidance rather than a compliance crosswalk: a marked chapter contributes to defending a risk but rarely closes it alone.

### AISVS v1.0 Coverage by LLM Risk

Legend: **●** primary defense · **○** supporting defense (from the official appendix).

| Risk | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **LLM01** Prompt Injection | | ● | | | | | ○ | | ● | ● | ● | ● |
| **LLM02** Sensitive Information Disclosure | ○ | | | | ● | | ● | ● | | | ● | ○ |
| **LLM03** Excessive Agency | | | | | ● | | | | ● | ● | | ○ |
| **LLM04** Supply Chain | ○ | | ● | ● | | ● | | | | ○ | | |
| **LLM05** Data & Model Poisoning | ● | | ● | | | ○ | | ● | | | ● | ○ |
| **LLM06** Unbounded Consumption | | | | | ○ | | ○ | | ● | | ● | ● |
| **LLM07** Misinformation | ○ | | | | | | ● | ○ | | | ○ | ● |
| **LLM08** Hidden Context Exposure | | ○ | | | ○ | | ● | | ● | | ● | ○ |
| **LLM09** Vector & Embedding Weaknesses | ○ | | | | ● | | ○ | ● | | | | ○ |
| **LLM10** Improper Output Handling | | | | | | | ● | | ● | ○ | | |

### AISVS v1.0 Chapter Index

| Chapter | Title | Mapped From |
|---------|-------|-------------|
| C1 | Training Data Integrity & Traceability | LLM02, LLM04, LLM05, LLM07, LLM09 |
| C2 | Input Validation | LLM01, LLM06, LLM08 |
| C3 | Model Lifecycle Management & Change Control | LLM04, LLM05 |
| C4 | Infrastructure, Configuration & Deployment Security | LLM04 |
| C5 | Access Control & Identity for AI Components & Users | LLM02, LLM03, LLM06, LLM08, LLM09 |
| C6 | Supply Chain Security for Models | LLM04, LLM05 |
| C7 | Model Behavior, Output Control & Safety Assurance | LLM01, LLM02, LLM06, LLM07, LLM08, LLM09, LLM10 |
| C8 | Memory, Embeddings & Vector Database Security | LLM01, LLM02, LLM05, LLM07, LLM09 |
| C9 | Orchestration & Agentic Security | LLM01, LLM02, LLM03, LLM06, LLM07, LLM08, LLM10 |
| C10 | Model Context Protocol (MCP) Security | LLM01, LLM03, LLM04, LLM06, LLM08, LLM10 |
| C11 | Adversarial Robustness | LLM01, LLM02, LLM05, LLM06, LLM07, LLM08, LLM09 |
| C12 | Monitoring, Logging & Anomaly Detection | all ten (cross-cutting) |

The AISVS requirement files themselves live at [`data/aisvs/`](../aisvs/) (research copy) and `plugins/code-security-skills/data/aisvs/` (bundled with the plugin).

## Updating

To refresh from upstream:

```bash
git clone --depth 1 https://github.com/GenAI-Security-Project/GenAI-LLM-Top10.git
ls GenAI-LLM-Top10/2026/final/
```

Then update individual files as needed, preserving the YAML frontmatter format. If the LLM Top 10 or AISVS advances a version, re-check the official AISVS mapping appendix — it is versioned to a specific pairing (currently Top 10 2026 → AISVS 1.0).
