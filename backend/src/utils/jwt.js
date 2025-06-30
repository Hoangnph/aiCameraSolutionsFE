const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const logger = require('./logger');

// Generate JWT token
function generateToken(payload, expiresIn = '15m') {
  try {
    return jwt.sign(payload, process.env.JWT_SECRET, {
      expiresIn: expiresIn
    });
  } catch (error) {
    logger.error('Error generating JWT token:', error);
    throw new Error('Failed to generate token');
  }
}

// Generate access token
function generateAccessToken(userId) {
  return generateToken(
    { userId, type: 'access' },
    process.env.JWT_ACCESS_TOKEN_EXPIRY || '15m'
  );
}

// Generate refresh token
function generateRefreshToken(userId) {
  return generateToken(
    { userId, type: 'refresh' },
    process.env.JWT_REFRESH_TOKEN_EXPIRY || '7d'
  );
}

// Verify JWT token
function verifyToken(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (error) {
    logger.error('Error verifying JWT token:', error);
    throw error;
  }
}

// Generate token pair (access + refresh)
function generateTokenPair(userId) {
  const accessToken = generateAccessToken(userId);
  const refreshToken = generateRefreshToken(userId);
  
  return {
    accessToken,
    refreshToken,
    tokenType: 'bearer'
  };
}

// Generate password reset token
function generatePasswordResetToken() {
  return crypto.randomBytes(32).toString('hex');
}

// Generate email verification token
function generateEmailVerificationToken() {
  return crypto.randomBytes(32).toString('hex');
}

// Hash token for storage
function hashToken(token) {
  return crypto.createHash('sha256').update(token).digest('hex');
}

// Generate random string
function generateRandomString(length = 32) {
  return crypto.randomBytes(length).toString('hex');
}

// Verify password reset token
function verifyPasswordResetToken(token, hashedToken) {
  const tokenHash = hashToken(token);
  return tokenHash === hashedToken;
}

// Get token from request headers
function getTokenFromHeader(req) {
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    return req.headers.authorization.split(' ')[1];
  }
  return null;
}

// Decode token without verification (for logging purposes)
function decodeToken(token) {
  try {
    return jwt.decode(token);
  } catch (error) {
    logger.error('Error decoding JWT token:', error);
    return null;
  }
}

// Check if token is expired
function isTokenExpired(token) {
  try {
    const decoded = jwt.decode(token);
    if (!decoded || !decoded.exp) {
      return true;
    }
    return Date.now() >= decoded.exp * 1000;
  } catch (error) {
    logger.error('Error checking token expiration:', error);
    return true;
  }
}

// Get token expiration time
function getTokenExpiration(token) {
  try {
    const decoded = jwt.decode(token);
    if (!decoded || !decoded.exp) {
      return null;
    }
    return new Date(decoded.exp * 1000);
  } catch (error) {
    logger.error('Error getting token expiration:', error);
    return null;
  }
}

module.exports = {
  generateToken,
  generateAccessToken,
  generateRefreshToken,
  verifyToken,
  generateTokenPair,
  generatePasswordResetToken,
  generateEmailVerificationToken,
  hashToken,
  generateRandomString,
  verifyPasswordResetToken,
  getTokenFromHeader,
  decodeToken,
  isTokenExpired,
  getTokenExpiration
}; 