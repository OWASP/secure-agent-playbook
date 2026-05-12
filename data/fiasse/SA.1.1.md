---
title: "SA.1.1 Measuring Analyzability"
fiasse_section: "SA.1.1"
fiasse_version: "1.0.4"
ssem_pillar: "Maintainability"
ssem_attributes:
  - Analyzability
when_to_use:
  - tracking volume, duplication, unit size, and complexity
  - running developer surveys and time-to-understand assessments
threats:
  - analyzability decay obscuring vulnerabilities
summary: "Quantitative and qualitative measures for Analyzability."
---

#### A.1.1. Analyzability

**Quantitative:**

- **Volume (Lines of Code):** Tracked per module/system. Lower LoC for a given functionality can indicate better analyzability.
- **Duplication percentage:** Measured by static analysis tools (e.g., SonarQube, PMD). Lower is better.
- **Unit size (e.g., mLoC/cLoC):** Average lines of code per method or class. Excessively large units are harder to analyze.
- **Unit complexity (e.g., Cyclomatic Complexity):** Measured by static analysis tools. Lower complexity per unit is generally better.
- **Comment density/quality:** Ratio of comment lines to code lines, or qualitative review of comment usefulness.

**Qualitative/process-based:**

- **Time to Understand (TTU):** Average time for a developer unfamiliar with a section of code to understand its purpose and flow for a specific task.
- **Developer surveys:** Periodic developer ratings of the analyzability of modules they work with.
