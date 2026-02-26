import mongoose from "mongoose";
const { Schema } = mongoose;

const ProductSchema = new Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      index: true
    },

    description: {
      type: String,
      trim: true
    },

    price: {
      type: Number,
      required: true,
      min: 0,
      index: true
    },

    tags: {
      type: [String],
      index: true
    },

    deletedAt: {
      type: Date,
      default: null,
      index: true
    }
  },
  { timestamps: true }
);


ProductSchema.pre(/^find/, function () {
  if (!this.getOptions().includeDeleted) {
    this.where({ deletedAt: null });
  }
});

export default mongoose.model("Product", ProductSchema);