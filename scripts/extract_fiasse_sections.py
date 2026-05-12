#!/usr/bin/env python3
"""
Extract FIASSE framework sections (v1.0.4) into structured markdown files
with YAML frontmatter.

Parses the FIASSE framework markdown (from OWASP/FIASSE,
file `docs/securable_framework.md`) and produces one file per logical section
under data/fiasse/. Each output file has YAML frontmatter (title,
fiasse_section, ssem_pillar, ssem_attributes, when_to_use, threats, summary)
followed by the section content.

Section files are named S{x.y.z}.md (e.g. S3.2.1.4.md for Observability,
SA.1.4.md for the Appendix A measurement subsection).

Updated for FIASSE v1.0.4. The v1.0.4 framework introduces:
  - Observability as a 10th SSEM attribute (under Maintainability)
  - The Principle of Least Astonishment (Section 2.6)
  - The Boundary Control Principle (Section 4.3, formerly "Flexibility")
  - Dependency Stewardship (Section 4.6)
  - Measurement guidance moved to Appendix A (formerly Section 3.4)
  - Major chapter renumbering (old 4.x -> 5.x, 5.x -> 6.x, 6.x -> 4.x, etc.)

Default upstream source:
  https://raw.githubusercontent.com/OWASP/FIASSE/refs/tags/v1.0.4/docs/securable_framework.md
"""

import re
import sys
import textwrap
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Section metadata registry
# ---------------------------------------------------------------------------
# Maps section_id -> metadata dict. Each entry defines the frontmatter fields
# that cannot be inferred from the framework text alone (when_to_use, threats,
# summary, and optionally ssem_pillar / ssem_attributes).

SECTION_META: dict[str, dict] = {
    # -----------------------------------------------------------------------
    # 1. Introduction
    # -----------------------------------------------------------------------
    "1.1": {
        "title": "The Application Security Challenge",
        "when_to_use": [
            "understanding why application security initiatives struggle",
            "framing the business case for securable code practices",
            "assessing friction between AppSec and Development teams",
            "evaluating the impact of generative AI on AppSec outcomes",
        ],
        "threats": [
            "slow progress in application security outcomes",
            "friction between AppSec and Development teams",
            "AI-generated code amplifying past security mistakes",
            "shift-left initiatives that fail to produce lasting change",
        ],
        "summary": (
            "The core challenge: organizations invest significantly in AppSec yet "
            "often see limited outcomes. Shift-left has underdelivered, AI code "
            "generation amplifies risk, and developers lack deep security expertise."
        ),
    },
    "1.2": {
        "title": "Document Purpose and Scope",
        "when_to_use": [
            "understanding the scope and audience of FIASSE",
            "distinguishing FIASSE from SSEM",
            "mapping FIASSE to organizational roles (AppSec, Product Security)",
            "introducing the term 'securable' versus 'secure'",
        ],
        "threats": [
            "misunderstanding the framework scope",
            "siloed security functions lacking a unifying framework",
        ],
        "summary": (
            "Defines FIASSE as the overarching strategic framework and SSEM as the "
            "design language model within it. Introduces the deliberate term "
            "'securable' over 'secure'."
        ),
    },
    # -----------------------------------------------------------------------
    # 2. Foundational Principles
    # -----------------------------------------------------------------------
    "2.1": {
        "title": "The Securable Paradigm: No Static Secure State",
        "when_to_use": [
            "explaining the difference between secure and securable",
            "challenging binary secure/insecure classification",
            "advocating for adaptive security posture",
            "applying the securable paradigm to features (e.g., Defendable Authentication)",
        ],
        "threats": [
            "treating security as a binary state",
            "brittle security that breaks when software changes",
            "failure to adapt to evolving threat landscape",
        ],
        "summary": (
            "There is no static state of secure. Software must be built with inherent "
            "qualities that enable it to adapt to evolving threats."
        ),
    },
    "2.2": {
        "title": "Resiliently Add Computing Value",
        "when_to_use": [
            "framing the primary directive of software engineering",
            "connecting security to business value creation",
            "justifying securable attributes as engineering requirements",
        ],
        "threats": [
            "software that cannot withstand change or stress",
            "security treated as separate from core engineering",
        ],
        "summary": (
            "The primary directive: resiliently add computing value -- code that is "
            "robust enough to withstand change, stress, and attack."
        ),
    },
    "2.3": {
        "title": "Security Mission: Reducing Material Impact",
        "when_to_use": [
            "defining the core mission of cybersecurity",
            "aligning security strategy with business objectives",
            "setting realistic security goals beyond breach elimination",
        ],
        "threats": [
            "pursuing the illusory goal of complete breach elimination",
            "security strategies misaligned with business objectives",
        ],
        "summary": (
            "The core mission is to reduce the probability of material impact of a "
            "cyber event. Security strategies must align with business objectives."
        ),
    },
    "2.4": {
        "title": "Aligning Security with Development",
        "when_to_use": [
            "integrating security into development using engineering terminology",
            "empowering developers to address security confidently",
            "calibrating mindset expectations between security and development",
            "engaging AppSec early in requirements and design",
        ],
        "threats": [
            "imposing security-centric jargon that disrupts development",
            "expecting developers to adopt adversarial mindsets as primary defense",
            "AppSec engaging too late in the SDLC to add value",
        ],
        "summary": (
            "Security and development are complementary disciplines. True alignment "
            "uses established software engineering terms and engages AppSec early "
            "(Participation over Assessment)."
        ),
    },
    "2.5": {
        "title": "The Transparency Principle",
        "ssem_attributes": ["Observability", "Accountability"],
        "when_to_use": [
            "designing observable and auditable systems",
            "implementing logging and instrumentation strategies",
            "evaluating system transparency for security analysis",
            "connecting transparency to Maintainability and Trustworthiness",
        ],
        "threats": [
            "opaque systems that resist security analysis",
            "reactive security posture due to lack of observability",
            "insufficient audit trails for incident response",
        ],
        "summary": (
            "Transparency is a foundational engineering strategy: designing systems so "
            "internal state and behavior are observable and understandable to "
            "authorized parties."
        ),
    },
    "2.6": {
        "title": "The Principle of Least Astonishment",
        "ssem_attributes": ["Analyzability", "Modifiability"],
        "when_to_use": [
            "designing intuitive and predictable system behavior",
            "reviewing code for surprising or hidden side effects",
            "establishing consistent naming and error-handling conventions",
            "complementing transparency with predictable behavior",
        ],
        "threats": [
            "unexpected behavior that hides security-relevant decisions",
            "hidden side effects that bypass intended boundaries",
            "inconsistent interfaces that obscure trust assumptions",
        ],
        "summary": (
            "Systems should behave in ways that are intuitive and predictable. POLA "
            "supports Analyzability, Modifiability, and clearer security boundaries; "
            "it works in concert with the Transparency Principle."
        ),
    },
    # -----------------------------------------------------------------------
    # 3. The Securable Software Engineering Model (SSEM)
    # -----------------------------------------------------------------------
    "3.1": {
        "title": "Model Overview and Design Language",
        "ssem_pillar": "All",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability", "Observability",
            "Confidentiality", "Accountability", "Authenticity",
            "Availability", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "introducing SSEM to a development team",
            "understanding the SSEM attribute taxonomy",
            "using SSEM as a design language for security discussions",
            "shifting the security question from binary to attribute-based",
        ],
        "threats": [
            "binary secure/insecure assessment without nuance",
            "security jargon that excludes developers",
            "find-and-fix monotony that does not scale",
        ],
        "summary": (
            "SSEM provides a design language using established software engineering "
            "terms. Ten attributes grouped into three pillars (Maintainability, "
            "Trustworthiness, Reliability)."
        ),
    },
    "3.2": {
        "title": "Core Securable Attributes",
        "ssem_pillar": "All",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability", "Observability",
            "Confidentiality", "Accountability", "Authenticity",
            "Availability", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "introducing the SSEM attribute set as a whole",
            "framing the attributes as concrete engineering qualities",
        ],
        "threats": [
            "treating securable attributes as abstract goals rather than measurable qualities",
        ],
        "summary": (
            "The building blocks of securable software: tangible characteristics that "
            "contribute directly to a system's security and resilience."
        ),
    },
    "3.2.1": {
        "title": "Maintainability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Analyzability", "Modifiability", "Testability", "Observability"],
        "when_to_use": [
            "reviewing code for maintainability attributes",
            "framing maintainability as a securable attribute",
        ],
        "threats": [
            "undetected vulnerabilities due to complex code",
            "slow vulnerability remediation",
            "introducing defects during security fixes",
        ],
        "summary": (
            "Maintainability encompasses Analyzability, Modifiability, Testability, "
            "and Observability -- the ability to evolve, correct, adapt, and observe "
            "software in operation."
        ),
    },
    "3.2.1.1": {
        "title": "Analyzability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Analyzability"],
        "when_to_use": [
            "assessing analyzability of a codebase",
            "evaluating ability to locate causes of behavior in code",
            "establishing analyzability metrics for review",
        ],
        "threats": [
            "complex or duplicated code that obscures vulnerabilities",
            "outsized units that resist analysis",
            "imbalanced components that hide failure causes",
        ],
        "summary": (
            "The ability to locate the cause of a behavior within the code. Drives "
            "the speed and accuracy of vulnerability remediation."
        ),
    },
    "3.2.1.2": {
        "title": "Modifiability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Modifiability"],
        "when_to_use": [
            "evaluating modifiability of a system",
            "assessing impact and coupling for safe change",
            "planning rapid response to newly discovered vulnerabilities",
        ],
        "threats": [
            "tightly coupled modules causing cascading change",
            "complex units that are hard to modify safely",
            "duplicated code producing inconsistent fixes",
        ],
        "summary": (
            "The ability to change code without breaking existing functionality or "
            "introducing new vulnerabilities. Enables rapid response to evolving threats."
        ),
    },
    "3.2.1.3": {
        "title": "Testability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Testability"],
        "when_to_use": [
            "checking testability of code under review",
            "designing isolated, automatable test surfaces",
            "scaling security assurance via automated tests",
        ],
        "threats": [
            "untestable code masking regressions",
            "tightly coupled units that resist isolation",
            "test gaps in security-relevant paths",
        ],
        "summary": (
            "The ability to write a test for a piece of code without modifying the "
            "code under test. Enables continuous verification of security controls."
        ),
    },
    "3.2.1.4": {
        "title": "Observability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Observability"],
        "when_to_use": [
            "designing logging, monitoring, and instrumentation",
            "evaluating runtime visibility of system behavior",
            "auditing whether observability is built into the code rather than bolted on",
            "designing UI feedback that surfaces meaningful state",
        ],
        "threats": [
            "opaque systems that depend on external tooling alone",
            "silent failures and exception swallowing",
            "log entries lacking sufficient context for incident analysis",
        ],
        "summary": (
            "The degree to which the internal state of a system can be inferred from "
            "its external outputs. Achieved through code-level instrumentation: "
            "structured logging, monitoring, instrumentation, and UI feedback."
        ),
    },
    "3.2.2": {
        "title": "Trustworthiness",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Confidentiality", "Accountability", "Authenticity"],
        "when_to_use": [
            "reviewing code for trustworthiness attributes",
            "assessing inherent qualities versus overlaid security controls",
        ],
        "threats": [
            "unauthorized data disclosure",
            "inability to trace actions to entities",
            "identity spoofing and non-repudiation failures",
        ],
        "summary": (
            "Trustworthiness encompasses Confidentiality, Accountability, and "
            "Authenticity -- the ability to meet stakeholder expectations in a "
            "verifiable way."
        ),
    },
    "3.2.2.1": {
        "title": "Confidentiality",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Confidentiality"],
        "when_to_use": [
            "assessing data protection at rest, in transit, and in use",
            "reviewing access controls and disclosure boundaries",
        ],
        "threats": [
            "unauthorized access to sensitive data",
            "leakage of information across trust boundaries",
        ],
        "summary": (
            "Property that information is not disclosed to unauthorized individuals, "
            "entities, or processes. Achieved through inherent protective qualities, "
            "not overlaid controls alone."
        ),
    },
    "3.2.2.2": {
        "title": "Accountability",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Accountability"],
        "when_to_use": [
            "evaluating audit trail design",
            "designing principal management and access attribution",
            "supporting incident response with traceable actions",
        ],
        "threats": [
            "actions that cannot be uniquely attributed to entities",
            "insufficient audit trails for incident response",
        ],
        "summary": (
            "Every action within a system is attributable to a specific, identified "
            "entity. Enables auditing and incident response."
        ),
    },
    "3.2.2.3": {
        "title": "Authenticity",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Authenticity"],
        "when_to_use": [
            "implementing or reviewing authentication mechanisms",
            "designing Defendable Authentication features",
            "applying signatures and certificates for identity verification",
        ],
        "threats": [
            "identity spoofing",
            "non-repudiation failures",
            "brittle authentication that cannot adapt to new attack patterns",
        ],
        "summary": (
            "The property that an entity is what it claims to be. Includes Defendable "
            "Authentication, digital signatures, and supporting non-repudiation."
        ),
    },
    "3.2.3": {
        "title": "Reliability",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Availability", "Integrity", "Resilience"],
        "when_to_use": [
            "reviewing code for reliability attributes",
            "assessing predictable operation under adverse conditions",
        ],
        "threats": [
            "denial of service attacks",
            "unauthorized data modification or corruption",
            "system failures and inability to recover",
        ],
        "summary": (
            "Reliability encompasses Availability, Integrity, and Resilience -- "
            "consistent and predictable operation under adverse conditions."
        ),
    },
    "3.2.3.1": {
        "title": "Availability",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Availability"],
        "when_to_use": [
            "assessing uptime and recovery design",
            "designing resistance to DDoS and similar attacks",
        ],
        "threats": [
            "denial of service attacks",
            "extended downtime from unmonitored failure modes",
        ],
        "summary": (
            "Property of being accessible and usable on demand by authorized "
            "entities, including during adverse circumstances."
        ),
    },
    "3.2.3.2": {
        "title": "Integrity",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Integrity"],
        "when_to_use": [
            "evaluating data and system integrity",
            "applying derived integrity to business-critical state",
            "implementing cryptographic hashing, checksums, and access controls",
        ],
        "threats": [
            "unauthorized modification of code, configuration, or data",
            "business logic manipulation through client-supplied state",
        ],
        "summary": (
            "Property of accuracy and completeness. Applies at both system and data "
            "levels; supported by the Derived Integrity Principle (Section 4.4.1.2)."
        ),
    },
    "3.2.3.3": {
        "title": "Resilience",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Resilience"],
        "when_to_use": [
            "designing for fault tolerance and graceful degradation",
            "reviewing recovery and error-handling paths",
            "applying defensive coding (Section 4.4)",
        ],
        "threats": [
            "cascading failures from unhandled component faults",
            "non-graceful failure that exposes system internals",
        ],
        "summary": (
            "The ability of a system to continue operating during and after failure, "
            "and to recover. Includes fault tolerance, defensive coding, and strong "
            "trust boundaries."
        ),
    },
    # -----------------------------------------------------------------------
    # 4. Practical Guidance for Securable Software Development
    # -----------------------------------------------------------------------
    "4.1": {
        "title": "Establishing Clear Expectations",
        "when_to_use": [
            "setting security expectations for development teams",
            "integrating security into requirements gathering",
            "improving proactive communication between AppSec and Dev",
        ],
        "threats": [
            "unclear security expectations leading to missing controls",
            "security imposed as afterthought rather than requirement",
            "implementation deficient by design due to incomplete requirements",
        ],
        "summary": (
            "Clear expectations through proactive communication and integrating "
            "security into requirements (features, threat scenarios, acceptance criteria)."
        ),
    },
    "4.1.1": {
        "title": "Proactive Communication",
        "when_to_use": [
            "rolling out new security testing initiatives to developers",
            "establishing regular AppSec-Development synchronization",
        ],
        "threats": [
            "AppSec initiatives launched without dev awareness or buy-in",
            "loss of momentum after initial security rollouts",
        ],
        "summary": (
            "Inform development teams about new initiatives, demonstrate tools, and "
            "maintain regular synchronization to sustain partnership."
        ),
    },
    "4.1.2": {
        "title": "Integrating Security into Requirements",
        "when_to_use": [
            "authoring security features, threat scenarios, and acceptance criteria",
            "moving security from post-development review to integral requirement",
            "establishing measurable security outcomes via implementation completeness",
        ],
        "threats": [
            "security gaps rooted in requirements that never specified them",
            "QA unable to verify security expectations because none were defined",
        ],
        "summary": (
            "Active AppSec participation in requirements gathering. Key deliverables: "
            "Security Features, Threat Scenarios, and Security Acceptance Criteria."
        ),
    },
    "4.2": {
        "title": "Threat Modeling",
        "when_to_use": [
            "performing threat modeling activities",
            "distinguishing formal threat modeling from threat awareness",
            "selecting a methodology (STRIDE, PASTA, LINDDUN)",
        ],
        "threats": [
            "conflating informal threat awareness with formal threat modeling",
            "design-level threats missed because only code-level review occurred",
        ],
        "summary": (
            "Two distinct activities: formal Threat Modeling at the system/feature "
            "level, and continuous lightweight Threat Awareness at the code level."
        ),
    },
    "4.2.1": {
        "title": "Code-Level Threat Awareness",
        "when_to_use": [
            "applying the 'What can go wrong?' question during merge reviews",
            "incorporating static analysis findings into threat awareness",
            "using pair programming to build threat-awareness judgment",
        ],
        "threats": [
            "code-level findings that never escalate into the formal threat model",
            "missed design-level concerns in scoped reviews",
        ],
        "summary": (
            "Lightweight, continuous practice of asking 'What can go wrong?' at the "
            "code level. Findings that reveal design-level concerns must escalate "
            "into the formal threat model."
        ),
    },
    "4.2.2": {
        "title": "Threat Modeling Solution Framework",
        "when_to_use": [
            "answering 'What are we going to do about it?' with SSEM",
            "deriving security requirements from unaddressable threats",
            "mapping data flows to identify trust boundaries",
        ],
        "threats": [
            "default reach for security controls without considering inherent attributes",
            "threats addressed by localized fixes rather than design changes",
        ],
        "summary": (
            "Use SSEM (especially Trustworthiness and Reliability) to find inherent "
            "architectural solutions; gaps that cannot be addressed inherently become "
            "explicit security requirements."
        ),
    },
    "4.3": {
        "title": "The Boundary Control Principle",
        "ssem_attributes": ["Integrity", "Resilience", "Confidentiality"],
        "when_to_use": [
            "designing trust boundary handling",
            "balancing internal flexibility with control at boundaries",
            "applying canonical input handling at trust boundaries",
        ],
        "threats": [
            "uncontrolled flexibility at trust boundaries enabling injection attacks",
            "treating flexibility itself as the threat rather than its exposure",
        ],
        "summary": (
            "Flexibility within the interior is an engineering asset; control at "
            "every trust boundary is a security requirement. Harden the shell, keep "
            "the interior flexible. (Formerly called 'The Flexibility Principle'.)"
        ),
    },
    "4.4": {
        "title": "Resilient Coding",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Resilience", "Integrity", "Observability"],
        "when_to_use": [
            "implementing defensive coding practices",
            "reviewing input handling, error handling, and resource management",
            "applying least privilege at the code level",
            "designing for graceful and secure failure",
        ],
        "threats": [
            "injection attacks from unvalidated input",
            "resource leaks introducing availability or memory risks",
            "error paths leaking internal state to untrusted parties",
            "code retaining elevated privileges longer than required",
        ],
        "summary": (
            "Defensive coding practices that produce predictable, recoverable "
            "behavior: strong typing, input validation, output encoding, safe "
            "resource management, graceful and secure failure, and least privilege "
            "at the code level."
        ),
    },
    "4.4.1": {
        "title": "Canonical Input Handling",
        "ssem_attributes": ["Integrity", "Resilience"],
        "when_to_use": [
            "designing input validation strategies at trust boundaries",
            "applying canonicalization, validation, and sanitization",
            "passing contextualized objects after validation",
        ],
        "threats": [
            "malformed or malicious input propagating into core logic",
            "sanitization gaps that miss context-specific encodings",
        ],
        "summary": (
            "Apply minimum acceptable range at the point of input through "
            "canonicalization/normalization, validation, and sanitization."
        ),
    },
    "4.4.1.1": {
        "title": "The Request Surface Minimization Principle",
        "ssem_attributes": ["Integrity", "Resilience", "Observability"],
        "when_to_use": [
            "designing endpoints that consume only expected named values",
            "logging and rejecting unexpected input fields in sensitive contexts",
            "detecting reconnaissance and probing behavior",
        ],
        "threats": [
            "blanket processing of request envelopes enabling injection",
            "silent acceptance of unexpected fields enabling reconnaissance",
            "manipulation of derived values via extra fields",
        ],
        "summary": (
            "Process only the specific named values expected. Log or reject "
            "deviations; in sensitive contexts, log-and-reject is the more "
            "defensible posture."
        ),
    },
    "4.4.1.2": {
        "title": "The Derived Integrity Principle",
        "ssem_attributes": ["Integrity", "Authenticity"],
        "when_to_use": [
            "deriving prices, totals, and other authoritative values server-side",
            "managing user permissions and object state from trusted sources",
            "validating JWT signature algorithms server-side",
        ],
        "threats": [
            "business logic manipulation through client-supplied authoritative values",
            "JWT algorithm-confusion attacks",
            "client-supplied permission elevation",
        ],
        "summary": (
            "Any value critical to system or business-logic integrity must be "
            "derived in a trusted context, never accepted from a client. The client "
            "expresses intent; the server enforces integrity."
        ),
    },
    "4.5": {
        "title": "Dependency Management",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability",
            "Authenticity", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "evaluating third-party library adoption",
            "applying SSEM to dependency selection and management",
            "going beyond CVE scanning to assess transitive risk",
        ],
        "threats": [
            "insecure dependencies introducing vulnerabilities",
            "supply chain attacks through tampered packages",
            "unnecessary dependencies expanding attack surface",
        ],
        "summary": (
            "Evaluate dependencies against SSEM attributes before introduction. "
            "Minimize dependencies, update regularly, go beyond CVE scanning."
        ),
    },
    "4.6": {
        "title": "Dependency Stewardship",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability",
            "Authenticity", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "treating ongoing dependency relationships as a securable attribute",
            "monitoring dependency health and maintainer activity over time",
            "raising stewardship in sprint planning, architecture, and merge reviews",
        ],
        "threats": [
            "dependencies that decay after initial evaluation",
            "abandoned or compromised maintainer communities",
            "tightly coupled dependencies that resist replacement",
        ],
        "summary": (
            "The ongoing application of SSEM attributes to dependency selection, "
            "integration, monitoring, and lifecycle management. Stewardship asks: "
            "would this dependency be responsible, maintainable, and trustworthy "
            "now and over time?"
        ),
    },
    # -----------------------------------------------------------------------
    # 5. Integrating Security into Development Processes
    # -----------------------------------------------------------------------
    "5.1": {
        "title": "Natively Extending Development Processes",
        "when_to_use": [
            "integrating security into existing dev workflows",
            "repositioning security as a partner rather than gatekeeper",
            "extending architecture, checklists, and usability with security",
        ],
        "threats": [
            "imposing external security gates that disrupt development",
            "adversarial relationship between security and development",
        ],
        "summary": (
            "Integrate security into existing workflows rather than imposing "
            "separate gates. Security as partner in design, not external assessor."
        ),
    },
    "5.2": {
        "title": "The Role of Merge Reviews",
        "when_to_use": [
            "establishing security-focused code review practices",
            "scaling securable code review through pull/merge requests",
            "treating reviews as guardrails rather than gates",
        ],
        "threats": [
            "security vulnerabilities missed without structured review",
            "review processes that become friction rather than guidance",
        ],
        "summary": (
            "Merge reviews are an effective scaling point for securable review and "
            "knowledge transfer. SSEM attributes provide a shared review basis."
        ),
    },
    "5.3": {
        "title": "Early Integration: Planning and Requirements",
        "when_to_use": [
            "integrating security into requirements gathering",
            "defining security acceptance criteria for features",
            "shifting security to a design-phase concern",
        ],
        "threats": [
            "security treated as post-development afterthought",
            "vulnerabilities discovered late at significantly higher remediation cost",
        ],
        "summary": (
            "Set security expectations at planning and requirements. Active AppSec "
            "participation in requirements (Section 4.1.2) is the primary mechanism."
        ),
    },
    # -----------------------------------------------------------------------
    # 6. Common AppSec Anti-Patterns
    # -----------------------------------------------------------------------
    "6.1": {
        "title": "The Shoveling Left Phenomenon",
        "when_to_use": [
            "identifying ineffective AppSec practices",
            "applying the Actionable Security Intelligence Principle",
            "evaluating how security findings reach developers",
        ],
        "threats": [
            "raw vulnerability dumps overwhelming developers",
            "exploit-first training that fails to build engineering skills",
            "developer disengagement from AppSec",
        ],
        "summary": (
            "Shoveling Left: supplying impractical information to developers. The "
            "corrective discipline is the Actionable Security Intelligence Principle."
        ),
    },
    "6.1.1": {
        "title": "Ineffective Vulnerability Reporting",
        "when_to_use": [
            "improving how scanner findings reach development",
            "validating, prioritizing, and root-cause-grouping findings",
        ],
        "threats": [
            "raw scanner output routed directly to backlog",
            "whack-a-mole patterns from unaddressed root causes",
        ],
        "summary": (
            "Avoid routing raw scanner output to development. Validate true "
            "positives, identify root causes, prioritize impact, and verify fixes."
        ),
    },
    "6.1.2": {
        "title": "Pitfalls of Exploit-First Training",
        "when_to_use": [
            "evaluating developer security training effectiveness",
            "designing training grounded in engineering principles, not exploitation",
        ],
        "threats": [
            "training that emphasizes exploitation over engineering",
            "false sense of security from superficial exploit knowledge",
        ],
        "summary": (
            "Training centered on exploitation does not equip developers with the "
            "engineering principles needed to build inherently securable systems."
        ),
    },
    "6.2": {
        "title": "Strategic Use of Security Output",
        "when_to_use": [
            "establishing processes for sharing scanning and testing results",
            "avoiding disruption of developer workflows",
            "translating raw findings into actionable intelligence",
        ],
        "threats": [
            "fix requests bypassing established workflows",
            "treating scanner output as finished intelligence rather than input",
        ],
        "summary": (
            "Scanning and testing output must be converted into engineering-grounded "
            "direction tied to requirements and acceptance criteria, not handed to "
            "developers as finished intelligence."
        ),
    },
    # -----------------------------------------------------------------------
    # 7. Roles and Responsibilities
    # -----------------------------------------------------------------------
    "7.1": {
        "title": "The Role of the Security Team",
        "when_to_use": [
            "defining the role of AppSec in development organizations",
            "framing security metrics as partnership measures",
            "investing security effort in design and requirements",
        ],
        "threats": [
            "security metrics misattributed as developer compliance measures",
            "security team policing line-level fixes instead of partnering",
        ],
        "summary": (
            "Security metrics measure partnership effectiveness, not developer "
            "adherence. The security team's effectiveness is limited by software "
            "quality."
        ),
    },
    "7.2": {
        "title": "Senior Software Engineers",
        "when_to_use": [
            "defining expectations for senior engineers in FIASSE adoption",
            "establishing senior engineers as primary technical partners for security",
            "scrutinizing AI-generated code for SSEM attribute alignment",
        ],
        "threats": [
            "senior engineers not engaged in security considerations",
            "AI-generated code accepted without judgment about trust boundaries",
        ],
        "summary": (
            "Senior engineers drive security requirements, lead SSEM-based merge "
            "reviews, maintain prompt engineering standards for AI-assisted "
            "generation, and mentor peers."
        ),
    },
    "7.3": {
        "title": "Developing Software Engineers",
        "when_to_use": [
            "mentoring developing engineers in securable practices",
            "establishing learning paths grounded in engineering fundamentals",
            "building SSEM mental models in less experienced team members",
        ],
        "threats": [
            "developing engineers introducing vulnerabilities from inexperience",
            "AI-generated code accepted without critical review",
        ],
        "summary": (
            "Developing engineers benefit from SSEM mental models. Focus on "
            "engineering fundamentals, defensive coding, trust boundaries, and "
            "scrutinizing AI-generated code."
        ),
    },
    "7.4": {
        "title": "Product Owners and Managers",
        "when_to_use": [
            "engaging product owners in security planning",
            "allocating time for security activities and dependency maintenance",
            "evaluating scope cuts for securability impact",
        ],
        "threats": [
            "scope cuts that silently degrade securable attributes",
            "vendor selection without securability evaluation",
            "security activities deprioritized in product planning",
        ],
        "summary": (
            "FIASSE-literate Product Owners assess backlog items for securability "
            "implications, validate security acceptance criteria, and recognize "
            "when scope cuts erode securable attributes."
        ),
    },
    # -----------------------------------------------------------------------
    # 8. Organizational Adoption of FIASSE
    # -----------------------------------------------------------------------
    "8": {
        "title": "Organizational Adoption of FIASSE",
        "when_to_use": [
            "planning organizational adoption of FIASSE",
            "assessing readiness and identifying influencers",
            "integrating SSEM terminology into standards and training",
        ],
        "threats": [
            "FIASSE treated as a separate security initiative",
            "failed adoption from lack of stakeholder buy-in",
        ],
        "summary": (
            "Six-step adoption path: assess practices, integrate SSEM terminology, "
            "identify influencers, educate teams, foster collaboration, and monitor "
            "continuously."
        ),
    },
    # -----------------------------------------------------------------------
    # Appendix A. Measuring SSEM Attributes
    # -----------------------------------------------------------------------
    "A.1": {
        "title": "Measuring Maintainability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Analyzability", "Modifiability", "Testability", "Observability"],
        "when_to_use": [
            "establishing metrics for maintainability attributes",
            "defining measurement criteria for securability reviews",
        ],
        "threats": [
            "unmeasured code quality degrading over time",
            "inability to track improvement in securable attributes",
        ],
        "summary": (
            "Quantitative and qualitative measurement approaches for Analyzability, "
            "Modifiability, Testability, and Observability."
        ),
    },
    "A.1.1": {
        "title": "Measuring Analyzability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Analyzability"],
        "when_to_use": [
            "tracking volume, duplication, unit size, and complexity",
            "running developer surveys and time-to-understand assessments",
        ],
        "threats": ["analyzability decay obscuring vulnerabilities"],
        "summary": "Quantitative and qualitative measures for Analyzability.",
    },
    "A.1.2": {
        "title": "Measuring Modifiability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Modifiability"],
        "when_to_use": [
            "tracking module coupling, change impact size, and regression rate",
            "assessing time-to-implement and ease-of-change qualitatively",
        ],
        "threats": ["high coupling causing cascading change"],
        "summary": "Quantitative and qualitative measures for Modifiability.",
    },
    "A.1.3": {
        "title": "Measuring Testability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Testability"],
        "when_to_use": [
            "tracking code coverage, unit test density, and mocking complexity",
            "evaluating ease of writing tests and execution time",
        ],
        "threats": ["test gaps in security-relevant paths"],
        "summary": "Quantitative and qualitative measures for Testability.",
    },
    "A.1.4": {
        "title": "Measuring Observability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Observability"],
        "when_to_use": [
            "tracking log coverage, instrumentation coverage, alert SNR, and MTTD",
            "auditing structured-logging quality and code-level instrumentation",
            "identifying silent failure paths",
        ],
        "threats": [
            "silent failures and exception swallowing",
            "instrumentation gaps creating opaque code paths",
        ],
        "summary": (
            "Quantitative and qualitative measures for Observability, including "
            "structured logging review, instrumentation audits, and failure-path "
            "observability."
        ),
    },
    "A.2": {
        "title": "Measuring Trustworthiness",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Confidentiality", "Accountability", "Authenticity"],
        "when_to_use": [
            "establishing metrics for trustworthiness attributes",
            "auditing data protection, access controls, and authentication coverage",
        ],
        "threats": [
            "data leaks from insufficient confidentiality controls",
            "untraceable actions due to poor accountability",
        ],
        "summary": (
            "Quantitative and qualitative measurement approaches for "
            "Confidentiality, Accountability, and Authenticity."
        ),
    },
    "A.2.1": {
        "title": "Measuring Confidentiality",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Confidentiality"],
        "when_to_use": [
            "tracking identified data leaks and access control violations",
            "reviewing data classification and least-privilege adherence",
        ],
        "threats": ["uncontrolled data disclosure"],
        "summary": "Quantitative and qualitative measures for Confidentiality.",
    },
    "A.2.2": {
        "title": "Measuring Accountability",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Accountability"],
        "when_to_use": [
            "tracking audit log coverage and traceability success rate",
            "assessing non-repudiation strength",
        ],
        "threats": ["actions that cannot be uniquely attributed"],
        "summary": "Quantitative and qualitative measures for Accountability.",
    },
    "A.2.3": {
        "title": "Measuring Authenticity",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Authenticity"],
        "when_to_use": [
            "tracking authentication failures and mechanism coverage",
            "assessing defendability of authentication mechanisms",
        ],
        "threats": ["brittle authentication that cannot adapt"],
        "summary": "Quantitative and qualitative measures for Authenticity.",
    },
    "A.3": {
        "title": "Measuring Reliability",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Availability", "Integrity", "Resilience"],
        "when_to_use": [
            "establishing metrics for reliability attributes",
            "measuring uptime, recovery, and resilience under stress",
        ],
        "threats": [
            "prolonged downtime from unmonitored availability",
            "undetected data corruption",
        ],
        "summary": (
            "Quantitative and qualitative measurement approaches for Availability, "
            "Integrity, and Resilience."
        ),
    },
    "A.3.1": {
        "title": "Measuring Availability",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Availability"],
        "when_to_use": [
            "tracking uptime percentage, MTBF, MTTR",
            "reviewing redundancy and disaster recovery test results",
        ],
        "threats": ["service disruption and slow recovery"],
        "summary": "Quantitative and qualitative measures for Availability.",
    },
    "A.3.2": {
        "title": "Measuring Integrity",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Integrity"],
        "when_to_use": [
            "tracking corruption incidents and checksum/hash validation rates",
            "reviewing input validation and file integrity monitoring",
        ],
        "threats": ["unauthorized data modification"],
        "summary": "Quantitative and qualitative measures for Integrity.",
    },
    "A.3.3": {
        "title": "Measuring Resilience",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Resilience"],
        "when_to_use": [
            "tracking RTO adherence and performance under stress",
            "reviewing defensive coding practices",
        ],
        "threats": ["cascading failures and slow recovery"],
        "summary": "Quantitative and qualitative measures for Resilience.",
    },
}

# ---------------------------------------------------------------------------
# Section-ID mapping to framework heading patterns
# ---------------------------------------------------------------------------
# The FIASSE framework uses numbered headings (## 1. Introduction, ### 1.1., etc.).
# In v1.0.4, headings range from level 2 (chapters) down to level 5
# (sub-sub-attributes like ##### 4.4.1.1).

# Ordered list of section IDs to extract. Order is significant: each section
# extends until the next sibling listed here, or until a chapter heading
# (whichever comes first).
TARGET_SECTIONS: list[str] = [
    # 1. Introduction
    "1.1", "1.2",
    # 2. Foundational Principles
    "2.1", "2.2", "2.3", "2.4", "2.5", "2.6",
    # 3. SSEM
    "3.1", "3.2",
    "3.2.1", "3.2.1.1", "3.2.1.2", "3.2.1.3", "3.2.1.4",
    "3.2.2", "3.2.2.1", "3.2.2.2", "3.2.2.3",
    "3.2.3", "3.2.3.1", "3.2.3.2", "3.2.3.3",
    # 4. Practical Guidance
    "4.1", "4.1.1", "4.1.2",
    "4.2", "4.2.1", "4.2.2",
    "4.3",
    "4.4", "4.4.1", "4.4.1.1", "4.4.1.2",
    "4.5", "4.6",
    # 5. Integrating Security into Development Processes
    "5.1", "5.2", "5.3",
    # 6. Common AppSec Anti-Patterns
    "6.1", "6.1.1", "6.1.2", "6.2",
    # 7. Roles and Responsibilities
    "7.1", "7.2", "7.3", "7.4",
    # 8. Organizational Adoption of FIASSE
    "8",
    # Appendix A. Measuring SSEM Attributes
    "A.1", "A.1.1", "A.1.2", "A.1.3", "A.1.4",
    "A.2", "A.2.1", "A.2.2", "A.2.3",
    "A.3", "A.3.1", "A.3.2", "A.3.3",
]

# Map section_id -> regex pattern matching its starting heading in the framework.
# Headings may optionally be prefixed with 'S' (e.g. "## S2.1 ..." or "## 2.1.").
# The framework typically uses a trailing period after the section number.
HEADING_PATTERNS: dict[str, re.Pattern] = {
    sid: re.compile(
        rf"^#{{2,6}}\s+S?{re.escape(sid)}\.?\s",
        re.MULTILINE,
    )
    for sid in TARGET_SECTIONS
}

# Map section_id -> next sibling in TARGET_SECTIONS order. Used as the primary
# end-of-section marker.
_NEXT_SECTION: dict[str, Optional[str]] = {}
for i, sid in enumerate(TARGET_SECTIONS):
    _NEXT_SECTION[sid] = TARGET_SECTIONS[i + 1] if i + 1 < len(TARGET_SECTIONS) else None

# Higher-level chapter headings that terminate a section. Matches "## N.\s"
# or "### N.\s" for chapters 1-10, plus the Appendix A heading.
_CHAPTER_HEADS = [
    re.compile(rf"^#{{2,3}}\s+S?{ch}\.\s", re.MULTILINE)
    for ch in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
]
_APPENDIX_HEAD = re.compile(r"^#{2,3}\s+Appendix\s+A[:\s]", re.MULTILINE)


def _find_heading(content: str, section_id: str, start: int = 0) -> Optional[int]:
    """Return the character offset of the heading for section_id, or None."""
    pat = HEADING_PATTERNS.get(section_id)
    if not pat:
        return None
    m = pat.search(content, start)
    return m.start() if m else None


def _section_top(section_id: str) -> str:
    """Return the top-level chapter identifier ('A' for appendix sections)."""
    return section_id.split(".")[0]


def _find_section_end(content: str, section_id: str, body_start: int) -> int:
    """
    Find where a section ends. It ends at the start of the next target section's
    heading, or at a higher-level chapter heading, whichever comes first.
    """
    candidates: list[int] = []

    # Next section in our ordered list.
    nxt = _NEXT_SECTION.get(section_id)
    if nxt:
        pos = _find_heading(content, nxt, body_start)
        if pos is not None:
            candidates.append(pos)

    top = _section_top(section_id)

    # Numeric chapter heads. Only count if it's a different chapter from the
    # current section.
    for pat in _CHAPTER_HEADS:
        m = pat.search(content, body_start)
        if m:
            heading_text = content[m.start():m.end()]
            heading_num = re.search(r"(\d+)\.", heading_text)
            if heading_num and heading_num.group(1) != top:
                candidates.append(m.start())

    # Appendix A heading terminates any non-appendix section.
    if top != "A":
        m = _APPENDIX_HEAD.search(content, body_start)
        if m:
            candidates.append(m.start())

    return min(candidates) if candidates else len(content)


def extract_sections(content: str) -> list[tuple[str, str]]:
    """
    Parse FIASSE framework markdown into (section_id, body) tuples.
    Returns only sections listed in TARGET_SECTIONS.
    """
    results: list[tuple[str, str]] = []
    for sid in TARGET_SECTIONS:
        start = _find_heading(content, sid)
        if start is None:
            print(f"  WARNING: heading for section {sid} not found", file=sys.stderr)
            continue
        end = _find_section_end(content, sid, start + 1)
        body = content[start:end].strip()
        results.append((sid, body))
    return results


def _build_frontmatter(section_id: str) -> str:
    """Build YAML frontmatter for a section file."""
    meta = SECTION_META.get(section_id, {})
    title = meta.get("title", f"Section {section_id}")
    fm_id = f"S{section_id}"

    lines = [
        "---",
        f'title: "S{section_id} {title}"',
        f'fiasse_section: "{fm_id}"',
        'fiasse_version: "1.0.4"',
    ]

    if "ssem_pillar" in meta:
        lines.append(f'ssem_pillar: "{meta["ssem_pillar"]}"')

    if "ssem_attributes" in meta:
        lines.append("ssem_attributes:")
        for attr in meta["ssem_attributes"]:
            lines.append(f"  - {attr}")

    if "when_to_use" in meta:
        lines.append("when_to_use:")
        for item in meta["when_to_use"]:
            lines.append(f"  - {item}")

    if "threats" in meta:
        lines.append("threats:")
        for item in meta["threats"]:
            lines.append(f"  - {item}")

    if "summary" in meta:
        lines.append(f'summary: "{meta["summary"]}"')

    lines.append("---")
    return "\n".join(lines)


def extract(source_path: Path, dest_dir: Path) -> list[Path]:
    """
    Read source_path, extract sections, write each to dest_dir with YAML
    frontmatter. Returns paths of written files.
    """
    if not source_path.is_file():
        raise FileNotFoundError(f"Not a file: {source_path}")

    text = source_path.read_text(encoding="utf-8")
    sections = extract_sections(text)

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for section_id, body in sections:
        frontmatter = _build_frontmatter(section_id)
        out_path = dest_dir / f"S{section_id}.md"
        content = f"{frontmatter}\n\n{body}\n"
        out_path.write_text(content, encoding="utf-8")
        written.append(out_path)
    return written


def main() -> None:
    if len(sys.argv) < 2:
        print(
            textwrap.dedent("""\
            Usage: extract_fiasse_sections.py <source.md> [dest_dir]

              source.md  Path to FIASSE framework markdown file (v1.0.4+).
              dest_dir   Output directory (default: data/fiasse).

            Download the v1.0.4 framework:
              curl -o /tmp/securable_framework.md \\
                https://raw.githubusercontent.com/OWASP/FIASSE/refs/tags/v1.0.4/docs/securable_framework.md
              python scripts/extract_fiasse_sections.py /tmp/securable_framework.md data/fiasse/
            """),
            file=sys.stdout,
        )
        sys.exit(1)

    source = Path(sys.argv[1]).resolve()
    dest = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else Path("data/fiasse").resolve()
    )

    try:
        paths = extract(source, dest)
        for p in paths:
            print(p)
        print(f"Wrote {len(paths)} section(s) to {dest}", file=sys.stderr)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
