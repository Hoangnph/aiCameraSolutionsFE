const jwt = require('jsonwebtoken');
const { executeQuery } = require('../config/database');
const logger = require('../utils/logger');

// Protect routes - require authentication
async function protect(req, res, next) {
  let token;

  // Check for token in headers
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  }

  // Check if token exists
  if (!token) {
    return res.status(401).json({
      success: false,
      error: {
        code: 401,
        message: 'Not authorized to access this route'
      }
    });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Check if user still exists
    const userQuery = 'SELECT id, username, email, role, is_active FROM users WHERE id = $1';
    const userResult = await executeQuery(userQuery, [decoded.userId]);

    if (userResult.rows.length === 0) {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'User no longer exists'
        }
      });
    }

    const user = userResult.rows[0];

    // Check if user is active
    if (!user.is_active) {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'User account is deactivated'
        }
      });
    }

    // Add user to request object
    req.user = user;
    next();
  } catch (error) {
    logger.error('Token verification error:', error);
    return res.status(401).json({
      success: false,
      error: {
        code: 401,
        message: 'Not authorized to access this route'
      }
    });
  }
}

// Grant access to specific roles
function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'Not authorized to access this route'
        }
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        error: {
          code: 403,
          message: `User role ${req.user.role} is not authorized to access this route`
        }
      });
    }

    next();
  };
}

// Optional authentication - doesn't fail if no token
async function optionalAuth(req, res, next) {
  let token;

  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return next();
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    const userQuery = 'SELECT id, username, email, role, is_active FROM users WHERE id = $1';
    const userResult = await executeQuery(userQuery, [decoded.userId]);

    if (userResult.rows.length > 0 && userResult.rows[0].is_active) {
      req.user = userResult.rows[0];
    }
  } catch (error) {
    logger.error('Optional auth error:', error);
  }

  next();
}

module.exports = {
  protect,
  authorize,
  optionalAuth
}; 