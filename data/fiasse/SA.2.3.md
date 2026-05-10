---
title: "SA.2.3 Measuring Authenticity"
fiasse_section: "SA.2.3"
fiasse_version: "1.0.4"
ssem_pillar: "Trustworthiness"
ssem_attributes:
  - Authenticity
when_to_use:
  - tracking authentication failures and mechanism coverage
  - assessing defendability of authentication mechanisms
threats:
  - brittle authentication that cannot adapt
summary: "Quantitative and qualitative measures for Authenticity."
---

#### A.2.3. Authenticity

**Quantitative:**

- **Authentication failures:** Number of failed login attempts (can indicate brute-forcing or misconfiguration).
- **Authentication mechanism coverage:** Percentage of authentication points implementing factors appropriate to the context, with a documented rationale for each configuration choice.

**Qualitative/process-based:**

- **Verification of identities:** Review of processes for verifying user and system identities.
- **Defendability of authentication mechanisms:** Assessment of whether the authentication system's design supports ongoing analysis, modification, and verification, testability of authentication flows, auditability of authentication events, and the ability to adapt controls as threats evolve.
