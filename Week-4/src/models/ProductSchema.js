import mongoose from "mongoose";
const { Schema } = mongoose;

const ProductSchema = new Schema({
    name: { type: String, required: true, trim: true },
    description: { type: String },
    price: { type: Number, required: true, min: 0 },
    },
    { timestamps: true } );

export default mongoose.model("Product", ProductSchema);