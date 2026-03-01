import { Router } from "express";
import accountController from "../controllers/account.controller.js";
import { validate } from "../middlewares/validation.middleware.js";
import { registerAccountSchema, emailParamSchema, updateNameSchema,} from "../validation/account.validation.js";

const router = Router();

router.post( "/addAccount", validate(registerAccountSchema), accountController.register);

router.get( "/:email", validate(emailParamSchema), accountController.getByEmail);

router.delete( "/:email", validate(emailParamSchema), accountController.deleteByEmail);

router.patch( "/updateName", validate(updateNameSchema), accountController.updateEmail);

export default router;