---
name: sca-audit
description: Scan project dependencies for known vulnerabilities (CVEs). Use when reviewing dependency files (package.json, requirements.txt, go.mod, pom.xml, Gemfile, Cargo.toml, etc.), triaging Dependabot/Renovate alerts, or performing pre-deployment security checks.
license: CC-BY-4.0
---

# Software Composition Analysis Audit

Scan dependencies for known CVEs by following the full procedure in `plays/tier1-code-analysis/sca-audit.md`.

## Steps

1. **Identify Dependency Manifests** — Scan for all dependency files and lockfiles across ecosystems (Node.js, Python, Go, Java, Ruby, Rust, .NET, PHP). Prefer lockfiles for exact resolved versions.

2. **Run Vulnerability Scan** — Use available tools in preference order:
   - `osv-scanner --lockfile=<path> --format=json` (recommended, multi-ecosystem)
   - `npm audit --json` (Node.js)
   - `pip-audit -r requirements.txt --format=json` (Python)
   - `govulncheck ./...` (Go)
   - `trivy fs --format json --scanners vuln <path>` (multi-ecosystem)
   - If no scanner is installed, **stop and ask the user to install one** (e.g., `brew install osv-scanner`). Manual analysis is not viable — even small projects have 50+ dependencies. For individual package triage, point the user to [OSV.dev](https://osv.dev/list).

3. **Analyze Results** — For each vulnerability: determine reachability (is the vulnerable code path used?), check exploitability context (deployment matters), and identify fix availability (patch vs major version bump).

4. **Dependency Health** — Beyond CVEs, flag unmaintained packages (2+ years inactive), typosquatting risks, license concerns, and version pinning issues.

## Output

Scan summary (ecosystems, dependency count, scanner used), findings sorted by severity using `templates/finding.md`, condensed table for medium/low, dependency health flags, and exact remediation commands.

## OWASP References

- A06:2021: Vulnerable and Outdated Components
- OWASP Dependency-Check
- OWASP SCVS
