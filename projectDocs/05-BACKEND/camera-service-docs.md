# Lý thuyết quản lý Camera - Camera Management Theory

## 📊 Tổng quan

Hệ thống quản lý camera là thành phần cốt lõi của AI Camera Counting System, chịu trách nhiệm quản lý toàn bộ lifecycle của cameras từ registration đến decommissioning.

## 🎯 Mục tiêu và Yêu cầu

### Mục tiêu chính
- **Centralized Management**: Quản lý tập trung tất cả cameras trong hệ thống
- **Real-time Monitoring**: Theo dõi trạng thái cameras theo thời gian thực
- **Automated Processing**: Tự động xử lý camera streams với AI models
- **Scalable Architecture**: Khả năng mở rộng để hỗ trợ hàng trăm cameras
- **Fault Tolerance**: Xử lý lỗi và recovery tự động
- **Security**: Bảo mật camera streams và access control

### Yêu cầu Production
- **Performance**: Sub-second response time cho camera operations
- **Reliability**: 99.9% uptime cho camera management services
- **Scalability**: Support 100+ concurrent camera streams
- **Security**: Encrypted streams, access control, audit logging
- **Monitoring**: Real-time health monitoring và alerting

## 🏗️ Kiến trúc Camera Management

### Camera Management Architecture

#### Camera Lifecycle Management Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA LIFECYCLE MANAGEMENT                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              LIFECYCLE PHASES                               │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Planning  │    │   Setup     │    │   Operation │    │   Decommission│ │ │
│  │  │   Phase     │    │   Phase     │    │   Phase     │    │   Phase      │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Requirements   │                   │                   │      │ │
│  │         │ 2. Site Survey    │                   │                   │      │ │
│  │         │ 3. Design         │                   │                   │      │ │
│  │         │ 4. Procurement    │                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Installation   │                   │      │ │
│  │         │                   │ 6. Configuration  │                   │      │ │
│  │         │                   │ 7. Testing        │                   │      │ │
│  │         │                   │ 8. Registration   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 9. Monitoring     │      │ │
│  │         │                   │                   │ 10. Maintenance   │      │ │
│  │         │                   │                   │ 11. Optimization  │      │ │
│  │         │                   │                   │ 12. Troubleshooting│     │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │                   │ 13. Deactivate│ │
│  │         │                   │                   │                   │ 14. Archive│ │
│  │         │                   │                   │                   │ 15. Remove│ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STATUS TRANSITIONS                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Planned   │    │   Installed │    │   Online    │    │   Offline   │  │ │
│  │  │             │    │             │    │             │    │             │  │ │
│  │  │ • Design    │    │ • Hardware  │    │ • Processing│    │ • Error     │  │ │
│  │  │ • Specs     │    │ • Network   │    │ • Streaming │    │ • Maintenance│ │ │
│  │  │ • Budget    │    │ • Software  │    │ • Analytics │    │ • Disabled  │  │ │
│  │  │ • Timeline  │    │ • Testing   │    │ • Monitoring│    │ • Archived  │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ Install           │ Configure          │ Error/Disable     │      │ │
│  │         │──────────────────►│──────────────────►│◄──────────────────│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ Recover/Enable    │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Camera Processing Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA PROCESSING FLOW                             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PROCESSING PIPELINE                            │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Camera    │    │   Frame     │    │   AI        │    │   Result    │  │ │
│  │  │   Stream    │    │   Capture   │    │   Processing│    │   Storage   │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. RTSP Stream    │                   │                   │      │ │
│  │         │ (1920x1080, 25fps)│                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Frame Buffer   │                   │      │ │
│  │         │                   │ (Queue Management)│                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Preprocessing  │      │ │
│  │         │                   │                   │ (Resize, Normalize)│     │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. AI Detection   │      │ │
│  │         │                   │                   │ (People Detection)│      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 5. Post-processing│      │ │
│  │         │                   │                   │ (Filtering, Tracking)│   │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 6. Result Storage │      │ │
│  │         │                   │                   │ (Database + Cache)│      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              REAL-TIME FEEDBACK                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Result    │    │   WebSocket │    │   Frontend  │    │   Analytics │  │ │
│  │  │   Storage   │    │   Service   │    │   (React)   │    │   Service   │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 7. Broadcast      │                   │                   │      │ │
│  │         │ Results           │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 8. Real-time      │                   │      │ │
│  │         │                   │ Updates           │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 9. UI Update      │      │ │
│  │         │                   │                   │ (Dashboard)       │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 10. Analytics     │      │ │
│  │         │                   │                   │ Update            │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Camera Monitoring Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA MONITORING ARCHITECTURE                      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MONITORING LAYERS                              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Health        │  │   Performance   │  │   Security      │              │ │
│  │  │   Monitoring    │  │   Monitoring    │  │   Monitoring    │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Connection    │  │ • Processing    │  │ • Access Logs   │              │ │
│  │  │   Status        │  │   Latency       │  │ • Authentication│              │ │
│  │  │ • Stream Health │  │ • Detection     │  │ • Authorization │              │ │
│  │  │ • Error Rates   │  │   Accuracy      │  │ • Data Access   │              │ │
│  │  │ • Recovery      │  │ • Resource      │  │ • Audit Trails  │              │ │
│  │  │   Time          │  │   Usage         │  │ • Threat        │              │ │
│  │  │ • Uptime        │  │ • Throughput    │  │   Detection     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MONITORING COMPONENTS                          │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Camera    │    │   Worker    │    │   Monitoring│    │   Alerting  │  │ │
│  │  │   Registry  │    │   Pool      │    │   Service   │    │   Service   │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Health Check   │                   │                   │      │ │
│  │         │ (Every 30s)       │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Status Report  │                   │      │ │
│  │         │                   │ (CPU, Memory,     │                   │      │ │
│  │         │                   │  Network, Errors) │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Metrics        │      │ │
│  │         │                   │                   │ Collection        │      │ │
│  │         │                   │                   │ (Prometheus)      │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Threshold      │      │ │
│  │         │                   │                   │ Check              │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 5. Alert          │      │ │
│  │         │                   │                   │ Generation        │      │ │
│  │         │                   │                   │ (Email, SMS,      │      │ │
│  │         │                   │                   │  Slack, PagerDuty)│      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DASHBOARD METRICS                              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Real-time     │  │   Historical    │  │   Predictive    │              │ │
│  │  │   Metrics       │  │   Analytics     │  │   Analytics     │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Current Count │  │ • Daily Trends  │  │ • Capacity      │              │ │
│  │  │ • Processing    │  │ • Peak Hours    │  │   Planning      │              │ │
│  │  │   Status        │  │ • Performance   │  │ • Maintenance   │              │ │
│  │  │ • Error Status  │  │   Trends        │  │   Scheduling    │              │ │
│  │  │ • Resource      │  │ • Usage         │  │ • Scaling       │              │ │
│  │  │   Usage         │  │   Patterns      │  │   Predictions   │              │ │
│  │  │ • Alert Status  │  │ • Anomaly       │  │ • Risk          │              │ │
│  │  │                 │  │   Detection     │  │   Assessment    │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Camera Deployment Strategy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA DEPLOYMENT STRATEGY                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DEPLOYMENT PHASES                              │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Planning  │    │   Staging   │    │   Production│    │   Scaling   │  │ │
│  │  │   Phase     │    │   Phase     │    │   Phase     │    │   Phase     │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Site Survey    │                   │                   │      │ │
│  │         │ 2. Network Design │                   │                   │      │ │
│  │         │ 3. Hardware       │                   │                   │      │ │
│  │         │    Selection      │                   │                   │      │ │
│  │         │ 4. Security       │                   │                   │      │ │
│  │         │    Planning       │                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Test Setup     │                   │      │ │
│  │         │                   │ 6. Configuration  │                   │      │ │
│  │         │                   │ 7. Integration    │                   │      │ │
│  │         │                   │ 8. Performance    │                   │      │ │
│  │         │                   │    Testing        │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 9. Live Deployment│      │ │
│  │         │                   │                   │ 10. Monitoring    │      │ │
│  │         │                   │                   │ 11. Optimization  │      │ │
│  │         │                   │                   │ 12. Maintenance   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │                   │ 13. Scale│ │
│  │         │                   │                   │                   │ 14. Upgrade│ │
│  │         │                   │                   │                   │ 15. Migrate│ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DEPLOYMENT STRATEGIES                          │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Blue-Green    │  │   Canary        │  │   Rolling       │              │ │
│  │  │   Deployment    │  │   Deployment    │  │   Update        │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Zero Downtime │  │ • Risk Mitigation│ │ • Gradual       │              │ │
│  │  │ • Fast Rollback │  │ • A/B Testing   │  │   Updates       │              │ │
│  │  │ • Full Testing  │  │ • Performance   │  │ • Continuous    │              │ │
│  │  │ • Resource      │  │   Monitoring    │  │   Availability  │              │ │
│  │  │   Intensive     │  │ • User Feedback │  │ • Resource      │              │ │
│  │  │ • Cost Higher   │  │ • Slow Rollout  │  │   Efficient     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE CONSIDERATIONS                  │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Network       │  │   Security      │  │   Scalability   │              │ │
│  │  │   Requirements  │  │   Requirements  │  │   Requirements  │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Bandwidth     │  │ • Encryption    │  │ • Auto-scaling  │              │ │
│  │  │ • Latency       │  │ • Authentication│  │ • Load Balancing│              │ │
│  │  │ • Reliability   │  │ • Authorization │  │ • Resource      │              │ │
│  │  │ • Redundancy    │  │ • Audit Logging │  │   Management    │              │ │
│  │  │ • QoS           │  │ • Compliance    │  │ • Performance   │              │ │
│  │  │ • Monitoring    │  │ • Incident      │  │   Optimization  │              │ │
│  │  │                 │  │   Response      │  │ • Cost          │              │ │
│  │  │                 │  │                 │  │   Optimization  │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Camera Security Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA SECURITY ARCHITECTURE                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECURITY LAYERS                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Network       │  │   Application   │  │   Data          │              │ │
│  │  │   Security      │  │   Security      │  │   Security      │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • VPN           │  │ • Authentication│  │ • Encryption    │              │ │
│  │  │ • Firewall      │  │ • Authorization │  │ • Access Control│              │ │
│  │  │ • IDS/IPS       │  │ • Input Valid   │  │ • Audit Logging │              │ │
│  │  │ • Network       │  │ • Session Mgmt  │  │ • Backup        │              │ │
│  │  │   Segmentation  │  │ • Rate Limiting │  │ • Compliance    │              │ │
│  │  │ • DDoS Protect  │  │ • API Security  │  │ • Data          │              │ │
│  │  │                 │  │                 │  │   Classification│              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ACCESS CONTROL MATRIX                          │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │   Role      │ │ Network     │ │ Application │ │ Data        │ │ Audit  │ │ │
│  │  │             │ │ Access      │ │ Access      │ │ Access      │ │ Access │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ Admin       │ │ Full        │ │ Full        │ │ Full        │ │ Full   │ │ │
│  │  │             │ │ Access      │ │ Access      │ │ Access      │ │ Access │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ Operator    │ │ Limited     │ │ Read/Write  │ │ Read/Write  │ │ Read   │ │ │
│  │  │             │ │ Access      │ │ Access      │ │ Access      │ │ Access │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ Viewer      │ │ Read Only   │ │ Read Only   │ │ Read Only   │ │ None   │ │ │
│  │  │             │ │ Access      │ │ Access      │ │ Access      │ │ Access │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │ │
│  │  │ Guest       │ │ No Access   │ │ No Access   │ │ No Access   │ │ No     │ │ │
│  │  │             │ │             │ │             │ │             │ │ Access │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECURITY COMPONENTS                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Authentication│  │   Authorization │  │   Monitoring    │              │ │
│  │  │   & Identity    │  │   & Access      │  │   & Alerting    │              │ │
│  │  │   Management    │  │   Control       │  │                 │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Multi-factor  │  │ • Role-based    │  │ • SIEM          │              │ │
│  │  │   Auth (MFA)    │  │   Access Control│  │ • Threat        │              │ │
│  │  │ • Single Sign-on│  │ • Attribute-based│ │   Detection     │              │ │
│  │  │   (SSO)         │  │   Access Control│  │ • Incident      │              │ │
│  │  │ • Certificate   │  │ • Policy-based  │  │   Response      │              │ │
│  │  │   Management    │  │   Access Control│  │ • Compliance    │              │ │
│  │  │ • Identity      │  │ • Dynamic       │  │   Monitoring    │              │ │
│  │  │   Federation    │  │   Authorization │  │ • Audit         │              │ │
│  │  │ • Password      │  │ • Just-in-time  │  │   Logging       │              │ │
│  │  │   Policies      │  │   Access        │  │ • Forensics     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Camera Performance Optimization Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA PERFORMANCE OPTIMIZATION                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              OPTIMIZATION AREAS                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Stream        │  │   Processing    │  │   Storage       │              │ │
│  │  │   Optimization  │  │   Optimization  │  │   Optimization  │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Connection    │  │ • Model Caching │  │ • Data          │              │ │
│  │  │   Pooling       │  │ • Frame Skipping│  │   Compression   │              │ │
│  │  │ • Buffer        │  │ • Parallel      │  │ • Indexing      │              │ │
│  │  │   Management    │  │   Processing    │  │ • Partitioning  │              │ │
│  │  │ • Quality       │  │ • Resource      │  │ • Archiving     │              │ │
│  │  │   Scaling       │  │   Management    │  │ • Caching       │              │ │
│  │  │ • Bandwidth     │  │ • Load          │  │ • Backup        │              │ │
│  │  │   Management    │  │   Balancing     │  │   Optimization  │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PERFORMANCE METRICS                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Latency       │  │   Throughput    │  │   Resource      │              │ │
│  │  │   Metrics       │  │   Metrics       │  │   Usage         │              │ │
│  │  │                 │  │                 │  │   Metrics       │              │ │
│  │  │ • Frame Capture │  │ • FPS           │  │ • CPU Usage     │              │ │
│  │  │   Time          │  │ • Processing    │  │ • Memory Usage  │              │ │
│  │  │ • Processing    │  │   Rate          │  │ • Network       │              │ │
│  │  │   Latency       │  │ • Detection     │  │   Bandwidth     │              │ │
│  │  │ • Response      │  │   Rate          │  │ • Storage I/O   │              │ │
│  │  │   Time          │  │ • Accuracy      │  │ • GPU Usage     │              │ │
│  │  │ • End-to-end    │  │ • Error Rate    │  │ • Disk Space    │              │ │
│  │  │   Latency       │  │ • Success Rate  │  │ • Cache Hit     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              OPTIMIZATION STRATEGIES                        │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Horizontal    │  │   Vertical      │  │   Hybrid        │              │ │
│  │  │   Scaling       │  │   Scaling       │  │   Scaling       │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Add More      │  │ • Upgrade       │  │ • Auto-scaling  │              │ │
│  │  │   Workers       │  │   Hardware      │  │ • Load          │              │ │
│  │  │ • Load          │  │ • Increase      │  │   Balancing     │              │ │
│  │  │   Distribution  │  │   Resources     │  │ • Resource      │              │ │
│  │  │ • Geographic    │  │ • Optimize      │  │   Optimization  │              │ │
│  │  │   Distribution  │  │   Software      │  │ • Performance   │              │ │
│  │  │ • Fault         │  │ • Tune          │  │   Monitoring    │              │ │
│  │  │   Tolerance     │  │   Parameters    │  │ • Cost          │              │ │
│  │  │ • Cost          │  │ • Reduce        │  │   Optimization  │              │ │
│  │  │   Effective     │  │   Overhead      │  │ • Adaptive      │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA MANAGEMENT LAYER                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Camera        │  │   Stream        │  │   Configuration │                  │
│  │   Registry      │  │   Manager       │  │   Manager       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Camera CRUD   │  │ • Stream        │  │ • Settings      │                  │
│  │ • Metadata      │  │   Validation    │  │ • AI Models     │                  │
│  │ • Status        │  │ • Health Check  │  │ • Zones         │                  │
│  │ • History       │  │ • Recovery      │  │ • Alerts        │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WORKER POOL LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Worker        │  │   Load          │  │   Task          │                  │
│  │   Manager       │  │   Balancer      │  │   Scheduler     │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Worker        │  │ • Camera        │  │ • Processing    │                  │
│  │   Assignment    │  │   Distribution  │  │   Queue         │                  │
│  │ • Health        │  │ • Failover      │  │ • Priority      │                  │
│  │   Monitoring    │  │ • Scaling       │  │   Management    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PROCESSING LAYER                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   AI Model      │  │   Frame         │  │   Counting      │                  │
│  │   Manager       │  │   Processor     │  │   Engine        │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Model         │  │ • Frame         │  │ • People        │                  │
│  │   Loading       │  │   Capture       │  │   Detection     │                  │
│  │ • Version       │  │ • Preprocessing │  │ • Tracking      │                  │
│  │   Control       │  │ • Quality       │  │ • Analytics     │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Camera Lifecycle Management

### 1. Camera Registration Phase

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Camera    │    │   Stream    │    │   Worker    │
│   (React)   │    │   Registry  │    │   Manager   │    │   Pool      │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Add Camera     │                   │                   │
       │    Request        │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Validate       │                   │
       │                   │    Camera Config  │                   │
       │                   │                   │                   │
       │                   │ 3. Store Camera   │                   │
       │                   │    Data           │                   │
       │                   │                   │                   │
       │                   │ 4. Test Stream    │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │ 5. Stream Valid   │                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │                   │ 6. Assign Worker  │                   │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
       │ 7. Success        │                   │                   │
       │    Response       │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
```

#### Registration Steps:
1. **Camera Configuration**: User nhập thông tin camera (name, location, stream URL)
2. **Validation**: Validate camera settings và stream URL
3. **Database Storage**: Lưu camera data vào PostgreSQL
4. **Stream Testing**: Test kết nối stream để đảm bảo accessibility
5. **Worker Assignment**: Assign camera cho available worker
6. **Status Update**: Update camera status thành "online"

### 2. Camera Processing Phase

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Camera    │    │   Worker    │    │   AI Model  │    │   Database  │
│   Stream    │    │   Pool      │    │   Manager   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. RTSP Stream    │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Load AI Model  │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │ 3. Model Loaded   │                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │                   │ 4. Process Frames │                   │
       │                   │                   │                   │
       │                   │ 5. Store Results  │                   │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
```

#### Processing Steps:
1. **Stream Connection**: Worker kết nối đến camera stream
2. **Model Loading**: Load AI model phù hợp cho camera
3. **Frame Processing**: Capture và process frames theo thời gian thực
4. **AI Detection**: Thực hiện people detection với AI model
5. **Data Storage**: Lưu counting results vào database
6. **Real-time Updates**: Broadcast updates qua WebSocket

### 3. Camera Monitoring Phase

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Health    │    │   Camera    │    │   Alert     │    │   Frontend  │
│   Monitor   │    │   Registry  │    │   System    │    │   (React)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Health Check   │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Status Update  │                   │
       │                   │                   │                   │
       │                   │ 3. Check Alerts   │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │ 4. Alert Trigger  │                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │                   │ 5. Notify User    │                   │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
```

#### Monitoring Steps:
1. **Health Check**: Regular health check cho camera streams
2. **Status Monitoring**: Monitor camera status và performance
3. **Alert Management**: Trigger alerts khi có issues
4. **User Notification**: Notify users qua multiple channels
5. **Recovery Actions**: Automatic recovery khi có thể

### 4. Camera Decommissioning Phase

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Camera    │    │   Worker    │    │   Database  │
│   (React)   │    │   Registry  │    │   Pool      │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Delete Camera  │                   │                   │
       │    Request        │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Stop Processing│                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │ 3. Processing     │                   │
       │                   │    Stopped        │                   │
       │                   │◄──────────────────│                   │
       │                   │                   │                   │
       │                   │ 4. Archive Data   │                   │
       │                   │──────────────────────────────────────►│
       │                   │                   │                   │
       │ 5. Success        │                   │                   │
       │    Response       │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
```

#### Decommissioning Steps:
1. **Delete Request**: User request xóa camera
2. **Stop Processing**: Stop camera processing trong worker
3. **Data Archival**: Archive historical data
4. **Cleanup**: Clean up resources và configurations
5. **Confirmation**: Confirm deletion thành công

## 🗄️ Camera Data Model

### Core Camera Entity

```sql
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    stream_url VARCHAR(500) NOT NULL,
    stream_type VARCHAR(20) DEFAULT 'rtsp',
    location VARCHAR(200),
    coordinates POINT,
    status camera_status DEFAULT 'offline',
    worker_id VARCHAR(50),
    settings JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    security_config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Camera Settings Schema

```json
{
  "detection_sensitivity": 0.8,
  "max_occupancy": 50,
  "counting_zones": [
    {
      "id": "zone_1",
      "name": "Entrance Zone",
      "x": 100,
      "y": 200,
      "width": 300,
      "height": 100,
      "direction": "in"
    }
  ],
  "alert_threshold": 40,
  "notification_enabled": true,
  "ai_model_id": 1,
  "processing_fps": 25,
  "quality_threshold": 0.7
}
```

### Camera Metadata Schema

```json
{
  "manufacturer": "Hikvision",
  "model": "DS-2CD2142FWD-I",
  "resolution": "1920x1080",
  "fps": 25,
  "bitrate": "2048kbps",
  "firmware_version": "V5.5.82",
  "serial_number": "DS-2CD2142FWD-I20201201AACH123456789",
  "installation_date": "2024-01-15",
  "maintenance_schedule": "monthly"
}
```

### Security Configuration Schema

```json
{
  "encryption_enabled": true,
  "access_control": ["user1", "user2"],
  "ip_whitelist": ["192.168.1.0/24"],
  "authentication": {
    "username": "admin",
    "password_encrypted": "encrypted_password"
  },
  "ssl_enabled": true,
  "certificate_path": "/certs/camera1.pem"
}
```

## 🔐 Security Considerations

### Stream Security
- **Encryption**: Encrypt camera streams với TLS/SSL
- **Authentication**: Implement camera authentication
- **Access Control**: IP whitelisting và user-based access control
- **Audit Logging**: Log tất cả access attempts

### Data Security
- **Data Encryption**: Encrypt sensitive camera data
- **Backup Security**: Secure backup procedures
- **Access Logging**: Comprehensive access logging
- **Compliance**: GDPR và data privacy compliance

## 📈 Performance Optimization

### Stream Optimization
- **Connection Pooling**: Efficient connection management
- **Buffer Management**: Optimal buffer sizing
- **Quality Scaling**: Dynamic quality adjustment
- **Bandwidth Management**: Bandwidth optimization

### Processing Optimization
- **Model Caching**: Cache AI models cho fast loading
- **Frame Skipping**: Skip frames khi cần thiết
- **Parallel Processing**: Parallel frame processing
- **Resource Management**: Efficient resource allocation

## 🚨 Error Handling & Recovery

### Common Error Scenarios
1. **Stream Connection Failure**: Camera không accessible
2. **AI Model Loading Failure**: Model không load được
3. **Worker Failure**: Worker process crash
4. **Database Connection Failure**: Database không accessible
5. **Network Issues**: Network connectivity problems

### Recovery Strategies
1. **Automatic Retry**: Retry failed operations
2. **Failover**: Switch to backup workers
3. **Graceful Degradation**: Reduce functionality khi cần
4. **Manual Intervention**: Alert operators cho manual fix
5. **Data Recovery**: Recover lost data từ backups

## 📊 Monitoring & Metrics

### Key Metrics
- **Camera Uptime**: Percentage of time camera is operational
- **Processing Latency**: Time từ frame capture đến result
- **Detection Accuracy**: Accuracy của AI detection
- **Resource Usage**: CPU, memory, network usage
- **Error Rates**: Error frequency và types

### Alerting Rules
- **Camera Offline**: Camera không accessible > 5 minutes
- **High Latency**: Processing latency > 1 second
- **Low Accuracy**: Detection accuracy < 80%
- **High Error Rate**: Error rate > 5%
- **Resource Exhaustion**: Resource usage > 90%

---

**Tài liệu này cung cấp lý thuyết toàn diện về quản lý camera trong hệ thống AI Camera Counting, bao gồm lifecycle management, security, performance, và monitoring.** 