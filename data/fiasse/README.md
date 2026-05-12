# FIASSE / SSEM Reference Data

61 structured FIASSE section files sourced from the [FIASSE framework v1.0.4](https://github.com/OWASP/FIASSE/blob/v1.0.4/docs/securable_framework.md) by Alton Crossley.

FIASSE (Framework for Integrating Application Security into Software Engineering) provides the overarching strategic approach. SSEM (Securable Software Engineering Model) provides the design language with **10 core attributes** grouped into 3 pillars: Maintainability, Trustworthiness, and Reliability.

## Source & License

These files are derived from the [OWASP/FIASSE](https://github.com/OWASP/FIASSE) repository at tag `v1.0.4`. Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "S3.2.1 Maintainability"
fiasse_section: "S3.2.1"
fiasse_version: "1.0.4"
ssem_pillar: "Maintainability"             # (optional) SSEM pillar
ssem_attributes:                           # (optional) SSEM sub-attributes
  - Analyzability
  - Modifiability
  - Testability
  - Observability
when_to_use:                               # Task-matching triggers
  - reviewing code for maintainability
  - assessing analyzability of a codebase
threats:                                   # Security implications addressed
  - undetected vulnerabilities due to complex code
  - slow vulnerability remediation
summary: "Definitions and contributing factors for Maintainability sub-attributes."
---
```

Followed by the FIASSE section content. Measurement sections (Appendix A, files `SA.*.md`) include tables:

```
| Metric | Type | Description |
| --- | --- | --- |
| Volume (LoC) | Quantitative | Overall size of the codebase |
```

## SSEM Model Reference (v1.0.4)

| **Maintainability** | **Trustworthiness** | **Reliability** |
|:--------------------|:-------------------:|----------------:|
| Analyzability       | Confidentiality     | Availability    |
| Modifiability       | Accountability      | Integrity       |
| Testability         | Authenticity        | Resilience      |
| Observability       |                     |                 |

**v1.0.4 changes**: Observability is the 10th SSEM attribute (under Maintainability). The Principle of Least Astonishment (S2.6) and the Boundary Control Principle (S4.3, formerly "Flexibility Principle") are also introduced.

## Usage in Skills

### Securability Engineering Review (`/securability-engineering-review`)

When scoring SSEM attributes, reference the specific section for definitions and measurement criteria. Leaf attribute files give granular lookups:

```markdown
- **FIASSE Ref**: S3.2.1.1 Analyzability (definition + contributing factors)
- **Measurement**: SA.1.1 Measuring Analyzability (metrics + qualitative checks)
```

### FIASSE Code Analysis (`/securability-engineering-review`)

When identifying code-level threats, apply the "What can go wrong?" framework (Section 4.2.1) and map identified issues to the relevant SSEM attributes and FIASSE sections for context and remediation guidance.

Use `when_to_use` frontmatter to match tasks to relevant FIASSE sections. For example, when reviewing dependency management:
- `S4.5` — Dependency Management
- `S4.6` — Dependency Stewardship (ongoing relationship)

### Task-Based Lookup

Use the `when_to_use` and `ssem_attributes` frontmatter to match analysis tasks to relevant sections. Leaf files (e.g., `S3.2.1.4.md` Observability) carry attribute-specific metadata for finer-grained matching.

## Section Index

| Section | Topic | Files |
|---------|-------|-------|
| §1 | Introduction | S1.1–S1.2 |
| §2 | Foundational Principles | S2.1–S2.6 |
| §3.1 | Model Overview and Design Language | S3.1 |
| §3.2 | Core Securable Attributes | S3.2, S3.2.1–S3.2.3 (umbrella + leaf) |
| §4 | Practical Guidance | S4.1–S4.6 (with leaf subsections) |
| §5 | Integrating Security into Dev Processes | S5.1–S5.3 |
| §6 | Common AppSec Anti-Patterns | S6.1–S6.2 (with leaf subsections) |
| §7 | Roles & Responsibilities | S7.1–S7.4 |
| §8 | Organizational Adoption of FIASSE | S8 |
| Appendix A | Measuring SSEM Attributes | SA.1–SA.3 (with attribute leaves) |

## Detailed File Listing

| File | Title |
|------|-------|
| S1.1.md | The Application Security Challenge |
| S1.2.md | Document Purpose and Scope |
| S2.1.md | The Securable Paradigm: No Static Secure State |
| S2.2.md | Resiliently Add Computing Value |
| S2.3.md | Security Mission: Reducing Material Impact |
| S2.4.md | Aligning Security with Development |
| S2.5.md | The Transparency Principle |
| S2.6.md | The Principle of Least Astonishment |
| S3.1.md | Model Overview and Design Language |
| S3.2.md | Core Securable Attributes |
| S3.2.1.md | Maintainability (umbrella) |
| S3.2.1.1.md | Analyzability |
| S3.2.1.2.md | Modifiability |
| S3.2.1.3.md | Testability |
| S3.2.1.4.md | Observability |
| S3.2.2.md | Trustworthiness (umbrella) |
| S3.2.2.1.md | Confidentiality |
| S3.2.2.2.md | Accountability |
| S3.2.2.3.md | Authenticity |
| S3.2.3.md | Reliability (umbrella) |
| S3.2.3.1.md | Availability |
| S3.2.3.2.md | Integrity |
| S3.2.3.3.md | Resilience |
| S4.1.md | Establishing Clear Expectations |
| S4.1.1.md | Proactive Communication |
| S4.1.2.md | Integrating Security into Requirements |
| S4.2.md | Threat Modeling |
| S4.2.1.md | Code-Level Threat Awareness |
| S4.2.2.md | Threat Modeling Solution Framework |
| S4.3.md | The Boundary Control Principle |
| S4.4.md | Resilient Coding |
| S4.4.1.md | Canonical Input Handling |
| S4.4.1.1.md | The Request Surface Minimization Principle |
| S4.4.1.2.md | The Derived Integrity Principle |
| S4.5.md | Dependency Management |
| S4.6.md | Dependency Stewardship |
| S5.1.md | Natively Extending Development Processes |
| S5.2.md | The Role of Merge Reviews |
| S5.3.md | Early Integration: Planning and Requirements |
| S6.1.md | The "Shoveling Left" Phenomenon |
| S6.1.1.md | Ineffective Vulnerability Reporting |
| S6.1.2.md | Pitfalls of Exploit-First Training |
| S6.2.md | Strategic Use of Security Output |
| S7.1.md | The Role of the Security Team |
| S7.2.md | Senior Software Engineers |
| S7.3.md | Developing Software Engineers |
| S7.4.md | Product Owners and Managers |
| S8.md | Organizational Adoption of FIASSE |
| SA.1.md | Measuring Maintainability (umbrella) |
| SA.1.1.md | Measuring Analyzability |
| SA.1.2.md | Measuring Modifiability |
| SA.1.3.md | Measuring Testability |
| SA.1.4.md | Measuring Observability |
| SA.2.md | Measuring Trustworthiness (umbrella) |
| SA.2.1.md | Measuring Confidentiality |
| SA.2.2.md | Measuring Accountability |
| SA.2.3.md | Measuring Authenticity |
| SA.3.md | Measuring Reliability (umbrella) |
| SA.3.1.md | Measuring Availability |
| SA.3.2.md | Measuring Integrity |
| SA.3.3.md | Measuring Resilience |

## Updating

To refresh from upstream:

```bash
# Fetch the v1.0.4 framework
curl -o /tmp/securable_framework.md https://raw.githubusercontent.com/OWASP/FIASSE/refs/tags/v1.0.4/docs/securable_framework.md
# Extract sections using the extraction script
python scripts/extract_fiasse_sections.py /tmp/securable_framework.md data/fiasse/
```
