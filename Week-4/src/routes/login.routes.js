import accountController from '../controllers/account.controller.js';
import {Router } from 'express'

const router = Router();

router.post("/",accountController.login);

export default router;