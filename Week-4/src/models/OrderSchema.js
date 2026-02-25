import mongoose from "mongoose";
const { Schema } = mongoose;

const OrderSchema = new Schema(
  {
    account: {
      type: Schema.Types.ObjectId,
      ref: "Account",
      required: true
    },

    items: [
      {
        product: {
          type: Schema.Types.ObjectId,
          ref: "Product",
          required: true
        },
        quantity: {
          type: Number,
          required: true,
          min: 1
        },
        priceAtPurchase: {
          type: Number,
          required: true
        }
      }
    ],

    totalAmount: {
      type: Number,
    },

    status: {
      type: String,
      enum: ["pending", "processing", "shipped", "delivered", "cancelled"],
      default: "pending"
    }
  },
  { timestamps: true }
);

OrderSchema.pre("save", function () {
  this.totalAmount = this.items.reduce(
    (sum, item) => sum + item.priceAtPurchase * item.quantity,
    0
  );
});

OrderSchema.index({ status: 1, createdAt: -1 });

export default mongoose.model("Order", OrderSchema);