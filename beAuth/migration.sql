-- Migration script to add missing tables for test cases
-- Run this script to update the database schema

-- Connect to the database
\c people_counting_db;

-- Create registration_codes table
CREATE TABLE IF NOT EXISTS registration_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name TEXT,
    description TEXT,
    max_uses INTEGER DEFAULT 1,
    used_count INTEGER DEFAULT 0,
    current_uses INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create refresh_tokens table (separate from user_sessions for better management)
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for new tables
CREATE INDEX IF NOT EXISTS idx_registration_codes_code ON registration_codes(code);
CREATE INDEX IF NOT EXISTS idx_registration_codes_active ON registration_codes(is_active);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_revoked ON refresh_tokens(is_revoked);

-- Create trigger for registration_codes updated_at
DROP TRIGGER IF EXISTS update_registration_codes_updated_at ON registration_codes;
CREATE TRIGGER update_registration_codes_updated_at 
    BEFORE UPDATE ON registration_codes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for refresh_tokens updated_at
DROP TRIGGER IF EXISTS update_refresh_tokens_updated_at ON refresh_tokens;
CREATE TRIGGER update_refresh_tokens_updated_at 
    BEFORE UPDATE ON refresh_tokens 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert test registration codes
INSERT INTO registration_codes (code, description, max_uses, is_active, expires_at)
VALUES 
    ('REG001', 'Test registration code for development', 100, true, '2025-12-31 23:59:59'),
    ('REG002', 'Another test registration code', 50, true, '2025-12-31 23:59:59'),
    ('EXPIRED', 'Expired registration code', 10, false, '2024-01-01 00:00:00'),
    ('LIMITED', 'Limited use registration code', 1, true, '2025-12-31 23:59:59')
ON CONFLICT (code) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON TABLE registration_codes TO postgres;
GRANT ALL PRIVILEGES ON TABLE refresh_tokens TO postgres;
GRANT ALL PRIVILEGES ON SEQUENCE registration_codes_id_seq TO postgres;
GRANT ALL PRIVILEGES ON SEQUENCE refresh_tokens_id_seq TO postgres;

-- Log completion
SELECT 'Migration completed successfully! Added registration_codes and refresh_tokens tables.' as status; 