# Add pdf-to-md skill

- Added `pdf-to-md` skill: converts text-based PDFs into one clean, structured Markdown file (layout-aware extraction, auto-strips page furniture, reflows wrapped paragraphs, maps document structure to headings).
- Added README skills-table row for it.
- Why: repeatable, document-agnostic PDF to Markdown conversion without OCR.
- New dependency: `pypdf` (runtime, ask-first before install; not vendored into the repo).
