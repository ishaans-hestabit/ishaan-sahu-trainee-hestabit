import { queueWelcomeEmail } from "../jobs/email/email.queue.js";
import accountRepository from "../repositories/account.repository.js";
import AppError from "../utils/AppError.js";

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