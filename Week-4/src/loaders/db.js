import mongoose from 'mongoose';
import config from '../config/index.js';
import logger from '../utils/logger.js';

export default async () => {
  try {
    const connection = await mongoose.connect(config.dbUrl);
    
    logger.info('✔ Database connected');
    
    return connection.connection.db;
  } catch (error) {
    logger.error('Database connection failed: ', error.message);
    process.exit(1);
  }
};