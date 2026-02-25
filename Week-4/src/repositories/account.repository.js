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