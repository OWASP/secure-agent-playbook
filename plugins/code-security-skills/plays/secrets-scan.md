# Play: Secrets Scan

Detect hardcoded credentials, API keys, tokens, and other secrets in source code and configuration files.

## Trigger Conditions

Use this skill when:
- Reviewing code for leaked secrets before commit or merge
- Auditing a repository for historical secret exposure
- A user asks to check for hardcoded credentials
- Setting up pre-commit hooks for secret detection

## Inputs

- Repository or directory to scan
- (Optional) List of known-safe patterns to ignore (e.g., test fixtures, example placeholders)
- (Optional) Whether to scan git history or just current files

## Procedure

### 1. Run Automated Scanner

Use available tools in order of preference:

1. **trufflehog** (recommended — scans current files + git history):
   ```bash
   trufflehog filesystem --directory=<path> --json
   trufflehog git file://<repo_path> --json  # includes git history
   ```

2. **gitleaks** (git-aware scanning):
   ```bash
   gitleaks detect --source=<path> --report-format=json --report-path=results.json
   ```

3. **detect-secrets** (Yelp's baseline-aware scanner):
   ```bash
   detect-secrets scan <path> --all-files
   ```

If no scanner is installed, proceed with manual analysis.

### 2. Manual Pattern Analysis

Search for these high-confidence patterns:

#### API Keys & Tokens
| Pattern | Service | Regex Hint |
|---------|---------|-----------|
| `AKIA[0-9A-Z]{16}` | AWS Access Key ID | Exact format |
| `sk-[a-zA-Z0-9]{48}` | OpenAI API Key | Prefix match |
| `sk-ant-[a-zA-Z0-9-]{80,}` | Anthropic API Key | Prefix match |
| `ghp_[a-zA-Z0-9]{36}` | GitHub Personal Access Token | Prefix match |
| `gho_`, `ghu_`, `ghs_`, `ghr_` | GitHub OAuth/App tokens | Prefix match |
| `xoxb-`, `xoxp-`, `xoxs-` | Slack tokens | Prefix match |
| `SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}` | SendGrid API Key | Format match |
| `sk_live_`, `pk_live_`, `rk_live_` | Stripe keys | Prefix match |

#### Credentials in Config
| Pattern | What to Look For |
|---------|-----------------|
| Connection strings | `://user:password@host` patterns |
| Password assignments | `password = "..."`, `PASSWORD: ...`, `passwd`, `secret` |
| Private keys | `-----BEGIN (RSA\|EC\|OPENSSH) PRIVATE KEY-----` |
| Certificates | PEM-encoded certificates with private key material |
| JWT secrets | `JWT_SECRET`, `TOKEN_SECRET` assignments |
| Database credentials | `DB_PASSWORD`, `MONGO_URI`, `DATABASE_URL` with embedded credentials |

#### High-Risk File Patterns
Scan these files with extra scrutiny:
- `.env`, `.env.*` files
- `**/config/**`, `**/settings/**`
- `docker-compose*.yml` (environment sections)
- `*.tfvars`, `terraform.tfstate`
- `kubeconfig`, `*.kubeconfig`
- `credentials`, `credentials.json`, `service-account*.json`
- `.npmrc`, `.pypirc`, `pip.conf` (registry tokens)
- `**/ci/**`, `.github/workflows/**` (inline secrets)

### 3. Contextual Analysis

For each detected secret:

1. **Is it real?** Filter out:
   - Placeholder values (`CHANGE_ME`, `xxx`, `your-api-key-here`, `<token>`)
   - Test fixtures with known dummy values
   - Documentation examples
   - Base64-encoded non-secret data that matches key patterns

2. **Is it active?** If possible:
   - Check if the key format is currently valid for the service
   - Look for rotation evidence (was it replaced in a later commit?)
   - Check `.gitignore` — is the file supposed to be excluded?

3. **What's the blast radius?**
   - What service does this credential access?
   - What permissions does it grant?
   - Is it a production or development credential?
   - How long has it been exposed?

### 4. Check Preventive Controls

Verify that the project has:
- [ ] `.gitignore` entries for sensitive files (`.env`, `*.key`, `*.pem`, tfstate, etc.)
- [ ] Pre-commit hooks for secret scanning (trufflehog, gitleaks, detect-secrets)
- [ ] CI pipeline secret scanning step
- [ ] Documentation on how to manage secrets (env vars, vault, etc.)
- [ ] `.gitleaks.toml` or equivalent allowlist config for known false positives

## Output Format

```markdown
## Secrets Scan: [Repository/Directory]

### Scan Summary
- **Scanner used**: [tool or manual]
- **Scope**: Current files | Git history | Both
- **Files scanned**: [count]
- **Secrets found**: [count by category]

### Findings
[Standard finding template for each secret, with type and blast radius]

### Preventive Controls
| Control | Status |
|---------|--------|
| .gitignore covers sensitive files | Present/Missing |
| Pre-commit secret scanning | Present/Missing |
| CI secret scanning | Present/Missing |

### Immediate Actions Required
[If active production secrets are found, list rotation steps]
```

## Important Notes

- **Never include the actual secret value in findings.** Show a redacted version: `AKIA****EXAMPLE`
- If active production secrets are found, flag this as requiring **immediate rotation** — the secret must be assumed compromised once it's been in version control
- Historical secrets in git history remain accessible even after deletion from current files — git history rewriting or rotation is required

## OWASP References

- **A07:2021** — Identification and Authentication Failures
- **CWE-798** — Use of Hard-coded Credentials
- **CWE-312** — Cleartext Storage of Sensitive Information
- OWASP Cheat Sheet: Secrets Management
- OWASP WSTG-CONF-04: Review Old Backup and Unreferenced Files for Sensitive Information
