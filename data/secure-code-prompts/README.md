# Secure Code Prompts — Reference Data

Structured security prompt data sourced from the [SecCodePrompts](https://github.com/theJonMccoy/SecCodePrompts) community project and adapted into the playbook's YAML frontmatter format.

## Source & License

Original prompts by [theJonMccoy/SecCodePrompts](https://github.com/theJonMccoy/SecCodePrompts), licensed under [MIT](https://opensource.org/licenses/MIT). Adapted with OWASP standard mappings and structured metadata.

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "Terraform Security Review"
domain: "infrastructure"       # infrastructure | design | coding
when_to_use:
  - reviewing Terraform configurations
threats:
  - overly permissive IAM policies
summary: "Brief description."
owasp_references: ["A01:2021", "A05:2021"]
---
```

Followed by the security review checklist organized by focus area.

## File Index

| File | Domain | Focus |
|------|--------|-------|
| [terraform.md](terraform.md) | Infrastructure | Terraform/OpenTofu IaC security review |
| [kubernetes.md](kubernetes.md) | Infrastructure | Kubernetes manifest and cluster config review |
| [cloudformation.md](cloudformation.md) | Infrastructure | AWS CloudFormation template security review |
| [api-design.md](api-design.md) | Design | Secure API design checklist |

## Usage in Skills

### IaC Security Review (`/iac-security-review`)

When reviewing infrastructure code, the skill auto-detects the IaC type and references the matching prompt data:
- `.tf` files → `terraform.md`
- Kubernetes manifests (Deployment, Pod, Service) → `kubernetes.md`
- CloudFormation templates (AWSTemplateFormatVersion) → `cloudformation.md`

### API Security Review (`/api-security-review`)

The `api-design.md` data supplements the existing API security review skill with secure-by-default design guidance.
