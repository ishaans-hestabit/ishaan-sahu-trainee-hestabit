import {v4 as uuidv4} from 'uuid';
import { AsyncLocalStorage } from 'async_hooks';

export const traceHolder = new AsyncLocalStorage();

export const requestTracer = (req,res,next)=>{

    const requestId = req.get('X-Request-ID') || uuidv4();

    res.setHeader('X-Request-ID', requestId);

    traceHolder.run(requestId,()=>{
        next();
    })
}