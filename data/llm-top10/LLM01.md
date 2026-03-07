---
title: "LLM01 Prompt Injection"
owasp_llm_id: "LLM01"
when_to_use:
  - reviewing LLM applications that accept user input
  - assessing chatbots or AI assistants for injection risks
  - evaluating RAG pipelines where external content reaches the model
  - red-teaming AI applications for prompt manipulation
threats:
  - direct prompt injection via user input
  - indirect prompt injection via external content (web pages, documents, tool outputs)
  - jailbreaking to bypass safety guidelines
  - multimodal injection via images or audio
  - adversarial suffix attacks
summary: "Prompt injection occurs when user inputs or external content manipulate LLM behavior in unintended ways, causing guideline violations, unauthorized access, or data exfiltration."
---

# LLM01:2025 Prompt Injection

## Description

Prompt injection vulnerabilities occur when user inputs manipulate LLM behavior in unintended ways. These attacks can be imperceptible to humans and exploit how models process prompts. The vulnerability can cause models to violate guidelines, generate harmful content, enable unauthorized access, or influence critical decisions. While RAG and fine-tuning improve relevance, they don't fully prevent prompt injection.

**Direct Prompt Injection**: User input directly alters model behavior, either intentionally (malicious) or unintentionally (accidental).

**Indirect Prompt Injection**: External sources like websites, files, or tool outputs contain content that alters model behavior when processed.

## Potential Impacts

- Disclosure of sensitive information or system prompts
- Content manipulation producing incorrect or biased outputs
- Unauthorized access to LLM functions or connected systems
- Arbitrary command execution in downstream systems
- Manipulation of critical decision-making processes
- Cross-modal attacks via multimodal AI systems

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Constrain model behavior | Provide specific instructions about role, capabilities, and limitations in system prompts. Enforce strict context adherence. |
| 2 | Define and validate output formats | Specify clear output formats, request detailed reasoning with source citations. |
| 3 | Implement input/output filtering | Define sensitive categories, apply semantic filters, use the RAG Triad for relevance assessment. |
| 4 | Enforce privilege control | Provide the application with its own API tokens, handle functions in code rather than delegating to the model. |
| 5 | Require human approval | Implement human-in-the-loop controls for privileged operations. |
| 6 | Segregate external content | Separate and clearly denote untrusted content to limit its influence on user prompts. |
| 7 | Conduct adversarial testing | Perform regular penetration testing and breach simulations, treating the model as an untrusted user. |

## Example Attack Scenarios

1. **Direct injection** — Attacker injects prompt into customer support chatbot instructing it to ignore guidelines, access private data, and send emails.
2. **Indirect injection** — LLM summarizes webpage with hidden instructions causing insertion of image linked to URL, exfiltrating private conversation.
3. **RAG poisoning** — Attacker modifies document in RAG repository. When user query returns modified content, malicious instructions alter LLM output.
4. **Payload splitting** — Attacker uploads resume with split malicious prompts. Combined prompts during evaluation manipulate model response.
5. **Multimodal injection** — Attacker embeds malicious prompt in image accompanying benign text. Multimodal AI processing both concurrently processes hidden prompt.
6. **Adversarial suffix** — Attacker appends seemingly meaningless character string to prompt, influencing output and bypassing safety measures.
7. **Multilingual/obfuscated attack** — Attacker uses multiple languages or encodes instructions via Base64 or emojis to evade filters.

## Related Frameworks

- AML.T0051.000 — LLM Prompt Injection: Direct (MITRE ATLAS)
- AML.T0051.001 — LLM Prompt Injection: Indirect (MITRE ATLAS)
- AML.T0054 — LLM Jailbreak Injection: Direct (MITRE ATLAS)

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)
- [Threat Modeling LLM Applications — AI Village](https://aivillage.org/large%20language%20models/threat-modeling-llm/)
