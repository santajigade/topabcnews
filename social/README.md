# Social posts for Top ABC News

Makes one 1080 x 1350 px post image (with the ABC News logo) and one LinkedIn
caption with a UTM-tracked link for every new article. Nothing here is part
of the website build.

## Files
- `build.py` : renders `social/work/<slug>.json` to `social/out/<date>/<slug>.png` and writes `captions.txt`
- `pick.py` : lists articles from the last 30 hours that are not in `posted.txt`
- `posted.txt` : slugs that already have social posts (one per line)
- `data.example.json` : data format
- `assets/` : logo and fonts (Anton, Inter; SIL Open Font License)
- `work/` and `out/` are scratch folders, never committed

## Data format (`social/work/<slug>.json`)
- `headline` (required): short, punchy, 3 to 9 words, uppercase is automatic. Wrap the key words in `*stars*` to make them red. `|` forces a line break (use it for 3 balanced lines).
- `sub` (required): one sentence, 10 to 20 words, adds the key fact the headline leaves out.
- `kicker` (optional): one word tag before the category, e.g. `Breaking`, `Alert`, `Live`, `Explainer`. Never repeat the category.
- `bigStat` (optional): `{"label", "value", "badge"}` shows one huge number left of the headline (AQI, score, price, rate). Value max 4 characters. Keep the headline to about 4 words when using it.
- `block` (optional, recommended), one of:
  - `{"type": "stats", "items": [{"value", "label"}]}` 2 or 3 numbers. Value max 7 characters, label max 4 words.
  - `{"type": "list", "title", "items": [{"left", "right"}]}` 2 to 5 rows: schedules, fixtures, steps, eligibility. Left max 8 characters, right max 5 words.
  - `{"type": "tips", "items": ["..."]}` 2 or 3 short actions, max 4 words each (health, safety, how to apply).
- `theme` (optional): `dark`, `light` or `alert`. Default by category: Health = alert; World, Education, Yojana, Bollywood, Entertainment = light; the rest = dark.
- `caption` (required): short fallback text, 2 or 3 short sentences, plain and factual, no hype.
- `linkedin` (required): the LinkedIn post. `hook` = one strong opening sentence with the main news (max 25 words); `points` = 3 key facts from the article, one short line each (max 15 words); `close` = one line on what happens next, why it matters or a practical tip. No questions begging for likes, no hype words, no emoji. build.py adds the UTM link and hashtags.
- `hashtags` (required): 3 to 5 relevant hashtags.

## Rules
- Every fact, number and date must come from the article itself. Never invent or round up numbers.
- Absolutely no em dash or en dash characters (hyphens inside words are fine). `build.py` refuses them.
- Neutral wording for politics, crime, conflict and health stories; attribute claims ("police say").
- No photos of people, no logos of other brands.

## Run
```
python3 social/pick.py
# write social/work/<slug>.json for each listed article
python3 social/build.py
```
`build.py` shrinks the headline to fit and fails if text still does not fit. Then look at every PNG with the Read tool and fix anything clipped, badly wrapped or hard to read. Finally append the slugs to `posted.txt`, commit only that file, and push (commits that touch only `social/` do not redeploy the site).
