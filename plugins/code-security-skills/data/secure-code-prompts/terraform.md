---
title: "Terraform Security Review"
domain: "infrastructure"
when_to_use:
  - reviewing Terraform or OpenTofu configurations
  - auditing cloud infrastructure-as-code for misconfigurations
  - assessing IaC before deployment for security risks
  - evaluating Terraform modules from third-party sources
threats:
  - overly permissive IAM policies and wildcard permissions
  - hardcoded credentials or secrets in Terraform variables
  - publicly exposed services via open security groups
  - unencrypted storage and data at rest
  - unsafe module sources and unpinned provider versions
  - state file exposure revealing secrets
summary: "Security review checklist for Terraform infrastructure code covering IAM, secrets, networking, storage, encryption, logging, resource exposure, Terraform-specific risks, supply chain, and abuse prevention."
owasp_references: ["A01:2021", "A02:2021", "A05:2021", "A09:2021"]
---

# Terraform Security Review

Review Terraform configurations for security risks, misconfigurations, and insecure patterns.

## 1. Identity and Access Management

Check for:
- Overly permissive IAM policies
- Wildcard permissions (`*`)
- Lack of least privilege
- Hardcoded credentials or access keys
- Publicly assumable roles
- Improper trust relationships

## 2. Secrets Management

Identify:
- Hardcoded secrets
- Tokens or API keys in Terraform variables
- Secrets stored in plain text
- Secrets passed via environment variables insecurely
- Missing use of secret managers (Vault, AWS Secrets Manager, etc.)

## 3. Network Security

Review:
- Publicly exposed services
- Security groups with open ingress rules (e.g., `0.0.0.0/0`)
- Unrestricted ports such as SSH (22), RDP (3389), databases
- Missing network segmentation
- Missing private networking for sensitive resources

## 4. Storage Security

Check whether storage resources:
- Allow public access
- Lack encryption at rest
- Lack versioning or backup protections
- Allow insecure transport

## 5. Encryption

Verify that:
- Encryption at rest is enabled
- Encryption in transit is enforced
- Managed keys or KMS services are used
- Sensitive resources do not use default or weak encryption settings

## 6. Logging and Monitoring

Check whether:
- Logging is enabled for critical services
- Audit logs are configured
- Monitoring alerts exist for security events

## 7. Resource Exposure

Identify resources that may expose sensitive services to the internet:
- Databases
- Internal APIs
- Message queues
- Admin interfaces

## 8. Terraform-Specific Risks

Check for:
- Use of `terraform state` that may expose secrets
- Sensitive variables not marked `sensitive = true`
- Lack of remote state encryption
- Remote state without locking
- Unsafe module sources
- Unpinned module or provider versions
- Use of untrusted modules

## 9. Supply Chain Risks

Identify:
- Unpinned provider versions
- External modules without version constraints
- Modules from unverified sources

## 10. Cost and Abuse Risks

Flag configurations that could allow:
- Resource abuse
- Crypto mining infrastructure
- Unlimited scaling without guardrails

## Output Format

For each finding:
- **Severity**: Critical / High / Medium / Low
- **Resource**: Terraform resource affected
- **Issue**: Description of the security problem
- **Impact**: Why this is dangerous
- **Recommendation**: How to fix it
- **Example Fix**: Suggested Terraform code improvement

## References

- [CIS Benchmark for AWS/Azure/GCP](https://www.cisecurity.org/cis-benchmarks)
- [OWASP Infrastructure Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html)
- [Terraform Security Best Practices — HashiCorp](https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices)
