export const SITE = {
  name: 'Top ABC News',
  tagline: 'The trusted source of recent news and updates',
  url: 'https://topabcnews.com',
  email: 'contact@topabcnews.com',
  // Paste your AdSense publisher id (ca-pub-XXXX) to enable ads site wide
  adsenseClient: '',
};

export const CATEGORIES = [
  { name: 'Health', slug: 'health', color: '#16a34a' },
  { name: 'Technology', slug: 'technology', color: '#7c3aed' },
  { name: 'Finance', slug: 'finance', color: '#0891b2' },
  { name: 'Education', slug: 'education', color: '#ea580c' },
  { name: 'Bollywood', slug: 'bollywood', color: '#db2777' },
  { name: 'Yojana', slug: 'yojana', color: '#2563eb' },
  { name: 'Sports', slug: 'sports', color: '#dc2626' },
  { name: 'Automobile', slug: 'automobile', color: '#475569' },
] as const;

export const CATEGORY_NAMES = CATEGORIES.map((c) => c.name) as unknown as [string, ...string[]];
export const catBySlug = (s: string) => CATEGORIES.find((c) => c.slug === s);
export const catByName = (n: string) => CATEGORIES.find((c) => c.name === n)!;
export const PER_PAGE = 12;

export const fmtDate = (d: Date) =>
  d.toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Asia/Kolkata' });
