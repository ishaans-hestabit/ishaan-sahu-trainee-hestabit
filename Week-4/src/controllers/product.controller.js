import ProductService from "../services/product.service.js";

class productController {

  async getProducts(req, res, next) {
    try {
        const { search, minPrice, maxPrice, tags, sort, limit, cursorPrice, cursorId } = req.query;

        const [sortField, sortDir] = (sort || "price:asc").split(":");

        const result = await ProductService.getProducts({ search, minPrice, maxPrice, tags, sortField, sortDir, limit, cursorPrice, cursorId });

        res.status(200).json({
          success: true,
          ...result
        });
      } catch (err) {
        next(err);
      }
  };

  async getProductById(req, res, next) {
    try {
        const product = await ProductService.getProductById(req.params.id);

        res.status(200).json({
          success: true,
          data: product
        });
      } catch (err) {
        next(err);
      }
  };


  async createProduct(req, res, next) {
    try {
        const product = await ProductService.createProduct(req.body);

        res.status(201).json({
          success: true,
          data: product
        });
      } catch (err) {
        next(err);
      }
  };

  async deleteProduct(req, res, next) {
    try {
      const product = await ProductService.deleteProduct(req.params.id);

      res.status(200).json({
          success: true,
          data: product
        });
      } catch (err) {
        next(err);
      }
  };

}

export default new productController();