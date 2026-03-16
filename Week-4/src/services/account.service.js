import { queueWelcomeEmail } from "../jobs/email/email.queue.js";
import accountRepository from "../repositories/account.repository.js";
import AppError from "../utils/AppError.js";
import jwt from 'jsonwebtoken';

class AccountService {
  async register(data) {
    const existing = await accountRepository.findByEmail(data.email);
    if (existing) {
      throw new AppError("Email already exists", 409, 'Duplicate Found');
    }

    const account = await accountRepository.create(data);  
    
    queueWelcomeEmail(account);

    return account;

  }

  async findAll(){
    const users = await accountRepository.findAll();
    if(!users){
      throw AppError("Unable to find Accounts", 404,"Accounts not found")
    }
    else {
      return users;
    }
  }

    async login(email, password) {
        const account = await accountRepository.login({ email, password });
        if (!account) {
          throw new AppError("Email or password wrong", 401, "Unauthorized");
        }

        const token = jwt.sign(
          { id: account._id, email: account.email },
          process.env.JWT_SECRET,
          { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
        );

        return token; 
    }

  async getByEmail(email) {
    return accountRepository.findByEmail(email);
  }

  async deleteByEmail(email){
    return accountRepository.delete(email);
  }

  async updateName(data){
    return accountRepository.updateName(data);
  }
}

export default new AccountService();