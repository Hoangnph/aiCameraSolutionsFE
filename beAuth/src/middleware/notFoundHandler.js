// Not found handler middleware
function notFoundHandler(req, res, next) {
  // Skip logging for common browser requests that are expected to fail
  const skipLogging = [
    '/favicon.ico',
    '/robots.txt',
    '/.well-known/appspecific/com.chrome.devtools.json',
    '/.well-known/security.txt'
  ];
  
  const error = new Error(`Not Found - ${req.originalUrl}`);
  error.statusCode = 404;
  
  // Only log if it's not a common browser request
  if (!skipLogging.includes(req.originalUrl)) {
    next(error);
  } else {
    res.status(404).json({
      success: false,
      error: {
        code: 404,
        message: 'Not Found'
      }
    });
  }
}

module.exports = { notFoundHandler }; 