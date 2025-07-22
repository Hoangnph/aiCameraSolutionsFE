#!/usr/bin/env python3
"""
Dashboard Test Script
Tests dashboard functionality and checks for console errors
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enable console logging
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    return webdriver.Chrome(options=chrome_options)

def test_dashboard():
    """Test dashboard functionality"""
    print("🔍 Starting Dashboard Test")
    print("=" * 50)
    
    driver = None
    try:
        driver = setup_driver()
        
        # Test 1: Login first
        print("🔐 Testing login...")
        driver.get("http://localhost:3000/authentication/sign-in")
        time.sleep(3)
        
        # Check if login page loads
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_input = driver.find_element(By.NAME, "password")
            
            # Fill login form
            email_input.send_keys("admin@example.com")
            password_input.send_keys("admin123")
            
            # Submit form
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            print("✅ Login form submitted")
            
        except TimeoutException:
            print("❌ Login page elements not found")
            return False
        
        # Wait for redirect to dashboard
        time.sleep(5)
        
        # Test 2: Check dashboard URL
        current_url = driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        if "/dashboard" in current_url:
            print("✅ Successfully redirected to dashboard")
        else:
            print("❌ Not redirected to dashboard")
            return False
        
        # Test 3: Check for console errors
        print("\n🔍 Checking console logs...")
        logs = driver.get_log('browser')
        
        errors = []
        warnings = []
        
        for log in logs:
            if log['level'] == 'SEVERE':
                errors.append(log['message'])
            elif log['level'] == 'WARNING':
                warnings.append(log['message'])
        
        print(f"📊 Found {len(errors)} errors and {len(warnings)} warnings")
        
        # Test 4: Check for specific errors
        console_errors = []
        for error in errors:
            if "Cannot read properties of undefined" in error:
                console_errors.append("ApexCharts Error")
            elif "defaultProps" in error:
                console_errors.append("DefaultProps Warning")
            elif "React Router" in error:
                console_errors.append("React Router Warning")
            else:
                console_errors.append("Other Error")
        
        # Test 5: Check dashboard elements
        print("\n🔍 Checking dashboard elements...")
        try:
            # Wait for dashboard to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check for charts
            charts = driver.find_elements(By.CLASS_NAME, "apexcharts-canvas")
            print(f"📈 Found {len(charts)} charts")
            
            # Check for menu/sidebar
            sidebar = driver.find_elements(By.CSS_SELECTOR, "[data-testid='sidebar'], .sidebar, nav")
            print(f"📋 Found {len(sidebar)} navigation elements")
            
            # Check for content
            content = driver.find_elements(By.CSS_SELECTOR, "main, .content, .dashboard-content")
            print(f"📄 Found {len(content)} content areas")
            
        except TimeoutException:
            print("❌ Dashboard elements not found")
        
        # Test 6: Summary
        print("\n" + "=" * 50)
        print("📊 DASHBOARD TEST SUMMARY")
        print("=" * 50)
        
        success = True
        
        if "/dashboard" in current_url:
            print("✅ Dashboard Access: PASS")
        else:
            print("❌ Dashboard Access: FAIL")
            success = False
        
        if len(errors) == 0:
            print("✅ Console Errors: PASS (No errors)")
        else:
            print(f"⚠️ Console Errors: {len(errors)} errors found")
            for i, error in enumerate(console_errors[:5]):  # Show first 5
                print(f"   {i+1}. {error}")
            success = False
        
        if len(warnings) == 0:
            print("✅ Console Warnings: PASS (No warnings)")
        else:
            print(f"⚠️ Console Warnings: {len(warnings)} warnings found")
            success = False
        
        if len(charts) > 0:
            print("✅ Charts: PASS")
        else:
            print("❌ Charts: FAIL (No charts found)")
            success = False
        
        if len(sidebar) > 0:
            print("✅ Navigation: PASS")
        else:
            print("❌ Navigation: FAIL (No menu found)")
            success = False
        
        print(f"\n🎯 Overall Result: {'PASS' if success else 'FAIL'}")
        
        return success
        
    except WebDriverException as e:
        print(f"❌ WebDriver Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_dashboard() 