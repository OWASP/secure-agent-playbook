---
title: "SA.1.4 Measuring Observability"
fiasse_section: "SA.1.4"
fiasse_version: "1.0.4"
ssem_pillar: "Maintainability"
ssem_attributes:
  - Observability
when_to_use:
  - tracking log coverage, instrumentation coverage, alert SNR, and MTTD
  - auditing structured-logging quality and code-level instrumentation
  - identifying silent failure paths
threats:
  - silent failures and exception swallowing
  - instrumentation gaps creating opaque code paths
summary: "Quantitative and qualitative measures for Observability, including structured logging review, instrumentation audits, and failure-path observability."
---

#### A.1.4. Observability

**Quantitative:**

- **Log coverage:** Percentage of trust boundaries and security-sensitive operations emitting structured log events with sufficient context (identity, action, outcome, timestamp).
- **Instrumentation coverage:** Fraction of critical execution paths exposing health and performance metrics through a standardized API (e.g., authentication failure counts, input validation error rates, resource utilization).
- **Alert signal-to-noise ratio:** Ratio of actionable alerts to total alerts fired over a reporting period. A low ratio indicates instrumentation that generates noise rather than insight.
- **Mean Time to Detect (MTTD):** Average elapsed time between an anomalous event occurring and its appearance in monitoring output. Lower values indicate more effective instrumentation.

**Qualitative/process-based:**

- **Structured logging review:** Assessment of whether log entries include sufficient context to support incident analysis. Specifically whether the who, what, where, when, and outcome of security-relevant events are captured, not just that an event occurred.
- **Code-level instrumentation audit:** Review of whether observability is built into the code itself at key points, or whether it depends entirely on external tooling. A system that is not instrumented at the code level is opaque by construction; this audit identifies those blind spots.
- **Failure-path observability:** Assessment of whether error and recovery paths produce observable output. Silent failures and exception swallowing are common gaps; code paths that produce no signal under failure conditions should be identified and instrumented.
- **UI and operator feedback review:** Assessment of whether the system surfaces meaningful state to operators and end users at decision points (including error messages, permission feedback, and session state) without leaking internal implementation details.
