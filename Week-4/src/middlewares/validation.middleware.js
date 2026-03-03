import { ZodError } from "zod";
import AppError from "../utils/AppError.js";

export const validate = (schema) => (req, res, next) => {
  try {
   
    schema.parse({
      body: req.body,
      params: req.params,
      query: req.query,
    });
    
    next();
  } catch (err) {
     
    if (err instanceof ZodError) {
        
      const message = err.issues
        .map((e) => `${e.path.join(".")}: ${e.message}`)
        .join(", ");
       
      return next(
        new AppError(
          message,
          422, // Unprocessable Entity
          "VALIDATION_ERROR"
        )
      );
    }
    
    
    next(err);
  }
};