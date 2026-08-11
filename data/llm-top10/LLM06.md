---
title: "LLM06 Unbounded Consumption"
owasp_llm_id: "LLM06"
owasp_llm_version: "2026"
when_to_use:
  - reviewing rate limiting and quota enforcement on inference endpoints
  - assessing cost controls for pay-per-token or cloud-hosted models
  - evaluating agentic architectures for recursion and fan-out limits
  - auditing extended-thinking / reasoning models for token budget controls
  - reviewing multimodal endpoints for per-request cost asymmetry
  - assessing inference serving frameworks for known CVEs
threats:
  - variable-length input flood and output explosion
  - denial of wallet (DoW) through cost-per-use exploitation
  - large-context abuse staying just within limits
  - reasoning-loop and thinking-token exhaustion
  - adversarial inputs optimized for resource overconsumption (sponge examples)
  - multimodal token amplification
  - model extraction and distillation theft
  - agent-tool recursive loops and tool-call fan-out
  - inference infrastructure exploitation (unsafe deserialization, special-token injection)
summary: "Excessive and uncontrolled inferences let attackers disrupt availability, inflict unsustainable cost, or steal IP through model cloning. The defining characteristic is cost asymmetry — attackers trigger disproportionately expensive computation at negligible cost."
aisvs_mappings:
  - section: "C2.1"
    title: "Prompt Injection Defenses"
    requirements: ["2.1.4"]
  - section: "C5.2"
    title: "AI Resource Authorization & Classification"
    requirements: ["5.2.1"]
  - section: "C7.1"
    title: "Output Format Enforcement"
    requirements: ["7.1.2"]
  - section: "C9.1"
    title: "Execution Budgets, Loop Control, and Circuit Breakers"
    requirements: ["9.1.1", "9.1.2", "9.1.3"]
  - section: "C9.3"
    title: "Component Isolation and Tool Authorization"
    requirements: ["9.3.1", "9.3.3", "9.3.4"]
  - section: "C9.6"
    title: "Shutdown and Graceful Degradation"
    requirements: ["9.6.1", "9.6.3"]
  - section: "C10.4"
    title: "Schema, Message, and Input Validation"
    requirements: ["10.4.3", "10.4.5"]
  - section: "C11.2"
    title: "Membership-Inference and Model-Inversion Mitigation"
    requirements: ["11.2.2"]
  - section: "C11.3"
    title: "Model-Extraction Defense"
    requirements: ["11.3.1", "11.3.2", "11.3.3", "11.3.4"]
  - section: "C12.2"
    title: "Detection and Alerting"
    requirements: ["12.2.4", "12.2.5"]
---

# LLM06:2026 Unbounded Consumption

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM06:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM06_UnboundedConsumption.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

Unbounded Consumption occurs when an LLM application allows excessive and uncontrolled inferences, enabling attackers to disrupt service availability, inflict unsustainable financial costs, or steal intellectual property through model cloning — all by exploiting the absence of adequate controls over how resources are consumed.

The high computational demands of LLMs, particularly in cloud and pay-per-token environments, make them inherently susceptible to resource exploitation. **A defining characteristic is cost asymmetry**: attackers trigger disproportionately expensive computation at negligible cost to themselves, whether through crafted prompts, stolen credentials, or manipulated workflows.

The risk is compounded by:

- extended-thinking and reasoning models with large or insufficiently constrained output budgets
- multimodal models that substantially increase per-request compute cost
- agentic architectures and tool-use protocols (such as MCP) that amplify a single request into cascading downstream operations
- shared inference infrastructure introducing new supply-chain attack surfaces

**Traditional request-rate limiting alone is no longer sufficient.** Effective defense demands token-aware cost controls, hard spending caps, agent-level circuit breakers, and continuous cost-attribution monitoring.

## Potential Impacts

- Service degradation or outage for legitimate users
- Financial ruin through denial of wallet on pay-per-use services
- Loss of intellectual property via functional model replication
- Cascading downstream operations from a single request in agentic deployments

## Common Examples of Risk

1. **Variable-length input flood and output explosion** — includes output explosion via fine-tuning poisoning, where a single malicious training sample breaks end-of-sequence behavior and pushes output to maximum length on every request.
2. **Denial of Wallet (DoW)** — high-volume operations exploit the cost-per-use model of cloud AI services.
3. **Large-context abuse** — repeated near-limit requests, context accumulation, and application-side rechunking. Many APIs reject over-limit inputs outright, so the durable risk comes from requests that **stay just within limits while inflating per-request cost**.
4. **Reasoning-loop and thinking-token exhaustion** — short, benign-looking prompts force extended-thinking models into prolonged or non-terminating reasoning loops, consuming massive thinking-token budgets while bypassing input-size filters. Standard input validation provides no protection.
5. **Adversarial inputs optimized for resource overconsumption** — sponge examples and adversarial visual perturbations. Distinct from simply asking for a resource-intensive task; requires explicit optimization over the input space.
6. **Multimodal inputs and outputs** — images, audio, and video convert into large numbers of tokens, so a single request can cost substantially more than a comparable text-only request.
7. **Model extraction and distillation theft** — crafted queries collect enough outputs to replicate a partial model or fine-tune a functional equivalent. **Exposure of logits and log-probabilities significantly accelerates extraction.**
8. **Agent-tool interactions flooding model resources** — published tools force recursive or infinite tool-calling loops; a single task can spawn hundreds of calls.
9. **Inference infrastructure exploitation** — vulnerabilities in serving frameworks (vLLM, TensorRT-LLM, SGLang, Triton, Ollama) via unsafe deserialization, special-token injection, and injected chat templates.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Rate limiting and input size validation | Move beyond requests/second to **tokens-per-minute, tokens-per-day, and estimated cost per request**. Use pre-flight token estimation to reject before inference begins. |
| 2 | Hard spending caps | Non-overridable budget ceilings per API key, user, team, and cloud account. These must **halt inference**, not merely alert — fast-accumulating workloads outpace alerting thresholds. Account for cost differences between modalities and tool protocols. |
| 3 | Resource allocation management | Monitor and manage allocation dynamically so no single user or request consumes excessive resources. |
| 4 | Sandbox techniques | Restrict the LLM's access to network resources, internal services, and APIs, limiting exfiltration of extracted model information. |
| 5 | Graceful degradation | Maintain partial functionality under heavy load rather than complete failure. |
| 6 | Limit queued actions and scale robustly | Restrict queued and total actions; incorporate dynamic scaling and load balancing. |
| 7 | Scan for adversarial perturbations | Particularly visual inputs to LVLMs, for perturbations causing resource overconsumption. |
| 8 | Detect resource-intensive tool interactions | Baseline normal tool behavior; identify sessions causing recursive or unbounded action without a clear end state. |
| 9 | Agentic circuit breakers | Step limits, recursion depth limits, time limits, and per-run cost ceilings. **Use state hashing to detect recursive loops.** |
| 10 | Inference infrastructure hardening | Keep serving frameworks updated; disable unsafe deserialization, restrict special-token passthrough, enforce authentication on all inference endpoints. |

## Example Attack Scenarios

1. **Uncontrolled input size** — an unusually large input causes excessive memory and CPU load, crashing or slowing the service.
2. **Repeated requests** — high-volume API requests make the service unavailable to legitimate users.
3. **Resource-intensive queries** — inputs crafted to trigger the most computationally expensive processes, producing prolonged GPU usage.
4. **Denial of Wallet** — excessive operations exploit the pay-per-use model, causing unsustainable provider costs.
5. **Functional model replication** — the API generates synthetic training data used to fine-tune a functional equivalent, bypassing traditional extraction limitations.
6. **Perturbations in LVLM image input** — adversarial images optimized to make the model overconsume output tokens.
7. **Multi-turn tool calling loops and fan-out** — a malicious published tool instructs an agent to perform recursive cyclical tasks or tasks requiring a large number of calls.
8. **Growing LLM context in agentic sessions** — content injected gradually into an open session so each inference re-processes the full accumulated context. Per-turn cost climbs from roughly $0.001 on turn one to about $0.50 by turn 100. **No single request triggers rate limits**, yet the aggregate across concurrent or long-lived sessions reaches hundreds of dollars.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C2.1 Prompt Injection Defenses | Input length controls that **reject** rather than truncate over-limit input | 2.1.4 |
| C5.2 AI Resource Authorization & Classification | Default-deny access control on endpoints and compute instances | 5.2.1 |
| C7.1 Output Format Enforcement | Length limits and termination controls on generated output | 7.1.2 |
| C9.1 Execution Budgets & Circuit Breakers | Per-tool quotas and timeouts, per-execution budgets (recursion depth, token use, monetary spend), swarm-level kill-switch | 9.1.1, 9.1.2, 9.1.3 |
| C9.3 Component Isolation and Tool Authorization | Least-privilege sandbox, manifest-declared resource limits, runtime enforcement of those limits | 9.3.1, 9.3.3, 9.3.4 |
| C9.6 Shutdown and Graceful Degradation | Manual kill-switch halting inference; out-of-band shutdown channel | 9.6.1, 9.6.3 |
| C10.4 Schema, Message, and Input Validation | Reject unrecognized or oversized parameters; enforce maximum MCP payload sizes | 10.4.3, 10.4.5 |
| C11.2 Membership-Inference & Model-Inversion Mitigation | Per-principal and global rate limits sized to the extraction threat model | 11.2.2 |
| C11.3 Model-Extraction Defense | Query-pattern analysis feeding an extraction detector, restricted raw-output exposure, watermarking, automated response | 11.3.1–11.3.4 |
| C12.2 Detection and Alerting | Extraction-alert query metadata; **token usage tracked per user, session, endpoint, and team** | 12.2.4, 12.2.5 |

## Related Frameworks

- AML.T0024.002 — Extract AI Model (MITRE ATLAS)
- AML.T0029 — Denial of AI Service (MITRE ATLAS)
- ASI08 — Cascading Failures (OWASP Top 10 for Agentic Applications)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [Sponge Examples: Energy-Latency Attacks on Neural Networks](https://arxiv.org/abs/2006.03463)
- [Stealing Part of a Production Language Model](https://arxiv.org/abs/2403.06634)
