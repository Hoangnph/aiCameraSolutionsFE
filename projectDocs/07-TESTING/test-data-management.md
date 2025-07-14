# Test Data Management Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa chiến lược quản lý test data cho hệ thống AI Camera Counting, bao gồm data generation, fixtures, cleanup procedures, và data privacy protection.

### 🎯 Mục tiêu
- Đảm bảo test data consistency và reliability
- Tự động hóa test data generation
- Bảo vệ privacy và security của test data
- Tối ưu hóa test execution time

### 🏗️ Test Data Strategy

#### Data Management Principles
```python
# Test Data Management Principles
class TestDataPrinciples:
    """
    Core principles for test data management
    """
    
    # 1. Isolation: Each test should have isolated data
    ISOLATION = "Each test should have its own data set"
    
    # 2. Deterministic: Tests should be repeatable
    DETERMINISTIC = "Same input should produce same output"
    
    # 3. Minimal: Use only necessary data
    MINIMAL = "Use minimum data required for test"
    
    # 4. Realistic: Data should represent real scenarios
    REALISTIC = "Data should mimic real-world scenarios"
    
    # 5. Secure: Sensitive data should be masked
    SECURE = "Sensitive data must be properly masked"
    
    # 6. Fast: Data generation should be efficient
    FAST = "Data generation should be optimized for speed"
```

#### Data Categories
```python
# Test Data Categories
class TestDataCategories:
    """
    Categories of test data for different testing needs
    """
    
    # User Data
    USERS = {
        "admin_users": "Administrative users with full access",
        "regular_users": "Standard users with limited access",
        "test_users": "Users for specific test scenarios",
        "inactive_users": "Users with disabled accounts"
    }
    
    # Camera Data
    CAMERAS = {
        "active_cameras": "Cameras currently in use",
        "inactive_cameras": "Cameras not currently active",
        "maintenance_cameras": "Cameras under maintenance",
        "test_cameras": "Cameras for testing purposes"
    }
    
    # Count Data
    COUNT_DATA = {
        "normal_counts": "Typical counting scenarios",
        "high_volume_counts": "High traffic scenarios",
        "edge_case_counts": "Boundary condition scenarios",
        "error_counts": "Error condition scenarios"
    }
    
    # System Data
    SYSTEM_DATA = {
        "configurations": "System configuration data",
        "settings": "User and system settings",
        "logs": "Application and error logs",
        "metrics": "Performance and usage metrics"
    }
```

### 🏭 Data Generation

#### Factory Pattern Implementation
```python
# Test Data Factories
import factory
from faker import Faker
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

fake = Faker()

class UserFactory(factory.Factory):
    """Factory for creating test users"""
    
    class Meta:
        model = dict
    
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    email = factory.LazyFunction(lambda: fake.email())
    username = factory.LazyFunction(lambda: fake.user_name())
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    password_hash = factory.LazyFunction(lambda: fake.sha256())
    role = factory.Iterator(['admin', 'user', 'viewer'])
    is_active = factory.Iterator([True, False])
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_month())

class CameraFactory(factory.Factory):
    """Factory for creating test cameras"""
    
    class Meta:
        model = dict
    
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.LazyFunction(lambda: f"Camera {fake.random_int(min=1, max=100)}")
    location = factory.LazyFunction(lambda: fake.address())
    ip_address = factory.LazyFunction(lambda: fake.ipv4())
    status = factory.Iterator(['active', 'inactive', 'maintenance'])
    model = factory.Iterator(['HD-1080p', '4K-UHD', 'PTZ-Camera'])
    resolution = factory.Iterator(['1920x1080', '3840x2160', '1280x720'])
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    last_maintenance = factory.LazyFunction(lambda: fake.date_time_this_month())

class CountDataFactory(factory.Factory):
    """Factory for creating test count data"""
    
    class Meta:
        model = dict
    
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    camera_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    count = factory.LazyFunction(lambda: fake.random_int(min=0, max=100))
    confidence = factory.LazyFunction(lambda: fake.pyfloat(min_value=0.5, max_value=1.0))
    timestamp = factory.LazyFunction(lambda: fake.date_time_this_month())
    duration = factory.LazyFunction(lambda: fake.random_int(min=1, max=3600))
    object_type = factory.Iterator(['person', 'vehicle', 'animal'])
    direction = factory.Iterator(['in', 'out', 'both'])
```

#### Data Builder Pattern
```python
# Data Builder Pattern
class TestDataBuilder:
    """Builder pattern for complex test data scenarios"""
    
    def __init__(self):
        self.data = {}
    
    def with_user(self, role: str = 'user', **kwargs) -> 'TestDataBuilder':
        """Add user data to the builder"""
        user_data = UserFactory(**kwargs)
        user_data['role'] = role
        self.data['user'] = user_data
        return self
    
    def with_camera(self, status: str = 'active', **kwargs) -> 'TestDataBuilder':
        """Add camera data to the builder"""
        camera_data = CameraFactory(**kwargs)
        camera_data['status'] = status
        self.data['camera'] = camera_data
        return self
    
    def with_count_data(self, count: int = 10, **kwargs) -> 'TestDataBuilder':
        """Add count data to the builder"""
        count_data = []
        for _ in range(count):
            count_data.append(CountDataFactory(**kwargs))
        self.data['count_data'] = count_data
        return self
    
    def with_system_config(self, **kwargs) -> 'TestDataBuilder':
        """Add system configuration data"""
        self.data['system_config'] = {
            'api_version': 'v1',
            'max_cameras': 100,
            'data_retention_days': 30,
            'alert_threshold': 50,
            **kwargs
        }
        return self
    
    def build(self) -> Dict:
        """Build and return the complete test data set"""
        return self.data.copy()

# Usage example
test_scenario = (TestDataBuilder()
                .with_user(role='admin')
                .with_camera(status='active')
                .with_count_data(count=5)
                .with_system_config()
                .build())
```

### 🔒 Data Privacy & Security

#### Data Masking Implementation
```python
# Data Masking for Privacy
import hashlib
import re
from typing import Any, Dict, List

class DataMasker:
    """Utility for masking sensitive data in test data"""
    
    def __init__(self):
        self.masking_rules = {
            'email': self._mask_email,
            'phone': self._mask_phone,
            'ip_address': self._mask_ip,
            'password': self._mask_password,
            'name': self._mask_name,
            'address': self._mask_address
        }
    
    def mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive data in test data"""
        masked_data = data.copy()
        
        for key, value in masked_data.items():
            if isinstance(value, dict):
                masked_data[key] = self.mask_sensitive_data(value)
            elif isinstance(value, list):
                masked_data[key] = [self.mask_sensitive_data(item) if isinstance(item, dict) else item for item in value]
            else:
                for pattern, mask_func in self.masking_rules.items():
                    if pattern in key.lower():
                        masked_data[key] = mask_func(value)
        
        return masked_data
    
    def _mask_email(self, email: str) -> str:
        """Mask email address"""
        if '@' in email:
            username, domain = email.split('@')
            masked_username = username[0] + '*' * (len(username) - 2) + username[-1] if len(username) > 2 else username
            return f"{masked_username}@{domain}"
        return email
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone number"""
        return re.sub(r'\d', '*', phone)
    
    def _mask_ip(self, ip: str) -> str:
        """Mask IP address"""
        parts = ip.split('.')
        return f"{parts[0]}.{parts[1]}.*.*"
    
    def _mask_password(self, password: str) -> str:
        """Mask password"""
        return '*' * len(password)
    
    def _mask_name(self, name: str) -> str:
        """Mask name"""
        if len(name) > 2:
            return name[0] + '*' * (len(name) - 2) + name[-1]
        return name
    
    def _mask_address(self, address: str) -> str:
        """Mask address"""
        parts = address.split()
        if len(parts) > 2:
            return f"{parts[0]} *** {parts[-1]}"
        return address

# Usage
masker = DataMasker()
sensitive_data = {
    'email': 'john.doe@example.com',
    'phone': '123-456-7890',
    'ip_address': '192.168.1.100',
    'password': 'secretpassword'
}
masked_data = masker.mask_sensitive_data(sensitive_data)
```

#### Data Anonymization
```python
# Data Anonymization
class DataAnonymizer:
    """Utility for anonymizing test data"""
    
    def __init__(self):
        self.hash_salt = "test_salt_2024"
    
    def anonymize_user_data(self, user_data: Dict) -> Dict:
        """Anonymize user data while maintaining referential integrity"""
        anonymized = user_data.copy()
        
        # Hash sensitive fields for consistency
        if 'email' in anonymized:
            anonymized['email'] = self._hash_value(anonymized['email'])
        
        if 'username' in anonymized:
            anonymized['username'] = self._hash_value(anonymized['username'])
        
        # Remove or mask other sensitive fields
        sensitive_fields = ['ssn', 'credit_card', 'bank_account']
        for field in sensitive_fields:
            if field in anonymized:
                anonymized[field] = self._mask_sensitive_field(anonymized[field])
        
        return anonymized
    
    def _hash_value(self, value: str) -> str:
        """Hash a value consistently"""
        return hashlib.sha256((value + self.hash_salt).encode()).hexdigest()[:16]
    
    def _mask_sensitive_field(self, value: str) -> str:
        """Mask sensitive field values"""
        return '*' * len(str(value))
```

### 🧹 Data Cleanup

#### Cleanup Strategies
```python
# Test Data Cleanup
import asyncio
from typing import List, Set
from datetime import datetime, timedelta

class TestDataCleanup:
    """Manages cleanup of test data"""
    
    def __init__(self, database_connection):
        self.db = database_connection
        self.cleanup_strategies = {
            'immediate': self._immediate_cleanup,
            'deferred': self._deferred_cleanup,
            'scheduled': self._scheduled_cleanup
        }
    
    async def cleanup_test_data(self, test_id: str, strategy: str = 'immediate'):
        """Clean up test data based on strategy"""
        if strategy in self.cleanup_strategies:
            await self.cleanup_strategies[strategy](test_id)
        else:
            raise ValueError(f"Unknown cleanup strategy: {strategy}")
    
    async def _immediate_cleanup(self, test_id: str):
        """Clean up data immediately after test"""
        cleanup_queries = [
            f"DELETE FROM count_data WHERE test_id = '{test_id}'",
            f"DELETE FROM cameras WHERE test_id = '{test_id}'",
            f"DELETE FROM users WHERE test_id = '{test_id}'",
            f"DELETE FROM system_logs WHERE test_id = '{test_id}'"
        ]
        
        for query in cleanup_queries:
            await self.db.execute(query)
    
    async def _deferred_cleanup(self, test_id: str):
        """Schedule cleanup for later execution"""
        cleanup_time = datetime.now() + timedelta(hours=1)
        
        cleanup_task = {
            'test_id': test_id,
            'scheduled_time': cleanup_time,
            'status': 'pending'
        }
        
        await self.db.execute(
            "INSERT INTO cleanup_schedule (test_id, scheduled_time, status) VALUES (%s, %s, %s)",
            (test_id, cleanup_time, 'pending')
        )
    
    async def _scheduled_cleanup(self, test_id: str):
        """Clean up data based on retention policy"""
        retention_days = 7
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        cleanup_queries = [
            f"DELETE FROM count_data WHERE test_id = '{test_id}' AND created_at < %s",
            f"DELETE FROM system_logs WHERE test_id = '{test_id}' AND created_at < %s"
        ]
        
        for query in cleanup_queries:
            await self.db.execute(query, (cutoff_date,))
```

#### Fixture Management
```python
# Test Fixtures
import pytest
from typing import Dict, Any

class TestFixtures:
    """Manages test fixtures and data setup"""
    
    @pytest.fixture
    def sample_user(self) -> Dict[str, Any]:
        """Fixture for sample user data"""
        return UserFactory()
    
    @pytest.fixture
    def admin_user(self) -> Dict[str, Any]:
        """Fixture for admin user data"""
        return UserFactory(role='admin', is_active=True)
    
    @pytest.fixture
    def active_camera(self) -> Dict[str, Any]:
        """Fixture for active camera data"""
        return CameraFactory(status='active')
    
    @pytest.fixture
    def count_data_set(self) -> List[Dict[str, Any]]:
        """Fixture for count data set"""
        return [CountDataFactory() for _ in range(10)]
    
    @pytest.fixture
    def complete_test_scenario(self) -> Dict[str, Any]:
        """Fixture for complete test scenario"""
        return (TestDataBuilder()
                .with_user(role='admin')
                .with_camera(status='active')
                .with_count_data(count=5)
                .with_system_config()
                .build())
    
    @pytest.fixture
    async def clean_database(self):
        """Fixture for clean database state"""
        # Setup: Clean database
        await self._clean_database()
        yield
        # Teardown: Clean database again
        await self._clean_database()
    
    async def _clean_database(self):
        """Clean all test data from database"""
        cleanup_queries = [
            "DELETE FROM count_data WHERE test_id IS NOT NULL",
            "DELETE FROM cameras WHERE test_id IS NOT NULL",
            "DELETE FROM users WHERE test_id IS NOT NULL",
            "DELETE FROM system_logs WHERE test_id IS NOT NULL"
        ]
        
        for query in cleanup_queries:
            await self.db.execute(query)
```

### 📊 Data Validation

#### Data Quality Checks
```python
# Test Data Validation
from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class ValidationRule:
    """Validation rule for test data"""
    field_name: str
    rule_type: str
    expected_value: Any
    error_message: str

class TestDataValidator:
    """Validates test data quality and consistency"""
    
    def __init__(self):
        self.validation_rules = {
            'user': self._get_user_validation_rules(),
            'camera': self._get_camera_validation_rules(),
            'count_data': self._get_count_data_validation_rules()
        }
    
    def validate_data(self, data_type: str, data: Dict) -> List[str]:
        """Validate test data against rules"""
        errors = []
        
        if data_type in self.validation_rules:
            rules = self.validation_rules[data_type]
            for rule in rules:
                if not self._validate_rule(rule, data):
                    errors.append(rule.error_message)
        
        return errors
    
    def _get_user_validation_rules(self) -> List[ValidationRule]:
        """Get validation rules for user data"""
        return [
            ValidationRule('email', 'format', r'^[^@]+@[^@]+\.[^@]+$', 'Invalid email format'),
            ValidationRule('username', 'length', (3, 50), 'Username length must be between 3 and 50 characters'),
            ValidationRule('role', 'enum', ['admin', 'user', 'viewer'], 'Invalid user role'),
            ValidationRule('is_active', 'type', bool, 'is_active must be boolean')
        ]
    
    def _get_camera_validation_rules(self) -> List[ValidationRule]:
        """Get validation rules for camera data"""
        return [
            ValidationRule('name', 'length', (1, 100), 'Camera name cannot be empty'),
            ValidationRule('ip_address', 'format', r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', 'Invalid IP address'),
            ValidationRule('status', 'enum', ['active', 'inactive', 'maintenance'], 'Invalid camera status'),
            ValidationRule('resolution', 'format', r'^\d+x\d+$', 'Invalid resolution format')
        ]
    
    def _get_count_data_validation_rules(self) -> List[ValidationRule]:
        """Get validation rules for count data"""
        return [
            ValidationRule('count', 'range', (0, 1000), 'Count must be between 0 and 1000'),
            ValidationRule('confidence', 'range', (0.0, 1.0), 'Confidence must be between 0.0 and 1.0'),
            ValidationRule('timestamp', 'type', datetime, 'Timestamp must be datetime object'),
            ValidationRule('object_type', 'enum', ['person', 'vehicle', 'animal'], 'Invalid object type')
        ]
    
    def _validate_rule(self, rule: ValidationRule, data: Dict) -> bool:
        """Validate a single rule against data"""
        if rule.field_name not in data:
            return False
        
        value = data[rule.field_name]
        
        if rule.rule_type == 'format':
            return bool(re.match(rule.expected_value, str(value)))
        elif rule.rule_type == 'length':
            min_len, max_len = rule.expected_value
            return min_len <= len(str(value)) <= max_len
        elif rule.rule_type == 'enum':
            return value in rule.expected_value
        elif rule.rule_type == 'type':
            return isinstance(value, rule.expected_value)
        elif rule.rule_type == 'range':
            min_val, max_val = rule.expected_value
            return min_val <= value <= max_val
        
        return True
```

### 🚀 Performance Optimization

#### Data Generation Optimization
```python
# Optimized Data Generation
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

class OptimizedDataGenerator:
    """Optimized test data generator"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def generate_bulk_data(self, data_type: str, count: int) -> List[Dict[str, Any]]:
        """Generate bulk test data efficiently"""
        if data_type == 'users':
            return await self._generate_bulk_users(count)
        elif data_type == 'cameras':
            return await self._generate_bulk_cameras(count)
        elif data_type == 'count_data':
            return await self._generate_bulk_count_data(count)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    async def _generate_bulk_users(self, count: int) -> List[Dict[str, Any]]:
        """Generate bulk user data"""
        loop = asyncio.get_event_loop()
        
        # Split work into chunks
        chunk_size = count // self.max_workers
        chunks = [chunk_size] * self.max_workers
        chunks[-1] += count % self.max_workers
        
        # Generate data in parallel
        tasks = []
        for chunk_size in chunks:
            task = loop.run_in_executor(
                self.executor,
                self._generate_user_chunk,
                chunk_size
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Combine results
        all_users = []
        for chunk in results:
            all_users.extend(chunk)
        
        return all_users
    
    def _generate_user_chunk(self, count: int) -> List[Dict[str, Any]]:
        """Generate a chunk of user data"""
        return [UserFactory() for _ in range(count)]
    
    async def _generate_bulk_cameras(self, count: int) -> List[Dict[str, Any]]:
        """Generate bulk camera data"""
        loop = asyncio.get_event_loop()
        
        chunk_size = count // self.max_workers
        chunks = [chunk_size] * self.max_workers
        chunks[-1] += count % self.max_workers
        
        tasks = []
        for chunk_size in chunks:
            task = loop.run_in_executor(
                self.executor,
                self._generate_camera_chunk,
                chunk_size
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        all_cameras = []
        for chunk in results:
            all_cameras.extend(chunk)
        
        return all_cameras
    
    def _generate_camera_chunk(self, count: int) -> List[Dict[str, Any]]:
        """Generate a chunk of camera data"""
        return [CameraFactory() for _ in range(count)]
    
    async def _generate_bulk_count_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate bulk count data"""
        loop = asyncio.get_event_loop()
        
        chunk_size = count // self.max_workers
        chunks = [chunk_size] * self.max_workers
        chunks[-1] += count % self.max_workers
        
        tasks = []
        for chunk_size in chunks:
            task = loop.run_in_executor(
                self.executor,
                self._generate_count_data_chunk,
                chunk_size
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        all_count_data = []
        for chunk in results:
            all_count_data.extend(chunk)
        
        return all_count_data
    
    def _generate_count_data_chunk(self, count: int) -> List[Dict[str, Any]]:
        """Generate a chunk of count data"""
        return [CountDataFactory() for _ in range(count)]
```

### 📋 Implementation Checklist

#### Setup Phase
- [ ] Install required dependencies (factory_boy, faker)
- [ ] Configure data factories
- [ ] Setup data masking utilities
- [ ] Implement cleanup strategies
- [ ] Create validation rules

#### Development Phase
- [ ] Create test data generators
- [ ] Implement data builders
- [ ] Setup fixtures
- [ ] Configure data validation
- [ ] Optimize data generation

#### Testing Phase
- [ ] Test data generation performance
- [ ] Validate data quality
- [ ] Test cleanup procedures
- [ ] Verify data privacy protection
- [ ] Test data consistency

#### Production Phase
- [ ] Monitor data generation performance
- [ ] Track data quality metrics
- [ ] Optimize based on usage patterns
- [ ] Update data schemas as needed
- [ ] Maintain data privacy compliance

### 🎯 Success Metrics

#### Performance Metrics
- **Data Generation Speed**: < 1 second for 1000 records
- **Memory Usage**: < 100MB for large datasets
- **Cleanup Time**: < 5 seconds for complete cleanup
- **Validation Speed**: < 100ms per record

#### Quality Metrics
- **Data Consistency**: 100% referential integrity
- **Data Completeness**: > 95% required fields populated
- **Data Accuracy**: > 99% valid data formats
- **Privacy Compliance**: 100% sensitive data masked

#### Operational Metrics
- **Test Execution Time**: < 30% increase due to data setup
- **Test Reliability**: > 95% test success rate
- **Data Reusability**: > 80% data reuse across tests
- **Maintenance Effort**: < 2 hours per week

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 