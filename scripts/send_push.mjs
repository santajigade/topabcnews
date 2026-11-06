// Sends ONE daily web push for the best article of the last 24 hours.
// Usage: node scripts/send_push.mjs <subsDir> <vapid.json> <lastSent.json> <expiredOut.txt>
import fs from 'node:fs';
import path from 'node:path';
import webpush from 'web-push';

const [subsDir, vapidFile, lastFile, expiredOut] = process.argv.slice(2);
const SITE = 'https://topabcnews.com';
// Higher = more likely to be chosen for the daily alert
const PRIORITY = { Yojana: 8, Finance: 7, Education: 6, Technology: 5, Sports: 4, Automobile: 3, Health: 2, Bollywood: 1 };

function frontmatter(file) {
  const s = fs.readFileSync(file, 'utf8');
  const m = s.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  const get = (k) => { const r = m[1].match(new RegExp(`^${k}:\\s*(.*)$`, 'm')); return r ? r[1].trim().replace(/^"|"$/g, '') : ''; };
  return { title: get('title'), slug: get('slug'), description: get('description'), date: new Date(get('date')), category: get('category'), image: get('image') };
}

const last = fs.existsSync(lastFile) ? JSON.parse(fs.readFileSync(lastFile, 'utf8')) : {};
const today = new Date(Date.now() + 5.5 * 3600e3).toISOString().slice(0, 10); // IST date
if (last.date === today && !process.env.FORCE) { console.log(`Already sent today (${last.slug}). Max 1 per day.`); process.exit(0); }

const dir = 'src/content/posts';
const posts = fs.readdirSync(dir).filter((f) => f.endsWith('.md')).map((f) => frontmatter(path.join(dir, f))).filter(Boolean);
const cutoff = Date.now() - 24 * 3600e3;
const cands = posts.filter((p) => p.date.valueOf() >= cutoff && p.slug !== last.slug)
  .sort((a, b) => (PRIORITY[b.category] || 0) - (PRIORITY[a.category] || 0) || b.date - a.date);
if (!cands.length) { console.log('No new article in the last 24 hours. Nothing sent.'); process.exit(0); }
const pick = cands[0];

const subs = fs.existsSync(subsDir) ? fs.readdirSync(subsDir).filter((f) => f.endsWith('.json')) : [];
console.log(`Subscribers: ${subs.length}. Article: ${pick.title}`);
if (!subs.length) process.exit(0);

const v = JSON.parse(fs.readFileSync(vapidFile, 'utf8'));
webpush.setVapidDetails('mailto:contact@topabcnews.com', v.publicKey, v.privateKey);
const payload = JSON.stringify({
  title: pick.title,
  body: pick.description.slice(0, 140),
  image: pick.image ? SITE + pick.image : undefined,
  url: `${SITE}/${encodeURI(pick.slug)}/?utm_source=push&utm_medium=web&utm_campaign=daily`,
});

let ok = 0, fail = 0; const expired = [];
const queue = [...subs];
async function worker() {
  while (queue.length) {
    const f = queue.shift();
    try {
      const sub = JSON.parse(fs.readFileSync(path.join(subsDir, f), 'utf8'));
      await webpush.sendNotification(sub, payload, { TTL: 12 * 3600, urgency: 'normal' });
      ok++;
    } catch (e) {
      fail++;
      if (e.statusCode === 404 || e.statusCode === 410) expired.push(f);
    }
  }
}
await Promise.all(Array.from({ length: 50 }, worker));
fs.writeFileSync(expiredOut, expired.join('\n'));
fs.writeFileSync(lastFile, JSON.stringify({ date: today, slug: pick.slug, sent: ok, failed: fail, subscribers: subs.length }));
console.log(`Sent ${ok}, failed ${fail}, expired removed ${expired.length}`);
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,
  `### Daily push\n- Article: ${pick.title}\n- Subscribers: ${subs.length}\n- Delivered: ${ok}\n- Expired removed: ${expired.length}\n`);
