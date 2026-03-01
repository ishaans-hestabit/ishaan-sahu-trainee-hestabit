import { Router } from "express";
import productController from "../controllers/product.controller.js";
import { validate } from "../middlewares/validation.middleware.js";
import { createProductSchema, productQuerySchema, productIdParamSchema} from "../validation/product.validation.js";

const router = Router();

router.post( "/", validate(createProductSchema),productController.createProduct);

router.get( "/", validate(productQuerySchema), productController.getProducts);

router.get( "/:id", validate(productIdParamSchema), productController.getProductById );

router.delete( "/:id", validate(productIdParamSchema), productController.deleteProduct);

export default router;