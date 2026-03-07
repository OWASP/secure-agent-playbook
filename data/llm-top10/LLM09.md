---
title: "LLM09 Misinformation"
owasp_llm_id: "LLM09"
when_to_use:
  - reviewing LLM apps used in high-stakes domains (medical, legal, financial)
  - assessing grounding and fact-checking mechanisms in LLM outputs
  - evaluating code generation features for hallucinated packages
  - auditing user-facing AI applications for overreliance risks
threats:
  - hallucinated facts presented as authoritative
  - fabricated legal cases, medical advice, or technical references
  - hallucinated software packages weaponized for supply chain attacks
  - reputational and legal liability from incorrect AI outputs
summary: "LLMs generate false or misleading information that appears credible (hallucination), causing security breaches when fabricated packages are weaponized, legal liability from incorrect advice, and reputational damage from authoritative-sounding misinformation."
---

# LLM09:2025 Misinformation

## Description

This vulnerability addresses how LLMs generate false or misleading information that appears credible, potentially causing security breaches, reputational damage, and legal liability. Key causes include hallucination (models fabricate content by filling training data gaps using statistical patterns) and overreliance (users place excessive trust in LLM outputs without verification).

## Common Examples

1. **Factual inaccuracies** — Air Canada's chatbot provided incorrect travel information, resulting in successful litigation against the airline.
2. **Unsupported claims** — ChatGPT generated fictitious legal cases that were cited in actual court proceedings.
3. **Misrepresentation of expertise** — Chatbots misrepresent complexity regarding health matters, falsely suggesting legitimate debate around unproven treatments.
4. **Unsafe code generation** — LLMs recommend non-existent or insecure code libraries, introducing vulnerabilities when developers trust suggestions without scrutiny.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Retrieval-Augmented Generation | Retrieve verified information from trusted external databases to reduce hallucinations. |
| 2 | Model fine-tuning | Apply techniques like parameter-efficient tuning and chain-of-thought prompting. |
| 3 | Cross-verification | Implement fact-checking processes with trained human reviewers. |
| 4 | Automatic validation | Validate outputs programmatically in high-stakes environments. |
| 5 | Risk communication | Clearly convey limitations and misinformation potential to users. |
| 6 | Secure coding practices | Verify all LLM-suggested packages and libraries exist and are trustworthy before use. |
| 7 | UI design | Label AI-generated content, integrate filters, specify field-of-use limitations. |
| 8 | Training and education | Educate users on LLM limitations and importance of independent verification. |

## Example Attack Scenarios

1. **Package hallucination attack** — Attackers identify hallucinated package names suggested by coding assistants, then publish malicious packages using those names. Developers unknowingly integrate compromised code.
2. **Medical chatbot liability** — A company deploys a diagnosis chatbot without ensuring accuracy. Poor guidance causes patient harm, leading to successful litigation.

## Related Frameworks

- CWE-1357 — Reliance on Insufficiently Trustworthy Component

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [AI Package Hallucinations — Lasso Security](https://www.lasso.security/blog/ai-package-hallucinations)
- [Air Canada Chatbot Misinformation — BBC](https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-]
