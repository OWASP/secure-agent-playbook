---
title: "SA.3.3 Measuring Resilience"
fiasse_section: "SA.3.3"
fiasse_version: "1.0.4"
ssem_pillar: "Reliability"
ssem_attributes:
  - Resilience
when_to_use:
  - tracking RTO adherence and performance under stress
  - reviewing defensive coding practices
threats:
  - cascading failures and slow recovery
summary: "Quantitative and qualitative measures for Resilience."
---

#### A.3.3. Resilience

**Quantitative:**

- **Recovery Time Objective (RTO) adherence:** Frequency with which RTOs are met following an incident.
- **Performance under stress:** System performance metrics during load testing or simulated attacks (e.g., DDoS simulation).

**Qualitative/process-based:**

- **Defensive coding practices review:** Assessment of code for input validation, output encoding, and robust error handling.
- **Incident response plan effectiveness:** Review of how well the system and team recover from security incidents or operational failures.
