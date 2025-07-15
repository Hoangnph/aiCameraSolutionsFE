#!/usr/bin/env python3
"""
Create Admin Registration Code Script
Tạo mã đăng ký ADMIN để test hệ thống authentication
"""

import psycopg2
import uuid
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_admin_registration_code():
    """Tạo mã đăng ký ADMIN"""
    
    # Database connection parameters
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'people_counting_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    try:
        # Connect to database
        print("🔌 Đang kết nối đến database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Generate unique registration code
        admin_code = f"ADMIN_{uuid.uuid4().hex[:8].upper()}"
        
        # Set expiration date (30 days from now)
        expires_at = datetime.datetime.now() + datetime.timedelta(days=30)
        
        # Insert registration code
        insert_query = """
        INSERT INTO registration_codes 
        (code, name, description, max_uses, used_count, current_uses, is_active, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        cursor.execute(insert_query, (
            admin_code,
            "Admin Registration Code",
            "Mã đăng ký cho tài khoản ADMIN - Có quyền truy cập đầy đủ hệ thống",
            5,  # max_uses - cho phép tạo 5 tài khoản admin
            0,  # used_count
            0,  # current_uses
            True,  # is_active
            expires_at
        ))
        
        code_id = cursor.fetchone()[0]
        
        # Commit transaction
        conn.commit()
        
        print("✅ Tạo mã đăng ký ADMIN thành công!")
        print("=" * 50)
        print(f"📋 Mã đăng ký: {admin_code}")
        print(f"📝 Tên: Admin Registration Code")
        print(f"📖 Mô tả: Mã đăng ký cho tài khoản ADMIN")
        print(f"🔢 Số lần sử dụng tối đa: 5")
        print(f"⏰ Hết hạn: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 ID: {code_id}")
        print("=" * 50)
        print("💡 Hướng dẫn sử dụng:")
        print("1. Mở trình duyệt và truy cập: http://localhost:3000/vision-ui-dashboard-react")
        print("2. Chuyển đến tab 'Đăng ký'")
        print("3. Điền thông tin tài khoản")
        print(f"4. Nhập mã đăng ký: {admin_code}")
        print("5. Chọn 'Tôi đồng ý với Điều khoản sử dụng'")
        print("6. Nhấn 'Đăng ký'")
        print("=" * 50)
        
        # Verify the code was created
        cursor.execute("SELECT * FROM registration_codes WHERE code = %s", (admin_code,))
        result = cursor.fetchone()
        
        if result:
            print("✅ Xác nhận: Mã đăng ký đã được lưu vào database")
        else:
            print("❌ Lỗi: Mã đăng ký không được lưu vào database")
        
    except psycopg2.Error as e:
        print(f"❌ Lỗi database: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("🔌 Đã đóng kết nối database")

def list_registration_codes():
    """Liệt kê tất cả mã đăng ký hiện có"""
    
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'people_counting_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, code, name, description, max_uses, used_count, current_uses, 
               is_active, expires_at, created_at
        FROM registration_codes
        ORDER BY created_at DESC
        """)
        
        results = cursor.fetchall()
        
        if results:
            print("📋 Danh sách mã đăng ký hiện có:")
            print("=" * 80)
            for row in results:
                print(f"ID: {row[0]}")
                print(f"Mã: {row[1]}")
                print(f"Tên: {row[2]}")
                print(f"Mô tả: {row[3]}")
                print(f"Sử dụng: {row[5]}/{row[4]} (hiện tại: {row[6]})")
                print(f"Trạng thái: {'✅ Hoạt động' if row[7] else '❌ Không hoạt động'}")
                print(f"Hết hạn: {row[8]}")
                print(f"Tạo lúc: {row[9]}")
                print("-" * 40)
        else:
            print("📭 Không có mã đăng ký nào trong database")
            
    except psycopg2.Error as e:
        print(f"❌ Lỗi database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Script tạo mã đăng ký ADMIN")
    print("=" * 50)
    
    # Check if database is accessible
    try:
        import psycopg2
    except ImportError:
        print("❌ Lỗi: Cần cài đặt psycopg2")
        print("💡 Chạy: pip install psycopg2-binary")
        exit(1)
    
    # Create admin registration code
    create_admin_registration_code()
    
    print("\n" + "=" * 50)
    
    # List existing codes
    list_registration_codes()
    
    print("\n🎉 Hoàn thành!") 