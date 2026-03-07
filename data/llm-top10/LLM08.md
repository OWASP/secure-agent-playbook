---
title: "LLM08 Vector and Embedding Weaknesses"
owasp_llm_id: "LLM08"
when_to_use:
  - reviewing RAG pipeline implementations for security risks
  - assessing vector database access controls and tenant isolation
  - evaluating embedding models for inversion or extraction risks
  - auditing knowledge base ingestion pipelines for poisoning
threats:
  - unauthorized access to embeddings across tenants
  - embedding inversion attacks recovering source text
  - RAG data poisoning via hidden content in documents
  - cross-context information leaks in multi-tenant vector stores
  - knowledge conflicts between retrieved and trained data
summary: "Vector and embedding weaknesses affect RAG systems through unauthorized access to embeddings, data poisoning of knowledge bases, embedding inversion attacks, and cross-tenant information leaks in shared vector stores."
---

# LLM08:2025 Vector and Embedding Weaknesses

## Description

This vulnerability category addresses risks in systems using Retrieval Augmented Generation (RAG) with LLMs. RAG combines pre-trained language models with external knowledge sources to enhance response quality and contextual relevance. Weaknesses in how vectors and embeddings are generated, stored, and retrieved can be exploited to inject harmful content, manipulate model outputs, or access sensitive information.

## Common Examples

1. **Unauthorized access and data leakage** — Insufficient access controls expose sensitive embeddings. Personal data, proprietary information, or copyrighted material disclosed without proper authorization.
2. **Cross-context information leaks** — In multi-tenant environments, risk of context leakage between users or queries. Data from multiple sources may contradict each other.
3. **Embedding inversion attacks** — Attackers invert embeddings to recover significant amounts of source information, compromising data confidentiality.
4. **Data poisoning attacks** — Malicious or unintentional poisoned data from insiders, prompts, or unverified sources manipulate model outputs.
5. **Behavior alteration** — RAG can inadvertently reduce qualities like emotional intelligence while improving factual accuracy.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Permission-aware vector stores | Implement fine-grained controls with strict logical and access partitioning to prevent cross-user access. |
| 2 | Data validation | Establish robust validation pipelines, regularly audit knowledge base integrity, accept data only from trusted sources. |
| 3 | Data classification | Thoroughly review combined datasets, tag and classify information to control access levels. |
| 4 | Monitoring and logging | Maintain detailed immutable logs of retrieval activities to detect suspicious behavior. |

## Example Attack Scenarios

1. **Data poisoning** — Attacker embeds hidden instructions (white text on white background) in a resume submitted to a RAG-based job screening system, causing it to recommend an unqualified candidate.
2. **Access control failure** — In multi-tenant environments sharing a vector database, embeddings from one user group are retrieved for another group's queries, leaking sensitive information.
3. **Behavior alteration** — After RAG implementation, an LLM's response to an emotional query becomes purely factual, losing empathetic tone despite remaining accurate.

## Related Frameworks

- AML.T0043 — Craft Adversarial Data (MITRE ATLAS)

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [Information Leakage in Embedding Models](https://arxiv.org/abs/2004.00053)
- [ConfusedPilot: Confused Deputy Risks in RAG-based LLMs](https://confusedpilot.info)
