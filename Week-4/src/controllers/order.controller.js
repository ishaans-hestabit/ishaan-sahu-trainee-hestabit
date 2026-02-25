import orderService from "../services/order.service.js";

class OrderController {
  async create(req, res, next) {
    try {
      const order = await orderService.createOrder(req.body);
      res.status(201).json(order);
    } catch (err) {
      next(err);
    }
  }

  async getById(req, res, next) {
    try {
        // console.log(req.params.id);
        
      const order = await orderService.getOrderById(req.params.id);
      if (!order) {
        return res.status(404).json({ message: "Order not found" });
      }
      res.json(order);
    } catch (err) {
      next(err);
    }
  }

  async getByAccount(req, res, next) {
    try {
      const orders = await orderService.getOrdersByAccount(req.params.accountId);
      if (!orders) {
        return res.status(404).json({ message: "Account not found" });
      }
      res.json(orders);
    } catch (err) {
      next(err);
    }
  }

  async updateStatus(req, res, next) {
    try {
      const updated = await orderService.updateOrderStatus(
        req.params.id,
        req.body.status
      );

      if (!updated) {
        return res.status(404).json({ message: "Order not found" });
      }

      res.json(updated);
    } catch (err) {
      next(err);
    }
  }
}

export default new OrderController();