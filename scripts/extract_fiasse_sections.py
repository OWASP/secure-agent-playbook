#!/usr/bin/env python3
"""
Extract FIASSE RFC sections into structured markdown files with YAML frontmatter.

Parses the FIASSE RFC markdown (from Xcaciv/securable_software_engineering) and
produces one file per logical section under data/fiasse/. Each output file has
YAML frontmatter (title, fiasse_section, ssem_pillar, ssem_attributes,
when_to_use, threats, summary) followed by the section content.

Section files are named S{x.y}.md (e.g. S3.2.1.md) matching the RFC numbering.
"""

import re
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Section metadata registry
# ---------------------------------------------------------------------------
# Maps section_id -> metadata dict. Each entry defines the frontmatter fields
# that cannot be inferred from the RFC text alone (when_to_use, threats,
# summary, and optionally ssem_pillar / ssem_attributes).

SECTION_META: dict[str, dict] = {
    "1.1": {
        "title": "The Application Security Challenge",
        "when_to_use": [
            "understanding why application security initiatives struggle",
            "framing the business case for securable code practices",
            "assessing friction between AppSec and Development teams",
        ],
        "threats": [
            "slow progress in application security outcomes",
            "friction between AppSec and Development teams",
            "AI-generated code amplifying past security mistakes",
        ],
        "summary": (
            "The core challenge: organizations invest significantly in AppSec yet "
            "often see limited outcomes. Shift-left has underdelivered, AI code "
            "generation amplifies risk, and developers lack deep security expertise."
        ),
    },
    "1.2": {
        "title": "A Developer-Centric Security Paradigm",
        "when_to_use": [
            "advocating for developer empowerment in security",
            "reframing the security-development relationship",
            "building a case for integrating security through engineering discipline",
        ],
        "threats": [
            "expecting developers to adopt adversarial mindsets",
            "treating the AppSec-Dev gap as inherently problematic",
            "neglecting business processes and skillsets in software production",
        ],
        "summary": (
            "Advocates for empowering developers through sound software engineering "
            "principles rather than expecting them to think like attackers."
        ),
    },
    "1.3": {
        "title": "Document Purpose and Scope",
        "when_to_use": [
            "understanding the scope and audience of FIASSE",
            "distinguishing FIASSE from SSEM",
            "mapping FIASSE to organizational roles (AppSec, Product Security)",
        ],
        "threats": [
            "misunderstanding the framework scope",
            "siloed security functions lacking a unifying framework",
        ],
        "summary": (
            "Defines FIASSE as the overarching strategic framework and SSEM as the "
            "design language model within it."
        ),
    },
    "2.1": {
        "title": "The Securable Paradigm: No Static Secure State",
        "when_to_use": [
            "explaining the difference between secure and securable",
            "challenging binary secure/insecure classification",
            "advocating for adaptive security posture",
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
            "The primary directive: resiliently add computing value — code that is "
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
            "pursuing illusory goal of complete breach elimination",
            "security strategies misaligned with business objectives",
        ],
        "summary": (
            "The core mission is to reduce the probability of material impact of a "
            "cyber event. Security strategies must align with business objectives."
        ),
    },
    "2.4": {
        "title": "Mindset Convergence: Hacker vs. Engineer",
        "when_to_use": [
            "challenging the assumption that developers should think like attackers",
            "distinguishing vulnerability identification from secure implementation",
            "framing security and development as complementary disciplines",
        ],
        "threats": [
            "expecting developers to adopt adversarial mindsets as primary defense",
            "relying on line-level fixes that do not scale",
        ],
        "summary": (
            "Identifying a vulnerability and implementing a robust engineering "
            "solution are different skills. Security and development are complementary."
        ),
    },
    "2.5": {
        "title": "Aligning Security with Development",
        "when_to_use": [
            "integrating security into development using engineering terminology",
            "empowering developers to address security confidently",
            "enabling security to recognize securable attributes in existing code",
        ],
        "threats": [
            "imposing security-centric jargon that disrupts development",
            "developers unable to address security due to unfamiliar terminology",
        ],
        "summary": (
            "True alignment requires using well-established software engineering "
            "terms to describe securable code attributes."
        ),
    },
    "2.6": {
        "title": "The Transparency Principle",
        "ssem_attributes": ["Transparency"],
        "when_to_use": [
            "designing observable and auditable systems",
            "implementing logging and instrumentation strategies",
            "evaluating system transparency for security analysis",
        ],
        "threats": [
            "opaque systems that resist security analysis",
            "reactive security posture due to lack of observability",
            "insufficient audit trails for incident response",
        ],
        "summary": (
            "Transparency is a foundational engineering strategy: designing systems so "
            "internal state and behavior are observable and understandable."
        ),
    },
    "3.1": {
        "title": "Securable Software Engineering Model Overview",
        "ssem_pillar": "All",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability",
            "Confidentiality", "Accountability", "Authenticity",
            "Availability", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "introducing SSEM to a development team",
            "understanding the SSEM attribute taxonomy",
            "using SSEM as a design language for security discussions",
        ],
        "threats": [
            "binary secure/insecure assessment without nuance",
            "security jargon that excludes developers",
        ],
        "summary": (
            "SSEM provides a design language using established software engineering "
            "terms. Nine attributes grouped into three pillars."
        ),
    },
    "3.2.1": {
        "title": "Maintainability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Analyzability", "Modifiability", "Testability"],
        "when_to_use": [
            "reviewing code for maintainability attributes",
            "assessing analyzability of a codebase",
            "evaluating modifiability of a system",
            "checking testability of code under review",
        ],
        "threats": [
            "undetected vulnerabilities due to complex code",
            "slow vulnerability remediation",
            "introducing defects during security fixes",
        ],
        "summary": (
            "Maintainability encompasses Analyzability, Modifiability, and "
            "Testability — the ability to evolve, correct, and adapt software."
        ),
    },
    "3.2.2": {
        "title": "Trustworthiness",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Confidentiality", "Accountability", "Authenticity"],
        "when_to_use": [
            "reviewing code for trustworthiness attributes",
            "assessing data protection and confidentiality",
            "evaluating accountability and audit trail design",
            "checking authentication and identity verification",
        ],
        "threats": [
            "unauthorized data disclosure",
            "inability to trace actions to entities",
            "identity spoofing and non-repudiation failures",
        ],
        "summary": (
            "Trustworthiness encompasses Confidentiality, Accountability, and "
            "Authenticity — the degree to which a system achieves security requirements."
        ),
    },
    "3.2.3": {
        "title": "Reliability",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Availability", "Integrity", "Resilience"],
        "when_to_use": [
            "reviewing code for reliability attributes",
            "assessing system availability and uptime design",
            "evaluating data and system integrity",
            "checking resilience and fault tolerance",
        ],
        "threats": [
            "denial of service attacks",
            "unauthorized data modification or corruption",
            "system failures and inability to recover",
        ],
        "summary": (
            "Reliability encompasses Availability, Integrity, and Resilience — "
            "consistent and predictable operation under adverse conditions."
        ),
    },
    "3.3.1": {
        "title": "Transparency Strategy",
        "ssem_attributes": ["Transparency"],
        "when_to_use": [
            "designing logging and instrumentation strategies",
            "implementing audit trails for security events",
            "connecting transparency to maintainability and trustworthiness",
        ],
        "threats": [
            "opaque systems that resist debugging and security analysis",
            "missing audit trails preventing incident attribution",
        ],
        "summary": (
            "Transparency strengthens SSEM attributes through deliberate "
            "instrumentation, structured logging, and audit trails."
        ),
    },
    "3.3.2": {
        "title": "SSEM as a Design Language",
        "when_to_use": [
            "introducing SSEM terminology to a team",
            "shifting security conversations from vulnerability-centric to attribute-centric",
            "building a culture of quality around security attributes",
        ],
        "threats": [
            "myopic treatment of individual vulnerabilities",
            "find-and-fix monotony that fails to scale",
        ],
        "summary": (
            "SSEM provides a common design language using established software "
            "engineering terminology, shifting focus to inherent securable qualities."
        ),
    },
    "3.4.1": {
        "title": "Measuring Maintainability",
        "ssem_pillar": "Maintainability",
        "ssem_attributes": ["Analyzability", "Modifiability", "Testability"],
        "when_to_use": [
            "establishing metrics for maintainability attributes",
            "setting up static analysis for code quality",
            "defining measurement criteria for securability reviews",
        ],
        "threats": [
            "unmeasured code quality degrading over time",
            "inability to track improvement in securable attributes",
        ],
        "summary": (
            "Quantitative and qualitative measurement approaches for Analyzability, "
            "Modifiability, and Testability."
        ),
    },
    "3.4.2": {
        "title": "Measuring Trustworthiness",
        "ssem_pillar": "Trustworthiness",
        "ssem_attributes": ["Confidentiality", "Accountability", "Authenticity"],
        "when_to_use": [
            "establishing metrics for trustworthiness attributes",
            "auditing data protection and access controls",
            "evaluating logging and traceability completeness",
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
    "3.4.3": {
        "title": "Measuring Reliability",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Availability", "Integrity", "Resilience"],
        "when_to_use": [
            "establishing metrics for reliability attributes",
            "assessing system uptime and recovery capabilities",
            "measuring resilience under stress or attack",
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
    "4.1": {
        "title": "Applying SSEM to Dependency Management",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability",
            "Authenticity", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "evaluating third-party dependencies through SSEM lens",
            "selecting libraries for a project",
            "managing dependency security beyond CVE scanning",
        ],
        "threats": [
            "insecure dependencies introducing vulnerabilities",
            "supply chain attacks through tampered packages",
        ],
        "summary": (
            "SSEM principles apply equally to dependency management. Proactively "
            "evaluate libraries against all SSEM attributes."
        ),
    },
    "4.2": {
        "title": "Natively Extending Development Processes",
        "when_to_use": [
            "integrating security into existing dev workflows",
            "repositioning security as a partner rather than gatekeeper",
            "extending architecture and design processes with security",
        ],
        "threats": [
            "imposing external security gates that disrupt development",
            "adversarial relationship between security and development",
        ],
        "summary": (
            "Integrate security into existing workflows rather than imposing "
            "separate gates. Security should be a partner in design."
        ),
    },
    "4.3": {
        "title": "The Role of Merge Reviews",
        "when_to_use": [
            "establishing security-focused code review practices",
            "scaling securable code review through pull requests",
            "integrating threat modeling into merge reviews",
        ],
        "threats": [
            "security vulnerabilities missed without structured review",
            "loss of knowledge sharing between team members",
        ],
        "summary": (
            "Merge reviews are the single most effective technique for identifying "
            "security vulnerabilities early. Guardrails, not gates."
        ),
    },
    "4.4": {
        "title": "Early Integration: Planning and Requirements",
        "when_to_use": [
            "integrating security into requirements gathering",
            "defining security acceptance criteria for features",
            "shifting security to a design-phase concern",
        ],
        "threats": [
            "security treated as post-development afterthought",
            "vulnerabilities discovered late at 100x remediation cost",
        ],
        "summary": (
            "Set security expectations at planning and requirements. Fixing in "
            "design costs 100x less than in production."
        ),
    },
    "5.1": {
        "title": "The Shoveling Left Phenomenon",
        "when_to_use": [
            "identifying ineffective AppSec practices",
            "improving vulnerability reporting processes",
            "evaluating security training effectiveness",
        ],
        "threats": [
            "raw vulnerability dumps overwhelming developers",
            "exploit-first training that fails to build engineering skills",
            "developer disengagement from AppSec",
        ],
        "summary": (
            "Shoveling Left: supplying impractical information to developers. "
            "Manifests as raw scanner output and exploit-first training."
        ),
    },
    "5.2": {
        "title": "Strategic Use of Security Output",
        "when_to_use": [
            "establishing processes for sharing security findings with development",
            "avoiding disruption of developer workflows",
            "aligning security output with development processes",
        ],
        "threats": [
            "fix requests bypassing established workflows",
            "degraded software quality from disrupted developer processes",
        ],
        "summary": (
            "Security output must be used strategically. Fix requests must not "
            "circumvent established developer workflows."
        ),
    },
    "6.1": {
        "title": "Establishing Clear Expectations",
        "when_to_use": [
            "setting security expectations for development teams",
            "integrating security into requirements gathering",
            "improving proactive communication between AppSec and Dev",
        ],
        "threats": [
            "unclear security expectations leading to missing controls",
            "security imposed as afterthought rather than requirement",
        ],
        "summary": (
            "Clear expectations through proactive communication and integrating "
            "security into requirements (features, threat scenarios, acceptance criteria)."
        ),
    },
    "6.2": {
        "title": "Threat Modeling",
        "when_to_use": [
            "performing threat modeling activities",
            "applying the Four Question Framework",
            "identifying threats at the code level during merge reviews",
        ],
        "threats": [
            "unidentified threats in system design",
            "security controls that address symptoms rather than design flaws",
        ],
        "summary": (
            "Threat modeling using the Four Question Framework. Code-level threat "
            "identification through merge reviews and pair programming."
        ),
    },
    "6.3": {
        "title": "The Flexibility Principle",
        "ssem_attributes": ["Integrity", "Resilience"],
        "when_to_use": [
            "designing trust boundary handling",
            "balancing code flexibility with security control",
            "applying the trust boundary turtle analogy",
        ],
        "threats": [
            "uncontrolled flexibility enabling injection attacks",
            "careless handling of trust boundaries",
        ],
        "summary": (
            "The issue is not flexibility but its exposure through careless handling "
            "of trust boundaries. Harden the shell, keep the interior flexible."
        ),
    },
    "6.4": {
        "title": "Resilient Coding and System Resilience",
        "ssem_pillar": "Reliability",
        "ssem_attributes": ["Resilience", "Integrity"],
        "when_to_use": [
            "implementing defensive coding practices",
            "designing input handling and validation strategies",
            "applying the Derived Integrity Principle",
        ],
        "threats": [
            "injection attacks from unvalidated input",
            "business logic manipulation through client-supplied data",
            "race conditions from mutable shared state",
        ],
        "summary": (
            "Resilience through defensive coding: strong typing, input validation, "
            "output encoding. Includes Request Surface Minimization and Derived "
            "Integrity principles."
        ),
    },
    "6.5": {
        "title": "Dependency Management",
        "ssem_attributes": [
            "Analyzability", "Modifiability", "Testability",
            "Authenticity", "Integrity", "Resilience",
        ],
        "when_to_use": [
            "evaluating third-party library adoption",
            "managing software dependencies securely",
            "performing dependency security audits",
        ],
        "threats": [
            "insecure dependencies introducing vulnerabilities",
            "supply chain attacks through tampered packages",
            "unnecessary dependencies increasing attack surface",
        ],
        "summary": (
            "Evaluate libraries against SSEM attributes before introduction. "
            "Minimize dependencies, update regularly, go beyond CVE scanning."
        ),
    },
    "7.0": {
        "title": "Security's Role",
        "when_to_use": [
            "defining the role of AppSec in development organizations",
            "establishing security metrics and responsibilities",
            "understanding the partnership model between security and development",
        ],
        "threats": [
            "security metrics misattributed as development adherence measure",
            "AppSec micromanaging development teams",
        ],
        "summary": (
            "Security metrics measure effective partnership, not developer adherence. "
            "AppSec provides value through requirements, design, and assurance."
        ),
    },
    "7.1": {
        "title": "Empowering Senior Software Engineers",
        "when_to_use": [
            "defining expectations for senior engineers in FIASSE adoption",
            "establishing security champions within development teams",
            "guiding collaboration between AppSec and senior engineers",
        ],
        "threats": [
            "senior engineers not engaged in security considerations",
            "lack of security leadership within development teams",
        ],
        "summary": (
            "Senior engineers drive security requirements, lead SSEM-based merge "
            "reviews, champion dependency maintenance, and mentor peers."
        ),
    },
    "7.2": {
        "title": "Guiding Developing Software Engineers",
        "when_to_use": [
            "mentoring junior developers in security practices",
            "establishing learning paths for developing engineers",
            "building SSEM understanding in less experienced team members",
        ],
        "threats": [
            "junior developers introducing vulnerabilities from inexperience",
            "unvetted external dependencies introduced without due diligence",
        ],
        "summary": (
            "Developing engineers benefit from SSEM mental models. Focus on "
            "engineering fundamentals, defensive coding, and trust boundaries."
        ),
    },
    "7.3": {
        "title": "The Role of Product Owners and Managers",
        "when_to_use": [
            "engaging product owners in security planning",
            "allocating time for security activities in sprints",
            "integrating FIASSE into product development lifecycle",
        ],
        "threats": [
            "security activities deprioritized in product planning",
            "insufficient time allocated for dependency maintenance",
        ],
        "summary": (
            "Product Owners ensure FIASSE activities have space in the lifecycle. "
            "Advocate during planning and allocate time for training and maintenance."
        ),
    },
    "8.1": {
        "title": "Adapting to Emerging Software Engineering Trends",
        "when_to_use": [
            "applying FIASSE to AI-generated code",
            "securing low-code/no-code platforms",
            "addressing cloud-native and serverless security",
        ],
        "threats": [
            "AI-generated code propagating insecure patterns",
            "low-code platforms lacking security guardrails",
            "cloud-native architectures introducing new attack surfaces",
        ],
        "summary": (
            "FIASSE adapts to AI-driven development, low-code platforms, "
            "cloud-native architectures, and continuous security engineering."
        ),
    },
    "8.2": {
        "title": "Organizational Adoption Strategies",
        "when_to_use": [
            "planning organizational adoption of FIASSE",
            "assessing readiness for FIASSE integration",
            "identifying security champions and key influencers",
        ],
        "threats": [
            "failed adoption from lack of stakeholder buy-in",
            "FIASSE treated as separate security initiative",
        ],
        "summary": (
            "Strategic adoption: assess practices, integrate SSEM terminology, "
            "identify influencers, educate teams, foster collaboration, monitor."
        ),
    },
}

# ---------------------------------------------------------------------------
# Section-ID mapping to RFC heading patterns
# ---------------------------------------------------------------------------
# The FIASSE RFC uses numbered headings (## 1. Introduction, ### 1.1., etc.).
# We define the target sections and the heading patterns that start/end them.

# Ordered list of section IDs we want to extract.
TARGET_SECTIONS: list[str] = [
    "2.1", "2.2", "2.3", "2.4", "2.5", "2.6",
    "3.1", "3.2.1", "3.2.2", "3.2.3", "3.3.1", "3.3.2",
    "3.4.1", "3.4.2", "3.4.3",
    "4.1", "4.2", "4.3", "4.4",
    "5.1", "5.2",
    "6.1", "6.2", "6.3", "6.4", "6.5",
    "7.0", "7.1", "7.2", "7.3",
    "8.1", "8.2",
]

# Map section_id -> regex pattern matching its starting heading in the RFC.
# The RFC uses varied heading levels (##, ###, ####) so we match flexibly.
HEADING_PATTERNS: dict[str, re.Pattern] = {
    sid: re.compile(
        rf"^#{{2,5}}\s+{re.escape(sid)}\.?\s",
        re.MULTILINE,
    )
    for sid in TARGET_SECTIONS
}

# For sections that are parents of sub-sections (e.g. 3.2 contains 3.2.1),
# we need to know where each section ENDS. A section ends at the start of
# the next sibling or parent heading. We build this from TARGET_SECTIONS order.

# Map section_id -> list of regex patterns that signal the end of this section.
# The section ends when any of these patterns match (whichever comes first).

# Next-sibling mappings (section -> next section at same or higher level)
_NEXT_SECTION: dict[str, str | None] = {}
for i, sid in enumerate(TARGET_SECTIONS):
    _NEXT_SECTION[sid] = TARGET_SECTIONS[i + 1] if i + 1 < len(TARGET_SECTIONS) else None

# Also include higher-level headings that would terminate a section.
# E.g. "## 4." terminates anything in section 3.x.
_CHAPTER_HEADS = [
    re.compile(rf"^#{{2,3}}\s+{ch}\.\s", re.MULTILINE)
    for ch in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
]


def _find_heading(content: str, section_id: str, start: int = 0) -> int | None:
    """Return the character offset of the heading for section_id, or None."""
    pat = HEADING_PATTERNS.get(section_id)
    if not pat:
        return None
    m = pat.search(content, start)
    return m.start() if m else None


def _find_section_end(content: str, section_id: str, body_start: int) -> int:
    """
    Find where a section ends. It ends at the start of the next target section's
    heading, or at a higher-level chapter heading, whichever comes first.
    """
    candidates: list[int] = []

    # Next section in our ordered list
    nxt = _NEXT_SECTION.get(section_id)
    if nxt:
        pos = _find_heading(content, nxt, body_start)
        if pos is not None:
            candidates.append(pos)

    # Any higher-level chapter heading
    # Determine current top-level chapter number
    top = section_id.split(".")[0]
    for pat in _CHAPTER_HEADS:
        m = pat.search(content, body_start)
        if m:
            # Only count if it's a DIFFERENT chapter
            heading_text = content[m.start():m.end()]
            heading_num = re.search(r"(\d+)\.", heading_text)
            if heading_num and heading_num.group(1) != top:
                candidates.append(m.start())

    return min(candidates) if candidates else len(content)


def extract_sections(content: str) -> list[tuple[str, str]]:
    """
    Parse FIASSE RFC markdown into (section_id, body) tuples.
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
    Read source_path (FIASSE RFC .md), extract sections, write each to dest_dir
    with YAML frontmatter. Returns paths of written files.
    """
    if not source_path.is_file():
        raise FileNotFoundError(f"Not a file: {source_path}")

    text = source_path.read_text(encoding="utf-8")
    sections = extract_sections(text)

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for section_id, body in sections:
        frontmatter = _build_frontmatter(section_id, body)
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

              source.md  Path to FIASSE RFC markdown file.
              dest_dir   Output directory (default: data/fiasse).

            Downloads the latest RFC:
              curl -o /tmp/FIASSE-RFC.md \\
                https://raw.githubusercontent.com/Xcaciv/securable_software_engineering/main/docs/FIASSE-RFC.md
              python scripts/extract_fiasse_sections.py /tmp/FIASSE-RFC.md data/fiasse/
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
