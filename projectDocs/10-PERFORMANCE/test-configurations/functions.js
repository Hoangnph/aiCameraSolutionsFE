// Artillery functions for load testing

function setAuthHeader(requestParams, context, ee, next) {
  // Set authorization header if token exists
  if (context.vars.authToken) {
    requestParams.headers.Authorization = `Bearer ${context.vars.authToken}`;
  }
  return next();
}

function generateRandomData(requestParams, context, ee, next) {
  // Generate random test data
  context.vars.randomName = `Test Camera ${Math.random().toString(36).substring(7)}`;
  context.vars.randomLocation = `Location ${Math.random().toString(36).substring(7)}`;
  context.vars.randomIp = `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`;
  
  return next();
}

function validateResponse(requestParams, response, context, ee, next) {
  // Custom response validation
  if (response.statusCode >= 400) {
    console.log(`Error response: ${response.statusCode} - ${response.body}`);
  }
  
  // Validate JSON response
  try {
    if (response.body) {
      const data = JSON.parse(response.body);
      if (data.error) {
        console.log(`API Error: ${data.error}`);
      }
    }
  } catch (e) {
    // Response is not JSON, which might be expected for some endpoints
  }
  
  return next();
}

function logPerformance(requestParams, response, context, ee, next) {
  // Log performance metrics
  const duration = response.timings.duration;
  const url = requestParams.url;
  
  if (duration > 1000) {
    console.log(`Slow request: ${url} took ${duration}ms`);
  }
  
  return next();
}

function handleWebSocketMessage(message, context, ee, next) {
  // Handle WebSocket messages
  try {
    const data = JSON.parse(message);
    if (data.type === 'pong') {
      console.log('Received pong from WebSocket');
    }
  } catch (e) {
    console.log('Received non-JSON WebSocket message');
  }
  
  return next();
}

function cleanupTestData(requestParams, response, context, ee, next) {
  // Cleanup test data after tests
  if (context.vars.cameraId) {
    // This would typically delete the test camera
    console.log(`Test camera ${context.vars.cameraId} should be cleaned up`);
  }
  
  return next();
}

module.exports = {
  setAuthHeader,
  generateRandomData,
  validateResponse,
  logPerformance,
  handleWebSocketMessage,
  cleanupTestData
}; 