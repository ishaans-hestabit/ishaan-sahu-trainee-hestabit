import { z } from "zod";

export const createProductSchema = z.object({
  body: z.object({
    name: z
      .string()
      .trim()
      .min(3, "Product name too short")
      .max(100, "Product name too long"),

    price: z
      .number()
      .positive("Price must be greater than 0")
      .max(1_000_000, "Price exceeds limit"),

    description: z
      .string()
      .max(1000, "Description too long")
      .optional(),

    tags: z
      .array(
        z.string().trim().min(1, "Tag cannot be empty").max(20)
      )
      .max(10, "Maximum 10 tags allowed")
      .optional(),
  }),
});

export const productQuerySchema = z.object({
  query: z.object({
    search: z.string().optional(),

    minPrice: z.coerce
      .number()
      .positive("minPrice must be positive")
      .optional(),

    maxPrice: z.coerce
      .number()
      .positive("maxPrice must be positive")
      .optional(),

    tags: z.string().optional(), 

    sort: z
      .string()
      .regex(/^price:(asc|desc)$/, "Invalid sort format")
      .optional(),

    limit: z.coerce
      .number()
      .int()
      .min(1, "Limit must be at least 1")
      .max(100, "Limit cannot exceed 100")
      .optional(),

    cursorPrice: z.coerce
      .number()
      .positive()
      .optional(),

    cursorId: z.string().optional(),
  }),
});

export const productIdParamSchema = z.object({
  params: z.object({
    id: z
      .string()
      .regex(/^[0-9a-fA-F]{24}$/, "Invalid product ID"),
  }),
});