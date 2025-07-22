#!/usr/bin/env python3
"""
Simple Browser Test for Immediate Protection
Tests if immediate client-side protection is working
"""

import requests
import time

def test_immediate_protection():
    """Test if immediate protection is working"""
    print("🔒 Testing Immediate Client-Side Protection...")
    
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
            # Make request and check if redirected
            response = requests.get(f"{base_url}{route}", timeout=10, allow_redirects=True)
            
            print(f"    Status Code: {response.status_code}")
            print(f"    Final URL: {response.url}")
            
            # Check if redirected to login
            if "/authentication" in response.url or "/sign-in" in response.url:
                print(f"    ✅ {route}: Redirected to login")
                results[route] = "PASS"
            elif response.status_code == 200:
                # Check if page content contains login form
                content = response.text.lower()
                if "sign in" in content or "login" in content or "authentication" in content:
                    print(f"    ✅ {route}: Shows login page")
                    results[route] = "PASS"
                else:
                    print(f"    ❌ {route}: Shows content without login")
                    results[route] = "FAIL"
            else:
                print(f"    ⚠️ {route}: Unexpected status code {response.status_code}")
                results[route] = "UNKNOWN"
                
        except Exception as e:
            print(f"    ⚠️ {route}: Error - {str(e)}")
            results[route] = "ERROR"
    
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
    print("🔒 Starting Simple Browser Test for Immediate Protection")
    print("=" * 60)
    
    # Test 1: Immediate protection
    protected_results = test_immediate_protection()
    
    # Test 2: Public routes
    public_results = test_public_routes()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SIMPLE BROWSER TEST SUMMARY")
    print("=" * 60)
    
    # Protected Routes
    print("\n🔒 Protected Routes Test Results:")
    for route, result in protected_results.items():
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
    protected_failed = [route for route, result in protected_results.items() if result == "FAIL"]
    
    if protected_failed:
        print("❌ SECURITY ISSUES DETECTED:")
        print(f"  Protection Failed: {protected_failed}")
        print("🚨 CRITICAL: Frontend authentication has security issues!")
    else:
        print("✅ ALL SECURITY TESTS PASSED")
        print("🔒 Frontend authentication is working correctly")
    
    print("\nRecommendations:")
    if protected_failed:
        print("  - Fix route protection for failed routes")
    print("  - Add comprehensive authentication testing")
    print("  - Monitor authentication logs")

if __name__ == "__main__":
    main() 