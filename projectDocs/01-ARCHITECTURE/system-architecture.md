# Kiến trúc tổng thể hệ thống AI Camera Counting

## 📊 Tổng quan

Hệ thống AI Camera Counting được thiết kế theo kiến trúc microservices với 3 thành phần chính:
- **Frontend (React)**: Dashboard UI với real-time updates
- **Backend Services**: beAuth (Authentication) + beCamera (Camera Processing)
- **Infrastructure**: Database, Cache, Message Queue, WebSocket

## 🏗️ System Architecture Overview

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM ARCHITECTURE OVERVIEW                       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRESENTATION LAYER                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Web       │  │   Mobile    │  │   Desktop   │  │   Admin     │        │ │
│  │  │   Dashboard │  │   App       │  │   Client    │  │   Panel     │        │ │
│  │  │   (React)   │  │   (React)   │  │   (Electron)│  │   (React)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API GATEWAY LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Rate      │  │   Auth      │  │   Request   │        │ │
│  │  │   Balancer  │  │   Limiting  │  │   Gateway   │  │   Routing   │        │ │
│  │  │   (NGINX)   │  │   (Redis)   │  │   (JWT)     │  │   (Proxy)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   beAuth    │  │   beCamera  │  │   WebSocket │  │   Analytics │        │ │
│  │  │   Service   │  │   Service   │  │   Service   │  │   Service   │        │ │
│  │  │   (Node.js) │  │   (Python)  │  │   (Node.js) │  │   (Python)  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA LAYER                                      │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Primary   │  │   Cache     │  │   Message   │  │   File      │        │ │
│  │  │   Database  │  │   (Redis)   │  │   Queue     │  │   Storage   │        │ │
│  │  │   (PostgreSQL)│ │             │  │   (RabbitMQ)│  │   (S3/MinIO)│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE LAYER                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Monitoring│  │   Logging   │  │   Security  │  │   Backup    │        │ │
│  │  │   (Prometheus)│ │   (ELK)     │  │   (WAF)     │  │   (Automated)│       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COMPONENT INTERACTION FLOW                         │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Frontend  │    │   API       │    │   Backend   │    │   External  │      │
│  │   (React)   │    │   Gateway   │    │   Services  │    │   Systems   │      │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. User Login     │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Auth Request   │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Validate User  │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Return JWT     │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 5. JWT Token      │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 6. Access Token   │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
│         │ 7. Camera Request │                   │                   │          │
│         │ (with JWT)        │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 8. Forward Request│                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 9. Process Camera │          │
│         │                   │                   │ Data              │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 10. Return Data   │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 11. Display Data  │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW ARCHITECTURE                             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              REAL-TIME DATA FLOW                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Camera    │    │   Worker    │    │   beCamera  │    │   Database  │  │ │
│  │  │   Stream    │    │   Pool      │    │   Service   │    │   (PostgreSQL)│ │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Video Stream   │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. AI Processing  │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Store Results │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Cache Data    │      │ │
│  │         │                   │                   │◄──────────────────┤      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Real-time      │                   │      │ │
│  │         │                   │ Updates           │                   │      │ │
│  │         │                   │◄──────────────────┤                   │      │ │
│  │         │                   │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BATCH DATA FLOW                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Scheduler │    │   Analytics │    │   Data      │    │   Reporting │  │ │
│  │  │   (Cron)    │    │   Engine    │    │   Warehouse │    │   Service   │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Trigger Batch  │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Process Data   │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Generate      │      │ │
│  │         │                   │                   │ Reports          │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Cache Reports │      │ │
│  │         │                   │                   │◄──────────────────┤      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Return Results │                   │      │ │
│  │         │                   │◄──────────────────┤                   │      │ │
│  │         │                   │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TECHNOLOGY STACK OVERVIEW                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              FRONTEND STACK                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   React     │  │   Material  │  │   ApexCharts│  │   WebSocket │        │ │
│  │  │   18.2.0    │  │   UI v5.9.2 │  │   v3.30.0   │  │   Client    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   React     │  │   Emotion   │  │   React     │  │   Create    │        │ │
│  │  │   Router    │  │   (CSS-in-JS)│  │   Icons     │  │   React App │        │ │
│  │  │   DOM v5.2  │  │             │  │   v4.3.1    │  │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BACKEND STACK                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Node.js   │  │   Python    │  │   FastAPI   │  │   Express   │        │ │
│  │  │   + Express │  │   + FastAPI │  │   + Pydantic│  │   + Joi     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   JWT       │  │   bcryptjs  │  │   Winston   │  │   Nodemailer│        │ │
│  │  │   Tokens    │  │   Hashing   │  │   Logging   │  │   Email     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA STACK                                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   PostgreSQL│  │   Redis     │  │   RabbitMQ  │  │   MinIO/S3  │        │ │
│  │  │   Database  │  │   Cache     │  │   Message   │  │   File      │        │ │
│  │  │             │  │             │  │   Queue     │  │   Storage   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE STACK                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Docker    │  │   NGINX     │  │   Prometheus│  │   ELK Stack │        │ │
│  │  │   + Compose │  │   Load      │  │   + Grafana │  │   Logging   │        │ │
│  │  │             │  │   Balancer  │  │   Monitoring│  │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DEPLOYMENT ARCHITECTURE                            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRODUCTION ENVIRONMENT                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Auto      │  │   Container │  │   Database  │        │ │
│  │  │   Balancer  │  │   Scaling   │  │   Orchestrator│ │   Cluster   │        │ │
│  │  │   (NGINX)   │  │   Group     │  │   (K8s/Docker)│ │   (PostgreSQL)│      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                    │                                         │ │
│  │                                    ▼                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Frontend  │  │   beAuth    │  │   beCamera  │  │   WebSocket │        │ │
│  │  │   (React)   │  │   Service   │  │   Service   │  │   Service   │        │ │
│  │  │   Container │  │   Container │  │   Container │  │   Container │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DEVELOPMENT ENVIRONMENT                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Frontend  │  │   beAuth    │  │   beCamera  │  │   Database  │        │ │
│  │  │   Dev Server│  │   Dev Server│  │   Dev Server│  │   (Docker)  │        │ │
│  │  │   Port 3000 │  │   Port 3001 │  │   Port 8000 │  │   Port 5432 │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CI/CD PIPELINE                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Source    │  │   Build     │  │   Test      │  │   Deploy    │        │ │
│  │  │   Control   │  │   Process   │  │   Suite     │  │   Process   │        │ │
│  │  │   (Git)     │  │   (Docker)  │  │   (Jest)    │  │   (K8s)     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY ARCHITECTURE                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECURITY LAYERS                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Network   │  │   Application│  │   Data      │  │   Physical  │        │ │
│  │  │   Security  │  │   Security  │  │   Security  │  │   Security  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Firewall  │  │ • JWT Auth  │  │ • Encryption│  │ • Access    │        │ │
│  │  │ • DDoS      │  │ • Rate Limit│  │ • Backup    │  │   Control   │        │ │
│  │  │ • VPN       │  │ • Input Val │  │ • Audit Log │  │ • Monitoring│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              AUTHENTICATION FLOW                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   User      │    │   Frontend  │    │   beAuth    │    │   Database  │  │ │
│  │  │   Login     │    │   (React)   │    │   Service   │    │   (PostgreSQL)│ │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Credentials    │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Auth Request   │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Validate User │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Generate JWT  │      │ │
│  │         │                   │                   │◄──────────────────┤      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Return Token   │                   │      │ │
│  │         │                   │◄──────────────────┤                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 6. Store Token    │                   │                   │      │ │
│  │         │◄──────────────────┤                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Kiến trúc tổng thể

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   React App     │  │   WebSocket     │  │   API Client    │                  │
│  │   (Dashboard)   │  │   Connection    │  │   (authAPI)     │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Real-time UI  │  │ • Live Updates  │  │ • HTTP Requests │                  │
│  │ • State Mgmt    │  │ • Event Stream  │  │ • Auth Token    │                  │
│  │ • User Auth     │  │ • Reconnection  │  │ • Error Handling│                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Load Balancer │  │   Rate Limiter  │  │   SSL/TLS       │                  │
│  │   (NGINX)       │  │   (Redis)       │  │   Termination   │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Traffic Dist  │  │ • API Throttling│  │ • Cert Mgmt     │                  │
│  │ • Health Check  │  │ • IP Whitelist  │  │ • Security      │                  │
│  │ • Failover      │  │ • DDoS Protect  │  │ • Compression   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND SERVICES                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   beAuth        │  │   beCamera      │  │   WebSocket     │                  │
│  │   Service       │  │   Service       │  │   Service       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • User Auth     │  │ • Camera Mgmt   │  │ • Real-time     │                  │
│  │ • JWT Tokens    │  │ • AI Processing │  │ • Broadcasting  │                  │
│  │ • User Mgmt     │  │ • Analytics     │  │ • Connection    │                  │
│  │ • Permissions   │  │ • Worker Pool   │  │ • Event Routing │                  │
│  │ • Workers       │  │ • Export Logs   │  │ • Export Logs   │                  │
│  │ • Refresh Tokens│  │ • Model Assignments│ │ • Custom Reports│                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   PostgreSQL    │  │   Redis Cache   │  │   Message Queue │                  │
│  │   (Primary DB)  │  │   (L2 Cache)    │  │   (RabbitMQ)    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • User Data     │  │ • Session Data  │  │ • Event Queue   │                  │
│  │ • Camera Data   │  │ • Real-time     │  │ • Task Queue    │                  │
│  │ • Analytics     │  │ • Analytics     │  │ • Dead Letter   │                  │
│  │ • Audit Logs    │  │ • Rate Limiting │  │ • Retry Logic   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INFRASTRUCTURE                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Monitoring    │  │   Logging       │  │   Backup        │                  │
│  │   (Prometheus)  │  │   (ELK Stack)   │  │   (Automated)   │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Metrics       │  │ • Log Aggreg    │  │ • Data Backup   │                  │
│  │ • Alerting      │  │ • Search        │  │ • Disaster Rec  │                  │
│  │ • Dashboards    │  │ • Analysis      │  │ • Point-in-time │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Mục tiêu và Yêu cầu

### Mục tiêu chính
- **Real-time Processing**: Xử lý dữ liệu camera streams theo thời gian thực (< 500ms latency)
- **High Availability**: 99.9% uptime với auto-scaling và fault tolerance
- **Data Consistency**: ACID compliance cho critical data, eventual consistency cho analytics
- **Scalability**: Horizontal scaling cho worker pool, vertical scaling cho database
- **Security**: End-to-end encryption, RBAC, audit logging
- **Observability**: Distributed tracing, metrics collection, centralized logging

### Yêu cầu Production
- **Performance**: Sub-second latency cho real-time data, < 2s cho analytics queries
- **Reliability**: 99.9% uptime, automatic failover, data durability
- **Security**: TLS 1.3, JWT tokens, API rate limiting, input validation
- **Monitoring**: Real-time metrics, alerting, performance dashboards
- **Compliance**: GDPR, data retention policies, audit trails

## 🔧 Technology Stack

### Frontend Stack (Current Implementation)
- **Framework**: React 18.2.0 với JavaScript
- **UI Library**: Material-UI (MUI) v5.9.2 + Vision UI Dashboard theme
- **State Management**: React Context API + useReducer (AuthContext)
- **Routing**: React Router DOM v5.2.0
- **HTTP Client**: Native fetch API với custom authAPI service
- **Build Tool**: Create React App (react-scripts v5.0.1)
- **Charts**: ApexCharts v3.30.0 + react-apexcharts
- **Icons**: React Icons v4.3.1 + @mui/icons-material
- **Styling**: Emotion (CSS-in-JS) + custom theme system
- **Authentication**: JWT tokens với refresh mechanism
- **Real-time**: Chưa implement (cần thêm WebSocket client)

### Backend Stack (Current Implementation)
- **beAuth Service**: Node.js + Express + PostgreSQL (đã implement)
- **beCamera Service**: Python + FastAPI + PostgreSQL (đang phát triển)
- **WebSocket Service**: Chưa implement (cần thêm cho real-time)
- **Message Queue**: Chưa implement (cần thêm cho worker pool)
- **Cache**: Redis (cần thêm cho session và caching)
- **Database**: PostgreSQL với connection pooling (đã setup)
- **Authentication**: JWT tokens với bcryptjs cho password hashing
- **Validation**: Joi cho input validation
- **Logging**: Winston cho structured logging
- **Email**: Nodemailer cho email notifications

### Infrastructure Stack (Current Implementation)
- **Load Balancer**: Chưa implement (cần thêm NGINX)
- **Container**: Docker + Docker Compose (đã setup cho beAuth)
- **Orchestration**: Chưa implement (cần thêm cho production)
- **Monitoring**: Chưa implement (cần thêm Prometheus + Grafana)
- **Logging**: Chưa implement (cần thêm ELK Stack)
- **CI/CD**: Chưa implement (cần thêm GitHub Actions)
- **Environment**: Development setup với hot reload
- **Database**: PostgreSQL với init scripts
- **Port Configuration**: 
  - Frontend: 3000 (React dev server)
  - beAuth: 3001 (Express server)
  - beCamera: 8000 (FastAPI server - planned)

## 🔄 Data Flow Patterns

### 1. Authentication Flow
```
Frontend → beAuth Service → PostgreSQL → Frontend
```

### 2. Real-time Camera Data Flow
```
Camera Stream → Worker Pool → beCamera Service → PostgreSQL → Redis → WebSocket → Frontend
```

### 3. Analytics Data Flow
```
Scheduler → Analytics Service → PostgreSQL → Redis → Frontend
```

### 4. Camera Management Flow
```
Frontend → beCamera Service → PostgreSQL → Worker Pool → Frontend
```

## 🗄️ Database Architecture

### Shared Database Approach
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Shared PostgreSQL Database                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Auth Schema   │  │  Camera Schema  │  │ Analytics Schema│                  │
│  │   (beAuth)      │  │   (beCamera)    │  │   (beCamera)    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • users         │  │ • cameras       │  │ • hourly_analytics                 │
│  │ • user_sessions │  │ • counting_results│ │ • daily_analytics                  │
│  │ • audit_log     │  │ • camera_events │  │ • monthly_analytics                │
│  │ • permissions   │  │ • camera_alerts │  │ • performance_metrics              │
│  │ • roles         │  │ • ai_models     │  │ • trend_analysis                   │
│  │ • refresh_tokens│  │ • model_assignments│ │ • custom_reports                  │
│  │ • workers       │  │ • export_logs     │  │ • export_logs                      │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔐 Security Architecture

### Security Measures
- **Authentication**: JWT tokens với refresh mechanism
- **Password Hashing**: bcryptjs với salt rounds
- **Input Validation**: Joi schema validation
- **CORS**: Express CORS middleware
- **Helmet**: Security headers
- **Rate Limiting**: express-rate-limit
- **Encryption**: Chưa implement TLS/SSL (cần thêm cho production)
- **WAF**: Chưa implement (cần thêm cho production)
- **Secrets Management**: Environment variables
- **Session Management**: JWT-based với localStorage

## 📈 Monitoring & Observability

### Monitoring Stack
- **Metrics Collection**: Prometheus, Grafana (planned)
- **Log Aggregation**: ELK Stack (planned)
- **Tracing**: Jaeger, Zipkin (planned)
- **Alerting**: PagerDuty, Slack, Email (planned)

### Key Metrics
- **Performance**: Response time, throughput, latency
- **Availability**: Uptime, downtime, MTTR
- **Resource Usage**: CPU, memory, disk, network
- **Error Rates**: Error percentage, failure rates
- **Business Metrics**: User engagement, feature usage, quality metrics

## 🚀 Implementation Roadmap

### Phase 1: Foundation (COMPLETED)
- ✅ Authentication system
- ✅ Basic frontend structure
- ✅ Backend API foundation

### Phase 2: Camera Management (IN PROGRESS)
- 🔄 Camera CRUD operations
- 🔄 Camera configuration interface
- 🔄 Stream management

### Phase 3: Real-time Processing (NEXT)
- ⏳ WebSocket integration
- ⏳ Worker pool implementation
- ⏳ Real-time data streaming

### Phase 4: Analytics & Reporting (PLANNED)
- ⏳ Analytics engine
- ⏳ Report generation
- ⏳ Data visualization

### Phase 5: Production Infrastructure (PLANNED)
- ⏳ Containerization
- ⏳ Monitoring & logging
- ⏳ Security hardening

## 📋 Production Readiness Checklist

### Infrastructure Readiness
- [ ] **High Availability**: Multi-zone deployment
- [ ] **Load Balancing**: Proper load balancer configuration
- [ ] **Auto-scaling**: Auto-scaling policies configured
- [ ] **Monitoring**: Comprehensive monitoring setup
- [ ] **Backup Strategy**: Automated backup và recovery
- [ ] **Security**: Security measures implemented
- [ ] **Compliance**: Compliance requirements met

### Application Readiness
- [ ] **Error Handling**: Comprehensive error handling
- [ ] **Logging**: Structured logging implemented
- [ ] **Performance**: Performance benchmarks met
- [ ] **Testing**: Comprehensive test coverage
- [ ] **Documentation**: Complete documentation
- [ ] **Deployment**: Automated deployment pipeline
- [ ] **Rollback**: Rollback procedures in place

### Operational Readiness
- [ ] **Monitoring**: Real-time monitoring và alerting
- [ ] **Incident Response**: Incident response procedures
- [ ] **Support**: 24/7 support coverage
- [ ] **Training**: Team training completed
- [ ] **Disaster Recovery**: Disaster recovery plan
- [ ] **Capacity Planning**: Capacity planning completed
- [ ] **Performance Tuning**: Performance optimization completed

---

**Tài liệu này cung cấp tổng quan kiến trúc hệ thống AI Camera Counting, bao gồm technology stack, data flow patterns, và implementation roadmap.** 