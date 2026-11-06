import { allPosts } from '../lib/posts';
export async function GET() {
  const posts = await allPosts();
  return new Response(JSON.stringify(posts.map((p) => ({ t: p.data.title, s: p.data.slug, c: p.data.category, d: p.data.description, i: p.data.image ?? '' }))),
    { headers: { 'Content-Type': 'application/json' } });
}
