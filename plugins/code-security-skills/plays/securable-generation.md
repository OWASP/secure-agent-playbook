# Securable Generation — Full Loop Play

> **Status:** Stub. This play is referenced by the `securability-engineering` skill in **Full Loop Mode**. Real content is deferred to a follow-up PR.

## Intent

End-to-end securable code delivery loop: **PRD-enhance → generate → review → enhance → report**.

When activated (via `--full-loop`, "end-to-end securable", or an explicit reference), this play chains together three skills so a single user intent produces (1) a securability-enhanced requirements artifact, (2) generated code that satisfies those requirements, and (3) an SSEM scorecard validating the output.

In **Default Mode**, the `securability-engineering` skill alone handles single-shot code generation. This play is **only** for the opt-in full-loop flow.

## Procedure

TODO — formalize the loop. High-level shape:

1. **PRD enhancement** — invoke `prd-securability-enhancement` to add explicit ASVS controls and SSEM acceptance criteria to the incoming feature/spec.
2. **Generation** — invoke `securability-engineering` (Default Mode) with the enhanced PRD as input. Apply SSEM constraints and emit a Securability Notes block.
3. **Review** — invoke `securability-engineering-review` to score the generated code against the SSEM rubric and produce findings.
4. **Enhancement pass** — feed review findings back to `securability-engineering` for a remediation iteration. Bounded retries (default: 1 pass).
5. **Report** — emit a consolidated artifact: enhanced PRD + final code + SSEM scorecard + remediation diff.

## Output

TODO — define the consolidated report shape. Likely a single markdown bundle with sections: Requirements (post-enhancement), Generated Code, SSEM Scorecard, Remediation Notes.

## References

- Triggering skill: [`plugins/code-security-skills/skills/securability-engineering/SKILL.md`](../skills/securability-engineering/SKILL.md)
- Dependent skills: `prd-securability-enhancement`, `securability-engineering-review`
- FIASSE v1.0.4: `data/fiasse/` (foundational principles + SSEM attributes)
- OWASP ASVS v5.0: `data/asvs/`
