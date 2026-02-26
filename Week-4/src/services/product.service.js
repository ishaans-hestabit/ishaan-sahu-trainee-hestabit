import ProductRepository from "../repositories/product.repository.js";
import AppError from "../utils/AppError.js";

class ProductService {
 
  async getProducts({ search, minPrice, maxPrice, tags, sortField = "price", sortDir = "asc", limit = 10, cursorPrice, cursorId }) {
  limit = Math.min(Number(limit), 100);

  const filter = {};


  if (search) {
    filter.$or = [
      { name: { $regex: search, $options: "i" } },
      { description: { $regex: search, $options: "i" } }
    ];
  }

  if (minPrice || maxPrice) {
    filter.price = {};
    if (minPrice) filter.price.$gte = Number(minPrice);
    if (maxPrice) filter.price.$lte = Number(maxPrice);
  }

  if (tags) {
    filter.tags = { $in: tags.split(",") };
  }

  if (sortField !== "price") {
    throw new AppError("Only price sorting is supported");
  }

  const sortOrder = sortDir === "desc" ? -1 : 1;

  const cursor = cursorPrice && cursorId ? { price: Number(cursorPrice), id: cursorId } : null;

  return await ProductRepository.findWithCursor(filter, {
    limit,
    cursor,
    sortOrder
  });
}

  
  async deleteProduct(productId) {
    const product = await ProductRepository.softDeleteById(productId);

    if (!product) {
      throw new AppError("Product not found or already deleted", 404);
    }

    return product;
  }

  
  async createProduct(data) {
    if (!data.name || !data.price) {
      throw new AppError("Name and price are required", 400);
    }

    return ProductRepository.create(data);
  }

  
  async getProductById(id) {
    const product = await ProductRepository.findById(id);

    if (!product) {
      throw new AppError("Product not found", 404);
    }

    return product;
  }
}

export default new ProductService();