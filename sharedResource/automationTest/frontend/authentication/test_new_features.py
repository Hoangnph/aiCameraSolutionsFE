#!/usr/bin/env python3
"""
Simple test for new authentication features
- Reset Password button in profile page
- Forgot Password link in sign-up page
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestNewFeatures(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
    def tearDown(self):
        if self.driver:
            self.driver.quit()
    
    def test_forgot_password_link_in_signin(self):
        """Test that forgot password link exists in sign-in page and navigates correctly"""
        try:
            # Navigate to sign-in page
            self.driver.get("http://localhost:3000/authentication/sign-in")
            time.sleep(2)
            
            # Check if forgot password link exists
            forgot_password_link = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quên mật khẩu')]"))
            )
            
            # Verify link text
            self.assertIn("Quên mật khẩu", forgot_password_link.text)
            
            # Click on forgot password link
            forgot_password_link.click()
            time.sleep(2)
            
            # Verify navigation to forgot password page
            current_url = self.driver.current_url
            self.assertIn("/authentication/forgot-password", current_url)
            
            # Check if forgot password form is displayed
            title = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Quên mật khẩu')]"))
            )
            self.assertIn("Quên mật khẩu", title.text)
            
            # Check if email input field exists
            email_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            self.assertTrue(email_input.is_displayed())
            
            # Check if submit button exists
            submit_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'GỬI LINK ĐẶT LẠI MẬT KHẨU')]"))
            )
            self.assertTrue(submit_button.is_displayed())
            
            print("✅ Forgot password link test passed")
            
        except Exception as e:
            print(f"❌ Forgot password link test failed: {str(e)}")
            raise
    
    def test_forgot_password_form_submission(self):
        """Test forgot password form submission with valid email"""
        try:
            # Navigate to forgot password page
            self.driver.get("http://localhost:3000/authentication/forgot-password")
            time.sleep(2)
            
            # Find email input and submit button
            email_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            submit_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'GỬI LINK ĐẶT LẠI MẬT KHẨU')]"))
            )
            
            # Enter valid email
            email_input.clear()
            email_input.send_keys("test@example.com")
            
            # Submit form
            submit_button.click()
            time.sleep(3)
            
            # Check for success message
            success_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'link đặt lại mật khẩu đã được gửi')]"))
            )
            self.assertIn("link đặt lại mật khẩu đã được gửi", success_message.text)
            
            print("✅ Forgot password form submission test passed")
            
        except Exception as e:
            print(f"❌ Forgot password form submission test failed: {str(e)}")
            raise
    
    def test_forgot_password_form_validation(self):
        """Test forgot password form validation with invalid email"""
        try:
            # Navigate to forgot password page
            self.driver.get("http://localhost:3000/authentication/forgot-password")
            time.sleep(2)
            
            # Find email input and submit button
            email_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            submit_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'GỬI LINK ĐẶT LẠI MẬT KHẨU')]"))
            )
            
            # Enter invalid email
            email_input.clear()
            email_input.send_keys("invalid-email")
            
            # Submit form
            submit_button.click()
            time.sleep(2)
            
            # Check for validation error
            error_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email không hợp lệ')]"))
            )
            self.assertIn("Email không hợp lệ", error_message.text)
            
            print("✅ Forgot password form validation test passed")
            
        except Exception as e:
            print(f"❌ Forgot password form validation test failed: {str(e)}")
            raise
    
    def test_forgot_password_navigation_links(self):
        """Test navigation links in forgot password page"""
        try:
            # Navigate to forgot password page
            self.driver.get("http://localhost:3000/authentication/forgot-password")
            time.sleep(2)
            
            # Test "Đăng nhập" link
            signin_link = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Đăng nhập')]"))
            )
            signin_link.click()
            time.sleep(2)
            
            # Verify navigation to sign-in page
            current_url = self.driver.current_url
            self.assertIn("/authentication/sign-in", current_url)
            
            # Navigate back to forgot password page
            self.driver.get("http://localhost:3000/authentication/forgot-password")
            time.sleep(2)
            
            # Test "Đăng ký" link
            signup_link = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Đăng ký')]"))
            )
            signup_link.click()
            time.sleep(2)
            
            # Verify navigation to sign-up page
            current_url = self.driver.current_url
            self.assertIn("/authentication/sign-up", current_url)
            
            print("✅ Forgot password navigation links test passed")
            
        except Exception as e:
            print(f"❌ Forgot password navigation links test failed: {str(e)}")
            raise

if __name__ == "__main__":
    unittest.main() 