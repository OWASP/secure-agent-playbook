---
name: web-security-review
description: Review web applications against the OWASP Top 10 for Web Applications (2021). Use when auditing web apps, reviewing server-side code, or assessing web frameworks for the classic OWASP Top 10 risks including injection, broken auth, and XSS.
license: CC-BY-4.0
---

# Web Security Review (OWASP Top 10)

Review web applications against all 10 OWASP Top 10 risks by following the full procedure in `plays/tier1-code-analysis/owasp-top10-web-review.md`.

## Steps

1. **Application Mapping** — Identify framework/language, deployment model (monolith/microservices), trust boundaries (internet/internal/local), data sensitivity (PII, financial, health), and authentication mechanisms.

2. **Assess Each OWASP Top 10 Risk**:
   - **A01 Broken Access Control** — Missing authz checks, IDOR, privilege escalation, path traversal, CORS misconfigurations
   - **A02 Cryptographic Failures** — Weak algorithms, missing TLS, hardcoded keys, improper key management, cleartext storage
   - **A03 Injection** — SQLi, NoSQLi, OS command injection, LDAP injection, XSS, SSTI, XPath injection
   - **A04 Insecure Design** — Missing security requirements, business logic flaws, insecure workflows, threat modeling gaps
   - **A05 Security Misconfiguration** — Default configs, verbose errors, missing headers, unnecessary features, outdated components
   - **A06 Vulnerable Components** — Unpatched libraries, unsupported dependencies, lack of inventory, missing SBOM
   - **A07 Identification & Auth Failures** — Weak passwords, session issues, MFA gaps, credential stuffing, brute force
   - **A08 Software & Data Integrity Failures** — Insecure deserialization, unsigned updates, CI/CD attacks, dependency confusion
   - **A09 Security Logging & Monitoring Failures** — Missing audit logs, insufficient monitoring, no incident response capability
   - **A10 Server-Side Request Forgery (SSRF)** — Unvalidated URL parameters, internal service access, cloud metadata endpoints

3. **Framework-Specific Analysis** — Apply checks for detected framework (React, Angular, Vue, Express, Django, Flask, Rails, Spring, ASP.NET, Laravel).

4. **Configuration Review** — Examine web server configs (nginx, Apache), application configs, and deployment manifests for security settings.

## Output

Application overview, risk matrix for all 10 categories with severity/status, detailed findings using `templates/finding.md`, positive controls observed, and prioritized remediation roadmap.

## OWASP References

- OWASP Top 10 for Web Applications (2021)
- OWASP ASVS v5.0 — Application Security Verification Standard
- OWASP Testing Guide (WSTG)
- OWASP Cheat Sheet Series
