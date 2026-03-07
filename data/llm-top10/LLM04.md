---
title: "LLM04 Data and Model Poisoning"
owasp_llm_id: "LLM04"
when_to_use:
  - reviewing training data pipelines for integrity risks
  - evaluating fine-tuning processes that use external data
  - assessing RAG knowledge bases for poisoning vectors
  - auditing model integrity and backdoor risks
threats:
  - training data manipulation introducing backdoors or biases
  - split-view and frontrunning data poisoning
  - sleeper agent models with dormant triggers
  - RAG knowledge base poisoning
  - malicious model serialization
summary: "Data poisoning manipulates training data across pre-training, fine-tuning, and embedding stages to introduce vulnerabilities, backdoors, or biases — including 'sleeper agent' models that remain dormant until triggered."
---

# LLM04:2025 Data and Model Poisoning

## Description

Data poisoning involves manipulating training data across pre-training, fine-tuning, embedding, and transfer learning stages to introduce vulnerabilities, backdoors, or biases. This integrity attack compromises model security, performance, and ethical behavior. External data sources pose particular risks, and distributed models may contain malware through malicious serialization techniques. Poisoning can implement backdoors that remain dormant until triggered, effectively creating "sleeper agent" models.

## Common Examples

1. **Split-view / frontrunning poisoning** — Malicious actors introduce harmful data using techniques that achieve biased outputs
2. **Direct content injection** — Harmful content injected during training compromises output quality
3. **User-contributed sensitive data** — Users unknowingly introduce sensitive or proprietary information during interactions
4. **Unverified training data** — Insufficient vetting increases risks of biased or erroneous outputs
5. **Insufficient resource restrictions** — Unrestricted data access allows ingestion of unsafe data

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Track data origins | Use OWASP CycloneDX or ML-BOM tools for provenance tracking. |
| 2 | Vet data vendors | Rigorously vet vendors and validate outputs against trusted sources. |
| 3 | Sandboxing | Implement strict sandboxing and anomaly detection to filter adversarial data. |
| 4 | Targeted fine-tuning | Tailor models through specific fine-tuning datasets for defined objectives. |
| 5 | Infrastructure controls | Prevent unintended data source access. |
| 6 | Data version control | Use DVC to track dataset changes and detect manipulation. |
| 7 | Vector database separation | Store user-supplied information in vector databases for adjustment without full retraining. |
| 8 | Red team campaigns | Conduct adversarial testing, including federated learning approaches. |
| 9 | Monitor training loss | Watch for poisoning signs using thresholds for anomaly detection. |
| 10 | RAG grounding | Integrate RAG and grounding techniques during inference to reduce risks. |

## Example Attack Scenarios

1. **Training data manipulation** — Attackers manipulate training data to bias model outputs and spread misinformation.
2. **Toxic data propagation** — Unfiltered toxic data produces harmful outputs that propagate dangerous information.
3. **Falsified training documents** — Malicious actors introduce falsified documents, causing inaccurate model outputs.
4. **Backdoor triggers** — Poisoning techniques embed triggers enabling authentication bypass, data exfiltration, or hidden command execution.

## Related Frameworks

- AML.T0018 — Backdoor ML Model (MITRE ATLAS)
- ML07:2023 — Transfer Learning Attack (OWASP ML Security Top 10)

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training — Anthropic](https://arxiv.org/abs/2401.05566)
- [Poisoning Language Models During Instruction Tuning](https://arxiv.org/abs/2305.00944)
