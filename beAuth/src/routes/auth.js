const express = require('express');
const bcrypt = require('bcryptjs');
const { executeQuery } = require('../config/database');
const { validate } = require('../utils/validation');
const { generateTokenPair, generatePasswordResetToken, hashToken, verifyPasswordResetToken } = require('../utils/jwt');
const { protect } = require('../middleware/auth');
const { customValidations } = require('../utils/validation');
const logger = require('../utils/logger');

const router = express.Router();

// @desc    Register user
// @route   POST /api/v1/auth/register
// @access  Public
router.post('/register', validate('register'), async (req, res, next) => {
  try {
    const { username, email, password, firstName, lastName, registrationCode } = req.body;

    // Check if username is available
    const isUsernameAvailable = await customValidations.isUsernameAvailable(username);
    if (!isUsernameAvailable) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Username already exists'
        }
      });
    }

    // Check if email is available
    const isEmailAvailable = await customValidations.isEmailAvailable(email);
    if (!isEmailAvailable) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Email already exists'
        }
      });
    }

    // Validate registration code
    const registrationCodeQuery = `
      SELECT id, code, name, max_uses, used_count, is_active, expires_at 
      FROM registration_codes 
      WHERE code = $1
    `;
    const registrationCodeResult = await executeQuery(registrationCodeQuery, [registrationCode]);

    if (registrationCodeResult.rows.length === 0) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Mã đăng ký không hợp lệ'
        }
      });
    }

    const registrationCodeData = registrationCodeResult.rows[0];

    // Check if registration code is active
    if (!registrationCodeData.is_active) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Mã đăng ký đã bị vô hiệu hóa'
        }
      });
    }

    // Check if registration code has expired
    if (registrationCodeData.expires_at && new Date() > new Date(registrationCodeData.expires_at)) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Mã đăng ký đã hết hạn'
        }
      });
    }

    // Check if registration code has reached max uses
    if (registrationCodeData.max_uses && registrationCodeData.used_count >= registrationCodeData.max_uses) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Mã đăng ký đã đạt giới hạn sử dụng'
        }
      });
    }

    // Hash password
    const salt = await bcrypt.genSalt(parseInt(process.env.BCRYPT_ROUNDS) || 12);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Insert user into database with registration code
    const insertQuery = `
      INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, registration_code_id)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING id, username, email, first_name, last_name, role, created_at
    `;
    
    const result = await executeQuery(insertQuery, [
      username,
      email,
      hashedPassword,
      firstName || null,
      lastName || null,
      'user',
      true,
      registrationCodeData.id
    ]);

    const user = result.rows[0];

    // Update used_count in registration_codes table
    const updateUsedCountQuery = `
      UPDATE registration_codes 
      SET used_count = used_count + 1 
      WHERE id = $1
    `;
    await executeQuery(updateUsedCountQuery, [registrationCodeData.id]);

    // Generate tokens
    const tokens = generateTokenPair(user.id);

    logger.info(`User registered successfully: ${user.username} with registration code: ${registrationCode}`);

    res.status(201).json({
      success: true,
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role
        },
        ...tokens
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Login user
// @route   POST /api/v1/auth/login
// @access  Public
router.post('/login', validate('login'), async (req, res, next) => {
  try {
    const { username, password } = req.body;

    // Find user by username or email
    const userQuery = `
      SELECT id, username, email, password_hash, first_name, last_name, role, is_active, last_login
      FROM users 
      WHERE username = $1 OR email = $1
    `;
    
    const userResult = await executeQuery(userQuery, [username]);

    if (userResult.rows.length === 0) {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'Invalid credentials'
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
          message: 'Account is deactivated'
        }
      });
    }

    // Check password
    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    if (!isPasswordValid) {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'Invalid credentials'
        }
      });
    }

    // Update last login
    const updateQuery = 'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1';
    await executeQuery(updateQuery, [user.id]);

    // Generate tokens
    const tokens = generateTokenPair(user.id);

    logger.info(`User logged in successfully: ${user.username}`);

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role
        },
        ...tokens
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Refresh token
// @route   POST /api/v1/auth/refresh
// @access  Public
router.post('/refresh', validate('refreshToken'), async (req, res, next) => {
  try {
    const { refreshToken } = req.body;

    // Verify refresh token
    const { verifyToken } = require('../utils/jwt');
    const decoded = verifyToken(refreshToken);

    if (decoded.type !== 'refresh') {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'Invalid refresh token'
        }
      });
    }

    // Check if user exists and is active
    const userQuery = 'SELECT id, username, email, first_name, last_name, role, is_active FROM users WHERE id = $1';
    const userResult = await executeQuery(userQuery, [decoded.userId]);

    if (userResult.rows.length === 0 || !userResult.rows[0].is_active) {
      return res.status(401).json({
        success: false,
        error: {
          code: 401,
          message: 'User not found or inactive'
        }
      });
    }

    const user = userResult.rows[0];

    // Generate new token pair
    const tokens = generateTokenPair(user.id);

    logger.info(`Token refreshed for user: ${user.username}`);

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role
        },
        ...tokens
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Logout user
// @route   POST /api/v1/auth/logout
// @access  Private
router.post('/logout', protect, async (req, res, next) => {
  try {
    // In a more complex system, you might want to blacklist the token
    // For now, we'll just return a success response
    // The client should remove the token from storage

    logger.info(`User logged out: ${req.user.username}`);

    res.status(200).json({
      success: true,
      message: 'Logged out successfully'
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Forgot password
// @route   POST /api/v1/auth/forgot-password
// @access  Public
router.post('/forgot-password', validate('forgotPassword'), async (req, res, next) => {
  try {
    const { email } = req.body;

    // Check if user exists
    const userQuery = 'SELECT id, username, email FROM users WHERE email = $1 AND is_active = true';
    const userResult = await executeQuery(userQuery, [email]);

    if (userResult.rows.length === 0) {
      // Don't reveal if email exists or not for security
      return res.status(200).json({
        success: true,
        message: 'If the email exists, a password reset link has been sent'
      });
    }

    const user = userResult.rows[0];

    // Generate reset token
    const resetToken = generatePasswordResetToken();
    const hashedResetToken = hashToken(resetToken);

    // Store reset token in database
    const resetTokenExpiry = new Date(Date.now() + 10 * 60 * 1000); // 10 minutes
    const updateQuery = `
      UPDATE users 
      SET reset_password_token = $1, reset_password_expires = $2 
      WHERE id = $3
    `;
    
    await executeQuery(updateQuery, [hashedResetToken, resetTokenExpiry, user.id]);

    // TODO: Send email with reset link
    // For now, we'll just log the token (in production, send email)
    logger.info(`Password reset token for ${user.email}: ${resetToken}`);

    res.status(200).json({
      success: true,
      message: 'If the email exists, a password reset link has been sent'
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Reset password
// @route   POST /api/v1/auth/reset-password
// @access  Public
router.post('/reset-password', validate('resetPassword'), async (req, res, next) => {
  try {
    const { token, password } = req.body;

    // Find user with valid reset token
    const userQuery = `
      SELECT id, username, email, reset_password_token, reset_password_expires 
      FROM users 
      WHERE reset_password_token IS NOT NULL 
      AND reset_password_expires > CURRENT_TIMESTAMP
    `;
    
    const userResult = await executeQuery(userQuery);

    let user = null;
    for (const row of userResult.rows) {
      if (verifyPasswordResetToken(token, row.reset_password_token)) {
        user = row;
        break;
      }
    }

    if (!user) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Invalid or expired reset token'
        }
      });
    }

    // Hash new password
    const salt = await bcrypt.genSalt(parseInt(process.env.BCRYPT_ROUNDS) || 12);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Update password and clear reset token
    const updateQuery = `
      UPDATE users 
      SET password_hash = $1, reset_password_token = NULL, reset_password_expires = NULL 
      WHERE id = $2
    `;
    
    await executeQuery(updateQuery, [hashedPassword, user.id]);

    logger.info(`Password reset successfully for user: ${user.username}`);

    res.status(200).json({
      success: true,
      message: 'Password reset successfully'
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Get current user
// @route   GET /api/v1/auth/me
// @access  Private
router.get('/me', protect, async (req, res, next) => {
  try {
    res.status(200).json({
      success: true,
      data: {
        user: {
          id: req.user.id,
          username: req.user.username,
          email: req.user.email,
          firstName: req.user.first_name,
          lastName: req.user.last_name,
          role: req.user.role
        }
      }
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router; 