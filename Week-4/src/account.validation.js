import { z } from "zod";

export const registerAccountSchema = z.object({
  body: z.object({
    firstName: z
      .string()
      .trim()
      .min(2, "First name too short")
      .max(50, "First name too long")
      .regex(/^[a-zA-Z]+$/, "Only alphabets allowed"),

    lastName: z
      .string()
      .trim()
      .min(2, "Last name too short")
      .max(50, "Last name too long")
      .regex(/^[a-zA-Z]+$/, "Only alphabets allowed"),

    email: z
      .string()
      .email("Invalid email format")
      .transform((v) => v.toLowerCase().trim()),

    password: z
      .string()
      .min(8, "Password must be at least 8 characters")
      .max(100, "Password too long"),
  }),
});

export const emailParamSchema = z.object({
  params: z.object({
    email: z.string().email("Invalid email format"),
  }),
});

export const updateNameSchema = z.object({
  body: z.object({
    email: z.string().email(),
    firstName: z
      .string()
      .trim()
      .min(2)
      .max(50)
      .regex(/^[a-zA-Z]+$/, "Only alphabets allowed"),
  }),
});