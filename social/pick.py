"""List articles that still need social posts (newest first).

Usage: python3 social/pick.py [hours]   (default 30)
An article qualifies if its date is within the last <hours> hours and its
slug is not in social/posted.txt.
"""
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
hours = float(sys.argv[1]) if len(sys.argv) > 1 else 30
posted = set((ROOT / "social/posted.txt").read_text().split()) if (ROOT / "social/posted.txt").exists() else set()
now = dt.datetime.now(dt.timezone.utc)
rows = []
for p in (ROOT / "src/content/posts").glob("*.md"):
    fm = p.read_text(encoding="utf-8").split("---", 2)[1]
    m = re.search(r"^date:\s*(\S+)", fm, re.M)
    if not m or p.stem in posted:
        continue
    try:
        d = dt.datetime.fromisoformat(m.group(1).strip('"'))
    except ValueError:
        continue
    if d.tzinfo and now - d <= dt.timedelta(hours=hours):
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.M).group(1)
        cat = re.search(r'^category:\s*"?(.*?)"?\s*$', fm, re.M).group(1)
        rows.append((d, p.stem, cat, title))
rows.sort(reverse=True)
print(f"{len(rows)} article(s) need social posts")
for d, slug, cat, title in rows:
    print(f"{slug} | {cat} | {d.isoformat()} | {title}")
