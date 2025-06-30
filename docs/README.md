# People Counting Dashboard - System Documentation

## Tổng quan hệ thống

Hệ thống People Counting Dashboard là một ứng dụng web React được thiết kế để quản lý và hiển thị dữ liệu đếm người từ các camera sử dụng AI (SSD - Single Shot Detector) để phát hiện và đếm người ra vào.

## Kiến trúc hệ thống

### Frontend (React + Material-UI)
- **Framework**: React 18.2.0
- **UI Library**: Material-UI (MUI) 5.9.2
- **Routing**: React Router DOM 5.2.0
- **Charts**: ApexCharts 3.30.0
- **State Management**: React Context + Hooks
- **Real-time**: WebSocket connection

### Backend (Python)
- **Framework**: FastAPI
- **AI Model**: SSD (Single Shot Detector)
- **Computer Vision**: OpenCV
- **Database**: PostgreSQL/MySQL
- **Real-time**: WebSocket server

## Cấu trúc thư mục

```
feMain/
├── docs/                          # Tài liệu hệ thống
│   ├── README.md                  # Tài liệu tổng quan
│   ├── architecture.md            # Kiến trúc hệ thống
│   ├── api-specification.md       # Đặc tả API
│   ├── component-structure.md     # Cấu trúc component
│   ├── database-schema.md         # Schema cơ sở dữ liệu
│   └── deployment-guide.md        # Hướng dẫn triển khai
├── src/
│   ├── components/                # React components
│   ├── layouts/                   # Layout components
│   ├── services/                  # API services
│   ├── hooks/                     # Custom hooks
│   └── utils/                     # Utility functions
└── public/                        # Static files
```

## Tính năng chính

### 1. Dashboard
- Hiển thị thống kê thời gian thực
- Grid camera streams
- Quick stats và alerts

### 2. Camera Management
- Quản lý danh sách camera
- Xem camera trực tiếp
- Cài đặt camera

### 3. Analytics & Reports
- Thống kê thời gian thực
- Báo cáo đếm người (People Count)
- Báo cáo giờ cao điểm (Peak Hours)
- Xuất báo cáo (PDF/Excel)

### 4. Alerts
- Thông báo hệ thống
- Lịch sử cảnh báo

### 5. Settings
- Quản lý hồ sơ
- Cài đặt hệ thống
- Cài đặt phát hiện

## Luồng dữ liệu

```
Camera → Backend (AI Processing) → Database → WebSocket → Frontend → Dashboard
```

## Công nghệ sử dụng

- **Frontend**: React, Material-UI, ApexCharts
- **Backend**: Python, FastAPI, OpenCV, SSD Model
- **Database**: PostgreSQL/MySQL
- **Real-time**: WebSocket
- **Deployment**: Docker, Nginx

## Phiên bản

- **Version**: 1.0.0
- **Last Updated**: 2024
- **Status**: Development

## Tài liệu liên quan

- [Kiến trúc hệ thống](./architecture.md)
- [Đặc tả API](./api-specification.md)
- [Cấu trúc Component](./component-structure.md)
- [Schema Database](./database-schema.md)
- [Hướng dẫn triển khai](./deployment-guide.md) 