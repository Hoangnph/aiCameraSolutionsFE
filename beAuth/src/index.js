const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const { errorHandler } = require('./middleware/errorHandler');
const { notFoundHandler } = require('./middleware/notFoundHandler');
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/user');
const { connectDatabase } = require('./config/database');
const logger = require('./utils/logger');

const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());

// CORS configuration
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting - enabled with optimized settings for testing
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000, // 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 1000, // 1000 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.'
  },
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests from this IP, please try again later.',
      retryAfter: Math.ceil(parseInt(process.env.RATE_LIMIT_WINDOW_MS) / 1000 / 60) // minutes
    });
  },
  skip: (req) => {
    // Skip rate limiting for token verification endpoint
    return req.path === '/api/v1/auth/verify' || req.path === '/api/v1/auth/verify/';
  }
});
// app.use("/api/", limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging middleware
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));

// Root endpoint
app.get('/', (req, res) => {
  res.status(200).json({
    message: 'Authentication Service API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      auth: `/api/${process.env.API_VERSION || 'v1'}/auth`,
      users: `/api/${process.env.API_VERSION || 'v1'}/users`
    },
    documentation: 'Check the API documentation for available endpoints'
  });
});

// Favicon handler
app.get('/favicon.ico', (req, res) => {
  res.status(204).end(); // No content response
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    service: 'Authentication Service',
    version: '1.0.0'
  });
});

// API routes
app.use(`/api/${process.env.API_VERSION || 'v1'}/auth`, authRoutes);
app.use(`/api/${process.env.API_VERSION || 'v1'}/users`, userRoutes);

// Error handling middleware
app.use(notFoundHandler);
app.use(errorHandler);

// Start server
async function startServer() {
  try {
    // Connect to database
    await connectDatabase();
    logger.info('Database connected successfully');

    // Start server
    app.listen(PORT, () => {
      logger.info(`Authentication service running on port ${PORT}`);
      logger.info(`Environment: ${process.env.NODE_ENV}`);
      logger.info(`API Version: ${process.env.API_VERSION || 'v1'}`);
    });
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  logger.error('Unhandled Promise Rejection:', err);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  logger.error('Uncaught Exception:', err);
  process.exit(1);
});

startServer();

module.exports = app; 