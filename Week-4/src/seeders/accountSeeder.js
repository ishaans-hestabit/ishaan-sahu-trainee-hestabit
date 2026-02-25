
import mongoose from "mongoose";
import dotenv from "dotenv";
import User from "../models/AccountSchema.js";
 
dotenv.config({ path: ".env.local" });
 
const users = [];
 
for (let i = 1; i <= 40; i++) {
  users.push({
    firstName: `User ${i}`,
    lastName: `Last ${i}`,
    email: `user${i}@example.com`,
    password: "password123",
  });
}
 
const seedUsers = async () => {
  try {
    await mongoose.connect(process.env.DATABASE_URL);
 
    // await User.deleteMany();
 
    await User.create(users);
 
    console.log("Users seeded successfully");
    process.exit();
  } catch (error) {
    console.error("Seeder error", error);
    process.exit(1);
  }
};
 
seedUsers();
 