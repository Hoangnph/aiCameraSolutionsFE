# Database Diagrams - AI Camera Counting System

## 📊 Tổng quan

Thư mục này chứa tất cả các sơ đồ và diagram liên quan đến database design cho hệ thống AI Camera Counting.

## 📁 Cấu trúc thư mục

```
diagrams/
├── README.md                    # Tài liệu này
├── erd/                        # Entity Relationship Diagrams
│   ├── main-erd.png           # ERD chính của hệ thống
│   ├── user-management-erd.png # ERD cho user management
│   ├── camera-system-erd.png   # ERD cho camera system
│   └── analytics-erd.png       # ERD cho analytics system
├── architecture/               # Architecture Diagrams
│   ├── database-architecture.png # Kiến trúc database tổng thể
│   ├── multi-tenant-arch.png   # Kiến trúc multi-tenant
│   ├── high-availability.png   # Kiến trúc high availability
│   └── scaling-strategy.png    # Chiến lược scaling
├── data-flow/                  # Data Flow Diagrams
│   ├── main-data-flow.png      # Data flow chính
│   ├── real-time-processing.png # Real-time data processing
│   ├── batch-processing.png    # Batch processing flow
│   └── analytics-flow.png      # Analytics data flow
├── cache/                      # Cache Architecture
│   ├── redis-architecture.png  # Redis cache architecture
│   ├── cache-key-structure.png # Cache key structure
│   └── cache-flow.png          # Cache data flow
├── queue/                      # Queue Architecture
│   ├── rabbitmq-architecture.png # RabbitMQ architecture
│   ├── queue-flow.png          # Queue message flow
│   └── dead-letter-queue.png   # Dead letter queue handling
├── security/                   # Security Diagrams
│   ├── security-architecture.png # Security architecture
│   ├── access-control.png      # Access control matrix
│   └── encryption-flow.png     # Encryption data flow
├── performance/                # Performance Diagrams
│   ├── performance-architecture.png # Performance architecture
│   ├── indexing-strategy.png   # Indexing strategy
│   └── partitioning-strategy.png # Partitioning strategy
├── deployment/                 # Deployment Diagrams
│   ├── ci-cd-pipeline.png      # CI/CD pipeline
│   ├── blue-green-deployment.png # Blue-green deployment
│   └── environment-structure.png # Environment structure
└── monitoring/                 # Monitoring Diagrams
    ├── monitoring-architecture.png # Monitoring architecture
    ├── alerting-flow.png       # Alerting flow
    └── metrics-dashboard.png   # Metrics dashboard
```

## 🎯 Mục đích

### ERD (Entity Relationship Diagrams)
- **main-erd.png**: Sơ đồ quan hệ thực thể chính của toàn bộ hệ thống
- **user-management-erd.png**: Chi tiết về user, roles, permissions
- **camera-system-erd.png**: Chi tiết về cameras, streams, events
- **analytics-erd.png**: Chi tiết về analytics, reports, metrics

### Architecture Diagrams
- **database-architecture.png**: Kiến trúc database tổng thể với các layer
- **multi-tenant-arch.png**: Kiến trúc multi-tenant với tenant isolation
- **high-availability.png**: Kiến trúc high availability và disaster recovery
- **scaling-strategy.png**: Chiến lược scaling horizontal và vertical

### Data Flow Diagrams
- **main-data-flow.png**: Luồng dữ liệu chính từ camera đến analytics
- **real-time-processing.png**: Xử lý dữ liệu real-time
- **batch-processing.png**: Xử lý batch và ETL
- **analytics-flow.png**: Luồng dữ liệu analytics

### Cache Architecture
- **redis-architecture.png**: Kiến trúc Redis cache
- **cache-key-structure.png**: Cấu trúc cache keys
- **cache-flow.png**: Luồng dữ liệu cache

### Queue Architecture
- **rabbitmq-architecture.png**: Kiến trúc RabbitMQ
- **queue-flow.png**: Luồng message trong queue
- **dead-letter-queue.png**: Xử lý dead letter queue

### Security Diagrams
- **security-architecture.png**: Kiến trúc bảo mật tổng thể
- **access-control.png**: Ma trận kiểm soát truy cập
- **encryption-flow.png**: Luồng mã hóa dữ liệu

### Performance Diagrams
- **performance-architecture.png**: Kiến trúc tối ưu hiệu suất
- **indexing-strategy.png**: Chiến lược indexing
- **partitioning-strategy.png**: Chiến lược partitioning

### Deployment Diagrams
- **ci-cd-pipeline.png**: Pipeline CI/CD
- **blue-green-deployment.png**: Blue-green deployment strategy
- **environment-structure.png**: Cấu trúc môi trường

### Monitoring Diagrams
- **monitoring-architecture.png**: Kiến trúc monitoring
- **alerting-flow.png**: Luồng alerting
- **metrics-dashboard.png**: Dashboard metrics

## 🔧 Công cụ tạo diagram

### Recommended Tools
- **Draw.io / Diagrams.net**: Free, web-based diagram tool
- **Lucidchart**: Professional diagram tool
- **Visio**: Microsoft diagram tool
- **PlantUML**: Code-based diagram generation
- **Mermaid**: Markdown-based diagram tool

### File Formats
- **PNG**: Cho web và documentation
- **SVG**: Cho vector graphics
- **PDF**: Cho printing và sharing
- **Draw.io format**: Cho editing

## 📋 Guidelines

### Naming Convention
- Sử dụng kebab-case cho tên file
- Mô tả rõ ràng nội dung diagram
- Thêm version number nếu cần

### Quality Standards
- **Resolution**: Minimum 1920x1080 for detailed diagrams
- **Colors**: Consistent color scheme across all diagrams
- **Fonts**: Readable fonts (Arial, Helvetica, etc.)
- **Labels**: Clear and descriptive labels
- **Legends**: Include legends for complex diagrams

### Version Control
- Track changes in Git
- Use meaningful commit messages
- Tag major versions
- Keep backup copies

## 🚀 Usage

### For Developers
1. Reference diagrams for understanding system architecture
2. Use as basis for implementation
3. Update diagrams when architecture changes
4. Include in technical documentation

### For Stakeholders
1. Use for system overview presentations
2. Include in project documentation
3. Share with clients and partners
4. Use for training materials

## 📝 Maintenance

### Regular Updates
- Update diagrams when architecture changes
- Review diagrams quarterly
- Validate accuracy with implementation
- Remove outdated diagrams

### Documentation
- Keep README updated
- Document diagram creation process
- Maintain change log
- Version control all diagrams

---

**Lưu ý**: Tất cả diagrams trong thư mục này phải được cập nhật đồng bộ với implementation và documentation trong các file markdown tương ứng. 