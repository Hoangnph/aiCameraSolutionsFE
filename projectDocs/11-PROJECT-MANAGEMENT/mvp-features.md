# MVP Features - AI Camera Counting System

## 📊 Tổng quan
Tài liệu này định nghĩa chi tiết các MVP features cho hệ thống AI Camera Counting, bao gồm user stories, acceptance criteria, và technical requirements.

## 🎯 MVP Strategy

### Core MVP Features (Phase 1)
Tập trung vào demo cho khách hàng với các tính năng cốt lõi:

1. **Authentication System** - Đăng nhập/đăng ký
2. **Dashboard Overview** - Tổng quan hệ thống
3. **Camera Management** - Quản lý camera cơ bản
4. **Real-time Counting** - Đếm người thời gian thực
5. **Basic Analytics** - Thống kê đơn giản

### Disabled Features (Phase 2+)
- Billing/Payment system
- Advanced analytics
- Complex reporting
- RTL support
- Advanced settings

## 📋 Feature Specifications

### 1. Authentication System

#### 1.1 User Registration
```markdown
## User Story
As a new user, I want to register an account so that I can access the camera counting system.

## Acceptance Criteria
- [ ] User can register with email, password, first name, last name
- [ ] Registration requires a valid registration code
- [ ] Password must meet security requirements (min 8 chars, uppercase, lowercase, number)
- [ ] Email must be unique and valid format
- [ ] User receives confirmation email
- [ ] User is automatically logged in after successful registration

## Technical Requirements
- Frontend: Registration form with validation
- Backend: User creation API with email verification
- Database: Users table with proper constraints
- Security: Password hashing, JWT token generation
```

#### 1.2 User Login
```markdown
## User Story
As a registered user, I want to log in so that I can access my dashboard.

## Acceptance Criteria
- [ ] User can login with email and password
- [ ] Invalid credentials show appropriate error message
- [ ] Successful login redirects to dashboard
- [ ] JWT token is generated and stored
- [ ] Remember me functionality works
- [ ] Failed login attempts are limited

## Technical Requirements
- Frontend: Login form with validation
- Backend: Authentication API with JWT
- Security: Rate limiting, password verification
```

#### 1.3 Password Reset
```markdown
## User Story
As a user, I want to reset my password so that I can regain access if I forget it.

## Acceptance Criteria
- [ ] User can request password reset via email
- [ ] Reset link is sent to registered email
- [ ] Reset link expires after 1 hour
- [ ] User can set new password via reset link
- [ ] Old password is invalidated after reset

## Technical Requirements
- Frontend: Password reset form
- Backend: Password reset API with email service
- Security: Secure token generation, email validation
```

### 2. Dashboard Overview

#### 2.1 System Overview Cards
```markdown
## User Story
As a user, I want to see system overview so that I can quickly understand the current status.

## Acceptance Criteria
- [ ] Display total number of cameras
- [ ] Display number of active cameras
- [ ] Display total people count for today
- [ ] Display system status (online/offline)
- [ ] Cards update in real-time
- [ ] Cards are responsive on mobile devices

## Technical Requirements
- Frontend: Dashboard cards with real-time updates
- Backend: Analytics API for summary data
- WebSocket: Real-time data streaming
- Database: Aggregated count data
```

#### 2.2 Recent Activity Feed
```markdown
## User Story
As a user, I want to see recent activity so that I can monitor system events.

## Acceptance Criteria
- [ ] Display last 10 system events
- [ ] Show camera status changes
- [ ] Show count updates
- [ ] Show user login/logout events
- [ ] Events are timestamped
- [ ] Events are color-coded by type

## Technical Requirements
- Frontend: Activity feed component
- Backend: Activity logging API
- Database: Activity log table
- Real-time: WebSocket updates
```

#### 2.3 Quick Stats
```markdown
## User Story
As a user, I want to see quick statistics so that I can understand usage patterns.

## Acceptance Criteria
- [ ] Display peak hour of the day
- [ ] Display total people in/out today
- [ ] Display average count per hour
- [ ] Display system uptime percentage
- [ ] Stats are calculated for last 24 hours
- [ ] Stats update every 5 minutes

## Technical Requirements
- Frontend: Stats display component
- Backend: Statistics calculation API
- Database: Time-series data aggregation
- Caching: Redis for performance
```

### 3. Camera Management

#### 3.1 Camera List View
```markdown
## User Story
As a user, I want to see all cameras so that I can manage them effectively.

## Acceptance Criteria
- [ ] Display list of all cameras
- [ ] Show camera name, location, status
- [ ] Show current count for each camera
- [ ] Allow filtering by status (active/inactive)
- [ ] Allow searching by name/location
- [ ] Pagination for large lists (20 per page)
- [ ] Responsive grid layout

## Technical Requirements
- Frontend: Camera list component with filters
- Backend: Camera list API with pagination
- Database: Cameras table with status tracking
- Real-time: Status updates via WebSocket
```

#### 3.2 Add New Camera
```markdown
## User Story
As an admin user, I want to add new cameras so that I can expand the system.

## Acceptance Criteria
- [ ] Form for camera details (name, location, stream URL)
- [ ] Validation for required fields
- [ ] Stream URL format validation (RTSP)
- [ ] Camera is created with 'offline' status
- [ ] Success message after creation
- [ ] Redirect to camera list after creation

## Technical Requirements
- Frontend: Camera creation form
- Backend: Camera creation API
- Database: Camera record creation
- Validation: Input sanitization and validation
```

#### 3.3 Edit Camera
```markdown
## User Story
As an admin user, I want to edit camera details so that I can update information.

## Acceptance Criteria
- [ ] Pre-populated form with current data
- [ ] Allow editing name, location, stream URL
- [ ] Validation for all fields
- [ ] Success message after update
- [ ] Cancel button returns to list
- [ ] Changes are reflected immediately

## Technical Requirements
- Frontend: Camera edit form
- Backend: Camera update API
- Database: Camera record update
- Validation: Field validation and sanitization
```

#### 3.4 Delete Camera
```markdown
## User Story
As an admin user, I want to delete cameras so that I can remove unused ones.

## Acceptance Criteria
- [ ] Confirmation dialog before deletion
- [ ] Show warning about data loss
- [ ] Delete camera and all associated data
- [ ] Success message after deletion
- [ ] Remove from camera list
- [ ] Update total camera count

## Technical Requirements
- Frontend: Delete confirmation dialog
- Backend: Camera deletion API
- Database: Cascade delete related data
- Cleanup: Remove associated count data
```

### 4. Real-time Counting

#### 4.1 Live Camera Stream
```markdown
## User Story
As a user, I want to view live camera streams so that I can monitor activity in real-time.

## Acceptance Criteria
- [ ] Display live video stream from camera
- [ ] Stream quality is adjustable (720p/480p)
- [ ] Stream loads within 3 seconds
- [ ] Stream is stable and responsive
- [ ] Fallback image if stream fails
- [ ] Stream controls (play/pause/refresh)

## Technical Requirements
- Frontend: Video player component
- Backend: Stream proxy service
- WebSocket: Real-time stream management
- Fallback: Static image when stream unavailable
```

#### 4.2 Real-time Count Display
```markdown
## User Story
As a user, I want to see real-time count updates so that I can monitor current activity.

## Acceptance Criteria
- [ ] Display current count prominently
- [ ] Show people in/out counts
- [ ] Show confidence score (0-100%)
- [ ] Updates every 2-3 seconds
- [ ] Visual indicators for count changes
- [ ] Historical trend line (last 10 minutes)

## Technical Requirements
- Frontend: Count display component
- Backend: Real-time count API
- WebSocket: Live count updates
- Database: Time-series count storage
```

#### 4.3 Count Accuracy Validation
```markdown
## User Story
As a user, I want to trust the count accuracy so that I can rely on the data.

## Acceptance Criteria
- [ ] Display confidence score for each count
- [ ] Highlight low confidence counts (<70%)
- [ ] Show count history for verification
- [ ] Allow manual count adjustment (admin only)
- [ ] Track count accuracy over time
- [ ] Alert on unusual count patterns

## Technical Requirements
- Frontend: Confidence indicators
- Backend: Accuracy validation API
- AI Model: Confidence scoring
- Database: Accuracy tracking
```

### 5. Basic Analytics

#### 5.1 Daily Summary
```markdown
## User Story
As a user, I want to see daily summaries so that I can understand daily patterns.

## Acceptance Criteria
- [ ] Display total people in/out for today
- [ ] Show peak hours (top 3)
- [ ] Show average count per hour
- [ ] Compare with previous day
- [ ] Export data to CSV
- [ ] Print-friendly format

## Technical Requirements
- Frontend: Daily summary dashboard
- Backend: Daily analytics API
- Database: Daily aggregation queries
- Export: CSV generation service
```

#### 5.2 Hourly Chart
```markdown
## User Story
As a user, I want to see hourly patterns so that I can identify busy periods.

## Acceptance Criteria
- [ ] Display 24-hour chart
- [ ] Show people in/out by hour
- [ ] Highlight peak hours
- [ ] Allow date selection
- [ ] Interactive chart with tooltips
- [ ] Responsive chart design

## Technical Requirements
- Frontend: Chart component (Chart.js/ApexCharts)
- Backend: Hourly data API
- Database: Hourly aggregation
- Caching: Redis for chart data
```

#### 5.3 Camera Comparison
```markdown
## User Story
As a user, I want to compare cameras so that I can understand usage differences.

## Acceptance Criteria
- [ ] Compare 2-4 cameras side by side
- [ ] Show count totals for each camera
- [ ] Show peak hours for each camera
- [ ] Allow date range selection
- [ ] Export comparison data
- [ ] Visual comparison charts

## Technical Requirements
- Frontend: Comparison component
- Backend: Multi-camera analytics API
- Database: Cross-camera aggregation
- Charts: Comparison visualization
```

## 🎨 UI/UX Requirements

### 1. Design System
```markdown
## Color Palette
- Primary: #4318FF (Blue)
- Secondary: #A0AEC0 (Gray)
- Success: #48BB78 (Green)
- Warning: #ED8936 (Orange)
- Error: #F56565 (Red)
- Background: #F7FAFC (Light Gray)

## Typography
- Font Family: Inter, sans-serif
- Headings: 24px, 20px, 18px, 16px
- Body: 14px
- Caption: 12px

## Components
- Cards: Rounded corners, subtle shadows
- Buttons: Consistent styling, hover effects
- Forms: Clear labels, validation states
- Tables: Clean layout, sortable columns
```

### 2. Responsive Design
```markdown
## Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Mobile Requirements
- Touch-friendly buttons (min 44px)
- Swipe gestures for navigation
- Optimized for portrait orientation
- Reduced data usage for streams

## Desktop Requirements
- Full feature access
- Multi-column layouts
- Keyboard shortcuts
- Large screen optimization
```

### 3. Accessibility
```markdown
## WCAG 2.1 AA Compliance
- Color contrast ratio > 4.5:1
- Keyboard navigation support
- Screen reader compatibility
- Focus indicators
- Alt text for images
- Semantic HTML structure
```

## 🔧 Technical Requirements

### 1. Performance Standards
```markdown
## Response Times
- Page load: < 3 seconds
- API responses: < 200ms
- Real-time updates: < 2 seconds
- Image loading: < 1 second

## Scalability
- Support 100 concurrent users
- Handle 1000+ cameras
- Process 10,000+ count events/day
- 99.5% uptime requirement
```

### 2. Security Requirements
```markdown
## Authentication
- JWT tokens with refresh
- Password complexity requirements
- Rate limiting on auth endpoints
- Session timeout (8 hours)

## Authorization
- Role-based access control
- API endpoint protection
- Data access permissions
- Admin privilege validation

## Data Protection
- HTTPS encryption
- Input validation and sanitization
- SQL injection prevention
- XSS protection
```

### 3. Data Requirements
```markdown
## Data Retention
- Count data: 1 year
- User logs: 6 months
- System logs: 3 months
- Backup retention: 30 days

## Data Accuracy
- Count accuracy: > 90%
- Confidence threshold: > 70%
- Real-time latency: < 3 seconds
- Data consistency: ACID compliance
```

## 📊 Success Metrics

### 1. User Experience Metrics
```markdown
## Engagement
- Daily active users: > 80%
- Session duration: > 10 minutes
- Feature adoption: > 70%
- User satisfaction: > 4.0/5.0

## Performance
- Page load time: < 3 seconds
- API response time: < 200ms
- Error rate: < 1%
- Uptime: > 99.5%
```

### 2. Business Metrics
```markdown
## Usage
- Cameras monitored: > 10
- Daily count events: > 1000
- User registrations: > 50
- System uptime: > 99.5%

## Quality
- Count accuracy: > 90%
- False positives: < 5%
- System reliability: > 99%
- User retention: > 80%
```

## 🚀 Implementation Phases

### Phase 1: Core MVP (Weeks 1-4)
1. **Week 1**: Authentication system
2. **Week 2**: Basic dashboard and camera management
3. **Week 3**: Real-time counting and stream display
4. **Week 4**: Basic analytics and testing

### Phase 2: Enhancement (Weeks 5-8)
1. **Week 5**: Advanced analytics and reporting
2. **Week 6**: Performance optimization
3. **Week 7**: Security hardening
4. **Week 8**: User acceptance testing

### Phase 3: Production (Weeks 9-12)
1. **Week 9**: Production deployment
2. **Week 10**: Monitoring and alerting
3. **Week 11**: Documentation and training
4. **Week 12**: Go-live and support

---

**Last Updated**: 2025-07-03  
**Version**: 1.0.0  
**Status**: Ready for Implementation 