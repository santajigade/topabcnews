import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import path from 'node:path';

// Read each post's date/updated so the sitemap can tell Google when a page changed
const lastmod = {};
const postsDir = './src/content/posts';
for (const f of fs.readdirSync(postsDir).filter((f) => f.endsWith('.md'))) {
  const head = fs.readFileSync(path.join(postsDir, f), 'utf8').split('\n---')[0];
  const slug = head.match(/^slug:\s*"?([^"\n]+)"?/m)?.[1];
  const date = head.match(/^updated:\s*(\S+)/m)?.[1] ?? head.match(/^date:\s*(\S+)/m)?.[1];
  if (slug && date && !isNaN(Date.parse(date))) lastmod[`https://topabcnews.com/${slug}/`] = new Date(date).toISOString();
}
const newest = Object.values(lastmod).sort().pop();

export default defineConfig({
  site: 'https://topabcnews.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap({
    // keep noindex pages (search, 404, pagination) out of the sitemap
    filter: (p) => !p.includes('/search/') && !p.includes('/404') && !/\/page\/\d+\/$/.test(p) && !/\/category\/[^/]+\/\d+\/$/.test(p),
    serialize(item) {
      if (lastmod[item.url]) item.lastmod = lastmod[item.url];
      else if (item.url === 'https://topabcnews.com/' || item.url.includes('/category/')) item.lastmod = newest;
      return item;
    },
  })],
});
