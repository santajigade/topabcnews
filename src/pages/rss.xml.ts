import rss from '@astrojs/rss';
import { allPosts } from '../lib/posts';
import { SITE } from '../lib/site';
export async function GET(context) {
  const posts = (await allPosts()).slice(0, 50);
  return rss({
    title: SITE.name, description: SITE.tagline, site: context.site,
    items: posts.map((p) => ({ title: p.data.title, description: p.data.description, pubDate: p.data.date, link: `/${p.data.slug}/`, categories: [p.data.category] })),
  });
}
