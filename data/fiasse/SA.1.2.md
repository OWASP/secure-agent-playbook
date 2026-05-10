---
title: "SA.1.2 Measuring Modifiability"
fiasse_section: "SA.1.2"
fiasse_version: "1.0.4"
ssem_pillar: "Maintainability"
ssem_attributes:
  - Modifiability
when_to_use:
  - tracking module coupling, change impact size, and regression rate
  - assessing time-to-implement and ease-of-change qualitatively
threats:
  - high coupling causing cascading change
summary: "Quantitative and qualitative measures for Modifiability."
---

#### A.1.2. Modifiability

**Quantitative:**

- **Module coupling (afferent/efferent):** Number of incoming and outgoing dependencies for modules. Lower afferent coupling typically indicates a module is easier to change without broad impact.
- **Change impact size:** Number of files/modules typically affected by a common type of change. Smaller is better.
- **Regression rate:** Percentage of changes that introduce new defects. Lower is better.

**Qualitative/process-based:**

- **Ease of change assessment:** During code reviews, assess how difficult a hypothetical related change would be.
- **Time to implement change:** Average time to complete standard types of modifications or feature enhancements.
