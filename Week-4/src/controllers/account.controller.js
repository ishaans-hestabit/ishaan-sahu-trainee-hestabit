import accountService from "../services/account.service.js";

class AccountController {
  async register(req, res, next) {
    try {
        console.log(req.body);
        
      const account = await accountService.register(req.body);
      res.status(201).json(account);
    } catch (err) {
      next(err);
    }
  }

  async getByEmail(req, res, next) {
    try {
        
      const account = await accountService.getByEmail(req.params.email);
      if (!account) {
        return res.status(404).json({ message: "Account not found" });
      }
      res.json(account);
    } catch (err) {
      next(err);
    }
  }
}

export default new AccountController();