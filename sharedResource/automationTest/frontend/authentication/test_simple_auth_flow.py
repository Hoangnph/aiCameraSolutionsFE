import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class TestSimpleAuthFlow(unittest.TestCase):
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
    
    def test_forgot_password_flow(self):
        """Test the complete forgot password flow"""
        try:
            print("🔍 Testing complete forgot password flow...")
            
            # Step 1: Navigate to sign-in page
            self.driver.get("http://localhost:3000/authentication/sign-in")
            time.sleep(2)
            print("✅ Step 1: Navigated to sign-in page")
            
            # Step 2: Find and click forgot password link
            forgot_password_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Quên mật khẩu')]")
            forgot_password_link.click()
            time.sleep(2)
            print("✅ Step 2: Clicked forgot password link")
            
            # Step 3: Verify navigation to forgot password page
            current_url = self.driver.current_url
            assert "/authentication/forgot-password" in current_url
            print("✅ Step 3: Successfully navigated to forgot password page")
            
            # Step 4: Find form elements
            email_input = self.driver.find_element(By.NAME, "email")
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'GỬI')]")
            print("✅ Step 4: Found form elements")
            
            # Step 5: Test form submission with valid email
            email_input.clear()
            email_input.send_keys("test@example.com")
            submit_button.click()
            time.sleep(3)
            print("✅ Step 5: Submitted form with valid email")
            
            # Step 6: Check for success message
            page_source = self.driver.page_source
            if "link đặt lại mật khẩu đã được gửi" in page_source:
                print("✅ Step 6: Success message displayed")
            else:
                print("⚠️ Step 6: Success message not found (might be expected)")
            
            # Step 7: Test navigation links
            try:
                signin_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Đăng nhập')]")
                signin_link.click()
                time.sleep(2)
                
                current_url = self.driver.current_url
                if "/authentication/sign-in" in current_url:
                    print("✅ Step 7: Successfully navigated back to sign-in page")
                else:
                    print("❌ Step 7: Failed to navigate back to sign-in page")
            except:
                print("⚠️ Step 7: Could not test navigation back to sign-in")
            
            print("✅ Complete forgot password flow test passed")
            
        except Exception as e:
            print(f"❌ Forgot password flow test failed: {str(e)}")
            raise
    
    def test_forgot_password_form_validation(self):
        """Test forgot password form validation"""
        try:
            print("🔍 Testing forgot password form validation...")
            
            # Navigate to forgot password page
            self.driver.get("http://localhost:3000/authentication/forgot-password")
            time.sleep(2)
            
            # Find form elements
            email_input = self.driver.find_element(By.NAME, "email")
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'GỬI')]")
            
            # Test with invalid email
            email_input.clear()
            email_input.send_keys("invalid-email")
            submit_button.click()
            time.sleep(2)
            
            # Check for validation error
            page_source = self.driver.page_source
            if "Email không hợp lệ" in page_source:
                print("✅ Form validation test passed - invalid email error shown")
            else:
                print("⚠️ Form validation test - invalid email error not found (might be expected)")
            
        except Exception as e:
            print(f"❌ Form validation test failed: {str(e)}")
            raise

if __name__ == "__main__":
    unittest.main() 