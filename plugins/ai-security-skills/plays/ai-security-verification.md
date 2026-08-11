# Play: AI Security Verification Standard (AISVS)

Comprehensive security verification of AI-driven applications using the OWASP AI Security
Verification Standard (AISVS) **v1.0** (June 2026) — 12 chapters, 44 sections, 191 testable
requirements across three verification levels.

## Trigger Conditions

Use this play when:
- Conducting security verification of AI/ML applications
- Performing pre-deployment security assessments
- Evaluating AI system compliance with security standards
- Auditing existing AI applications for security gaps
- Preparing for AI security certifications or compliance reviews
- Assessing third-party AI solutions before procurement

## Inputs

- AI application architecture documentation
- Model training, fine-tuning, and deployment pipelines
- Data governance policies and procedures
- Infrastructure and deployment configurations
- Access control and identity management systems
- MCP server and tool/plugin configurations
- Agent orchestration and approval-gate configuration
- Monitoring and logging implementations

## Verification Levels

AISVS assigns each requirement a level. Scope the assessment before starting:

| Level | Applies to | Meaning |
|-------|-----------|---------|
| **1** | All AI systems | Baseline controls; expected of any production AI system |
| **2** | Systems handling sensitive data or taking consequential actions | Standard for most business applications |
| **3** | High-assurance systems | Critical/regulated deployments; includes cryptographic and formal-assurance controls |

State the target level in the report. A finding against an L3 requirement in an L1-scoped
system is informational, not a gap.

## Procedure

Work through the 12 chapters. Each section below names the AISVS sections it covers; consult
the corresponding `C<chapter>.<section>.md` reference files for the verbatim requirement text
and levels.

### C1. Training Data Integrity & Traceability

*Sections: C1.1 Training Data Origin & Data Security · C1.2 Data Labeling and Annotation
Security · C1.3 Training Data Quality and Security Assurance*

- [ ] **Data minimization** — Does training data contain only features required for the model's stated purpose? (1.1.1, L1)
- [ ] **Source inventory** — Is there an up-to-date inventory of every training-data source with origin, responsible party, license, collection method, use constraints, and processing history? (1.1.2, L2)
- [ ] **Integrity in storage and transit** — Is training data integrity-protected when stored and transferred, with monitoring for unauthorized modification? (1.1.3–1.1.4, L2)
- [ ] **Dataset watermarking** — Are datasets watermarked so unauthorized use can be attributed? (1.1.5, L3)
- [ ] **Labeling access control** — Do labeling platforms restrict who can create, modify, or approve annotations? (1.2.1, L1)
- [ ] **Label artifact integrity** — Are labeling artifacts cryptographically integrity-protected, with sensitive label content redacted or encrypted? (1.2.2–1.2.3, L2)
- [ ] **Poisoning detection** — Do training and fine-tuning pipelines implement poisoning detection? (1.3.1, L2)
- [ ] **Label quality gates** — Are machine-generated labels subject to confidence thresholds and consistency checks? (1.3.2, L2)
- [ ] **Bias evaluation** — Are models used in security-relevant decisions evaluated for bias patterns? (1.3.3, L2)
- [ ] **Disallowed content removal** — Is disallowed content detected and removed before training? (1.3.4, L2)
- [ ] **Clean-label defenses** — Are defenses against clean-label poisoning implemented? (1.3.5, L3)

**Testing approach:** Review data governance documentation and the source inventory. Audit
dataset access logs and the labeling platform's permission model. Verify checksums/signatures
on stored datasets. Inspect pipeline code for poisoning-detection and content-filtering steps.

---

### C2. Input Validation

*Sections: C2.1 Prompt Injection Defenses · C2.2 Content & Policy Screening*

- [ ] **Normalization** — Is input normalized before tokenization or embedding? (2.1.1, L1)
- [ ] **Encoding smuggling** — Is encoding/representation smuggling detected and mitigated via canonicalization, schema validation, rejection, or explicit marking? (2.1.2, L1)
- [ ] **Injection screening** — Are all behavior-steering inputs treated as untrusted and screened by an injection ruleset or classifier, with flagged inputs *blocked*? (2.1.3, L1)
- [ ] **Length controls** — Do input length controls *reject* over-limit input rather than truncating it? (2.1.4, L1)
- [ ] **Character allow-list** — Is there an allow-list character-set restriction? (2.1.5, L1)
- [ ] **Instruction hierarchy** — Do system/developer messages override user instructions even after user input has been processed? (2.1.6, L2)
- [ ] **Special tokens** — Are reserved special tokens encoded as literals so they cannot be injected? (2.1.7, L2)
- [ ] **Many-shot jailbreak detection** — Can the system detect many-shot jailbreaking patterns? (2.1.8, L3)
- [ ] **Content classification** — Is every prompt scored for violence, self-harm, hate, and sexual content against configurable thresholds, and rejected or sanitized above them? (2.2.1, L1)
- [ ] **Language coverage** — Is prompt classification evaluated for unsupported languages? (2.2.2, L1)
- [ ] **Non-text inputs** — Are image/video/audio inputs checked for adversarial perturbations, steganographic payloads, and hidden content? (2.2.3, L2)
- [ ] **Cross-modal attacks** — Are coordinated attacks spanning multiple input types detected? (2.2.4, L3)

**Testing approach:** Run a prompt-injection payload set (direct, indirect, encoded,
multilingual). Submit oversized inputs and confirm rejection rather than truncation. Attempt
special-token injection. Test classifier behavior in low-resource languages. For multimodal
systems, submit steganographic image payloads paired with benign text.

---

### C3. Model Lifecycle Management & Change Control

*Sections: C3.1 Model Authorization & Integrity · C3.2 Model Validation & Testing ·
C3.3 Controlled Deployment & Rollback · C3.4 Secure Development Practices ·
C3.5 Pipeline Fine-Tuning*

- [ ] **Model registry** — Does a registry inventory all deployed model artifacts and their origin? (3.1.1, L1)
- [ ] **Artifact signing** — Are weights, configs, tokenizers, base models, fine-tunes, adapters, and safety models cryptographically signed, with signatures verified at admission and on load? (3.1.2–3.1.3, L2)
- [ ] **Pre-deployment testing** — Do models undergo input validation, safety evaluation, and output sanitization testing before deployment? (3.2.1, L1)
- [ ] **Quantization re-evaluation** — Are quantized artifacts re-run against the same safety and alignment suite? (3.2.2, L2)
- [ ] **Provider change gates** — Do provider model, version, or routing changes trigger security re-evaluation? (3.2.3, L3)
- [ ] **Rollout and rollback** — Are there rollout mechanisms with automated rollback triggers, and does rollback restore complete model state? (3.3.1–3.3.2, L2)
- [ ] **Parallel version isolation** — Do parallel model versions use isolated runtime state? (3.3.3, L2)
- [ ] **Environment separation** — Are AI runtime components unshared across dev/staging/prod, and training environments isolated from production? (3.4.1–3.4.2, L1–L2)
- [ ] **RLHF integrity** — Are RLHF models versioned and integrity-verified before a training run? (3.5.1, L2)
- [ ] **Reward hacking detection** — Do RLHF stages include automated reward-hacking / over-optimization detection? (3.5.2, L3)
- [ ] **Multi-stage verification** — Is each fine-tuning stage's output integrity-verified before the next stage consumes it, with checkpoints registered as distinct artifacts? (3.5.3–3.5.4, L3)

**Testing approach:** Inspect the model registry against what is actually loaded in
production. Attempt to deploy an unsigned or modified artifact and confirm admission is
denied. Execute a rollback and verify complete state restoration. Trace a fine-tuning run
end-to-end for integrity checks between stages.

---

### C4. Infrastructure, Configuration & Deployment Security

*Sections: C4.1 AI Workload Sandboxing & Validation · C4.2 AI Hardware Security ·
C4.3 Edge & Distributed AI Security*

- [ ] **Model sandboxing** — Do models execute in isolated sandboxes? (4.1.1, L1)
- [ ] **Serialization allow-list** — Does artifact loading enforce an allow-list of formats that cannot execute code during deserialization? (4.1.2, L1)
- [ ] **Workload attestation** — Is the execution environment attested before model loading? (4.1.3, L3)
- [ ] **Confidential inference** — Are model weights protected at runtime by isolated execution environments? (4.1.4, L3)
- [ ] **Accelerator firmware** — Is GPU/accelerator firmware version-pinned, signed, and attested at boot? (4.2.1, L2)
- [ ] **TEE isolation** — Does TEE execution provide hardware-enforced isolation, memory encryption, and integrity protection? (4.2.2, L3)
- [ ] **GPU attestation and memory isolation** — Is accelerator integrity attested per workload, with memory partitioned and sanitized between jobs? (4.2.3–4.2.4, L3)
- [ ] **Interconnect restriction** — Are accelerator interconnects restricted to approved topologies and authenticated endpoints? (4.2.5, L3)
- [ ] **Edge device authentication** — Do edge AI devices authenticate to central infrastructure with strong mechanisms? (4.3.1, L1)
- [ ] **Signed on-device models** — Are edge/mobile models signed at packaging and validated by the on-device runtime before load? (4.3.2, L2)
- [ ] **On-device isolation and encryption** — Do inference runtimes enforce process/memory/file isolation, with weights encrypted using hardware-backed key stores and decrypted only inside a trusted runtime? (4.3.3–4.3.5, L3)

**Testing approach:** Attempt to load a model in a code-executing serialization format
(e.g. pickle) and confirm rejection. Test sandbox escape from the inference process. On
mobile/edge targets, extract the app package and attempt to recover usable weights.

---

### C5. Access Control & Identity for AI Components & Users

*Sections: C5.1 Authentication · C5.2 AI Resource Authorization & Classification ·
C5.3 Multi-Tenant Isolation*

- [ ] **Step-up authentication** — Do high-risk AI operations (model deployment, weight export, training data access, production config changes) require step-up authentication? (5.1.1, L3)
- [ ] **Federated agent tokens** — Do agents in federated deployments authenticate with short-lived, minimal-scoped, signed tokens? (5.1.2, L3)
- [ ] **Default-deny on AI resources** — Do datasets, endpoints, vector collections, embedding indices, and compute instances enforce explicit allow-lists and default-deny? (5.2.1, L2)
- [ ] **End-user context in retrieval** — Do RAG queries and embedding lookups enforce the *end user's* authorization at each retrieval and assembly stage, not just the service account's? (5.2.2, L2)
- [ ] **Retrieval over memorization** — Is sensitive data retrieved at query time rather than baked into model weights? (5.2.3, L2)
- [ ] **Post-inference filtering** — Do filters prevent responses containing data the requester is not authorized to receive? (5.2.4, L2)
- [ ] **PDP isolation** — Is the policy decision point for agent authorization isolated from the agent's execution environment? (5.2.5, L2)
- [ ] **Just-in-time privilege** — Is privileged access to weights, pipelines, and production AI config granted just in time with automatic expiry? (5.2.6, L3)
- [ ] **Label propagation** — Do data classification labels propagate to embeddings, prompt caches, and model outputs? (5.2.7, L3)
- [ ] **Tenant isolation in serving** — Does shared serving infrastructure prevent one tenant's fine-tuning, inference, or embedding operations from influencing or observing another's? (5.3.1, L2)
- [ ] **Compute-level tenant isolation** — Is cross-tenant influence via shared compute prevented (hardware partitioning, confidential computing, or dedicated allocation)? (5.3.2, L3)

**Testing approach:** As a low-privilege user, issue RAG queries targeting documents you
cannot read directly and confirm they are not retrieved or surfaced. Test whether the
retrieval service account is the effective principal. In multi-tenant systems, probe shared
prompt/KV caches for another tenant's content.

---

### C6. Supply Chain Security for Models

*Sections: C6.1 Model Artifact Integrity · C6.2 AI BOM & Supply Chain Monitoring*

- [ ] **Malicious code scanning** — Are models scanned for malicious code before import? (6.1.1, L1)
- [ ] **Approved sources** — Are weights, datasets, and adapters downloaded only from approved sources? (6.1.2, L1)
- [ ] **Artifact verification** — Can every third-party model artifact be integrity-verified? (6.1.3, L2)
- [ ] **Behavioral acceptance** — Do models pass a behavioral acceptance test suite before promotion beyond development? (6.1.4, L2)
- [ ] **AI BOM** — Does every model artifact publish a version-controlled, machine-readable AI BOM listing datasets, weights, licenses, and data-origin statements? (6.2.1, L1)
- [ ] **Signed BOM** — Are AI BOMs cryptographically signed before deployment? (6.2.2, L2)
- [ ] **Completeness enforcement** — Do AI BOM completeness checks fail the build on missing component metadata? (6.2.3, L2)

**Testing approach:** Audit where model artifacts are actually pulled from versus the
approved-source list. Scan a representative artifact with a model-security scanner. Verify
the AI BOM against the artifact's real composition, and confirm the build fails on an
intentionally incomplete BOM.

---

### C7. Model Behavior, Output Control & Safety Assurance

*Sections: C7.1 Output Format Enforcement · C7.2 Hallucination Detection & Mitigation ·
C7.3 Output Safety · C7.4 Source Attribution & Citation Integrity*

- [ ] **Schema validation** — Are all model outputs validated against a defined schema, with non-matching output rejected? (7.1.1, L1)
- [ ] **Output bounds** — Is generated output bounded by length limits and termination controls? (7.1.2, L1)
- [ ] **Confidence estimation** — Is answer reliability assessed with a confidence estimation method? (7.2.1, L2)
- [ ] **Low-confidence fallback** — Are answers blocked or replaced with a fallback below a defined confidence threshold? (7.2.2, L2)
- [ ] **High-risk verification** — Do policy-classified high-risk responses get an additional verification step? (7.2.3, L3)
- [ ] **Harmful content blocking** — Do classifiers scan every response and block defined harmful categories? (7.3.1, L1)
- [ ] **Prompt/backend disclosure** — Do output filters block responses disclosing system prompt content or backend data? (7.3.2, L2)
- [ ] **Outbound request prevention** — Is model output prevented from triggering outbound requests? (7.3.3, L2)
- [ ] **Hidden content** — Are outputs checked for hidden or encoded content via homoglyphs, formatting, metadata, or structured fields? (7.3.4, L3)
- [ ] **RAG attribution** — Do RAG responses attribute source documents, with attributions derived from *retrieval metadata* rather than generated by the model? (7.4.1–7.4.2, L1)
- [ ] **Claim traceability** — Can claims in a RAG response be traced to the retrieved chunk? (7.4.3, L2)
- [ ] **Media watermarking** — Is generated media watermarked as AI-generated? (7.4.4, L3)

**Testing approach:** Submit outputs that violate the declared schema and confirm rejection.
Attempt system-prompt extraction and check the output filter. Test exfiltration via
model-generated image URLs or links. Verify citations against the actual retrieved chunks —
in particular whether a citation can be fabricated by the model.

---

### C8. Memory, Embeddings & Vector Database Security

*Sections: C8.1 Access Controls on Memory & RAG Indices · C8.2 Embedding Sanitization &
Validation · C8.3 Memory Expiry & Revocation*

- [ ] **Namespace uniqueness** — Do vector identifiers and namespaces enforce per-tenant uniqueness and prevent cross-tenant collisions? (8.1.1, L1)
- [ ] **Immutable metadata** — Are document metadata tags immutable after initial write? (8.1.2, L2)
- [ ] **Scoped retrieval** — Do retrieval operations enforce scope constraints? (8.1.3, L2)
- [ ] **Pre-embedding masking** — Are sensitive fields detected before embedding and masked, tokenized, or dropped? (8.2.1, L1)
- [ ] **Outlier quarantine** — Are vectors outside normal clustering patterns flagged and quarantined before entering production indices? (8.2.2, L2)
- [ ] **Validated memory writes** — Are agent and tool outputs blocked from automatic writes to trusted memory without explicit source validation? (8.2.3, L2)
- [ ] **Retrieval-manipulation detection** — Is content crafted to manipulate retrieval results rejected or quarantined before vectorization? (8.2.4, L3)
- [ ] **Contradiction checks** — Is new memory content checked for contradictions with stored content, with conflicts alerting? (8.2.5, L3)
- [ ] **Expiry** — Are expired vectors excluded from retrieval results? (8.3.1, L2)
- [ ] **Memory reset** — Can memory be reset? (8.3.2, L2)
- [ ] **Quarantine retention** — Is quarantined content retained but excluded from all retrieval? (8.3.3, L3)

**Testing approach:** Attempt cross-tenant retrieval via crafted identifiers or namespaces.
Poison the index with content engineered to dominate similarity search and confirm detection.
Write attacker-controlled tool output into agent memory and check for source validation.
Delete a document and confirm it is no longer retrievable.

---

### C9. Orchestration & Agentic Security

*Sections: C9.1 Execution Budgets, Loop Control, and Circuit Breakers · C9.2 High-Impact
Action Approval and Irreversibility Controls · C9.3 Component Isolation and Tool
Authorization · C9.4 Agent and Orchestrator Identity · C9.5 Agent Authorization, Delegation,
and Continuous Enforcement · C9.6 Shutdown and Graceful Degradation*

- [ ] **Tool quotas** — Are per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) enforced? (9.1.1, L1)
- [ ] **Execution budgets** — Are per-execution budgets (recursion depth, token use, monetary spend) enforced by the runtime? (9.1.2, L1)
- [ ] **Swarm kill-switch** — Is there a swarm-level kill-switch that halts all active agent instances? (9.1.3, L2)
- [ ] **Approval gate** — Does the runtime block privileged, high-impact, or irreversible actions until explicit human approval is received and verified? (9.2.1, L1)
- [ ] **Faithful approval display** — Do approval requests show canonicalized, complete action parameters without truncation or unsafe transformation? (9.2.2, L2)
- [ ] **Reversibility classification** — Does each high-impact action carry a trusted reversibility classification that the runtime enforces? (9.2.3–9.2.4, L2)
- [ ] **Self-modification bounds** — Are self-modification capabilities (prompt rewriting, tool-list changes, parameter updates) restricted by enforceable boundaries? (9.2.5, L2)
- [ ] **AI review is additive** — Is any AI-augmented pre-execution review *in addition to* — never instead of — the deterministic policy gate, and hardened against prompt injection? (9.2.6–9.2.7, L2)
- [ ] **Bound approvals** — Are approvals cryptographically bound to parameters, requester identity, context, and a single-use nonce, with signing key material isolated from the agent runtime? (9.2.8–9.2.9, L3)
- [ ] **Chain-level gating** — Do approval gates for multi-step or multi-agent chains enforce the highest-impact reversibility class anywhere in the chain? (9.2.10, L3)
- [ ] **Tool sandboxing** — Does each tool/plugin execute in a least-privilege sandbox or is otherwise isolated from model operations? (9.3.1, L1)
- [ ] **Tool output schemas** — Are tool outputs validated against schemas? (9.3.2, L1)
- [ ] **Manifest enforcement** — Do tool manifests declare privileges, resource limits, and output-validation requirements, and does the runtime enforce them? (9.3.3–9.3.4, L2)
- [ ] **Untrusted-data isolation** — Are components processing untrusted data isolated from tool-calling capability, with architectural separation between untrusted tool output and agent operations? (9.3.5–9.3.6, L2)
- [ ] **External resource allow-list** — Are external resources named in model output checked against an approved allow-list before install or invocation? (9.3.7, L2)
- [ ] **Automated containment** — Do policy violations trigger automated tool containment? (9.3.8, L3)
- [ ] **Agent identity** — Does each agent instance have a unique cryptographic identity and authenticate as a first-class principal downstream? (9.4.1, L2)
- [ ] **Non-repudiation** — Are agent-initiated actions cryptographically bound to each step of the execution chain? (9.4.2, L2)
- [ ] **Credential rotation and state integrity** — Do agent credentials rotate on a schedule, and is persisted agent state integrity-protected? (9.4.3–9.4.4, L3)
- [ ] **Fine-grained authorization** — Are agent actions authorized against runtime-enforced policies restricting which tools *and which parameter values* the agent may use? (9.5.1, L2)
- [ ] **Delegated user context** — Is an integrity-protected, scope-limited token carrying the user's authorization context propagated and enforced at every downstream call? (9.5.2, L2)
- [ ] **No model-made access decisions** — Are all access control decisions made by application logic or a policy engine, never the model? (9.5.3, L2)
- [ ] **Secrets outside context** — Are runtime secrets kept out of the context window, system prompts, and tool call parameters? (9.5.4, L2)
- [ ] **Delegation policy** — Is inter-agent task delegation restricted by explicit authorization policy? (9.5.5, L2)
- [ ] **Continuous enforcement** — Do long-running sessions re-evaluate backend authorization on every privileged action? (9.5.6, L3)
- [ ] **Inference kill-switch** — Does a manual kill-switch immediately halt model inference and output? (9.6.1, L1)
- [ ] **Fail-closed approval timeout** — When a human-approval gate is not satisfied in time, does the system *block* the pending action? (9.6.2, L2)
- [ ] **Out-of-band shutdown** — Are kill-switch commands delivered over a channel isolated from the agent runtime? (9.6.3, L3)

**Testing approach:** Drive the agent into a recursive loop and confirm budgets halt it.
Attempt a high-impact action and check that the gate is deterministic — try to talk the agent
past an LLM-based reviewer with injected content. Inspect whether approval prompts display
the real, untruncated parameters. Enumerate tool scopes against what each tool actually
needs. Grep the context window and tool arguments for credentials. Let an approval deadline
lapse and confirm fail-closed behavior.

---

### C10. Model Context Protocol (MCP) Security

*Sections: C10.1 Component Integrity · C10.2 Authentication & Authorization ·
C10.3 Secure Transport · C10.4 Schema, Message, and Input Validation*

- [ ] **Trusted MCP sources** — Are MCP components obtained only from trusted sources and cryptographically verified? (10.1.1, L1)
- [ ] **Server allow-list** — Are only allow-listed MCP servers permitted? (10.1.2, L2)
- [ ] **Local server sandbox** — Do locally launched MCP servers run in a least-privilege sandbox with restricted filesystem, network, and system access? (10.1.3, L2)
- [ ] **Per-request token validation** — Do MCP servers validate access tokens on every request rather than relying on transport security? (10.2.1, L1)
- [ ] **Claim validation** — Are issuer, audience, expiration, and scope claims validated per OAuth 2.1? (10.2.2, L1)
- [ ] **No token persistence** — Do MCP servers acting as OAuth 2.1 resource servers avoid storing or persisting tokens and credentials? (10.2.3, L1)
- [ ] **Scoped tool listing** — Does `tools/list` return only tools permitted by the resource owner's authorized scopes? (10.2.4, L2)
- [ ] **Per-invocation authorization** — Is access control enforced on every tool invocation, validating both the tool *and the specific argument values*? (10.2.5, L2)
- [ ] **Session cleanup** — Are all session artifacts removed at session termination? (10.2.6, L2)
- [ ] **No token pass-through** — Are client-supplied access tokens kept from being passed through to downstream APIs? (10.2.7, L2)
- [ ] **Transport security** — Is authenticated, encrypted streamable HTTP used for remote MCP, with stdio limited to controlled local environments? (10.3.1–10.3.2, L1)
- [ ] **Origin and Host validation** — Are Origin and Host headers validated independently on all HTTP transports to prevent DNS rebinding? (10.3.3, L2)
- [ ] **Version floor** — Do MCP clients enforce a minimum protocol version and reject lower proposals in `initialize` responses? (10.3.4, L2)
- [ ] **Sender-constrained tokens** — Are tokens sender-constrained with mTLS or DPoP? (10.3.5, L3)
- [ ] **Response schema validation** — Are `tools/list` and `tools/call` responses validated against declared schemas before entering the model context? (10.4.1, L1)
- [ ] **Injection screening on responses** — Are those responses screened for indirect prompt injection before entering the context? (10.4.2, L1)
- [ ] **Parameter hygiene** — Do servers reject unrecognized or oversized parameters, enforce strict schema validation, and enforce maximum payload sizes? (10.4.3–10.4.5, L1–L2)
- [ ] **Replay detection** — Are tool responses signed with a unique nonce and timestamp so clients can detect replay? (10.4.6, L2)
- [ ] **Install consent** — Do clients present explicit consent and cancellation on local MCP server installation? (10.4.7, L2)
- [ ] **Rug-pull protection** — Do clients snapshot tool definitions and require re-approval when a definition changes? (10.4.8, L3)

**Testing approach:** Enumerate configured MCP servers against the allow-list. Call a tool
with a token whose scope covers a different tool or different argument values. Attempt DNS
rebinding against a locally bound server. Plant injection text inside a tool description and
confirm it is screened before reaching the model. Change a tool definition post-approval and
verify re-approval is demanded.

---

### C11. Adversarial Robustness

*Sections: C11.1 Model Alignment, Safety, and Robustness Testing and Training ·
C11.2 Membership-Inference and Model-Inversion Mitigation · C11.3 Model-Extraction Defense ·
C11.4 Model Runtime Anomaly Detection*

- [ ] **Alignment training** — Has the model undergone alignment/safety training to prevent disallowed content categories? (11.1.1, L1)
- [ ] **Alignment test suite** — Is a version-controlled alignment test suite run on every model update or release? (11.1.2, L1)
- [ ] **Modality-relevant adversarial evaluation** — Are models evaluated against known adversarial techniques for their modality? (11.1.3, L1)
- [ ] **Adversarial hardening** — Are models hardened against adversarial inputs? (11.1.4, L2)
- [ ] **Regression detection** — Does an automated evaluator measure harmful-content rate and flag regressions past a threshold? (11.1.5, L3)
- [ ] **Sensitive attribute suppression** — Are model-inferred sensitive attributes kept out of outputs? (11.2.1, L1)
- [ ] **Extraction-sized rate limits** — Do inference endpoints enforce per-principal and global rate limits sized to the *extraction threat model*, not just generic API throttling? (11.2.2, L1)
- [ ] **Output calibration** — Are outputs calibrated to reduce overconfident predictions? (11.2.3, L2)
- [ ] **Differential privacy** — Does training on sensitive datasets use differentially-private optimization? (11.2.4, L2)
- [ ] **Membership-inference simulation** — Do simulations show attack accuracy no better than random guessing? (11.2.5, L3)
- [ ] **Extraction detection** — Does query-pattern analysis feed an extraction-attempt detector? (11.3.1, L1)
- [ ] **Raw output exposure** — Are raw model outputs kept behind the application backend, with external responses calibrated to extraction risk? (11.3.2, L2)
- [ ] **Watermarking** — Are watermarking or fingerprinting techniques applied so unauthorized copies can be identified? (11.3.3, L3)
- [ ] **Extraction response** — Does suspected extraction trigger response measures? (11.3.4, L3)
- [ ] **Pre-inference anomaly detection** — Do inputs from external or untrusted sources pass anomaly detection before inference, with flagged inputs triggering gating actions? (11.4.1–11.4.2, L2)
- [ ] **Feedback-loop protection** — Does the safety-violation feedback pipeline include poisoning detection and human review gates? (11.4.3, L3)

**Testing approach:** Run the alignment suite and compare against the recorded baseline.
Generate adversarial examples for each supported modality. Issue a high-volume systematic
query campaign and check whether extraction detection fires and what response follows. Test
whether flagged anomalous inputs are actually gated or merely logged.

---

### C12. Monitoring, Logging & Anomaly Detection

*Sections: C12.1 Request & Response Logging · C12.2 Detection and Alerting ·
C12.3 Model, Data, and Performance Drift Detection · C12.4 Proactive Security Behavior
Monitoring · C12.5 Training Data & Model Lifecycle Audit*

- [ ] **Interaction logging** — Are AI interactions logged with session context and AI-specific telemetry? (12.1.1, L1)
- [ ] **Policy decision logging** — Are safety filtering and policy decisions logged in enough detail for audit, debugging, and forensics? (12.1.2, L2)
- [ ] **Structured inference schema** — Do inference log entries follow a structured schema including model identifier, input/output token usage, provider, and operation type? (12.1.3, L2)
- [ ] **RAG retrieval logging** — Are retrieval events logged with query, documents retrieved, and knowledge source? (12.1.4, L2)
- [ ] **Attack detection** — Does the system detect and alert on known jailbreak patterns, prompt injection attempts, and adversarial inputs? (12.2.1, L1)
- [ ] **Behavioral anomaly detection** — Are unusual conversation patterns, excessive retries, and probing behaviors identified? (12.2.2, L2)
- [ ] **AI-specific rules** — Do custom rules cover coordinated jailbreaks, injection, and system-prompt extraction? (12.2.3, L2)
- [ ] **Alert enrichment** — Do extraction alerts include offending query metadata? (12.2.4, L2)
- [ ] **Token attribution** — Is token usage tracked per user, session, feature endpoint, and team/workspace? (12.2.5, L2)
- [ ] **Covert channel monitoring** — Is LLM API traffic monitored for covert-channel and C2 signatures? (12.2.6, L3)
- [ ] **Data drift** — Does drift detection use statistically validated methods matched to the input type (KS/PSI for tabular, embedding-distance for text/image)? (12.3.1, L1)
- [ ] **Hallucination monitoring** — Are hallucinated outputs flagged and rates tracked as time-series metrics for trend analysis? (12.3.2–12.3.3, L2)
- [ ] **Shift attribution** — Are unexplained behavioral shifts distinguished from expected operational drift? (12.3.4, L3)
- [ ] **Proactive action evaluation** — Do autonomous action triggers include behavior-pattern analysis, security evaluation, and threat-landscape assessment? (12.4.1, L2)
- [ ] **Approval audit trail** — Do audit logs capture security-critical proactive actions with approver identity, timestamp, parameters, and outcome? (12.4.2, L2)
- [ ] **Emergency control logging** — Are kill-switch activations and override commands logged? (12.4.3, L2)
- [ ] **Dataset lineage** — Does lineage record each dataset and its transformations, augmentations, and merges, with all labeling activity logged? (12.5.1–12.5.2, L1)
- [ ] **Immutable model change records** — Do all model changes generate immutable audit records? (12.5.3, L2)
- [ ] **Write-time document tagging** — Is every ingested document tagged with source, writer identity, and timestamp? (12.5.4, L2)

**Testing approach:** Execute a known jailbreak and confirm it is detected, alerted, and
logged with usable context. Reconstruct a full session from logs alone. Verify log
immutability and retention. Check that a RAG retrieval of a poisoned document leaves a
traceable record including source and writer.

---

## Risk Prioritization Matrix

Prioritize findings by severity, impact, and the deployment context of the system:

| AISVS chapter | Example finding | Severity | Impact | Priority |
|---------------|----------------|----------|--------|----------|
| C2 Input Validation | Prompt injection reaches tool-calling agent | High | High | Critical |
| C9 Orchestration & Agentic | Irreversible action executes without approval gate | High | High | Critical |
| C10 MCP Security | MCP server passes client token through to downstream API | High | High | Critical |
| C5 Access Control | RAG retrieval uses service account rather than end-user context | High | High | Critical |
| C8 Memory & Embeddings | Tool output written to trusted memory unvalidated | High | Medium | High |
| C6 Supply Chain | Unverified third-party model imported | Medium | High | High |
| C7 Output Control | No schema validation on model output | Medium | Medium | Medium |
| C12 Monitoring | No AI-specific logging or detection | Low | Medium | Medium |

## Output Format

```markdown
## AI Security Verification Assessment: [Application Name]

### Executive Summary
- **AISVS version**: v1.0 (June 2026)
- **Target verification level**: [L1 / L2 / L3]
- **Overall compliance**: [X/12 chapters fully compliant at target level]
- **Requirements assessed**: [X of 191 in scope]
- **Critical findings**: [Number of critical security gaps]
- **Compliance status**: [Ready / Not ready for production]

### Chapter Assessment

#### C1. Training Data Integrity & Traceability
- **Status**: [Compliant / Partial / Non-Compliant / N/A]
- **Requirements in scope**: [e.g. 1.1.1–1.3.4 at L2]
- **Key findings**: [Summary, citing requirement IDs]
- **Recommendations**: [Priority actions]

[Repeat for C2–C12]

### Critical Security Gaps
[High-priority findings requiring immediate attention, each citing its AISVS requirement ID]

### Compliance Roadmap
[Structured plan to reach the target verification level]

### Verification Evidence
[Documentation, test output, and configuration supporting each compliance claim]

### Risk Assessment
[Overall risk rating and justification]
```

Individual findings use the structure in `templates/finding.md`, with the **OWASP Ref** field
carrying the AISVS requirement ID (e.g. `AISVS v1.0 C9.2.1`).

## Notes on N/A Chapters

Not every chapter applies to every system. Mark **N/A** with justification rather than
omitting:

- **C1, C3.5** — N/A for systems consuming only third-party hosted models with no training or fine-tuning.
- **C4.2, C4.3** — N/A without self-managed accelerators or edge/on-device deployment.
- **C8** — N/A without RAG, embeddings, or persistent agent memory.
- **C9** — N/A for non-agentic systems with no tool calling.
- **C10** — N/A when MCP is not in use.
- **C11.2–C11.3** — N/A for systems that do not train models and do not expose inference endpoints externally.

## OWASP References

- **OWASP AI Security Verification Standard (AISVS) v1.0** — [github.com/OWASP/AISVS](https://github.com/OWASP/AISVS)
- OWASP Top 10 for LLM Applications 2025
- OWASP Top 10 for Agentic Applications 2026
- OWASP Agentic AI Threats and Mitigations
- OWASP MCP Security Cheat Sheet
- OWASP AI Testing Guide
- OWASP Application Security Verification Standard (ASVS)
