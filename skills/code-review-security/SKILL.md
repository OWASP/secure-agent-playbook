---
name: code-review-security
description: Security-focused code review mapped to OWASP Top 10 and ASVS. Use when reviewing pull requests, auditing files or modules for vulnerabilities, or performing pre-merge security gate checks. Covers injection, auth, authorization, cryptography, data exposure, misconfiguration, and deserialization.
license: CC-BY-4.0
---

# Security Code Review

Review code for security vulnerabilities by following the full procedure in `plays/tier1-code-analysis/code-review-security.md`.

## Steps

1. **Scope & Context** — Establish language/framework, trust boundary (server/client/library/CLI), data sensitivity (PII, credentials, financial), and exposure (internet-facing, internal, local).

2. **Systematic Review by Vulnerability Class** (priority order):
   - **Injection (A03)** — SQL, command, XSS, SSTI, LDAP, path traversal, header, log injection
   - **Authentication & Session (A07)** — Hardcoded credentials, missing auth, weak sessions, JWT issues
   - **Authorization (A01)** — Missing authz checks, IDOR, horizontal/vertical privilege escalation
   - **Cryptography (A02)** — Weak algorithms, hardcoded keys, missing encryption, custom crypto
   - **Data Exposure (A01)** — Sensitive data in errors/logs, credentials in code, debug mode
   - **Misconfiguration (A05)** — Default credentials, permissive CORS, missing security headers
   - **Deserialization (A08)** — Untrusted deserialization, missing integrity checks, CSRF gaps

3. **Framework-Specific Checks** — Apply checks for detected framework (React, Express, Django, Flask, Spring, Rails, Go).

4. **Diff-Specific Analysis** (for PRs) — Focus on changed lines plus context, verify security controls preserved, check new endpoints match auth patterns, look for removed security controls.

5. **Produce Findings** — Cite file:line, show vulnerable snippet, explain attack scenario, provide fixed code, rate confidence.

## Output

Scope summary, findings sorted by severity using `templates/finding.md`, positive observations (good security controls in place), and severity count table.

## OWASP References

- OWASP Top 10 (2021): A01-A10
- OWASP ASVS v5.0
- OWASP Code Review Guide
- OWASP Cheat Sheet Series
