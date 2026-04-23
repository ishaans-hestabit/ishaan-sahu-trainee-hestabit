import AppError from "../utils/AppError.js";

const errorMiddleware = (err, req, res, next) => {
  let error = err;

  if (!(error instanceof AppError)) {
    error = new AppError(
      "Something went wrong",
      500,
      "INTERNAL_SERVER_ERROR"
    );
  }

  const statusCode = error.statusCode || 500;

  res.status(statusCode).json({
    success: false,
    message: error.message,
    code: error.code,
    timestamp: new Date().toISOString(),
    path: req.originalUrl
  });
};

export default errorMiddleware;