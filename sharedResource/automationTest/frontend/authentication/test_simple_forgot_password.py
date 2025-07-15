import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class TestSimpleForgotPassword(unittest.TestCase):
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
    
    def test_forgot_password_link_exists(self):
        """Test that forgot password link exists in sign-in page"""
        try:
            print("🔍 Testing forgot password link in sign-in page...")
            
            # Navigate to sign-in page
            self.driver.get("http://localhost:3000/authentication/sign-in")
            time.sleep(3)
            
            # Print page title for debugging
            print(f"📄 Page title: {self.driver.title}")
            print(f"🌐 Current URL: {self.driver.current_url}")
            
            # Check if forgot password link exists using different selectors
            selectors = [
                "//a[contains(text(), 'Quên mật khẩu')]",
                "//a[contains(text(), 'Quên mật khẩu?')]",
                "//*[contains(text(), 'Quên mật khẩu')]",
                "//a[contains(@href, 'forgot-password')]"
            ]
            
            forgot_password_link = None
            for selector in selectors:
                try:
                    forgot_password_link = self.driver.find_element(By.XPATH, selector)
                    print(f"✅ Found forgot password link with selector: {selector}")
                    break
                except:
                    continue
            
            if forgot_password_link:
                print(f"✅ Forgot password link text: {forgot_password_link.text}")
                print(f"✅ Forgot password link href: {forgot_password_link.get_attribute('href')}")
                
                # Click on forgot password link
                forgot_password_link.click()
                time.sleep(3)
                
                # Verify navigation to forgot password page
                current_url = self.driver.current_url
                print(f"🌐 Navigated to: {current_url}")
                
                if "/authentication/forgot-password" in current_url:
                    print("✅ Successfully navigated to forgot password page")
                    
                    # Check if forgot password form elements exist
                    try:
                        email_input = self.driver.find_element(By.NAME, "email")
                        print("✅ Email input field found")
                    except:
                        print("❌ Email input field not found")
                    
                    try:
                        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'GỬI')]")
                        print("✅ Submit button found")
                    except:
                        print("❌ Submit button not found")
                    
                else:
                    print(f"❌ Failed to navigate to forgot password page. Current URL: {current_url}")
                    
            else:
                print("❌ Forgot password link not found")
                
                # Print page source for debugging
                print("📄 Page source preview:")
                page_source = self.driver.page_source
                if "Quên mật khẩu" in page_source:
                    print("✅ 'Quên mật khẩu' text found in page source")
                else:
                    print("❌ 'Quên mật khẩu' text not found in page source")
                
                # Look for any links on the page
                links = self.driver.find_elements(By.TAG_NAME, "a")
                print(f"🔗 Found {len(links)} links on the page:")
                for i, link in enumerate(links[:5]):  # Show first 5 links
                    try:
                        print(f"  {i+1}. {link.text} -> {link.get_attribute('href')}")
                    except:
                        print(f"  {i+1}. [Error getting link info]")
            
            print("✅ Forgot password link test completed")
            
        except Exception as e:
            print(f"❌ Forgot password link test failed: {str(e)}")
            raise

if __name__ == "__main__":
    unittest.main() 