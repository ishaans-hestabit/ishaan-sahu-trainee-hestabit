import dbLoader from './db.js';
import middlewareLoader from './middleware.js';

export default async ({ expressApp }) => {
  await dbLoader();
  
  await middlewareLoader({ app: expressApp });
};