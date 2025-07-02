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

    // Create registration code "adminfe" if it doesn't exist
    const checkRegistrationCodeQuery = "SELECT id FROM registration_codes WHERE code = 'adminfe'";
    const registrationCodeExists = await executeQuery(checkRegistrationCodeQuery);

    if (registrationCodeExists.rows.length === 0) {
      // Get admin user ID for created_by
      const adminUserQuery = "SELECT id FROM users WHERE username = 'admin'";
      const adminUserResult = await executeQuery(adminUserQuery);
      const adminUserId = adminUserResult.rows[0]?.id || null;

      const createRegistrationCodeQuery = `
        INSERT INTO registration_codes (code, name, description, type, max_uses, created_by)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, code, name
      `;

      const registrationCodeResult = await executeQuery(createRegistrationCodeQuery, [
        'adminfe',
        'Admin Future Eyes',
        'Mã đăng ký mặc định cho hệ thống Future Eyes',
        'organization',
        null, // Không giới hạn số lần sử dụng
        adminUserId
      ]);

      logger.info('Registration code created:', registrationCodeResult.rows[0]);
    } else {
      logger.info('Registration code "adminfe" already exists');
    }

    // Get the registration code ID
    const getRegistrationCodeQuery = "SELECT id FROM registration_codes WHERE code = 'adminfe'";
    const registrationCodeResult = await executeQuery(getRegistrationCodeQuery);
    const registrationCodeId = registrationCodeResult.rows[0]?.id;

    if (registrationCodeId) {
      // Update all existing users to use this registration code
      const updateUsersQuery = `
        UPDATE users 
        SET registration_code_id = $1 
        WHERE registration_code_id IS NULL
      `;
      
      const updateResult = await executeQuery(updateUsersQuery, [registrationCodeId]);
      
      if (updateResult.rowCount > 0) {
        logger.info(`Updated ${updateResult.rowCount} users with registration code "adminfe"`);
      } else {
        logger.info('All users already have registration codes assigned');
      }

      // Update the used_count in registration_codes table
      const countUsersQuery = "SELECT COUNT(*) as count FROM users WHERE registration_code_id = $1";
      const countResult = await executeQuery(countUsersQuery, [registrationCodeId]);
      const userCount = parseInt(countResult.rows[0].count);

      const updateUsedCountQuery = "UPDATE registration_codes SET used_count = $1 WHERE id = $2";
      await executeQuery(updateUsedCountQuery, [userCount, registrationCodeId]);
      
      logger.info(`Updated registration code used_count to ${userCount}`);
    }

    logger.info('Database seeding completed successfully');
    logger.info('Default users:');
    logger.info('- Admin: admin / Admin123!');
    logger.info('- Test User: testuser / Test123!');
    logger.info('- Viewer: viewer / Viewer123!');
    logger.info('Registration code: adminfe (assigned to all users)');

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