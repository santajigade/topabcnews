export const SITE = {
  name: 'Top ABC News',
  tagline: 'The trusted source of recent news and updates',
  url: 'https://topabcnews.com',
  email: 'contact@topabcnews.com',
  // Paste your AdSense publisher id (ca-pub-XXXX) to enable ads site wide
  adsenseClient: '',
  // Paste your GA4 Measurement ID (G-XXXXXXXXXX) to enable Google Analytics site wide
  ga4Id: 'G-BNW7V5L0GZ',
};

// Official social profiles (footer icons and schema sameAs)
export const SOCIAL = [
  { name: 'Facebook', url: 'https://www.facebook.com/838269312701045' },
  { name: 'Instagram', url: 'https://www.instagram.com/topabcnews/' },
  { name: 'LinkedIn', url: 'https://www.linkedin.com/company/108845031/' },
] as const;

export const CATEGORIES = [
  { name: 'World', slug: 'world', color: '#0f766e' },
  { name: 'Technology', slug: 'technology', color: '#7c3aed' },
  { name: 'Finance', slug: 'finance', color: '#0891b2' },
  { name: 'Sports', slug: 'sports', color: '#dc2626' },
  { name: 'Health', slug: 'health', color: '#16a34a' },
  { name: 'Science', slug: 'science', color: '#4f46e5' },
  { name: 'Entertainment', slug: 'entertainment', color: '#c026d3' },
  { name: 'Bollywood', slug: 'bollywood', color: '#db2777' },
  { name: 'Education', slug: 'education', color: '#ea580c' },
  { name: 'Automobile', slug: 'automobile', color: '#475569' },
  { name: 'Yojana', slug: 'yojana', color: '#2563eb' },
] as const;

// Header menu. A group with `slug` links to that category; `children` open as a dropdown.
export const NAV: { label: string; slug?: string; children?: string[] }[] = [
  { label: 'World', slug: 'world' },
  { label: 'Technology', slug: 'technology' },
  { label: 'Finance', slug: 'finance' },
  { label: 'Sports', slug: 'sports' },
  { label: 'Health', slug: 'health', children: ['science'] },
  { label: 'Entertainment', slug: 'entertainment', children: ['bollywood'] },
  { label: 'India', children: ['yojana', 'education', 'automobile'] },
];

export const CATEGORY_NAMES = CATEGORIES.map((c) => c.name) as unknown as [string, ...string[]];
export const catBySlug = (s: string) => CATEGORIES.find((c) => c.slug === s);
export const catByName = (n: string) => CATEGORIES.find((c) => c.name === n)!;
export const PER_PAGE = 12;

export const fmtDate = (d: Date) =>
  d.toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Asia/Kolkata' });
