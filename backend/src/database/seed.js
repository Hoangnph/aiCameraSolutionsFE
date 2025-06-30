const bcrypt = require('bcryptjs');
const { executeQuery } = require('../config/database');
const logger = require('../utils/logger');

// Seed data script
async function runSeeds() {
  try {
    logger.info('Starting database seeding...');

    // Check if admin user already exists
    const checkAdminQuery = "SELECT id FROM users WHERE username = 'admin'";
    const adminExists = await executeQuery(checkAdminQuery);

    if (adminExists.rows.length === 0) {
      // Create admin user
      const salt = await bcrypt.genSalt(12);
      const adminPasswordHash = await bcrypt.hash('Admin123!', salt);

      const createAdminQuery = `
        INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, email_verified)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id, username, email, role
      `;

      const adminResult = await executeQuery(createAdminQuery, [
        'admin',
        'admin@peoplecounting.com',
        adminPasswordHash,
        'System',
        'Administrator',
        'admin',
        true,
        true
      ]);

      logger.info('Admin user created:', adminResult.rows[0]);
    } else {
      logger.info('Admin user already exists');
    }

    // Check if test user exists
    const checkTestUserQuery = "SELECT id FROM users WHERE username = 'testuser'";
    const testUserExists = await executeQuery(checkTestUserQuery);

    if (testUserExists.rows.length === 0) {
      // Create test user
      const salt = await bcrypt.genSalt(12);
      const testPasswordHash = await bcrypt.hash('Test123!', salt);

      const createTestUserQuery = `
        INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, email_verified)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id, username, email, role
      `;

      const testUserResult = await executeQuery(createTestUserQuery, [
        'testuser',
        'test@peoplecounting.com',
        testPasswordHash,
        'Test',
        'User',
        'user',
        true,
        true
      ]);

      logger.info('Test user created:', testUserResult.rows[0]);
    } else {
      logger.info('Test user already exists');
    }

    // Check if viewer user exists
    const checkViewerQuery = "SELECT id FROM users WHERE username = 'viewer'";
    const viewerExists = await executeQuery(checkViewerQuery);

    if (viewerExists.rows.length === 0) {
      // Create viewer user
      const salt = await bcrypt.genSalt(12);
      const viewerPasswordHash = await bcrypt.hash('Viewer123!', salt);

      const createViewerQuery = `
        INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, email_verified)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id, username, email, role
      `;

      const viewerResult = await executeQuery(createViewerQuery, [
        'viewer',
        'viewer@peoplecounting.com',
        viewerPasswordHash,
        'View',
        'Only',
        'viewer',
        true,
        true
      ]);

      logger.info('Viewer user created:', viewerResult.rows[0]);
    } else {
      logger.info('Viewer user already exists');
    }

    logger.info('Database seeding completed successfully');
    logger.info('Default users:');
    logger.info('- Admin: admin / Admin123!');
    logger.info('- Test User: testuser / Test123!');
    logger.info('- Viewer: viewer / Viewer123!');

  } catch (error) {
    logger.error('Seeding failed:', error);
    throw error;
  }
}

// Run seeds if this file is executed directly
if (require.main === module) {
  const { connectDatabase, closeDatabase } = require('../config/database');
  
  async function main() {
    try {
      await connectDatabase();
      await runSeeds();
      await closeDatabase();
      process.exit(0);
    } catch (error) {
      logger.error('Seed script failed:', error);
      process.exit(1);
    }
  }

  main();
}

module.exports = { runSeeds }; 