---
title: "CWE-16 Configuration"
cwe_id: "CWE-16"
owasp_top10: "A05:2021 Security Misconfiguration"
opencre_mappings:
  - cre_id: "180-488"
    cre_name: "Proper Configuration for all applications and frameworks"
  - cre_id: "462-245"
    cre_name: "Remove unnecessary elements from external components"
  - cre_id: "623-347"
    cre_name: "Disallow shared high privileged accounts"
when_to_use:
  - reviewing application and framework configurations
  - assessing production deployments for debug settings
  - evaluating security headers and CORS policies
  - auditing default credentials and unnecessary features
threats:
  - default credentials left in production
  - debug mode or verbose errors enabled in production
  - overly permissive CORS configurations
  - missing security headers
  - unnecessary features or admin panels exposed
summary: "Security misconfiguration occurs when applications, frameworks, or infrastructure use insecure defaults, unnecessary features, or improperly configured security controls."
---

# CWE-16: Configuration

## OpenCRE Mappings

| CRE ID | CRE Name | Link |
|--------|----------|------|
| 180-488 | Proper Configuration for all applications and frameworks | [opencre.org/cre/180-488](https://www.opencre.org/cre/180-488) |
| 462-245 | Remove unnecessary elements from external components | [opencre.org/cre/462-245](https://www.opencre.org/cre/462-245) |
| 623-347 | Disallow shared high privileged accounts | [opencre.org/cre/623-347](https://www.opencre.org/cre/623-347) |

## What to Look For

- Default credentials or sample configurations in production
- Debug endpoints, admin panels, or development tools exposed
- Missing security headers (X-Content-Type-Options, Strict-Transport-Security, etc.)
- Overly permissive CORS (Access-Control-Allow-Origin: *)
- Directory listing enabled
- Missing rate limiting on sensitive endpoints

## References

- [CWE-16](https://cwe.mitre.org/data/definitions/16.html)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
