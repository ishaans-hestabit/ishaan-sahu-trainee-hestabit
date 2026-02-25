import { Router } from "express";
import accountController from "../controllers/account.controller.js"

const router = Router();

router.post("/addAccount",accountController.register);

router.get("/:email",accountController.getByEmail);

router.delete("/:email",accountController.deleteByEmail);

router.patch("/updateName",accountController.updateEmail);

export default router;