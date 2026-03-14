---
name: security-guidance
description: Security-first development guidance based on OWASP ASVS (Application Security Verification Standard). Use this skill automatically when planning or implementing any code that touches user input, authentication, data persistence, network communication, file I/O, cryptography, or access control. This skill ensures all generated code adheres to industry-standard security practices with explicit references to applied guidance.
---

# Security Guidance

## Core Principle

Security is a first-class requirement. Before completing any plan or producing any code that touches security-sensitive operations, consult the ASVS reference index below and apply all relevant guidance.

**All generated code and plans must demonstrably adhere to the selected guidance, with safe defaults and explicit inline citations.**

## Workflow

1. **Identify relevant sections** — Match the current task against the `When to use:` triggers in the index below. A task may match multiple sections; apply all of them.
2. **Read the reference file** — For each matched section, read the full reference file listed at the end of its index entry to get the complete verification requirements.
3. **Apply the guidance** — Implement the requirements. Default to the most secure option when the requirements allow choice. Apply all Level 1 requirements as a minimum baseline; note any Level 2 or Level 3 requirements that are relevant but not yet implemented.
4. **Cite applied requirements inline** — In code comments or plan notes, reference each requirement you satisfy: `// ASVS 6.2.4: password checked against top-3000 list`.

## Escalation

If no section in the index matches a task that involves security-sensitive operations, or if guidance is conflicting or unclear, **stop and flag the gap** before proceeding. Do not guess or paraphrase guidance — escalate instead.

If the index below is empty, report that the reference index failed to load and list which ASVS chapters are likely relevant based on the task description.

## Reference Index

### V1.1 Encoding and Sanitization Architecture

Architectural requirements for the order and placement of encoding, escaping, and decoding operations.

When to use:

- designing a data processing pipeline that handles untrusted input
- deciding where in the request/response lifecycle to encode or escape data
- storing data that will later be rendered in different output contexts

See `references/asvs/V1.1.md` for detailed guidance.

### V1.2 Injection Prevention

Output encoding and escaping requirements to prevent injection into interpreters (SQL, HTML, JS, OS, LDAP, etc.).

When to use:

- building database queries (SQL, NoSQL, HQL, Cypher, XPath, LDAP)
- constructing OS commands or shell scripts with dynamic data
- building URLs or redirects with user-supplied values
- rendering user input inside HTML, CSS, or JavaScript
- processing LaTeX input
- evaluating regular expressions containing user-supplied patterns
- generating CSV, XLS, or spreadsheet exports with user data

See `references/asvs/V1.2.md` for detailed guidance.

### V1.3 Sanitization

Requirements for sanitizing untrusted HTML and dynamic content when encoding is not applicable.

When to use:

- accepting rich text or HTML input from users (e.g., WYSIWYG editors)
- using eval() or dynamic code execution with user-supplied content
- rendering user-submitted markup where encoding alone is insufficient

See `references/asvs/V1.3.md` for detailed guidance.

### V1.4 Memory, String, and Unmanaged Code

Requirements for safe memory handling and string operations in unmanaged or low-level code.

When to use:

- writing or integrating unmanaged code (C, C++, assembly)
- using unsafe memory operations, pointer arithmetic, or raw buffers
- calling native libraries or FFI from a managed language
- handling string operations in low-level or performance-critical code

See `references/asvs/V1.4.md` for detailed guidance.

### V1.5 Safe Deserialization

Requirements for safely deserializing data from untrusted or external sources.

When to use:

- deserializing objects or data structures from untrusted sources
- accepting serialized data via network, file upload, or API payloads
- using Java serialization, Python pickle, PHP unserialize, or similar mechanisms
- processing binary or text-based serialization formats (XML, JSON, YAML, MessagePack)

See `references/asvs/V1.5.md` for detailed guidance.

### V2.1 Validation and Business Logic Documentation

Requirements for documenting expected inputs and business logic rules.

When to use:

- documenting what inputs an application accepts and their expected formats
- defining business rules and workflow constraints for a feature

See `references/asvs/V2.1.md` for detailed guidance.

### V2.2 Input Validation

Requirements for validating input data at application boundaries.

When to use:

- processing any user-supplied input at an application boundary
- validating that inputs match expected types, formats, lengths, or value ranges
- checking data received from external systems or APIs

See `references/asvs/V2.2.md` for detailed guidance.

### V2.3 Business Logic Security

Requirements for securing business workflows against manipulation, skipping steps, or race conditions.

When to use:

- implementing multi-step workflows or transaction sequences
- enforcing ordering or timing constraints between operations
- handling financial transactions, inventory updates, or state machines
- implementing features where users should not be able to skip or replay steps

See `references/asvs/V2.3.md` for detailed guidance.

### V2.4 Anti-automation

Requirements for protecting against automated abuse, scraping, and excessive requests.

When to use:

- adding rate limiting to endpoints or operations
- protecting forms or APIs from automated abuse or credential stuffing
- implementing CAPTCHA or bot detection on public-facing endpoints
- limiting how many times an operation can be performed per user or IP

See `references/asvs/V2.4.md` for detailed guidance.

### V3.1 Web Frontend Security Documentation

Requirements for documenting frontend security decisions and browser security configurations.

When to use:

- documenting security decisions for a web frontend application
- defining which content security policies and browser protections will be used

See `references/asvs/V3.1.md` for detailed guidance.

### V3.2 Unintended Content Interpretation

Requirements to prevent browsers from misinterpreting response content types.

When to use:

- serving user-uploaded files or content from the application
- setting Content-Type headers for HTTP responses
- rendering HTML pages that include user-controlled content
- preventing browsers from MIME-sniffing response types

See `references/asvs/V3.2.md` for detailed guidance.

### V3.3 Cookie Setup

Requirements for securely configuring cookie attributes.

When to use:

- setting cookies in HTTP responses (session, preference, or tracking cookies)
- configuring cookie attributes (HttpOnly, Secure, SameSite, domain, path)

See `references/asvs/V3.3.md` for detailed guidance.

### V3.4 Browser Security Mechanism Headers

Requirements for HTTP security headers that instruct browsers to enforce security policies.

When to use:

- setting HTTP security headers on web application responses
- configuring Content Security Policy (CSP)
- setting HSTS, X-Frame-Options, Referrer-Policy, or Permissions-Policy headers

See `references/asvs/V3.4.md` for detailed guidance.

### V3.5 Browser Origin Separation

Requirements for enforcing origin boundaries and preventing cross-origin attacks in browsers.

When to use:

- configuring Cross-Origin Resource Sharing (CORS) policies
- building applications that interact across multiple origins or subdomains
- preventing cross-site request forgery (CSRF)
- using postMessage or cross-frame communication

See `references/asvs/V3.5.md` for detailed guidance.

### V3.6 External Resource Integrity

Requirements for verifying the integrity of externally loaded resources.

When to use:

- loading third-party scripts, stylesheets, or fonts from external CDNs
- using subresource integrity (SRI) for external assets
- embedding external resources in HTML pages

See `references/asvs/V3.6.md` for detailed guidance.

### V3.7 Other Browser Security Considerations

Miscellaneous browser security requirements not covered by other V3 sections.

When to use:

- building browser-based applications with complex client-side logic
- handling sensitive data in browser storage (localStorage, sessionStorage, IndexedDB)
- using service workers or browser caching mechanisms

See `references/asvs/V3.7.md` for detailed guidance.

### V4.1 Generic Web Service Security

General security requirements applicable to all HTTP-based web services.

When to use:

- building or consuming HTTP-based APIs or web services
- implementing REST endpoints
- designing the request/response lifecycle of a web service

See `references/asvs/V4.1.md` for detailed guidance.

### V4.2 HTTP Message Structure Validation

Requirements for validating the structure and fields of HTTP messages.

When to use:

- parsing HTTP request headers, query parameters, or body content in an API
- validating Content-Type, Accept, or other HTTP header fields
- handling HTTP request routing or middleware in a web service

See `references/asvs/V4.2.md` for detailed guidance.

### V4.3 GraphQL

Security requirements specific to GraphQL APIs.

When to use:

- implementing a GraphQL API or schema
- handling GraphQL queries, mutations, or subscriptions
- configuring a GraphQL server or gateway

See `references/asvs/V4.3.md` for detailed guidance.

### V4.4 WebSocket

Security requirements for WebSocket connections and message handling.

When to use:

- implementing WebSocket connections for real-time communication
- building a WebSocket server or client
- handling WebSocket upgrade requests and message routing

See `references/asvs/V4.4.md` for detailed guidance.

### V5.1 File Handling Documentation

Requirements for documenting file handling expectations and security decisions.

When to use:

- documenting file upload or download features
- defining accepted file types, sizes, and handling behavior for a feature

See `references/asvs/V5.1.md` for detailed guidance.

### V5.2 File Upload and Content

Requirements for securely accepting and validating user-uploaded files.

When to use:

- implementing file upload functionality
- accepting files from users via HTTP, form submission, or API
- validating file type, size, or content before processing
- handling zip or archive uploads that will be extracted

See `references/asvs/V5.2.md` for detailed guidance.

### V5.3 File Storage

Requirements for securely storing files and preventing path traversal or server-side execution.

When to use:

- storing uploaded or generated files on disk or object storage
- constructing file paths for stored files
- serving stored files via HTTP
- handling file paths provided by users

See `references/asvs/V5.3.md` for detailed guidance.

### V5.4 File Download

Requirements for securely serving files to users for download.

When to use:

- serving files for download via HTTP responses
- allowing users to download stored files
- setting Content-Disposition or Content-Type for file downloads

See `references/asvs/V5.4.md` for detailed guidance.

### V6.1 Authentication Documentation

Requirements for documenting authentication decisions and mechanisms.

When to use:

- documenting authentication mechanisms for an application
- defining which authentication methods are supported

See `references/asvs/V6.1.md` for detailed guidance.

### V6.2 Password Security

Requirements for securely handling user passwords, including storage, policies, and breach detection.

When to use:

- implementing password-based login
- storing or verifying user passwords
- implementing password creation, reset, or change flows
- enforcing password policies or checking against breached password lists

See `references/asvs/V6.2.md` for detailed guidance.

### V6.3 General Authentication Security

General security requirements for all authentication mechanisms.

When to use:

- implementing any authentication mechanism (login, API key, certificate)
- building login flows, authentication endpoints, or credential verification
- protecting authentication against brute force, enumeration, or timing attacks

See `references/asvs/V6.3.md` for detailed guidance.

### V6.4 Authentication Factor Lifecycle and Recovery

Requirements for managing authentication factor enrollment, recovery, and revocation.

When to use:

- implementing account recovery or password reset flows
- managing enrollment or removal of authentication factors
- handling forgotten passwords or locked accounts

See `references/asvs/V6.4.md` for detailed guidance.

### V6.5 General Multi-factor Authentication Requirements

General requirements for implementing multi-factor authentication.

When to use:

- adding multi-factor authentication (MFA) to a login flow
- implementing TOTP, hardware keys, or other second factors
- enforcing MFA for privileged or sensitive operations

See `references/asvs/V6.5.md` for detailed guidance.

### V6.6 Out-of-Band Authentication Mechanisms

Requirements for authentication mechanisms that use a separate out-of-band channel.

When to use:

- implementing SMS, email, or push notification-based authentication
- using out-of-band channels (phone call, email link) for login or verification

See `references/asvs/V6.6.md` for detailed guidance.

### V6.7 Cryptographic Authentication Mechanism

Requirements for cryptographic authentication mechanisms such as WebAuthn, passkeys, and client certificates.

When to use:

- implementing certificate-based authentication
- supporting hardware security keys (FIDO2, WebAuthn, passkeys)
- using cryptographic proof-of-possession for authentication

See `references/asvs/V6.7.md` for detailed guidance.

### V6.8 Authentication with an Identity Provider

Requirements for authenticating users via an external identity provider using federated protocols.

When to use:

- integrating with an external identity provider (IdP) for authentication
- implementing "Sign in with Google/Apple/GitHub" or similar social login
- federating authentication via SAML, OIDC, or similar protocols

See `references/asvs/V6.8.md` for detailed guidance.

### V7.1 Session Management Documentation

Requirements for documenting session management decisions.

When to use:

- documenting session management design for an application
- defining session token types and storage mechanisms

See `references/asvs/V7.1.md` for detailed guidance.

### V7.2 Fundamental Session Management Security

Foundational requirements for creating and issuing secure session tokens.

When to use:

- issuing session tokens or cookies after successful authentication
- generating session identifiers
- binding sessions to users after login

See `references/asvs/V7.2.md` for detailed guidance.

### V7.3 Session Timeout

Requirements for limiting session duration and implementing idle or absolute timeouts.

When to use:

- implementing session expiry or idle timeout
- configuring absolute or sliding session lifetimes
- managing session validity periods

See `references/asvs/V7.3.md` for detailed guidance.

### V7.4 Session Termination

Requirements for securely terminating sessions on logout or credential change.

When to use:

- implementing logout functionality
- invalidating sessions server-side on logout
- terminating all sessions when a user changes credentials

See `references/asvs/V7.4.md` for detailed guidance.

### V7.5 Defenses Against Session Abuse

Requirements for detecting and preventing session theft, fixation, and hijacking.

When to use:

- protecting sessions against fixation, hijacking, or replay attacks
- implementing session binding to device or IP
- detecting concurrent sessions from multiple locations

See `references/asvs/V7.5.md` for detailed guidance.

### V7.6 Federated Re-authentication

Requirements for session management in federated identity and SSO scenarios.

When to use:

- managing sessions in a federated SSO environment
- handling re-authentication requests from an identity provider
- implementing single logout (SLO) across federated services

See `references/asvs/V7.6.md` for detailed guidance.

### V8.1 Authorization Documentation

Requirements for documenting authorization rules and decision factors.

When to use:

- documenting access control rules and permission models
- defining which roles or attributes govern access to resources

See `references/asvs/V8.1.md` for detailed guidance.

### V8.2 General Authorization Design

Requirements for function-level, data-level, and field-level access control enforcement.

When to use:

- important when making changes to authentication implementations
- controlling which users can call which functions or endpoints
- restricting access to specific data records by user identity
- implementing object-level or field-level access control
- preventing insecure direct object reference (IDOR)

See `references/asvs/V8.2.md` for detailed guidance.

### V8.3 Operation Level Authorization

Requirements for enforcing authorization at the correct service tier and handling permission changes promptly.

When to use:

- enforcing authorization in server-side logic (not just client-side)
- applying permission changes immediately when roles are updated
- designing authorization in multi-service or microservice architectures

See `references/asvs/V8.3.md` for detailed guidance.

### V8.4 Other Authorization Considerations

Additional authorization requirements for multi-tenant systems and administrative interfaces.

When to use:

- building multi-tenant applications with tenant isolation
- implementing administrative or privileged interfaces
- applying contextual access controls (time, location, device) to authorization

See `references/asvs/V8.4.md` for detailed guidance.

### V9.1 Token Source and Integrity

Requirements for verifying the source, signature, and integrity of self-contained tokens.

When to use:

- validating JWTs or other self-contained tokens received from clients or services
- verifying the signature or integrity of tokens before trusting their claims
- configuring which signing algorithms are accepted for tokens

See `references/asvs/V9.1.md` for detailed guidance.

### V9.2 Token Content

Requirements for the content, claims, and lifetime of self-contained tokens.

When to use:

- defining the claims or payload stored inside a JWT or similar token
- setting expiry, audience, issuer, or other standard claims on tokens
- preventing sensitive data from being stored in token payloads

See `references/asvs/V9.2.md` for detailed guidance.

### V10.1 Generic OAuth and OIDC Security

General security requirements applicable to all OAuth and OIDC implementations.

When to use:

- implementing any OAuth 2.0 or OpenID Connect flow
- designing an application that uses OAuth or OIDC regardless of role

See `references/asvs/V10.1.md` for detailed guidance.

### V10.2 OAuth Client

Security requirements for applications acting as an OAuth client.

When to use:

- building an application that requests access tokens from an authorization server
- implementing the authorization code flow or other OAuth grant types as a client
- using PKCE in an OAuth client

See `references/asvs/V10.2.md` for detailed guidance.

### V10.3 OAuth Resource Server

Security requirements for APIs acting as an OAuth resource server.

When to use:

- building an API that accepts and validates OAuth access tokens
- implementing token introspection or JWT validation on an API
- protecting API endpoints using OAuth bearer tokens

See `references/asvs/V10.3.md` for detailed guidance.

### V10.4 OAuth Authorization Server

Security requirements for OAuth authorization servers that issue tokens.

When to use:

- implementing or configuring an OAuth authorization server
- issuing access tokens, refresh tokens, or authorization codes
- building a custom authorization server rather than using a third-party one

See `references/asvs/V10.4.md` for detailed guidance.

### V10.5 OIDC Client

Security requirements for applications acting as an OIDC relying party (client).

When to use:

- implementing OpenID Connect login in a relying party application
- validating OIDC ID tokens
- requesting user identity information (claims) via OIDC

See `references/asvs/V10.5.md` for detailed guidance.

### V10.6 OpenID Provider

Security requirements for OpenID Providers that authenticate users and issue ID tokens.

When to use:

- implementing or configuring an OpenID Provider
- issuing OIDC ID tokens and serving user identity claims
- building a custom identity provider that supports OIDC

See `references/asvs/V10.6.md` for detailed guidance.

### V10.7 Consent Management

Requirements for managing and recording user consent in OAuth and OIDC flows.

When to use:

- implementing OAuth consent screens or authorization dialogs
- managing user consent for delegated access to resources
- storing, revoking, or auditing user consent decisions

See `references/asvs/V10.7.md` for detailed guidance.

### V11.1 Cryptographic Inventory and Documentation

Requirements for documenting and inventorying cryptographic implementations.

When to use:

- documenting cryptographic choices in an application
- maintaining an inventory of cryptographic algorithms and keys in use
- planning migration to new or post-quantum cryptographic algorithms

See `references/asvs/V11.1.md` for detailed guidance.

### V11.2 Secure Cryptography Implementation

Requirements for correctly implementing cryptographic operations using vetted libraries.

When to use:

- implementing cryptographic operations in application code
- choosing and using cryptographic libraries or APIs
- ensuring correct usage of cryptographic primitives

See `references/asvs/V11.2.md` for detailed guidance.

### V11.3 Encryption Algorithms

Requirements for selecting and configuring approved encryption algorithms.

When to use:

- encrypting or decrypting data in an application
- choosing symmetric or asymmetric encryption algorithms and modes
- configuring encryption parameters (key size, IV, mode of operation)

See `references/asvs/V11.3.md` for detailed guidance.

### V11.4 Hashing and Hash-based Functions

Requirements for selecting approved hash functions and HMAC constructions.

When to use:

- hashing data for integrity verification or checksums
- using HMACs for message authentication
- choosing hash algorithms for non-password data

See `references/asvs/V11.4.md` for detailed guidance.

### V11.5 Random Values

Requirements for generating cryptographically secure random values.

When to use:

- generating random tokens, nonces, salts, or keys
- seeding random number generators in security-sensitive contexts
- generating session identifiers, CSRF tokens, or API keys

See `references/asvs/V11.5.md` for detailed guidance.

### V11.6 Public Key Cryptography

Requirements for using public key cryptography for signing and asymmetric encryption.

When to use:

- signing or verifying data with asymmetric (public/private) keys
- encrypting data with RSA or elliptic curve keys
- managing public/private key pairs
- implementing digital signatures or certificate-based operations

See `references/asvs/V11.6.md` for detailed guidance.

### V11.7 In-Use Data Cryptography

Requirements for cryptographic protections applied to data while it is actively being used.

When to use:

- protecting data while it is being processed in memory
- implementing confidential computing or secure enclaves
- minimizing the exposure window of sensitive data during processing

See `references/asvs/V11.7.md` for detailed guidance.

### V12.1 General TLS Security Guidance

General requirements for TLS configuration including protocol versions, cipher suites, and certificate management.

When to use:

- configuring TLS on any server or endpoint
- selecting TLS versions and cipher suites
- managing TLS certificates and revocation

See `references/asvs/V12.1.md` for detailed guidance.

### V12.2 HTTPS Communication with External Facing Services

Requirements for HTTPS on externally accessible services, including publicly trusted certificates.

When to use:

- exposing HTTP endpoints to end users or external clients
- configuring HTTPS on a public-facing web application or API
- obtaining and deploying TLS certificates for external services

See `references/asvs/V12.2.md` for detailed guidance.

### V12.3 General Service to Service Communication Security

Requirements for encrypted and authenticated communication between internal services and backends.

When to use:

- configuring encrypted communication between internal services or microservices
- connecting to databases, message queues, caches, or external APIs over a network
- setting up mutual TLS (mTLS) between services
- validating TLS certificates in outbound connections

See `references/asvs/V12.3.md` for detailed guidance.

### V13.1 Configuration Documentation

Requirements for documenting security-relevant configuration decisions.

When to use:

- documenting security configuration decisions for an application
- defining what configuration is required in different deployment environments

See `references/asvs/V13.1.md` for detailed guidance.

### V13.2 Backend Communication Configuration

Requirements for securely configuring the application's outbound backend connections.

When to use:

- configuring outbound connections from the application to backends (databases, APIs, services)
- setting timeouts, retries, or connection pool settings for backend communications

See `references/asvs/V13.2.md` for detailed guidance.

### V13.3 Secret Management

Requirements for securely storing, accessing, and rotating application secrets and credentials.

When to use:

- storing or accessing application secrets, API keys, database credentials, or certificates
- configuring environment variables or secret stores (Vault, AWS Secrets Manager, etc.)
- rotating or auditing secrets used by the application

See `references/asvs/V13.3.md` for detailed guidance.

### V13.4 Unintended Information Leakage

Requirements for preventing the application from leaking sensitive information through errors, headers, or responses.

When to use:

- configuring error pages and HTTP responses sent to clients
- disabling stack traces, debug output, or verbose error messages in production
- controlling what information the application reveals in headers or responses

See `references/asvs/V13.4.md` for detailed guidance.

### V14.1 Data Protection Documentation

Requirements for identifying, classifying, and documenting protection requirements for sensitive data.

When to use:

- classifying data sensitivity levels in an application
- documenting data protection requirements for different data categories
- designing data handling policies for PII or regulated data

See `references/asvs/V14.1.md` for detailed guidance.

### V14.2 General Data Protection

Requirements for protecting sensitive data from unauthorized access, leakage, and excessive exposure.

When to use:

- transmitting or storing sensitive data (PII, payment info, credentials)
- controlling what sensitive data is returned in API responses
- preventing sensitive data from leaking into URLs, logs, or caches
- implementing data retention or deletion policies

See `references/asvs/V14.2.md` for detailed guidance.

### V14.3 Client-side Data Protection

Requirements for protecting sensitive data stored or processed on client devices and browsers.

When to use:

- storing data in browser storage (localStorage, sessionStorage, cookies, IndexedDB)
- controlling what data is cached by browsers or client devices
- handling sensitive data in mobile or desktop client applications

See `references/asvs/V14.3.md` for detailed guidance.

### V15.1 Secure Coding and Architecture Documentation

Requirements for documenting dependency risk, dangerous functionality, and remediation policies.

When to use:

- managing third-party or open-source dependencies
- documenting risky or security-sensitive components in an application
- defining remediation timelines for vulnerable dependencies

See `references/asvs/V15.1.md` for detailed guidance.

### V15.2 Security Architecture and Dependencies

Requirements for dependency management, supply chain security, and architectural isolation of risky components.

When to use:

- managing third-party library versions and updates
- sandboxing or isolating high-risk components in the architecture
- protecting against dependency confusion or supply chain attacks
- designing for availability of resource-intensive operations

See `references/asvs/V15.2.md` for detailed guidance.

### V15.3 Defensive Coding

Requirements for defensive coding practices in security-sensitive code paths.

When to use:

- writing code that uses dynamic execution, reflection, or deserialization
- handling untrusted data in low-level or security-critical code paths
- implementing input handling in security-sensitive functions
- reviewing code for memory safety or injection risks

See `references/asvs/V15.3.md` for detailed guidance.

### V15.4 Safe Concurrency

Requirements for safe concurrency to prevent race conditions and data corruption in multi-threaded code.

When to use:

- writing multi-threaded or concurrent application code
- implementing shared state or shared resources across threads or processes
- using locks, semaphores, or other synchronization primitives
- designing async or parallel processing workflows

See `references/asvs/V15.4.md` for detailed guidance.

### V16.1 Security Logging Documentation

Requirements for documenting logging decisions and defining which events must be recorded.

When to use:

- designing a logging strategy for an application
- documenting what security events should be logged

See `references/asvs/V16.1.md` for detailed guidance.

### V16.2 General Logging

General requirements for what application logs should record and how.

When to use:

- implementing application logging
- deciding what information to include in log messages
- configuring log formats and output destinations

See `references/asvs/V16.2.md` for detailed guidance.

### V16.3 Security Events

Requirements for logging security-relevant events such as authentication, authorization failures, and sensitive actions.

When to use:

- logging authentication successes and failures
- recording authorization failures or access control decisions
- logging security-relevant user actions (password changes, account modifications)
- building an audit trail for sensitive operations

See `references/asvs/V16.3.md` for detailed guidance.

### V16.4 Log Protection

Requirements for protecting log data from tampering, injection, and unauthorized access.

When to use:

- protecting log files or log pipelines from tampering or unauthorized access
- forwarding logs to a centralized or immutable log store
- ensuring log integrity for forensic or audit purposes

See `references/asvs/V16.4.md` for detailed guidance.

### V16.5 Error Handling

Requirements for handling errors safely without leaking sensitive information to users.

When to use:

- implementing error handling and exception management in application code
- returning error responses to API consumers or users
- configuring error pages or error messages in a web application

See `references/asvs/V16.5.md` for detailed guidance.

### V17.1 TURN Server

Security requirements for TURN server deployments used in WebRTC applications.

When to use:

- operating or configuring a TURN server for WebRTC NAT traversal
- deploying coturn or similar TURN server infrastructure

See `references/asvs/V17.1.md` for detailed guidance.

### V17.2 Media

Security requirements for WebRTC media servers handling real-time audio and video streams.

When to use:

- hosting a WebRTC media server (SFU, MCU, recording server, or gateway)
- processing or routing SRTP/DTLS media streams on the server side
- building real-time audio/video conferencing infrastructure

See `references/asvs/V17.2.md` for detailed guidance.

### V17.3 Signaling

Security requirements for WebRTC signaling servers that coordinate peer connections.

When to use:

- implementing a WebRTC signaling server
- handling SDP offer/answer exchange between WebRTC peers
- securing the signaling channel for WebRTC session establishment

See `references/asvs/V17.3.md` for detailed guidance.
