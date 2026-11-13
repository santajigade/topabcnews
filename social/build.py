"""Render 1080x1350 social posts and LinkedIn captions for Top ABC News articles.

Usage:
  python3 social/build.py                 # every social/work/*.json
  python3 social/build.py <slug> [<slug>] # only these

Reads social/work/<slug>.json (format: social/data.example.json) and the
article in src/content/posts/<slug>.md. Writes:
  social/out/<YYYY-MM-DD>/<slug>.png
  social/out/<YYYY-MM-DD>/captions.txt
Exits with an error if any text does not fit or any dash character is found.
"""
import datetime as dt
import html
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOCIAL = ROOT / "social"
ASSETS = SOCIAL / "assets"
WORK = SOCIAL / "work"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
SITE = "https://topabcnews.com"
W, H = 1080, 1350

THEMES = {
    "dark": dict(bg="#0d0d0d", fg="#ffffff", sub="#e8e8e8", muted="#c9c9c9", hi="#ff3b30",
                 card="#1c1c1c", cardfg="#ffffff", line="#e10600", tag="#ffffff", tagfg="#0d0d0d"),
    "light": dict(bg="#f6f3ee", fg="#111111", sub="#333333", muted="#555555", hi="#e10600",
                  card="#111111", cardfg="#ffffff", line="#d8d2c8", tag="#111111", tagfg="#ffffff"),
    "alert": dict(bg="#26262b", fg="#ffffff", sub="#e2e2e6", muted="#cfcfd4", hi="#ff4a3d",
                  card="#34343a", cardfg="#ffffff", line="#ff4a3d", tag="#ffffff", tagfg="#26262b"),
}
CATEGORY_THEME = {"Health": "alert", "World": "light", "Education": "light", "Yojana": "light",
                  "Bollywood": "light", "Entertainment": "light"}
DASHES = re.compile("[\\u2012-\\u2015]")


def esc(s):
    return html.escape(str(s), quote=True)


def headline_html(text):
    """*word* marks the highlighted (red) part; | forces a line break."""
    out = esc(text)
    out = re.sub(r"\*(.+?)\*", r'<span class="hi">\1</span>', out)
    return out.replace("|", "<br>")


def front_matter(slug):
    p = ROOT / "src/content/posts" / f"{slug}.md"
    if not p.exists():
        sys.exit(f"ERROR: no article {p}")
    fm = p.read_text(encoding="utf-8").split("---", 2)[1]
    get = lambda k: (re.search(rf'^{k}:\s*"?(.*?)"?\s*$', fm, re.M) or [None, ""])[1]
    return {"title": get("title"), "category": get("category"), "date": get("date")}


def block_html(b, t):
    if not b:
        return ""
    kind, items = b.get("type"), b.get("items", [])
    if kind == "stats":
        if not 2 <= len(items) <= 3:
            sys.exit("ERROR: stats block needs 2 or 3 items")
        cells = "".join(
            f'<div class="stat"><div class="sv">{esc(i["value"])}</div><div class="sl">{esc(i["label"])}</div></div>'
            for i in items)
        return f'<div class="stats" style="grid-template-columns: repeat({len(items)}, minmax(0, 1fr))">{cells}</div>'
    if kind == "list":
        if not 2 <= len(items) <= 5:
            sys.exit("ERROR: list block needs 2 to 5 items")
        rows = "".join(f'<div class="row"><span class="rl">{esc(i["left"])}</span><span class="rr">{esc(i["right"])}</span></div>'
                       for i in items)
        title = f'<div class="ltitle">{esc(b["title"])}</div>' if b.get("title") else ""
        return f'<div class="list">{title}{rows}</div>'
    if kind == "tips":
        if not 2 <= len(items) <= 3:
            sys.exit("ERROR: tips block needs 2 or 3 items")
        check = ('<svg aria-hidden="true" width="40" height="40" viewBox="0 0 24 24" fill="none" '
                 f'stroke="{t["hi"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
                 '<path d="M4 12l5 5L20 6"></path></svg>')
        cells = "".join(f'<div class="tip">{check}<span>{esc(i)}</span></div>' for i in items)
        return f'<div class="tips" style="grid-template-columns: repeat({len(items)}, minmax(0, 1fr))">{cells}</div>'
    sys.exit(f"ERROR: unknown block type {kind}")


def page_html(d, meta):
    t = THEMES[d.get("theme") or CATEGORY_THEME.get(meta["category"], "dark")]
    a = ASSETS.as_uri()
    big = d.get("bigStat")
    big_html = ""
    if big:
        badge = f'<div class="badge">{esc(big["badge"])}</div>' if big.get("badge") else ""
        big_html = (f'<div class="big"><div class="bl">{esc(big.get("label", ""))}</div>'
                    f'<div class="bv">{esc(big["value"])}</div>{badge}</div>')
    kicker = f'<span class="tag solid">{esc(d["kicker"])}</span>' if d.get("kicker") else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url({a}/fonts/anton.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url({a}/fonts/inter-400.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url({a}/fonts/inter-600.woff2)}}
@font-face{{font-family:Inter;font-weight:800;src:url({a}/fonts/inter-800.woff2)}}
*{{box-sizing:border-box}} body{{margin:0}}
.post{{width:{W}px;height:{H}px;background:{t['bg']};color:{t['fg']};font-family:Inter,sans-serif;display:flex;flex-direction:column;overflow:hidden}}
.bar{{height:14px;background:#e10600;flex:none}}
.head{{display:flex;justify-content:space-between;align-items:center;padding:44px 72px 0;flex:none}}
.head img{{width:200px;height:116px;display:block}}
.tags{{display:flex;gap:10px}}
.tag{{border:2px solid {t['fg']};font-weight:600;font-size:22px;letter-spacing:2px;padding:6px 14px;text-transform:uppercase}}
.tag.solid{{background:{t['tag']};color:{t['tagfg']};border-color:{t['tag']};font-weight:800}}
.main{{flex:1;min-height:0;display:flex;flex-direction:column;padding:64px 72px 44px;gap:28px;overflow:hidden}}
.top{{display:flex;gap:44px;align-items:center}}
.big{{flex:none;display:flex;flex-direction:column;align-items:flex-start}}
.bl{{font-size:24px;font-weight:600;letter-spacing:2px;color:{t['muted']};text-transform:uppercase}}
.bv{{font-family:Anton,sans-serif;font-size:250px;line-height:.95;color:{t['hi']}}}
.badge{{background:{t['hi']};color:#111;font-weight:800;font-size:26px;letter-spacing:2px;padding:6px 14px;text-transform:uppercase}}
.hl{{font-family:Anton,sans-serif;line-height:1.02;text-transform:uppercase;letter-spacing:.5px;overflow-wrap:normal;min-width:0}}
.hi{{color:{t['hi']}}}
.sub{{font-size:42px;font-weight:600;line-height:1.3;color:{t['sub']}}}
.lead{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:32px;min-height:0}}
.blk{{flex:none}}
.stats{{display:grid;gap:24px}}
.stat{{border-top:4px solid #e10600;padding-top:16px;display:flex;flex-direction:column;gap:8px}}
.sv{{font-family:Anton,sans-serif;font-size:76px;line-height:1}}
.sl{{font-size:25px;line-height:1.3;color:{t['muted']}}}
.list{{display:flex;flex-direction:column;gap:14px}}
.ltitle{{font-weight:800;font-size:24px;letter-spacing:2px;color:{t['hi']};text-transform:uppercase}}
.row{{display:flex;gap:24px;align-items:baseline;border-bottom:2px solid {t['line']};padding-bottom:12px}}
.rl{{font-weight:800;font-size:30px;flex:none;min-width:150px}}
.rr{{font-size:30px}}
.tips{{display:grid;gap:20px}}
.tip{{background:{t['card']};color:{t['cardfg']};padding:24px;display:flex;gap:14px;align-items:center;font-size:26px;font-weight:600;line-height:1.3}}
.tip svg{{flex:none}}
.foot{{background:#e10600;color:#fff;padding:28px 72px;display:flex;justify-content:space-between;font-size:30px;font-weight:800;flex:none}}
</style></head><body><div class="post">
<div class="bar"></div>
<div class="head"><img src="{a}/logo.svg" alt="ABC News"><div class="tags">{kicker}<span class="tag">{esc(meta['category'])}</span></div></div>
<div class="main">
<div class="lead"><div class="top">{big_html}<div class="hl" id="hl">{headline_html(d['headline'])}</div></div>
<div class="sub" id="sub">{esc(d['sub'])}</div></div>
<div class="blk">{block_html(d.get('block'), t)}</div>
</div>
<div class="foot"><span>Read the full story</span><span>topabcnews.com</span></div>
</div></body></html>"""


FIT_JS = """(hasBig) => {
  const hl = document.getElementById('hl'), sub = document.getElementById('sub');
  const main = document.querySelector('.main');
  const lead = document.querySelector('.lead');
  const fits = () => hl.scrollWidth <= hl.clientWidth + 1 && main.scrollHeight <= main.clientHeight + 1 && lead.scrollHeight <= lead.clientHeight + 1;
  let s = hasBig ? 124 : 150, ss = 42;
  hl.style.fontSize = s + 'px';
  while (s > 72 && (!fits() || hl.offsetHeight > (hasBig ? 480 : 560))) { s -= 4; hl.style.fontSize = s + 'px'; }
  while (ss > 30 && !fits()) { ss -= 2; sub.style.fontSize = ss + 'px'; }
  const lines = Math.round(hl.offsetHeight / (s * 1.02));
  return { ok: fits(), headline: s, sub: ss, lines };
}"""


def linkedin_text(d):
    li = d.get("linkedin")
    if not li:
        return d["caption"]
    pts = "\n".join(f"\u2022 {x}" for x in li["points"])
    return f"{li['hook']}\n\n{pts}\n\n{li['close']}"


def caption(d, meta, slug):
    link = (f"{SITE}/{slug}/?utm_source=linkedin&utm_medium=social"
            f"&utm_campaign=daily_news&utm_content={slug}")
    fb = link.replace("utm_source=linkedin", "utm_source=facebook")
    tags = " ".join(d.get("hashtags", []))
    return (f"=== {meta['title']}\nImage: {slug}.png\n\nLINKEDIN POST (copy from here):\n"
            f"{linkedin_text(d)}\n\nRead the full story: {link}\n\n{tags}\n\n"
            f"Facebook / Instagram link: {fb}\n")


def main():
    slugs = sys.argv[1:] or sorted(p.stem for p in WORK.glob("*.json"))
    if not slugs:
        sys.exit("ERROR: nothing in social/work/")
    out = SOCIAL / "out" / dt.datetime.now(IST).strftime("%Y-%m-%d")
    out.mkdir(parents=True, exist_ok=True)
    caps, problems = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H})
        for slug in slugs:
            d = json.loads((WORK / f"{slug}.json").read_text(encoding="utf-8"))
            meta = front_matter(slug)
            text = json.dumps(d, ensure_ascii=False)
            li = d.get("linkedin")
            if li and not (li.get("hook") and li.get("close") and 2 <= len(li.get("points", [])) <= 4):
                problems.append(f"{slug}: linkedin needs hook, 2 to 4 points and close")
            if DASHES.search(text):
                problems.append(f"{slug}: em or en dash in data")
            tmp = WORK / f".{slug}.html"
            tmp.write_text(page_html(d, meta), encoding="utf-8")
            page.goto(tmp.as_uri())
            page.evaluate("document.fonts.ready")
            r = page.evaluate(FIT_JS, bool(d.get("bigStat")))
            if not r["ok"]:
                problems.append(f"{slug}: text does not fit, shorten headline, sub or block")
            page.locator(".post").screenshot(path=str(out / f"{slug}.png"))
            tmp.unlink()
            caps.append(caption(d, meta, slug))
            print(f"{slug}: headline {r['headline']}px ({r['lines']} lines), sub {r['sub']}px -> {out / (slug + '.png')}")
        browser.close()
    (out / "captions.txt").write_text("\n".join(caps), encoding="utf-8")
    print(f"captions: {out / 'captions.txt'}")
    if problems:
        print("PROBLEMS:\n" + "\n".join(problems))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
