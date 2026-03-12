import orderRepository from "../repositories/order.repository.js";
import AppError from "../utils/AppError.js";

class OrderService {
  async createOrder(data) {
    return orderRepository.create(data);
  }

  async getOrderById(orderId) {
    return orderRepository.findById(orderId);
  }

  async getOrdersByAccount(accountId) {
    return orderRepository.findByAccount(accountId);
  }

  async updateOrderStatus(orderId, status) {
    const allowedStatuses = [
      "pending",
      "processing",
      "shipped",
      "delivered",
      "cancelled"
    ];

    if (!allowedStatuses.includes(status)) {
      throw new AppError("Invalid order status", 400, "Invalid Status");
    }

    return orderRepository.updateStatus(orderId, status);
  }
}

export default new OrderService();