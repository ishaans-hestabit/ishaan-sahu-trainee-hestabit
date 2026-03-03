import { Worker } from "bullmq";
import logger from "../../utils/logger.js";
import {sendWelcomeEmail} from "../../services/email.service.js"
import { redisConnection } from "../../config/redis.js";
import { traceHolder } from "../../middlewares/trace.middleware.js";

const QUEUE_NAME = 'email-queue';

export const setupEmailWorker = ()=>{
    const worker = new Worker(QUEUE_NAME,
        async (job)=>{

            await traceHolder.run(job.data.requestID, async()=>{
                logger.info(`Starting Email Job: for ${job.data.email}`);
                await sendWelcomeEmail(job.data);
            });
        },
        { 
            connection: redisConnection,
            concurrency: 5 
        }
    )

    worker.on('failed', (job, err) => {
        logger.error(`Email Job failed for ${job.data.email}: ${err.message}`);
    });
}