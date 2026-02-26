import { BaseRepository } from "./BaseRepository.js";
import Product from "../models/ProductSchema.js";
import AppError from "../utils/AppError.js";

class ProductRepository extends BaseRepository {
  constructor() {
    super(Product);
  }

  
  async findWithCursor(filter = {}, options = {}) {
    const {
      limit = 10,
      cursor = null,
      sortOrder = 1,
      includeDeleted = false
    } = options;

    const query = { ...filter };

    const parsedLimit = Number(limit);
        
    if (!Number.isFinite(parsedLimit) || parsedLimit <= 0) {
      throw new AppError("Limit must be a positive number", 400, "INVALID_LIMIT");
    }

    if (cursor) {
      query.$or = [
        { price: { [sortOrder === 1 ? "$gt" : "$lt"]: cursor.price } },
        {
          price: cursor.price,
          _id: { [sortOrder === 1 ? "$gt" : "$lt"]: cursor.id }
        }
      ];
    }

    const docs = await this.model
        .find(query)
        .sort({ price: sortOrder, _id: sortOrder })
        .limit(limit + 1) // fetch extra to check hasNext
        .setOptions({ includeDeleted });

    const hasNextPage = docs.length > limit;
    const results = hasNextPage ? docs.slice(0, limit) : docs;

    const nextCursor = hasNextPage ? { price: results[results.length - 1].price, id: results[results.length - 1]._id } : null;

    return {
      data: results,
      nextCursor,
      hasNextPage
    };
  }

  async softDeleteById(id) {
    return this.model.findOneAndUpdate(
        { _id: id, deletedAt: null },
        { deletedAt: new Date() },
        { returnDocument: "after" }
      );
    }
}

export default new ProductRepository();