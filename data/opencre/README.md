# OpenCRE — Cross-Standard Reference Data

12 structured CWE-to-CRE mapping files with verified OpenCRE IDs, plus API documentation for lookups.

[OpenCRE](https://www.opencre.org) (Open Common Requirements Enumeration) maps security requirements across standards, creating a unified graph that links CWEs, OWASP projects, NIST, ISO 27001, and more.

## Source & License

OpenCRE is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). CRE IDs were verified against the OpenCRE REST API (`GET /rest/v1/standard/CWE/sectionid/{id}`).

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "CWE-79 Cross-site Scripting (XSS)"
cwe_id: "CWE-79"
owasp_top10: "A03:2021 Injection"
opencre_mappings:                         # Verified CRE IDs from API
  - cre_id: "366-835"
    cre_name: "Escape output against XSS"
when_to_use:                              # Task-matching triggers
  - reviewing code that renders user input in HTML pages
threats:                                  # Relevant threat categories
  - reflected XSS via URL parameters
summary: "Brief description."
---
```

Followed by OpenCRE mapping table, cross-standard references, "What to Look For" checklist, and external references.

## Usage in Skills

### Finding Cross-References

When producing a finding, look up the CWE file to get the verified CRE ID:

```markdown
- **CWE**: CWE-79
- **OpenCRE**: [366-835](https://www.opencre.org/cre/366-835) — Escape output against XSS
```

The OpenCRE link gives readers one-click access to every related standard, cheat sheet, and test case.

### Task-Based Lookup

Use the `when_to_use` frontmatter to match tasks to relevant CWE/CRE mappings. For example, if reviewing file upload code, check:
- `CWE-22` — Path Traversal
- `CWE-502` — Deserialization of Untrusted Data

## CWE Mapping Index

| File | CWE | OWASP Top 10 | Primary CRE ID | CRE Name |
|------|-----|-------------|----------------|----------|
| [CWE-79](CWE-79.md) | CWE-79 | A03 Injection | 366-835 | Escape output against XSS |
| [CWE-89](CWE-89.md) | CWE-89 | A03 Injection | 732-873 | Lock/precompile queries (parameterization) |
| [CWE-78](CWE-78.md) | CWE-78 | A03 Injection | 857-718 | Protect against OS command injection |
| [CWE-22](CWE-22.md) | CWE-22 | A01 Broken Access Control | 675-168 | Sanitize filename metadata from untrusted origin |
| [CWE-287](CWE-287.md) | CWE-287 | A07 Auth Failures | 813-610 | Do not use static secrets |
| [CWE-200](CWE-200.md) | CWE-200 | A01 Broken Access Control | 227-045 | Identify sensitive data and subject it to a policy |
| [CWE-327](CWE-327.md) | CWE-327 | A02 Cryptographic Failures | 742-431 | Use approved cryptographic algorithms |
| [CWE-352](CWE-352.md) | CWE-352 | A01 Broken Access Control | 464-084 | Add CSRF protection for cookie based REST services |
| [CWE-384](CWE-384.md) | CWE-384 | A07 Auth Failures | 002-630 | Generate a new session token after authentication |
| [CWE-502](CWE-502.md) | CWE-502 | A08 Data Integrity | 831-563 | Avoid deserialization logic |
| [CWE-778](CWE-778.md) | CWE-778 | A09 Logging Failures | 184-284 | Log all security relevant events |
| [CWE-798](CWE-798.md) | CWE-798 | A07 Auth Failures | 774-888 | Do not store secrets in the code |
| [CWE-16](CWE-16.md) | CWE-16 | A05 Misconfiguration | 180-488 | Proper Configuration for all apps and frameworks |

## CRE Hierarchy

OpenCRE organizes security into five root domains:

| CRE ID | Domain |
|--------|--------|
| 636-660 | Technical application security controls |
| 546-564 | Cross-cutting concerns |
| 616-305 | Development processes for security |
| 862-452 | Operating processes for security |
| 567-755 | Governance processes for security |

## REST API

Base URL: `https://www.opencre.org/rest/v1`

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /id/{cre-id}` | Lookup by CRE ID | `/id/366-835` |
| `GET /standard/{name}/sectionid/{id}` | Lookup by standard | `/standard/CWE/sectionid/79` |
| `GET /root_cres` | Get all root categories | `/root_cres` |

Web UI: `https://www.opencre.org/cre/{cre-id}`

## Standards Mapped

| Standard | Coverage |
|----------|----------|
| CWE | Common Weakness Enumeration |
| OWASP Top 10 (2021) | A01-A10 |
| OWASP ASVS | Application Security Verification Standard |
| OWASP WSTG | Web Security Testing Guide |
| OWASP Proactive Controls | C1-C10 |
| OWASP Cheat Sheets | Per-topic defense guidance |
| NIST 800-53 v5 | Security and Privacy Controls |
| NIST SSDF | Secure Software Development Framework |
| ISO 27001 | Information Security Management |
| CAPEC | Common Attack Pattern Enumeration |

## Adding New Mappings

To add a CWE not listed here:

```bash
# Look up the CWE in OpenCRE API
curl -s "https://www.opencre.org/rest/v1/standard/CWE/sectionid/XXX" | jq '.data[].links[].document | select(.doctype == "CRE") | {id, name}'
```

Then create a new `CWE-XXX.md` file following the existing format.
