import IORedis from 'ioredis';
import logger from '../utils/logger.js';
import AppError from '../utils/AppError.js';

const redisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: process.env.REDIS_PORT || 6379,
  maxRetriesPerRequest: null, 
};

export const redisConnection = new IORedis(redisConfig);

redisConnection.on('error', (err) => {
    logger.error('Redis Connection Error', err)
    throw new AppError("Unable to connect to Redis", 503, "Redis Connection Error")
});
redisConnection.on('connect', () => logger.info('Successfully connected to Redis'));