# Security Architecture - Kiến trúc bảo mật

## 📊 Tổng quan

Tài liệu này mô tả kiến trúc bảo mật toàn diện cho hệ thống AI Camera Counting, bao gồm các lớp bảo mật, protocols, và best practices để đảm bảo tính bảo mật end-to-end.

## 🎯 Mục tiêu bảo mật

### Mục tiêu chính
- **Confidentiality**: Bảo vệ tính bí mật của dữ liệu
- **Integrity**: Đảm bảo tính toàn vẹn dữ liệu
- **Availability**: Đảm bảo tính khả dụng của hệ thống
- **Authentication**: Xác thực người dùng và hệ thống
- **Authorization**: Phân quyền truy cập
- **Audit**: Ghi log và theo dõi hoạt động

### Yêu cầu bảo mật
- **Compliance**: Tuân thủ GDPR, ISO 27001, SOC 2
- **Encryption**: End-to-end encryption cho dữ liệu nhạy cảm
- **Access Control**: Role-based access control (RBAC)
- **Monitoring**: Real-time security monitoring
- **Incident Response**: Phản ứng nhanh với security incidents

## 🏗️ Security Architecture Overview

### Multi-Layer Security Architecture

#### Security Architecture Overview Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY ARCHITECTURE OVERVIEW                      │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECURITY LAYERS                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Network       │  │   Application   │  │   Data          │              │ │
│  │  │   Security      │  │   Security      │  │   Security      │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Firewall      │  │ • Authentication│  │ • Encryption    │              │ │
│  │  │ • DDoS Protect  │  │ • Authorization │  │ • Access Control│              │ │
│  │  │ • VPN           │  │ • Input Valid   │  │ • Audit Logging │              │ │
│  │  │ • IDS/IPS       │  │ • Session Mgmt  │  │ • Backup        │              │ │
│  │  │ • Load Balancer │  │ • Rate Limiting │  │ • Compliance    │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE SECURITY                        │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Physical      │  │   System        │  │   Monitoring    │              │ │
│  │  │   Security      │  │   Security      │  │   & Alerting    │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Access Control│  │ • OS Hardening  │  │ • SIEM          │              │ │
│  │  │ • Surveillance  │  │ • Patch Mgmt    │  │ • Threat Intel  │              │ │
│  │  │ • Environmental │  │ • Vulnerability │  │ • Incident Resp │              │ │
│  │  │ • Power Backup  │  │   Scanning      │  │ • Forensics     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────┘
```

#### Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUTHENTICATION FLOW                                │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │   Client    │    │   API       │    │   Auth      │    │   Database  │       │
│  │   (Frontend)│    │   Gateway   │    │   Service   │    │             │       │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘       │
│         │                   │                   │                   │           │
│         │ 1. Login Request  │                   │                   │           │
│         │ (username/password)│                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Route to Auth  │                   │          │
│         │                   │ Service           │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Validate User  │          │
│         │                   │                   │ (bcrypt hash)     │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. User Data      │          │
│         │                   │                   │ (roles/permissions)│         │
│         │                   │                   │◄──────────────────│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Generate JWT   │          │
│         │                   │                   │ (access + refresh)│          │
│         │                   │                   │                   │          │
│         │                   │ 6. JWT Response   │                   │          │
│         │                   │◄──────────────────│                   │          │
│         │                   │                   │                   │          │
│         │ 7. JWT Response   │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 8. Store Tokens   │                   │                   │          │
│         │ (localStorage)    │                   │                   │          │
│         │                   │                   │                   │          │
│         │ 9. API Requests   │                   │                   │          │
│         │ (with JWT)        │                   │                   │          │
│         │                   │                   │                   │          │
│         │ 10. Token Refresh │                   │                   │          │
│         │ (when expired)    │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Authorization Matrix Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUTHORIZATION MATRIX                               │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ROLE-BASED ACCESS CONTROL (RBAC)               │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Roles         │  │   Permissions   │  │   Resources     │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Super Admin   │  │ • camera:read   │  │ • /cameras/*    │              │ │
│  │  │ • Admin         │  │ • camera:write  │  │ • /users/*      │              │ │
│  │  │ • Operator      │  │ • camera:delete │  │ • /analytics/*  │              │ │
│  │  │ • Viewer        │  │ • user:read     │  │ • /reports/*    │              │ │
│  │  │ • Guest         │  │ • user:write    │  │ • /settings/*   │              │ │
│  │  │                 │  │ • analytics:read│  │ • /logs/*       │              │ │
│  │  │                 │  │ • analytics:write│ │ • /admin/*      │              │ │
│  │  │                 │  │ • system:admin  │  │ • /api/*        │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PERMISSION MATRIX                              │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │   Resource  │ │ Super Admin │ │   Admin     │ │  Operator   │ │ Viewer  │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ /cameras/*  │ │    CRUD     │ │    CRUD     │ │    R,U      │ │    R    │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ /users/*    │ │    CRUD     │ │    R,U      │ │     -       │ │    -    │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ /analytics/*│ │    CRUD     │ │    CRUD     │ │    R,U      │ │    R    │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ /admin/*    │ │    CRUD     │ │    R,U      │ │     -       │ │    -    │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ /logs/*     │ │    CRUD     │ │    R,U      │ │     -       │ │    -    │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │                                                                             │ │
│  │  Legend: C=Create, R=Read, U=Update, D=Delete, -=No Access                 │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Data Protection Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA PROTECTION ARCHITECTURE                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA CLASSIFICATION                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Public        │  │   Internal      │  │   Confidential  │              │ │
│  │  │   Data          │  │   Data          │  │   Data          │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • System Status │  │ • Camera Config │  │ • User Credentials│            │ │
│  │  │ • Public Analytics│ │ • User Preferences│ │ • Camera Streams│            │ │
│  │  │ • API Docs      │  │ • Internal Reports│ │ • Admin Logs    │            │ │
│  │  │ • Error Messages│  │ • Performance Data│ │ • Security Logs │            │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ Encryption: No  │  │ Encryption: Yes │  │ Encryption: Yes │              │ │
│  │  │ Retention: 1Y   │  │ Retention: 3Y   │  │ Retention: 7Y   │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ENCRYPTION STRATEGY                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   At Rest       │  │   In Transit    │  │   In Use        │              │ │
│  │  │   Encryption    │  │   Encryption    │  │   Encryption    │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Database:     │  │ • API: TLS 1.3  │  │ • Memory:       │              │ │
│  │  │   AES-256-GCM   │  │ • Database:     │  │   Secure Memory │              │ │
│  │  │ • Files:        │  │   TLS 1.3       │  │ • Processing:   │              │ │
│  │  │   AES-256-GCM   │  │ • Camera: SRTP  │  │   Encrypted     │              │ │
│  │  │ • Backups:      │  │ • WebSocket:    │  │   Containers    │              │ │
│  │  │   AES-256-GCM   │  │   WSS (TLS)     │  │ • Keys: HSM     │              │ │
│  │  │ • Keys: AWS KMS │  │ • VPN: IPSec    │  │ • Sessions:     │              │ │
│  │  │ • Rotation: 90D │  │ • Rotation:     │  │   Secure Storage│              │ │
│  │  └─────────────────┘  │   Auto          │  └─────────────────┘              │ │
│  │                       └─────────────────┘                                   │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ACCESS CONTROL                                  │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Authentication│  │   Authorization │  │   Audit         │              │ │
│  │  │                 │  │                 │  │   Logging       │              │ │
│  │  │ • JWT Tokens    │  │ • RBAC          │  │ • Access Logs   │              │ │
│  │  │ • MFA (TOTP)    │  │ • ABAC          │  │ • Change Logs   │              │ │
│  │  │ • Session Mgmt  │  │ • Resource-based│  │ • Security Logs │              │ │
│  │  │ • Password      │  │ • Time-based    │  │ • Compliance    │              │ │
│  │  │   Policies      │  │ • Location-based│  │   Reports       │              │ │
│  │  │ • Account Lock  │  │ • IP Whitelist  │  │ • Alerting      │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Network Security Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              NETWORK SECURITY ARCHITECTURE                       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              NETWORK SEGMENTATION                           │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   DMZ           │  │   Application   │  │   Database      │              │ │
│  │  │   (Public)      │  │   (Private)     │  │   (Private)     │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Load Balancer │  │ • API Servers   │  │ • PostgreSQL    │              │ │
│  │  │ • Web Servers   │  │ • WebSocket     │  │ • Redis         │              │ │
│  │  │ • CDN           │  │ • Worker Pool   │  │ • Message Queue │              │ │
│  │  │ • WAF           │  │ • Auth Service  │  │ • Backup Storage│              │ │
│  │  │ • SSL/TLS       │  │ • Monitoring    │  │ • Log Storage   │              │ │
│  │  │ • DDoS Protect  │  │ • Logging       │  │ • Encryption    │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  │         │                       │                       │                   │ │
│  │         │ Firewall Rules        │ Firewall Rules        │ Firewall Rules   │ │
│  │         │ (Port 80, 443)        │ (Internal Only)       │ (DB Only)        │ │
│  │         └───────────────────────┴───────────────────────┴───────────────────┘ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECURITY COMPONENTS                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Firewall      │  │   IDS/IPS       │  │   VPN           │              │ │
│  │  │   (Network)     │  │   (Intrusion)   │  │   (Remote)      │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Stateful      │  │ • Signature     │  │ • IPSec         │              │ │
│  │  │   Inspection    │  │   Detection     │  │ • SSL/TLS       │              │ │
│  │  │ • Packet Filter │  │ • Anomaly       │  │ • Multi-factor  │              │ │
│  │  │ • NAT/PAT       │  │   Detection     │  │ • Split Tunneling│             │ │
│  │  │ • Rate Limiting │  │ • Real-time     │  │ • Kill Switch   │              │ │
│  │  │ • Geo-blocking  │  │   Blocking      │  │ • Audit Logging │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   WAF           │  │   DDoS          │  │   Monitoring    │              │ │
│  │  │   (Web)         │  │   Protection    │  │   (Network)     │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • SQL Injection │  │ • Rate Limiting │  │ • Traffic       │              │ │
│  │  │ • XSS Protection│  │ • IP Reputation │  │   Analysis      │              │ │
│  │  │ • CSRF Protection│ │ • Behavioral    │  │ • Anomaly       │              │ │
│  │  │ • Bot Detection │  │   Analysis      │  │   Detection     │              │ │
│  │  │ • API Security  │  │ • Scrubbing     │  │ • Alerting      │              │ │
│  │  │ • OWASP Top 10  │  │ • Blacklisting  │  │ • Reporting     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Incident Response Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INCIDENT RESPONSE FLOW                             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INCIDENT LIFECYCLE                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Detection │    │   Analysis  │    │   Response  │    │   Recovery  │  │ │
│  │  │   Phase     │    │   Phase     │    │   Phase     │    │   Phase     │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. SIEM Alert     │                   │                   │      │ │
│  │         │ 2. Manual Report  │                   │                   │      │ │
│  │         │ 3. User Report    │                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 4. Triage         │                   │      │ │
│  │         │                   │ 5. Classification │                   │      │ │
│  │         │                   │ 6. Impact Assess  │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 7. Containment   │      │ │
│  │         │                   │                   │ 8. Eradication   │      │ │
│  │         │                   │                   │ 9. Communication │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │                   │ 10. Restore│ │
│  │         │                   │                   │                   │ 11. Monitor│ │
│  │         │                   │                   │                   │ 12. Lessons│ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ESCALATION MATRIX                              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Severity      │  │   Response      │  │   Escalation    │              │ │
│  │  │   Level         │  │   Time          │  │   Path          │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Critical      │  │ • < 15 minutes │  │ • Immediate     │              │ │
│  │  │   (P0)          │  │                 │  │ • All channels  │              │ │
│  │  │                 │  │                 │  │ • 24/7 support  │              │ │
│  │  │ • High (P1)     │  │ • < 1 hour      │  │ • Within 1 hour │              │ │
│  │  │                 │  │                 │  │ • Phone + Email │              │ │
│  │  │ • Medium (P2)   │  │ • < 4 hours     │  │ • Within 4 hours│              │ │
│  │  │                 │  │                 │  │ • Email + Slack │              │ │
│  │  │ • Low (P3)      │  │ • < 24 hours    │  │ • Within 24 hours│             │ │
│  │  │                 │  │                 │  │ • Email only    │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              COMMUNICATION PLAN                              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Internal      │  │   External      │  │   Regulatory    │              │ │
│  │  │   Team          │  │   Customers     │  │   Bodies        │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Slack         │  │ • Email         │  │ • Formal Report │              │ │
│  │  │ • Phone         │  │ • Status Page   │  │ • Compliance    │              │ │
│  │  │ • SMS           │  │ • Social Media  │  │   Documentation │              │ │
│  │  │ • Email         │  │ • Press Release │  │ • Legal Review  │              │ │
│  │  │ • PagerDuty     │  │ • Customer      │  │ • Timeline      │              │ │
│  │  │ • Escalation    │  │   Support       │  │   Requirements  │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY LAYERS                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Network       │  │   Application   │  │   Data          │                  │
│  │   Security      │  │   Security      │  │   Security      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Firewall      │  │ • Authentication│  │ • Encryption    │                  │
│  │ • DDoS Protect  │  │ • Authorization │  │ • Access Control│                  │
│  │ • VPN           │  │ • Input Valid   │  │ • Audit Logging │                  │
│  │ • IDS/IPS       │  │ • Session Mgmt  │  │ • Backup        │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INFRASTRUCTURE SECURITY                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Physical      │  │   System        │  │   Monitoring    │                  │
│  │   Security      │  │   Security      │  │   & Alerting    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Access Control│  │ • OS Hardening  │  │ • SIEM          │                  │
│  │ • Surveillance  │  │ • Patch Mgmt    │  │ • Threat Intel  │                  │
│  │ • Environmental │  │ • Vulnerability │  │ • Incident Resp │                  │
│  │ • Power Backup  │  │   Scanning      │  │ • Forensics     │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔐 Authentication & Authorization

### 1. Authentication Strategy

#### JWT Token Architecture
```javascript
// JWT Token Structure
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "iss": "ai-camera-system",
    "aud": "camera-api",
    "exp": 1642233600,
    "iat": 1642147200,
    "roles": ["admin", "operator"],
    "permissions": ["camera:read", "camera:write"],
    "org_id": "org_123"
  },
  "signature": "RS256_signature"
}
```

#### Multi-Factor Authentication (MFA)
```yaml
# MFA Configuration
mfa:
  enabled: true
  methods:
    - totp: true      # Time-based One-Time Password
    - sms: false      # SMS-based verification
    - email: true     # Email verification
    - hardware_key: false  # Hardware security keys
  
  policies:
    admin_required: true
    session_timeout: 3600  # 1 hour
    max_attempts: 3
    lockout_duration: 900  # 15 minutes
```

### 2. Authorization Strategy

#### Role-Based Access Control (RBAC)
```yaml
# RBAC Configuration
roles:
  super_admin:
    permissions:
      - "*:*"  # All permissions
    description: "Full system access"
  
  admin:
    permissions:
      - "camera:*"
      - "user:read"
      - "analytics:*"
      - "system:read"
    description: "Administrative access"
  
  operator:
    permissions:
      - "camera:read"
      - "camera:update"
      - "analytics:read"
    description: "Camera operation access"
  
  viewer:
    permissions:
      - "camera:read"
      - "analytics:read"
    description: "Read-only access"
```

#### Permission Matrix
```yaml
# Permission Matrix
permissions:
  camera:
    create: ["admin", "super_admin"]
    read: ["admin", "operator", "viewer", "super_admin"]
    update: ["admin", "operator", "super_admin"]
    delete: ["admin", "super_admin"]
    stream: ["admin", "operator", "super_admin"]
  
  user:
    create: ["admin", "super_admin"]
    read: ["admin", "super_admin"]
    update: ["admin", "super_admin"]
    delete: ["admin", "super_admin"]
  
  analytics:
    read: ["admin", "operator", "viewer", "super_admin"]
    export: ["admin", "super_admin"]
    configure: ["admin", "super_admin"]
```

## 🔒 Data Security

### 1. Data Classification

#### Data Sensitivity Levels
```yaml
# Data Classification
data_classification:
  public:
    description: "Public information"
    examples: ["system status", "public analytics"]
    encryption: false
    retention: "1 year"
  
  internal:
    description: "Internal business data"
    examples: ["camera configurations", "user preferences"]
    encryption: true
    retention: "3 years"
  
  confidential:
    description: "Sensitive business data"
    examples: ["user credentials", "camera streams"]
    encryption: true
    retention: "7 years"
  
  restricted:
    description: "Highly sensitive data"
    examples: ["admin credentials", "security logs"]
    encryption: true
    retention: "10 years"
```

### 2. Encryption Strategy

#### Encryption at Rest
```yaml
# Encryption at Rest
encryption_at_rest:
  database:
    algorithm: "AES-256-GCM"
    key_management: "AWS KMS"
    key_rotation: "90 days"
  
  file_storage:
    algorithm: "AES-256-GCM"
    key_management: "AWS KMS"
    key_rotation: "90 days"
  
  backup:
    algorithm: "AES-256-GCM"
    key_management: "AWS KMS"
    key_rotation: "90 days"
```

#### Encryption in Transit
```yaml
# Encryption in Transit
encryption_in_transit:
  api_communication:
    protocol: "TLS 1.3"
    cipher_suites: ["TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"]
    certificate_management: "Let's Encrypt"
  
  database_connection:
    protocol: "TLS 1.3"
    cipher_suites: ["TLS_AES_256_GCM_SHA384"]
    certificate_validation: true
  
  camera_streams:
    protocol: "SRTP"
    encryption: "AES-128-GCM"
    key_management: "DTLS"
```

## 🛡️ Network Security

### 1. Network Segmentation

#### Network Architecture
```yaml
# Network Segmentation
network_segments:
  dmz:
    description: "Demilitarized Zone"
    services: ["load_balancer", "web_servers"]
    access: ["internet", "internal"]
    security: ["firewall", "waf"]
  
  application:
    description: "Application Layer"
    services: ["api_servers", "websocket_servers"]
    access: ["dmz", "database"]
    security: ["firewall", "ids"]
  
  database:
    description: "Database Layer"
    services: ["postgresql", "redis"]
    access: ["application"]
    security: ["firewall", "encryption"]
  
  camera_network:
    description: "Camera Network"
    services: ["camera_streams", "worker_pool"]
    access: ["application"]
    security: ["vpn", "firewall"]
```

### 2. Firewall Configuration

#### Firewall Rules
```yaml
# Firewall Configuration
firewall_rules:
  inbound:
    - port: 443
      protocol: "HTTPS"
      source: "0.0.0.0/0"
      action: "ALLOW"
      description: "HTTPS access"
    
    - port: 80
      protocol: "HTTP"
      source: "0.0.0.0/0"
      action: "REDIRECT_TO_HTTPS"
      description: "HTTP redirect"
    
    - port: 22
      protocol: "SSH"
      source: "admin_ips"
      action: "ALLOW"
      description: "SSH access"
  
  outbound:
    - port: 443
      protocol: "HTTPS"
      destination: "0.0.0.0/0"
      action: "ALLOW"
      description: "HTTPS outbound"
    
    - port: 53
      protocol: "DNS"
      destination: "dns_servers"
      action: "ALLOW"
      description: "DNS resolution"
```

## 🔍 Security Monitoring

### 1. Security Information and Event Management (SIEM)

#### SIEM Configuration
```yaml
# SIEM Configuration
siem:
  platform: "ELK Stack"
  components:
    - elasticsearch: "log_storage"
    - logstash: "log_processing"
    - kibana: "log_visualization"
    - beats: "log_collection"
  
  data_sources:
    - application_logs
    - system_logs
    - network_logs
    - security_logs
    - database_logs
  
  alerting:
    - failed_login_attempts
    - suspicious_network_activity
    - unauthorized_access_attempts
    - data_exfiltration
    - system_anomalies
```

### 2. Threat Detection

#### Threat Detection Rules
```yaml
# Threat Detection
threat_detection:
  brute_force:
    threshold: 5
    time_window: "5 minutes"
    action: "block_ip"
  
  sql_injection:
    patterns: ["sql_injection_patterns"]
    action: "block_request"
  
  xss_attack:
    patterns: ["xss_patterns"]
    action: "block_request"
  
  data_exfiltration:
    threshold: "100MB"
    time_window: "1 hour"
    action: "alert_admin"
  
  unauthorized_access:
    patterns: ["unauthorized_patterns"]
    action: "block_user"
```

## 🚨 Incident Response

### 1. Incident Response Plan

#### Response Procedures
```yaml
# Incident Response
incident_response:
  phases:
    preparation:
      - incident_response_team
      - communication_plan
      - escalation_procedures
    
    identification:
      - threat_detection
      - incident_classification
      - impact_assessment
    
    containment:
      - isolate_affected_systems
      - prevent_further_damage
      - preserve_evidence
    
    eradication:
      - remove_threat
      - patch_vulnerabilities
      - restore_systems
    
    recovery:
      - system_restoration
      - monitoring
      - validation
    
    lessons_learned:
      - incident_documentation
      - process_improvement
      - training_updates
```

### 2. Communication Plan

#### Communication Matrix
```yaml
# Communication Plan
communication_plan:
  stakeholders:
    - technical_team: "immediate"
    - management: "within_1_hour"
    - customers: "within_4_hours"
    - regulators: "within_24_hours"
  
  channels:
    - slack: "technical_team"
    - email: "management"
    - phone: "critical_incidents"
    - public_announcement: "customer_impact"
```

## 📋 Security Compliance

### 1. Compliance Frameworks

#### Compliance Requirements
```yaml
# Compliance Frameworks
compliance:
  gdpr:
    data_protection: true
    user_consent: true
    data_portability: true
    right_to_be_forgotten: true
  
  iso_27001:
    information_security: true
    risk_management: true
    security_controls: true
  
  soc_2:
    security: true
    availability: true
    processing_integrity: true
    confidentiality: true
    privacy: true
```

### 2. Security Controls

#### Security Control Matrix
```yaml
# Security Controls
security_controls:
  access_control:
    - user_authentication
    - role_based_access
    - session_management
    - privileged_access_management
  
  data_protection:
    - encryption_at_rest
    - encryption_in_transit
    - data_classification
    - data_retention
  
  network_security:
    - firewall_configuration
    - network_segmentation
    - vpn_access
    - ddos_protection
  
  monitoring:
    - security_monitoring
    - log_management
    - incident_detection
    - threat_intelligence
```

## 🧪 Security Testing

### 1. Security Testing Strategy

#### Testing Types
```yaml
# Security Testing
security_testing:
  static_analysis:
    - code_review
    - static_code_analysis
    - dependency_scanning
  
  dynamic_analysis:
    - penetration_testing
    - vulnerability_scanning
    - security_scanning
  
  configuration_testing:
    - security_configuration_review
    - infrastructure_security_testing
    - compliance_testing
```

### 2. Penetration Testing

#### Penetration Testing Plan
```yaml
# Penetration Testing
penetration_testing:
  scope:
    - web_application
    - api_endpoints
    - network_infrastructure
    - mobile_application
  
  methodology:
    - reconnaissance
    - scanning
    - exploitation
    - post_exploitation
    - reporting
  
  frequency: "quarterly"
  reporting: "detailed_report_with_remediation"
```

## 📊 Security Metrics

### 1. Key Security Metrics

#### Security KPIs
```yaml
# Security Metrics
security_metrics:
  incident_metrics:
    - mean_time_to_detect: "< 1 hour"
    - mean_time_to_resolve: "< 4 hours"
    - incident_frequency: "< 1 per month"
  
  vulnerability_metrics:
    - critical_vulnerabilities: "0"
    - high_vulnerabilities: "< 5"
    - patch_compliance: "> 95%"
  
  access_metrics:
    - failed_login_attempts: "< 10 per day"
    - unauthorized_access_attempts: "0"
    - privileged_access_reviews: "monthly"
```

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Setup authentication system
- [ ] Implement RBAC
- [ ] Configure encryption
- [ ] Setup monitoring

### Phase 2: Advanced Security (Weeks 3-4)
- [ ] Implement MFA
- [ ] Setup SIEM
- [ ] Configure threat detection
- [ ] Establish incident response

### Phase 3: Compliance & Testing (Weeks 5-6)
- [ ] Security testing
- [ ] Compliance audit
- [ ] Documentation review
- [ ] Team training

---

**Tài liệu này cung cấp kiến trúc bảo mật toàn diện cho hệ thống AI Camera Counting, đảm bảo tính bảo mật end-to-end và tuân thủ các tiêu chuẩn bảo mật quốc tế.** 