# Examples

This directory holds two kinds of artifacts: **sample reports** (skill outputs) and **review fixtures** (skill inputs). Both are synthetic but realistic.

## Sample Reports

Skill outputs — demonstrate the format and level of detail each skill produces. Built on the standard [finding template](../templates/finding.md) and [report template](../templates/report.md).

| Example | Skill Used | Target |
|---------|-----------|--------|
| [sca-audit-sample.md](sca-audit-sample.md) | `sca-audit` | Node.js/Express project with known vulnerable dependencies |

## Review Fixtures

Skill inputs — small, intentionally vulnerable source trees used to verify agent output shape and exercise rules end-to-end. Point the relevant agent or skill at the fixture directory.

| Fixture | Skill | Platform | Contents |
|---------|-------|----------|----------|
| [mobile-android-fixture/](mobile-android-fixture/) | `mobile-code-review` | Android | `AndroidManifest.xml`, `SecretStore.kt` |
| [mobile-ios-fixture/](mobile-ios-fixture/) | `mobile-code-review` | iOS | `Info.plist`, `NetworkClient.swift` |
| [mobile-flutter-fixture/](mobile-flutter-fixture/) | `mobile-code-review` | Cross-platform shell | `pubspec.yaml`, `lib/` |
