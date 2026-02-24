import winston from 'winston'
import config from '../config/index.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const logsDir = path.resolve(__dirname, '../../logs'); 

if (config.env === 'prod' && !fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

const colors = {
  error: 'red',
  warn: 'yellow',
  info: 'blue',
  http: 'magenta',
  debug: 'white',
};

winston.addColors(colors);

const format = winston.format.combine(
    winston.format.timestamp({format: 'YYYY-MM-DD HH:mm:ss.SSS'}),

    config.env === 'local' || config.env === 'dev' ? winston.format.colorize({all: true}) : winston.format.uncolorize(),

    winston.format.printf(
        info => `${info.timestamp} ${info.level} : ${info.message}`
    )
);

const logger = winston.createLogger({
    level: config.logs.level, // this defines the base level, log those which are equal or more sever than this 
    // less means more sever
    levels: { error: 0, warn: 1, info: 2, http: 3, debug: 4 },
    format,
    transports: [
    new winston.transports.Console(),

    ...(config.env === 'prod'
      ? [new winston.transports.File({ filename: `${logsDir}/error.log`, level: 'error' })]
      : [])
  ],
});

export default logger;