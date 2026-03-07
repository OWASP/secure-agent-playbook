# Third-Party Notices

This project incorporates or references material from the following third-party sources.

## Arcanum Prompt Injection Taxonomy

- **Source**: [Arcanum-Sec/arc_pi_taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy)
- **Author**: Jason Haddix, Arcanum Information Security
- **License**: CC BY 4.0
- **Used in**: `plays/tier4-ai-security/prompt-injection-testing.md`, `.claude/skills/prompt-injection-test/SKILL.md`
- **Usage**: Attack intent, technique, and evasion classifications for prompt injection testing

## OWASP Agent Skills Project (ASVS 5.0 Data)

- **Source**: [eoftedal/owasp-agent-skills-project](https://github.com/eoftedal/owasp-agent-skills-project)
- **Author**: Erlend Oftedal and contributors
- **License**: CC BY-SA 4.0 (OWASP ASVS)
- **Used in**: `data/asvs/` (80 section files V1.1 through V17.3)
- **Usage**: ASVS 5.0 verification requirements with YAML frontmatter for context-aware lookups

## OpenCRE (Open Common Requirements Enumeration)

- **Source**: [opencre.org](https://www.opencre.org)
- **License**: Apache 2.0
- **Used in**: `data/opencre/`, cross-standard references in all findings
- **Usage**: CRE ID mappings for cross-standard traceability (CWE, ASVS, WSTG, NIST 800-53)

## OWASP Standards

The following OWASP standards are referenced throughout this project:

| Standard | License | Usage |
|----------|---------|-------|
| [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/) | CC BY-SA 4.0 | Risk classification in all plays |
| [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/) | CC BY-SA 4.0 | API security review play |
| [OWASP Top 10 for LLM Applications](https://genai.owasp.org) | CC BY-SA 4.0 | LLM risk assessment play |
| [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org) | CC BY-SA 4.0 | Agentic AI risk assessment play |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | CC BY-SA 4.0 | Verification-level mapping |
| [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) | CC BY-SA 4.0 | Testing methodology references |

## CWE (Common Weakness Enumeration)

- **Source**: [cwe.mitre.org](https://cwe.mitre.org)
- **Author**: MITRE Corporation
- **License**: [CWE Terms of Use](https://cwe.mitre.org/about/termsofuse.html)
- **Usage**: Weakness classification in findings
