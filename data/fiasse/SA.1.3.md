---
title: "SA.1.3 Measuring Testability"
fiasse_section: "SA.1.3"
fiasse_version: "1.0.4"
ssem_pillar: "Maintainability"
ssem_attributes:
  - Testability
when_to_use:
  - tracking code coverage, unit test density, and mocking complexity
  - evaluating ease of writing tests and execution time
threats:
  - test gaps in security-relevant paths
summary: "Quantitative and qualitative measures for Testability."
---

#### A.1.3. Testability

**Quantitative:**

- **Code coverage:** Percentage of code covered by automated tests (unit, integration). Higher is generally better.
- **Unit test density:** Number of unit tests per KLoC or per class/module.
- **Mocking/stubbing complexity:** Difficulty or setup required to isolate units for testing.

**Qualitative/process-based:**

- **Ease of writing tests:** Developer feedback on how straightforward it is to write meaningful tests for new or existing code.
- **Test execution time:** Excessively long test suite runs can reduce testing frequency, indirectly affecting testability in practice.
