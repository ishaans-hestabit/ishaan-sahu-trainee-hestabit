import { Queue } from "bullmq";

import {redisConnection} from "../../config/redis.js"
import { traceHolder } from "../../middlewares/trace.middleware.js";

const QUEUE_NAME = 'email-queue';

const emailQueue = new Queue(QUEUE_NAME, { connection: redisConnection });

export const queueWelcomeEmail = async (user) => {
  return await emailQueue.add('send-welcome', {
    firstName: user.firstName,
    lastName: user.lastName,
    email: user.email,
    createdAt: user.createdAt,
    requestID: traceHolder.getStore()
  }, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 }
  });
};