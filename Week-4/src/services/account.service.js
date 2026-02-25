import accountRepository from "../repositories/account.repository.js";

class AccountService {
  async register(data) {
    const existing = await accountRepository.findByEmail(data.email);
    if (existing) {
      const err = new Error("Email already exists");
      err.status = 409;
      throw err;
    }

    return accountRepository.create(data);
  }

  async getByEmail(email) {
    return accountRepository.findByEmail(email);
  }
}

export default new AccountService();