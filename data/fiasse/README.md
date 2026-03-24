# FIASSE / SSEM Reference Data

35 structured FIASSE section files sourced from the [FIASSE RFC](https://github.com/Xcaciv/securable_software_engineering/blob/main/docs/FIASSE-RFC.md) by Alton Crossley.


[OWASP FIASSE](https://owasp.org/www-project-fiasse/) (Framework for Integrating Application Security into Software Engineering) provides the overarching strategic approach. SSEM (Securable Software Engineering Model) provides the design language with 9 core attributes grouped into 3 pillars: Maintainability, Trustworthiness, and Reliability.

## Source & License

These files are derived from the [Xcaciv/securable_software_engineering](https://github.com/Xcaciv/securable_software_engineering) repository. Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "S3.2.1 Maintainability"
fiasse_section: "S3.2.1"
ssem_pillar: "Maintainability"             # (optional) SSEM pillar
ssem_attributes:                           # (optional) SSEM sub-attributes
  - Analyzability
  - Modifiability
  - Testability
when_to_use:                               # Task-matching triggers
  - reviewing code for maintainability
  - assessing analyzability of a codebase
threats:                                   # Security implications addressed
  - undetected vulnerabilities due to complex code
  - slow vulnerability remediation
summary: "Definitions and contributing factors for Maintainability sub-attributes."
---
```

Followed by the FIASSE section content. Sections that define measurable requirements use a table:

```
| Metric | Type | Description |
| --- | --- | --- |
| Volume (LoC) | Quantitative | Overall size of the codebase |
```

## SSEM Model Reference

| **Maintainability** | **Trustworthiness** | **Reliability** |
|:---------------------|:---------------------:|----------------:|
| Analyzability        | Confidentiality       | Availability    |
| Modifiability        | Accountability        | Integrity       |
| Testability          | Authenticity          | Resilience      |

## Usage in Skills

### Securability Engineering Review (`/securability-engineering-review`)

When scoring SSEM attributes, reference the specific section for definitions and measurement criteria:

```markdown
- **FIASSE Ref**: S3.2.1 Maintainability — Analyzability (S3.2.1.1)
- **Measurement**: S3.4.1 Measuring Maintainability
```

### FIASSE Code Analysis (`/securability-engineering-review`)

When identifying code-level threats, use the "What can go wrong?" framework and map identified issues to the relevant SSEM attributes and FIASSE sections for context and remediation guidance.

Use `when_to_use` frontmatter to match tasks to relevant FIASSE sections. For example, when reviewing dependency management:
- `S4.1` — Applying SSEM to Dependency Management
- `S6.5` — Dependency Management Practices

### Task-Based Lookup

Use the `when_to_use` and `ssem_attributes` frontmatter to match analysis tasks to relevant sections.

## Section Index

| Section | Topic | Files |
|---------|-------|-------|
| §1 | Introduction | S1.1–S1.3 |
| §2 | Foundational Principles | S2.1–S2.6 |
| §3.1 | SSEM Overview | S3.1 |
| §3.2 | Core Securable Attributes | S3.2.1–S3.2.3 |
| §3.3 | Securable Code Strategy | S3.3.1–S3.3.2 |
| §3.4 | Measuring SSEM Attributes | S3.4.1–S3.4.3 |
| §4 | Integrating Security | S4.1–S4.4 |
| §5 | AppSec Anti-Patterns | S5.1–S5.2 |
| §6 | Practical Guidance | S6.1–S6.5 |
| §7 | Roles & Responsibilities | S7.0–S7.3 |
| §8 | Evolution & Adoption | S8.1–S8.2 |

## Detailed File Listing

| File | Title |
|------|-------|
| S1.1.md | The Application Security Challenge |
| S1.2.md | A Developer-Centric Security Paradigm |
| S1.3.md | Document Purpose and Scope |
| S2.1.md | The Securable Paradigm: No Static Secure State |
| S2.2.md | Resiliently Add Computing Value |
| S2.3.md | Security Mission: Reducing Material Impact |
| S2.4.md | Mindset Convergence: Hacker vs. Engineer |
| S2.5.md | Aligning Security with Development |
| S2.6.md | The Transparency Principle |
| S3.1.md | Securable Software Engineering Model Overview |
| S3.2.1.md | Maintainability (Analyzability, Modifiability, Testability) |
| S3.2.2.md | Trustworthiness (Confidentiality, Accountability, Authenticity) |
| S3.2.3.md | Reliability (Availability, Integrity, Resilience) |
| S3.3.1.md | Transparency Strategy |
| S3.3.2.md | SSEM as a Design Language |
| S3.4.1.md | Measuring Maintainability |
| S3.4.2.md | Measuring Trustworthiness |
| S3.4.3.md | Measuring Reliability |
| S4.1.md | Applying SSEM to Dependency Management |
| S4.2.md | Natively Extending Development Processes |
| S4.3.md | The Role of Merge Reviews |
| S4.4.md | Early Integration: Planning and Requirements |
| S5.1.md | The "Shoveling Left" Phenomenon |
| S5.2.md | Strategic Use of Security Output |
| S6.1.md | Establishing Clear Expectations |
| S6.2.md | Threat Modeling |
| S6.3.md | The Flexibility Principle |
| S6.4.md | Resilient Coding and System Resilience |
| S6.5.md | Dependency Management |
| S7.0.md | Security's Role |
| S7.1.md | Empowering Senior Software Engineers |
| S7.2.md | Guiding Developing Software Engineers |
| S7.3.md | The Role of Product Owners and Managers |
| S8.1.md | Adapting to Emerging Software Engineering Trends |
| S8.2.md | Organizational Adoption Strategies |

## Updating

To refresh from upstream:

```bash
# Fetch the latest FIASSE RFC
curl -o /tmp/FIASSE-RFC.md https://raw.githubusercontent.com/Xcaciv/securable_software_engineering/main/docs/FIASSE-RFC.md
# Extract sections using the extraction script
python scripts/extract_fiasse_sections.py /tmp/FIASSE-RFC.md data/fiasse/
```
