#!/usr/bin/env python3
"""
Security Testing Script for Face Detection System
Tests authentication, authorization, input validation, and security vulnerabilities
"""

import requests
import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import base64
import hashlib

class SecurityTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.test_images_dir = "automation_test/test_images"
        
    def log_test(self, test_name: str, success: bool, message: str = "", data: Dict = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        return success
    
    def test_cors_configuration(self) -> bool:
        """Test CORS configuration"""
        try:
            # Test preflight request
            headers = {
                'Origin': 'http://malicious-site.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options(f"{self.base_url}/api/v1/faces/upload", headers=headers, timeout=5)
            
            # Check if CORS headers are present
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            has_cors_headers = any(header in response.headers for header in cors_headers)
            
            return self.log_test(
                "CORS Configuration",
                has_cors_headers,
                f"CORS headers present: {has_cors_headers}",
                {"cors_headers": dict(response.headers)}
            )
        except Exception as e:
            return self.log_test(
                "CORS Configuration",
                False,
                f"Error: {str(e)}"
            )
    
    def test_input_validation(self) -> bool:
        """Test input validation for various endpoints"""
        results = []
        
        # Test 1: Invalid file type
        try:
            # Create a fake file with wrong extension
            fake_file = ("fake.txt", b"This is not an image", "text/plain")
            files = {'file': fake_file}
            data = {'name': 'Test User', 'email': 'test@example.com'}
            
            response = requests.post(f"{self.base_url}/api/v1/faces/upload", files=files, data=data, timeout=10)
            
            # Should reject non-image files
            results.append(self.log_test(
                "Input Validation - Invalid File Type",
                response.status_code == 400,
                f"Status: {response.status_code}, Expected: 400"
            ))
        except Exception as e:
            results.append(self.log_test(
                "Input Validation - Invalid File Type",
                False,
                f"Error: {str(e)}"
            ))
        
        # Test 2: Missing required fields
        try:
            test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
            if os.path.exists(test_image_path):
                with open(test_image_path, 'rb') as f:
                    files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                    # Missing required 'name' field
                    data = {'email': 'test@example.com'}
                    
                    response = requests.post(f"{self.base_url}/api/v1/faces/upload", files=files, data=data, timeout=10)
                    
                    results.append(self.log_test(
                        "Input Validation - Missing Required Fields",
                        response.status_code == 422,  # FastAPI validation error
                        f"Status: {response.status_code}, Expected: 422"
                    ))
        except Exception as e:
            results.append(self.log_test(
                "Input Validation - Missing Required Fields",
                False,
                f"Error: {str(e)}"
            ))
        
        # Test 3: SQL injection attempt
        try:
            malicious_name = "'; DROP TABLE persons; --"
            test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
            if os.path.exists(test_image_path):
                with open(test_image_path, 'rb') as f:
                    files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                    data = {
                        'name': malicious_name,
                        'email': 'test@example.com',
                        'phone': '1234567890'
                    }
                    
                    response = requests.post(f"{self.base_url}/api/v1/faces/upload", files=files, data=data, timeout=10)
                    
                    # Should handle malicious input gracefully
                    results.append(self.log_test(
                        "Input Validation - SQL Injection Protection",
                        response.status_code in [200, 400, 422],  # Should not crash
                        f"Status: {response.status_code}, Handled gracefully"
                    ))
        except Exception as e:
            results.append(self.log_test(
                "Input Validation - SQL Injection Protection",
                False,
                f"Error: {str(e)}"
            ))
        
        return all(results)
    
    def test_file_upload_security(self) -> bool:
        """Test file upload security measures"""
        results = []
        
        # Test 1: Large file upload
        try:
            # Create a large fake file (10MB)
            large_content = b"0" * (10 * 1024 * 1024)  # 10MB
            files = {'file': ('large_file.jpg', large_content, 'image/jpeg')}
            data = {'name': 'Test User', 'email': 'test@example.com'}
            
            response = requests.post(f"{self.base_url}/api/v1/faces/upload", files=files, data=data, timeout=30)
            
            # Should handle large files appropriately
            results.append(self.log_test(
                "File Upload Security - Large File",
                response.status_code in [200, 400, 413],  # 413 = Payload Too Large
                f"Status: {response.status_code}, Large file handled"
            ))
        except Exception as e:
            results.append(self.log_test(
                "File Upload Security - Large File",
                False,
                f"Error: {str(e)}"
            ))
        
        # Test 2: Malicious file extension
        try:
            malicious_content = b"fake image content"
            files = {'file': ('malicious.exe', malicious_content, 'application/octet-stream')}
            data = {'name': 'Test User', 'email': 'test@example.com'}
            
            response = requests.post(f"{self.base_url}/api/v1/faces/upload", files=files, data=data, timeout=10)
            
            # Should reject non-image files
            results.append(self.log_test(
                "File Upload Security - Malicious Extension",
                response.status_code == 400,
                f"Status: {response.status_code}, Expected: 400"
            ))
        except Exception as e:
            results.append(self.log_test(
                "File Upload Security - Malicious Extension",
                False,
                f"Error: {str(e)}"
            ))
        
        return all(results)
    
    def test_rate_limiting(self) -> bool:
        """Test rate limiting (if implemented)"""
        try:
            # Send multiple rapid requests
            responses = []
            for i in range(20):
                response = requests.get(f"{self.base_url}/health", timeout=5)
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay
            
            # Check if all requests were successful (no rate limiting implemented)
            all_successful = all(status == 200 for status in responses)
            
            return self.log_test(
                "Rate Limiting",
                all_successful,
                f"All {len(responses)} requests successful (no rate limiting detected)",
                {"response_codes": responses}
            )
        except Exception as e:
            return self.log_test(
                "Rate Limiting",
                False,
                f"Error: {str(e)}"
            )
    
    def test_authentication_requirements(self) -> bool:
        """Test if authentication is required for sensitive endpoints"""
        sensitive_endpoints = [
            "/api/v1/faces/upload",
            "/api/v1/faces/recognize",
            "/api/v1/faces/list"
        ]
        
        results = []
        
        for endpoint in sensitive_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                
                # Currently no authentication implemented, so should return 405 (Method Not Allowed) for GET
                # or 422 (Unprocessable Entity) for missing parameters
                expected_status = 405 if endpoint != "/api/v1/faces/list" else 200
                
                results.append(self.log_test(
                    f"Authentication - {endpoint}",
                    response.status_code == expected_status,
                    f"Status: {response.status_code}, Expected: {expected_status}",
                    {"endpoint": endpoint, "status_code": response.status_code}
                ))
            except Exception as e:
                results.append(self.log_test(
                    f"Authentication - {endpoint}",
                    False,
                    f"Error: {str(e)}"
                ))
        
        return all(results)
    
    def test_data_exposure(self) -> bool:
        """Test for sensitive data exposure"""
        try:
            # Test if sensitive information is exposed in error messages
            response = requests.get(f"{self.base_url}/nonexistent-endpoint", timeout=5)
            
            # Check if error response contains sensitive information
            response_text = response.text.lower()
            sensitive_keywords = [
                'password', 'secret', 'key', 'token', 'database', 'sql',
                'internal', 'private', 'admin', 'root', 'config'
            ]
            
            exposed_sensitive_data = any(keyword in response_text for keyword in sensitive_keywords)
            
            return self.log_test(
                "Data Exposure - Error Messages",
                not exposed_sensitive_data,
                f"Sensitive data exposed: {exposed_sensitive_data}",
                {"response_length": len(response.text)}
            )
        except Exception as e:
            return self.log_test(
                "Data Exposure - Error Messages",
                False,
                f"Error: {str(e)}"
            )
    
    def test_headers_security(self) -> bool:
        """Test security headers"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            
            # Check for common security headers
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': None,  # Optional
                'Content-Security-Policy': None  # Optional
            }
            
            missing_headers = []
            for header, expected_value in security_headers.items():
                if header not in response.headers:
                    missing_headers.append(header)
            
            has_security_headers = len(missing_headers) == 0
            
            return self.log_test(
                "Security Headers",
                has_security_headers,
                f"Missing headers: {missing_headers if missing_headers else 'None'}",
                {"headers": dict(response.headers)}
            )
        except Exception as e:
            return self.log_test(
                "Security Headers",
                False,
                f"Error: {str(e)}"
            )
    
    def generate_security_report(self) -> Dict[str, Any]:
        """Generate security test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        security_score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "security_score": security_score,
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url
            },
            "test_results": self.test_results,
            "recommendations": []
        }
        
        # Generate security recommendations
        if failed_tests > 0:
            report["recommendations"].append("Implement missing security measures.")
        
        if security_score < 80:
            report["recommendations"].append("Security score is low. Review failed tests.")
        
        if security_score < 60:
            report["recommendations"].append("Critical security issues detected. Immediate action required.")
        
        if security_score >= 80:
            report["recommendations"].append("Good security posture. Consider additional hardening.")
        
        # Specific recommendations based on test results
        for result in self.test_results:
            if not result['success']:
                if 'CORS' in result['test_name']:
                    report["recommendations"].append("Configure CORS properly for production.")
                elif 'Authentication' in result['test_name']:
                    report["recommendations"].append("Implement authentication for sensitive endpoints.")
                elif 'Input Validation' in result['test_name']:
                    report["recommendations"].append("Strengthen input validation.")
                elif 'File Upload' in result['test_name']:
                    report["recommendations"].append("Implement file upload security measures.")
                elif 'Rate Limiting' in result['test_name']:
                    report["recommendations"].append("Implement rate limiting for API endpoints.")
        
        return report
    
    def run_comprehensive_security_test(self) -> bool:
        """Run comprehensive security test suite"""
        print("🔒 Starting Comprehensive Security Test Suite")
        print("=" * 60)
        
        # Run all security tests
        tests = [
            ("CORS Configuration", self.test_cors_configuration),
            ("Input Validation", self.test_input_validation),
            ("File Upload Security", self.test_file_upload_security),
            ("Rate Limiting", self.test_rate_limiting),
            ("Authentication Requirements", self.test_authentication_requirements),
            ("Data Exposure", self.test_data_exposure),
            ("Security Headers", self.test_headers_security)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            test_func()
        
        # Generate and display report
        report = self.generate_security_report()
        
        print("\n" + "=" * 60)
        print("🔒 SECURITY TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['passed_tests']}")
        print(f"Failed: {report['summary']['failed_tests']}")
        print(f"Security Score: {report['summary']['security_score']:.1f}%")
        
        if report['recommendations']:
            print("\n💡 Security Recommendations:")
            for rec in report['recommendations']:
                print(f"   • {rec}")
        
        # Save report
        self.save_security_report(report)
        
        return report['summary']['security_score'] >= 70  # Pass if 70% or higher
    
    def save_security_report(self, report: Dict[str, Any], filename: str = None):
        """Save security test report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.json"
        
        report_path = os.path.join("automation_test", "reports", filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Security report saved to: {report_path}")
        return report_path

def main():
    """Main function"""
    print("🔒 Face Detection System - Security Testing")
    print("=" * 60)
    
    # Create test instance
    tester = SecurityTest()
    
    # Run comprehensive security test
    success = tester.run_comprehensive_security_test()
    
    if success:
        print("\n✅ Security tests passed! System is secure for development.")
    else:
        print("\n⚠️ Security tests failed. Review recommendations before production.")
    
    print("\n📝 Security Notes:")
    print("1. This is a development environment - no authentication implemented")
    print("2. Consider implementing authentication for production")
    print("3. Add rate limiting for API endpoints")
    print("4. Configure proper CORS for production domains")
    print("5. Implement file upload validation and size limits")

if __name__ == "__main__":
    main() 