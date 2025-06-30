const { executeQuery } = require('../config/database');
const logger = require('../utils/logger');

// Database migration script
async function runMigrations() {
  try {
    logger.info('Starting database migrations...');

    // Create users table
    const createUsersTable = `
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
        is_active BOOLEAN DEFAULT TRUE,
        last_login TIMESTAMP,
        reset_password_token VARCHAR(255),
        reset_password_expires TIMESTAMP,
        email_verification_token VARCHAR(255),
        email_verified BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // Create user_sessions table
    const createUserSessionsTable = `
      CREATE TABLE IF NOT EXISTS user_sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        session_token VARCHAR(255) UNIQUE NOT NULL,
        refresh_token VARCHAR(255) UNIQUE NOT NULL,
        ip_address INET,
        user_agent TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // Create audit_log table
    const createAuditLogTable = `
      CREATE TABLE IF NOT EXISTS audit_log (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(50) NOT NULL,
        action VARCHAR(20) NOT NULL,
        record_id INTEGER,
        old_values JSONB,
        new_values JSONB,
        user_id INTEGER REFERENCES users(id),
        ip_address INET,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // Create indexes
    const createIndexes = [
      'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);',
      'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);',
      'CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);',
      'CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);',
      'CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_password_token);',
      'CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);',
      'CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);',
      'CREATE INDEX IF NOT EXISTS idx_user_sessions_refresh_token ON user_sessions(refresh_token);',
      'CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at);',
      'CREATE INDEX IF NOT EXISTS idx_audit_log_table_name ON audit_log(table_name);',
      'CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);',
      'CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp);'
    ];

    // Create trigger function for updated_at
    const createTriggerFunction = `
      CREATE OR REPLACE FUNCTION update_updated_at_column()
      RETURNS TRIGGER AS $$
      BEGIN
          NEW.updated_at = CURRENT_TIMESTAMP;
          RETURN NEW;
      END;
      $$ language 'plpgsql';
    `;

    // Create triggers
    const createTriggers = [
      'CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();'
    ];

    // Execute migrations
    await executeQuery(createUsersTable);
    logger.info('Users table created/verified');

    await executeQuery(createUserSessionsTable);
    logger.info('User sessions table created/verified');

    await executeQuery(createAuditLogTable);
    logger.info('Audit log table created/verified');

    await executeQuery(createTriggerFunction);
    logger.info('Trigger function created/updated');

    // Create indexes
    for (const indexQuery of createIndexes) {
      await executeQuery(indexQuery);
    }
    logger.info('Indexes created/verified');

    // Create triggers
    for (const triggerQuery of createTriggers) {
      await executeQuery(triggerQuery);
    }
    logger.info('Triggers created/verified');

    logger.info('Database migrations completed successfully');
  } catch (error) {
    logger.error('Migration failed:', error);
    throw error;
  }
}

// Run migrations if this file is executed directly
if (require.main === module) {
  const { connectDatabase, closeDatabase } = require('../config/database');
  
  async function main() {
    try {
      await connectDatabase();
      await runMigrations();
      await closeDatabase();
      process.exit(0);
    } catch (error) {
      logger.error('Migration script failed:', error);
      process.exit(1);
    }
  }

  main();
}

module.exports = { runMigrations }; 