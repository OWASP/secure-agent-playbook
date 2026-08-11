---
title: "AWS CloudFormation Security Review"
domain: "infrastructure"
when_to_use:
  - reviewing AWS CloudFormation templates
  - auditing AWS infrastructure definitions for security risks
  - assessing nested stacks and cross-stack references
  - evaluating CloudFormation before deployment
threats:
  - overly permissive IAM policies with wildcard permissions
  - plaintext credentials in parameters or environment variables
  - open security groups and unrestricted network access
  - unencrypted S3 buckets, EBS volumes, and databases
  - missing CloudTrail, VPC Flow Logs, and audit logging
  - publicly exposed EC2 instances, databases, and admin interfaces
summary: "Security review checklist for AWS CloudFormation templates covering IAM, secrets, networking, storage, encryption, logging, public exposure, resource hardening, infrastructure misconfiguration, and supply chain integrity."
owasp_references: ["A01:2021", "A02:2021", "A05:2021", "A09:2021"]
---

# AWS CloudFormation Security Review

Review CloudFormation templates for security risks, insecure configurations, and potential misconfigurations.

## 1. Identity and Access Management (IAM)

Review IAM resources including Roles, Policies, Instance Profiles, and Service Roles.

Check for:
- Overly permissive policies (`Action: "*"`)
- Wildcard resources (`Resource: "*"`)
- Excessive administrative privileges
- Roles assumable by unintended principals
- Missing separation of duties

Recommend least privilege IAM policies.

## 2. Secrets and Sensitive Data

Identify whether the template:
- Embeds secrets directly in parameters
- Stores credentials in plaintext
- Exposes API keys or access tokens
- Stores secrets in environment variables without secure handling

Recommend using AWS Secrets Manager, SSM Parameter Store, or encrypted parameters.

## 3. Network Security

Review Security Groups, Network ACLs, Load Balancers, and VPC configuration.

Check for:
- Open ingress rules (`0.0.0.0/0`)
- Publicly accessible databases
- Unrestricted SSH or RDP access
- Internal services exposed to the internet
- Missing network segmentation

## 4. Storage Security

Review S3 buckets, EBS volumes, EFS, and RDS storage.

Check whether:
- S3 buckets allow public access
- Encryption at rest is disabled
- Versioning is missing
- Public read/write access is enabled

## 5. Encryption

Verify encryption for sensitive resources (S3, RDS, EBS, SQS, SNS):
- Encryption at rest is enabled
- Customer-managed keys (KMS) are used when appropriate
- Encryption in transit is enforced

## 6. Logging and Monitoring

Check whether the template enables:
- CloudTrail
- CloudWatch Logs
- VPC Flow Logs
- S3 access logging

Identify missing logging controls that could prevent detection of security incidents.

## 7. Public Resource Exposure

Identify resources exposed to the public internet:
- EC2 instances
- Load balancers
- Databases
- Admin interfaces
- Management APIs

Evaluate whether exposure is necessary and recommend limiting access.

## 8. Resource Hardening

Check whether compute resources are hardened (EC2, containers, Lambda):
- Overly permissive instance roles
- Outdated AMIs
- Lack of runtime restrictions
- Missing patch management practices

## 9. Infrastructure Misconfiguration

Identify general infrastructure risks:
- Insecure defaults
- Lack of network isolation
- Missing resource limits
- Lack of tagging or environment separation

## 10. Supply Chain and Template Integrity

Check for:
- Templates pulled from untrusted sources
- Unverified nested stacks
- Lack of template validation or scanning
- Deployment pipelines lacking security checks

## Output Format

For each finding:
- **Severity**: Critical / High / Medium / Low
- **Resource**: CloudFormation resource affected
- **Issue**: Description of the security problem
- **Impact**: Why this is dangerous
- **Recommendation**: How to fix it
- **Example Fix**: Suggested CloudFormation configuration improvement

## Guidance & Reference Sources

- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [AWS Well-Architected Framework — Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) and [cfn-nag](https://github.com/stelligent/cfn_nag)
