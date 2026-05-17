# Play: API Security Review

Comprehensive API security assessment against OWASP API Security Top 10 (2023) with real-world attack scenarios, automated testing integration, and detailed remediation guidance.

## Trigger Conditions

Use this play when:
- Reviewing OpenAPI/Swagger specifications or API documentation
- Auditing REST, GraphQL, gRPC, or SOAP API implementations
- Testing API authentication and authorization mechanisms
- Reviewing API gateway configurations (Kong, nginx, Envoy, AWS API Gateway)
- Conducting pre-deployment security assessments
- Performing API penetration testing or security audits
- A user asks to "test my API for security issues"

## Inputs

- OpenAPI/Swagger specification (YAML/JSON) or API documentation
- API source code (routes, controllers, middleware, authentication logic)
- API gateway and infrastructure configurations
- Authentication implementation details (JWT, OAuth, API keys)
- Environment information (production, staging, development)
- Previous security assessment reports (if available)

## Procedure

### Phase 1: Discovery & Reconnaissance

#### 1.1 API Surface Enumeration

**With OpenAPI Spec:**
```bash
# Parse and analyze OpenAPI spec
# Look for:
- Total endpoints and HTTP methods
- Authentication requirements per endpoint
- Request/response schemas
- Rate limiting documentation
- Deprecated endpoints
```

**Without OpenAPI Spec (Code Analysis):**
- Scan route definitions in framework-specific patterns:
  - Express: `app.get()`, `router.post()`
  - Django: `path()`, `url()`
  - Rails: `resources`, `get/post/put/delete`
  - Spring: `@GetMapping`, `@RequestMapping`
  - FastAPI: `@app.get()`, decorator-based routes

**Key Questions:**
- How many endpoints exist?
- Which require authentication vs. public?
- What data types are exchanged?
- Are there file upload endpoints?
- Are there admin/debug endpoints?

#### 1.2 Authentication Mechanism Identification

Document all auth mechanisms in use:

| Mechanism | Indicators | Security Considerations |
|-----------|-----------|------------------------|
| **JWT** | `Authorization: Bearer eyJ...` | Algorithm, signing key strength, expiration |
| **OAuth 2.0** | `/oauth/authorize`, `/oauth/token` | Flow type, PKCE, state parameter, redirect URI |
| **API Keys** | `X-API-Key`, `api_key` query param | Key rotation, transmission security, scope |
| **Session Cookies** | `Set-Cookie: sessionid=...` | HttpOnly, Secure, SameSite, expiration |
| **mTLS** | Client certificate requirements | Certificate validation, revocation |
| **Basic Auth** | `Authorization: Basic base64` | HTTPS enforcement, credential storage |

### Phase 2: Authentication Security Assessment

#### 2.1 JWT Security Testing

**Common JWT Vulnerabilities:**

1. **Algorithm Confusion (CVE-2015-9235)**
   ```
   Attack: Change algorithm from RS256 to none or HS256
   Header: {"alg":"none","typ":"JWT"}
   Result: Token accepted without verification
   ```

2. **Weak Signing Keys**
   ```bash
   # Test for weak secrets if using HS256
   # Use jwt_tool or hashcat for brute force
   jwt_tool.py token_here -C -d /usr/share/wordlists/rockyou.txt
   ```

3. **Missing Expiration**
   ```
   Check: Does payload contain "exp" claim?
   Risk: Tokens valid forever if stolen
   ```

4. **Token Storage Issues**
   ```javascript
   // Insecure: localStorage (XSS accessible)
   localStorage.setItem('jwt', token);
   
   // More secure: httpOnly cookie
   document.cookie = "jwt=" + token + "; HttpOnly; Secure; SameSite=Strict";
   ```

**Testing Checklist:**
- [ ] Test algorithm confusion (change alg to "none")
- [ ] Attempt key confusion attacks (RS256 → HS256)
- [ ] Check for missing expiration (exp claim)
- [ ] Verify signature validation cannot be bypassed
- [ ] Test token revocation mechanisms
- [ ] Check for sensitive data in JWT payload

#### 2.2 OAuth 2.0 Security Testing

**Critical Checks:**

1. **Authorization Code Flow**
   ```
   Required: PKCE (Proof Key for Code Exchange)
   Check: code_challenge and code_verifier parameters
   Risk: Without PKCE, auth codes can be stolen and used
   ```

2. **State Parameter**
   ```
   Required: Random state parameter to prevent CSRF
   Check: Is state validated on callback?
   Attack: Omit state → CSRF login attack
   ```

3. **Redirect URI Validation**
   ```
   Check: Is redirect_uri strictly validated?
   Attack: redirect_uri=https://attacker.com/callback
   Risk: Authorization code/token sent to attacker
   ```

4. **Scope Validation**
   ```
   Check: Can user modify requested scopes?
   Attack: Change scope=read to scope=admin
   Risk: Privilege escalation via scope manipulation
   ```

**Testing Checklist:**
- [ ] Verify PKCE implementation for public clients
- [ ] Test state parameter CSRF protection
- [ ] Attempt redirect URI manipulation
- [ ] Test scope escalation attacks
- [ ] Check for open redirect vulnerabilities
- [ ] Verify token endpoint authentication

#### 2.3 API Key Security

**Common Issues:**

1. **Key Exposure**
   ```bash
   # Search for hardcoded keys
   grep -r "api_key\|apikey\|api-key" --include="*.js" --include="*.py" --include="*.env"
   
   # Check client-side code
   # API keys in frontend code can be stolen
   ```

2. **Insufficient Scope**
   ```
   Issue: Single key with full access
   Best Practice: Scoped keys (read-only, write, admin)
   ```

3. **Missing Rotation**
   ```
   Check: Can keys be rotated without downtime?
   Risk: Compromised keys valid indefinitely
   ```

### Phase 3: OWASP API Top 10 Deep Assessment

#### API1: Broken Object Level Authorization (BOLA/IDOR)

> **Risk**: Attackers access other users' data by manipulating object IDs

**Real-World Impact**:
- **2019**: First American Financial exposed 885 million records via IDOR
- **2020**: Twitter API IDOR allowed viewing protected tweets
- **2021**: Facebook IDOR exposed private posts

**Attack Scenarios:**

1. **Sequential ID Manipulation**
   ```http
   GET /api/users/123/orders
   
   # Try:
   GET /api/users/124/orders  # Access other user's orders
   GET /api/users/1/orders    # Access admin's orders
   ```

2. **UUID Predictability**
   ```
   If using predictable UUIDv1 (timestamp-based):
   Generate nearby UUIDs to find other users
   ```

3. **Batch Endpoint Bypass**
   ```http
   POST /api/orders/bulk
   {
     "order_ids": [1001, 1002, 1003, 1004]  # Can access any IDs?
   }
   ```

4. **Indirect Object References**
   ```http
   GET /api/orders?id=1001
   
   # vs
   
   GET /api/orders?id=1001&user_id=123  # Is user_id validated?
   ```

**Testing Approach:**

1. **Map Object IDs**: Identify all endpoints accepting object IDs
2. **Cross-User Testing**: 
   - Create User A and User B accounts
   - Have User A create resources
   - Attempt to access with User B's credentials
3. **Batch Testing**: Test if batch endpoints filter by ownership
4. **File Access**: Test file download endpoints with different IDs
5. **IDOR Automation**:
   ```bash
   # Use Burp Intruder or custom script
   # Iterate through IDs and check for 200 responses
   for i in {1..1000}; do
     curl -H "Authorization: Bearer $TOKEN" \
          "https://api.example.com/orders/$i" | grep -q "order_id" && echo "Found: $i"
   done
   ```

**Remediation:**
```python
# BAD: No ownership check
def get_order(order_id):
    return Order.objects.get(id=order_id)

# GOOD: Verify ownership
def get_order(order_id, user):
    return Order.objects.get(id=order_id, user=user)
    # Or: Check ownership after retrieval
    order = Order.objects.get(id=order_id)
    if order.user_id != user.id:
        raise PermissionDenied()
    return order
```

#### API2: Broken Authentication

> **Risk**: Weak authentication allows account takeover

**Real-World Impact**:
- **2022**: Uber breach via compromised contractor account
- **2023**: 23andMe breach via credential stuffing

**Attack Scenarios:**

1. **Credential Stuffing**
   ```bash
   # Automated login attempts with breached credentials
   # APIs often lack CAPTCHA or rate limiting
   ```

2. **JWT None Algorithm**
   ```
   Header: {"alg":"none","typ":"JWT"}
   Payload: {"user_id":1,"role":"admin"}
   Signature: (empty)
   
   Result: Server accepts unsigned token
   ```

3. **Weak Password Policy**
   ```
   POST /api/login
   {"username":"admin","password":"123456"}
   
   # Test common passwords
   # Check minimum length requirements
   ```

4. **Session Fixation**
   ```
   Attacker sets session ID
   Victim logs in with attacker's session ID
   Attacker uses same session ID to access account
   ```

**Testing Approach:**

1. **Brute Force Testing**:
   ```bash
   # Test login endpoint rate limiting
   for i in {1..100}; do
     curl -X POST https://api.example.com/login \
          -d "username=admin&password=wrong$i"
   done
   # Check if account locks or IP is blocked
   ```

2. **Token Security**:
   - Decode JWT and analyze claims
   - Test algorithm confusion
   - Check expiration and refresh mechanisms
   - Test token revocation

3. **Password Policy**:
   - Test minimum length (should be 12+)
   - Test complexity requirements
   - Check common password blocking
   - Verify secure password reset flow

4. **Multi-Factor Authentication**:
   - Is MFA enforced for sensitive operations?
   - Can MFA be bypassed?
   - Are backup codes secure?

**Remediation:**
```python
# Implement rate limiting
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login(request):
    # Login logic
    pass

# Strong password validation
from django.contrib.auth.password_validation import validate_password

def validate_user_password(password):
    try:
        validate_password(password)
    except ValidationError as e:
        raise e

# Secure JWT configuration
JWT_SETTINGS = {
    'ALGORITHM': 'HS256',  # Use strong algorithms only
    'VERIFY_EXPIRATION': True,
    'EXPIRATION_DELTA': timedelta(minutes=15),
    'REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}
```

#### API3: Broken Object Property Level Authorization

> **Risk**: Mass assignment and data over-exposure

**Real-World Impact**:
- **2012**: GitHub mass assignment allowed unauthorized repo access
- **2019**: Facebook mass assignment exposed user data

**Attack Scenarios:**

1. **Mass Assignment**
   ```http
   POST /api/users
   {
     "username": "newuser",
     "email": "user@example.com",
     "password": "password123",
     "role": "admin",  # Should not be user-settable
     "is_verified": true  # Should not be user-settable
   }
   ```

2. **Response Over-Exposure**
   ```http
   GET /api/users/123
   
   Response:
   {
     "id": 123,
     "username": "john",
     "email": "john@example.com",
     "password_hash": "$2b$12$...",  # Should not be exposed!
     "ssn": "123-45-6789",  # PII exposure
     "internal_notes": "Difficult customer"
   }
   ```

3. **Field-Level Authorization Bypass**
   ```http
   PUT /api/users/123
   {
     "salary": 200000  # Can regular users modify this?
   }
   ```

**Testing Approach:**

1. **Mass Assignment Testing**:
   ```python
   # Send extra fields in POST/PUT requests
   payload = {
       "username": "test",
       "email": "test@test.com",
       "password": "password",
       "role": "admin",  # Try to escalate
       "is_admin": True,
       "credit_balance": 10000
   }
   ```

2. **Response Analysis**:
   - Capture all API responses
   - Look for sensitive fields (passwords, tokens, PII)
   - Compare responses for different user roles
   - Check if internal fields are exposed

3. **GraphQL Over-Exposure**:
   ```graphql
   # Request fields you shouldn't see
   query {
     user(id: 123) {
       id
       name
       email
       password  # Should be rejected
       ssn       # Should be rejected
       salary    # Should be rejected for non-admins
     }
   }
   ```

**Remediation:**
```python
# Use allowlist approach
ALLOWED_USER_FIELDS = ['username', 'email', 'password']

def update_user(user_id, data, current_user):
    # Filter input to allowed fields only
    filtered_data = {k: v for k, v in data.items() 
                     if k in ALLOWED_USER_FIELDS}
    
    # Check field-level permissions
    if 'role' in data and not current_user.is_admin:
        raise PermissionDenied("Cannot modify role")
    
    return User.objects.filter(id=user_id).update(**filtered_data)

# Response serialization
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Explicit allowlist
        # Never include: password, ssn, internal_notes
```

#### API4: Unrestricted Resource Consumption

> **Risk**: DoS via resource exhaustion, financial drain

**Real-World Impact**:
- **2023**: OpenAI API abuse cost companies thousands
- **2022**: GraphQL query DoS attacks on multiple platforms

**Attack Scenarios:**

1. **Rate Limit Bypass**
   ```http
   # Distributed attack from multiple IPs
   # Or using different API keys
   # Or changing User-Agent headers
   ```

2. **Expensive Query Abuse**
   ```graphql
   # Deeply nested GraphQL query
   query {
     users {
       posts {
         comments {
           author {
             posts {
               comments {
                 author {
                   posts { ... }  # Infinite recursion potential
                 }
               }
             }
           }
         }
       }
     }
   }
   ```

3. **Large Payload Attacks**
   ```http
   POST /api/upload
   Content-Length: 1000000000  # 1GB file
   
   # Or JSON bomb:
   {"a":{"a":{"a":{"a":...}}}}  # Deeply nested JSON
   ```

4. **Pagination Abuse**
   ```http
   GET /api/items?limit=1000000  # Request all records
   GET /api/items?page=1&per_page=10000  # Large page size
   ```

**Testing Approach:**

1. **Rate Limit Testing**:
   ```bash
   # Test from single IP
   for i in {1..1000}; do
     curl https://api.example.com/data
   done
   
   # Test bypass methods:
   # - Different API keys
   # - Rotating User-Agents
   # - Distributed requests
   ```

2. **GraphQL DoS**:
   ```bash
   # Test query complexity
   # Test query depth
   # Test expensive operations
   ```

3. **Resource Exhaustion**:
   - Upload extremely large files
   - Send deeply nested JSON
   - Request massive result sets
   - Trigger expensive database queries

**Remediation:**
```python
# Rate limiting
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='100/h', method=['GET', 'POST'])
def api_endpoint(request):
    pass

# GraphQL safeguards
GRAPHQL_SETTINGS = {
    'MAX_DEPTH': 10,
    'MAX_COMPLEXITY': 1000,
    'DISABLE_INTROSPECTION': True,  # In production
}

# Pagination limits
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20

def get_items(request):
    page_size = min(
        int(request.GET.get('limit', DEFAULT_PAGE_SIZE)),
        MAX_PAGE_SIZE
    )
    return Item.objects.all()[:page_size]

# File upload limits
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Timeout configuration
REQUEST_TIMEOUT = 30  # seconds
```

#### API5: Broken Function Level Authorization

> **Risk**: Access to admin/sensitive functions without proper authorization

**Real-World Impact**:
- **2020**: Twitter admin tool breach
- **2021**: Parler admin API exposed

**Attack Scenarios:**

1. **Admin Endpoint Discovery**
   ```http
   GET /api/admin/users  # Try common admin paths
   GET /api/v1/admin/config
   GET /api/internal/audit-logs
   GET /api/debug/info
   ```

2. **HTTP Method Switching**
   ```http
   GET /api/users/123    # Allowed for regular users
   DELETE /api/users/123 # Should require admin, but is it checked?
   PUT /api/users/123/role  # Can users change their own role?
   ```

3. **Parameter-Based Access Control**
   ```http
   POST /api/users
   {
     "username": "test",
     "role": "admin"  # Is this validated server-side?
   }
   ```

**Testing Approach:**

1. **Endpoint Enumeration**:
   ```bash
   # Use wordlists to find admin endpoints
   # Common paths: /admin, /internal, /debug, /system
   ```

2. **Method Testing**:
   ```bash
   # For each endpoint, test all HTTP methods
   curl -X GET /api/resource
   curl -X POST /api/resource
   curl -X PUT /api/resource
   curl -X DELETE /api/resource
   curl -X PATCH /api/resource
   ```

3. **Role Escalation**:
   - Create regular user account
   - Attempt to access admin endpoints
   - Try to modify role/privilege fields

**Remediation:**
```python
# Centralized authorization decorator
from functools import wraps

def require_admin(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(
                {"error": "Admin access required"}, 
                status=403
            )
        return f(request, *args, **kwargs)
    return decorated_function

@require_admin
def admin_endpoint(request):
    pass

# Middleware approach
class AdminAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_paths = ['/api/admin/', '/api/internal/']
    
    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.admin_paths):
            if not request.user.is_admin:
                return HttpResponseForbidden()
        return self.get_response(request)
```

#### API6: Unrestricted Access to Sensitive Business Flows

> **Risk**: Automated abuse of business logic

**Real-World Impact**:
- **Ticket scalping**: Bots buying all concert tickets
- **E-commerce**: Inventory hoarding, price scraping
- **Crypto**: Flash loan attacks via API manipulation

**Attack Scenarios:**

1. **Inventory Exhaustion**
   ```http
   POST /api/cart/add
   {"product_id": 123, "quantity": 999999}  # Buy all inventory
   ```

2. **Automated Purchasing**
   ```http
   # Script that completes purchase faster than humans
   # Bypassing any client-side rate limits
   ```

3. **Price Manipulation**
   ```http
   POST /api/order
   {
     "items": [...],
     "total": 1.00  # Is total calculated server-side?
   }
   ```

4. **Reservation Abuse**
   ```http
   POST /api/reservations
   {"resource_id": 123, "start": "2024-01-01", "end": "2025-12-31"}
   # Reserve resource for entire year
   ```

**Testing Approach:**

1. **Business Logic Testing**:
   - Attempt to complete purchases with modified prices
   - Try to add negative quantities
   - Test race conditions in multi-step flows
   - Attempt to bypass payment steps

2. **Automation Testing**:
   ```python
   # Script to test if flows can be automated
   import requests
   import time
   
   start = time.time()
   for i in range(100):
       requests.post('/api/purchase', json={...})
   elapsed = time.time() - start
   
   # If no rate limiting, 100 requests complete quickly
   ```

**Remediation:**
```python
# Server-side price calculation
def create_order(items, user):
    total = sum(item.product.price * item.quantity for item in items)
    # Never trust client-provided total
    
    # Inventory checks
    for item in items:
        if item.quantity > item.product.available_stock:
            raise ValidationError("Insufficient inventory")
    
    # Rate limiting per user
    if user.orders.filter(created_at__gte=timezone.now() - timedelta(hours=1)).count() > 10:
        raise RateLimitError("Too many orders")
    
    return Order.objects.create(user=user, items=items, total=total)

# CAPTCHA for sensitive operations
from django_recaptcha.fields import ReCaptchaField

class PurchaseForm(forms.Form):
    recaptcha = ReCaptchaField()
    # ... other fields
```

#### API7: Server-Side Request Forgery (SSRF)

> **Risk**: Server makes requests to attacker-controlled or internal resources

**Real-World Impact**:
- **2019**: Capital One breach via SSRF (100M records)
- **2021**: Multiple cloud metadata service exploits

**Attack Scenarios:**

1. **Cloud Metadata Access**
   ```http
   GET /api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
   # Retrieves AWS credentials
   ```

2. **Internal Service Access**
   ```http
   GET /api/fetch?url=http://localhost:8080/admin
   GET /api/fetch?url=http://internal-api.company.local/secrets
   ```

3. **URL Bypass Techniques**
   ```
   http://127.0.0.1 → localhost bypass
   http://0177.0.0.1 → Octal encoding
   http://2130706433 → Decimal IP
   http://0x7f.0x0.0x0.0x1 → Hex encoding
   http://[::ffff:127.0.0.1] → IPv6
   http://127.1 → Shortened
   ```

4. **DNS Rebinding**
   ```
   Attacker controls DNS that resolves to:
   - First request: legitimate.com → 1.2.3.4
   - Second request: attacker.com → 169.254.169.254
   ```

**Testing Approach:**

1. **Basic SSRF Testing**:
   ```bash
   # Test internal IP access
   curl "https://api.example.com/fetch?url=http://169.254.169.254/"
   curl "https://api.example.com/fetch?url=http://localhost:22"
   curl "https://api.example.com/fetch?url=file:///etc/passwd"
   ```

2. **Bypass Testing**:
   ```bash
   # Try various encodings
   curl "https://api.example.com/fetch?url=http://0177.0.0.1/"
   curl "https://api.example.com/fetch?url=http://2130706433/"
   curl "https://api.example.com/fetch?url=http://[::ffff:127.0.0.1]/"
   ```

3. **Port Scanning via SSRF**:
   ```bash
   # Test if server can reach internal ports
   for port in 22 80 443 3306 5432 6379 8080; do
     curl "https://api.example.com/fetch?url=http://localhost:$port"
   done
   ```

**Remediation:**
```python
import ipaddress
import re
from urllib.parse import urlparse

def is_internal_ip(ip_str):
    """Check if IP is internal/private"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        return False

def validate_url(url):
    """Validate URL for SSRF prevention"""
    parsed = urlparse(url)
    
    # Allowlist approach (recommended)
    allowed_hosts = ['api.trusted.com', 'cdn.trusted.com']
    if parsed.hostname not in allowed_hosts:
        raise ValidationError("URL not in allowlist")
    
    # Blocklist approach (supplementary)
    blocked_schemes = ['file', 'ftp', 'gopher', 'dict']
    if parsed.scheme in blocked_schemes:
        raise ValidationError("Scheme not allowed")
    
    # Resolve and check IP
    import socket
    try:
        ip = socket.gethostbyname(parsed.hostname)
        if is_internal_ip(ip):
            raise ValidationError("Internal IPs not allowed")
    except socket.gaierror:
        raise ValidationError("Could not resolve hostname")
    
    return url

# Alternative: Use a dedicated SSRF protection library
# pip install ssrf-protect
from ssrf_protect import SSRFProtect

@SSRFProtect()
def fetch_url(request):
    url = request.GET.get('url')
    # Safe to fetch
    return requests.get(url)
```

#### API8: Security Misconfiguration

> **Risk**: Insecure default configurations expose APIs to attacks

**Real-World Impact**:
- **2018**: Tesla Kubernetes API exposed (cryptomining)
- **2020**: Multiple Elasticsearch instances exposed without auth

**Attack Scenarios:**

1. **CORS Misconfiguration**
   ```http
   Access-Control-Allow-Origin: *  # Too permissive
   Access-Control-Allow-Credentials: true  # Dangerous combination
   ```

2. **Verbose Error Messages**
   ```json
   {
     "error": "SQL syntax error near 'user_id = 123'",
     "stack_trace": "...",
     "query": "SELECT * FROM users WHERE user_id = 123"
   }
   ```

3. **Missing Security Headers**
   ```http
   # Missing headers:
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   Content-Security-Policy: ...
   Strict-Transport-Security: max-age=31536000
   ```

4. **Debug Mode Enabled**
   ```
   /api/debug/vars  # Exposes Go runtime variables
   /api/swagger-ui/  # API documentation with try-it feature
   /api/actuator/health  # Spring Boot endpoints
   ```

**Testing Approach:**

1. **Security Headers Check**:
   ```bash
   curl -I https://api.example.com/endpoint | grep -i "access-control\|x-"
   ```

2. **Error Handling Test**:
   ```bash
   # Trigger errors and check responses
   curl "https://api.example.com/endpoint?param=' OR 1=1--"
   curl "https://api.example.com/endpoint" -X INVALID_METHOD
   ```

3. **Debug Endpoint Discovery**:
   ```bash
   # Common debug paths
   /debug
   /actuator
   /swagger-ui
   /api-docs
   /health
   /metrics
   ```

**Remediation:**
```python
# Django middleware for security headers
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'"
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # CORS (restrictive)
        response['Access-Control-Allow-Origin'] = 'https://trusted-domain.com'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response

# Disable debug mode in production
DEBUG = False

# Custom error handler (don't expose internals)
from django.http import JsonResponse

def custom_error_handler(request, exception=None):
    return JsonResponse(
        {"error": "An error occurred"},
        status=500
    )
```

#### API9: Improper Inventory Management

> **Risk**: Shadow APIs and undocumented endpoints create attack surface

**Real-World Impact**:
- **2021**: Facebook API exposed user data via undocumented endpoint
- **2022**: Twitter API v1.1 endpoints still accessible after v2 launch

**Attack Scenarios:**

1. **Shadow API Discovery**
   ```
   Compare OpenAPI spec with actual code
   Look for endpoints not in documentation
   ```

2. **Deprecated API Usage**
   ```http
   GET /api/v1/users  # Old version still active
   GET /api/v2/users  # New version
   # v1 may have known vulnerabilities
   ```

3. **Environment Confusion**
   ```
   Production API: api.company.com
   Staging API: api-staging.company.com  # Exposed?
   Dev API: api-dev.company.com  # Exposed with debug enabled?
   ```

**Testing Approach:**

1. **API Inventory**:
   ```bash
   # Extract all routes from code
   grep -r "@app.route\|@GetMapping\|path(" --include="*.py" --include="*.java"
   
   # Compare with OpenAPI spec
   # Identify undocumented endpoints
   ```

2. **Version Testing**:
   ```bash
   # Test old API versions
   curl https://api.example.com/v1/users
   curl https://api.example.com/v2/users
   ```

3. **Environment Discovery**:
   ```bash
   # Check for exposed environments
   curl https://api-staging.example.com/health
   curl https://api-dev.example.com/debug
   ```

**Remediation:**
```yaml
# API Gateway configuration (Kong example)
plugins:
  - name: request-termination
    config:
      status_code: 410
      message: "API version deprecated"
    route: api-v1-routes

# Automated API discovery
# Use tools like:
# - OWASP ZAP API scanner
# - Postman collection generator
# - Swagger Codegen

# Regular audits
# Monthly: Compare deployed endpoints with documentation
# Quarterly: Review and deprecate old API versions
```

#### API10: Unsafe Consumption of APIs

> **Risk**: Trusting third-party API responses leads to injection attacks

**Real-World Impact**:
- **2020**: Multiple XXE attacks via external API responses
- **2021**: Deserialization attacks from webhook payloads

**Attack Scenarios:**

1. **XXE via External API**
   ```xml
   <!-- Malicious response from third-party API -->
   <?xml version="1.0"?>
   <!DOCTYPE foo [
     <!ENTITY xxe SYSTEM "file:///etc/passwd">
   ]>
   <data>&xxe;</data>
   ```

2. **Deserialization Attack**
   ```python
   # Attacker controls serialized data
   import pickle
   malicious = b'...crafted pickle payload...'
   data = pickle.loads(malicious)  # RCE!
   ```

3. **Webhook Replay**
   ```http
   # Attacker captures webhook and replays it
   POST /api/webhooks/payment
   X-Webhook-Signature: valid_signature
   {"event": "payment.success", "amount": 1000}
   
   # Replay same request to double credits
   ```

4. **JSON Injection**
   ```json
   // Malicious JSON from external API
   {
     "username": "admin",
     "bio": "<script>alert('XSS')</script>"
   }
   ```

**Testing Approach:**

1. **XXE Testing**:
   ```bash
   # If API accepts XML from third parties
   # Send malicious XML to test for XXE
   ```

2. **Deserialization Testing**:
   ```bash
   # Check for unsafe deserialization
   # Look for pickle, ObjectInputStream, unserialize
   ```

3. **Webhook Security**:
   ```bash
   # Test webhook replay
   # Check signature validation
   # Verify timestamp/nonce checks
   ```

**Remediation:**
```python
# XXE Prevention
import xml.etree.ElementTree as ET
from defusedxml import ElementTree as DefusedET

def parse_xml_safely(xml_string):
    # Use defusedxml to prevent XXE
    return DefusedET.fromstring(xml_string)

# Deserialization Safety
import json

def safe_deserialize(data):
    # Use JSON instead of pickle for untrusted data
    return json.loads(data)
    
    # If you must use pickle, sign the data
    import hmac
    import hashlib
    
    signature = hmac.new(
        SECRET_KEY,
        data,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid signature")
    
    return pickle.loads(data)

# Webhook Security
import hmac
import hashlib
import time

def verify_webhook(request):
    # Verify signature
    signature = request.headers.get('X-Webhook-Signature')
    expected = hmac.new(
        WEBHOOK_SECRET,
        request.body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        raise ValueError("Invalid signature")
    
    # Check timestamp (prevent replay)
    timestamp = int(request.headers.get('X-Webhook-Timestamp'))
    if abs(time.time() - timestamp) > 300:  # 5 minutes
        raise ValueError("Request too old")
    
    # Check nonce (prevent replay)
    nonce = request.headers.get('X-Webhook-Nonce')
    if nonce in used_nonces:
        raise ValueError("Nonce already used")
    used_nonces.add(nonce)
    
    return True
```

### Phase 4: Automated Security Testing

#### 4.1 API Security Scanning

**OWASP ZAP**:
```bash
# Automated API scan
zap-api-scan.py -t https://api.example.com/openapi.json -f openapi

# With authentication
zap-api-scan.py -t https://api.example.com/openapi.json \
  -f openapi \
  -config "replacer.full_list(0).description=auth" \
  -config "replacer.full_list(0).enabled=true" \
  -config "replacer.full_list(0).matchtype=REQ_HEADER" \
  -config "replacer.full_list(0).matchstr=Authorization" \
  -config "replacer.full_list(0).replacement=Bearer $TOKEN"
```

**Burp Suite**:
- Import OpenAPI spec
- Run active scan on all endpoints
- Test for BOLA, authentication bypasses

**Postman Security Tests**:
```javascript
// Test for sensitive data in response
pm.test("Response does not contain sensitive data", function () {
    pm.expect(pm.response.text()).to.not.include("password");
    pm.expect(pm.response.text()).to.not.include("secret");
});

// Test for security headers
pm.test("Security headers present", function () {
    pm.response.to.have.header("X-Content-Type-Options");
    pm.response.to.have.header("X-Frame-Options");
});
```

#### 4.2 Custom Security Tests

**BOLA Testing Script**:
```python
import requests

def test_bola(base_url, token, user_a_id, user_b_id):
    """Test for Broken Object Level Authorization"""
    
    # Get User A's token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to access User B's resources
    endpoints = [
        f"/api/users/{user_b_id}",
        f"/api/users/{user_b_id}/orders",
        f"/api/orders?user_id={user_b_id}",
    ]
    
    for endpoint in endpoints:
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        if response.status_code == 200:
            print(f"BOLA VULNERABILITY: {endpoint}")
            print(f"User A can access User B's data!")
```

**Rate Limit Testing**:
```python
import requests
import time

def test_rate_limiting(url, headers, requests_count=100):
    """Test if rate limiting is enforced"""
    
    success_count = 0
    start_time = time.time()
    
    for i in range(requests_count):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            print(f"Rate limit hit after {i} requests")
            break
    
    elapsed = time.time() - start_time
    print(f"Made {success_count} requests in {elapsed:.2f} seconds")
    
    if success_count == requests_count:
        print("WARNING: No rate limiting detected!")
```

### Phase 5: API Gateway & Infrastructure Review

#### 5.1 Kong Gateway Configuration

```yaml
# kong.yml
plugins:
  # Rate limiting
  - name: rate-limiting
    config:
      minute: 100
      hour: 1000
      policy: redis
      redis_host: redis
  
  # CORS (restrictive)
  - name: cors
    config:
      origins:
        - "https://app.example.com"
      methods:
        - GET
        - POST
        - PUT
        - DELETE
      headers:
        - Authorization
        - Content-Type
      credentials: true
      max_age: 3600
  
  # Request size limiting
  - name: request-size-limiting
    config:
      allowed_payload_size: 10  # MB
  
  # Bot detection
  - name: bot-detection
    config:
      deny:
        - "Mozilla/5.0 (compatible; Googlebot/2.1)"
  
  # IP restriction
  - name: ip-restriction
    config:
      allow:
        - "10.0.0.0/8"
        - "172.16.0.0/12"
```

#### 5.2 nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    # Request size limit
    client_max_body_size 10M;
    
    # Timeout settings
    proxy_connect_timeout 30s;
    proxy_send_timeout 30s;
    proxy_read_timeout 30s;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5.3 AWS API Gateway

```yaml
# serverless.yml or CloudFormation
Resources:
  ApiGateway:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: SecureAPI
      
  # Throttling
  ApiGatewayStage:
    Type: AWS::ApiGateway::Stage
    Properties:
      RestApiId: !Ref ApiGateway
      StageName: prod
      MethodSettings:
        - ResourcePath: /*
          HttpMethod: *
          ThrottlingBurstLimit: 100
          ThrottlingRateLimit: 50
          
  # WAF
  WebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: APIWAF
      Rules:
        - Name: RateLimit
          Priority: 1
          Statement:
            RateBasedStatement:
              Limit: 2000
              AggregateKeyType: IP
          Action:
            Block: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
```

## Output Format

```markdown
## API Security Assessment: [API Name]

### Executive Summary
- **API Type**: REST | GraphQL | gRPC | SOAP
- **Total Endpoints**: [count]
- **Authentication**: [JWT | OAuth 2.0 | API Keys | Session]
- **Risk Rating**: [Critical | High | Medium | Low]
- **Overall Security Posture**: [Brief assessment]

### API Surface Inventory

#### Authentication Mechanisms
| Mechanism | Implementation | Security Rating |
|-----------|---------------|-----------------|
| JWT | HS256, 15min expiry | ✅ Secure |
| OAuth 2.0 | PKCE enabled | ✅ Secure |

#### Endpoint Breakdown
| Category | Count | Auth Required |
|----------|-------|---------------|
| Public | 5 | No |
| Authenticated | 45 | Yes |
| Admin | 8 | Yes + Admin role |

### Risk Matrix

| OWASP API Ref | Risk | Severity | Status | Evidence |
|--------------|------|----------|--------|----------|
| API1 | BOLA | HIGH | Finding | /api/orders/{id} lacks ownership check |
| API2 | Broken Auth | MEDIUM | Finding | JWT alg=none accepted |
| API3 | BOPA | HIGH | Finding | Mass assignment on /api/users |
| API4 | Resource Consumption | LOW | Finding | No rate limiting on search |
| API5 | BFLA | MEDIUM | Finding | Admin endpoints accessible to users |
| API6 | Business Flows | N/A | N/A | Not applicable |
| API7 | SSRF | CRITICAL | Finding | Cloud metadata accessible |
| API8 | Misconfiguration | MEDIUM | Finding | Debug mode enabled |
| API9 | Inventory | LOW | Finding | Undocumented /api/internal endpoints |
| API10 | Unsafe Consumption | HIGH | Finding | Webhooks lack signature validation |

### Critical Findings

#### [CRITICAL] API7: SSRF - Cloud Metadata Exposure
- **Location**: `/api/fetch?url=` parameter
- **Impact**: AWS credentials can be extracted, leading to full cloud compromise
- **Evidence**: 
  ```
  GET /api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
  Response: 200 OK with IAM role credentials
  ```
- **Remediation**: Implement URL allowlist, block internal IPs

### High Findings
[Additional findings...]

### Positive Security Controls
- ✅ JWT tokens use strong signing (RS256)
- ✅ HTTPS enforced with TLS 1.2+
- ✅ Security headers present
- ✅ Input validation on all endpoints

### Remediation Roadmap

#### Immediate (Critical/High - 1 week)
1. Fix SSRF vulnerability (API7)
2. Implement BOLA checks on all object endpoints (API1)
3. Disable debug mode (API8)

#### Short-term (High/Medium - 1 month)
4. Implement comprehensive rate limiting (API4)
5. Add field-level authorization (API3)
6. Secure admin endpoints (API5)

#### Long-term (Medium/Low - 3 months)
7. Implement API inventory management (API9)
8. Add webhook signature validation (API10)
9. Conduct regular security testing

### Testing Artifacts
- [ ] OWASP ZAP scan results
- [ ] Burp Suite scan results
- [ ] Custom test scripts output
- [ ] API gateway configuration review

### References
- OWASP API Security Top 10 (2023)
- OWASP ASVS v5.0 - V13: API and Web Service
- OWASP Testing Guide: WSTG-APIT
```

## OWASP References

- **OWASP API Security Top 10 (2023)** — [owasp.org/API-Security](https://owasp.org/API-Security/)
- **OWASP ASVS v5.0** — V13: API and Web Service Verification
- **OWASP Testing Guide** — WSTG-APIT: API Testing
- **OWASP Cheat Sheet Series**:
  - REST Security
  - GraphQL Security
  - JWT Security
  - OAuth 2.0
  - SAML Security
- **OWASP ZAP** — API scanning capabilities
