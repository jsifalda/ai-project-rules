#!/usr/bin/env python3
# ig2md.py — convert Instagram post to Markdown using instaloader
# Usage:
#   python3 ig2md.py <post_url_or_shortcode> [--outdir images] [--embed-local]
#   python3 ig2md.py https://www.instagram.com/p/BYtf4B4guNo/
#   python3 ig2md.py BYtf4B4guNo --embed-local --outdir ./outputs/ig

import sys, os, re, argparse, urllib.request, html
import instaloader

SESSION_FILE = '/root/.openclaw/workspace/data/instagram_session'
IG_USER = 'bearoyofficial'

def linkify_hashtags(text):
    return re.sub(r'(?<!\w)#([A-Za-z0-9_]+)', r'[#\1](https://www.instagram.com/explore/tags/\1/)', text)

def linkify_mentions(text):
    return re.sub(r'@([A-Za-z0-9_.]+)', r'[@\1](https://www.instagram.com/\1/)', text)

def download(url, outdir, filename):
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, filename)
    try:
        urllib.request.urlretrieve(url, out)
        return out
    except Exception:
        return url

def extract_shortcode(input_str):
    m = re.search(r'instagram\.com/p/([A-Za-z0-9_-]+)', input_str)
    if m:
        return m.group(1)
    return input_str.strip('/')

def main():
    p = argparse.ArgumentParser(description='Convert Instagram post to Markdown')
    p.add_argument('post', help='Post URL or shortcode')
    p.add_argument('--outdir', default='./outputs/ig', help='Directory to save images')
    p.add_argument('--embed-local', action='store_true', help='Download media and embed local paths')
    args = p.parse_args()

    shortcode = extract_shortcode(args.post)

    L = instaloader.Instaloader()
    L.load_session_from_file(IG_USER, SESSION_FILE)

    post = instaloader.Post.from_shortcode(L.context, shortcode)

    caption = post.caption or ''
    caption = html.unescape(caption)
    caption_md = linkify_mentions(linkify_hashtags(caption))

    author = post.owner_username
    date_iso = post.date_utc.strftime('%Y-%m-%d')
    source = f'https://www.instagram.com/p/{shortcode}/'

    # Collect media URLs
    media_items = []
    if post.typename == 'GraphSidecar':
        for i, node in enumerate(post.get_sidecar_nodes()):
            media_items.append({'url': node.display_url, 'idx': i+1, 'is_video': node.is_video})
    else:
        media_items.append({'url': post.url, 'idx': 1, 'is_video': post.is_video})

    title = caption.splitlines()[0].strip()[:80] if caption else f'Instagram post by {author}'

    md = []
    md.append('---')
    md.append(f'title: "{title.replace(chr(34), chr(92)+chr(34))}"')
    md.append(f'author: "{author}"')
    md.append(f'date: {date_iso}')
    md.append(f'source: "{source}"')
    md.append(f'likes: {post.likes}')
    md.append('---\n')

    for item in media_items:
        if args.embed_local:
            ext = 'mp4' if item['is_video'] else 'jpg'
            fname = f'{shortcode}_{item["idx"]}.{ext}'
            local = download(item['url'], args.outdir, fname)
            md.append(f'![{author}]({local})\n')
        else:
            md.append(f'![{author}]({item["url"]})\n')

    if caption_md:
        md.append(caption_md + '\n')

    md.append(f'---')
    md.append(f'❤️ {post.likes} likes · 💬 {post.comments} comments')

    print('\n'.join(md))

if __name__ == '__main__':
    main()
