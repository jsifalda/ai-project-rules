---
name: pdf-to-md
description: Convert a text-based PDF into one clean, structured Markdown file. Extracts with layout-aware spacing (fixes the run-together words plain extraction produces), auto-strips repeated page headers, footers and page numbers, reflows wrapped lines into paragraphs, and maps document structure such as parts, sections and lists to Markdown headings. Use when the user wants to turn a PDF (law, statute, report, manual, handbook, contract, book) into Markdown, or says "convert this PDF to md", "pdf to markdown", or "make a markdown version of this document". Probe the PDF first, then map its structure. Do NOT use for scanned or image-only PDFs that have no text layer and need OCR, for filling in PDF forms, or when the user only wants a single table pulled out of a PDF.
---

# PDF to Markdown

Turn a text-based PDF into one clean, navigable `.md` file. The hard part is not extraction, it is undoing what the PDF layout did to the text: run-together words at line wraps, justified-text padding, repeated page furniture, and paragraphs split across visual lines. This skill does that mechanically, then you map the document's own structure onto Markdown.

## Requirements

Python with `pypdf`. Check with `python3 -c "import pypdf"`. If missing, ask the user before installing (`pip install pypdf`). No other dependencies. No OCR.

## Workflow

Always probe before you convert. Structure differs per document, so never guess the markers.

### 1. Probe

```
python3 scripts/pdf_to_md.py INPUT.pdf --probe
```

Reports page count, text-layer health (avg chars per page), the repeated page furniture it will strip, and counts of candidate structural markers. Read it:

- **avg chars/page near zero** -> the PDF is scanned or image-only. Stop. This skill does not do OCR. Tell the user.
- **furniture list** -> confirms the running header/footer it will drop. Per-page-varying furniture (page numbers, URLs ending in `N/M`, date-time stamps) is caught by built-in patterns, so it may not show here yet still gets removed.
- **marker counts** -> tells you the document's hierarchy (for example many `§` and a few `ČÁST`, or `ARTICLE` and `SECTION`). This is what you map to headings.

### 2. Convert

```
python3 scripts/pdf_to_md.py INPUT.pdf -o OUTPUT.md \
  --title "Document title" \
  --heading '^ČÁST \w+::2' \
  --heading '^§ \d+::3'
```

Key flags:

- `--heading 'REGEX::LEVEL'` (repeatable) maps blocks matching the regex to `#`*LEVEL. First match wins.
- `--block-start 'REGEX'` (repeatable) adds a marker that begins a new block, on top of the built-in defaults (`§`, `(N)`, `N.`, `a)`, roman numerals, `ČÁST/HLAVA/Článek/PART/CHAPTER/ARTICLE/SECTION`). Use it when a document has its own divider words.
- `--drop 'REGEX'` (repeatable) strips extra furniture lines the auto-detector missed.
- `--mode plain` is a fallback if `layout` (the default) mangles a particular file. Layout is almost always better because it preserves spacing.
- `--keep-lines` skips reflow when you want one line per physical line.

### 3. Refine the mapping (your judgement, per document)

The core produces clean, reflowed, heading-mapped Markdown. Good documents are done here. Richer documents need a short custom post-pass that only you can size up. Common additions:

- a linked table of contents built from the top-level headings, using GitHub-style anchor slugs (lowercase, drop punctuation, spaces to hyphens, keep the exact heading text so the slug matches)
- a section title merged onto its heading when the line after a bare section number is a short title
- footnote or endnote lists gathered under one heading
- tables that the layout flattened, split back onto one row per line using the row's own repeating marker
- numbered legal points kept literal (escape the dot, `1\.`) so a Markdown renderer does not renumber them

For anything beyond heading mapping, read the relevant pages, write a small Python pass over the core's output (or fork the core), and keep the source text verbatim. Change whitespace, furniture and line-wraps only. Never reword, translate or renumber.

### 4. Verify

- word-joins fixed: pick two words that wrapped in the PDF and grep that the spaced form exists and the joined form does not
- furniture gone: grep the footer URL or page-number pattern returns nothing in the body
- structure sane: heading counts match what probe reported (for example the `§` count)
- boundaries: the file opens with the title and ends with the document's real last content
- render it and eyeball the head, a mid-section, and the tail

## Worked example: Czech Income Tax Act (Zákon 586/1992 Sb.)

A 117-page consolidated statute from zakonyprolidi.cz. Probe showed a text layer, a running-header timestamp, footer URLs ending `N/117`, 206 `§` lines and 7 `ČÁST` parts, no deeper hierarchy.

Mapping used: `ČÁST` -> H2, `§` -> H3. The core stripped furniture and fixed spacing. The custom refine pass on top added: an H1 plus a metadata blockquote parsed from the cover page, a linked TOC of the 7 parts with anchor slugs, section titles merged onto their `§` heading, a `Poznámky pod čarou` footnote section (footnote entries start with `N)` or `Nx)` such as `5b)`), the depreciation-group appendix table split one row per `(N-M)` marker with `ODPISOVÁ SKUPINA` subheadings, and the post-`§ 42` transitional provisions broken on amendment dividers (`Přechodné ustanovení zavedeno...`, `Čl. IV`, `Účinnost`) with numbered points escaped as `1\.` to preserve exact numbering.

Two guards that mattered:

- **Section-marker false positives.** A wrapped body line can start with a `§` reference. Require the section line to be short and be either the number alone or the number followed by a capital, so mid-sentence references stay in the paragraph.
- **Inline enumerations stay whole.** `a) se zvyšuje o 1. částky..., 2. částky...` is one sentence with an inline list. Only break on `N.` when it starts a physical line, never mid-line, or you corrupt the text.

## Gotchas

- **Why words run together.** Plain `extract_text()` drops the space where a line wrapped, giving `rezidentiČeské` instead of `rezidenti České`. Layout mode keeps the space. This is the single biggest reason to prefer layout.
- **Layout padding.** Layout mode pads justified text with runs of spaces and can echo multi-column blocks. The core collapses the padding. Skim the cover page and any multi-column pages in the output.
- **Tables.** No text extractor recovers a real grid from a flattened PDF table reliably. If the data has a regular row marker, split on it into a list. Do not invent columns.
- **One file only.** This skill produces a single `.md`. It does not split per chapter.
