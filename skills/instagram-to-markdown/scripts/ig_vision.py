#!/usr/bin/env python3
# ig_vision.py — extract text from downloaded Instagram images using OpenAI vision API
# Usage:
#   python3 ig_vision.py /path/to/outputs/ig/SHORTCODE_*.jpg
#   python3 ig_vision.py SHORTCODE_1.jpg SHORTCODE_2.jpg ...
# Output: prints extracted text per image to stdout, labeled Image 1, Image 2, etc.
# Requires: OPENAI_API_KEY in env

import sys, os, base64, json
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
    sys.exit(1)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_text_from_images(image_paths):
    client = OpenAI()
    results = []

    for i, path in enumerate(image_paths, 1):
        if not os.path.exists(path):
            print(f"WARNING: File not found: {path}", file=sys.stderr)
            continue

        ext = Path(path).suffix.lower().lstrip('.')
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        b64 = encode_image(path)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract ALL text from this image exactly as written. Include every word, number, heading, bullet point, and label visible. If there is no text, say '(no text)'."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"}
                    }
                ]
            }],
            max_tokens=1000
        )

        text = response.choices[0].message.content.strip()
        results.append((i, path, text))
        print(f"Image {i}: {Path(path).name}\n{text}\n", flush=True)

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ig_vision.py <image1> [image2] ...", file=sys.stderr)
        sys.exit(1)

    extract_text_from_images(sys.argv[1:])
