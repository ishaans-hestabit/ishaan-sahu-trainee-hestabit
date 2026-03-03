import dbLoader from './db.js';
import middlewareLoader from './middleware.js';
import routeLoader from '../loaders/routes.js'
import { setupEmailWorker } from '../jobs/email/email.worker.js';
import logger from '../utils/logger.js';

export default async ({ expressApp }) => {
  await dbLoader();
  
  await middlewareLoader({ app: expressApp });


  await routeLoader({app: expressApp});

  setupEmailWorker();
  logger.info('Background Email Worker initialized');
};