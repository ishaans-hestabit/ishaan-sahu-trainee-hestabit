import express from "express";
import cors from "cors";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import logger from "../utils/logger.js";
import { requestTracer } from "../middlewares/trace.middleware.js";

export default async ({ app }) => {
  
  app.use(requestTracer);

  app.use(
    cors({
      origin: "*",
      methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
    })
  );
  app.use(helmet());
  
  app.use(
    express.json({
      limit: "10kb",
    })
  );
  app.use(
    express.urlencoded({
      extended: true,
      limit: "10kb",
    })
  );

  const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100,               
  });
  app.use(apiLimiter);


  logger.info("✔ Middlewares loaded");
  return app;
};