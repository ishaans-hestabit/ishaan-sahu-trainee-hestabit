import Account from '../models/AccountSchema.js'

import { BaseRepository } from './BaseRepository.js'

class AccountRepository extends BaseRepository{
    constructor(){
        super(Account);
    }

    async findByEmail(email, includePassword = false) {
        const query = this.model.findOne({ email });
        if (includePassword) query.select('+password');
        return await query;
    }

    async delete(id){
        return await this.model.findByIdAndUpdate(id,{isDeleted: true},{ new: true });
    }
}

export default new AccountRepository();