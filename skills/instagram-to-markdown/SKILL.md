---
name: instagram-to-markdown
description: Download Instagram posts and convert them to Markdown. Fetches post metadata, images, and captions via instaloader using a saved session. Optionally extracts text from images using vision AI. Can save the result as an Obsidian note via n8n webhook. Use when user shares an Instagram URL or shortcode and asks to download, convert, save, or extract content from it. Triggers include "download this ig post", "convert instagram post to markdown", "save this instagram post to obsidian", "extract text from instagram images". Do NOT use for YouTube, TikTok, or other platforms.
---

# Instagram to Markdown

## Setup (one-time)

Session file: `/root/.openclaw/workspace/data/instagram_session`
Account: `bearoyofficial`

If session is missing or expired, re-authenticate:
```python
import instaloader
L = instaloader.Instaloader()
L.context._session.cookies.set('sessionid', '<sessionid_cookie>', domain='.instagram.com')
L.context._session.cookies.set('csrftoken', '<csrftoken_cookie>', domain='.instagram.com')
L.context._session.cookies.set('ds_user_id', '<ds_user_id_cookie>', domain='.instagram.com')
L.context.username = 'bearoyofficial'
L.save_session_to_file('/root/.openclaw/workspace/data/instagram_session')
```
Get fresh cookies from George's browser (instagram.com → DevTools → Application → Cookies).

---

## Workflow

### 1. Convert post to Markdown

```bash
python3 <skill_dir>/scripts/ig2md.py "<url_or_shortcode>"
# With local image download:
python3 <skill_dir>/scripts/ig2md.py "<url_or_shortcode>" --embed-local --outdir ./outputs/ig
```

`<skill_dir>` = directory of this SKILL.md (resolve relative to it).

Output: Markdown with YAML frontmatter (title, author, date, source, likes), embedded images, caption with linked hashtags/mentions, like/comment counts.

### 2. Extract text from images (if post contains infographic/text slides)

When the post images contain text (infographics, carousels with slide text, tips), extract via vision:

```bash
python3 <skill_dir>/scripts/ig_vision.py ./outputs/ig/SHORTCODE_*.jpg
```

Or do it inline using the `image` tool on the downloaded files — pass all images in one call, ask to extract all text labeled by image number.

### 3. Save to Obsidian (optional)

Use n8n webhook — see TOOLS.md for auth and endpoint.
```bash
curl -s -X POST "https://www.mypi.one/webhook/d28998fc-d1a7-4672-8500-aff44d4bb5ff" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <n8n_token>" \
  --max-time 180 \
  -d '{"text": "<markdown_content>", "parent": "<folder>"}'
```
Default parent folder: `"Automations"`. Ask George if he wants a different folder.

---

## Decision Guide

| User intent | Action |
|---|---|
| "download" / "convert" | Run ig2md.py, show Markdown |
| "extract text from images" | Run ig_vision.py (or `image` tool) on downloaded images |
| "save to obsidian" | Full flow: download → extract text if needed → post to n8n webhook |
| Post has text slides/infographic | Always extract image text, merge into Markdown body |
| Post is photo-only with caption | ig2md.py output is sufficient |

---

## Notes

- `ig2md.py` handles single posts and carousel/sidecar posts (multiple images).
- Session expires periodically — if `instaloader.LoginRequiredException` appears, ask George for fresh cookies.
- Images saved to `outputs/ig/SHORTCODE_N.jpg`.
- Private posts work as long as `bearoyofficial` follows the account.
