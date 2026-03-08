---
title: "Kubernetes Security Review"
domain: "infrastructure"
when_to_use:
  - reviewing Kubernetes manifests or Helm charts
  - auditing cluster configurations for security risks
  - assessing pod security, RBAC, and network policies
  - evaluating container images and supply chain integrity
threats:
  - containers running as root or with privileged access
  - unpinned or unverified container images
  - secrets stored in plain text in manifests
  - overly broad RBAC permissions and cluster-admin usage
  - missing network policies allowing unrestricted pod communication
  - sensitive host path mounts enabling container escape
summary: "Security review checklist for Kubernetes manifests and cluster configurations covering pod security, image security, secrets, RBAC, networking, resource constraints, volume mounts, logging, supply chain, and service exposure."
owasp_references: ["A01:2021", "A02:2021", "A05:2021", "A06:2021"]
---

# Kubernetes Security Review

Review Kubernetes configuration files for security risks, insecure patterns, and misconfigurations.

## 1. Pod Security Configuration

Check whether containers:
- Run as root
- Lack `runAsNonRoot`
- Allow privilege escalation
- Run in `privileged: true` mode
- Mount sensitive host paths
- Use `hostNetwork`, `hostPID`, or `hostIPC`
- Lack seccomp profiles
- Lack AppArmor or SELinux policies

Recommend secure `securityContext` configurations.

## 2. Container Image Security

Check for:
- Images using `latest` tag
- Unpinned image versions
- Images from untrusted registries
- Lack of image provenance verification
- Containers running outdated base images

Recommend pinned versions and trusted registries.

## 3. Secrets Management

Identify:
- Secrets stored in plain text in manifests
- Secrets embedded directly in environment variables
- ConfigMaps used for sensitive data
- Missing integration with secret management systems (Vault, External Secrets Operator, etc.)

## 4. RBAC and Permissions

Review Role, ClusterRole, RoleBinding, and ClusterRoleBinding definitions.

Check for:
- Wildcard permissions (`*`)
- Overly broad `cluster-admin` privileges
- Roles applied at cluster scope unnecessarily
- Service accounts with excessive privileges

Recommend least privilege RBAC policies.

## 5. Network Security

Analyze Services, NetworkPolicies, and Ingress configurations.

Identify:
- Missing NetworkPolicies
- Pods exposed without restrictions
- Services exposed externally unnecessarily
- Public LoadBalancers exposing internal services
- Ingress rules allowing unrestricted access

Recommend proper network segmentation and policies.

## 6. Resource Constraints

Check for missing resource constraints:
- CPU limits
- Memory limits
- Resource requests

Missing constraints can allow denial-of-service conditions or cluster instability.

## 7. Sensitive Volume Mounts

Identify containers mounting:
- Docker socket paths
- `/etc` directories
- `/proc` filesystem
- Host filesystem paths

These mounts can allow container escape or host compromise.

## 8. Logging and Monitoring

Check whether workloads support:
- Centralized logging
- Security event monitoring
- Audit logging

Recommend enabling Kubernetes audit logging and observability tools.

## 9. Supply Chain Risks

Identify:
- Helm charts from unverified sources
- Containers without vulnerability scanning
- Unpinned Helm chart versions
- Untrusted container registries

Recommend secure supply chain practices.

## 10. Service Exposure Risks

Identify publicly exposed services that could expose sensitive systems:
- Databases
- Internal APIs
- Admin dashboards
- Message queues

Recommend internal-only networking where appropriate.

## Output Format

For each finding:
- **Severity**: Critical / High / Medium / Low
- **Resource**: Kubernetes resource affected
- **Issue**: Description of the security problem
- **Impact**: Why this is dangerous
- **Recommendation**: How to fix it
- **Example Fix**: Suggested Kubernetes configuration improvement

## Guidance & Reference Sources

- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
- [OWASP Kubernetes Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
- [Pod Security Standards (PSS)](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
