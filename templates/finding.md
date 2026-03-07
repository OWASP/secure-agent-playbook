# Finding Template

Use this structure for all security findings produced by skills.

```markdown
### [SEVERITY] Title

- **ID**: NDC-YYYY-NNN (auto-incrementing)
- **CWE**: CWE-XXX (if applicable)
- **CVE**: CVE-YYYY-NNNNN (if applicable)
- **OpenCRE**: [CRE-ID](https://www.opencre.org/cre/CRE-ID) — requirement name (see data/opencre/)
- **OWASP Ref**: Top 10 A01, ASVS 4.1.1, LLM01, etc.
- **Location**: file_path:line_number or component name
- **Impact**: What an attacker can achieve (1-2 sentences)
- **Evidence**: Code snippet, command output, or proof-of-concept
- **Remediation**: Specific fix with code example
- **Confidence**: HIGH | MEDIUM | LOW (how certain is this finding)
```

### Resolving OpenCRE Links

When you have a CWE, look up its OpenCRE mapping via the API:

```
GET https://www.opencre.org/rest/v1/standard/CWE/sectionid/{cwe-number}
```

This returns the CRE ID and linked standards (ASVS, WSTG, NIST 800-53, cheat sheets). Include the CRE link in findings to give readers one-click access to all related standards and remediation guidance.

Common mappings are pre-populated in `data/opencre/README.md`.

## Severity Definitions

| Severity | CVSS Range | Criteria |
|----------|-----------|----------|
| CRITICAL | 9.0-10.0 | Remote code execution, full system compromise, mass data breach |
| HIGH | 7.0-8.9 | Privilege escalation, significant data exposure, auth bypass |
| MEDIUM | 4.0-6.9 | Limited data exposure, requires user interaction or specific conditions |
| LOW | 0.1-3.9 | Information disclosure, minor misconfigurations |
| INFORMATIONAL | N/A | Best practice recommendations, defense-in-depth suggestions |

## Confidence Levels

| Level | Meaning |
|-------|---------|
| HIGH | Confirmed via code path analysis, PoC, or tool output |
| MEDIUM | Strong indicators but not fully confirmed — needs manual verification |
| LOW | Heuristic match or pattern-based — may be false positive |
