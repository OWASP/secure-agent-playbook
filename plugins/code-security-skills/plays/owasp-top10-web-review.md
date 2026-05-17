# Play: OWASP Top 10 Web Security Review

Review web applications against the OWASP Top 10 for Web Applications (2021), producing actionable findings with severity ratings and remediation guidance.

## Trigger Conditions

Use this play when:
- Auditing a web application (monolith, microservices, or serverless)
- Reviewing server-side web code for security vulnerabilities
- A user asks for an "OWASP Top 10 review" or "web security assessment"
- Assessing a web framework or CMS for security posture
- Performing a pre-deployment security review of a web app

## Inputs

- Web application source code (frontend and backend)
- Framework/language information (React, Django, Rails, etc.)
- Deployment context (internet-facing, internal, cloud platform)
- Authentication/authorization implementation details
- (Optional) Previous security assessments or pentest reports

## Procedure

### 1. Application Mapping

Before assessing risks, understand the application:

| Aspect | Questions |
|--------|-----------|
| **Framework** | What language/framework? (Node.js/Express, Python/Django, Ruby/Rails, Java/Spring, PHP/Laravel, etc.) |
| **Architecture** | Monolith, microservices, serverless (Lambda/Cloud Functions), SPA vs SSR? |
| **Trust Boundary** | Internet-facing, internal network, or local-only? |
| **Data Sensitivity** | Does it handle PII, credentials, financial data, health data (HIPAA)? |
| **Authentication** | Session-based, JWT, OAuth, SSO, API keys? |
| **Data Stores** | SQL database, NoSQL, cache (Redis), file storage, external APIs? |

Document the attack surface: entry points, data flows, trust boundaries.

### 2. Assess Each OWASP Top 10 Risk

#### A01: Broken Access Control

> CWE-200, CWE-201, CWE-352, CWE-639

**What to Look For:**

- [ ] **Missing authorization checks** — Endpoints or functions accessible without verifying user permissions
- [ ] **IDOR (Insecure Direct Object References)** — Can User A access User B's data by changing IDs in URLs/parameters?
- [ ] **Privilege escalation** — Can regular users access admin functions? Can users elevate their own privileges?
- [ ] **Path traversal** — Can file paths include `../` to escape intended directories?
- [ ] **CORS misconfiguration** — Overly permissive CORS allowing cross-origin attacks
- [ ] **Forced browsing** — Can unauthenticated users access protected resources by guessing URLs?
- [ ] **JWT token issues** — Missing signature validation, algorithm confusion attacks
- [ ] **Broken function-level authorization** — Different auth requirements for UI vs API endpoints

**Testing Approach:**
1. Map all endpoints requiring authentication
2. Test each without authentication (should fail)
3. Test cross-user access (User A accessing User B's resources)
4. Test privilege escalation paths (user → admin)
5. Verify authorization on every object access, not just initial authentication

---

#### A02: Cryptographic Failures

> CWE-261, CWE-296, CWE-310, CWE-319, CWE-326, CWE-327, CWE-916

**What to Look For:**

- [ ] **Weak algorithms** — MD5, SHA1 for passwords; DES, RC4 for encryption; ECB mode
- [ ] **Missing TLS** — HTTP instead of HTTPS, weak TLS versions (<1.2), insecure ciphers
- [ ] **Hardcoded credentials/keys** — API keys, database passwords, encryption keys in source code
- [ ] **Improper key management** — Keys stored in version control, no key rotation, weak key generation
- [ ] **Cleartext transmission** — Sensitive data sent over unencrypted channels
- [ ] **Cleartext storage** — Passwords, tokens, or PII stored without encryption
- [ ] **Insufficient randomness** — Predictable tokens, session IDs, or nonces
- [ ] **Missing integrity checks** — Unsigned or unvalidated data that could be tampered with

**Testing Approach:**
1. Search for hardcoded secrets using patterns (see secrets-scan.md)
2. Verify TLS configuration (certificates, protocol versions, cipher suites)
3. Check password storage (should use bcrypt, Argon2, or PBKDF2)
4. Validate encryption implementations (no custom crypto)
5. Test for sensitive data in URLs, headers, and logs

---

#### A03: Injection

> CWE-74, CWE-78, CWE-79, CWE-89, CWE-91, CWE-564, CWE-943

**What to Look For:**

| Injection Type | Indicators | Impact |
|---------------|------------|---------|
| **SQL Injection** | String concatenation in SQL, `cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")`, dynamic queries | Data exfiltration, authentication bypass, RCE |
| **NoSQL Injection** | Unsanitized JSON in MongoDB queries, `$where` clauses with user input | Data manipulation, authentication bypass |
| **OS Command Injection** | `exec()`, `system()`, `subprocess.call()` with user input | Remote code execution |
| **LDAP Injection** | User input in LDAP filters without escaping | Authentication bypass, data access |
| **XSS (Cross-Site Scripting)** | User input rendered without encoding, `innerHTML`, `dangerouslySetInnerHTML`, unescaped template output | Session hijacking, credential theft, defacement |
| **SSTI (Server-Side Template Injection)** | User input in Jinja2, ERB, EJS templates | RCE, file access |
| **XPath Injection** | User input in XPath queries | XML data access |
| **Log Injection** | CRLF in log entries (`\n\r`), log forging | Log tampering, data exfiltration |
| **Header Injection** | CRLF in HTTP headers | Response splitting, XSS |

**Testing Approach:**
1. Search for dangerous functions (concatenation, eval, exec, innerHTML)
2. Test each input field with injection payloads
3. Verify output encoding for all user-controlled data
4. Check prepared statements/parameterized queries usage
5. Validate Content Security Policy (CSP) headers for XSS mitigation

---

#### A04: Insecure Design

> CWE-73, CWE-183, CWE-209, CWE-213, CWE-235, CWE-256, CWE-257, CWE-266, CWE-269, CWE-280, CWE-434, CWE-444, CWE-501, CWE-522, CWE-697, CWE-799, CWE-807, CWE-840, CWE-841, CWE-927, CWE-1021, CWE-1173, CWE-1174, CWE-1233

**What to Look For:**

- [ ] **Missing threat modeling** — No documented attack surface, trust boundaries, or threat actors
- [ ] **Business logic flaws** — Workflow bypasses (skip payment step), race conditions (TOCTOU), price manipulation
- [ ] **Insecure workflows** — Missing confirmation steps for destructive actions, no CSRF protection on state changes
- [ ] **Lack of rate limiting** — Brute force vulnerabilities on login, password reset, or sensitive operations
- [ ] **Insufficient validation** — Client-side only validation, missing server-side checks
- [ ] **Insecure defaults** — Debug mode enabled, verbose errors in production, default credentials
- [ ] **Trust without verification** — Trusting client-provided data (prices, user IDs, permissions)
- [ ] **Missing defense in depth** — Single point of failure for security controls

**Testing Approach:**
1. Review architecture documentation for security considerations
2. Test business logic flows for bypass opportunities
3. Check for race conditions in multi-step processes
4. Verify rate limiting on sensitive endpoints
5. Ensure all validation happens server-side

---

#### A05: Security Misconfiguration

> CWE-2, CWE-11, CWE-13, CWE-15, CWE-16, CWE-209, CWE-250, CWE-260, CWE-312, CWE-497, CWE-538, CWE-540, CWE-541, CWE-547, CWE-611, CWE-614, CWE-756, CWE-942

**What to Look For:**

- [ ] **Default configurations** — Default passwords, default admin accounts, sample applications deployed
- [ ] **Verbose error messages** — Stack traces, internal paths, SQL errors exposed to users
- [ ] **Missing security headers** — No `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`
- [ ] **Unnecessary features** — Unused ports open, unnecessary services running, debug endpoints enabled
- [ ] **Directory listing** — Web servers showing directory contents
- [ ] **Outdated software** — Old framework versions, unpatched components
- [ ] **Cloud misconfigurations** — Exposed S3 buckets, open security groups, public databases
- [ ] **Missing hardening** — Default SSL/TLS settings, unnecessary HTTP methods enabled

**Testing Approach:**
1. Review configuration files (nginx.conf, .htaccess, application.yml)
2. Check for default credentials and accounts
3. Verify security headers using tools or manual inspection
4. Test error handling (trigger errors, check responses)
5. Scan for unnecessary open ports and services
6. Check cloud configurations for public exposure

---

#### A06: Vulnerable and Outdated Components

> CWE-937, CWE-1035, CWE-1104

**What to Look For:**

- [ ] **Unpatched dependencies** — Known CVEs in libraries (see sca-audit.md)
- [ ] **Unsupported software** — End-of-life frameworks, operating systems, databases
- [ ] **Missing SBOM** — No inventory of software components
- [ ] **Unused dependencies** — Dead code increasing attack surface
- [ ] **Transitive vulnerabilities** — Vulnerabilities in dependencies of dependencies
- [ ] **Supply chain risks** — Typosquatting, malicious packages, compromised dependencies

**Testing Approach:**
1. Run SCA scanner (osv-scanner, npm audit, pip-audit)
2. Review dependency files (package.json, requirements.txt, etc.)
3. Check for end-of-life components
4. Verify dependency update processes
5. Review lockfiles for reproducible builds

---

#### A07: Identification and Authentication Failures

> CWE-287, CWE-288, CWE-290, CWE-294, CWE-295, CWE-297, CWE-300, CWE-302, CWE-304, CWE-306, CWE-307, CWE-346, CWE-384, CWE-521, CWE-613, CWE-620, CWE-640, CWE-798, CWE-940, CWE-1216

**What to Look For:**

- [ ] **Weak password policy** — No minimum length, no complexity requirements, common passwords allowed
- [ ] **Credential stuffing** — No protection against automated login attempts using breached credentials
- [ ] **Brute force** — No rate limiting or account lockout on authentication endpoints
- [ ] **Session vulnerabilities** — Predictable session IDs, session fixation, missing HttpOnly/Secure flags
- [ ] **Missing MFA** — No multi-factor authentication for sensitive accounts
- [ ] **Weak session management** — Sessions don't expire, no concurrent session limits
- [ ] **Insecure password recovery** — Weak reset tokens, predictable questions, unverified email changes
- [ ] **JWT issues** — None algorithm allowed, weak signing keys, missing expiration

**Testing Approach:**
1. Test password requirements and complexity
2. Attempt credential stuffing with known breached credentials
3. Test for brute force protection (rate limiting, CAPTCHA, lockout)
4. Analyze session handling (cookies, tokens, expiration)
5. Test password reset flows for security
6. Verify MFA implementation and bypass opportunities

---

#### A08: Software and Data Integrity Failures

> CWE-345, CWE-353, CWE-426, CWE-494, CWE-502, CWE-565, CWE-784, CWE-829, CWE-830, CWE-915

**What to Look For:**

- [ ] **Insecure deserialization** — Deserializing untrusted data (Python pickle, Java ObjectInputStream, PHP unserialize)
- [ ] **Unsigned updates** — Software updates without integrity verification
- [ ] **CI/CD attacks** — Unprotected build pipelines, compromised build agents
- [ ] **Dependency confusion** — Internal packages with names matching public packages
- [ ] **Unsigned commits** — No signature verification on code commits
- [ ] **Tamper-evident logs** — No integrity protection for audit logs
- [ ] **XML external entities (XXE)** — XML parsers with external entity processing enabled

**Testing Approach:**
1. Search for deserialization functions with user-controlled input
2. Verify update mechanisms include signature verification
3. Review CI/CD configurations for security controls
4. Check for XXE vulnerabilities in XML parsing
5. Verify integrity checks on critical data

---

#### A09: Security Logging and Monitoring Failures

> CWE-117, CWE-223, CWE-532, CWE-778, CWE-1175

**What to Look For:**

- [ ] **Missing audit logs** — No logging of authentication events, access to sensitive data, or security-critical actions
- [ ] **Insufficient log detail** — Logs don't include enough context (who, what, when, where)
- [ ] **Sensitive data in logs** — Passwords, tokens, PII logged in plaintext
- [ ] **No log protection** — Logs stored without integrity checks, accessible to attackers
- [ ] **Missing monitoring** — No alerting on suspicious activity, no SIEM integration
- [ ] **Log injection** — Attackers can forge or tamper with log entries
- [ ] **No incident response** — No documented procedures for security incidents

**Testing Approach:**
1. Review what events are logged (authentication, authorization, data access)
2. Check log format and content for sufficiency
3. Search for sensitive data in log statements
4. Verify log storage security and retention
5. Assess monitoring and alerting capabilities

---

#### A10: Server-Side Request Forgery (SSRF)

> CWE-918

**What to Look For:**

- [ ] **Unvalidated URL parameters** — User-supplied URLs fetched by the server without validation
- [ ] **Internal service access** — Can attacker reach internal services (metadata endpoints, admin panels, databases)?
- [ ] **Cloud metadata endpoints** — Access to `169.254.169.254` (AWS, Azure, GCP metadata services)
- [ ] **File protocol access** — Can `file://` URLs be used to read local files?
- [ ] **Redirect following** — Server follows redirects to attacker-controlled URLs
- [ ] **DNS rebinding** — Time-of-check vs time-of-use vulnerabilities
- [ ] **URL parsing inconsistencies** — Differences between URL parsers (e.g., `@` handling)

**Testing Approach:**
1. Identify all endpoints accepting URLs from users
2. Test for internal service access (localhost, private IPs)
3. Attempt cloud metadata endpoint access
4. Test alternative protocols (file://, gopher://, dict://)
5. Test for URL parsing bypasses (unicode, encoding, case variations)

---

### 3. Framework-Specific Checks

Apply additional checks based on detected framework:

| Framework | Key Security Checks |
|-----------|---------------------|
| **React/Next.js** | XSS via `dangerouslySetInnerHTML`, SSRF in `getServerSideProps`, API routes without auth |
| **Angular** | XSS protection bypasses, unsafe `bypassSecurityTrustHtml`, HTTP client interceptors |
| **Vue.js** | `v-html` XSS risks, server-side rendering vulnerabilities |
| **Express.js** | Missing Helmet middleware, no rate limiting, prototype pollution |
| **Django** | `DEBUG=True`, `SECRET_KEY` exposure, raw SQL, CSRF exemptions |
| **Flask** | Jinja2 autoescape disabled, unsafe session handling, debug mode |
| **Ruby on Rails** | Mass assignment, `render` with user input, SQL fragments, weak parameters |
| **Spring Boot** | SpEL injection, actuator endpoints exposed, mass assignment, CORS issues |
| **Laravel** | Mass assignment, raw queries, debug mode, configuration exposure |
| **ASP.NET Core** | Razor XSS, insecure deserialization, missing anti-forgery tokens |

---

### 4. Configuration Review

Examine these configuration areas:

#### Web Server Configuration
- **nginx/Apache**: Security headers, TLS settings, rate limiting, access controls
- **Reverse proxy**: Header forwarding, SSL termination, upstream validation
- **Load balancer**: Health checks, session affinity, DDoS protection

#### Application Configuration
- **Environment-specific settings**: Debug mode, error handling, logging levels
- **Security settings**: Password policies, session timeouts, CSRF protection
- **External integrations**: API keys, webhook secrets, OAuth configs

#### Deployment Configuration
- **Container security**: Non-root user, read-only filesystems, resource limits
- **Kubernetes**: Network policies, security contexts, RBAC
- **Cloud services**: IAM roles, security groups, encryption at rest

---

### 5. Produce Findings

For each identified vulnerability:
- Assign severity based on exploitability and impact in deployment context
- Provide concrete evidence (code locations, configuration gaps, test results)
- Propose specific remediation steps with code examples
- Rate confidence (HIGH, MEDIUM, LOW)

---

## Output Format

```markdown
## Web Security Review: [Application Name]

### Application Overview
- **Framework**: [React/Express, Django, Rails, etc.]
- **Deployment**: [Internet-facing, internal, cloud platform]
- **Architecture**: [Monolith, microservices, serverless]
- **Authentication**: [Session-based, JWT, OAuth]

### Risk Matrix
| OWASP Ref | Risk | Severity | Status |
|-----------|------|----------|--------|
| A01 | Broken Access Control | HIGH | Finding |
| A02 | Cryptographic Failures | MEDIUM | Finding |
| A03 | Injection | CRITICAL | Finding |
| A04 | Insecure Design | LOW | Finding |
| A05 | Security Misconfiguration | MEDIUM | Finding |
| A06 | Vulnerable Components | HIGH | Finding |
| A07 | Auth Failures | HIGH | Finding |
| A08 | Integrity Failures | N/A | N/A |
| A09 | Logging Failures | MEDIUM | Finding |
| A10 | SSRF | N/A | N/A |

### Findings
[Standard finding template for each identified risk]

### Positive Controls Observed
[Security controls already in place — acknowledge good practices]

### Recommendations
[Prioritized remediation roadmap]
```

---

## OWASP References

- **OWASP Top 10 for Web Applications (2021)** — [owasp.org/Top10](https://owasp.org/Top10/)
- **OWASP ASVS v5.0** — Application Security Verification Standard
- **OWASP Testing Guide (WSTG)** — Web Security Testing Guide
- **OWASP Cheat Sheet Series** — Language and framework-specific guidance
- **OWASP Proactive Controls** — Secure development practices
