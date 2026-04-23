import Account from '../models/AccountSchema.js'
import AppError from '../utils/AppError.js';
import bcrypt from "bcrypt";
import { BaseRepository } from './BaseRepository.js'

class AccountRepository extends BaseRepository{
    constructor(){
        super(Account);
    }

    async login(data) {
        const account = await Account.findOne({ email: data.email }).select('+password');

        if (!account) return null;

        const isMatch = await account.comparePassword(data.password);
        if (!isMatch) return null;

        return account;
    }

    async findByEmail(email, includePassword = false) {
        const query = this.model.findOne({ email });
        if (includePassword) query.select('+password');
        return await query;
    }

    async delete(email){
        return await this.model.findOneAndUpdate({email},{isDeleted: true},{ returnDocument: "after",
    runValidators: true });
    }

    async updateName(data){
        return await this.model.findOneAndUpdate({email: data.email},{
            firstName: data.firstName
        },{ returnDocument: "after",
    runValidators: true });
    }
}

export default new AccountRepository();