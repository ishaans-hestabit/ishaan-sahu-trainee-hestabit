import accountsRoute from "../routes/account.routes.js";
import ordersRoute from "../routes/order.routes.js";
import healthRoute from "../routes/health.routes.js";
import productRoute from "../routes/product.routes.js";
import loginRoute from "../routes/login.routes.js";
import errorMiddleware from "../middlewares/error.middleware.js";
import logger from "../utils/logger.js"
import protect from "../middlewares/auth.middleware.js";
import accountController from "../controllers/account.controller.js";
import { validate } from "../middlewares/validation.middleware.js";
import { registerAccountSchema, emailParamSchema, updateNameSchema,} from "../validation/account.validation.js";

export default ({ app }) => {

  app.use("/login", loginRoute);
  app.post("/accounts/addAccount", validate(registerAccountSchema), accountController.register);

  app.use(protect);

  app.use("/health",healthRoute);

  app.use("/accounts", accountsRoute);
  
  app.use("/orders", ordersRoute);

  app.use("/product",productRoute);

  app.use(errorMiddleware);

  logger.info("✔ Routes loaded")
};