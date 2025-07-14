# Enterprise-Grade Security & Compliance - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày các tiêu chuẩn bảo mật enterprise-grade và compliance requirements cho hệ thống AI Camera Counting, bao gồm SOC2, ISO27001, PCI DSS, và GDPR compliance.

## 🎯 Enterprise Security Objectives

- **SOC2 Compliance**: Đạt chứng nhận SOC2 Type II
- **ISO27001 Certification**: Tuân thủ tiêu chuẩn ISO27001
- **PCI DSS Compliance**: Đảm bảo bảo mật dữ liệu thanh toán
- **GDPR Compliance**: Tuân thủ quy định bảo vệ dữ liệu EU
- **Zero Trust Architecture**: Triển khai mô hình zero trust
- **Continuous Security Monitoring**: Giám sát bảo mật liên tục

## 🏗️ Enterprise Security Architecture

### Zero Trust Security Model

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ZERO TRUST SECURITY ARCHITECTURE                   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              IDENTITY & ACCESS MANAGEMENT                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Multi-    │  │   Role-     │  │   Privileged│  │   Identity  │        │ │
│  │  │   Factor    │  │   Based     │  │   Access    │  │   Federation│        │ │
│  │  │   Auth      │  │   Access    │  │   Management│  │             │        │ │
│  │  │             │  │   Control   │  │             │  │             │        │ │
│  │  │ • Biometric │  │ • RBAC      │  │ • PAM       │  │ • SSO       │        │ │
│  │  │   Auth      │  │ • ABAC      │  │ • Just-in-  │  │ • SAML      │        │ │
│  │  │ • Hardware  │  │ • Dynamic   │  │   Time      │  │ • OAuth 2.0 │        │ │
│  │  │   Tokens    │  │   Access    │  │   Access    │  │ • OIDC      │        │ │
│  │  │ • Smart     │  │ • Context-  │  │ • Session   │  │ • LDAP      │        │ │
│  │  │   Cards     │  │   Aware     │  │   Recording │  │   Integration│       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              NETWORK SECURITY LAYER                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Network   │  │   Micro-    │  │   API       │  │   DDoS      │        │ │
│  │  │   Segmentation│   Segmentation│   Security   │  │   Protection│        │ │
│  │  │             │  │             │  │   Gateway   │  │             │        │ │
│  │  │ • VLAN      │  │ • Service   │  │             │  │ • Rate      │        │ │
│  │  │   Isolation │  │   Mesh      │  │ • API       │  │   Limiting  │        │ │
│  │  │ • Firewall  │  │ • Network   │  │   Keys      │  │ • Traffic   │        │ │
│  │  │   Rules     │  │   Policies  │  │ • OAuth 2.0 │  │   Filtering │        │ │
│  │  │ • VPN       │  │ • Zero-     │  │ • Rate      │  │ • Bot       │        │ │
│  │  │   Tunnels   │  │   Trust     │  │   Limiting  │  │   Detection │        │ │
│  │  │ • SDN       │  │   Network   │  │ • WAF       │  │ • Geo-      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA SECURITY LAYER                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Data      │  │   Database  │  │   File      │  │   Backup    │        │ │
│  │  │   Encryption│  │   Security  │  │   Security  │  │   Security  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • AES-256   │  │ • TDE       │  │ • File      │  │ • Encrypted │        │ │
│  │  │   Encryption│  │ • Column-   │  │   Encryption│  │   Backups   │        │ │
│  │  │ • Key       │  │   Level     │  │ • Access    │  │ • Secure    │        │ │
│  │  │   Management│  │   Encryption│  │   Control   │  │   Storage   │        │ │
│  │  │ • HSM       │  │ • Row-Level │  │ • DLP       │  │ • Air-gapped│        │ │
│  │  │   Integration│  │   Security  │  │ • Data      │  │   Backup    │        │ │
│  │  │ • KMS       │  │ • Audit     │  │   Loss      │  │ • Immutable │        │ │
│  │  │   Services  │  │   Logging   │  │   Prevention│  │   Storage   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔐 SOC2 Compliance Implementation

### SOC2 Trust Service Criteria

```sql
-- SOC2 compliance tracking
CREATE TABLE soc2_compliance (
    id SERIAL PRIMARY KEY,
    trust_service VARCHAR(20) NOT NULL, -- CC, DC, PR, PI, AI
    control_id VARCHAR(50) NOT NULL,
    control_name VARCHAR(200) NOT NULL,
    control_description TEXT,
    implementation_status VARCHAR(20) DEFAULT 'pending', -- pending, implemented, tested, certified
    last_assessment_date DATE,
    next_assessment_date DATE,
    compliance_evidence TEXT,
    risk_level VARCHAR(20), -- low, medium, high, critical
    remediation_required BOOLEAN DEFAULT FALSE,
    remediation_plan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define SOC2 controls
INSERT INTO soc2_compliance (trust_service, control_id, control_name, control_description) VALUES
-- Common Criteria (CC)
('CC', 'CC1.1', 'Control Environment', 'Entity demonstrates commitment to integrity and ethical values'),
('CC', 'CC2.1', 'Communication and Information', 'Entity communicates information to support functioning of internal control'),
('CC', 'CC3.1', 'Risk Assessment', 'Entity demonstrates commitment to identify and assess risks'),
('CC', 'CC4.1', 'Monitoring Activities', 'Entity demonstrates commitment to evaluate and remediate deficiencies'),
('CC', 'CC5.1', 'Control Activities', 'Entity demonstrates commitment to develop and perform control activities'),

-- Availability (AI)
('AI', 'AI1.1', 'Availability', 'Entity maintains, monitors, and evaluates current processing capacity and use of system resources'),
('AI', 'AI2.1', 'System Processing', 'Entity implements logical access security software, infrastructure, and architectures'),
('AI', 'AI3.1', 'System Operations', 'Entity implements procedures to detect, identify, and respond to security events'),

-- Security (CC)
('CC', 'CC6.1', 'Logical and Physical Access Controls', 'Entity implements logical and physical access controls'),
('CC', 'CC6.2', 'System Operations', 'Entity implements procedures to detect, identify, and respond to security events'),
('CC', 'CC6.3', 'Change Management', 'Entity implements procedures to detect, identify, and respond to security events'),
('CC', 'CC6.4', 'Risk Mitigation', 'Entity implements procedures to detect, identify, and respond to security events'),

-- Confidentiality (PI)
('PI', 'PI1.1', 'Information Disposal', 'Entity disposes of information, software, or hardware to meet the entity''s objectives'),
('PI', 'PI2.1', 'System Processing', 'Entity implements logical access security software, infrastructure, and architectures'),
('PI', 'PI3.1', 'System Operations', 'Entity implements procedures to detect, identify, and respond to security events'),

-- Privacy (PR)
('PR', 'PR1.1', 'Notice and Communication of Objectives', 'Entity provides notice to data subjects about its privacy practices'),
('PR', 'PR2.1', 'Choice and Consent', 'Entity communicates choices available regarding the collection, use, retention, disclosure, and disposal of personal information'),
('PR', 'PR3.1', 'Collection', 'Entity collects personal information consistent with the entity''s objectives related to privacy'),
('PR', 'PR4.1', 'Use, Retention, and Disposal', 'Entity uses, retains, and disposes of personal information consistent with the entity''s objectives related to privacy'),
('PR', 'PR5.1', 'Access', 'Entity provides data subjects with access to their personal information for review and update'),
('PR', 'PR6.1', 'Disclosure and Notification', 'Entity discloses personal information to third parties only for the purposes identified and disclosed to data subjects'),
('PR', 'PR7.1', 'Quality', 'Entity maintains accurate, complete, and relevant personal information for the purposes identified in the entity''s objectives related to privacy'),
('PR', 'PR8.1', 'Monitoring and Enforcement', 'Entity monitors compliance with its objectives related to privacy and takes action to address noncompliance');

-- SOC2 assessment tracking
CREATE TABLE soc2_assessments (
    id SERIAL PRIMARY KEY,
    assessment_period VARCHAR(20) NOT NULL, -- Q1-2024, Q2-2024, etc.
    assessment_type VARCHAR(20) NOT NULL, -- Type I, Type II
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    auditor VARCHAR(100),
    overall_status VARCHAR(20) DEFAULT 'in_progress', -- in_progress, completed, failed
    findings_count INTEGER DEFAULT 0,
    critical_findings INTEGER DEFAULT 0,
    remediation_required BOOLEAN DEFAULT FALSE,
    certification_date DATE,
    next_assessment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SOC2 evidence collection
CREATE TABLE soc2_evidence (
    id SERIAL PRIMARY KEY,
    control_id VARCHAR(50) NOT NULL,
    evidence_type VARCHAR(50) NOT NULL, -- policy, procedure, log, test, interview
    evidence_description TEXT NOT NULL,
    evidence_file_path VARCHAR(500),
    evidence_date DATE NOT NULL,
    collected_by VARCHAR(100),
    reviewed_by VARCHAR(100),
    review_date DATE,
    is_approved BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛡️ ISO27001 Implementation

### ISO27001 Controls Framework

```sql
-- ISO27001 controls management
CREATE TABLE iso27001_controls (
    id SERIAL PRIMARY KEY,
    control_category VARCHAR(50) NOT NULL, -- A.5, A.6, A.7, etc.
    control_id VARCHAR(20) NOT NULL,
    control_name VARCHAR(200) NOT NULL,
    control_description TEXT,
    implementation_status VARCHAR(20) DEFAULT 'planned', -- planned, implemented, monitored, improved
    risk_assessment VARCHAR(20), -- low, medium, high
    implementation_date DATE,
    last_review_date DATE,
    next_review_date DATE,
    responsible_person VARCHAR(100),
    documentation_reference VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define ISO27001 controls
INSERT INTO iso27001_controls (control_category, control_id, control_name, control_description) VALUES
-- A.5 Information Security Policies
('A.5', 'A.5.1', 'Information Security Policy', 'Management direction for information security'),
('A.5', 'A.5.2', 'Information Security Policy Review', 'Regular review and update of security policies'),

-- A.6 Organization of Information Security
('A.6', 'A.6.1', 'Internal Organization', 'Information security roles and responsibilities'),
('A.6', 'A.6.2', 'Mobile Device Policy', 'Security requirements for mobile devices'),
('A.6', 'A.6.3', 'Teleworking', 'Security requirements for teleworking'),

-- A.7 Human Resource Security
('A.7', 'A.7.1', 'Prior to Employment', 'Background verification checks'),
('A.7', 'A.7.2', 'During Employment', 'Security awareness and training'),
('A.7', 'A.7.3', 'Termination and Change of Employment', 'Return of assets and access removal'),

-- A.8 Asset Management
('A.8', 'A.8.1', 'Responsibility for Assets', 'Inventory and ownership of information assets'),
('A.8', 'A.8.2', 'Information Classification', 'Classification of information assets'),
('A.8', 'A.8.3', 'Media Handling', 'Secure handling of storage media'),

-- A.9 Access Control
('A.9', 'A.9.1', 'Business Requirements of Access Control', 'Access control policy'),
('A.9', 'A.9.2', 'User Access Management', 'User registration and de-registration'),
('A.9', 'A.9.3', 'User Responsibilities', 'Password use and security'),
('A.9', 'A.9.4', 'System and Application Access Control', 'Secure log-on procedures'),

-- A.10 Cryptography
('A.10', 'A.10.1', 'Cryptographic Controls', 'Encryption policy and procedures'),
('A.10', 'A.10.2', 'Key Management', 'Cryptographic key management'),

-- A.11 Physical and Environmental Security
('A.11', 'A.11.1', 'Secure Areas', 'Physical security perimeters'),
('A.11', 'A.11.2', 'Equipment', 'Equipment placement and protection'),

-- A.12 Operations Security
('A.12', 'A.12.1', 'Operational Procedures and Responsibilities', 'Documented operating procedures'),
('A.12', 'A.12.2', 'Protection from Malware', 'Malware protection controls'),
('A.12', 'A.12.3', 'Backup', 'Regular backup of information'),
('A.12', 'A.12.4', 'Logging and Monitoring', 'Event logging and monitoring'),
('A.12', 'A.12.5', 'Control of Operational Software', 'Installation of software on operational systems'),
('A.12', 'A.12.6', 'Technical Vulnerability Management', 'Timely application of security patches'),
('A.12', 'A.12.7', 'Information Systems Audit Considerations', 'Protection of audit tools'),

-- A.13 Communications Security
('A.13', 'A.13.1', 'Network Security Management', 'Network security controls'),
('A.13', 'A.13.2', 'Information Transfer', 'Secure information transfer procedures'),

-- A.14 System Acquisition, Development and Maintenance
('A.14', 'A.14.1', 'Security Requirements of Information Systems', 'Security requirements analysis'),
('A.14', 'A.14.2', 'Security in Development and Support Processes', 'Secure development practices'),
('A.14', 'A.14.3', 'Test Data', 'Protection of test data'),

-- A.15 Supplier Relationships
('A.15', 'A.15.1', 'Supplier Service Delivery Management', 'Supplier service monitoring'),
('A.15', 'A.15.2', 'Supplier Service Development and Improvement', 'Supplier service improvement'),

-- A.16 Information Security Incident Management
('A.16', 'A.16.1', 'Management of Information Security Incidents and Improvements', 'Incident management procedures'),

-- A.17 Information Security Aspects of Business Continuity Management
('A.17', 'A.17.1', 'Information Security Continuity', 'Business continuity planning'),
('A.17', 'A.17.2', 'Redundancies', 'Redundant information processing facilities'),

-- A.18 Compliance
('A.18', 'A.18.1', 'Compliance with Legal and Contractual Requirements', 'Legal and regulatory compliance'),
('A.18', 'A.18.2', 'Information Security Reviews', 'Independent review of information security');

-- ISO27001 risk assessment
CREATE TABLE iso27001_risk_assessment (
    id SERIAL PRIMARY KEY,
    asset_id VARCHAR(50) NOT NULL,
    threat_source VARCHAR(100) NOT NULL,
    threat_type VARCHAR(100) NOT NULL,
    vulnerability_description TEXT,
    likelihood INTEGER CHECK (likelihood BETWEEN 1 AND 5),
    impact INTEGER CHECK (impact BETWEEN 1 AND 5),
    risk_level INTEGER GENERATED ALWAYS AS (likelihood * impact) STORED,
    risk_rating VARCHAR(20) GENERATED ALWAYS AS (
        CASE 
            WHEN likelihood * impact <= 4 THEN 'LOW'
            WHEN likelihood * impact <= 8 THEN 'MEDIUM'
            WHEN likelihood * impact <= 15 THEN 'HIGH'
            ELSE 'CRITICAL'
        END
    ) STORED,
    mitigation_controls TEXT,
    residual_risk INTEGER,
    assessment_date DATE DEFAULT CURRENT_DATE,
    next_review_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 💳 PCI DSS Compliance

### PCI DSS Requirements Implementation

```sql
-- PCI DSS compliance tracking
CREATE TABLE pci_dss_compliance (
    id SERIAL PRIMARY KEY,
    requirement_id VARCHAR(10) NOT NULL, -- 1.1, 1.2, 2.1, etc.
    requirement_title VARCHAR(200) NOT NULL,
    requirement_description TEXT,
    implementation_status VARCHAR(20) DEFAULT 'not_implemented', -- not_implemented, partially_implemented, implemented, tested, validated
    last_assessment_date DATE,
    next_assessment_date DATE,
    compliance_evidence TEXT,
    compensating_controls TEXT,
    risk_level VARCHAR(20), -- low, medium, high, critical
    remediation_required BOOLEAN DEFAULT FALSE,
    remediation_deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define PCI DSS requirements
INSERT INTO pci_dss_compliance (requirement_id, requirement_title, requirement_description) VALUES
-- Build and Maintain a Secure Network and Systems
('1.1', 'Firewall Configuration', 'Establish and implement firewall and router configuration standards'),
('1.2', 'Firewall Configuration', 'Build firewall and router configurations that restrict connections'),
('1.3', 'Firewall Configuration', 'Prohibit direct public access between the Internet and any system component'),
('1.4', 'Firewall Configuration', 'Install personal firewall software on any mobile and/or employee-owned computers'),
('1.5', 'Firewall Configuration', 'Document business justification and approval for use of all services'),
('1.6', 'Firewall Configuration', 'Document groups, roles, and responsibilities for logical access management'),
('1.7', 'Firewall Configuration', 'Require documented approval by authorized parties for all network connections'),
('1.8', 'Firewall Configuration', 'Implement a formal process for testing and approval of all network connections'),
('1.9', 'Firewall Configuration', 'Implement a formal process for testing and approval of all network connections'),

-- Protect Cardholder Data
('3.1', 'Data Protection', 'Keep cardholder data storage to a minimum'),
('3.2', 'Data Protection', 'Do not store sensitive authentication data after authorization'),
('3.3', 'Data Protection', 'Mask PAN when displayed'),
('3.4', 'Data Protection', 'Render PAN unreadable anywhere it is stored'),
('3.5', 'Data Protection', 'Document and implement procedures to protect keys'),
('3.6', 'Data Protection', 'Fully document and implement all key-management processes'),

-- Maintain Vulnerability Management Program
('5.1', 'Malware Protection', 'Deploy anti-virus software on all systems commonly affected by malicious software'),
('5.2', 'Malware Protection', 'Ensure that all anti-virus mechanisms are current, actively running, and capable of generating audit logs'),
('5.3', 'Malware Protection', 'Ensure that anti-virus mechanisms are actively running and cannot be disabled or altered by users'),

-- Implement Strong Access Control Measures
('7.1', 'Access Control', 'Limit access to system components and cardholder data to only those individuals whose job requires such access'),
('7.2', 'Access Control', 'Establish an access control system for systems components that restricts access based on a user''s need to know'),
('8.1', 'Access Control', 'Define and implement policies and procedures to ensure proper user identification management'),
('8.2', 'Access Control', 'In addition to assigning a unique ID, employ at least one of the following methods to authenticate all users'),
('8.3', 'Access Control', 'Secure all individual access into any database containing cardholder data'),
('8.4', 'Access Control', 'Document and communicate authentication procedures and policies to all users'),
('8.5', 'Access Control', 'Do not use group, shared, or generic IDs, passwords, or other authentication methods'),
('8.6', 'Access Control', 'Where other authentication mechanisms are used, these must be assigned to an individual account'),
('8.7', 'Access Control', 'All access to any database containing cardholder data is restricted'),

-- Regularly Monitor and Test Networks
('10.1', 'Audit Logs', 'Implement audit trails to link all access to system components to each individual user'),
('10.2', 'Audit Logs', 'Implement automated audit trails for all system components to reconstruct the following events'),
('10.3', 'Audit Logs', 'Record at least the following audit trail entries for all system components for each event'),
('10.4', 'Audit Logs', 'Using time-synchronization technology, synchronize all critical system clocks and times'),
('10.5', 'Audit Logs', 'Secure audit trails so they cannot be altered'),
('10.6', 'Audit Logs', 'Review logs and security events for all system components to identify anomalies or suspicious activity'),
('10.7', 'Audit Logs', 'Retain audit trail history for at least one year, with a minimum of three months immediately available'),

-- Maintain Information Security Policy
('12.1', 'Security Policy', 'Establish, publish, maintain, and disseminate a security policy'),
('12.2', 'Security Policy', 'Implement a risk-assessment process that is performed at least annually'),
('12.3', 'Security Policy', 'Develop usage policies for critical technologies and define proper use of these technologies'),
('12.4', 'Security Policy', 'Ensure that the security policy and procedures clearly define information security responsibilities'),
('12.5', 'Security Policy', 'Assign to an individual or team the following information security management responsibilities'),
('12.6', 'Security Policy', 'Implement a formal security awareness program to make all personnel aware of the importance of cardholder data security'),
('12.7', 'Security Policy', 'Screen potential personnel prior to hire to minimize the risk of attacks from internal sources'),
('12.8', 'Security Policy', 'Maintain and implement policies and procedures to manage service providers'),
('12.9', 'Security Policy', 'Implement an incident response plan'),
('12.10', 'Security Policy', 'Create the incident response plan to be implemented in the event of system breach'),
('12.11', 'Security Policy', 'Ensure that the incident response plan addresses the following'),
('12.12', 'Security Policy', 'Additional requirements for service providers only');

-- PCI DSS assessment tracking
CREATE TABLE pci_dss_assessments (
    id SERIAL PRIMARY KEY,
    assessment_type VARCHAR(20) NOT NULL, -- SAQ, ROC, QSA Assessment
    assessment_period VARCHAR(20) NOT NULL, -- Q1-2024, Annual-2024
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    assessor VARCHAR(100),
    overall_compliance_status VARCHAR(20) DEFAULT 'in_progress', -- in_progress, compliant, non_compliant
    requirements_compliant INTEGER DEFAULT 0,
    requirements_total INTEGER DEFAULT 0,
    compliance_percentage DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN requirements_total > 0 THEN (requirements_compliant * 100.0) / requirements_total
            ELSE 0
        END
    ) STORED,
    findings_count INTEGER DEFAULT 0,
    critical_findings INTEGER DEFAULT 0,
    remediation_required BOOLEAN DEFAULT FALSE,
    certification_date DATE,
    next_assessment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔒 GDPR Compliance Implementation

### GDPR Data Protection Framework

```sql
-- GDPR compliance management
CREATE TABLE gdpr_compliance (
    id SERIAL PRIMARY KEY,
    article_id VARCHAR(20) NOT NULL, -- Article 5, Article 6, etc.
    requirement_title VARCHAR(200) NOT NULL,
    requirement_description TEXT,
    implementation_status VARCHAR(20) DEFAULT 'not_implemented', -- not_implemented, implemented, tested, compliant
    data_processing_purpose VARCHAR(100),
    legal_basis VARCHAR(100), -- consent, legitimate_interest, contract, legal_obligation
    data_retention_period INTERVAL,
    last_assessment_date DATE,
    next_assessment_date DATE,
    compliance_evidence TEXT,
    risk_assessment VARCHAR(20), -- low, medium, high
    dpo_review_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define GDPR requirements
INSERT INTO gdpr_compliance (article_id, requirement_title, requirement_description) VALUES
-- Article 5 - Principles relating to processing of personal data
('Article 5', 'Lawfulness, fairness and transparency', 'Personal data shall be processed lawfully, fairly and in a transparent manner'),
('Article 5', 'Purpose limitation', 'Personal data shall be collected for specified, explicit and legitimate purposes'),
('Article 5', 'Data minimisation', 'Personal data shall be adequate, relevant and limited to what is necessary'),
('Article 5', 'Accuracy', 'Personal data shall be accurate and, where necessary, kept up to date'),
('Article 5', 'Storage limitation', 'Personal data shall be kept in a form which permits identification for no longer than is necessary'),
('Article 5', 'Integrity and confidentiality', 'Personal data shall be processed in a manner that ensures appropriate security'),

-- Article 6 - Lawfulness of processing
('Article 6', 'Legal basis for processing', 'Processing shall be lawful only if and to the extent that at least one of the following applies'),
('Article 6', 'Consent', 'The data subject has given consent to the processing'),
('Article 6', 'Contract', 'Processing is necessary for the performance of a contract'),
('Article 6', 'Legal obligation', 'Processing is necessary for compliance with a legal obligation'),
('Article 6', 'Vital interests', 'Processing is necessary to protect the vital interests of the data subject'),
('Article 6', 'Public task', 'Processing is necessary for the performance of a task carried out in the public interest'),
('Article 6', 'Legitimate interests', 'Processing is necessary for the purposes of legitimate interests'),

-- Article 7 - Conditions for consent
('Article 7', 'Conditions for consent', 'Where processing is based on consent, the controller shall be able to demonstrate that consent was given'),
('Article 7', 'Withdrawal of consent', 'The data subject shall have the right to withdraw his or her consent at any time'),

-- Article 12 - Transparent information
('Article 12', 'Transparent information', 'The controller shall take appropriate measures to provide information to the data subject'),
('Article 12', 'Information in writing', 'The information shall be provided in writing or by other means'),

-- Article 15 - Right of access
('Article 15', 'Right of access', 'The data subject shall have the right to obtain confirmation of processing'),
('Article 15', 'Information to be provided', 'The controller shall provide information about the processing'),

-- Article 16 - Right to rectification
('Article 16', 'Right to rectification', 'The data subject shall have the right to obtain rectification of inaccurate personal data'),

-- Article 17 - Right to erasure
('Article 17', 'Right to erasure', 'The data subject shall have the right to obtain erasure of personal data'),

-- Article 18 - Right to restriction
('Article 18', 'Right to restriction', 'The data subject shall have the right to obtain restriction of processing'),

-- Article 20 - Right to data portability
('Article 20', 'Right to data portability', 'The data subject shall have the right to receive personal data in a structured format'),

-- Article 21 - Right to object
('Article 21', 'Right to object', 'The data subject shall have the right to object to processing'),

-- Article 25 - Data protection by design
('Article 25', 'Data protection by design', 'The controller shall implement appropriate technical and organisational measures'),
('Article 25', 'Data protection by default', 'The controller shall implement appropriate technical and organisational measures'),

-- Article 30 - Records of processing activities
('Article 30', 'Records of processing activities', 'Each controller shall maintain a record of processing activities'),

-- Article 32 - Security of processing
('Article 32', 'Security of processing', 'The controller and the processor shall implement appropriate technical and organisational measures'),

-- Article 33 - Notification of personal data breach
('Article 33', 'Notification of breach', 'In the case of a personal data breach, the controller shall notify the supervisory authority'),

-- Article 34 - Communication of personal data breach
('Article 34', 'Communication of breach', 'When the personal data breach is likely to result in a high risk to the rights and freedoms'),

-- Article 35 - Data protection impact assessment
('Article 35', 'Data protection impact assessment', 'Where a type of processing is likely to result in a high risk to the rights and freedoms'),

-- Article 37 - Designation of data protection officer
('Article 37', 'Designation of DPO', 'The controller and the processor shall designate a data protection officer'),

-- Article 47 - Binding corporate rules
('Article 47', 'Binding corporate rules', 'The competent supervisory authority shall approve binding corporate rules'),

-- Article 83 - General conditions for imposing administrative fines
('Article 83', 'Administrative fines', 'Each supervisory authority shall ensure that the imposition of administrative fines'),

-- Article 84 - Penalties
('Article 84', 'Penalties', 'Member States shall lay down the rules on other penalties applicable to infringements'),

-- Article 85 - Processing and freedom of expression
('Article 85', 'Freedom of expression', 'Member States shall by law reconcile the right to the protection of personal data'),

-- Article 86 - Processing and public access to official documents
('Article 86', 'Public access', 'Personal data in official documents held by a public authority or a public body'),

-- Article 87 - Processing of the national identification number
('Article 87', 'National identification number', 'Member States may further determine the specific conditions for the processing'),

-- Article 88 - Processing in the context of employment
('Article 88', 'Employment context', 'Member States may, by law or by collective agreements, provide for more specific rules'),

-- Article 89 - Safeguards and derogations
('Article 89', 'Safeguards and derogations', 'Processing for archiving purposes in the public interest, scientific or historical research purposes'),

-- Article 90 - Obligations of secrecy
('Article 90', 'Obligations of secrecy', 'Member States may adopt specific rules to set out the powers of the supervisory authorities'),

-- Article 91 - Existing data protection rules of churches
('Article 91', 'Churches and religious associations', 'Where in a Member State, churches and religious associations or communities apply'),

-- Article 92 - Exercise of the delegation
('Article 92', 'Exercise of the delegation', 'The power to adopt delegated acts is conferred on the Commission subject to the conditions'),

-- Article 93 - Committee procedure
('Article 93', 'Committee procedure', 'The Commission shall be assisted by a committee'),

-- Article 94 - Repeal of Directive 95/46/EC
('Article 94', 'Repeal of Directive 95/46/EC', 'Directive 95/46/EC is repealed with effect from 25 May 2018'),

-- Article 95 - Relationship with Directive 2002/58/EC
('Article 95', 'Relationship with Directive 2002/58/EC', 'This Regulation shall not impose additional obligations on natural or legal persons'),

-- Article 96 - Relationship with previously concluded Agreements
('Article 96', 'Relationship with previously concluded Agreements', 'International agreements involving the transfer of personal data'),

-- Article 97 - Commission reports
('Article 97', 'Commission reports', 'By 25 May 2020 and every four years thereafter, the Commission shall submit a report'),

-- Article 98 - Review of other Union legal acts on data protection
('Article 98', 'Review of other Union legal acts', 'The Commission shall, if appropriate, submit legislative proposals'),

-- Article 99 - Entry into force and application
('Article 99', 'Entry into force and application', 'This Regulation shall enter into force on the twentieth day following that of its publication'),

-- Article 100 - Repeal of Directive 95/46/EC
('Article 100', 'Repeal of Directive 95/46/EC', 'Directive 95/46/EC is repealed with effect from 25 May 2018');

-- GDPR data processing activities
CREATE TABLE gdpr_data_processing (
    id SERIAL PRIMARY KEY,
    processing_activity_name VARCHAR(200) NOT NULL,
    processing_purpose TEXT NOT NULL,
    legal_basis VARCHAR(100) NOT NULL,
    data_categories TEXT[] NOT NULL,
    data_subject_categories TEXT[] NOT NULL,
    data_retention_period INTERVAL,
    data_recipients TEXT[],
    third_country_transfers BOOLEAN DEFAULT FALSE,
    third_country_name VARCHAR(100),
    safeguards_implemented TEXT,
    risk_assessment VARCHAR(20), -- low, medium, high
    dpo_consultation_required BOOLEAN DEFAULT FALSE,
    dpia_required BOOLEAN DEFAULT FALSE,
    dpia_status VARCHAR(20) DEFAULT 'not_required', -- not_required, required, in_progress, completed
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GDPR data subject rights
CREATE TABLE gdpr_data_subject_rights (
    id SERIAL PRIMARY KEY,
    data_subject_id VARCHAR(100) NOT NULL,
    right_type VARCHAR(50) NOT NULL, -- access, rectification, erasure, portability, objection
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    request_description TEXT,
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, rejected
    response_date TIMESTAMP,
    response_description TEXT,
    verification_method VARCHAR(100),
    verification_date TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    processing_time_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GDPR data breaches
CREATE TABLE gdpr_data_breaches (
    id SERIAL PRIMARY KEY,
    breach_description TEXT NOT NULL,
    breach_date TIMESTAMP NOT NULL,
    discovery_date TIMESTAMP NOT NULL,
    breach_type VARCHAR(100) NOT NULL, -- unauthorized_access, data_loss, system_breach
    affected_data_categories TEXT[],
    affected_data_subjects INTEGER,
    risk_level VARCHAR(20) NOT NULL, -- low, medium, high
    notification_required BOOLEAN DEFAULT FALSE,
    supervisory_authority_notified BOOLEAN DEFAULT FALSE,
    notification_date TIMESTAMP,
    data_subjects_notified BOOLEAN DEFAULT FALSE,
    notification_deadline TIMESTAMP,
    containment_measures TEXT,
    remediation_actions TEXT,
    lessons_learned TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 Compliance Monitoring and Reporting

### Compliance Dashboard

```sql
-- Compliance monitoring view
CREATE VIEW compliance_dashboard AS
SELECT 
    'SOC2' as compliance_framework,
    COUNT(*) as total_controls,
    COUNT(CASE WHEN implementation_status = 'certified' THEN 1 END) as implemented_controls,
    ROUND(
        (COUNT(CASE WHEN implementation_status = 'certified' THEN 1 END) * 100.0) / COUNT(*), 2
    ) as compliance_percentage
FROM soc2_compliance

UNION ALL

SELECT 
    'ISO27001' as compliance_framework,
    COUNT(*) as total_controls,
    COUNT(CASE WHEN implementation_status = 'implemented' THEN 1 END) as implemented_controls,
    ROUND(
        (COUNT(CASE WHEN implementation_status = 'implemented' THEN 1 END) * 100.0) / COUNT(*), 2
    ) as compliance_percentage
FROM iso27001_controls

UNION ALL

SELECT 
    'PCI DSS' as compliance_framework,
    COUNT(*) as total_controls,
    COUNT(CASE WHEN implementation_status = 'validated' THEN 1 END) as implemented_controls,
    ROUND(
        (COUNT(CASE WHEN implementation_status = 'validated' THEN 1 END) * 100.0) / COUNT(*), 2
    ) as compliance_percentage
FROM pci_dss_compliance

UNION ALL

SELECT 
    'GDPR' as compliance_framework,
    COUNT(*) as total_controls,
    COUNT(CASE WHEN implementation_status = 'compliant' THEN 1 END) as implemented_controls,
    ROUND(
        (COUNT(CASE WHEN implementation_status = 'compliant' THEN 1 END) * 100.0) / COUNT(*), 2
    ) as compliance_percentage
FROM gdpr_compliance;

-- Compliance risk assessment
CREATE VIEW compliance_risk_assessment AS
SELECT 
    'SOC2' as framework,
    control_id,
    control_name,
    risk_level,
    implementation_status,
    remediation_required
FROM soc2_compliance
WHERE risk_level IN ('high', 'critical') OR remediation_required = TRUE

UNION ALL

SELECT 
    'ISO27001' as framework,
    control_id,
    control_name,
    risk_assessment as risk_level,
    implementation_status,
    FALSE as remediation_required
FROM iso27001_controls
WHERE risk_assessment IN ('high', 'critical')

UNION ALL

SELECT 
    'PCI DSS' as framework,
    requirement_id as control_id,
    requirement_title as control_name,
    risk_level,
    implementation_status,
    remediation_required
FROM pci_dss_compliance
WHERE risk_level IN ('high', 'critical') OR remediation_required = TRUE

UNION ALL

SELECT 
    'GDPR' as framework,
    article_id as control_id,
    requirement_title as control_name,
    risk_assessment as risk_level,
    implementation_status,
    FALSE as remediation_required
FROM gdpr_compliance
WHERE risk_assessment IN ('high', 'critical');

-- Compliance reporting function
CREATE OR REPLACE FUNCTION generate_compliance_report(
    p_framework VARCHAR(20) DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    report JSONB;
BEGIN
    SELECT jsonb_build_object(
        'report_generated_at', NOW(),
        'compliance_overview', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'framework', compliance_framework,
                    'total_controls', total_controls,
                    'implemented_controls', implemented_controls,
                    'compliance_percentage', compliance_percentage
                )
            )
            FROM compliance_dashboard
            WHERE p_framework IS NULL OR compliance_framework = p_framework
        ),
        'high_risk_items', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'framework', framework,
                    'control_id', control_id,
                    'control_name', control_name,
                    'risk_level', risk_level,
                    'implementation_status', implementation_status,
                    'remediation_required', remediation_required
                )
            )
            FROM compliance_risk_assessment
            WHERE p_framework IS NULL OR framework = p_framework
        ),
        'upcoming_assessments', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'framework', 'SOC2',
                    'assessment_type', assessment_type,
                    'next_assessment_date', next_assessment_date
                )
            )
            FROM soc2_assessments
            WHERE next_assessment_date <= NOW() + INTERVAL '90 days'
        )
    ) INTO report;
    
    RETURN report;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Enterprise-Grade Security & Compliance, đảm bảo tuân thủ các tiêu chuẩn quốc tế và bảo vệ dữ liệu ở mức cao nhất.** 