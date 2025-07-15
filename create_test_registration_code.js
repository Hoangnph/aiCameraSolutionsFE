const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'people_counting_db',
  user: 'postgres',
  password: 'dev_password',
});

async function createTestRegistrationCode() {
  try {
    // Connect to database
    const client = await pool.connect();
    
    // Check if admin user exists
    const adminResult = await client.query('SELECT id FROM users WHERE username = $1', ['admin']);
    let adminUserId = null;
    
    if (adminResult.rows.length > 0) {
      adminUserId = adminResult.rows[0].id;
    } else {
      // Create admin user if not exists
      const createAdminResult = await client.query(`
        INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, email_verified)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id
      `, [
        'admin',
        'admin@aicamera.com',
        '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i', // Admin123!
        'Admin',
        'User',
        'admin',
        true,
        true
      ]);
      adminUserId = createAdminResult.rows[0].id;
      console.log('✅ Admin user created with ID:', adminUserId);
    }
    
    // Check if registration code exists
    const codeResult = await client.query('SELECT id FROM registration_codes WHERE code = $1', ['adminfe']);
    
    if (codeResult.rows.length === 0) {
      // Create registration code
      const createCodeResult = await client.query(`
        INSERT INTO registration_codes (code, name, description, type, max_uses, created_by)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, code, name
      `, [
        'adminfe',
        'Admin Future Eyes',
        'Mã đăng ký mặc định cho hệ thống Future Eyes',
        'organization',
        null, // Không giới hạn số lần sử dụng
        adminUserId
      ]);
      
      console.log('✅ Registration code created:', createCodeResult.rows[0]);
    } else {
      console.log('✅ Registration code "adminfe" already exists');
    }
    
    // Create additional test codes
    const testCodes = [
      {
        code: 'TEST001',
        name: 'Test Code 001',
        description: 'Mã test cho development',
        type: 'general',
        max_uses: 100
      },
      {
        code: 'DEV2024',
        name: 'Development 2024',
        description: 'Mã cho development team',
        type: 'department',
        max_uses: 50
      }
    ];
    
    for (const testCode of testCodes) {
      const existingCode = await client.query('SELECT id FROM registration_codes WHERE code = $1', [testCode.code]);
      
      if (existingCode.rows.length === 0) {
        await client.query(`
          INSERT INTO registration_codes (code, name, description, type, max_uses, created_by)
          VALUES ($1, $2, $3, $4, $5, $6)
        `, [
          testCode.code,
          testCode.name,
          testCode.description,
          testCode.type,
          testCode.max_uses,
          adminUserId
        ]);
        console.log(`✅ Test code "${testCode.code}" created`);
      } else {
        console.log(`✅ Test code "${testCode.code}" already exists`);
      }
    }
    
    // List all registration codes
    const allCodes = await client.query('SELECT code, name, type, max_uses, used_count, is_active FROM registration_codes');
    console.log('\n📋 Available registration codes:');
    allCodes.rows.forEach(code => {
      console.log(`  - ${code.code}: ${code.name} (${code.type}, uses: ${code.used_count}/${code.max_uses || 'unlimited'}, active: ${code.is_active})`);
    });
    
    client.release();
    await pool.end();
    
    console.log('\n✅ Registration codes setup completed!');
    
  } catch (error) {
    console.error('❌ Error creating registration codes:', error);
    process.exit(1);
  }
}

createTestRegistrationCode(); 