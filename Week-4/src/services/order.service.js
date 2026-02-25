import orderRepository from "../repositories/order.repository.js";

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
      const err = new Error("Invalid order status");
      err.status = 400;
      throw err;
    }

    return orderRepository.updateStatus(orderId, status);
  }
}

export default new OrderService();