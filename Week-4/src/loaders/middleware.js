import express from 'express';
import cors from 'cors';
import logger from '../utils/logger.js';

export default async ({ app }) => {
  
  app.use(cors('*'));   
  app.use(express.json());

  logger.info('✔ Middlewares loaded');

  return app;
};