# IaC Security Review

Security review procedure for Infrastructure-as-Code configurations including Terraform, Kubernetes manifests, and AWS CloudFormation templates.

## Trigger Conditions

- Reviewing `.tf`, `.tofu` files (Terraform/OpenTofu)
- Reviewing Kubernetes YAML manifests or Helm charts
- Reviewing CloudFormation YAML/JSON templates
- Pre-deployment security gate for infrastructure changes
- Auditing cloud infrastructure configurations

## Prerequisites

- Access to IaC files under review
- Understanding of target cloud provider (AWS, Azure, GCP)
- Optional: `tfsec`, `checkov`, `trivy config`, `kube-linter`, `cfn-nag` for automated scanning

## Procedure

### Phase 1: Scope & Context

Establish:
- **IaC technology**: Terraform, Kubernetes, CloudFormation, Helm, or mixed
- **Target environment**: Production, staging, development
- **Cloud provider**: AWS, Azure, GCP, multi-cloud
- **Sensitivity**: What data/services does this infrastructure support?
- **Compliance**: Any regulatory requirements (SOC2, HIPAA, PCI-DSS)?

### Phase 2: Automated Scanning (if tools available)

Run available scanners first to catch low-hanging fruit:

```bash
# Terraform
tfsec .                          # Static analysis for Terraform
checkov -d .                     # Policy-as-code scanning
trivy config .                   # Misconfiguration scanning

# Kubernetes
kube-linter lint .               # Kubernetes manifest linting
trivy config .                   # Misconfiguration scanning
kubesec scan manifest.yaml       # Security risk scoring

# CloudFormation
cfn-lint template.yaml           # CloudFormation linting
cfn_nag_scan --input-path .      # Security-focused scanning
checkov -d .                     # Policy-as-code scanning
```

### Phase 3: Manual Review by Security Domain

Review each domain systematically. Reference the corresponding prompt data file for the detected IaC type:
- Terraform → `data/secure-code-prompts/terraform.md`
- Kubernetes → `data/secure-code-prompts/kubernetes.md`
- CloudFormation → `data/secure-code-prompts/cloudformation.md`

#### 3.1 Identity & Access Management

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| Least privilege | `aws_iam_policy` wildcards | RBAC ClusterRole wildcards | `AWS::IAM::Policy` wildcards |
| No hardcoded creds | Variables, provider blocks | ServiceAccount tokens | Parameters, UserData |
| Role scoping | Trust relationships | Namespace-scoped roles | AssumeRolePolicyDocument |
| Separation of duties | Separate roles per function | Separate ServiceAccounts | Separate IAM roles |

#### 3.2 Secrets Management

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| No plaintext secrets | `sensitive = true`, no defaults | No secrets in manifests | No secrets in Parameters |
| External secret store | Vault provider, AWS SM data source | External Secrets Operator | Secrets Manager references |
| No secrets in state | Remote encrypted state | No ConfigMaps for secrets | No secrets in Outputs |

#### 3.3 Network Security

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| No open ingress | Security group `0.0.0.0/0` | NetworkPolicy exists | SecurityGroup `0.0.0.0/0` |
| Restricted ports | SSH/RDP not world-open | Services not NodePort/LB unnecessarily | No unrestricted SSH/RDP |
| Private networking | Private subnets for sensitive resources | Internal ClusterIP default | VPC private subnets |
| Segmentation | Separate VPCs/subnets | NetworkPolicies per namespace | Network ACLs |

#### 3.4 Encryption

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| At rest | `encrypted = true` on storage | etcd encryption, PV encryption | `StorageEncrypted: true` |
| In transit | TLS on load balancers | TLS on Ingress, mTLS between services | HTTPS listeners |
| Key management | KMS key references | Secrets encryption config | KMS key references |

#### 3.5 Storage Security

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| No public access | S3 `block_public_access` | PV access modes | S3 `PublicAccessBlockConfiguration` |
| Versioning | `versioning { enabled = true }` | N/A | `VersioningConfiguration` |
| Backup | Lifecycle rules, snapshots | PV reclaim policies | Backup retention |

#### 3.6 Logging & Monitoring

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| Audit logging | CloudTrail, Flow Logs enabled | Audit policy configured | CloudTrail resource exists |
| Access logging | S3 access logs, ALB logs | Pod logging to aggregator | S3/ALB access logging |
| Alerting | CloudWatch alarms | Prometheus/alerting rules | CloudWatch Alarms |

#### 3.7 Resource Exposure

Check for databases, admin interfaces, message queues, or internal APIs exposed to the public internet. Recommend private networking and access restrictions.

#### 3.8 Supply Chain

| Check | Terraform | Kubernetes | CloudFormation |
|-------|-----------|------------|----------------|
| Pinned versions | Provider/module version constraints | Image tags (not `latest`) | Template version tracking |
| Trusted sources | Terraform Registry, verified modules | Trusted registries only | Verified nested stacks |
| Integrity | Module hashes in lockfile | Image digest pinning | Template validation |

#### 3.9 Platform-Specific Risks

**Terraform:**
- State file contains secrets → ensure remote + encrypted + locked
- `sensitive = true` on all secret variables
- Module sources pinned to specific versions

**Kubernetes:**
- `privileged: true` containers → almost never needed
- `runAsNonRoot: true` and `allowPrivilegeEscalation: false`
- No host path mounts to sensitive directories
- Resource limits set to prevent DoS

**CloudFormation:**
- No secrets in Outputs (visible in console)
- Nested stacks from trusted sources only
- Stack policies to prevent accidental deletion

### Phase 4: Produce Findings

For each finding, use the standard output format:

```markdown
### [SEVERITY] Title
- **Resource**: resource type and identifier
- **Issue**: Description of the misconfiguration
- **Impact**: What an attacker can achieve
- **Recommendation**: How to fix it
- **Example Fix**: Corrected IaC code snippet
```

### Phase 5: Summary

Provide:
- Total findings by severity (Critical / High / Medium / Low)
- Most critical risks to address first
- General recommendations for improving infrastructure security posture
- Suggested tooling for ongoing automated checks

## Benchmark References

| Benchmark | Applies To |
|-----------|-----------|
| CIS AWS Foundations | Terraform (AWS), CloudFormation |
| CIS Azure Foundations | Terraform (Azure) |
| CIS GCP Foundations | Terraform (GCP) |
| CIS Kubernetes | Kubernetes manifests |
| NSA/CISA K8s Hardening | Kubernetes clusters |
| AWS Well-Architected (Security) | CloudFormation, Terraform (AWS) |
| Pod Security Standards | Kubernetes pods |
