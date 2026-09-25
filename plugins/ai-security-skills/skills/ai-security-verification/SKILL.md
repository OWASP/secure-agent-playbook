---
name: ai-security-verification
description: Comprehensive AI security verification using OWASP AI Security Verification Standard (AISVS) framework. Use when verifying an AI-driven application, ML pipeline, or LLM-integrated system against AISVS, preparing for an AI security audit, or checking security and ethical controls across 13 categories from training data governance to human oversight.
license: CC-BY-4.0
---

# AI Security Verification Standard (AISVS)

Conduct comprehensive security verification of AI-driven applications using the OWASP AI Security Verification Standard (AISVS) framework's 13-category structured checklist. Follow the full procedure in `plays/ai-security-verification.md`.

## Steps

1. **Training Data Governance & Bias Management** — Assess data quality, provenance, bias detection, and governance controls throughout the data lifecycle.

2. **User Input Validation** — Evaluate input sanitization, prompt injection defenses, adversarial input detection, and boundary validation mechanisms.

3. **Model Lifecycle Management & Change Control** — Review model versioning, deployment controls, rollback capabilities, and change management processes.

4. **Infrastructure, Configuration & Deployment Security** — Examine deployment security, container hardening, network controls, and infrastructure configuration.

5. **Access Control & Identity** — Verify authentication mechanisms, authorization controls, privilege management, and identity governance.

6. **Supply Chain Security for Models, Frameworks & Data** — Assess third-party model security, dependency management, and supply chain integrity.

7. **Model Behavior, Output Control & Safety Assurance** — Evaluate output validation, safety guardrails, behavior monitoring, and harmful content prevention.

8. **Memory, Embeddings & Vector Database Security** — Review vector database security, embedding protection, memory isolation, and context management.

9. **Autonomous Orchestration & Agentic Action Security** — Assess agent coordination security, tool access controls, and autonomous decision-making safeguards.

10. **Adversarial Robustness & Attack Resistance** — Test resilience against adversarial examples, evasion attacks, and model extraction attempts.

11. **Privacy Protection & Personal Data Management** — Verify privacy controls, data minimization, consent management, and regulatory compliance.

12. **Monitoring, Logging & Anomaly Detection** — Evaluate security monitoring, audit logging, anomaly detection, and incident response capabilities.

13. **Human Oversight and Trust** — Assess human-in-the-loop controls, explainability mechanisms, and trust calibration measures.

## Output

Use the finding format from `templates/finding.md`. Produce:
- **AISVS Compliance Assessment** — Verification status across all 13 categories
- **Security Control Evaluation** — Detailed analysis of implemented controls
- **Gap Analysis** — Missing or inadequate security measures
- **Risk-Based Prioritization** — Critical findings requiring immediate attention
- **Compliance Roadmap** — Structured plan to achieve AISVS compliance
- **Verification Evidence** — Documentation supporting compliance claims

## OWASP References

- **OWASP AI Security Verification Standard (AISVS)**
- OWASP Top 10 for LLM Applications 2025
- OWASP AI Security and Privacy Guide
- OWASP Application Security Verification Standard (ASVS)
- OWASP AI Testing Guide
- Full procedure: `plays/ai-security-verification.md`
