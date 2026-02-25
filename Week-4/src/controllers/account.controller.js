import accountService from "../services/account.service.js";

class AccountController {
  async register(req, res, next) {
    try {
        // console.log(req.body);
        
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

  async deleteByEmail(req,res,next){
    try{
        const deletedAccount = await accountService.deleteByEmail(req.params.email);
        if (!deletedAccount) {
        return res.status(404).json({ message: "Account not found" });
      }
      res.json(deletedAccount);
    }
    catch (err) {
      next(err);
    }
  }

  async updateEmail(req,res,next){
    try{
        // console.log(req.body);
        
        const updatedAccount = await accountService.updateName(req.body);

        if(!updatedAccount){
            return res.status(404).json({ message: "Account not found" });
        }
        res.json(updatedAccount);
    }
    catch(err){
        next(err);
    }
  }
}

export default new AccountController();