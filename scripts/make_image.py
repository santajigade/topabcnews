"""Create a 1200x675 featured image for a post.
Usage: python3 scripts/make_image.py <slug> "<Headline>" <Category>
Writes public/images/posts/<slug>.webp and prints its URL path.
"""
import os, sys, textwrap, re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_B = os.path.join(ROOT, 'scripts/fonts/DejaVuSans-Bold.ttf')
FONT_R = os.path.join(ROOT, 'scripts/fonts/DejaVuSans.ttf')
COLORS = {'Health': '#16a34a', 'Technology': '#7c3aed', 'Finance': '#0891b2', 'Education': '#ea580c',
          'Bollywood': '#db2777', 'Yojana': '#2563eb', 'Sports': '#dc2626', 'Automobile': '#475569'}

def hex2rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make(slug, title, category, out=None):
    W, H = 1200, 675
    base = hex2rgb(COLORS.get(category, '#e10600'))
    dark = tuple(int(c * 0.35) for c in base)
    img = Image.new('RGB', (W, H), dark)
    d = ImageDraw.Draw(img)
    for y in range(H):  # diagonal style gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(dark[i] * (1 - t) + base[i] * t * 0.9) for i in range(3)))
    for i in range(0, W + H, 60):  # subtle stripes
        d.line([(i, 0), (i - H, H)], fill=tuple(min(255, c + 12) for c in dark), width=2)
    # brand bar
    d.rectangle([0, 0, W, 14], fill='#e10600')
    d.rectangle([60, 60, 60 + 200, 60 + 52], fill='#ffd60a')
    d.text((160, 86), 'ABC NEWS', font=ImageFont.truetype(FONT_B, 30), fill='#111', anchor='mm')
    cf = ImageFont.truetype(FONT_B, 26)
    cw = d.textlength(category.upper(), font=cf)
    d.rounded_rectangle([280, 64, 280 + cw + 32, 108], radius=8, fill=base)
    d.text((296, 86), category.upper(), font=cf, fill='#fff', anchor='lm')
    # headline, auto size
    for size in (72, 64, 56, 50, 44):
        f = ImageFont.truetype(FONT_B, size)
        lines = textwrap.wrap(title, width=int(1080 / (size * 0.58)))
        if len(lines) * size * 1.22 <= 400:
            break
    y = 170 + (400 - len(lines) * size * 1.22) / 2
    for ln in lines:
        d.text((60, y), ln, font=f, fill='#fff')
        y += size * 1.22
    d.text((60, H - 50), 'topabcnews.com', font=ImageFont.truetype(FONT_R, 26), fill=(255, 255, 255, 200))
    out = out or os.path.join(ROOT, 'public/images/posts', f'{slug}.webp')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, quality=82)
    return '/' + os.path.relpath(out, os.path.join(ROOT, 'public')).replace(os.sep, '/')

if __name__ == '__main__':
    slug, title, cat = sys.argv[1], sys.argv[2], sys.argv[3]
    if not re.fullmatch(r'[a-z0-9-]+', slug):
        sys.exit('slug must be lowercase letters, digits and hyphens')
    print(make(slug, title, cat))
