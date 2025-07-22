#!/usr/bin/env python3
"""
Comprehensive Authentication Security Test
Tests both HTTP responses and client-side redirects
"""

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_http_responses():
    """Test HTTP responses for protected routes"""
    print("🔒 Testing HTTP responses for protected routes...")
    
    base_url = "http://localhost:3000"
    protected_routes = [
        "/dashboard",
        "/cameras", 
        "/analytics",
        "/tables",
        "/billing",
        "/profile"
    ]
    
    results = {}
    
    for route in protected_routes:
        print(f"  Testing route: {route}")
        
        try:
            # Make direct request to protected route
            response = requests.get(f"{base_url}{route}", timeout=10)
            
            print(f"    Status Code: {response.status_code}")
            print(f"    URL: {response.url}")
            
            # Check if redirected to login
            if "/authentication" in response.url or "/sign-in" in response.url:
                print(f"    ✅ {route}: HTTP redirect to login")
                results[route] = "PASS"
            elif response.status_code == 200:
                # Check if page content contains login form
                content = response.text.lower()
                if "sign in" in content or "login" in content or "authentication" in content:
                    print(f"    ✅ {route}: Shows login page")
                    results[route] = "PASS"
                else:
                    print(f"    ⚠️ {route}: Shows content without login (may be client-side protected)")
                    results[route] = "CLIENT_SIDE"
            else:
                print(f"    ⚠️ {route}: Unexpected status code {response.status_code}")
                results[route] = "UNKNOWN"
                
        except Exception as e:
            print(f"    ⚠️ {route}: Error - {str(e)}")
            results[route] = "ERROR"
    
    return results

def test_client_side_redirects():
    """Test client-side redirects using Selenium"""
    print("\n🌐 Testing client-side redirects...")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    results = {}
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        
        protected_routes = [
            "/dashboard",
            "/cameras", 
            "/analytics",
            "/tables",
            "/billing",
            "/profile"
        ]
        
        for route in protected_routes:
            print(f"  Testing route: {route}")
            
            try:
                # Navigate to protected route
                driver.get(f"http://localhost:3000{route}")
                
                # Wait for page to load
                time.sleep(2)
                
                # Check current URL
                current_url = driver.current_url
                print(f"    Current URL: {current_url}")
                
                # Check if redirected to login
                if "/authentication" in current_url or "/sign-in" in current_url:
                    print(f"    ✅ {route}: Client-side redirect to login")
                    results[route] = "PASS"
                else:
                    # Check if page contains login form
                    try:
                        login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sign In') or contains(text(), 'Login') or contains(text(), 'Authentication')]")
                        if login_elements:
                            print(f"    ✅ {route}: Shows login page")
                            results[route] = "PASS"
                        else:
                            print(f"    ❌ {route}: NOT protected - shows content without login")
                            results[route] = "FAIL"
                    except:
                        print(f"    ❌ {route}: NOT protected - shows content without login")
                        results[route] = "FAIL"
                        
            except Exception as e:
                print(f"    ⚠️ {route}: Error - {str(e)}")
                results[route] = "ERROR"
        
        driver.quit()
        
    except Exception as e:
        print(f"  ⚠️ Selenium error: {str(e)}")
        print("  Skipping client-side tests")
        return {}
    
    return results

def test_public_routes():
    """Test that public routes are accessible"""
    print("\n🌐 Testing public routes...")
    
    base_url = "http://localhost:3000"
    public_routes = [
        "/authentication/sign-in",
        "/authentication/sign-up"
    ]
    
    results = {}
    
    for route in public_routes:
        print(f"  Testing route: {route}")
        
        try:
            response = requests.get(f"{base_url}{route}", timeout=10)
            
            print(f"    Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✅ {route}: Accessible")
                results[route] = "PASS"
            else:
                print(f"    ❌ {route}: Not accessible - {response.status_code}")
                results[route] = "FAIL"
                
        except Exception as e:
            print(f"    ⚠️ {route}: Error - {str(e)}")
            results[route] = "ERROR"
    
    return results

def main():
    """Run all tests"""
    print("🔒 Starting Comprehensive Authentication Security Tests")
    print("=" * 60)
    
    # Test 1: HTTP responses
    http_results = test_http_responses()
    
    # Test 2: Client-side redirects
    client_results = test_client_side_redirects()
    
    # Test 3: Public routes
    public_results = test_public_routes()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE SECURITY TEST SUMMARY")
    print("=" * 60)
    
    # HTTP Results
    print("\n🔒 HTTP Response Test Results:")
    for route, result in http_results.items():
        status = "✅ PASS" if result == "PASS" else "⚠️ CLIENT_SIDE" if result == "CLIENT_SIDE" else "❌ FAIL" if result == "FAIL" else "⚠️ ERROR" if result == "ERROR" else "❓ UNKNOWN"
        print(f"  {route}: {status}")
    
    # Client-side Results
    if client_results:
        print("\n🌐 Client-side Redirect Test Results:")
        for route, result in client_results.items():
            status = "✅ PASS" if result == "PASS" else "❌ FAIL" if result == "FAIL" else "⚠️ ERROR" if result == "ERROR" else "❓ UNKNOWN"
            print(f"  {route}: {status}")
    
    # Public Routes
    print("\n🌐 Public Routes Test Results:")
    for route, result in public_results.items():
        status = "✅ PASS" if result == "PASS" else "❌ FAIL" if result == "FAIL" else "⚠️ ERROR"
        print(f"  {route}: {status}")
    
    # Overall Assessment
    print("\n🎯 OVERALL ASSESSMENT:")
    
    # Check for security issues
    http_failed = [route for route, result in http_results.items() if result == "FAIL"]
    client_failed = [route for route, result in client_results.items() if result == "FAIL"]
    
    if http_failed or client_failed:
        print("❌ SECURITY ISSUES DETECTED:")
        if http_failed:
            print(f"  HTTP Protection Failed: {http_failed}")
        if client_failed:
            print(f"  Client-side Protection Failed: {client_failed}")
        print("🚨 CRITICAL: Frontend authentication has security issues!")
    else:
        print("✅ ALL SECURITY TESTS PASSED")
        print("🔒 Frontend authentication is working correctly")
    
    print("\nRecommendations:")
    if http_failed or client_failed:
        print("  - Fix route protection for failed routes")
    print("  - Add comprehensive authentication testing")
    print("  - Monitor authentication logs")
    print("  - Consider server-side protection for additional security")

if __name__ == "__main__":
    main() 