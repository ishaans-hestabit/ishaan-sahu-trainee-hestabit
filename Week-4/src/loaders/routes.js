import accountsRoute from "../routes/account.routes.js";
import ordersRoute from "../routes/order.routes.js";
import healthRoute from "../routes/health.routes.js";
import productRoute from "../routes/product.routes.js";
import errorMiddleware from "../middlewares/error.middleware.js";
import logger from "../utils/logger.js"

export default ({ app }) => {

  app.use("/health", healthRoute);

  app.use("/accounts", accountsRoute);
  
  app.use("/orders", ordersRoute);

  app.use("/product",productRoute);

  app.use(errorMiddleware);

  logger.info("✔ Routes loaded")
};