# Top ABC News (topabcnews.com)

Static Astro news site. Every push to `main` builds and deploys to Hostinger by FTP (`.github/workflows/deploy.yml`). Live about 2 minutes after push.

## Repo layout
- `src/content/posts/*.md` : news articles (one file each, HTML or Markdown body)
- `src/content/pages/*.md` : static pages (about, privacy, contact...)
- `public/images/posts/` : featured images for new posts (made by `scripts/make_image.py`)
- `public/wp-content/uploads/` : images of old migrated WordPress posts
- `src/lib/site.ts` : site name, categories, header menu (`NAV`), AdSense id. A new category also needs a colour in `scripts/make_image.py`.

## Writing a news post (auto publishing run)

0. **Volume: 2 articles per run, never more** (about 8 a day across 4 runs; decided 2026-11-16 to reduce scaled content risk). Publishing 1 strong article, or none, is better than adding a weak one.
1. **Avoid duplicates.** List titles of the last 3 days first (sorted by the `date` field, not file time):
   `grep -H '^date:' src/content/posts/*.md | sort -t: -k3 -r | head -60 | cut -d: -f1 | xargs grep -h '^title:'`
   Never cover a story already covered unless there is a genuinely new development (then write a new angle, do not repeat).
2. **Pick topics** from both Indian and global news trending today. Scan major global news outlets (Reuters, AP, BBC, Al Jazeera, CNN, Bloomberg, The Guardian, CNBC) as well as Indian ones for ideas, and aim for a mix: in each batch, at least 1 and ideally about half of the articles should be global (non-India) stories. Spread across categories:
   World, Technology, Finance, Sports, Health, Science, Entertainment, Bollywood, Education, Automobile, Yojana.
   **Choose stories where we can add something.** Before writing, name the value add in one line: what a reader gets here that a plain rewrite of the source would not give them. Skip stories that hundreds of sites are rewriting the same way (award show recaps, celebrity news, routine market closes) unless there is a real angle. Prefer: stories with a concrete India impact, official notices and schemes explained step by step (eligibility, how to apply, deadlines), exam and result guides, and global stories that need context to understand.
   World = major international news (diplomacy, elections, conflicts, disasters, climate summits) reported factually and neutrally. Science = space, research, climate and environment. Entertainment = global films, music, OTT and celebrities (non-Bollywood). Bollywood = Indian film industry. Yojana = Indian government schemes. Education includes exams, results, recruitment, study abroad and visa rules. Technology, Finance, Sports, Health and Automobile take both Indian and global stories.
3. **Research** with web search. Use at least 2 reliable sources (official sites like pib.gov.in, rbi.org.in, who.int, federalreserve.gov, company press releases, and major Indian or international news outlets). Every number, date, price and name must come from a source you actually read in this run. If you cannot verify a fact, leave it out. Do not rely on Substack, personal blogs, coaching sites or small unknown news blogs; prefer the original official notice or a major outlet.
4. **Write** an original article, 750 to 1100 words, in simple English for Indian and international readers. For global stories, explain why it matters and add an India angle where one genuinely exists (impact on Indian markets, prices, students, travellers), but never invent one.
   - Structure: short intro paragraph answering what/when/why, then 3 to 6 `##` sections, a "Key highlights" bullet list or a table where useful, and a short conclusion.
   - **Original value section (required).** Every article must have at least one `##` section that the sources do not provide in that form, built only from verified facts: for example what it means for Indian readers (prices, students, travellers, investors, job seekers) with real numbers, IST timings, a step by step how-to (apply, check, watch, claim), a comparison table with earlier years or rival options, or a short explainer of background terms. Never invent an angle or a number to fill it; if no genuine value section is possible, pick a different story.
   - Vary the structure between articles. Do not give every post the same section pattern, the same "Key highlights" list or the same closing style.
   - Do not copy sentences from sources. Rewrite fully in your own words. Quotes max 1 per source, under 15 words.
   - Headings must be specific to the story (e.g. "What the RBI Decision Means for Home Loans"). Never use generic AI style headings like Conclusion, Final Takeaway, Final Thoughts, Summary, Key Takeaways, Wrapping Up, The Bottom Line, In Conclusion.
   - Never start the body with an H1 (the title is already the H1). Use `##` and `###` only.
   - Avoid AI cliches such as "in today's fast-paced world", "delve", "game-changer", "it is worth noting", "landscape", "navigate".
   - Never use em dash or en dash characters. Hyphens inside words are fine.
   - No clickbait, no invented quotes, no speculation presented as fact.
   - Health / Finance / Yojana: add one line at the end saying it is general information, not professional advice.
   - Do NOT write a Sources or References section. Keep all sources in the frontmatter `sources` field (hidden on the site, used as a record).
   - Add 2 or 3 external links inside the text to high authority sites only: official government sites (gov.in, nic.in, pib.gov.in, rbi.org.in, sebi.gov.in, and other countries' official .gov sites), official company or international organisation sites (who.int, imf.org, un.org, etc.), and major outlets (The Hindu, Indian Express, Times of India, Hindustan Times, Economic Times, Mint, Reuters, AP, BBC, Al Jazeera, CNN, Bloomberg, The Guardian, CNBC, ESPNcricinfo, ESPN). Put the link naturally on a relevant phrase, never on words like "click here" or "source". Format: `<a href="https://..." target="_blank" rel="noopener">anchor text</a>`. Never link to blogs, aggregators or competitor news blogs.
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
   `date` = current IST time. `category` must be exactly one of the 11 names above. Slug: only a-z, 0-9 and hyphens, max 8 words.
7. **Build check**: `npm ci` (first time) then `npm run build`. Fix any error before committing.
8. **Commit and push** to `main` with message `news: <short title>` (one commit for the whole batch is fine). Pushing publishes.

## Do not
- Do not edit or delete migrated old posts or pages unless asked.
- Do not change workflows, `.htaccess` or design files during a writing run.
- Do not write about topics in a way that targets private individuals, or publish rumours about deaths, crimes or health of named people without official confirmation.
