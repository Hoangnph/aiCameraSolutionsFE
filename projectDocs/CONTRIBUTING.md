# 📝 **CONTRIBUTING TO DOCUMENTATION**

## 🎯 **TỔNG QUAN**

Tài liệu này hướng dẫn cách đóng góp vào documentation của dự án AI Camera Counting System.

---

## 📁 **CẤU TRÚC THƯ MỤC**

### **Quy tắc đặt tên**
- **Thư mục**: Sử dụng format `XX-CATEGORY` (ví dụ: `01-ARCHITECTURE`)
- **File**: Sử dụng lowercase với dấu gạch ngang (ví dụ: `api-overview.md`)
- **README**: Mỗi thư mục chính nên có README.md

### **Cấu trúc chuẩn**
```
projectDocs/
├── 00-OVERVIEW/          # Tổng quan dự án
├── 01-ARCHITECTURE/      # Kiến trúc hệ thống
├── 02-API-DOCUMENTATION/ # Tài liệu API
├── 03-DATABASE/          # Database
├── 04-FRONTEND/          # Frontend
├── 05-BACKEND/           # Backend Services
├── 06-DEPLOYMENT/        # Deployment
├── 07-TESTING/           # Testing
├── 08-MONITORING/        # Monitoring & Observability
├── 09-SECURITY/          # Security
├── 10-PERFORMANCE/       # Performance
├── 11-PROJECT-MANAGEMENT/# Quản lý dự án
├── 12-OPERATIONS/        # Operations
└── templates/            # Templates
```

---

## 📋 **QUY TRÌNH ĐÓNG GÓP**

### **1. Tạo tài liệu mới**

#### **Bước 1: Chọn template phù hợp**
- **Document chung**: Sử dụng `templates/document-template.md`
- **API documentation**: Sử dụng `templates/api-template.md`
- **Test cases**: Sử dụng `templates/test-case-template.md`
- **README**: Sử dụng `templates/readme-template.md`

#### **Bước 2: Đặt tên file**
- Sử dụng lowercase với dấu gạch ngang
- Mô tả rõ nội dung (ví dụ: `user-authentication-guide.md`)
- Tránh tên quá dài hoặc không rõ nghĩa

#### **Bước 3: Đặt vị trí file**
- Chọn thư mục phù hợp với nội dung
- Nếu không chắc chắn, đặt trong thư mục liên quan nhất

### **2. Cập nhật tài liệu hiện có**

#### **Bước 1: Backup**
- Tạo backup trước khi chỉnh sửa
- Commit thay đổi với message rõ ràng

#### **Bước 2: Cập nhật metadata**
- Cập nhật ngày cập nhật
- Cập nhật version nếu cần
- Cập nhật danh sách người đóng góp

#### **Bước 3: Kiểm tra links**
- Đảm bảo tất cả internal links hoạt động
- Cập nhật cross-references nếu cần

### **3. Cập nhật navigation**

#### **Bước 1: Cập nhật README chính**
- Thêm link đến tài liệu mới trong `projectDocs/README.md`
- Đảm bảo link chính xác và hoạt động

#### **Bước 2: Cập nhật cross-references**
- Thêm links từ tài liệu liên quan
- Cập nhật "LIÊN KẾT LIÊN QUAN" section

---

## 📝 **STANDARDS & GUIDELINES**

### **Formatting**

#### **Headers**
- Sử dụng `#` cho title chính
- Sử dụng `##` cho section chính
- Sử dụng `###` cho subsection
- Tối đa 3 levels deep

#### **Lists**
- Sử dụng `-` cho unordered lists
- Sử dụng `1.` cho ordered lists
- Indent properly cho nested lists

#### **Code Blocks**
```markdown
```javascript
// Code example
const example = "Hello World";
```
```

#### **Tables**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

### **Content Guidelines**

#### **Language**
- Sử dụng tiếng Việt cho nội dung chính
- Sử dụng tiếng Anh cho code, commands, technical terms
- Đảm bảo consistency trong terminology

#### **Structure**
- Bắt đầu với overview/tổng quan
- Chia thành sections rõ ràng
- Kết thúc với links liên quan
- Bao gồm metadata (tác giả, ngày cập nhật)

#### **Links**
- Sử dụng relative paths cho internal links
- Đảm bảo tất cả links hoạt động
- Cập nhật links khi di chuyển files

---

## 🔍 **QUALITY CHECKLIST**

### **Trước khi commit**
- [ ] File được đặt đúng thư mục
- [ ] Tên file tuân thủ convention
- [ ] Nội dung được format đúng
- [ ] Tất cả links hoạt động
- [ ] Cross-references được cập nhật
- [ ] Metadata được cập nhật
- [ ] Grammar và spelling được kiểm tra

### **Review checklist**
- [ ] Nội dung chính xác và cập nhật
- [ ] Cấu trúc logic và dễ hiểu
- [ ] Examples và code samples hoạt động
- [ ] Screenshots và diagrams rõ ràng
- [ ] Links và references chính xác

---

## 🚀 **COMMIT MESSAGES**

### **Format chuẩn**
```
docs: [action] [description]

- Chi tiết thay đổi 1
- Chi tiết thay đổi 2
```

### **Examples**
```
docs: add user authentication guide

- Add step-by-step authentication setup
- Include code examples for JWT implementation
- Add troubleshooting section
```

```
docs: update API documentation

- Update endpoint descriptions
- Add new error codes
- Fix broken links
```

---

## 📞 **SUPPORT**

### **Khi cần hỗ trợ**
1. Kiểm tra templates có sẵn
2. Tham khảo tài liệu tương tự
3. Liên hệ team lead hoặc documentation maintainer
4. Tạo issue nếu cần thảo luận

### **Feedback**
- Gửi feedback về documentation structure
- Đề xuất cải thiện templates
- Báo cáo broken links hoặc outdated content

---

## 📅 **MAINTENANCE**

### **Regular reviews**
- Review tài liệu định kỳ (monthly)
- Cập nhật outdated content
- Kiểm tra broken links
- Validate cross-references

### **Version control**
- Sử dụng Git cho version control
- Tag major documentation releases
- Maintain changelog cho significant changes

---

**📝 Last Updated**: [Ngày cập nhật]  
**👥 Maintainer**: [Tên maintainer]  
**📧 Contact**: [Email liên hệ] 