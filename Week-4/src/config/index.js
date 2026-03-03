import dotenv from 'dotenv';
import {z} from 'zod';
import path from 'path';
import { fileURLToPath } from 'url';

const VALID_ENVS = ['local', 'dev', 'prod'];
const nodeEnv = process.env.NODE_ENV || 'local';

if (!VALID_ENVS.includes(nodeEnv)) {
    console.error(`Invalid NODE_ENV: ${nodeEnv}. Expected one of: ${VALID_ENVS.join(', ')}`);
    process.exit(1);
}

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, '../../', `.env.${nodeEnv}`);

// loads data from that .env file to process.env
const envFound = dotenv.config({ path: envPath });

// console.log(envPath);

if(envFound.error){
	throw new Error(` Could'nt find .env file`)
}

const envSchema = z.object({
	PORT: z.coerce.number().int().min(1000).max(65535).default(3001),
	DATABASE_URL: z.string().min(1, "DB URL is required"),
	LOG_LEVEL: z.enum(['info', 'debug', 'error']).default('info'),
});

const envVars = envSchema.safeParse(process.env);
console.log(envVars);


if (!envVars.success) {
  const errors = envVars.error.flatten().fieldErrors;
  
  console.error('Environment Validation Failed:');
  console.table(errors);
  process.exit(1);
}

export default{
	port:envVars.data.PORT,
	dbUrl: envVars.data.DATABASE_URL,
	logs: {
		level: envVars.data.LOG_LEVEL
	},
    env:process.env.NODE_ENV
};

