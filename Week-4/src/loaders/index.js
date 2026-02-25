import dbLoader from './db.js';
import middlewareLoader from './middleware.js';
import routeLoader from '../loaders/routes.js'

export default async ({ expressApp }) => {
  await dbLoader();
  
  await middlewareLoader({ app: expressApp });

  await routeLoader({app: expressApp});
};