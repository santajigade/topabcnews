"""Prepare built social posts for auto publishing through Windsor.ai.

Usage:
  python3 social/publish.py                 # every social/work/*.json
  python3 social/publish.py <slug> [<slug>] # only these

Run after build.py. For each slug it:
  1. converts social/out/<date>/<slug>.png to a JPEG at
     public/social/<date>/<slug>.jpg (served at https://topabcnews.com/social/<date>/<slug>.jpg
     once the site deploys; Windsor.ai needs a public image URL)
  2. writes social/out/<date>/publish.json with the image URL and the
     Facebook, LinkedIn and Instagram texts for each post
  3. deletes public/social/<date> folders older than KEEP_DAYS (the platforms
     keep their own copy of the image once posted)
"""
import datetime as dt
import json
import pathlib
import shutil
import sys

from PIL import Image

from build import DASHES, IST, SITE, SOCIAL, WORK, front_matter, linkedin_text

ROOT = SOCIAL.parent
KEEP_DAYS = 3


def link(slug, source):
    return f"{SITE}/{slug}/?utm_source={source}&utm_medium=social&utm_campaign=daily_news"


def main():
    slugs = sys.argv[1:] or sorted(p.stem for p in WORK.glob("*.json"))
    if not slugs:
        sys.exit("ERROR: nothing in social/work/")
    today = dt.datetime.now(IST)
    date = today.strftime("%Y-%m-%d")
    out = SOCIAL / "out" / date
    pub = ROOT / "public" / "social" / date
    pub.mkdir(parents=True, exist_ok=True)
    posts, problems = [], []
    for slug in slugs:
        png = out / f"{slug}.png"
        if not png.exists():
            problems.append(f"{slug}: {png} missing, run build.py first")
            continue
        d = json.loads((WORK / f"{slug}.json").read_text(encoding="utf-8"))
        meta = front_matter(slug)
        jpg = pub / f"{slug}.jpg"
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=88, optimize=True, progressive=True)
        tags = " ".join(d.get("hashtags", []))
        post = {
            "slug": slug,
            "title": meta["title"],
            "image_url": f"{SITE}/social/{date}/{slug}.jpg",
            "facebook": f"{d['caption']}\n\nRead the full story: {link(slug, 'facebook')}\n\n{tags}",
            "linkedin": f"{linkedin_text(d)}\n\nRead the full story: {link(slug, 'linkedin')}\n\n{tags}",
            "instagram": f"{d['caption']}\n\nFull story on topabcnews.com (link in bio)\n\n{tags}",
        }
        if DASHES.search(json.dumps(post, ensure_ascii=False)):
            problems.append(f"{slug}: em or en dash in post text")
        if len(post["linkedin"]) > 3000 or len(post["instagram"]) > 2200:
            problems.append(f"{slug}: post text too long")
        posts.append(post)
        print(f"{slug}: {jpg.relative_to(ROOT)} ({jpg.stat().st_size // 1024} KB)")
    (out / "publish.json").write_text(json.dumps(posts, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"publish data: {out / 'publish.json'}")
    cutoff = (today - dt.timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    for old in (ROOT / "public" / "social").iterdir():
        if old.is_dir() and old.name < cutoff:
            shutil.rmtree(old)
            print(f"removed old {old.relative_to(ROOT)}")
    if problems:
        print("PROBLEMS:\n" + "\n".join(problems))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
