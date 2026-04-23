import Order from "../models/OrderSchema.js";
import { BaseRepository } from "./BaseRepository.js";

class OrderRepository extends BaseRepository {
  constructor() {
    super(Order);
  }

  async findById(id) {
    return this.model
      .findById(id)
      .populate("account");
  }

  async findByAccount(accountId) {
    return this.model
      .find({ account: accountId })
      .sort({ createdAt: -1 });
  }

  async updateStatus(orderId, status) {
    return this.model.findOneAndUpdate(
      { _id: orderId },
      { status },
      {
        returnDocument: "after",
        runValidators: true
      }
    );
  }
}

export default new OrderRepository();