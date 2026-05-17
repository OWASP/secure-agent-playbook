# Play: Software Composition Analysis Audit

Scan project dependencies for known vulnerabilities (CVEs), produce severity-ranked findings with remediation guidance.

## Trigger Conditions

Use this skill when:
- Reviewing a project's dependency files (package.json, requirements.txt, go.mod, pom.xml, Gemfile, Cargo.toml, etc.)
- A user asks to check for vulnerable dependencies
- Performing a pre-deployment security review
- Triaging a Dependabot/Renovate alert

## Inputs

- Project root directory (must contain dependency manifests and/or lockfiles)
- (Optional) Severity threshold — minimum severity to report (default: MEDIUM)
- (Optional) Ignore list — CVEs to suppress (with documented justification)

## Procedure

### 1. Identify Dependency Manifests

Scan for all dependency files in the project:

| Ecosystem | Manifest | Lockfile |
|-----------|----------|----------|
| Node.js | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| Python | requirements.txt, setup.py, pyproject.toml | Pipfile.lock, poetry.lock |
| Go | go.mod | go.sum |
| Java/Kotlin | pom.xml, build.gradle | gradle.lockfile |
| Ruby | Gemfile | Gemfile.lock |
| Rust | Cargo.toml | Cargo.lock |
| .NET | *.csproj, packages.config | packages.lock.json |
| PHP | composer.json | composer.lock |

Prefer lockfiles over manifests — they capture the exact resolved versions including transitive dependencies.

### 2. Run Vulnerability Scan

Use available tools in order of preference:

1. **osv-scanner** (recommended — uses OSV.dev database, covers all ecosystems):
   ```bash
   osv-scanner --lockfile=<lockfile_path> --format=json
   ```

2. **npm audit** (Node.js projects):
   ```bash
   npm audit --json
   ```

3. **pip-audit** (Python projects):
   ```bash
   pip-audit -r requirements.txt --format=json
   ```

4. **govulncheck** (Go projects):
   ```bash
   govulncheck ./...
   ```

5. **trivy** (multi-ecosystem, container images too):
   ```bash
   trivy fs --format json --scanners vuln <project_path>
   ```

If no scanner is installed, **stop and ask the user to install one** rather than attempting manual analysis. Even small projects have 50+ dependencies — manually cross-referencing versions against CVE databases is not cost-effective. Recommend:
```bash
# Fastest to install, covers all ecosystems
brew install osv-scanner    # or: npm install -g osv-scanner
# Node.js projects already have this
npm audit --json
```

For manual triage of individual packages, use the [OSV.dev vulnerability database](https://osv.dev/list) to search by package name or CVE.

### 3. Analyze Results

For each vulnerability found:

1. **Determine reachability**: Is the vulnerable code path actually used by this project?
   - Check import statements and usage patterns
   - A vulnerability in an unused function of a dependency is lower priority
2. **Check exploitability context**: Is the vulnerability exploitable in this deployment?
   - A client-side library vuln in a server-only project may not apply
   - A DoS vulnerability may be less critical for internal tools
3. **Identify fix availability**: Is there a patched version?
   - Check if upgrading is a minor/patch bump (low risk) or major bump (breaking changes)
   - Check if the fix is in a direct dependency or requires bumping a transitive dep

### 4. Produce Findings

For each confirmed vulnerability, generate a finding with:
- CVE/GHSA identifier
- Affected package and version
- Fixed version (if available)
- CVSS score and severity
- Whether the vulnerable code path is reachable
- Upgrade command to fix

### 5. Generate Dependency Health Summary

Beyond CVEs, flag:
- **Unmaintained packages**: No commits in 2+ years, archived repos
- **Typosquatting risk**: Package names that are suspiciously similar to popular packages
- **License concerns**: Packages with no license or unexpected license changes
- **Pinning issues**: Using ranges (^, ~) instead of exact versions in production lockfiles

## Output Format

```markdown
## SCA Audit: [Project Name]

### Scan Summary
- **Ecosystems**: [Node.js, Python, etc.]
- **Total dependencies**: [N direct, M transitive]
- **Scanner used**: [tool name and version]
- **Vulnerabilities found**: [X critical, Y high, Z medium, W low]

### Critical & High Findings
[Standard finding template for each, sorted by severity]

### Medium & Low Findings
[Condensed table format]
| Package | Version | CVE | Severity | Fixed In | Reachable? |
|---------|---------|-----|----------|----------|------------|

### Dependency Health
[Flags for unmaintained, license, pinning issues]

### Remediation Commands
[Exact commands to fix — e.g., `npm install package@version`]
```

## OWASP References

- **A06:2021** — Vulnerable and Outdated Components
- OWASP Dependency-Check
- OWASP Software Component Verification Standard (SCVS)
- OWASP Cheat Sheet: Vulnerable Dependency Management
