---
title: "LLM01 Prompt Injection"
owasp_llm_id: "LLM01"
owasp_llm_version: "2026"
when_to_use:
  - reviewing LLM applications that accept user input
  - assessing chatbots or AI assistants for injection risks
  - evaluating RAG pipelines where external content reaches the model
  - reviewing agents that read issues, tickets, emails, or repositories under user credentials
  - auditing MCP servers and tool outputs that re-enter the context window
  - red-teaming AI applications for prompt manipulation
threats:
  - direct prompt injection via user input
  - indirect prompt injection via external content (web pages, documents, tool outputs)
  - trusted-surface injection where the user's own agent acts under elevated credentials
  - cross-session memory and RAG corpus poisoning
  - multimodal and steganographic injection via images or audio
  - invisible-character (tag-block, variation-selector, zero-width) injection and exfiltration
  - multilingual, encoded, or low-resource-language payload evasion
  - jailbreaking to bypass safety guidelines
summary: "Input to an LLM — direct, retrieved, tool-supplied, multimodal, or remembered — alters model behavior in ways the developer did not intend. LLMs draw no architectural line between instructions and data, so defense is architectural: bound what a compromised model can reach."
aisvs_mappings:
  - section: "C2.1"
    title: "Prompt Injection Defenses"
    requirements: ["2.1.1", "2.1.2", "2.1.3", "2.1.4", "2.1.5", "2.1.6", "2.1.7", "2.1.8"]
  - section: "C2.2"
    title: "Content & Policy Screening"
    requirements: ["2.2.1", "2.2.2", "2.2.3", "2.2.4"]
  - section: "C7.3"
    title: "Output Safety"
    requirements: ["7.3.3", "7.3.4"]
  - section: "C8.2"
    title: "Embedding Sanitization & Validation"
    requirements: ["8.2.3", "8.2.4"]
  - section: "C9.2"
    title: "High-Impact Action Approval and Irreversibility Controls"
    requirements: ["9.2.1", "9.2.2", "9.2.6", "9.2.7"]
  - section: "C9.3"
    title: "Component Isolation and Tool Authorization"
    requirements: ["9.3.5", "9.3.6", "9.3.7"]
  - section: "C10.4"
    title: "Schema, Message, and Input Validation"
    requirements: ["10.4.1", "10.4.2", "10.4.8"]
  - section: "C11.1"
    title: "Model Alignment, Safety, and Robustness Testing and Training"
    requirements: ["11.1.1", "11.1.2", "11.1.3"]
  - section: "C11.4"
    title: "Model Runtime Anomaly Detection"
    requirements: ["11.4.1", "11.4.2"]
  - section: "C12.2"
    title: "Detection and Alerting"
    requirements: ["12.2.1", "12.2.2", "12.2.3"]
---

# LLM01:2026 Prompt Injection

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM01:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

A prompt-injection vulnerability occurs when input to an LLM — direct user input, retrieved content, tool output, image, audio, video, intermediate reasoning, or persistent memory — alters the model's behavior in ways the application developer did not intend. LLMs make no architectural distinction between "instructions" and "data" (both are tokens on the same stream), so there is no clean equivalent to parameterized queries. Inputs need not be human-readable, need not arrive directly from a user, and need not be visible in the rendered interface.

Three deployment-time properties make this worse:

- **Context-window pooling** — system prompt, user input, retrieved documents, tool outputs, conversation history, and memory are one token stream with no enforced trust boundary.
- **Memory persistence** — an injection that writes to long-term memory, a RAG corpus, or a vector store taints every subsequent session that reads it.
- **Agentic execution** — when model output drives tool calls, the blast radius extends from the chat surface to whatever the agent's tools can reach, and tool outputs re-enter the context, enabling chained or self-replicating effects.

**Anatomy.** Characterize any injection along three axes before selecting mitigations: **delivery surface** (direct input, retrieved content, tool output, tool connection channel, persistent memory), **propagation behavior** (single-shot, multi-step kill-chain, cross-session, self-replicating), and **encoding** (plain text, base64/obfuscation, invisible Unicode, multimodal/steganographic, low-resource language).

**Delivery-surface trust profiles** determine practical defenses: *untrusted* (public web, unknown-sender email), *semi-trusted* (issue titles, package READMEs, third-party API responses), and *trusted* (the developer's own repos, databases, internal documents — where an attacker may have planted content via an unrelated upstream vector).

Scope boundaries: this entry concerns the **input boundary**. What the model leaks through outputs is [LLM02](LLM02.md); consequences of output reaching privileged actions are [LLM03](LLM03.md); sanitizing output before it reaches downstream components is [LLM10](LLM10.md).

## Potential Impacts

- Disclosure of sensitive information, system-prompt content, retrieved private documents, or infrastructure details
- Manipulation of output to produce biased, harmful, or attacker-chosen content that downstream systems act on
- Unauthorized invocation of permitted tools, escalating to arbitrary command execution where the agent has shell, file-system, or cloud-API access
- Data exfiltration via image-URL channels, hidden Unicode, or covert tool-logging side channels
- Persistent compromise of agent behavior across sessions through memory or RAG poisoning

## Common Examples of Risk

1. **Direct prompt-input override** — a user message overrides the system prompt's role and capability limits.
2. **Indirect injection through retrieved content** — attacker instructions ride in a RAG passage, web page, document, or email.
3. **Trusted-surface indirect injection** — text planted in a low-privilege but trusted channel (issue tracker, feedback form, support ticket) makes the user's LLM act under its own elevated credentials.
4. **Multimodal and steganographic injection** — sub-perceptual perturbations in images, audio, or video extracted by the encoder.
5. **Invisible-character injection and exfiltration** — tag-block, variation-selector, and zero-width Unicode carry instructions or exfiltrate bytes inside benign-looking text.
6. **Cross-session memory and RAG corpus poisoning** — one tainted entry reaches every future session that reads it.
7. **Fine-tuning interface as gradient oracle ("fun-tuning")** — an attacker reads per-example loss from a vendor's fine-tuning API to optimize a payload, bringing white-box-style optimization to closed-weight models.
8. **Multilingual, encoded, or low-resource-language payloads** — Base64, ROT13, emoji, and code-mixed inputs evade classifiers not trained on the scheme.

## Prevention and Mitigation

No reliable prevention mechanism exists today. Defense is **architectural rather than interceptive**: assume the instruction boundary will be bypassed and constrain what the model may do and what its outputs may reach. Controls that *reduce injection success* degrade against adaptive attackers; controls that *bound blast radius* survive.

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Constrain role and capabilities | Declarative allow/deny statements in the system prompt. Partial control only — an attacker who infers the prompt bypasses it. |
| 2 | Strict output schema, validated in trusted code | Structural validation before any downstream action. Catches format violations, not semantic manipulation. |
| 3 | Filter at every modality boundary | Modality-specific classifiers, OCR over images, transcription over audio, then text filters on extracted content. |
| 4 | Hold credentials and state-change capability in application code | Least privilege per operation; route privileged calls through a deterministic policy engine that re-validates intent and arguments at execution time. |
| 5 | Strip invisible Unicode at ingest and render | Tag-block (U+E0000–E007F), variation-selector (U+FE00–FE0F), zero-width (U+200B/C/D, U+2060). |
| 6 | Provenance-labeled channel for external content | Structurally separate data from instructions. Reduces non-adaptive attack success only; mimicable once the scheme is known. |
| 7 | Human confirmation for privileged/irreversible actions | Surface the exact rendered action, not a summary — invisible-character smuggling can make displayed and executed actions differ. |
| 8 | Budget agent capabilities (Rule of Two floor) | Treat simultaneous (A) untrusted input, (B) sensitive data, and (C) state change or external communication as high-risk. Any [A,B,C] agent needs per-action human approval. |
| 9 | Treat agent memory writes as privileged | Log the causing prompt, classify writes for instruction content, require approval before instruction-bearing memories persist. |
| 10 | Pin, sign, and verify MCP servers and tool packages | Audit tool descriptions for hidden instructions; monitor tool composition. Pinning does not stop a payload in the pinned version. |
| 11 | Test against adaptive attackers | Red-team with the full defense specification disclosed. Static-only attack-success claims are not evidence. |

**The lethal trifecta** (Willison, 2025) restates the structural diagnosis as a pre-deployment check: an agent that can simultaneously access private data, ingest untrusted content, and communicate externally has the conditions for high-impact exploitation. Removing any one leg removes them.

## Example Attack Scenarios

1. **Direct injection** — attacker prompts a support chatbot to ignore guidelines, query private data stores, and send email.
2. **Indirect injection via retrieved web content** — hidden page instructions make the model insert a markdown image whose URL exfiltrates the conversation.
3. **Unintentional injection** — a job-description PDF embeds an AI-detection instruction; an applicant's LLM surfaces it and the recruiting system flags the candidate. Neither party acted maliciously.
4. **RAG repository poisoning** — as few as five poisoned documents reached roughly 90% attack success against a knowledge base of millions.
5. **Payload splitting** — instructions split across resume fields, recombined by the LLM at evaluation.
6. **Multimodal steganographic injection** — an instruction embedded below the human visual threshold, extracted by the vision encoder. Demonstrated against four frontier vision-language models in oncology imaging.
7. **Zero-click document-borne agentic exfiltration** — a crafted email triggers a productivity assistant to exfiltrate organizational data with no user interaction, bypassing both a deployed injection classifier and a link-redaction filter (Microsoft 365 Copilot, 2025).
8. **Agentic destructive command execution** — an agent with shell, file-system, or cloud-API access amplifies an injection into a host-impacting incident (Amazon Q, July 2025).
9. **Trusted-backend indirect injection through MCP** — a poisoned GitHub issue exfiltrated private repositories; a Supabase MCP server running `service_role` dumped a production database; a malicious `postmark-mcp` package BCC'd email to an attacker across an estimated 300 organizations.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C2.1 Prompt Injection Defenses | Normalization, encoding-smuggling detection, injection screening with blocking, length rejection, character allow-list, instruction hierarchy, special-token literals, many-shot detection | 2.1.1–2.1.8 |
| C2.2 Content & Policy Screening | Content classification with thresholds, unsupported-language evaluation, non-text input screening, cross-modal attack detection | 2.2.1–2.2.4 |
| C7.3 Output Safety | Prevent model output from triggering outbound requests; detect hidden/encoded content | 7.3.3, 7.3.4 |
| C8.2 Embedding Sanitization & Validation | Validate agent/tool output before memory writes; reject retrieval-manipulating content | 8.2.3, 8.2.4 |
| C9.2 High-Impact Action Approval | Deterministic approval gate, canonicalized parameter display, injection-hardened AI review | 9.2.1, 9.2.2, 9.2.6, 9.2.7 |
| C9.3 Component Isolation and Tool Authorization | Isolate untrusted-data processing from tool calling; allow-list external resources named in output | 9.3.5, 9.3.6, 9.3.7 |
| C10.4 Schema, Message, and Input Validation | Screen MCP responses for indirect injection; re-approve changed tool definitions | 10.4.1, 10.4.2, 10.4.8 |
| C11.1 Alignment, Safety & Robustness Testing | Alignment training, per-release test suite, modality-relevant adversarial evaluation | 11.1.1, 11.1.2, 11.1.3 |
| C11.4 Model Runtime Anomaly Detection | Pre-inference anomaly detection on untrusted input, with gating on flagged inputs | 11.4.1, 11.4.2 |
| C12.2 Detection and Alerting | Detect jailbreak/injection patterns, behavioral anomalies, coordinated attempts | 12.2.1, 12.2.2, 12.2.3 |

## Related Frameworks

- AML.T0051.000 — LLM Prompt Injection: Direct (MITRE ATLAS)
- AML.T0051.001 — LLM Prompt Injection: Indirect (MITRE ATLAS)
- AML.T0054 — LLM Jailbreak Injection: Direct (MITRE ATLAS)
- ASI04 — Agentic Supply Chain Vulnerabilities (OWASP Top 10 for Agentic Applications)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)
- [AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)
- [JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models](https://arxiv.org/abs/2404.01318)
- [Prompt injection attacks on vision language models in oncology](https://www.nature.com/articles/s41467-024-55631-x)
- [StruQ: Defending Against Prompt Injection with Structured Queries](https://www.usenix.org/system/files/usenixsecurity25-chen-sizhe.pdf)
