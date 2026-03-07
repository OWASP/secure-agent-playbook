---
name: secrets-scan
description: Detect hardcoded credentials, API keys, tokens, and secrets in source code and configuration files. Use when reviewing code for leaked secrets before commit/merge, auditing a repository for credential exposure, or setting up secret detection.
license: CC-BY-4.0
---

# Secrets Scan

Detect hardcoded secrets by following the full procedure in `plays/tier1-code-analysis/secrets-scan.md`.

## Steps

1. **Run Automated Scanner** — Use available tools in preference order:
   - `trufflehog filesystem --directory=<path> --json` (recommended)
   - `trufflehog git file://<repo> --json` (includes git history)
   - `gitleaks detect --source=<path> --report-format=json`
   - `detect-secrets scan <path> --all-files`
   - If no scanner available, proceed with manual pattern analysis.

2. **Manual Pattern Analysis** — Search for high-confidence patterns:
   - AWS keys (`AKIA...`), OpenAI (`sk-...`), Anthropic (`sk-ant-...`), GitHub (`ghp_...`), Slack (`xoxb-...`), Stripe (`sk_live_...`), SendGrid (`SG.`)
   - Connection strings with embedded passwords (`://user:pass@host`)
   - Private keys (PEM headers), JWT secrets, database credentials
   - High-risk files: `.env`, `docker-compose*.yml`, `*.tfvars`, `terraform.tfstate`, `kubeconfig`, `.npmrc`, `.pypirc`

3. **Contextual Analysis** — For each detection: Is it real (not a placeholder/test fixture)? Is it active? What's the blast radius (service, permissions, prod vs dev, exposure duration)?

4. **Check Preventive Controls** — Verify: `.gitignore` covers sensitive files, pre-commit hooks for secret scanning, CI pipeline scanning, secrets management documentation.

**Important**: Never include actual secret values in findings. Show redacted versions only (e.g., `AKIA****EXAMPLE`). Active production secrets require immediate rotation.

## Output

Scan summary, findings using `templates/finding.md`, preventive controls checklist, and immediate rotation actions if needed.

## OWASP References

- A07:2021: Identification and Authentication Failures
- CWE-798: Use of Hard-coded Credentials
- CWE-312: Cleartext Storage of Sensitive Information
