#!/usr/bin/env python3
"""
🧪 Database Connection Test - AI Camera Counting System
📅 Created: 2025-01-09
👥 Maintainer: QA Team

Test Case: DB-CONN-001 - Database Connection Test
Priority: High
Type: Positive
"""

import psycopg2
import json
import sys
import time
from datetime import datetime
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class DatabaseConnectionTest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        self.config = self.load_config()
        
    def load_config(self):
        """Load test configuration"""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'config', 'test_config.json'
        )
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Test configuration file not found")
            sys.exit(1)
    
    def log_test(self, test_name, status, message, details=None):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        
        # Print result
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {message}")
        
        if details:
            print(f"   Details: {details}")
    
    def test_database_connection(self):
        """Test basic database connection"""
        test_name = "DB-CONN-001"
        
        try:
            # Get database configuration
            db_config = self.config['test_environment']['database']
            
            # Debug: Print connection details
            print(f"🔍 Connecting to database: {db_config['name']} on {db_config['host']}:{db_config['port']}")
            
            # Attempt connection
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['name'],
                user=db_config['user'],
                password=db_config['password']
            )
            
            # Test connection
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.log_test(
                test_name,
                "PASS",
                "Database connection successful",
                f"PostgreSQL version: {version}"
            )
            return True
            
        except psycopg2.Error as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Database connection failed: {str(e)}",
                f"Error code: {e.pgcode}"
            )
            return False
    
    def test_database_tables(self):
        """Test if required tables exist"""
        test_name = "DB-TABLES-001"
        
        try:
            # Get database configuration
            db_config = self.config['test_environment']['database']
            
            # Connect to database
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['name'],
                user=db_config['user'],
                password=db_config['password']
            )
            
            cursor = conn.cursor()
            
            # Check required tables
            required_tables = [
                'users', 'cameras', 'refresh_tokens', 'user_sessions', 'registration_codes', 'audit_log',
                'ai_models', 'zones', 'counting_results', 'analytics', 'alerts', 'audit_logs', 'files', 'system_logs',
                'migrations', 'migration_log', 'deployment_migrations', 'deployment_execution_logs', 'model_logs', 'camera_events'
            ]
            
            missing_tables = []
            existing_tables = []
            
            for table in required_tables:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    );
                """, (table,))
                
                if cursor.fetchone()[0]:
                    existing_tables.append(table)
                else:
                    missing_tables.append(table)
            
            cursor.close()
            conn.close()
            
            if not missing_tables:
                self.log_test(
                    test_name,
                    "PASS",
                    f"All required tables exist ({len(existing_tables)} tables)",
                    f"Tables: {', '.join(existing_tables)}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Missing tables: {', '.join(missing_tables)}",
                    f"Existing: {', '.join(existing_tables)}"
                )
                return False
                
        except psycopg2.Error as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Table check failed: {str(e)}",
                f"Error code: {e.pgcode}"
            )
            return False
    
    def test_database_permissions(self):
        """Test database user permissions"""
        test_name = "DB-PERM-001"
        
        try:
            # Get database configuration
            db_config = self.config['test_environment']['database']
            
            # Connect to database
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['name'],
                user=db_config['user'],
                password=db_config['password']
            )
            
            cursor = conn.cursor()
            
            # Test basic permissions
            permissions = []
            
            # Test SELECT permission
            try:
                cursor.execute("SELECT COUNT(*) FROM users;")
                permissions.append("SELECT")
            except psycopg2.Error:
                pass
            
            # Test INSERT permission
            try:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, role) 
                    VALUES ('test_user', 'test@example.com', 'hash', 'user')
                    ON CONFLICT DO NOTHING;
                """)
                permissions.append("INSERT")
            except psycopg2.Error:
                pass
            
            # Test UPDATE permission
            try:
                cursor.execute("""
                    UPDATE users SET last_login = NOW() 
                    WHERE username = 'test_user';
                """)
                permissions.append("UPDATE")
            except psycopg2.Error:
                pass
            
            # Test DELETE permission
            try:
                cursor.execute("DELETE FROM users WHERE username = 'test_user';")
                permissions.append("DELETE")
            except psycopg2.Error:
                pass
            
            cursor.close()
            conn.close()
            
            if len(permissions) >= 2:  # At least SELECT and INSERT
                self.log_test(
                    test_name,
                    "PASS",
                    f"Database permissions verified ({len(permissions)} permissions)",
                    f"Permissions: {', '.join(permissions)}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Insufficient permissions ({len(permissions)} permissions)",
                    f"Available: {', '.join(permissions)}"
                )
                return False
                
        except psycopg2.Error as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Permission check failed: {str(e)}",
                f"Error code: {e.pgcode}"
            )
            return False
    
    def test_database_performance(self):
        """Test basic database performance"""
        test_name = "DB-PERF-001"
        
        try:
            # Get database configuration
            db_config = self.config['test_environment']['database']
            
            # Connect to database
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['name'],
                user=db_config['user'],
                password=db_config['password']
            )
            
            cursor = conn.cursor()
            
            # Test query performance
            start_time = time.time()
            
            # Simple query
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            
            simple_query_time = time.time() - start_time
            
            # Complex query
            start_time = time.time()
            cursor.execute("""
                SELECT u.username, c.name, cr.count_in, cr.count_out, cr.total_count, cr.confidence
                FROM users u
                LEFT JOIN cameras c ON 1=1
                LEFT JOIN counting_results cr ON c.id = cr.camera_id
                LIMIT 10;
            """)
            complex_result = cursor.fetchall()
            
            complex_query_time = time.time() - start_time
            
            cursor.close()
            conn.close()
            
            # Performance thresholds
            simple_threshold = 1.0  # 1 second
            complex_threshold = 5.0  # 5 seconds
            
            if simple_query_time < simple_threshold and complex_query_time < complex_threshold:
                self.log_test(
                    test_name,
                    "PASS",
                    f"Database performance acceptable",
                    f"Simple query: {simple_query_time:.3f}s, Complex query: {complex_query_time:.3f}s"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Database performance below threshold",
                    f"Simple query: {simple_query_time:.3f}s (threshold: {simple_threshold}s), Complex query: {complex_query_time:.3f}s (threshold: {complex_threshold}s)"
                )
                return False
                
        except psycopg2.Error as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Performance test failed: {str(e)}",
                f"Error code: {e.pgcode}"
            )
            return False
    
    def save_results(self):
        """Save test results to file"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        results = {
            'test_suite': 'Database Connection Tests',
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'total_tests': len(self.test_results),
            'passed_tests': len([r for r in self.test_results if r['status'] == 'PASS']),
            'failed_tests': len([r for r in self.test_results if r['status'] == 'FAIL']),
            'results': self.test_results
        }
        
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        # Save JSON results
        results_file = os.path.join(results_dir, 'database_connection_test_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Results saved to: {results_file}")
        
        return results
    
    def run_all_tests(self):
        """Run all database tests"""
        print("==========================================")
        print("🧪 DATABASE CONNECTION TESTS")
        print("AI Camera Counting System")
        print("==========================================")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Run tests
        tests = [
            self.test_database_connection,
            self.test_database_tables,
            self.test_database_permissions,
            self.test_database_performance
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        # Summary
        print("")
        print("==========================================")
        print("📊 TEST SUMMARY")
        print("==========================================")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All database tests passed!")
        else:
            print("⚠️  Some database tests failed!")
        
        # Save results
        results = self.save_results()
        
        return passed == total

def main():
    """Main function"""
    try:
        test_suite = DatabaseConnectionTest()
        success = test_suite.run_all_tests()
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 