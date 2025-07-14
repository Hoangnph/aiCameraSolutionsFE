# beCamera - Fix Test Results Log

## Các lỗi đã fix:

### 1. Update camera trả về 500
- Nguyên nhân: Không validate dữ liệu đầu vào, truyền thiếu trường hoặc giá trị không hợp lệ gây lỗi database.
- Đã fix: Thêm validate bắt buộc trường name, kiểm tra hợp lệ cho status, update động các trường, rollback transaction nếu lỗi.
- Đã test lại: Pass.

### 2. Đăng ký camera với dữ liệu không hợp lệ trả về 500
- Nguyên nhân: Không validate dữ liệu đầu vào, không kiểm tra định dạng IP, URL, status.
- Đã fix: Thêm validate cho name, ip_address, rtsp_url, status. Bắt lỗi integrity (trùng tên) trả về 409, lỗi dữ liệu trả về 400.
- Đã test lại: Pass.

### 3. Truy cập không token trả về 403 thay vì 401
- Nguyên nhân: FastAPI mặc định trả về 403 khi thiếu token.
- Đã fix: Thêm custom exception handler, nếu lỗi 403 và message "Not authenticated" thì trả về 401.
- Đã test lại: Pass.

## Kết luận
- Các lỗi trên đã được fix và xác nhận pass qua automation test/manual test.
- Sẵn sàng chuyển sang test case mới. 