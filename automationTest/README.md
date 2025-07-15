# AI Camera Counting System - Automation Test README

## Đã fix các lỗi backend camera API:

### 1. Lỗi update camera trả về 500
- Đã thêm validate dữ liệu đầu vào (bắt buộc name, kiểm tra status hợp lệ).
- Update động chỉ các trường được truyền vào, trả về lỗi 400 nếu không có trường hợp hợp lệ.
- Bắt lỗi database rõ ràng, rollback transaction nếu có lỗi.

### 2. Lỗi đăng ký camera với dữ liệu không hợp lệ trả về 500
- Đã thêm validate cho name (bắt buộc), ip_address (đúng định dạng), rtsp_url (bắt đầu bằng rtsp/http/https), status (chỉ nhận giá trị hợp lệ).
- Bắt lỗi integrity (trùng tên) trả về 409, lỗi dữ liệu trả về 400.

### 3. Lỗi truy cập không token trả về 403 thay vì 401
- Đã thêm custom exception handler, nếu lỗi 403 và message "Not authenticated" thì trả về 401.

## Hướng dẫn test lại các case liên quan

### Đăng ký camera (POST /api/v1/cameras)
- Truyền thiếu name hoặc name rỗng: trả về 400.
- Truyền ip_address sai định dạng: trả về 400.
- Truyền rtsp_url sai định dạng: trả về 400.
- Trùng tên camera: trả về 409.
- Đăng ký hợp lệ: trả về 200, có data camera.

### Update camera (PUT /api/v1/cameras/{id})
- Truyền thiếu name hoặc name rỗng: trả về 400.
- Truyền status không hợp lệ: trả về 400.
- Update hợp lệ: trả về 200, có data camera.

### Truy cập endpoint cần xác thực không có token
- Trả về 401 (Not authenticated).

## Đã cập nhật code và restart service. Chạy lại automation test suite để xác nhận các lỗi đã được fix hoàn toàn. 