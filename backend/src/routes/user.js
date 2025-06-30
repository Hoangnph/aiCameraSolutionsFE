const express = require('express');
const bcrypt = require('bcryptjs');
const { executeQuery } = require('../config/database');
const { validate } = require('../utils/validation');
const { protect, authorize } = require('../middleware/auth');
const { customValidations } = require('../utils/validation');
const logger = require('../utils/logger');

const router = express.Router();

// Protect all routes
router.use(protect);

// @desc    Get user profile
// @route   GET /api/v1/users/profile
// @access  Private
router.get('/profile', async (req, res, next) => {
  try {
    const userQuery = `
      SELECT id, username, email, first_name, last_name, role, is_active, last_login, created_at, updated_at
      FROM users 
      WHERE id = $1
    `;
    
    const result = await executeQuery(userQuery, [req.user.id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 404,
          message: 'User not found'
        }
      });
    }

    const user = result.rows[0];

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role,
          isActive: user.is_active,
          lastLogin: user.last_login,
          createdAt: user.created_at,
          updatedAt: user.updated_at
        }
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Update user profile
// @route   PUT /api/v1/users/profile
// @access  Private
router.put('/profile', validate('updateProfile'), async (req, res, next) => {
  try {
    const { username, email, firstName, lastName } = req.body;
    const userId = req.user.id;

    // Check if username is available (if changing)
    if (username && username !== req.user.username) {
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
    }

    // Check if email is available (if changing)
    if (email && email !== req.user.email) {
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
    }

    // Build update query dynamically
    const updateFields = [];
    const updateValues = [];
    let paramCount = 1;

    if (username) {
      updateFields.push(`username = $${paramCount++}`);
      updateValues.push(username);
    }

    if (email) {
      updateFields.push(`email = $${paramCount++}`);
      updateValues.push(email);
    }

    if (firstName !== undefined) {
      updateFields.push(`first_name = $${paramCount++}`);
      updateValues.push(firstName);
    }

    if (lastName !== undefined) {
      updateFields.push(`last_name = $${paramCount++}`);
      updateValues.push(lastName);
    }

    if (updateFields.length === 0) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'No fields to update'
        }
      });
    }

    // Add updated_at and user id
    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    updateValues.push(userId);

    const updateQuery = `
      UPDATE users 
      SET ${updateFields.join(', ')}
      WHERE id = $${paramCount}
      RETURNING id, username, email, first_name, last_name, role, is_active, updated_at
    `;

    const result = await executeQuery(updateQuery, updateValues);

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 404,
          message: 'User not found'
        }
      });
    }

    const updatedUser = result.rows[0];

    logger.info(`User profile updated: ${updatedUser.username}`);

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: updatedUser.id,
          username: updatedUser.username,
          email: updatedUser.email,
          firstName: updatedUser.first_name,
          lastName: updatedUser.last_name,
          role: updatedUser.role,
          isActive: updatedUser.is_active,
          updatedAt: updatedUser.updated_at
        }
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Change password
// @route   PUT /api/v1/users/change-password
// @access  Private
router.put('/change-password', validate('changePassword'), async (req, res, next) => {
  try {
    const { currentPassword, newPassword } = req.body;
    const userId = req.user.id;

    // Get current user with password hash
    const userQuery = 'SELECT id, username, password_hash FROM users WHERE id = $1';
    const userResult = await executeQuery(userQuery, [userId]);

    if (userResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 404,
          message: 'User not found'
        }
      });
    }

    const user = userResult.rows[0];

    // Verify current password
    const isCurrentPasswordValid = await bcrypt.compare(currentPassword, user.password_hash);
    if (!isCurrentPasswordValid) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Current password is incorrect'
        }
      });
    }

    // Hash new password
    const salt = await bcrypt.genSalt(parseInt(process.env.BCRYPT_ROUNDS) || 12);
    const hashedNewPassword = await bcrypt.hash(newPassword, salt);

    // Update password
    const updateQuery = `
      UPDATE users 
      SET password_hash = $1, updated_at = CURRENT_TIMESTAMP 
      WHERE id = $2
    `;
    
    await executeQuery(updateQuery, [hashedNewPassword, userId]);

    logger.info(`Password changed for user: ${user.username}`);

    res.status(200).json({
      success: true,
      message: 'Password changed successfully'
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Get all users (Admin only)
// @route   GET /api/v1/users
// @access  Private/Admin
router.get('/', authorize('admin'), async (req, res, next) => {
  try {
    const { page = 1, limit = 10, search, role, isActive } = req.query;
    const offset = (page - 1) * limit;

    // Build query with filters
    let whereConditions = [];
    let queryParams = [];
    let paramCount = 1;

    if (search) {
      whereConditions.push(`(username ILIKE $${paramCount} OR email ILIKE $${paramCount} OR first_name ILIKE $${paramCount} OR last_name ILIKE $${paramCount})`);
      queryParams.push(`%${search}%`);
      paramCount++;
    }

    if (role) {
      whereConditions.push(`role = $${paramCount++}`);
      queryParams.push(role);
    }

    if (isActive !== undefined) {
      whereConditions.push(`is_active = $${paramCount++}`);
      queryParams.push(isActive === 'true');
    }

    const whereClause = whereConditions.length > 0 ? `WHERE ${whereConditions.join(' AND ')}` : '';

    // Get total count
    const countQuery = `
      SELECT COUNT(*) as total
      FROM users
      ${whereClause}
    `;
    
    const countResult = await executeQuery(countQuery, queryParams);
    const total = parseInt(countResult.rows[0].total);

    // Get users with pagination
    const usersQuery = `
      SELECT id, username, email, first_name, last_name, role, is_active, last_login, created_at, updated_at
      FROM users
      ${whereClause}
      ORDER BY created_at DESC
      LIMIT $${paramCount++} OFFSET $${paramCount++}
    `;
    
    queryParams.push(parseInt(limit), offset);
    const usersResult = await executeQuery(usersQuery, queryParams);

    const users = usersResult.rows.map(user => ({
      id: user.id,
      username: user.username,
      email: user.email,
      firstName: user.first_name,
      lastName: user.last_name,
      role: user.role,
      isActive: user.is_active,
      lastLogin: user.last_login,
      createdAt: user.created_at,
      updatedAt: user.updated_at
    }));

    res.status(200).json({
      success: true,
      data: {
        users,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / limit)
        }
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Get user by ID (Admin only)
// @route   GET /api/v1/users/:id
// @access  Private/Admin
router.get('/:id', authorize('admin'), async (req, res, next) => {
  try {
    const { id } = req.params;

    const userQuery = `
      SELECT id, username, email, first_name, last_name, role, is_active, last_login, created_at, updated_at
      FROM users 
      WHERE id = $1
    `;
    
    const result = await executeQuery(userQuery, [id]);

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 404,
          message: 'User not found'
        }
      });
    }

    const user = result.rows[0];

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role,
          isActive: user.is_active,
          lastLogin: user.last_login,
          createdAt: user.created_at,
          updatedAt: user.updated_at
        }
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Update user by ID (Admin only)
// @route   PUT /api/v1/users/:id
// @access  Private/Admin
router.put('/:id', authorize('admin'), validate('updateProfile'), async (req, res, next) => {
  try {
    const { id } = req.params;
    const { username, email, firstName, lastName, role, isActive } = req.body;

    // Check if user exists
    const existingUserQuery = 'SELECT id, username, email FROM users WHERE id = $1';
    const existingUserResult = await executeQuery(existingUserQuery, [id]);

    if (existingUserResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 404,
          message: 'User not found'
        }
      });
    }

    const existingUser = existingUserResult.rows[0];

    // Check if username is available (if changing)
    if (username && username !== existingUser.username) {
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
    }

    // Check if email is available (if changing)
    if (email && email !== existingUser.email) {
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
    }

    // Build update query
    const updateFields = [];
    const updateValues = [];
    let paramCount = 1;

    if (username) {
      updateFields.push(`username = $${paramCount++}`);
      updateValues.push(username);
    }

    if (email) {
      updateFields.push(`email = $${paramCount++}`);
      updateValues.push(email);
    }

    if (firstName !== undefined) {
      updateFields.push(`first_name = $${paramCount++}`);
      updateValues.push(firstName);
    }

    if (lastName !== undefined) {
      updateFields.push(`last_name = $${paramCount++}`);
      updateValues.push(lastName);
    }

    if (role) {
      updateFields.push(`role = $${paramCount++}`);
      updateValues.push(role);
    }

    if (isActive !== undefined) {
      updateFields.push(`is_active = $${paramCount++}`);
      updateValues.push(isActive);
    }

    if (updateFields.length === 0) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'No fields to update'
        }
      });
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    updateValues.push(id);

    const updateQuery = `
      UPDATE users 
      SET ${updateFields.join(', ')}
      WHERE id = $${paramCount}
      RETURNING id, username, email, first_name, last_name, role, is_active, updated_at
    `;

    const result = await executeQuery(updateQuery, updateValues);
    const updatedUser = result.rows[0];

    logger.info(`User updated by admin: ${updatedUser.username}`);

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: updatedUser.id,
          username: updatedUser.username,
          email: updatedUser.email,
          firstName: updatedUser.first_name,
          lastName: updatedUser.last_name,
          role: updatedUser.role,
          isActive: updatedUser.is_active,
          updatedAt: updatedUser.updated_at
        }
      }
    });
  } catch (error) {
    next(error);
  }
});

// @desc    Delete user (Admin only)
// @route   DELETE /api/v1/users/:id
// @access  Private/Admin
router.delete('/:id', authorize('admin'), async (req, res, next) => {
  try {
    const { id } = req.params;

    // Check if user exists
    const userQuery = 'SELECT id, username FROM users WHERE id = $1';
    const userResult = await executeQuery(userQuery, [id]);

    if (userResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 404,
          message: 'User not found'
        }
      });
    }

    const user = userResult.rows[0];

    // Prevent admin from deleting themselves
    if (parseInt(id) === req.user.id) {
      return res.status(400).json({
        success: false,
        error: {
          code: 400,
          message: 'Cannot delete your own account'
        }
      });
    }

    // Delete user
    const deleteQuery = 'DELETE FROM users WHERE id = $1';
    await executeQuery(deleteQuery, [id]);

    logger.info(`User deleted by admin: ${user.username}`);

    res.status(200).json({
      success: true,
      message: 'User deleted successfully'
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router; 