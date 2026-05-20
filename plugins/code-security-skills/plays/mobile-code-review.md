# Play: Mobile Code Review

Source-only security review of native Android and iOS mobile application source code against all 8 [OWASP MASVS v2.1.0](https://mas.owasp.org/MASVS/) control groups, using extracted [MASTG](https://mas.owasp.org/MASTG/) Static Analysis content from `data/mastg/` as the per-control verification recipe. MASVS-RESILIENCE findings carry a static-only notice; MASVS-PRIVACY-2/3 findings carry a runtime-data-flow caveat.

## Trigger Conditions

Run this play when:

- A native mobile codebase or PR is under review (Android: Java/Kotlin/Gradle; iOS: Swift/Obj-C/Xcode)
- A `security-team-lead` assessment detects mobile artifacts during Phase 1 reconnaissance
- The user explicitly requests "review this mobile app for security"

Do **not** run when only built artifacts (APK/IPA) are present — flag and stop. Built-artifact static analysis is out of scope for this play.

## Inputs

- A mobile source tree (or PR diff against one)
- Optional: a target sensitivity statement (banking, healthcare, consumer, internal)
- Optional: a deployment-context statement (Play Store, App Store, enterprise distribution)

## Procedure

### 1. Scope & Context

Establish:

- Languages present (Java, Kotlin, Swift, Obj-C, Dart, JS)
- Platform(s) targeted (Android, iOS, cross-platform shell only)
- App type (consumer, banking, internal, B2B)
- Sensitive data handled (credentials, PII, financial, health)
- Exposure model (public app store, enterprise distribution, internal)

### 2. Platform Detection

Detect platform via fingerprints:

| Platform | Fingerprints |
|---|---|
| Android | `AndroidManifest.xml`, `build.gradle[.kts]`, `*.java`, `*.kt`, `src/main/AndroidManifest.xml`, `proguard-rules.pro` |
| iOS | `Info.plist`, `*.xcodeproj`, `*.xcworkspace`, `*.swift`, `*.m`, `*.mm`, `Podfile`, `Package.swift`, `*.entitlements` |
| Cross-platform shell | `pubspec.yaml` (Flutter), `package.json` with `react-native` dep, `capacitor.config.*` |

If only a cross-platform shell is detected and no native module exists, declare **partial coverage** in the scope summary and skip platform-specific signal grepping. Do not produce findings unless explicit Dart/JS-side security issues appear.

### 3. Systematic Review by MASVS Group

Walk the 8 groups in priority order. For each group, load the group overview from `data/masvs/MASVS-<GROUP>.md` and the individual controls (`MASVS-<GROUP>-<N>.md`). For each control:

1. Read the `mastg_tests:` list in the MASVS file.
2. For each MASTG test ID, load `data/mastg/MASTG-TEST-####.md`.
3. Apply the test's Static Analysis content (V1) or Steps/Observation/Evaluation (V2) to the source tree.
4. Emit findings citing the MASVS control + the MASTG test ID + version (annotate `[V1 — no V2 successor]` when the test's `upstream_version: v1-fallback`).

**Play rule — RESILIENCE caveat:** Findings against any `MASVS-RESILIENCE-*` control are static-signal-only by physics. Append the RESILIENCE static-only notice and cap confidence at MEDIUM unless backed by an unambiguous build-flag signal (e.g. a literal `android:debuggable="true"` in a release manifest, which stays HIGH). Append referenced MASTG test IDs to the dynamic-test follow-up list at the end of the report.

**Play rule — PRIVACY runtime caveat:** Findings against `MASVS-PRIVACY-2` or `MASVS-PRIVACY-3` (the data-handling-in-practice controls) cannot be fully assessed from source — they require runtime data-flow tracing. Cap confidence at LOW for any such finding that depends on data-flow inference. Append to the dynamic-test follow-up list.

**Play rule — MASTG cross-references in findings:** Each MASTG test you load may cite other MASTG entities via `@MASTG-<KIND>-####` strings in its body (e.g. `@MASTG-TECH-0056`, `@MASTG-TOOL-0073`). `data/mastg/` extracts only `MASTG-TEST-*` — the other entities (TECH, TOOL, APP, KNOW, BEST, DEMO, …) live upstream only. Surface them per-finding so the reader can follow them at the OWASP MASTG source:

1. While walking the MASTG tests that inform a finding, extract every `@MASTG-([A-Z]+)-(\d+)` from each test body.
2. Discard any match where `KIND == TEST` — already cited in `OWASP Ref`.
3. Group the remaining IDs by `KIND` alphabetically and emit a `MASTG references:` bullet on the finding. Within each KIND, sort IDs numerically. Omit the bullet entirely when the informing tests carry no non-TEST refs.
4. Do not interpret what each KIND means and do not fabricate per-page URLs. Point readers to the upstream roots once at the top of the report (see Output Format).

Per-finding rendering shape:

    - **MASTG references**:
      - TECH: MASTG-TECH-0056, MASTG-TECH-0095
      - TOOL: MASTG-TOOL-0073

**CWE mapping via MASWE (the canonical chain):**

OWASP MASWE (Mobile Application Security Weakness Enumeration) is the bridge between MASVS controls and the universal CWE catalog. Every MASWE entry maps to one or more MASVS controls AND to one or more CWE IDs — e.g. `MASWE-0041 → MASVS-AUTH-2 → CWE-603, CWE-307, CWE-287`. Enterprises standardize on CWE for risk management, so MASWE gives MASVS compatibility with the wider market.

**To populate the `CWE:` field of a mobile finding:**

1. Identify the MASVS control(s) violated by the finding (e.g. `MASVS-CRYPTO-2`).
2. Look up the corresponding MASWE entry at <https://mas.owasp.org/MASWE/> — find the MASWE entries that list this MASVS control in their mapping.
3. Use the CWE(s) listed in the matching MASWE entry as the `CWE:` field. Cite the most specific one; mention secondary CWEs in the `Impact` line if the issue is multi-faceted.

Do not invent CWE mappings or pick CWEs by visual similarity to the bug — always go through MASWE so the resulting CWE is the OWASP-blessed mapping.

**OpenCRE handling for mobile findings:**

OpenCRE does not currently treat MASVS as a first-class linked standard the way it treats ASVS, and its mobile-domain coverage is thin. For mobile findings:

- If the CWE cited has an existing pre-mapped entry in `data/opencre/CWE-XXX.md` (13 CWEs pre-mapped today), populate `OpenCRE:` from that file as usual.
- Otherwise, write `OpenCRE: N/A for mobile scan — OpenCRE's MASVS coverage is limited` in the finding. Do **not** instruct reviewers to add new OpenCRE mapping files solely to satisfy a mobile finding — that's contributor overhead with little reader benefit until OpenCRE expands its mobile coverage upstream.

#### A. MASVS-STORAGE

MASVS refs: `data/masvs/MASVS-STORAGE.md`, `MASVS-STORAGE-1.md`, `MASVS-STORAGE-2.md`
MASTG forward refs: MASTG-TEST-0001, MASTG-TEST-0003 (and per control)

| Check | Android signal | iOS signal |
|---|---|---|
| Secrets in default prefs | `SharedPreferences` for tokens | `NSUserDefaults` for tokens |
| KeyStore / Keychain misuse | Missing `EncryptedSharedPreferences`; KeyStore alias reuse | Missing/weak `kSecAttrAccessible*` |
| Backup leakage | `android:allowBackup="true"` without backup rules | `Documents/` data without `NSURLIsExcludedFromBackupKey` |
| External storage | `getExternalFilesDir` for secrets | App-group container for secrets |
| Logging | `Log.d` of secrets | `NSLog`/`print` of secrets |

#### B. MASVS-CRYPTO

MASVS refs: `data/masvs/MASVS-CRYPTO.md`, `MASVS-CRYPTO-1.md`, `MASVS-CRYPTO-2.md`
MASTG forward refs: MASTG-TEST-0011, MASTG-TEST-0013

| Check | Android signal | iOS signal |
|---|---|---|
| Weak algorithms | `Cipher.getInstance("DES")`, `MD5`, `SHA1` for security | `CC_MD5`, `CCCrypt(DES)` |
| Insecure mode | `AES/ECB` | `kCCOptionECBMode` |
| Hard-coded keys | `byte[] key = {...}` | `let key: [UInt8] = [...]` |
| Deterministic IV/nonce | `IvParameterSpec(new byte[16])` | `[UInt8](repeating: 0, count: 16)` |
| Weak RNG | `Random` for crypto | `arc4random` for cryptographic key material (use `SecRandomCopyBytes`) |

#### C. MASVS-AUTH

MASVS refs: `data/masvs/MASVS-AUTH.md`, `MASVS-AUTH-1.md`, `MASVS-AUTH-2.md`, `MASVS-AUTH-3.md`
MASTG forward refs: MASTG-TEST-0017, MASTG-TEST-0021

| Check | Android signal | iOS signal |
|---|---|---|
| Local auth bypass | JWT verified locally with hard-coded key | JWT decoded without signature verify |
| Biometric flags | `BIOMETRIC_WEAK` | `LAContext.evaluatePolicy(.deviceOwnerAuthentication)` without strong policy |
| OAuth public client | Missing PKCE | Missing PKCE |
| Token storage | Tokens in `SharedPreferences` plaintext | Tokens in `NSUserDefaults` plaintext |

#### D. MASVS-NETWORK

MASVS refs: `data/masvs/MASVS-NETWORK.md`, `MASVS-NETWORK-1.md`, `MASVS-NETWORK-2.md`
MASTG forward refs: MASTG-TEST-0024, MASTG-TEST-0026

| Check | Android signal | iOS signal |
|---|---|---|
| Cleartext traffic | `network_security_config` permits cleartext | `NSAllowsArbitraryLoads` true |
| Trust-all | Custom `TrustManager` accepting all | `URLSessionDelegate` accepts all `URLAuthenticationChallenge` |
| Pinning missing | No `CertificatePinner` (OkHttp) or no `Network Security Config` pins | No `NSPinnedDomains`; no manual `URLSession` validator |
| Mixed content | `WebView.setMixedContentMode(MIXED_CONTENT_ALWAYS_ALLOW)` | `WKWebView` configured to load mixed content |

#### E. MASVS-PLATFORM

MASVS refs: `data/masvs/MASVS-PLATFORM.md`, `MASVS-PLATFORM-1.md`, `MASVS-PLATFORM-2.md`, `MASVS-PLATFORM-3.md`
MASTG forward refs: MASTG-TEST-0030, MASTG-TEST-0033, MASTG-TEST-0035

| Check | Android signal | iOS signal |
|---|---|---|
| Exported components | `android:exported="true"` without `permission` | URL schemes registered, no validation |
| Intent / deep link | `Intent.getStringExtra` flowing to SQL/file/web | `application(_:open:)` without origin check |
| WebView bridge | `addJavascriptInterface` exposing native methods | `WKUserContentController` accepting any-origin messages |
| Screen capture | Missing `FLAG_SECURE` on sensitive activities | Missing background blur on app switch |
| Pasteboard | `ClipboardManager` for secrets | `UIPasteboard.general` for secrets |

#### F. MASVS-CODE

MASVS refs: `data/masvs/MASVS-CODE.md`, `MASVS-CODE-1.md`, `MASVS-CODE-2.md`, `MASVS-CODE-3.md`, `MASVS-CODE-4.md`
MASTG forward refs: MASTG-TEST-0040, MASTG-TEST-0042

| Check | Android signal | iOS signal |
|---|---|---|
| Outdated SDK | Old `minSdkVersion` / `compileSdkVersion` | Old deployment target |
| Vulnerable libs | Outdated `dependencies {}` versions | Outdated `Podfile.lock` / `Package.resolved` |
| Dangerous APIs | `Runtime.exec`, `WebView.evaluateJavascript` with user input | `NSTask`, `String(format:)` with user-controlled format |
| Deserialization | Untrusted `ObjectInputStream`, JSON `@JsonTypeInfo` polymorphism | `NSKeyedUnarchiver` of untrusted input |
| Error handling | Stack traces in release logs | `print(error)` to OSLog in release |

Cross-reference: defer detailed library CVE analysis to `sca-audit`.

#### G. MASVS-RESILIENCE (static signals only)

MASVS refs: `data/masvs/MASVS-RESILIENCE.md`, `MASVS-RESILIENCE-1..4.md`
MASTG entry points: `MASTG-TEST-0044` through `MASTG-TEST-0055` (load the test files referenced from each control's `mastg_tests:` list and apply their Static Analysis sections).

Useful starting-point signals while reading the MASTG content:

| Check | Android signal | iOS signal |
|---|---|---|
| Debuggable in release | `android:debuggable="true"` | `DEBUG` build configuration shipped |
| Obfuscation | Missing/empty `proguard-rules.pro`, R8 disabled | Symbols not stripped, no `bitcode` |
| Root/jailbreak detection | `RootBeer` / `SafetyNet` / Play Integrity absent | `IOSSecuritySuite` / `DTTJailbreakDetection` absent |
| Anti-debug / anti-tamper | `isDebuggerAttached` patterns absent | `ptrace(PT_DENY_ATTACH)` absent |

The RESILIENCE play rule at the top of §3 governs confidence and the dynamic-test follow-up list for every finding produced here.

#### H. MASVS-PRIVACY (partial — data-flow controls deferred)

MASVS refs: `data/masvs/MASVS-PRIVACY.md`, `MASVS-PRIVACY-1..4.md`
MASTG entry points: `MASTG-TEST-0260` through `MASTG-TEST-0263` (load the test files referenced from each control's `mastg_tests:` list and apply their Static Analysis sections).

Useful starting-point signals while reading the MASTG content:

| Check | Android signal | iOS signal |
|---|---|---|
| Permission minimization | Manifest `<uses-permission>` declared but unused | `Info.plist` `Usage Description` keys with no code path |
| Sensitive permissions | `READ_CONTACTS` + `INTERNET` co-occurrence without justification | `NSContactsUsageDescription` + analytics SDK |
| Third-party SDKs | `firebase-analytics`, `facebook-sdk`, `appsflyer`, `adjust` declared | Same Pods/Packages declared |
| Tracking transparency | n/a | `App Tracking Transparency` framework usage |
| Data exfil paths | Telemetry to non-prod endpoints | Same |

The PRIVACY play rule at the top of §3 governs confidence for any finding against `MASVS-PRIVACY-2` or `MASVS-PRIVACY-3` and appends the MASTG test IDs to the dynamic-test follow-up list.

### 4. Diff-Specific Analysis (for PRs)

When invoked on a PR diff:

- Focus on changed lines plus 3 lines of context
- Verify that pinning, permissions, manifest flags, and crypto choices were not weakened (compare new vs. old)
- Verify that any new exported activity / URL scheme has matching permission / validation
- Verify that newly-added third-party SDKs do not silently bypass network-security config

### 5. Produce Findings

Populate `templates/finding.md` exactly. The one mobile-specific extension is the `MASTG references:` bullet emitted per the cross-references play rule in §3. Per-field rules for mobile findings:

- **`CWE`** — mandatory; resolved via the MASWE chain (see §3). Verify MASWE IDs at <https://mas.owasp.org/MASWE/>.
- **`CVE`** — N/A for source-code weaknesses unless an exploited library is a direct trigger.
- **`OpenCRE`** — defaults to `N/A for mobile scan — OpenCRE's MASVS coverage is limited`; populate from `data/opencre/CWE-XXX.md` only if a pre-mapped entry exists.
- **`OWASP Ref`** — `MASVS-<GROUP>-<N>, MASWE-<NNNN>, MASTG-TEST-<NNNN> (dynamic verification recommended)` plus any overlapping `ASVS V#.#.#` or `Top 10 A##`.
- **`ID`** — assigned at report generation; leave as a placeholder during the review.
- **`Location`, `Impact`, `Evidence`, `Remediation`, `Confidence`** — per the standard template.
- **`MASTG references`** — mobile-only extension. Emit per the cross-references play rule in §3. Omit when the informing tests carry no non-TEST `@MASTG-<KIND>-####` refs.

Report-level rules:

- **Sort** findings by severity: CRITICAL > HIGH > MEDIUM > LOW > INFORMATIONAL.
- **Deduplicate** cross-group findings — e.g. a hard-coded key affecting both CRYPTO and STORAGE: keep one finding, cite the most specific MASVS control in `OWASP Ref`, and note the secondary group in `Impact`.

## Output Format

```markdown
## Mobile Code Review: [Target]

### Scope
- **Platform**: Android | iOS | both | cross-platform shell (partial coverage)
- **App type**: [consumer | banking | internal | B2B]
- **Data sensitivity**: [credentials | PII | financial | health | none]
- **Source-only confirmed**: yes | no
- **Files reviewed**: [count]

> All `MASTG-*` IDs below cross-reference OWASP MASTG.
> Canonical content: <https://github.com/OWASP/mastg> · <https://mas.owasp.org/MASTG/>

### Findings
[Standard finding template for each issue, sorted by severity. CWE resolved via the MASWE chain; OpenCRE N/A for mobile unless pre-mapped in `data/opencre/`; `OWASP Ref` carries `MASVS-<GROUP>-<N>, MASWE-<NNNN>, MASTG-TEST-<NNNN>`; each finding carries a `MASTG references:` bullet listing any non-TEST `@MASTG-<KIND>-####` cross-refs cited in the informing tests (omit when empty).]

### Positive Observations
[Security controls that ARE in place — acknowledge good practices]

### RESILIENCE Static-Only Notice
[Paragraph from the RESILIENCE block — confirms static signals only, defers runtime verification to Tier 3 `mobile-dynamic-test`]

### PRIVACY Static-Only Caveat
[Paragraph from the PRIVACY block — confirms declared-intent inspection only, defers data-flow tracing to Tier 3]

### Dynamic-Test Follow-Up
[List of MASTG-TEST IDs recommended for Tier 3 `mobile-dynamic-test`]

### Summary
| Severity | Count |
|----------|-------|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |
| INFO | N |
```

## References

- [OWASP MASVS v2.1.0](https://mas.owasp.org/MASVS/) — Mobile Application Security Verification Standard
- [OWASP MASTG](https://mas.owasp.org/MASTG/) — Mobile Application Security Testing Guide (forward references only)
- [OWASP MAS Checklist](https://mas.owasp.org/checklists/)
- [OWASP ASVS v5.0](https://owasp.org/www-project-application-security-verification-standard/) — overlapping items (V6 Cryptography, V14 Communications)
- CWE-312, CWE-327, CWE-295, CWE-926, CWE-749, CWE-200
- [OpenCRE](https://www.opencre.org) — cross-standard linking for findings
