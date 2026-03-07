---
title: "LLM02 Sensitive Information Disclosure"
owasp_llm_id: "LLM02"
when_to_use:
  - reviewing LLM apps that handle PII, credentials, or confidential data
  - assessing training data pipelines for data leakage risks
  - evaluating LLM outputs for unintended information exposure
  - auditing access controls on LLM-generated responses
threats:
  - PII leakage through model outputs
  - training data extraction and model inversion attacks
  - proprietary algorithm or business logic exposure
  - credential or API key disclosure via system prompts
summary: "LLMs may inadvertently expose sensitive data — PII, credentials, proprietary algorithms, or confidential business information — through their outputs, training data memorization, or misconfigured system prompts."
---

# LLM02:2025 Sensitive Information Disclosure

## Description

This vulnerability encompasses unauthorized exposure of sensitive data through LLM outputs, including PII, financial details, health records, confidential business information, security credentials, and proprietary algorithms. LLMs, especially when embedded in applications, risk exposing sensitive data through their output. The risk extends to both direct users and organizations deploying these systems.

## Common Examples

1. **PII leakage** — Unintended disclosure of personal identifiable information during LLM interactions
2. **Proprietary algorithm exposure** — Model misconfigurations revealing proprietary methods or training data, enabling inversion attacks
3. **Sensitive business data disclosure** — Confidential organizational information inadvertently included in generated responses
4. **Credential leakage** — API keys or credentials stored in system prompts exposed through prompt extraction

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Sanitization | Implement data scrubbing and masking techniques to prevent sensitive content from entering training processes. |
| 2 | Access controls | Limit access to sensitive data based on the principle of least privilege. Restrict model access to external data sources. |
| 3 | Federated learning | Deploy decentralized training across multiple servers to minimize centralized data exposure. |
| 4 | Differential privacy | Incorporate noise into data, making reverse-engineering individual data points difficult. |
| 5 | User education | Educate users on safe LLM interaction practices. Maintain clear data retention and deletion policies. |
| 6 | Secure configuration | Limit user ability to override system settings. Follow OWASP API8:2023 guidelines. |
| 7 | Tokenization and redaction | Use pattern-matching redaction to preprocess sensitive information before model interaction. |

## Example Attack Scenarios

1. **Unintentional data exposure** — Users receive responses containing others' personal data due to inadequate sanitization.
2. **Targeted prompt injection** — Attackers bypass filters to extract sensitive information through manipulated inputs.
3. **Training data leak** — Negligent inclusion of sensitive information in training datasets leads to disclosure.

## Related Frameworks

- AML.T0024.000 — Infer Training Data Membership (MITRE ATLAS)
- AML.T0024.001 — Invert ML Model (MITRE ATLAS)
- AML.T0024.002 — Extract ML Model (MITRE ATLAS)

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [ChatGPT Spit Out Sensitive Data When Told to Repeat 'Poem' Forever — Wired](https://www.wired.com/story/chatgpt-poem-forever-security-roundup/)
- [Lessons Learned from ChatGPT's Samsung Leak — Cybernews](https://cybernews.com/security/chatgpt-samsung-leak-explained-lessons/)
