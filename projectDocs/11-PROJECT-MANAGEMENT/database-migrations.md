# Database Migration & Seeding Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn quy trình database migration, seeding, backup, và optimization cho hệ thống AI Camera Counting.

### 🎯 Database Management Objectives
- Đảm bảo database schema consistency
- Manage data migrations safely
- Optimize database performance
- Maintain data integrity và backup

### 🗄️ Database Schema Management

#### Migration Strategy
```yaml
# Migration Strategy
migration_strategy:
  approach: "Version-based migrations"
  tool: "Custom migration scripts"
  environment_support:
    - "Development"
    - "Staging"
    - "Production"
  
  naming_convention: "YYYYMMDD_HHMMSS_description.sql"
  rollback_support: true
  data_preservation: true
```

#### Migration File Structure
```sql
-- migrations/20250703_143000_create_users_table.sql
-- Up Migration
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- Down Migration
DROP TABLE IF EXISTS users;
```

#### Migration Scripts
```javascript
// beAuth/src/database/migrate.js
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

class DatabaseMigrator {
  constructor(config) {
    this.pool = new Pool(config);
    this.migrationsPath = path.join(__dirname, 'migrations');
  }

  async runMigrations() {
    try {
      // Create migrations table if not exists
      await this.createMigrationsTable();
      
      // Get all migration files
      const migrationFiles = this.getMigrationFiles();
      
      // Get applied migrations
      const appliedMigrations = await this.getAppliedMigrations();
      
      // Run pending migrations
      for (const file of migrationFiles) {
        if (!appliedMigrations.includes(file)) {
          await this.runMigration(file);
        }
      }
      
      console.log('✅ All migrations completed successfully');
    } catch (error) {
      console.error('❌ Migration failed:', error);
      throw error;
    }
  }

  async createMigrationsTable() {
    const query = `
      CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) UNIQUE NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `;
    await this.pool.query(query);
  }

  getMigrationFiles() {
    return fs.readdirSync(this.migrationsPath)
      .filter(file => file.endsWith('.sql'))
      .sort();
  }

  async getAppliedMigrations() {
    const query = 'SELECT filename FROM migrations ORDER BY applied_at';
    const result = await this.pool.query(query);
    return result.rows.map(row => row.filename);
  }

  async runMigration(filename) {
    const filePath = path.join(this.migrationsPath, filename);
    const sql = fs.readFileSync(filePath, 'utf8');
    
    // Split up and down migrations
    const parts = sql.split('-- Down Migration');
    const upMigration = parts[0].replace('-- Up Migration', '').trim();
    
    try {
      await this.pool.query('BEGIN');
      
      // Execute up migration
      await this.pool.query(upMigration);
      
      // Record migration
      await this.pool.query(
        'INSERT INTO migrations (filename) VALUES ($1)',
        [filename]
      );
      
      await this.pool.query('COMMIT');
      console.log(`✅ Applied migration: ${filename}`);
    } catch (error) {
      await this.pool.query('ROLLBACK');
      throw error;
    }
  }

  async rollbackMigration(filename) {
    const filePath = path.join(this.migrationsPath, filename);
    const sql = fs.readFileSync(filePath, 'utf8');
    
    // Get down migration
    const parts = sql.split('-- Down Migration');
    const downMigration = parts[1]?.trim();
    
    if (!downMigration) {
      throw new Error(`No down migration found for ${filename}`);
    }
    
    try {
      await this.pool.query('BEGIN');
      
      // Execute down migration
      await this.pool.query(downMigration);
      
      // Remove migration record
      await this.pool.query(
        'DELETE FROM migrations WHERE filename = $1',
        [filename]
      );
      
      await this.pool.query('COMMIT');
      console.log(`✅ Rolled back migration: ${filename}`);
    } catch (error) {
      await this.pool.query('ROLLBACK');
      throw error;
    }
  }
}

module.exports = DatabaseMigrator;
```

### 🌱 Data Seeding

#### Seed Data Structure
```javascript
// beAuth/src/database/seed.js
const { Pool } = require('pg');
const bcrypt = require('bcrypt');

class DatabaseSeeder {
  constructor(config) {
    this.pool = new Pool(config);
  }

  async seedDatabase() {
    try {
      console.log('🌱 Starting database seeding...');
      
      await this.seedUsers();
      await this.seedCameras();
      await this.seedCountData();
      
      console.log('✅ Database seeding completed successfully');
    } catch (error) {
      console.error('❌ Seeding failed:', error);
      throw error;
    }
  }

  async seedUsers() {
    const users = [
      {
        email: 'admin@aicamera.com',
        password: 'admin123',
        name: 'System Administrator',
        role: 'admin'
      },
      {
        email: 'user@aicamera.com',
        password: 'user123',
        name: 'Test User',
        role: 'user'
      },
      {
        email: 'demo@aicamera.com',
        password: 'demo123',
        name: 'Demo User',
        role: 'user'
      }
    ];

    for (const user of users) {
      const hashedPassword = await bcrypt.hash(user.password, 10);
      
      await this.pool.query(`
        INSERT INTO users (email, password_hash, name, role)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (email) DO NOTHING
      `, [user.email, hashedPassword, user.name, user.role]);
    }
    
    console.log('✅ Users seeded successfully');
  }

  async seedCameras() {
    const cameras = [
      {
        name: 'Main Entrance Camera',
        location: 'Building A - Main Entrance',
        ip_address: '192.168.1.100',
        status: 'active'
      },
      {
        name: 'Parking Lot Camera',
        location: 'Building A - Parking Lot',
        ip_address: '192.168.1.101',
        status: 'active'
      },
      {
        name: 'Office Lobby Camera',
        location: 'Building B - Lobby',
        ip_address: '192.168.1.102',
        status: 'inactive'
      }
    ];

    for (const camera of cameras) {
      await this.pool.query(`
        INSERT INTO cameras (name, location, ip_address, status)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (ip_address) DO NOTHING
      `, [camera.name, camera.location, camera.ip_address, camera.status]);
    }
    
    console.log('✅ Cameras seeded successfully');
  }

  async seedCountData() {
    // Generate sample count data for the last 7 days
    const cameras = await this.pool.query('SELECT id FROM cameras WHERE status = $1', ['active']);
    
    for (const camera of cameras.rows) {
      for (let i = 0; i < 7; i++) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        
        // Generate 24 hours of data
        for (let hour = 0; hour < 24; hour++) {
          const count = Math.floor(Math.random() * 50) + 10; // 10-60 people
          const confidence = 0.8 + Math.random() * 0.2; // 80-100% confidence
          
          await this.pool.query(`
            INSERT INTO count_data (camera_id, count, confidence, timestamp)
            VALUES ($1, $2, $3, $4)
          `, [
            camera.id,
            count,
            confidence,
            new Date(date.getFullYear(), date.getMonth(), date.getDate(), hour)
          ]);
        }
      }
    }
    
    console.log('✅ Count data seeded successfully');
  }
}

module.exports = DatabaseSeeder;
```

### 🔄 Migration Management

#### Migration Commands
```bash
#!/bin/bash
# scripts/migrate.sh

ENVIRONMENT=$1
ACTION=$2

case $ACTION in
  "up")
    echo "Running migrations for $ENVIRONMENT..."
    node beAuth/src/database/migrate.js --env=$ENVIRONMENT
    ;;
  "down")
    echo "Rolling back last migration for $ENVIRONMENT..."
    node beAuth/src/database/migrate.js --env=$ENVIRONMENT --rollback
    ;;
  "seed")
    echo "Seeding database for $ENVIRONMENT..."
    node beAuth/src/database/seed.js --env=$ENVIRONMENT
    ;;
  "reset")
    echo "Resetting database for $ENVIRONMENT..."
    node beAuth/src/database/migrate.js --env=$ENVIRONMENT --reset
    node beAuth/src/database/seed.js --env=$ENVIRONMENT
    ;;
  *)
    echo "Usage: $0 {environment} {up|down|seed|reset}"
    exit 1
    ;;
esac
```

#### Migration Configuration
```javascript
// beAuth/src/database/config.js
const config = {
  development: {
    host: 'localhost',
    port: 5432,
    database: 'aicamera_dev',
    user: 'postgres',
    password: 'password'
  },
  staging: {
    host: process.env.DB_HOST || 'staging-db',
    port: 5432,
    database: 'aicamera_staging',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'password'
  },
  production: {
    host: process.env.DB_HOST,
    port: 5432,
    database: 'aicamera_prod',
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    ssl: {
      rejectUnauthorized: false
    }
  }
};

module.exports = config;
```

### 💾 Backup & Restore

#### Backup Strategy
```yaml
# Backup Strategy
backup_strategy:
  frequency:
    - "Full backup: Daily at 2 AM"
    - "Incremental backup: Every 6 hours"
    - "Transaction log backup: Every 15 minutes"
  
  retention:
    - "Daily backups: 7 days"
    - "Weekly backups: 4 weeks"
    - "Monthly backups: 12 months"
  
  storage:
    - "Local storage: 7 days"
    - "Cloud storage: 12 months"
    - "Offsite storage: 1 year"
```

#### Backup Scripts
```bash
#!/bin/bash
# scripts/backup.sh

ENVIRONMENT=$1
BACKUP_DIR="/backups/$ENVIRONMENT"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${ENVIRONMENT}_${DATE}.sql"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h $DB_HOST -U $DB_USER -d aicamera_$ENVIRONMENT > "$BACKUP_DIR/$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_DIR/$BACKUP_FILE"

# Upload to cloud storage
aws s3 cp "$BACKUP_DIR/$BACKUP_FILE.gz" "s3://aicamera-backups/$ENVIRONMENT/"

# Clean up old backups (keep last 7 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup completed: $BACKUP_FILE.gz"
```

#### Restore Scripts
```bash
#!/bin/bash
# scripts/restore.sh

ENVIRONMENT=$1
BACKUP_FILE=$2

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 {environment} {backup_file}"
  exit 1
fi

BACKUP_DIR="/backups/$ENVIRONMENT"
RESTORE_FILE="$BACKUP_DIR/$BACKUP_FILE"

# Download from cloud if not local
if [ ! -f "$RESTORE_FILE" ]; then
  aws s3 cp "s3://aicamera-backups/$ENVIRONMENT/$BACKUP_FILE" "$RESTORE_FILE"
fi

# Stop application
docker-compose -f docker-compose.$ENVIRONMENT.yml stop

# Restore database
gunzip -c "$RESTORE_FILE" | psql -h $DB_HOST -U $DB_USER -d aicamera_$ENVIRONMENT

# Start application
docker-compose -f docker-compose.$ENVIRONMENT.yml up -d

# Verify restore
./scripts/health-check.sh $ENVIRONMENT

echo "✅ Restore completed: $BACKUP_FILE"
```

### ⚡ Database Optimization

#### Performance Optimization
```sql
-- Database optimization queries
-- Analyze table statistics
ANALYZE users;
ANALYZE cameras;
ANALYZE count_data;

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY idx_count_data_camera_timestamp 
ON count_data(camera_id, timestamp);

CREATE INDEX CONCURRENTLY idx_count_data_timestamp 
ON count_data(timestamp DESC);

-- Partition large tables
CREATE TABLE count_data_partitioned (
    LIKE count_data INCLUDING ALL
) PARTITION BY RANGE (timestamp);

CREATE TABLE count_data_2025_01 PARTITION OF count_data_partitioned
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Optimize queries
EXPLAIN ANALYZE SELECT 
    camera_id,
    DATE(timestamp) as date,
    SUM(count) as total_count,
    AVG(confidence) as avg_confidence
FROM count_data 
WHERE timestamp >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY camera_id, DATE(timestamp)
ORDER BY date DESC;
```

#### Maintenance Scripts
```sql
-- Database maintenance procedures
-- Vacuum and analyze tables
VACUUM ANALYZE users;
VACUUM ANALYZE cameras;
VACUUM ANALYZE count_data;

-- Update table statistics
ANALYZE;

-- Clean up old data
DELETE FROM count_data 
WHERE timestamp < CURRENT_DATE - INTERVAL '90 days';

-- Archive old data
INSERT INTO count_data_archive 
SELECT * FROM count_data 
WHERE timestamp < CURRENT_DATE - INTERVAL '30 days';

DELETE FROM count_data 
WHERE timestamp < CURRENT_DATE - INTERVAL '30 days';
```

### 📊 Database Monitoring

#### Performance Monitoring
```sql
-- Database performance queries
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE tablename IN ('users', 'cameras', 'count_data');

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE schemaname = 'public';

-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

#### Health Checks
```javascript
// beAuth/src/database/health.js
const { Pool } = require('pg');

class DatabaseHealthChecker {
  constructor(config) {
    this.pool = new Pool(config);
  }

  async checkHealth() {
    const checks = [
      this.checkConnection(),
      this.checkTables(),
      this.checkIndexes(),
      this.checkPerformance()
    ];

    const results = await Promise.allSettled(checks);
    
    return {
      status: results.every(r => r.status === 'fulfilled' && r.value.healthy) ? 'healthy' : 'unhealthy',
      checks: results.map((result, index) => ({
        name: ['connection', 'tables', 'indexes', 'performance'][index],
        ...result
      }))
    };
  }

  async checkConnection() {
    try {
      const result = await this.pool.query('SELECT 1');
      return {
        healthy: true,
        message: 'Database connection successful'
      };
    } catch (error) {
      return {
        healthy: false,
        message: `Database connection failed: ${error.message}`
      };
    }
  }

  async checkTables() {
    try {
      const result = await this.pool.query(`
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
      `);
      
      const expectedTables = ['users', 'cameras', 'count_data', 'migrations'];
      const existingTables = result.rows.map(row => row.table_name);
      
      const missingTables = expectedTables.filter(table => !existingTables.includes(table));
      
      return {
        healthy: missingTables.length === 0,
        message: missingTables.length === 0 
          ? 'All expected tables exist' 
          : `Missing tables: ${missingTables.join(', ')}`
      };
    } catch (error) {
      return {
        healthy: false,
        message: `Table check failed: ${error.message}`
      };
    }
  }

  async checkIndexes() {
    try {
      const result = await this.pool.query(`
        SELECT indexname, idx_scan, idx_tup_read
        FROM pg_stat_user_indexes 
        WHERE schemaname = 'public'
      `);
      
      const unusedIndexes = result.rows.filter(row => row.idx_scan === 0);
      
      return {
        healthy: unusedIndexes.length === 0,
        message: unusedIndexes.length === 0 
          ? 'All indexes are being used' 
          : `Unused indexes: ${unusedIndexes.map(i => i.indexname).join(', ')}`
      };
    } catch (error) {
      return {
        healthy: false,
        message: `Index check failed: ${error.message}`
      };
    }
  }

  async checkPerformance() {
    try {
      const result = await this.pool.query(`
        SELECT 
          schemaname,
          tablename,
          n_tup_ins,
          n_tup_upd,
          n_tup_del,
          n_live_tup,
          n_dead_tup
        FROM pg_stat_user_tables 
        WHERE schemaname = 'public'
      `);
      
      const tablesWithDeadTuples = result.rows.filter(row => row.n_dead_tup > 0);
      
      return {
        healthy: tablesWithDeadTuples.length === 0,
        message: tablesWithDeadTuples.length === 0 
          ? 'No dead tuples found' 
          : `Tables with dead tuples: ${tablesWithDeadTuples.map(t => t.tablename).join(', ')}`
      };
    } catch (error) {
      return {
        healthy: false,
        message: `Performance check failed: ${error.message}`
      };
    }
  }
}

module.exports = DatabaseHealthChecker;
```

### 📋 Migration Checklist

#### Pre-Migration
- [ ] Backup database
- [ ] Test migration on staging
- [ ] Review migration script
- [ ] Plan rollback strategy
- [ ] Notify team
- [ ] Schedule maintenance window

#### During Migration
- [ ] Stop application
- [ ] Run migration script
- [ ] Verify migration success
- [ ] Update application
- [ ] Start application
- [ ] Run health checks

#### Post-Migration
- [ ] Verify data integrity
- [ ] Run smoke tests
- [ ] Monitor performance
- [ ] Update documentation
- [ ] Clean up backups
- [ ] Notify stakeholders

### 🎯 Database Management Success Metrics

#### Migration Metrics
- **Migration Success Rate**: > 99%
- **Migration Time**: < 30 minutes
- **Rollback Time**: < 15 minutes
- **Data Loss**: 0 incidents

#### Performance Metrics
- **Query Response Time**: < 100ms average
- **Index Usage**: > 90%
- **Dead Tuples**: < 1% of live tuples
- **Table Bloat**: < 10%

#### Backup Metrics
- **Backup Success Rate**: 100%
- **Backup Time**: < 2 hours
- **Restore Time**: < 4 hours
- **Data Retention**: 100% compliance

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 