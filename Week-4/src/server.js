import express from 'express';
import config from './config/index.js';
import loaders from './loaders/index.js';
import logger from './utils/logger.js';

async function startServer() {
  const app = express();

  try {
    await loaders({ expressApp: app });

    app.listen(config.port, (err) => {
      if (err) {
        logger.error('Server failed to start: ', err);
        process.exit(1);
      }

      logger.info(`✔ Server started on port ${config.port}`);
    });
  } catch (bootError) {
    logger.error('App failed to bootstrap:', bootError);
    process.exit(1);
  }
}

startServer();