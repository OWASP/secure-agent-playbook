---
title: "CWE-22 Path Traversal"
cwe_id: "CWE-22"
owasp_top10: "A01:2021 Broken Access Control"
opencre_mappings:
  - cre_id: "675-168"
    cre_name: "Sanitize filename metadata from untrusted origin if processing is required"
when_to_use:
  - reviewing file upload or download functionality
  - assessing user-supplied file paths in application code
  - evaluating MCP server tools that access the filesystem
  - auditing LLM agent tools that read or write files
threats:
  - directory traversal via ../ sequences in file paths
  - arbitrary file read via path manipulation
  - local file inclusion (LFI) via controlled path input
  - zip slip attacks via malicious archive extraction
summary: "Path traversal occurs when user-controlled input is used to construct file paths without canonicalization, allowing access to files outside intended directories."
---

# CWE-22: Path Traversal

## OpenCRE Mappings

| CRE ID | CRE Name | Link |
|--------|----------|------|
| 675-168 | Sanitize filename metadata from untrusted origin | [opencre.org/cre/675-168](https://www.opencre.org/cre/675-168) |

## What to Look For

- User input in file path construction without canonicalization
- Missing validation for `../` sequences or null bytes in file paths
- File operations using user-supplied filenames directly
- Archive extraction without path validation (zip slip)
- MCP server or LLM agent tools that accept file paths from model output

## References

- [CWE-22](https://cwe.mitre.org/data/definitions/22.html)
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
