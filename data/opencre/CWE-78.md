---
title: "CWE-78 OS Command Injection"
cwe_id: "CWE-78"
owasp_top10: "A03:2021 Injection"
opencre_mappings:
  - cre_id: "857-718"
    cre_name: "Protect against OS command injection attack"
  - cre_id: "683-722"
    cre_name: "Block direct execution of file metadata from untrusted origin"
when_to_use:
  - reviewing code that invokes shell commands or system processes
  - assessing LLM agents that run tools via shell
  - evaluating CI/CD pipelines for command injection risks
  - auditing MCP server tools that run system commands
threats:
  - command injection via unsanitized user input in shell calls
  - argument injection via special characters in command parameters
  - command injection via LLM-generated tool invocations
  - indirect injection via filenames or metadata containing shell metacharacters
summary: "OS command injection occurs when untrusted data is passed to system shell commands without proper sanitization, allowing attackers to run arbitrary commands."
---

# CWE-78: OS Command Injection

## OpenCRE Mappings

| CRE ID | CRE Name | Link |
|--------|----------|------|
| 857-718 | Protect against OS command injection attack | [opencre.org/cre/857-718](https://www.opencre.org/cre/857-718) |
| 683-722 | Block direct file metadata execution from untrusted origin | [opencre.org/cre/683-722](https://www.opencre.org/cre/683-722) |

## What to Look For

- User input in system(), popen(), or subprocess calls without sanitization
- Shell interpolation of variables in command strings
- Missing use of array-based process invocation (safer than shell strings)
- LLM agent tools that construct shell commands from model output
- MCP server tools accepting free-form command parameters

## References

- [CWE-78](https://cwe.mitre.org/data/definitions/78.html)
- [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
