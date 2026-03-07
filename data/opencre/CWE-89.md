---
title: "CWE-89 SQL Injection"
cwe_id: "CWE-89"
owasp_top10: "A03:2021 Injection"
opencre_mappings:
  - cre_id: "064-808"
    cre_name: "Encode output context-specifically"
  - cre_id: "732-873"
    cre_name: "Lock/precompile queries (parameterization) to avoid injection attacks"
when_to_use:
  - reviewing database query construction in application code
  - assessing ORM usage for raw query patterns
  - evaluating stored procedures or dynamic SQL
  - auditing LLM-generated SQL queries
threats:
  - SQL injection via string concatenation in queries
  - second-order SQL injection via stored data
  - blind SQL injection via boolean or time-based inference
  - SQL injection via LLM-generated queries
summary: "SQL injection occurs when untrusted data is sent to a database interpreter as part of a query, allowing attackers to read, modify, or delete data."
---

# CWE-89: SQL Injection

## OpenCRE Mappings

| CRE ID | CRE Name | Link |
|--------|----------|------|
| 064-808 | Encode output context-specifically | [opencre.org/cre/064-808](https://www.opencre.org/cre/064-808) |
| 732-873 | Lock/precompile queries (parameterization) | [opencre.org/cre/732-873](https://www.opencre.org/cre/732-873) |

## Cross-Standard References

Via OpenCRE 732-873:
- **ASVS**: V5.3.4 — Verify parameterized queries or ORM usage
- **WSTG**: WSTG-INPV-05 — Testing for SQL Injection
- **OWASP Cheat Sheet**: SQL Injection Prevention
- **NIST 800-53**: SI-10 — Information Input Validation

## What to Look For

- String concatenation or interpolation in SQL queries
- ORM raw query methods (`raw()`, `execute()`, `$queryRaw`)
- Missing parameterized queries or prepared statements
- Dynamic table/column names from user input
- LLM output passed directly to database query functions

## References

- [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
