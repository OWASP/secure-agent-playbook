---
title: "LLM09 Vector and Embedding Weaknesses"
owasp_llm_id: "LLM09"
owasp_llm_version: "2026"
when_to_use:
  - reviewing RAG pipelines, vector databases, or embedding stores
  - assessing multi-tenant similarity search for cross-tenant leakage
  - evaluating vector-store backups and export paths
  - auditing ingestion pipelines that embed externally sourced content
  - reviewing semantic caches and deduplication thresholds
  - assessing multimodal (CLIP, ColPali) retrieval pipelines
threats:
  - cross-tenant leakage via shared similarity search before access control
  - embedding inversion reconstructing source text
  - retrieval-time data poisoning placing content near target queries
  - retrieval jamming as an availability attack
  - membership inference via similarity scores
  - semantic cache and deduplication poisoning
  - multimodal embedding poisoning via crafted images
summary: "Security risks in any application that converts content into vectors and uses similarity search to decide what the model sees. These exploit embedding-space geometry rather than instruction-following, and many succeed even when retrieved content carries no malicious instructions."
aisvs_mappings:
  - section: "C1.1"
    title: "Training Data Origin & Data Security"
    requirements: ["1.1.3", "1.1.4"]
  - section: "C5.2"
    title: "AI Resource Authorization & Classification"
    requirements: ["5.2.1", "5.2.2", "5.2.4", "5.2.7"]
  - section: "C5.3"
    title: "Multi-Tenant Isolation"
    requirements: ["5.3.1", "5.3.2"]
  - section: "C7.4"
    title: "Source Attribution & Citation Integrity"
    requirements: ["7.4.1", "7.4.3"]
  - section: "C8.1"
    title: "Access Controls on Memory & RAG Indices"
    requirements: ["8.1.1", "8.1.2", "8.1.3"]
  - section: "C8.2"
    title: "Embedding Sanitization & Validation"
    requirements: ["8.2.1", "8.2.2", "8.2.3", "8.2.4", "8.2.5"]
  - section: "C8.3"
    title: "Memory Expiry & Revocation"
    requirements: ["8.3.1", "8.3.2", "8.3.3"]
  - section: "C11.2"
    title: "Membership-Inference and Model-Inversion Mitigation"
    requirements: ["11.2.1", "11.2.2", "11.2.4"]
  - section: "C12.1"
    title: "Request & Response Logging"
    requirements: ["12.1.4"]
  - section: "C12.2"
    title: "Detection and Alerting"
    requirements: ["12.2.2"]
---

# LLM09:2026 Vector and Embedding Weaknesses

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM09:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM09_VectorAndEmbeddingWeaknesses.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

Vector and embedding weaknesses present security risks in any LLM application that converts text, images, code, or audio into numerical representations and uses similarity search to decide what the model sees. RAG is the most familiar case, but the same machinery underlies vector-backed agent memory, semantic caches, and deduplication pipelines. **Whenever similarity search sits between a data source and the prompt, the embedding layer becomes part of the application's trust boundary.**

These weaknesses are distinct from prompt injection. They exploit **the geometry of the embedding space and the mechanics of similarity search** rather than the model's instruction-following behavior. Many succeed even when the retrieved content carries no malicious instructions at all.

> A useful frame: **poisoning makes the system wrong, inversion makes it leak, jamming makes it silent, and access-control failure makes it indiscriminate.**

Scope: indirect prompt injection through retrieved content is [LLM01](LLM01.md); training-time poisoning of the embedding model is [LLM05](LLM05.md); serialization flaws in vector-store libraries are [LLM04](LLM04.md); agent-memory attacks not relying on embedding geometry are ASI06. Vectorless retrieval systems (BM25-only, LLM-native tree navigation) inherit the non-geometric risks but have no LLM09 attack surface.

## Potential Impacts

- Cross-tenant inference of document existence, topic, and volume without ever seeing the documents
- Reclassification of an "embeddings-only" leak as a source-document breach, restarting notification clocks
- Attacker-controlled content served as trusted context to every user asking a target question
- Denial of service on the retrieval layer
- Regulatory exposure where membership itself is sensitive

## Common Examples of Risk

1. **Cross-tenant leakage via shared similarity search** — search frequently runs across the full index *before* application-layer access control. An attacker probes with crafted queries and infers existence, topic, and approximate volume of other tenants' documents from result counts, score distributions, and timing. **The attack succeeds even when every document is correctly tagged and every API call authenticated**, because the access-control decision happens after the embedding-space search has run. Conventional vector-DB auth flaws (CVE-2025-64513 Milvus, CVE-2025-69286 RAGFlow, both CVSS 9.3) compound this: because a vector-store leak is recoverable to source documents via inversion, an auth bug in a vector database carries higher consequence than the same bug in a document store.
2. **Embedding inversion** — recovery rates range from roughly 50–70% of words from sentence embeddings to 92% exact reconstruction of short 32-token inputs (Vec2Text). ZSInvert and Zero2Text operate **zero-shot** with no encoder-specific training, work in cross-domain and black-box settings, and remain effective against differential-privacy noise added at storage. Operationally: vector-database backups, embeddings shipped to third parties, and embeddings in misconfigured cloud storage should be treated as equivalent to a leak of the underlying documents.
3. **Retrieval-time data poisoning** — an attacker who can write to the corpus crafts content whose embedding lands close to a target query. Published attacks reliably achieve high success with a handful of poisoned documents, even in corpora of millions and against black-box systems. Success requires two conditions simultaneously — the content must be **retrieved** (geometric) and must **steer the response** (generation) — so defenders can intervene at either layer.
4. **Retrieval jamming** — a "blocker" document engineered to be retrieved for a specific query and cause the LLM to refuse or claim it lacks information. It carries no malicious instructions; it exploits retrieval mechanics and LLM safety behavior. A single blocker, generated through black-box optimization, suffices. **This is an availability attack on the retrieval layer.**
5. **Membership inference via similarity search** — the attacker wants to know whether a specific document exists, not what it says. **If the application returns raw similarity scores to the client, the index becomes a direct membership oracle with no LLM involved.**
6. **Semantic cache and deduplication poisoning** — an attacker crafting content just above or below the cosine-similarity threshold can poison a cache entry so it serves attacker text to all semantically equivalent queries, bypass deduplication with near-duplicates, or force legitimate content to be silently dropped as a duplicate. Demonstrated end-to-end across AWS, Azure, and Alibaba deployments. **Invisible to document-level controls.**
7. **Multimodal embedding poisoning** — cross-modal encoders (CLIP, ColPali) map images, audio, code, and text into one vector space. A crafted image whose embedding sits near a sensitive text query is retrieved as trusted context. To a human reviewer the image appears unremarkable, and text-based content scanning does not catch it.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Permission and access control | Enforce tenant scoping **inside the index query**, not as a post-retrieval filter, validated server-side. A client-supplied scope is a suggestion, not a control. Authenticate embedding and similarity-search endpoints as first-class APIs with per-tenant rate limits. Apply **chunk-level** access control — a mostly-public document can contain a confidential paragraph. |
| 2 | Data validation, source authentication, provenance | Normalize before embedding: strip zero-width characters, white-on-white text, Unicode homoglyphs at extraction. Track provenance per embedding (source, ingestion time, trust tier, pipeline version) so compromised batches can be invalidated. **Vet the embedding model itself — a backdoored encoder corrupts the geometry of everything ingested.** |
| 3 | Data segregation by trust tier | Mixed-trust content must not share an index without hard isolation. **Index-level segregation beats classification tags on a shared index** because it removes the misconfiguration path. |
| 4 | Anomaly detection at ingest and retrieval | Flag new vectors sitting unusually close to a wide range of common queries. Watch for queries returning too many high-similarity matches and unusual embedding-endpoint volume. **Do not return raw similarity scores to clients.** Cross-encoder re-ranking raises attack cost but does not replace provenance and ingest controls. |
| 5 | Storage lifecycle controls | Delete embeddings within a bounded time when the source is deleted, verified by reconciliation audits. Treat backups at the same sensitivity tier as source documents. Encrypt at rest with separately managed keys. **When rotating the embedding model, re-embed the corpus** rather than mixing old and new vectors. Treat embedding-API keys as secrets. |
| 6 | Monitoring, logging, incident response | Immutable retrieval logs (tenant scope, query, returned IDs, similarity scores). Monitor for tenant-filter bypass and cross-tenant anomalies. **Update playbooks so "embeddings only" leaks are treated as source-data leaks** for breach assessment under GDPR Article 33 and analogous regimes. |

## Example Attack Scenarios

1. **Embedding similarity attack on a public ingestion pipeline** — an attacker publishes forum posts engineered so their embeddings land near specific internal queries ("what is our Q3 revenue projection"). The same text pasted into a chat would have no effect; the attack works only because the attacker can place content near a target query in embedding space.
2. **Cross-tenant inference in a shared vector index** — Tenant A submits probing queries. Search runs across every embedding including Tenant B's before the filter applies. A never sees B's documents, but timing, result counts, and score-distribution gaps reveal existence and approximate topic. Over many queries A builds a useful map of B's data.
3. **Embedding inversion from a leaked vector store** — a cloud misconfiguration exposes a vector-database backup. The underlying documents are encrypted separately, so the incident is initially classified low-severity: "only the embeddings leaked." Zero-shot inversion reconstructs a substantial fraction of the source content including PII. **"Embeddings only" is not a safe-harbor classification.**

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C1.1 Training Data Origin & Data Security | Integrity in storage and transfer; integrity monitoring for the corpus behind the index | 1.1.3, 1.1.4 |
| C5.2 AI Resource Authorization & Classification | Default-deny on vector collections and embedding indices, **end-user authorization enforced at each retrieval stage**, post-inference filtering, label propagation to embeddings | 5.2.1, 5.2.2, 5.2.4, 5.2.7 |
| C5.3 Multi-Tenant Isolation | Prevent one tenant's embedding operations from influencing or observing another's | 5.3.1, 5.3.2 |
| C7.4 Source Attribution & Citation Integrity | Metadata-derived attribution and claim traceability to the retrieved chunk | 7.4.1, 7.4.3 |
| C8.1 Access Controls on Memory & RAG Indices | **Per-tenant uniqueness of identifiers and namespaces**, immutable document metadata, scope constraints on retrieval | 8.1.1, 8.1.2, 8.1.3 |
| C8.2 Embedding Sanitization & Validation | Pre-embedding sensitive-field masking, outlier vector quarantine, validated memory writes, retrieval-manipulation detection, contradiction checks | 8.2.1–8.2.5 |
| C8.3 Memory Expiry & Revocation | Expired vectors excluded from retrieval, memory reset, quarantined content retained but unreachable | 8.3.1, 8.3.2, 8.3.3 |
| C11.2 Membership-Inference & Model-Inversion Mitigation | Suppress inferred sensitive attributes, rate limits sized to the inference threat model, DP optimization | 11.2.1, 11.2.2, 11.2.4 |
| C12.1 Request & Response Logging | **RAG retrieval events logged with query, documents retrieved, and knowledge source** | 12.1.4 |
| C12.2 Detection and Alerting | Behavioral anomaly detection for probing and excessive retry patterns | 12.2.2 |

## Related Frameworks

- AML.T0070 — RAG Poisoning (MITRE ATLAS)
- AML.T0024.000 — Infer Training Data Membership (MITRE ATLAS)
- ASI06 — Memory and Context Poisoning (OWASP Top 10 for Agentic Applications)
- DSGAI13 — Embedding and vector-store protection (OWASP Data Security for GenAI)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [Text Embeddings Reveal (Almost) As Much As Text](https://arxiv.org/abs/2310.06816)
- [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867)
- [MM-PoisonRAG: Disrupting Multimodal RAG with Local and Global Poisoning Attacks](https://arxiv.org/abs/2502.17832)
