import { Router } from "express";
import accountController from "../controllers/account.controller.js"

const router = Router();

router.post("/addAccount",accountController.register);

router.get("/:email",accountController.getByEmail);

export default router;