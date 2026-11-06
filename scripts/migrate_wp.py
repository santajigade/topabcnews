"""One-time migration: WordPress WXR export -> Markdown files (HTML body) for Astro.
Usage: python3 scripts/migrate_wp.py export.xml
"""
import sys, re, html, json, os, xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

NS = {'wp': 'http://wordpress.org/export/1.2/',
      'content': 'http://purl.org/rss/1.0/modules/content/',
      'excerpt': 'http://wordpress.org/export/1.2/excerpt/'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP_PAGES = ['about-us', 'contact', 'privacy-policy', 'terms-conditions', 'our-mission',
              'legal-info', 'career', 'faqs', 'dnpa-code-of-ethics', 'advertise-with-us']

def meta(it, key):
    for m in it.findall('wp:postmeta', NS):
        if m.find('wp:meta_key', NS).text == key:
            return m.find('wp:meta_value', NS).text or ''
    return ''

def clean(body):
    body = body or ''
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    body = re.sub(r'\s(data-[\w-]+|class|style|srcset|sizes|decoding|loading|fetchpriority)="[^"]*"', '', body)
    body = body.replace('https://topabcnews.com/wp-content/uploads/', '/wp-content/uploads/')
    body = body.replace('http://topabcnews.com/wp-content/uploads/', '/wp-content/uploads/')
    body = re.sub(r'(<img\b)(?![^>]*\bloading=)', r'\1 loading="lazy"', body)
    # WordPress stores paragraphs without <p> (wpautop). Wrap only runs of inline text.
    BLOCK = r'(p|h\d|ul|ol|li|div|figure|figcaption|table|thead|tbody|tr|td|th|blockquote|iframe|section|hr|pre|form|label)'
    out, buf = [], []
    def flush():
        if buf:
            out.append('<p>' + '<br>\n'.join(buf) + '</p>')
            buf.clear()
    for line in body.split('\n'):
        t = line.strip()
        if not t:
            flush(); continue
        if re.match(r'^</?' + BLOCK + r'\b', t, re.I) or re.search(r'</' + BLOCK + r'>$', t, re.I):
            flush(); out.append(t)
        else:
            buf.append(t)
    flush()
    return '\n'.join(out)

def yq(s):
    return json.dumps(s, ensure_ascii=False)

def text_of(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

def main(path):
    r = ET.parse(path).getroot()
    att = {}
    for it in r.iter('item'):
        if it.find('wp:post_type', NS).text == 'attachment':
            att[it.find('wp:post_id', NS).text] = (it.find('wp:attachment_url', NS).text,
                                                   meta(it, '_wp_attachment_image_alt'))
    images = set()
    for it in r.iter('item'):
        ptype = it.find('wp:post_type', NS).text
        if it.find('wp:status', NS).text != 'publish' or ptype not in ('post', 'page'):
            continue
        link = it.find('link').text
        slug = unquote(urlparse(link).path.strip('/'))
        if ptype == 'page' and slug not in KEEP_PAGES:
            continue
        raw = it.find('content:encoded', NS).text or ''
        images |= set(re.findall(r'https?://topabcnews\.com/wp-content/uploads/[^"\'\s)<>]+?\.(?:jpe?g|png|webp|gif|svg)', raw, re.I))
        body = clean(raw)
        title = html.unescape(it.find('title').text or '')
        fm = ['---', f'title: {yq(title)}', f'slug: {yq(slug)}']
        if ptype == 'post':
            date = it.find('wp:post_date', NS).text.replace(' ', 'T') + '+05:30'
            cat = [c.text for c in it.findall('category') if c.get('domain') == 'category'][0]
            tags = [html.unescape(c.text) for c in it.findall('category') if c.get('domain') == 'post_tag']
            desc = meta(it, 'rank_math_description') or (it.find('excerpt:encoded', NS).text or '') or text_of(raw)[:155]
            kw = meta(it, 'rank_math_focus_keyword')
            fm += [f'description: {yq(text_of(desc))}', f'date: {date}', f'category: {yq(cat)}',
                   f'tags: {json.dumps(tags, ensure_ascii=False)}']
            if kw:
                fm.append(f'keywords: {yq(kw)}')
            tid = meta(it, '_thumbnail_id')
            if tid in att:
                url, alt = att[tid]
                images.add(url)
                fm += [f'image: {yq(url.replace("https://topabcnews.com", ""))}', f'imageAlt: {yq(alt or title)}']
            fm.append('author: "Editorial Staff"')
            dest = 'posts'
        else:
            fm.append(f'description: {yq(text_of(raw)[:155])}')
            dest = 'pages'
        fm.append('---')
        fname = re.sub(r'[^a-z0-9-]+', '-', slug.lower()).strip('-') + '.md'
        with open(os.path.join(ROOT, 'src/content', dest, fname), 'w', encoding='utf-8') as f:
            f.write('\n'.join(fm) + '\n\n' + body + '\n')
    with open(os.path.join(ROOT, 'scripts/wp_images.txt'), 'w') as f:
        f.write('\n'.join(sorted(images)) + '\n')
    print('images', len(images))

main(sys.argv[1])
