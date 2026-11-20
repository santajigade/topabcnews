import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { CATEGORY_NAMES } from './lib/site';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    category: z.enum(CATEGORY_NAMES),
    tags: z.array(z.string()).default([]),
    keywords: z.string().optional(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    author: z.string().default('Editorial Staff'),
    noindex: z.boolean().optional(),
    sources: z.array(z.object({ name: z.string(), url: z.string() })).default([]),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: z.object({ title: z.string(), slug: z.string(), description: z.string() }),
});

export const collections = { posts, pages };
