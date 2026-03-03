import logger from "./logger.js";

export default class AppError extends Error {
  constructor(message, statusCode = 500, code = "INTERNAL_ERROR") {
    super(message);

    this.statusCode = statusCode;
    this.code = code;
    this.isOperational = true;

    logger.error(`Error Occured Message: ${message} statusCode: ${statusCode}`)

    Error.captureStackTrace(this, this.constructor);
  }
}