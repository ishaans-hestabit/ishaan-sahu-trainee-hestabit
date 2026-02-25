import accountsRoute from "../routes/account.routes.js"
import healthRoute from "../routes/health.routes.js";

export default ({app})=>{
    app.use("/health",healthRoute);
    app.use("/accounts",accountsRoute);
}