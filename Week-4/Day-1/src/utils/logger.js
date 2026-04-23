import winston from 'winston';
import config from '../config/index.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { traceHolder } from '../middlewares/trace.middleware.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const logsDir = path.resolve(__dirname, '../../logs');

if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

const formatWithTrace = winston.format.printf((info) => {
  
  const requestId = traceHolder.getStore();
  const idPart = requestId ? ` [ID:${requestId}]` : '';

  return `${info.timestamp} ${info.level}${idPart} : ${info.message}`;
});

const logger = winston.createLogger({
  level: config.logs?.level || 'info',
  levels: { error: 0, warn: 1, info: 2, http: 3, debug: 4 },
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
    formatWithTrace
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize({ all: true }),
        winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
        formatWithTrace
      ),
    }),

    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      format: winston.format.combine(
        winston.format.uncolorize(), 
        winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
        formatWithTrace
      ),
      maxsize: 5242880, 
    }),
    
    new winston.transports.File({
      filename: path.join(logsDir, 'combined.log'),
      maxsize: 10485760, // 10MB
    }),
  ],
});

export default logger;