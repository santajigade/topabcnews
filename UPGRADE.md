# Upgrading older posts (daily scheduled run)

Goal: bring every post published before 2026-11-20 up to the writing rules in CLAUDE.md ("Writing a news post", steps 2 to 4b), to fix AdSense "low value content". Work through `UPGRADE_QUEUE.txt` from the top.

## Each run
1. `git pull --rebase origin main` first; the auto writer pushes several times a day.
2. Take the first **10** lines with status `todo` in `UPGRADE_QUEUE.txt`. Never more than 10 per run.
3. For each post, read it fully and decide one of three outcomes:

**A. Upgrade** (the normal case, for any story that is still useful or searchable: schemes, exams, recruitment, tax, prices, launches, technology explainers, evergreen topics, major world events):
- Keep the slug, `date`, category, featured image and the core story. Do not change the URL.
- Research the topic again with WebSearch and WebFetch. Every fact you add must come from a source you opened in this run; add those sources to `sources`. Correct any fact that is now wrong.
- If the situation has moved on (result declared, scheme changed, deadline passed, product launched), add a short `## Update (<DD Month YYYY>)` section near the top with the new facts.
- Apply CLAUDE.md step 4: facts first, an original value section (India impact, step by step how-to, comparison table, or background explainer, with real facts only), the Reader FAQ for Yojana, Education, Finance and Automobile, specific headings, 2 or 3 in-text links to high authority sites, 1 or 2 internal links to related posts that exist, Health/Finance/Yojana advice line.
- Target 750 to 1100 words. Remove filler, repeated points and generic paragraphs rather than padding.
- Humanise: load the `humanize-writing:humanize-writing` skill and follow it on the new text (keep every fact, figure, link, heading, table and FAQ). If it is not available, apply the same rules by hand.
- Improve `title` (55 to 70 chars, specific, no clickbait) and `description` (140 to 160 chars) only if they are weak; never change `slug`.
- Set `updated:` to the current IST time (format `2026-11-20T21:30:00+05:30`).
- Run the CLAUDE.md 4b quality check. Mark the queue line `done <YYYY-MM-DD>`.

**B. Noindex** (only for posts with no lasting value that cannot honestly be upgraded: one day news that is now stale and that nobody searches for, such as a routine match preview, a celebrity rumour, a market close, a short event that is over, or a thin post with no verifiable facts left):
- Add `noindex: true` to the frontmatter (just above `sources:`). Do not delete the file or change anything else. The page stays online for visitors, but leaves Google, both sitemaps and the AdSense review.
- Mark the queue line `noindex <YYYY-MM-DD>`. Use this sparingly; upgrade whenever a real upgrade is possible.

**C. Skip** if the post already meets every rule (mark `skip <YYYY-MM-DD> already ok`).

4. Never use em dash or en dash characters anywhere (`LC_ALL=C.UTF-8 grep -P "[\x{2013}\x{2014}]"` must find nothing in the changed files). Never invent numbers, quotes or angles.
5. `npm ci` (if needed) and `npm run build` must pass. Never push a failing build.
6. Commit the changed posts and `UPGRADE_QUEUE.txt` only, message `upgrade: <N> old posts <YYYY-MM-DD>`, `git pull --rebase origin main`, push to main.
7. When no `todo` lines are left, change nothing and report that the queue is finished.
