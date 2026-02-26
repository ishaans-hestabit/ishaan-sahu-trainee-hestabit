import mongoose from "mongoose";
import dotenv from "dotenv";
import Product from "../models/ProductSchema.js";

dotenv.config({ path: ".env.local" });

const products = [];
const TAGS = ["electronics", "fashion", "books", "home", "sports"];

for (let i = 1; i <= 40; i++) {
  products.push({
    name: `Product ${i}`,
    description: `Description for product ${i}`,
    price: i * 100,
    tags: [
      TAGS[i % TAGS.length],
      TAGS[(i + 1) % TAGS.length]
    ]
  });
}

const seedProducts = async () => {
  try {
    await mongoose.connect(process.env.DATABASE_URL);

    // await Product.deleteMany();

    await Product.create(products);

    console.log("Products seeded successfully with tags");
    process.exit();
  } catch (error) {
    console.error("Product seeder error", error);
    process.exit(1);
  }
};

seedProducts();