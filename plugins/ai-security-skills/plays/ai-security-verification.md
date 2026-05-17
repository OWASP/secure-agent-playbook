# Play: AI Security Verification Standard (AISVS)

Comprehensive security verification of AI-driven applications using the OWASP AI Security Verification Standard (AISVS) framework's 13-category structured checklist.

## Trigger Conditions

Use this play when:
- Conducting security verification of AI/ML applications
- Performing pre-deployment security assessments
- Evaluating AI system compliance with security standards
- Auditing existing AI applications for security gaps
- Preparing for AI security certifications or compliance reviews
- Assessing third-party AI solutions before procurement

## Inputs

- AI application architecture documentation
- Model training and deployment pipelines
- Data governance policies and procedures
- Infrastructure and deployment configurations
- Access control and identity management systems
- Monitoring and logging implementations
- Human oversight and governance frameworks

## Procedure

### 1. Training Data Governance & Bias Management

Assess the security and integrity of training data and bias management processes.

#### Data Quality & Provenance
- [ ] **Data Source Verification** — Are training data sources authenticated and trusted?
- [ ] **Data Lineage Tracking** — Is complete data provenance maintained throughout the lifecycle?
- [ ] **Data Integrity Validation** — Are checksums, signatures, or other integrity mechanisms used?
- [ ] **Version Control** — Are training datasets properly versioned and change-controlled?

#### Bias Detection & Mitigation
- [ ] **Bias Assessment** — Are systematic bias evaluations performed on training data?
- [ ] **Demographic Parity** — Is fairness across protected groups measured and maintained?
- [ ] **Bias Mitigation Controls** — Are technical and procedural bias reduction measures implemented?
- [ ] **Ongoing Monitoring** — Is bias continuously monitored in production?

#### Data Governance
- [ ] **Data Classification** — Are training datasets properly classified by sensitivity?
- [ ] **Access Controls** — Are appropriate access restrictions applied to training data?
- [ ] **Retention Policies** — Are data retention and disposal policies enforced?
- [ ] **Compliance Alignment** — Do data practices align with regulatory requirements?

**Testing Approach:**
1. Review data governance documentation and policies
2. Audit data access logs and permissions
3. Analyze bias detection reports and mitigation measures
4. Verify data lineage and provenance tracking systems

---

### 2. User Input Validation

Evaluate input sanitization and validation mechanisms to prevent injection attacks.

#### Input Sanitization
- [ ] **Prompt Injection Defense** — Are prompt injection attacks detected and blocked?
- [ ] **Input Length Limits** — Are appropriate input size restrictions enforced?
- [ ] **Character Filtering** — Are dangerous characters and sequences filtered?
- [ ] **Encoding Validation** — Is input encoding properly validated and normalized?

#### Adversarial Input Detection
- [ ] **Anomaly Detection** — Are unusual input patterns detected and flagged?
- [ ] **Adversarial Example Detection** — Are crafted adversarial inputs identified?
- [ ] **Rate Limiting** — Are input submission rates controlled to prevent abuse?
- [ ] **Content Analysis** — Is input content analyzed for malicious intent?

#### Boundary Validation
- [ ] **Input Type Validation** — Are input types strictly validated against expected formats?
- [ ] **Range Checking** — Are numerical inputs validated against acceptable ranges?
- [ ] **Schema Validation** — Are structured inputs validated against defined schemas?
- [ ] **Context Awareness** — Does validation consider the specific use context?

**Testing Approach:**
1. Test prompt injection attacks with various payloads
2. Submit adversarial examples and malformed inputs
3. Verify input validation error handling
4. Check rate limiting and abuse prevention mechanisms

---

### 3. Model Lifecycle Management & Change Control

Review model versioning, deployment controls, and change management processes.

#### Model Versioning
- [ ] **Version Control** — Are model versions properly tracked and managed?
- [ ] **Artifact Management** — Are model artifacts securely stored and versioned?
- [ ] **Dependency Tracking** — Are model dependencies documented and managed?
- [ ] **Reproducibility** — Can model builds be reproduced from version control?

#### Deployment Controls
- [ ] **Staged Deployment** — Are models deployed through controlled staging environments?
- [ ] **Approval Workflows** — Are deployment approvals required and documented?
- [ ] **Rollback Capabilities** — Can deployments be quickly rolled back if issues arise?
- [ ] **Blue-Green Deployment** — Are zero-downtime deployment strategies used?

#### Change Management
- [ ] **Change Documentation** — Are all model changes properly documented?
- [ ] **Impact Assessment** — Are security impacts assessed before changes?
- [ ] **Testing Requirements** — Are security tests required before deployment?
- [ ] **Audit Trails** — Are complete audit trails maintained for all changes?

**Testing Approach:**
1. Review model version control and artifact management systems
2. Test rollback procedures and recovery capabilities
3. Audit change management documentation and approvals
4. Verify deployment pipeline security controls

---

### 4. Infrastructure, Configuration & Deployment Security

Examine deployment security, container hardening, and infrastructure configuration.

#### Container & Orchestration Security
- [ ] **Container Hardening** — Are containers built with minimal attack surface?
- [ ] **Image Scanning** — Are container images scanned for vulnerabilities?
- [ ] **Runtime Security** — Are runtime security controls implemented?
- [ ] **Orchestration Security** — Are Kubernetes/orchestration platforms secured?

#### Network Security
- [ ] **Network Segmentation** — Are AI workloads properly network-segmented?
- [ ] **Encryption in Transit** — Is all network traffic encrypted?
- [ ] **Firewall Rules** — Are restrictive firewall rules applied?
- [ ] **API Gateway Security** — Are API gateways properly configured and secured?

#### Configuration Management
- [ ] **Secure Defaults** — Are secure configuration defaults used?
- [ ] **Configuration Drift** — Is configuration drift detected and prevented?
- [ ] **Secrets Management** — Are secrets properly managed and rotated?
- [ ] **Hardening Standards** — Are infrastructure hardening standards applied?

**Testing Approach:**
1. Scan container images and runtime environments
2. Test network segmentation and firewall rules
3. Review configuration management and secrets handling
4. Assess orchestration platform security settings

---

### 5. Access Control & Identity

Verify authentication mechanisms, authorization controls, and privilege management.

#### Authentication
- [ ] **Multi-Factor Authentication** — Is MFA required for administrative access?
- [ ] **Strong Authentication** — Are strong authentication mechanisms used?
- [ ] **Session Management** — Are sessions properly managed and secured?
- [ ] **Identity Verification** — Are user identities properly verified?

#### Authorization
- [ ] **Role-Based Access Control** — Is RBAC implemented for AI system access?
- [ ] **Principle of Least Privilege** — Are minimal necessary permissions granted?
- [ ] **Attribute-Based Access Control** — Is ABAC used for fine-grained control?
- [ ] **Dynamic Authorization** — Are access decisions made dynamically based on context?

#### Privilege Management
- [ ] **Privileged Account Management** — Are privileged accounts properly managed?
- [ ] **Regular Access Reviews** — Are access permissions regularly reviewed?
- [ ] **Automated Provisioning** — Is account provisioning/deprovisioning automated?
- [ ] **Segregation of Duties** — Are conflicting duties properly separated?

**Testing Approach:**
1. Test authentication mechanisms and session management
2. Verify authorization controls and privilege escalation prevention
3. Review access control policies and implementations
4. Audit privileged account management processes

---

### 6. Supply Chain Security for Models, Frameworks & Data

Assess third-party model security, dependency management, and supply chain integrity.

#### Third-Party Model Security
- [ ] **Model Provenance** — Is the source and integrity of third-party models verified?
- [ ] **Model Scanning** — Are third-party models scanned for vulnerabilities?
- [ ] **License Compliance** — Are model licenses properly managed and compliant?
- [ ] **Vendor Assessment** — Are model vendors properly security-assessed?

#### Dependency Management
- [ ] **Dependency Scanning** — Are software dependencies scanned for vulnerabilities?
- [ ] **Version Pinning** — Are dependency versions pinned and controlled?
- [ ] **Supply Chain Attacks** — Are supply chain attack vectors mitigated?
- [ ] **SBOM Generation** — Are Software Bills of Materials maintained?

#### Framework Security
- [ ] **Framework Hardening** — Are AI/ML frameworks properly hardened?
- [ ] **Security Updates** — Are framework security updates promptly applied?
- [ ] **Configuration Security** — Are framework configurations securely managed?
- [ ] **API Security** — Are framework APIs properly secured?

**Testing Approach:**
1. Audit third-party model sources and verification processes
2. Scan dependencies for known vulnerabilities
3. Review supply chain security controls and policies
4. Verify SBOM accuracy and completeness

---

### 7. Model Behavior, Output Control & Safety Assurance

Evaluate output validation, safety guardrails, and harmful content prevention.

#### Output Validation
- [ ] **Output Sanitization** — Are model outputs properly sanitized?
- [ ] **Content Filtering** — Are harmful or inappropriate outputs filtered?
- [ ] **Format Validation** — Are output formats validated against expectations?
- [ ] **Consistency Checking** — Are outputs checked for logical consistency?

#### Safety Guardrails
- [ ] **Safety Boundaries** — Are clear safety boundaries defined and enforced?
- [ ] **Harmful Content Detection** — Is harmful content automatically detected?
- [ ] **Escalation Procedures** — Are escalation procedures defined for safety violations?
- [ ] **Kill Switches** — Are emergency stop mechanisms implemented?

#### Behavior Monitoring
- [ ] **Behavioral Baselines** — Are normal behavior patterns established?
- [ ] **Drift Detection** — Is model behavior drift detected and addressed?
- [ ] **Anomaly Detection** — Are behavioral anomalies flagged for review?
- [ ] **Performance Monitoring** — Is model performance continuously monitored?

**Testing Approach:**
1. Test output validation and sanitization mechanisms
2. Attempt to generate harmful or inappropriate content
3. Verify safety guardrail effectiveness
4. Review behavior monitoring and alerting systems

---

### 8. Memory, Embeddings & Vector Database Security

Review vector database security, embedding protection, and memory isolation.

#### Vector Database Security
- [ ] **Access Controls** — Are vector databases properly access-controlled?
- [ ] **Encryption** — Are embeddings encrypted at rest and in transit?
- [ ] **Backup Security** — Are vector database backups properly secured?
- [ ] **Query Security** — Are vector queries validated and secured?

#### Embedding Protection
- [ ] **Embedding Integrity** — Is embedding integrity verified and maintained?
- [ ] **Poisoning Prevention** — Are embedding poisoning attacks prevented?
- [ ] **Similarity Attacks** — Are similarity-based attacks mitigated?
- [ ] **Extraction Prevention** — Is embedding extraction prevented?

#### Memory Isolation
- [ ] **Context Isolation** — Are user contexts properly isolated?
- [ ] **Memory Boundaries** — Are memory boundaries enforced between sessions?
- [ ] **Data Leakage Prevention** — Is cross-user data leakage prevented?
- [ ] **Memory Cleanup** — Is sensitive memory properly cleared?

**Testing Approach:**
1. Test vector database access controls and encryption
2. Attempt embedding poisoning and extraction attacks
3. Verify context isolation and memory boundaries
4. Check for data leakage between user sessions

---

### 9. Autonomous Orchestration & Agentic Action Security

Assess agent coordination security, tool access controls, and autonomous decision-making safeguards.

#### Agent Coordination Security
- [ ] **Inter-Agent Authentication** — Do agents properly authenticate each other?
- [ ] **Message Integrity** — Are inter-agent messages integrity-protected?
- [ ] **Communication Encryption** — Are agent communications encrypted?
- [ ] **Coordination Protocols** — Are coordination protocols secure?

#### Tool Access Controls
- [ ] **Tool Authorization** — Are agent tool access permissions properly controlled?
- [ ] **Capability Boundaries** — Are agent capabilities clearly bounded?
- [ ] **Tool Validation** — Are tool invocations validated before execution?
- [ ] **Privilege Escalation Prevention** — Is agent privilege escalation prevented?

#### Autonomous Decision Safeguards
- [ ] **Decision Boundaries** — Are autonomous decision boundaries defined?
- [ ] **Human Override** — Can humans override autonomous decisions?
- [ ] **Decision Logging** — Are autonomous decisions logged and auditable?
- [ ] **Risk Assessment** — Are high-risk decisions flagged for review?

**Testing Approach:**
1. Test inter-agent authentication and communication security
2. Verify tool access controls and capability boundaries
3. Attempt privilege escalation and unauthorized tool access
4. Review autonomous decision-making safeguards

---

### 10. Adversarial Robustness & Attack Resistance

Test resilience against adversarial examples, evasion attacks, and model extraction attempts.

#### Adversarial Example Resistance
- [ ] **Adversarial Training** — Are models trained with adversarial examples?
- [ ] **Input Preprocessing** — Are adversarial inputs detected and preprocessed?
- [ ] **Robustness Testing** — Is adversarial robustness regularly tested?
- [ ] **Defense Mechanisms** — Are adversarial defense mechanisms implemented?

#### Evasion Attack Prevention
- [ ] **Evasion Detection** — Are evasion attempts detected and blocked?
- [ ] **Model Ensemble** — Are ensemble methods used to improve robustness?
- [ ] **Uncertainty Quantification** — Is prediction uncertainty properly quantified?
- [ ] **Anomaly Detection** — Are evasive inputs flagged as anomalous?

#### Model Extraction Protection
- [ ] **Query Limiting** — Are model queries rate-limited and monitored?
- [ ] **Output Obfuscation** — Are model outputs obfuscated to prevent extraction?
- [ ] **Watermarking** — Are models watermarked for ownership protection?
- [ ] **API Security** — Are model APIs secured against extraction attacks?

**Testing Approach:**
1. Generate and test adversarial examples against the model
2. Attempt evasion attacks using various techniques
3. Test model extraction through API queries
4. Verify robustness defense mechanisms

---

### 11. Privacy Protection & Personal Data Management

Verify privacy controls, data minimization, consent management, and regulatory compliance.

#### Privacy Controls
- [ ] **Data Minimization** — Is data collection limited to necessary purposes?
- [ ] **Purpose Limitation** — Is data used only for stated purposes?
- [ ] **Anonymization** — Are appropriate anonymization techniques used?
- [ ] **Differential Privacy** — Is differential privacy implemented where appropriate?

#### Consent Management
- [ ] **Informed Consent** — Is informed consent obtained for data processing?
- [ ] **Consent Withdrawal** — Can users withdraw consent and have data deleted?
- [ ] **Granular Consent** — Is granular consent provided for different uses?
- [ ] **Consent Records** — Are consent records properly maintained?

#### Regulatory Compliance
- [ ] **GDPR Compliance** — Are GDPR requirements met (where applicable)?
- [ ] **CCPA Compliance** — Are CCPA requirements met (where applicable)?
- [ ] **Data Subject Rights** — Are data subject rights properly supported?
- [ ] **Privacy Impact Assessment** — Are PIAs conducted for high-risk processing?

**Testing Approach:**
1. Review privacy policies and consent mechanisms
2. Test data subject rights implementation
3. Verify anonymization and privacy-preserving techniques
4. Audit regulatory compliance measures

---

### 12. Monitoring, Logging & Anomaly Detection

Evaluate security monitoring, audit logging, and incident response capabilities.

#### Security Monitoring
- [ ] **Real-Time Monitoring** — Is real-time security monitoring implemented?
- [ ] **Threat Detection** — Are security threats automatically detected?
- [ ] **Alert Management** — Are security alerts properly managed and responded to?
- [ ] **Dashboard Visibility** — Are security dashboards available to operators?

#### Audit Logging
- [ ] **Comprehensive Logging** — Are all security-relevant events logged?
- [ ] **Log Integrity** — Is log integrity protected against tampering?
- [ ] **Log Retention** — Are logs retained for appropriate periods?
- [ ] **Log Analysis** — Are logs regularly analyzed for security insights?

#### Anomaly Detection
- [ ] **Behavioral Baselines** — Are normal behavior baselines established?
- [ ] **Statistical Anomalies** — Are statistical anomalies detected and flagged?
- [ ] **ML-Based Detection** — Are ML techniques used for anomaly detection?
- [ ] **False Positive Management** — Are false positives properly managed?

**Testing Approach:**
1. Review monitoring and alerting configurations
2. Test log integrity and retention mechanisms
3. Verify anomaly detection effectiveness
4. Assess incident response procedures

---

### 13. Human Oversight and Trust

Assess human-in-the-loop controls, explainability mechanisms, and trust calibration measures.

#### Human-in-the-Loop Controls
- [ ] **Human Review Points** — Are human review points defined for critical decisions?
- [ ] **Override Mechanisms** — Can humans override AI decisions when necessary?
- [ ] **Escalation Procedures** — Are clear escalation procedures defined?
- [ ] **Human Training** — Are human operators properly trained on AI systems?

#### Explainability & Transparency
- [ ] **Decision Explanations** — Are AI decisions explainable to users?
- [ ] **Model Interpretability** — Are model behaviors interpretable?
- [ ] **Transparency Reports** — Are transparency reports provided to stakeholders?
- [ ] **Algorithmic Auditing** — Are algorithms regularly audited for fairness?

#### Trust Calibration
- [ ] **Confidence Indicators** — Are confidence levels communicated to users?
- [ ] **Uncertainty Quantification** — Is prediction uncertainty properly communicated?
- [ ] **Trust Metrics** — Are trust metrics established and monitored?
- [ ] **User Education** — Are users educated about AI capabilities and limitations?

**Testing Approach:**
1. Test human override and escalation mechanisms
2. Evaluate explanation quality and interpretability
3. Review trust calibration and confidence indicators
4. Assess user education and training programs

## Risk Prioritization Matrix

Prioritize findings based on severity and impact:

| AISVS Category | Example Finding | Severity | Impact | Priority |
|----------------|----------------|----------|--------|----------|
| Input Validation | Prompt injection vulnerability | High | High | Critical |
| Access Control | Weak authentication | High | Medium | High |
| Supply Chain | Unverified third-party model | Medium | High | High |
| Privacy Protection | GDPR non-compliance | Medium | High | High |
| Monitoring | Insufficient logging | Low | Medium | Medium |

## Output Format

```markdown
## AI Security Verification Assessment: [Application Name]

### Executive Summary
- **Overall AISVS Compliance**: [X/13 categories fully compliant]
- **Critical Findings**: [Number of critical security gaps]
- **Compliance Status**: [Ready/Not Ready for production]

### AISVS Category Assessment

#### 1. Training Data Governance & Bias Management
- **Status**: [Compliant/Partial/Non-Compliant]
- **Key Findings**: [Summary of findings]
- **Recommendations**: [Priority actions]

[Repeat for all 13 categories]

### Critical Security Gaps
[High-priority findings requiring immediate attention]

### Compliance Roadmap
[Structured plan to achieve full AISVS compliance]

### Verification Evidence
[Documentation supporting compliance claims]

### Risk Assessment
[Overall risk rating and justification]
```

## OWASP References

- **OWASP AI Security Verification Standard (AISVS)**
- OWASP Top 10 for LLM Applications 2025
- OWASP AI Security and Privacy Guide
- OWASP Application Security Verification Standard (ASVS)
- OWASP AI Testing Guide
- OWASP Agentic AI Top 10