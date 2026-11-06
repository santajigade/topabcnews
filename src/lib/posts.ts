import { getCollection } from 'astro:content';
export async function allPosts() {
  const p = await getCollection('posts');
  return p.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}
export const postUrl = (slug: string) => `/${slug}/`;
