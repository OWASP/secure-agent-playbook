# Play: Security Code Review

A security code review identifies vulnerabilities in application logic, authentication, authorization, cryptography, and data handling. This play structures the review around OWASP weakness classes (injection, auth, crypto, etc.) and is applicable to any language or framework. Reviews can target full codebases, pull request diffs, or specific modules, and findings are mapped to OWASP standards and OpenCRE for multi-framework traceability.

Review code changes or codebases for security vulnerabilities, mapping findings to OWASP standards and OpenCRE cross-references for multi-framework traceability.

## Trigger Conditions

Use this skill when:
- Reviewing a pull request or diff for security issues
- A user asks for a security review of their code
- Auditing a specific file, module, or feature for vulnerabilities
- Performing a pre-merge security gate check

## Inputs

- Code diff (PR), specific files, or entire codebase to review
- (Optional) Language and framework context
- (Optional) ASVS level to verify against (L1, L2, or L3)
- (Optional) Specific concern areas to focus on

## Procedure

### 1. Scope & Context

Before diving in, establish:
- **Language/Framework**: Determines which vulnerability classes are relevant
- **Trust boundary**: Is this server-side, client-side, library, CLI, infrastructure code?
- **Data sensitivity**: Does this code handle PII, credentials, financial data, health data?
- **Exposure**: Is this internet-facing, internal, or local-only?

### 2. Systematic Review by Vulnerability Class

Review in priority order — highest-impact classes first:

#### A. Injection (CWE-74, OWASP A03, [OpenCRE 161-451](https://www.opencre.org/cre/161-451))

> ASVS refs: `data/asvs/V12.1.md` (Input Validation), `data/asvs/V13.1.md` (Output Encoding), `data/asvs/V5.3.md` (File Storage)

| Subtype | What to Look For |
|---------|-----------------|
| SQL Injection | String concatenation in queries, missing parameterization, ORM raw queries |
| Command Injection | User input in exec/spawn/system calls, unsanitized shell arguments |
| XSS | User input rendered without output encoding, unsafe DOM manipulation, unescaped template output |
| SSTI | User input in template strings that get evaluated server-side |
| LDAP Injection | User input in LDAP filters without escaping |
| Path Traversal | User input in file paths without canonicalization, `../` not blocked |
| Header Injection | User input in HTTP headers (CRLF injection) |
| Log Injection | User input written to logs without sanitization |

#### B. Authentication & Session (CWE-287, OWASP A07, [OpenCRE 633-428](https://www.opencre.org/cre/633-428))

> ASVS refs: `data/asvs/V2.1.md`–`V2.4.md` (Authentication), `data/asvs/V3.1.md`–`V3.7.md` (Session Management)

- Hardcoded credentials or API keys
- Missing authentication on endpoints
- Weak password requirements
- Session tokens in URLs or logs
- Missing session invalidation on logout/password change
- JWT issues: none algorithm, missing expiry, weak signing key, secrets in payload
- Missing MFA enforcement for sensitive operations

#### C. Authorization (CWE-862, OWASP A01, [OpenCRE 724-770](https://www.opencre.org/cre/724-770))

> ASVS refs: `data/asvs/V4.1.md`–`V4.4.md` (Access Control)

- Missing authorization checks on endpoints or functions
- IDOR: object references without ownership validation
- Horizontal privilege escalation (accessing other users' data)
- Vertical privilege escalation (accessing admin functions)
- Missing RBAC/ABAC enforcement
- Direct database queries that don't filter by user/tenant

#### D. Cryptography (CWE-327, OWASP A02, [OpenCRE 278-646](https://www.opencre.org/cre/278-646))

> ASVS refs: `data/asvs/V6.1.md`–`V6.8.md` (Cryptography)

- Weak algorithms: MD5, SHA1 for passwords, DES, RC4
- ECB mode usage
- Hardcoded encryption keys or IVs
- Missing encryption at rest for sensitive data
- Missing TLS enforcement
- Custom crypto implementations (don't roll your own)
- Insufficient key lengths (RSA < 2048, AES < 128)

#### E. Data Exposure (CWE-200, OWASP A01, [OpenCRE 126-668](https://www.opencre.org/cre/126-668))

> ASVS refs: `data/asvs/V8.1.md`–`V8.4.md` (Data Protection), `data/asvs/V7.1.md`–`V7.6.md` (Error Handling & Logging)

- Sensitive data in error messages or stack traces
- Verbose logging of requests/responses containing PII
- Credentials or tokens in source code, configs, or URLs
- Missing response headers (X-Content-Type-Options, etc.)
- API responses including more fields than necessary
- Debug mode enabled in production configs

#### F. Security Misconfiguration (OWASP A05, [OpenCRE 233-748](https://www.opencre.org/cre/233-748))

> ASVS refs: `data/asvs/V10.1.md`–`V10.7.md` (Configuration)

- Default credentials or configurations
- Unnecessary features enabled (debug endpoints, admin panels)
- Missing security headers
- Overly permissive CORS
- Directory listing enabled
- Missing rate limiting on sensitive endpoints

#### G. Deserialization & Data Integrity (CWE-502, OWASP A08, [OpenCRE 854-643](https://www.opencre.org/cre/854-643))

> ASVS refs: `data/asvs/V11.1.md`–`V11.7.md` (Business Logic)

- Deserializing untrusted data (unsafe deserialization in any language — Python, Java, PHP, Ruby, .NET)
- Missing integrity checks on data from untrusted sources
- Unsigned cookies or tokens
- Missing CSRF protection on state-changing operations

### 3. Framework-Specific Checks

Apply checks specific to the detected framework:

| Framework | Key Checks |
|-----------|-----------|
| React/Next.js | XSS via unsafe HTML rendering, SSRF in server-side data fetching, exposed API routes |
| Express/Node | Missing helmet, no rate limiting, prototype pollution, regex DoS |
| Django | Raw SQL, CSRF exemptions, DEBUG=True, SECRET_KEY exposure |
| Flask | Jinja2 autoescape disabled, unsafe session serialization, debug mode |
| Spring | SpEL injection, actuator exposure, mass assignment |
| Rails | Mass assignment, render user input, SQL fragments |
| Go net/http | Missing timeouts, TOCTOU in file operations, integer overflow |

### 4. Diff-Specific Analysis (for PR reviews)

When reviewing a diff rather than a full codebase:
- Focus on changed lines and their immediate context
- Check if security controls in surrounding (unchanged) code are preserved
- Verify that new endpoints have auth/authz matching existing patterns
- Check if new dependencies introduce vulnerabilities (cross-reference with sca-audit)
- Look for removed security controls (deleted validation, removed auth checks)

### 5. Produce Findings

For each issue:
- Cite the specific code location (file:line)
- Show the vulnerable code snippet
- Explain the attack scenario concretely
- Provide a fixed code snippet
- Rate confidence (HIGH if confirmed path, MEDIUM if contextual, LOW if heuristic)

## Output Format

```markdown
## Security Code Review: [Target]

### Scope
- **Files reviewed**: [count or list]
- **Language/Framework**: [detected]
- **Review type**: Full | PR diff | Targeted

### Findings
[Standard finding template for each issue, sorted by severity]

### Positive Observations
[Security controls that ARE in place — acknowledge good practices]

### Summary
| Severity | Count |
|----------|-------|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |
| INFO | N |
```

## Tools & Resources

### Static Analysis Tools
- **Semgrep** — Multi-language pattern-based SAST; highly customizable rules
- **CodeQL (GitHub)** — Query-based code analysis for Java, C++, C#, Go, Python, TypeScript, JavaScript, Ruby
- **SonarQube** — Code quality and security scanning with OWASP Top 10 mappings
- **Checkmarx/CxSAST** — Enterprise SAST with custom rule authoring
- **Snyk Code** — Developer-first SAST integrated into IDEs and CI/CD

### Language-Specific
- **Bandit** (Python) — Finds common security issues in Python code
- **Brakeman** (Ruby) — Scans Rails apps for OWASP risks
- **go-vuln-check** (Go) — Detects known vulnerabilities in Go code
- **ShiftLeft/Taint** (Java, Python, Go) — Data flow analysis for injection detection

### Code Review Checkers
- **OWASP Cheat Sheet Series** — Per-vulnerability quick guides and remediation
- **CWE Top 25** — Prioritized list of most dangerous weakness patterns
- **ASVS Interactive** — Maps review items to ASVS verification levels (L1/L2/L3)

## References

- OWASP Top 10 (2021): A01-A10
- OWASP ASVS v5.0 (for verification-level mapping)
- OWASP Code Review Guide
- OWASP Cheat Sheet Series (per-topic)
- OWASP Proactive Controls
- [OpenCRE](https://www.opencre.org) — Cross-standard requirement mappings (CWE, ASVS, WSTG, NIST 800-53, ISO 27001)
- [CWE](https://cwe.mitre.org) v4.19 — Common Weakness Enumeration
- ASVS 5.0 reference data in `data/asvs/` — sourced from [OWASP Agent Skills Project](https://github.com/eoftedal/owasp-agent-skills-project)
