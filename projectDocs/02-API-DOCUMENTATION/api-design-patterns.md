# API Design Patterns - Patterns thiết kế API

## 📊 Tổng quan

Tài liệu này trình bày các patterns lý thuyết về thiết kế API cho hệ thống AI Camera Counting, tập trung vào RESTful APIs, GraphQL, và real-time APIs.

## 🎯 Mục tiêu
- Đảm bảo API consistent, scalable và maintainable
- Cung cấp excellent developer experience
- Tối ưu hóa performance và resource usage
- Đảm bảo security và compliance

## 🏗️ API Architecture Patterns

### 1. API Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API ARCHITECTURE OVERVIEW                         │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Client        │  │   API Gateway   │  │   Service       │                  │
│  │   Applications  │  │                 │  │   Layer         │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Web Apps      │  │ • Authentication│  │ • REST APIs     │                  │
│  │ • Mobile Apps   │  │ • Authorization │  │ • GraphQL APIs  │                  │
│  │ • Third-party   │  │ • Rate Limiting │  │ • gRPC APIs     │                  │
│  │   Integrations  │  │ • Request       │  │ • WebSocket     │                  │
│  │ • IoT Devices   │  │   Routing       │  │   APIs          │                  │
│  │ • Analytics     │  │ • Load          │  │ • Event-Driven  │                  │
│  │   Tools         │  │   Balancing     │  │   APIs          │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Security      │  │   Monitoring    │  │   Documentation │                  │
│  │   Layer         │  │   Layer         │  │   Layer         │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • WAF           │  │ • API Metrics   │  │ • OpenAPI       │                  │
│  │ • DDoS          │  │ • Performance   │  │   Spec          │                  │
│  │   Protection    │  │   Monitoring    │  │ • Interactive   │                  │
│  │ • SSL/TLS       │  │ • Error         │  │   Docs          │                  │
│  │ • CORS          │  │   Tracking      │  │ • SDK           │                  │
│  │ • Input         │  │ • Usage         │  │   Generation    │                  │
│  │   Validation    │  │   Analytics     │  │ • Code          │                  │
│  │ • Output        │  │ • Alerting      │  │   Examples      │                  │
│  │   Sanitization  │  │ • Logging       │  │ • Testing       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API SERVICE TYPES                                 │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   REST APIs     │  │   GraphQL APIs  │  │   Real-time     │                  │
│  │                 │  │                 │  │   APIs          │                  │
│  │ • Resource-based│  │ • Single        │  │ • WebSocket     │                  │
│  │ • HTTP Methods  │  │   Endpoint      │  │   Connections   │                  │
│  │ • Stateless     │  │ • Flexible      │  │ • Server-Sent   │                  │
│  │ • Cacheable     │  │   Queries       │  │   Events        │                  │
│  │ • Uniform       │  │ • Strong        │  │ • Long Polling  │                  │
│  │   Interface     │  │   Typing        │  │ • Event         │                  │
│  │ • Layered       │  │ • Introspection │  │   Streaming     │                  │
│  │   System        │  │ • Real-time     │  │ • Message       │                  │
│  │ • Self-         │  │   Subscriptions │  │   Queues        │                  │
│  │   Describing    │  │ • Schema        │  │ • Pub/Sub       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. API Versioning Strategy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API VERSIONING STRATEGIES                         │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   URL           │  │   Header        │  │   Query         │                  │
│  │   Versioning    │  │   Versioning    │  │   Parameter     │                  │
│  │                 │  │                 │  │   Versioning    │                  │
│  │ /api/v1/users   │  │ Accept:         │  │ /api/users?     │                  │
│  │ /api/v2/users   │  │ application/    │  │ version=1       │                  │
│  │ /api/v3/users   │  │ json;version=1  │  │ /api/users?     │                  │
│  │                 │  │                 │  │ version=2       │                  │
│  │ • Clear         │  │ • Clean URLs    │  │ • Simple        │                  │
│  │   Separation    │  │ • Standard      │  │   Implementation│                  │
│  │ • Easy          │  │   HTTP          │  │ • Easy Testing  │                  │
│  │   Caching       │  │ • Flexible      │  │ • URL           │                  │
│  │ • Clear         │  │   Versioning    │  │   Pollution     │                  │
│  │   Migration     │  │ • Complex       │  │ • Cache         │                  │
│  │ • URL           │  │   Headers       │  │   Issues        │                  │
│  │   Pollution     │  │ • Debugging     │  │ • Version       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Content       │  │   Backward      │  │   Deprecation   │                  │
│  │   Negotiation   │  │   Compatibility │  │   Strategy      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ Accept:         │  │ • Maintain      │  │ • Deprecation   │                  │
│  │ application/    │  │   Old Versions  │  │   Timeline      │                  │
│  │ json;version=1  │  │ • Additive      │  │ • Migration     │                  │
│  │ Accept:         │  │   Changes Only  │  │   Guide         │                  │
│  │ application/    │  │ • Version       │  │ • Sunset        │                  │
│  │ json;version=2  │  │   Detection     │  │   Notifications │                  │
│  │                 │  │ • Graceful      │  │ • Breaking      │                  │
│  │ • Standard      │  │   Degradation   │  │   Changes       │                  │
│  │   HTTP          │  │ • Documentation │  │ • Version       │                  │
│  │ • Flexible      │  │ • Testing       │  │   Lifecycle     │                  │
│  │ • Complex       │  │ • Monitoring    │  │ • Support       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Security Patterns Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API SECURITY PATTERNS                             │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Authentication│  │   Authorization │  │   Rate          │                  │
│  │   Patterns      │  │   Patterns      │  │   Limiting      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • JWT Tokens    │  │ • Role-based    │  │ • Token Bucket  │                  │
│  │ • OAuth 2.0     │  │   Access        │  │ • Leaky Bucket  │                  │
│  │ • API Keys      │  │ • Permission-   │  │ • Fixed Window  │                  │
│  │ • SAML          │  │   based Access  │  │ • Sliding       │                  │
│  │ • Multi-factor  │  │ • Attribute-    │  │   Window        │                  │
│  │   Authentication│  │   based Access  │  │ • Rate Limit    │                  │
│  │ • Biometric     │  │ • Policy-based  │  │   Headers       │                  │
│  │   Authentication│  │   Access        │  │ • IP-based      │                  │
│  │ • Certificate-  │  │ • Dynamic       │  │   Limits        │                  │
│  │   based Auth    │  │   Authorization │  │ • User-based    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Input         │  │   Data          │  │   Transport     │                  │
│  │   Validation    │  │   Protection    │  │   Security      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Schema        │  │ • Encryption    │  │ • HTTPS/TLS     │                  │
│  │   Validation    │  │   at Rest       │  │ • Certificate   │                  │
│  │ • Type          │  │ • Encryption    │  │   Validation    │                  │
│  │   Validation    │  │   in Transit    │  │ • Perfect       │                  │
│  │ • Length        │  │ • Data          │  │   Forward       │                  │
│  │   Validation    │  │   Masking       │  │   Secrecy       │                  │
│  │ • Format        │  │ • Tokenization  │  │ • HSTS          │                  │
│  │   Validation    │  │ • Access        │  │ • CORS          │                  │
│  │ • Business      │  │   Logging       │  │   Configuration │                  │
│  │   Rule          │  │ • Audit Trail   │  │ • CSP           │                  │
│  │   Validation    │  │ • Compliance    │  │   Headers       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Error Handling Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ERROR HANDLING FLOW                               │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   API       │    │   Error     │    │   Error     │    │   Client    │      │
│  │   Request   │    │   Detection │    │   Processing│    │   Response  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Client Request │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 2. Validation     │                   │                   │          │
│         │    Error          │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 3. Authentication │                   │                   │          │
│         │    Error          │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 4. Authorization  │                   │                   │          │
│         │    Error          │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 5. Business Logic │                   │                   │          │
│         │    Error          │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 6. System Error   │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Error         │  │   Error         │  │   Error         │                  │
│  │   Categories    │  │   Response      │  │   Recovery      │                  │
│  │                 │  │   Format        │  │   Strategies    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • 4xx Client    │  │ • Error Code    │  │ • Retry Logic   │                  │
│  │   Errors        │  │ • Error Message │  │ • Circuit       │                  │
│  │ • 5xx Server    │  │ • Error Details │  │   Breaker       │                  │
│  │   Errors        │  │ • Timestamp     │  │ • Fallback      │                  │
│  │ • Validation    │  │ • Request ID    │  │   Mechanisms    │                  │
│  │   Errors        │  │ • Help URL      │  │ • Graceful      │                  │
│  │ • Rate Limit    │  │ • Documentation │  │   Degradation   │                  │
│  │   Errors        │  │ • Support       │  │ • Error         │                  │
│  │ • Network       │  │   Contact       │  │   Monitoring    │                  │
│  │   Errors        │  │ • Localization  │  │ • Alerting      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5. Rate Limiting Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              RATE LIMITING ARCHITECTURE                        │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Rate Limit    │  │   Rate Limit    │  │   Rate Limit    │                  │
│  │   Strategies    │  │   Storage       │  │   Enforcement   │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Token Bucket  │  │ • Redis         │  │ • API Gateway   │                  │
│  │ • Leaky Bucket  │  │ • In-Memory     │  │ • Middleware    │                  │
│  │ • Fixed Window  │  │ • Database      │  │ • Proxy         │                  │
│  │ • Sliding       │  │ • Distributed   │  │ • Load          │                  │
│  │   Window        │  │   Cache         │  │   Balancer      │                  │
│  │ • Adaptive      │  │ • Cluster       │  │ • Application   │                  │
│  │   Rate Limiting │  │   Mode          │  │   Level         │                  │
│  │ • Dynamic       │  │ • Persistence   │  │ • Service       │                  │
│  │   Rate Limiting │  │ • Backup        │  │   Level         │                  │
│  │ • User-based    │  │ • Recovery      │  │ • Endpoint      │                  │
│  │   Limits        │  │ • Monitoring    │  │   Level         │                  │
│  │ • IP-based      │  │ • Analytics     │  │ • Method        │                  │
│  │   Limits        │  │ • Reporting     │  │   Level         │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Rate Limit    │  │   Rate Limit    │  │   Rate Limit    │                  │
│  │   Headers       │  │   Monitoring    │  │   Configuration │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • X-RateLimit-  │  │ • Request       │  │ • Per-User      │                  │
│  │   Limit         │  │   Count         │  │   Limits        │                  │
│  │ • X-RateLimit-  │  │ • Response      │  │ • Per-IP        │                  │
│  │   Remaining     │  │   Time          │  │   Limits        │                  │
│  │ • X-RateLimit-  │  │ • Error Rate    │  │ • Per-Endpoint  │                  │
│  │   Reset         │  │ • Success Rate  │  │   Limits        │                  │
│  │ • Retry-After   │  │ • Peak Usage    │  │ • Burst Limits  │                  │
│  │ • X-RateLimit-  │  │ • Average       │  │ • Daily Limits  │                  │
│  │   Policy        │  │   Usage         │  │ • Monthly       │                  │
│  │ • X-RateLimit-  │  │ • Trend         │  │   Limits        │                  │
│  │   Retry-After   │  │   Analysis      │  │ • Dynamic       │                  │
│  │ • X-RateLimit-  │  │ • Alerting      │  │   Adjustment    │                  │
│  │   Retry-After   │  │ • Reporting     │  │ • A/B Testing   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 6. API Documentation Structure

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API DOCUMENTATION STRUCTURE                       │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   OpenAPI       │  │   Interactive   │  │   Code          │                  │
│  │   Specification │  │   Documentation │  │   Examples      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • API Info      │  │ • Swagger UI    │  │ • cURL          │                  │
│  │ • Servers       │  │ • ReDoc         │  │   Examples      │                  │
│  │ • Paths         │  │ • Postman       │  │ • JavaScript    │                  │
│  │ • Components    │  │   Collection    │  │   Examples      │                  │
│  │ • Security      │  │ • Insomnia      │  │ • Python        │                  │
│  │ • Tags          │  │   Collection    │  │   Examples      │                  │
│  │ • External      │  │ • Try-it-out    │  │ • Java          │                  │
│  │   Docs          │  │   Feature       │  │   Examples      │                  │
│  │ • Examples      │  │ • Request       │  │ • C#            │                  │
│  │ • Callbacks     │  │   Builder       │  │   Examples      │                  │
│  │ • Webhooks      │  │ • Response      │  │ • PHP           │                  │
│  │ • Links         │  │   Viewer        │  │   Examples      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   SDK           │  │   Testing       │  │   Versioning    │                  │
│  │   Generation    │  │   Documentation │  │   Documentation │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • JavaScript    │  │ • Test Cases    │  │ • Version       │                  │
│  │   SDK           │  │ • Test Data     │  │   History       │                  │
│  │ • Python SDK    │  │ • Test          │  │ • Migration     │                  │
│  │ • Java SDK      │  │   Environment   │  │   Guide         │                  │
│  │ • C# SDK        │  │ • Mock          │  │ • Breaking      │                  │
│  │ • PHP SDK       │  │   Services      │  │   Changes       │                  │
│  │ • Go SDK        │  │ • Integration   │  │ • Deprecation   │                  │
│  │ • Ruby SDK      │  │   Tests         │  │   Timeline      │                  │
│  │ • Swift SDK     │  │ • Performance   │  │ • Sunset        │                  │
│  │ • Kotlin SDK    │  │   Tests         │  │   Notifications │                  │
│  │ • TypeScript    │  │ • Load Tests    │  │ • Support       │                  │
│  │   SDK           │  │ • Security      │  │   Policy        │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ API Architecture Patterns

- **RESTful APIs**: Resource-based design với standard HTTP methods
- **GraphQL APIs**: Flexible query language cho complex data requirements
- **gRPC APIs**: High-performance RPC cho microservices communication
- **WebSocket APIs**: Real-time bidirectional communication
- **Event-Driven APIs**: Asynchronous communication via events

## 🔄 RESTful Design Patterns
- **Resource Naming**: Consistent và intuitive resource naming
- **HTTP Methods**: Proper use of GET, POST, PUT, DELETE, PATCH
- **Status Codes**: Appropriate HTTP status codes cho responses
- **Pagination**: Efficient pagination cho large datasets
- **Filtering & Sorting**: Flexible query parameters cho data retrieval

## 📊 API Versioning Patterns
- **URL Versioning**: Version trong URL path (/api/v1/resource)
- **Header Versioning**: Version trong HTTP headers
- **Query Parameter Versioning**: Version trong query parameters
- **Content Negotiation**: Version trong Accept header
- **Backward Compatibility**: Maintain compatibility across versions

## 🔒 Security Patterns
- **Authentication**: JWT, OAuth 2.0, API keys
- **Authorization**: Role-based access control (RBAC)
- **Rate Limiting**: Prevent abuse và ensure fair usage
- **Input Validation**: Validate và sanitize all inputs
- **CORS**: Cross-origin resource sharing configuration

## 📈 Performance Patterns
- **Caching**: HTTP caching, application caching
- **Compression**: Gzip, Brotli compression
- **Connection Pooling**: Efficient database connections
- **Async Processing**: Non-blocking operations cho long-running tasks
- **Load Balancing**: Distribute load across multiple instances

## 🔍 Error Handling Patterns
- **Standard Error Format**: Consistent error response structure
- **Error Codes**: Meaningful error codes và messages
- **Validation Errors**: Detailed validation error responses
- **Rate Limit Errors**: Clear rate limit exceeded responses
- **Retry Logic**: Implement retry mechanisms cho transient failures

## 📱 Real-time API Patterns
- **WebSocket Connections**: Persistent connections cho real-time data
- **Server-Sent Events**: One-way real-time updates
- **Long Polling**: Fallback cho real-time updates
- **Message Queues**: Reliable message delivery
- **Event Streaming**: Stream events cho real-time processing

## 🚀 Best Practices
- Follow RESTful principles cho resource-based APIs
- Implement comprehensive API documentation
- Sử dụng OpenAPI/Swagger cho API specification
- Thiết lập proper monitoring và logging
- Regular API performance và security reviews

---

**Tài liệu này là nền tảng lý thuyết cho việc thiết kế và triển khai APIs trong dự án AI Camera Counting.** 