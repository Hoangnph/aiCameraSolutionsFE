const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env.test') });

// Set test environment
process.env.NODE_ENV = 'test';

// Global test setup
beforeAll(async () => {
  // Any global setup before tests
});

afterAll(async () => {
  // Any global cleanup after tests
}); 