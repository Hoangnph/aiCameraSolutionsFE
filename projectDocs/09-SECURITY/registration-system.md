# Registration Code System - Hệ thống quản lý mã đăng ký

## Tổng quan

Hệ thống quản lý mã đăng ký cho phép admin tạo và quản lý các mã đăng ký để kiểm soát việc đăng ký tài khoản mới. Mỗi user khi đăng ký phải cung cấp một mã đăng ký hợp lệ.

## Mục đích

- **Kiểm soát đăng ký**: Chỉ những người có mã đăng ký mới có thể tạo tài khoản
- **Phân loại tổ chức**: Mã đăng ký có thể được phân loại theo doanh nghiệp, phòng ban
- **Giới hạn sử dụng**: Có thể thiết lập giới hạn số lần sử dụng cho mỗi mã
- **Quản lý thời gian**: Mã có thể có thời hạn sử dụng

## Cấu trúc dữ liệu

### Registration Codes Table

```sql
CREATE TABLE registration_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(20) DEFAULT 'organization' CHECK (type IN ('organization', 'department', 'general')),
    max_uses INTEGER DEFAULT NULL,
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP DEFAULT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Users Table (Updated)

```sql
-- Thêm trường registration_code_id vào bảng users
ALTER TABLE users ADD COLUMN registration_code_id INTEGER REFERENCES registration_codes(id);
```

## Các loại mã đăng ký

### 1. Organization Code
- **Mục đích**: Mã dành cho toàn bộ doanh nghiệp
- **Ví dụ**: "company123", "enterprise2024"
- **Sử dụng**: Thường không giới hạn số lần sử dụng

### 2. Department Code
- **Mục đích**: Mã dành cho phòng ban cụ thể
- **Ví dụ**: "hr2024", "it_dept", "sales_team"
- **Sử dụng**: Có thể giới hạn số lần sử dụng

### 3. General Code
- **Mục đích**: Mã chung cho các trường hợp khác
- **Ví dụ**: "public_access", "trial_code"
- **Sử dụng**: Linh hoạt theo nhu cầu

## Quy trình hoạt động

### 1. Tạo mã đăng ký (Admin)
```javascript
// Admin tạo mã mới
POST /api/v1/users/registration-codes
{
  "code": "hr2024",
  "name": "HR Department 2024",
  "description": "Mã đăng ký cho phòng Nhân sự",
  "type": "department",
  "maxUses": 10,
  "expiresAt": "2024-12-31T23:59:59Z"
}
```

### 2. Đăng ký tài khoản (User)
```javascript
// User đăng ký với mã
POST /api/v1/auth/register
{
  "username": "newuser",
  "email": "user@company.com",
  "password": "Password123!",
  "confirmPassword": "Password123!",
  "firstName": "John",
  "lastName": "Doe",
  "registrationCode": "hr2024"
}
```

### 3. Validation Process
1. **Kiểm tra mã tồn tại**: Mã phải có trong database
2. **Kiểm tra trạng thái**: Mã phải đang active (`is_active = true`)
3. **Kiểm tra thời hạn**: Mã chưa hết hạn (`expires_at > now()`)
4. **Kiểm tra giới hạn**: Chưa đạt giới hạn sử dụng (`used_count < max_uses`)
5. **Tăng số lượt sử dụng**: `used_count += 1`

## API Endpoints

### Quản lý mã đăng ký (Admin Only)

#### 1. Lấy danh sách mã đăng ký
```http
GET /api/v1/users/registration-codes?page=1&limit=10&search=hr&type=department&isActive=true
Authorization: Bearer <admin_token>
```

#### 2. Lấy chi tiết mã đăng ký
```http
GET /api/v1/users/registration-codes/:id
Authorization: Bearer <admin_token>
```

#### 3. Tạo mã đăng ký mới
```http
POST /api/v1/users/registration-codes
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "code": "string",
  "name": "string",
  "description": "string",
  "type": "organization|department|general",
  "maxUses": 10,
  "expiresAt": "2024-12-31T23:59:59Z"
}
```

#### 4. Cập nhật mã đăng ký
```http
PUT /api/v1/users/registration-codes/:id
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description",
  "type": "department",
  "maxUses": 5,
  "isActive": false,
  "expiresAt": "2024-12-31T23:59:59Z"
}
```

#### 5. Xóa mã đăng ký
```http
DELETE /api/v1/users/registration-codes/:id
Authorization: Bearer <admin_token>
```

**Lưu ý**: Chỉ có thể xóa mã chưa được sử dụng (`used_count = 0`)

## Validation Rules

### Khi tạo mã đăng ký
- `code`: Bắt buộc, duy nhất, 1-50 ký tự
- `name`: Bắt buộc, 1-100 ký tự
- `description`: Tùy chọn
- `type`: Tùy chọn, mặc định "organization"
- `maxUses`: Tùy chọn, số nguyên (null = không giới hạn)
- `expiresAt`: Tùy chọn, ISO date string (null = không hết hạn)

### Khi đăng ký tài khoản
- `registrationCode`: Bắt buộc, phải là mã hợp lệ
- Mã phải tồn tại trong database
- Mã phải đang active
- Mã chưa hết hạn
- Mã chưa đạt giới hạn sử dụng

## Error Messages

### Mã đăng ký không hợp lệ
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Mã đăng ký không hợp lệ"
  }
}
```

### Mã đăng ký đã bị vô hiệu hóa
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Mã đăng ký đã bị vô hiệu hóa"
  }
}
```

### Mã đăng ký đã hết hạn
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Mã đăng ký đã hết hạn"
  }
}
```

### Mã đăng ký đã đạt giới hạn sử dụng
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Mã đăng ký đã đạt giới hạn sử dụng"
  }
}
```

## Best Practices

### 1. Đặt tên mã
- Sử dụng tên có ý nghĩa: "hr_2024", "it_department", "sales_team"
- Tránh tên quá ngắn hoặc dễ đoán: "123", "abc", "test"

### 2. Giới hạn sử dụng
- **Organization codes**: Thường không giới hạn
- **Department codes**: Giới hạn theo số lượng nhân viên dự kiến
- **General codes**: Giới hạn thấp cho mục đích thử nghiệm

### 3. Thời hạn sử dụng
- Đặt thời hạn hợp lý cho từng loại mã
- Regular review và update các mã hết hạn
- Tạo mã mới thay vì gia hạn mã cũ

### 4. Monitoring
- Theo dõi số lượt sử dụng của mỗi mã
- Alert khi mã gần đạt giới hạn
- Log tất cả hoạt động tạo/sử dụng mã

## Migration và Seed Data

### Migration
```bash
# Chạy migration để tạo bảng và thêm trường
npm run migrate
```

### Seed Data
```bash
# Tạo mã mặc định "adminfe" và gán cho tất cả user hiện có
npm run seed
```

### Mã mặc định
- **Code**: "adminfe"
- **Name**: "Admin Future Eyes"
- **Description**: "Mã đăng ký mặc định cho hệ thống Future Eyes"
- **Type**: "organization"
- **Max Uses**: Không giới hạn
- **Status**: Active

## Security Considerations

### 1. Access Control
- Chỉ admin mới có thể quản lý mã đăng ký
- User thường chỉ có thể sử dụng mã để đăng ký

### 2. Code Generation
- Mã được tạo thủ công bởi admin
- Không có auto-generation để tránh brute force

### 3. Audit Trail
- Log tất cả hoạt động tạo, cập nhật, xóa mã
- Track người tạo và thời gian tạo

### 4. Rate Limiting
- Giới hạn số lần thử đăng ký với mã không hợp lệ
- Prevent brute force attacks

## Troubleshooting

### Mã không hoạt động
1. Kiểm tra mã có tồn tại trong database
2. Kiểm tra trạng thái `is_active`
3. Kiểm tra thời hạn `expires_at`
4. Kiểm tra giới hạn sử dụng `used_count < max_uses`

### Không thể xóa mã
- Chỉ có thể xóa mã chưa được sử dụng (`used_count = 0`)
- Thay vì xóa, có thể set `is_active = false`

### Performance Issues
- Đảm bảo có index trên `code`, `type`, `is_active`
- Monitor query performance với large datasets

## Future Enhancements

### 1. Auto-generation
- Tự động tạo mã theo pattern
- Bulk generation cho nhiều phòng ban

### 2. Analytics
- Dashboard hiển thị thống kê sử dụng mã
- Reports về hiệu quả của từng mã

### 3. Integration
- Integration với LDAP/Active Directory
- Single Sign-On (SSO) support

### 4. Advanced Features
- Mã có thể sử dụng nhiều lần cho cùng một user
- Temporary codes với thời hạn ngắn
- Code sharing giữa các admin 