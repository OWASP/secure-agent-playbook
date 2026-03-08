---
name: iac-security-review
description: Security review of Infrastructure-as-Code (Terraform, Kubernetes, CloudFormation). Use when reviewing IaC files for misconfigurations, overpermissioning, exposed resources, missing encryption, secrets in code, and supply chain risks. Covers CIS benchmarks and cloud security best practices.
license: CC-BY-4.0
---

# IaC Security Review

Review infrastructure-as-code for security risks by following the full procedure in `plays/tier1-code-analysis/iac-security-review.md`.

## Steps

1. **Detect IaC Type** — Identify the infrastructure technology from file extensions and content:
   - `.tf` / `.tofu` files → Terraform/OpenTofu (reference `data/secure-code-prompts/terraform.md`)
   - Kubernetes manifests (apiVersion, kind: Deployment/Pod/Service) → Kubernetes (reference `data/secure-code-prompts/kubernetes.md`)
   - CloudFormation templates (AWSTemplateFormatVersion, Resources with AWS::) → CloudFormation (reference `data/secure-code-prompts/cloudformation.md`)
   - Helm charts (`Chart.yaml`, templates/) → Kubernetes review with Helm-specific checks

2. **Systematic Review by Security Domain** (priority order):
   - **Identity & Access Management** — Overly permissive policies, wildcard permissions, hardcoded credentials, privilege escalation paths
   - **Secrets Management** — Hardcoded secrets, plaintext credentials, missing vault/secret manager integration
   - **Network Security** — Open ingress (`0.0.0.0/0`), unrestricted ports, missing segmentation, public exposure
   - **Encryption** — Missing encryption at rest/in transit, weak algorithms, default keys
   - **Storage Security** — Public buckets, unencrypted volumes, missing versioning
   - **Logging & Monitoring** — Missing audit trails, disabled CloudTrail/audit logging
   - **Resource Exposure** — Databases, admin interfaces, APIs exposed to internet
   - **Supply Chain** — Unpinned versions, untrusted sources, unverified modules/images
   - **Platform-Specific Risks** — Terraform state exposure, K8s privileged containers, CFN nested stack integrity

3. **Check Against Benchmarks** — Validate configurations against:
   - CIS Benchmarks (AWS/Azure/GCP/Kubernetes)
   - Cloud provider security best practices
   - Pod Security Standards (for Kubernetes)

4. **Produce Findings** — For each finding: cite resource path, explain the misconfiguration, describe attack scenario, provide fixed code example, rate severity.

## Output

Findings sorted by severity using `templates/finding.md` format, summary with severity counts, and secure configuration improvements section.

## References

- CIS Benchmarks (AWS, Azure, GCP, Kubernetes)
- OWASP Infrastructure Security Cheat Sheet
- NSA/CISA Kubernetes Hardening Guide
- Cloud provider Well-Architected Frameworks
