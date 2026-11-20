import { allPosts } from '../lib/posts';
import { SITE } from '../lib/site';
const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[c]!);
export async function GET() {
  // Google News sitemap: articles from the last 2 days (falls back to latest 10)
  const posts = (await allPosts()).filter((p) => !p.data.noindex);
  const cutoff = Date.now() - 2 * 864e5;
  let recent = posts.filter((p) => p.data.date.valueOf() >= cutoff);
  if (!recent.length) recent = posts.slice(0, 10);
  const body = recent.slice(0, 1000).map((p) => `<url><loc>${SITE.url}/${encodeURI(p.data.slug)}/</loc><news:news><news:publication><news:name>${SITE.name}</news:name><news:language>en</news:language></news:publication><news:publication_date>${p.data.date.toISOString()}</news:publication_date><news:title>${esc(p.data.title)}</news:title></news:news></url>`).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">${body}</urlset>`, { headers: { 'Content-Type': 'application/xml' } });
}
