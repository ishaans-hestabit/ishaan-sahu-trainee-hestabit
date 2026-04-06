import mongoose from "mongoose";
import bcrypt from "bcrypt";
import validator from 'validator';

const { Schema } = mongoose;

const AccountSchema = new Schema(
  {
    firstName: {
      type: String,
      required: [true, "First name is required"],
      trim: true,
    },

    lastName: {
      type: String,
      required: [true, "Last name is required"],
      trim: true,
    },

    email: {
      type: String,
      required: [true, "Email is required"],
      lowercase: true,
      trim: true,
      unique: true,
      index: true,
      validate: {
      validator: validator.isEmail,
      message: "Invalid email format"
    }
    },

    password: {
      type: String,
      required: [true, "Password is required"],
      select: false
    },

    isDeleted: {
      type: Boolean,
      default: false,
      index: true
    }
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

AccountSchema.pre("save", async function (next) {
  try {
    if (!this.isModified("password")) return next();
    this.password = await bcrypt.hash(this.password, 12);
  } catch (err) {
    next(err);
  }
});


AccountSchema.pre(/^find/, function () {
  if (!this.getOptions().includeDeleted) {
    this.where({ isDeleted: false });
  }
});

AccountSchema.virtual("fullName").get(function () {
  return `${this.firstName} ${this.lastName}`;
});

AccountSchema.methods.comparePassword = async function (candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

export default mongoose.model("Account", AccountSchema);