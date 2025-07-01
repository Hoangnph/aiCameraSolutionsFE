const API_BASE_URL = 'http://localhost:3001/api/v1';

// Test data
const testUser = {
  username: 'testuser123',
  email: 'testuser123@example.com',
  password: 'Test123!',
  firstName: 'Test',
  lastName: 'User'
};

let accessToken = null;
let refreshToken = null;

// Helper function to make API calls
async function makeRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    console.log(`${options.method || 'GET'} ${endpoint}:`, response.status, data);
    
    return { response, data };
  } catch (error) {
    console.error(`Error ${options.method || 'GET'} ${endpoint}:`, error);
    throw error;
  }
}

// Test functions
async function testRegister() {
  console.log('\n=== Testing Register ===');
  const { data } = await makeRequest('/auth/register', {
    method: 'POST',
    body: JSON.stringify(testUser)
  });
  
  if (data.success) {
    accessToken = data.data.accessToken;
    refreshToken = data.data.refreshToken;
    console.log('✅ Register successful');
  } else {
    console.log('❌ Register failed');
  }
}

async function testLogin() {
  console.log('\n=== Testing Login ===');
  const { data } = await makeRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      username: testUser.username,
      password: testUser.password
    })
  });
  
  if (data.success) {
    accessToken = data.data.accessToken;
    refreshToken = data.data.refreshToken;
    console.log('✅ Login successful');
  } else {
    console.log('❌ Login failed');
  }
}

async function testGetCurrentUser() {
  console.log('\n=== Testing Get Current User ===');
  const { data } = await makeRequest('/auth/me');
  
  if (data.success) {
    console.log('✅ Get current user successful');
    console.log('User:', data.data.user);
  } else {
    console.log('❌ Get current user failed');
  }
}

async function testRefreshToken() {
  console.log('\n=== Testing Refresh Token ===');
  const { data } = await makeRequest('/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refreshToken })
  });
  
  if (data.success) {
    accessToken = data.data.accessToken;
    refreshToken = data.data.refreshToken;
    console.log('✅ Refresh token successful');
  } else {
    console.log('❌ Refresh token failed');
  }
}

async function testLogout() {
  console.log('\n=== Testing Logout ===');
  const { data } = await makeRequest('/auth/logout', {
    method: 'POST'
  });
  
  if (data.success) {
    accessToken = null;
    refreshToken = null;
    console.log('✅ Logout successful');
  } else {
    console.log('❌ Logout failed');
  }
}

async function testProtectedRoute() {
  console.log('\n=== Testing Protected Route ===');
  const { data } = await makeRequest('/auth/me');
  
  if (data.success) {
    console.log('✅ Protected route accessible');
  } else {
    console.log('❌ Protected route blocked (expected after logout)');
  }
}

// Main test function
async function runTests() {
  console.log('🚀 Starting Authentication API Tests...\n');
  
  try {
    // Test 1: Register new user
    await testRegister();
    
    // Test 2: Login
    await testLogin();
    
    // Test 3: Get current user (protected route)
    await testGetCurrentUser();
    
    // Test 4: Refresh token
    await testRefreshToken();
    
    // Test 5: Get current user again (with new token)
    await testGetCurrentUser();
    
    // Test 6: Logout
    await testLogout();
    
    // Test 7: Try to access protected route after logout
    await testProtectedRoute();
    
    console.log('\n🎉 All tests completed!');
    
  } catch (error) {
    console.error('\n❌ Test failed:', error);
  }
}

// Run tests if this file is executed directly
if (typeof window === 'undefined') {
  // Node.js environment
  const fetch = require('node-fetch');
  runTests();
} else {
  // Browser environment
  console.log('Run this script in Node.js environment: node test-auth.js');
} 