# Authentication Integration Guide

## Tổng quan

Đã tích hợp thành công authentication microservice vào frontend React với các tính năng:

- ✅ Đăng nhập/Đăng ký với backend API
- ✅ JWT token management (access + refresh)
- ✅ Protected routes
- ✅ User profile display
- ✅ Logout functionality
- ✅ Loading states
- ✅ Error handling

## Cấu trúc đã tạo

### 1. Authentication Context (`src/context/AuthContext.js`)
- Quản lý trạng thái authentication toàn cục
- Xử lý login, register, logout
- Token management và auto-refresh
- Loading states

### 2. API Service (`src/services/authAPI.js`)
- Giao tiếp với backend authentication API
- Auto token refresh khi 401
- Error handling
- Request/response interceptors

### 3. Protected Route (`src/components/ProtectedRoute.js`)
- Bảo vệ các route cần authentication
- Redirect to login nếu chưa đăng nhập
- Loading state khi check auth

### 4. Updated Components
- **Sign In** (`src/layouts/authentication/sign-in/index.js`)
- **Sign Up** (`src/layouts/authentication/sign-up/index.js`)
- **Dashboard Navbar** (`src/examples/Navbars/DashboardNavbar/index.js`)
- **App.js** - Main routing với authentication

### 5. Loading Spinner (`src/components/LoadingSpinner.js`)
- Component hiển thị loading state
- Reusable cho toàn bộ app

## Setup Instructions

### 1. Backend Setup
```bash
cd beAuth
npm install
cp env.example .env
# Chỉnh sửa .env với thông tin database
npm run migrate
npm run seed
npm run dev
```

### 2. Frontend Setup
```bash
# Tạo file .env trong thư mục gốc
echo "REACT_APP_API_URL=http://localhost:3001/api/v1" > .env

# Cài đặt dependencies (nếu cần)
npm install

# Khởi chạy frontend
npm start
```

### 3. Environment Variables
Tạo file `.env` trong thư mục gốc:
```env
REACT_APP_API_URL=http://localhost:3001/api/v1
```

## Cách sử dụng

### 1. Đăng ký tài khoản mới
- Truy cập `/authentication/sign-up`
- Điền thông tin: First Name, Last Name, Username, Email, Password
- Password phải đáp ứng yêu cầu: 8+ ký tự, có chữ hoa, chữ thường, số, ký tự đặc biệt
- Click "SIGN UP"

### 2. Đăng nhập
- Truy cập `/authentication/sign-in` (màn hình chính)
- Nhập Username/Email và Password
- Click "SIGN IN"
- Sau khi đăng nhập thành công sẽ redirect đến `/dashboard`

### 3. Sử dụng hệ thống
- Tất cả các trang (trừ sign-in và sign-up) đều được bảo vệ
- User info hiển thị trên navbar
- Có thể logout từ menu user
- Token tự động refresh khi hết hạn

### 4. Tài khoản mặc định
Sau khi chạy seed, có thể sử dụng:
- **Admin**: `admin` / `Admin123!`
- **Test User**: `testuser` / `Test123!`
- **Viewer**: `viewer` / `Viewer123!`

## API Endpoints được sử dụng

### Authentication
- `POST /api/v1/auth/login` - Đăng nhập
- `POST /api/v1/auth/register` - Đăng ký
- `POST /api/v1/auth/logout` - Đăng xuất
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Lấy thông tin user hiện tại

### User Management
- `PUT /api/v1/users/profile` - Cập nhật profile
- `PUT /api/v1/users/change-password` - Đổi mật khẩu

## Security Features

### Frontend
- ✅ JWT token storage trong localStorage
- ✅ Auto token refresh
- ✅ Protected routes
- ✅ Input validation
- ✅ Error handling
- ✅ Loading states

### Backend Integration
- ✅ bcrypt password hashing
- ✅ JWT token signing
- ✅ Rate limiting
- ✅ CORS protection
- ✅ Input validation với Joi
- ✅ SQL injection prevention

## Troubleshooting

### Common Issues

1. **CORS Error**
   - Đảm bảo beAuth đang chạy trên port 3001
   - Kiểm tra CORS_ORIGIN trong beAuth .env
   - Frontend phải chạy trên port 3000

2. **Database Connection Error**
   - Kiểm tra PostgreSQL đang chạy
   - Kiểm tra thông tin database trong beAuth .env
   - Chạy `npm run migrate` và `npm run seed`

3. **Token Expired**
   - Token access tự động refresh
   - Nếu refresh fail, redirect to login
   - Kiểm tra JWT_SECRET trong beAuth

4. **Validation Errors**
   - Password phải đáp ứng yêu cầu
   - Email format phải hợp lệ
   - Username phải unique

### Debug Mode
Để debug, mở browser DevTools:
- Network tab: Xem API calls
- Console tab: Xem errors
- Application tab: Xem localStorage tokens

## Next Steps

### Immediate
1. Test tất cả flows: register, login, logout
2. Test protected routes
3. Test token refresh
4. Test error handling

### Future Enhancements
1. Email verification
2. Password reset flow
3. Remember me functionality
4. Social login (Google, Facebook)
5. Two-factor authentication
6. User roles và permissions
7. Session management với Redis
8. API documentation với Swagger

## File Structure

```
src/
├── context/
│   └── AuthContext.js          # Authentication context
├── services/
│   └── authAPI.js              # API service
├── components/
│   ├── ProtectedRoute.js       # Protected route wrapper
│   └── LoadingSpinner.js       # Loading component
├── layouts/authentication/
│   ├── sign-in/index.js        # Updated sign in
│   └── sign-up/index.js        # Updated sign up
├── examples/Navbars/
│   └── DashboardNavbar/index.js # Updated navbar
└── App.js                      # Updated main app
```

## Conclusion

Authentication system đã được tích hợp hoàn chỉnh với:
- ✅ Full authentication flow
- ✅ Secure token management
- ✅ Protected routes
- ✅ User interface
- ✅ Error handling
- ✅ Loading states

System sẵn sàng để sử dụng và có thể mở rộng thêm các tính năng khác. 