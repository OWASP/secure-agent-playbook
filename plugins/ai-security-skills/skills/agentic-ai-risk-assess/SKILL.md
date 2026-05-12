---
name: agentic-ai-risk-assess
description: Assess agentic AI applications against the OWASP Top 10 for Agentic Applications 2026. Use when reviewing autonomous AI agents, multi-agent systems, or agentic workflows for security risks including goal hijacking, tool misuse, privilege abuse, and rogue agent behavior.
license: CC-BY-4.0
---

# Agentic AI Risk Assessment

Evaluate agentic AI applications against all 10 risk categories by following the full procedure in `plays/tier4-ai-security/agentic-ai-risk-assess.md`.

## Steps

1. **Architecture Mapping** — Identify agent type (single/multi-agent), autonomy level, tool ecosystem, memory systems, inter-agent communication protocols, and human oversight mechanisms.

2. **Assess Each Agentic Top 10 Risk**:
   - **ASI01 Agent Goal Hijack** — Hidden prompts, instruction override, silent exfiltration via copilot patterns
   - **ASI02 Tool Misuse** — Legitimate tools bent into destructive outputs, tool parameter manipulation
   - **ASI03 Identity & Privilege Abuse** — Leaked credentials, excessive permissions, agent operating beyond scope
   - **ASI04 Agentic Supply Chain** — Poisoned MCP/A2A components, runtime component tampering, dynamic ecosystem risks
   - **ASI05 Unexpected Code Execution** — Natural language execution paths leading to RCE, code generation vulnerabilities
   - **ASI06 Memory & Context Poisoning** — Long-term behavior manipulation via memory attacks, context window exploits
   - **ASI07 Insecure Inter-Agent Communication** — Spoofed messages, man-in-the-middle between agents, cluster misdirection
   - **ASI08 Cascading Failures** — False signals propagating through automated pipelines, escalating impact chains
   - **ASI09 Human-Agent Trust Exploitation** — Confident misleading explanations, social engineering of human operators
   - **ASI10 Rogue Agents** — Misalignment, concealment, self-directed action, emergent harmful behavior

3. **Synthesize Findings** — Assign severity based on exploitability and deployment context. Provide code locations, configuration gaps, and concrete remediation.

## Output

Architecture overview, risk matrix (all 10 categories with status), detailed findings using `templates/finding.md`, positive controls observed, and prioritized recommendations.

## OWASP References

- OWASP Top 10 for Agentic Applications 2026
- OWASP GenAI Security Project
- OWASP Agentic Security Initiative
