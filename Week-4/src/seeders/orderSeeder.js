import mongoose from "mongoose";
import dotenv from "dotenv";

import Account from "../models/AccountSchema.js";
import Order from "../models/OrderSchema.js";

dotenv.config({ path: ".env.local" });

const seedOrders = async () => {
  try {
    await mongoose.connect(process.env.DATABASE_URL);
    const accounts = await Account.find();

    if (!accounts.length) {
      throw new Error("No accounts found. Seed accounts first.");
    }

    const orders = [];

    accounts.forEach((account, index) => {
      orders.push({
        account: account._id,
        items: [
          {
            product: new mongoose.Types.ObjectId(),
            quantity: 2,
            priceAtPurchase: 499
          },
          {
            product: new mongoose.Types.ObjectId(),
            quantity: 1,
            priceAtPurchase: 1299
          }
        ],
        status: index % 2 === 0 ? "pending" : "processing"
      });
    });

    // await Order.deleteMany(); 

    await Order.insertMany(orders, {runValidators: true});

    console.log("Orders seeded successfully");
    process.exit();
  } catch (error) {
    console.error("Order seeder error:", error);
    process.exit(1);
  }
};

seedOrders();