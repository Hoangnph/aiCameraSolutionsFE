# [API Name] - API Documentation Template

## 📊 **TỔNG QUAN**

**API Name**: [Tên API]  
**Base URL**: [Base URL]  
**Version**: [Version]  
**Authentication**: [Loại authentication]  
**Cập nhật lần cuối**: [Ngày cập nhật]  

---

## 🎯 **MỤC TIÊU**

- [Mục tiêu 1]
- [Mục tiêu 2]
- [Mục tiêu 3]

---

## 🔌 **ENDPOINTS**

### 1. [Endpoint Name]

#### **Request**
```http
[HTTP_METHOD] [ENDPOINT_PATH]
```

#### **Headers**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer [token]"
}
```

#### **Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | Yes | Description |
| param2 | number | No | Description |

#### **Request Body**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

#### **Response**
```json
{
  "status": "success",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

#### **Error Response**
```json
{
  "status": "error",
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

---

## 🔗 **LIÊN KẾT LIÊN QUAN**

- [API Overview](../02-API-DOCUMENTATION/api-overview.md)
- [Authentication Guide](../02-API-DOCUMENTATION/auth-integration-guide.md)
- [Error Handling](../05-BACKEND/error-handling.md)

---

## 📝 **GHI CHÚ**

[Ghi chú bổ sung nếu cần]

---

## 👥 **NGƯỜI ĐÓNG GÓP**

- **Tác giả**: [Tên tác giả]
- **Reviewer**: [Tên reviewer]
- **Ngày tạo**: [Ngày tạo]
- **Ngày cập nhật**: [Ngày cập nhật] 