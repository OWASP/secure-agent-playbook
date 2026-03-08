---
title: "Secure API Design Checklist"
domain: "design"
when_to_use:
  - designing new API endpoints or services
  - reviewing API architecture for security-by-default patterns
  - building API specifications with security requirements
  - evaluating API resilience and error handling patterns
threats:
  - missing or weak authentication and authorization
  - unvalidated inputs enabling injection attacks
  - sensitive data exposure in URLs, logs, or error messages
  - missing rate limiting enabling abuse
  - insecure cryptographic choices
summary: "Secure-by-default API design checklist covering maintainability, resilience, authentication, data protection, input validation, logging, and testing — aligned with OWASP API Security Top 10."
owasp_references: ["API1:2023", "API2:2023", "API3:2023", "API4:2023", "API8:2023"]
---

# Secure API Design Checklist

Apply these security principles when building API functionality. Addresses OWASP API Security Top 10 risks.

## Maintainability

- [ ] Modularize security logic (auth, validation, error handling) for clean reuse and updates
- [ ] Centralize security configs under version control — no hardcoding
- [ ] Standardize error/response schemas and log structures across services
- [ ] Document decisions and security trade-offs using OpenAPI or Markdown files
- [ ] Add regression tests for known vulnerabilities and past pentest findings

## Resilience

- [ ] Apply rate limiting and throttling (per token/IP/etc.) with clear failure responses (`429`)
- [ ] Use circuit breakers and fallback logic for dependencies and external services
- [ ] Gracefully handle errors without crashing; log details, return stable responses
- [ ] Implement liveness/readiness health checks and configure upstream timeouts
- [ ] Periodically load test and simulate failures to verify API behavior under stress

## Authentication & Authorization

- [ ] Use OAuth 2.0 with PKCE or OpenID Connect; avoid Basic Auth
- [ ] Enforce strong JWT validation (`alg`, expiration, issuer)
- [ ] Store secrets in a vault — never in code or configs
- [ ] Apply RBAC: check user permissions on every request
- [ ] Validate `redirect_uri` and use the `state` parameter in OAuth flows
- [ ] Secure all endpoints by default; document exceptions explicitly

## Data Protection

- [ ] Enforce HTTPS (TLS 1.2 or higher) and use strong cipher suites
- [ ] Add HSTS headers with preload and `includeSubDomains`
- [ ] Encrypt sensitive data at rest with AES-256 GCM or equivalent
- [ ] Never log or expose secrets, tokens, or PII in URLs or error messages
- [ ] Use vetted cryptographic libraries (e.g. libsodium, BouncyCastle)

## Input Validation

- [ ] Validate all inputs server-side (headers, body, query, etc.)
- [ ] Use JSON Schema or shared validators across services
- [ ] Enforce proper `Content-Type` and `Accept` headers
- [ ] Use parameterized queries — never build SQL strings manually
- [ ] Disable DTDs and external entities in XML parsers

## Logging & Error Handling

- [ ] Log authentication failures, denied access, and system errors
- [ ] Avoid logging secrets, passwords, or sensitive identifiers
- [ ] Send users generic error messages (e.g., "Invalid input"); log details internally
- [ ] Use correlation IDs in logs to trace request chains

## Testing & Deployment

- [ ] Write tests for authentication, validation, and error-handling flows
- [ ] Include negative tests (e.g., tampered tokens, malformed input)
- [ ] Store configs (e.g., allowed HTTP methods, token expiry) in version control
- [ ] Keep dependencies updated; review security PRs with intention

## References

- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/)
- [OWASP API Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
