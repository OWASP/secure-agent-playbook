# Security Assessment Report Template

## Report: [Target Name]

**Date**: YYYY-MM-DD
**Assessor**: Claude Code (agent-security-playbook)
**Scope**: [What was assessed — repo, service, architecture, agent config]
**Skills Used**: [List of skills invoked]

---

## Executive Summary

[2-3 sentences: what was tested, highest-severity finding, overall risk posture]

## Findings Summary

| # | Severity | Title | CWE | OpenCRE | OWASP Ref | Status |
|---|----------|-------|-----|---------|-----------|--------|
| 1 | CRITICAL | ... | CWE-XXX | [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | Open |
| 2 | HIGH | ... | CWE-XXX | [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | Open |

## Findings Detail

[Include full findings using templates/finding.md format]

## Out of Scope

[Explicitly list what was NOT tested]

## Standards Coverage

OpenCRE cross-references for all findings (auto-populated via `data/opencre/`):

| CRE ID | Requirement | CWE | ASVS | WSTG | NIST 800-53 | Findings |
|--------|-------------|-----|------|------|-------------|----------|
| [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | CWE-XXX | V#.#.# | WSTG-XXX-## | XX-## | #1, #2 |

## Recommendations

[Prioritized list of next steps, ordered by risk reduction impact]
