# Top ABC News (topabcnews.com)

Static Astro news site. Every push to `main` builds and deploys to Hostinger by FTP (`.github/workflows/deploy.yml`). Live about 2 minutes after push.

## Repo layout
- `src/content/posts/*.md` : news articles (one file each, HTML or Markdown body)
- `src/content/pages/*.md` : static pages (about, privacy, contact...)
- `public/images/posts/` : featured images for new posts (made by `scripts/make_image.py`)
- `public/wp-content/uploads/` : images of old migrated WordPress posts
- `src/lib/site.ts` : site name, categories, AdSense id

## Writing a news post (auto publishing run)

1. **Avoid duplicates.** List titles of the last 3 days first:
   `grep -h '^title:' $(ls -t src/content/posts/*.md | head -60)`
   Never cover a story already covered unless there is a genuinely new development (then write a new angle, do not repeat).
2. **Pick topics** that are trending in India today, spread across categories:
   Health, Technology, Finance, Education, Bollywood, Yojana, Sports, Automobile.
   Yojana = Indian government schemes. Education includes exams, results, recruitment.
3. **Research** with web search. Use at least 2 reliable sources (official sites like pib.gov.in, rbi.org.in, company press releases, and major news outlets). Every number, date, price and name must come from a source you actually read in this run. If you cannot verify a fact, leave it out.
4. **Write** an original article, 750 to 1100 words, in simple English for Indian readers.
   - Structure: short intro paragraph answering what/when/why, then 3 to 6 `##` sections, a "Key highlights" bullet list or a table where useful, and a short conclusion.
   - Do not copy sentences from sources. Rewrite fully in your own words. Quotes max 1 per source, under 15 words.
   - Headings must be specific to the story (e.g. "What the RBI Decision Means for Home Loans"). Never use generic AI style headings like Conclusion, Final Takeaway, Final Thoughts, Summary, Key Takeaways, Wrapping Up, The Bottom Line, In Conclusion.
   - Never start the body with an H1 (the title is already the H1). Use `##` and `###` only.
   - Avoid AI cliches such as "in today's fast-paced world", "delve", "game-changer", "it is worth noting", "landscape", "navigate".
   - Never use em dash or en dash characters. Hyphens inside words are fine.
   - No clickbait, no invented quotes, no speculation presented as fact.
   - Health / Finance / Yojana: add one line at the end saying it is general information, not professional advice.
   - Do NOT write a Sources or References section. Keep all sources in the frontmatter `sources` field (hidden on the site, used as a record).
   - Add 2 or 3 external links inside the text to high authority sites only: official government sites (gov.in, nic.in, pib.gov.in, rbi.org.in, sebi.gov.in), official company or organisation sites, and major outlets (The Hindu, Indian Express, Times of India, Hindustan Times, Reuters, BBC, Economic Times, Mint, ESPNcricinfo). Put the link naturally on a relevant phrase, never on words like "click here" or "source". Format: `<a href="https://..." target="_blank" rel="noopener">anchor text</a>`. Never link to blogs, aggregators or competitor news blogs.
   - Tables are fine and display full width.
   - Add 1 or 2 internal links to related older posts on the site when relevant (`/slug/`).
5. **Featured image**: `python3 scripts/make_image.py <slug> "<Title>" <Category>` (prints the image path). Never download photos from news sites.
6. **Save** as `src/content/posts/<slug>.md` with this frontmatter:

```md
---
title: "Headline, 55 to 70 characters, main keyword first"
slug: "lowercase-hyphenated-slug"
description: "Meta description, 140 to 160 characters"
date: 2026-11-06T10:30:00+05:30
category: "Technology"
tags: ["tag one", "tag two"]
keywords: "main keyword, secondary keyword"
image: "/images/posts/lowercase-hyphenated-slug.webp"
imageAlt: "Short description of the image"
author: "Editorial Staff"
sources:
  - name: "Source name"
    url: "https://..."
---
```
   `date` = current IST time. `category` must be exactly one of the 8 names. Slug: only a-z, 0-9 and hyphens, max 8 words.
7. **Build check**: `npm ci` (first time) then `npm run build`. Fix any error before committing.
8. **Commit and push** to `main` with message `news: <short title>` (one commit for the whole batch is fine). Pushing publishes.

## Do not
- Do not edit or delete migrated old posts or pages unless asked.
- Do not change workflows, `.htaccess` or design files during a writing run.
- Do not write about topics in a way that targets private individuals, or publish rumours about deaths, crimes or health of named people without official confirmation.
