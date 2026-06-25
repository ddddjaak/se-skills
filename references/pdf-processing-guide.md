# PDF Processing Guide for SE Documents

Techniques for extracting text, tables, and figures from engineering PDFs
(datasheets, PRDs, industry standards, customer specifications).

## Quick Reference: Which Tool for Which Task

| Task | Best Tool | Notes |
|------|-----------|-------|
| Extract all text preserving layout | `pdfplumber` | `page.extract_text()` — layout-aware |
| Extract tables (bordered) | `pdfplumber` | Lines strategy: `vertical_strategy="lines"` |
| Extract tables (borderless) | `pdfplumber` | Text strategy: `vertical_strategy="text"` |
| Extract text by region | `pdfplumber` | `page.within_bbox((x0, top, x1, bottom)).extract_text()` |
| Extract embedded images | `pdfimages` (poppler) or PyMuPDF | `pdfimages -all input.pdf output_prefix` |
| Render page to image (for VLM) | `pdf2image` or `pdftoppm` | 200-300 DPI, max 2000px |
| OCR scanned pages | `pytesseract` + `pdf2image` | Convert to image first |
| Fast CLI text extraction | `pdftotext -layout` | Pages 1-5: `-f 1 -l 5` |
| Extract text with coordinates | `pdftotext -bbox-layout` | Outputs XML with `<word>` elements + coords |
| Get PDF metadata | `pypdf` | `reader.metadata` → title, author, creator |
| Check if encrypted | `pypdf` | `reader.is_encrypted` |
| Repair corrupted PDF | `qpdf` | `qpdf --check` then `qpdf --fix-qdf` |
| Optimize large PDF | `qpdf` | `qpdf --optimize-level=all` |

## Text Extraction Strategy by Document Type

```
PDF Input
    │
    ├── Text-based PDF (normal)
    │   └── pdfplumber.extract_text()        ← Best: preserves columns/layout
    │
    ├── Text-based PDF (simple single-column)
    │   └── pypdf or pdftotext               ← Lighter, faster
    │
    ├── Scanned PDF (image-only, < 100 chars/page)
    │   └── pdf2image → pytesseract OCR       ← Fallback
    │
    └── Mixed (some pages text, some figures)
        └── pdfplumber + per-page decision    ← Check text_char_count
```

## Table Extraction Strategy

### Lines Strategy (default, works for 80% of datasheets)

```python
import pdfplumber

settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3,
    "intersection_tolerance": 15,
}

with pdfplumber.open("datasheet.pdf") as pdf:
    page = pdf.pages[5]
    tables = page.extract_tables(settings)
```

Use this when tables have visible borders or grid lines. This covers most
register maps, pin assignment tables, and electrical spec tables in datasheets.

### Text Strategy (fallback for borderless tables)

```python
settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "snap_tolerance": 5,
}
```

Use when tables are aligned with whitespace only (common in PRDs and
customer specs).

### Visual Debugging

```python
# Save page as image with debug overlay to verify table detection
img = page.to_image(resolution=150)
img.save("debug_page_5.png")
```

## Figure Extraction for SE Documents

### Method 1: Extract embedded images (preferred)

```bash
# Extract all images in original format
pdfimages -all datasheet.pdf figures/img

# List images with metadata (size, format, page)
pdfimages -list datasheet.pdf
```

This extracts the original image files embedded in the PDF — timing diagrams,
block diagrams, pinout drawings, etc. Much better quality than rendering.

### Method 2: Render pages to images (for VLM analysis)

```python
from pdf2image import convert_from_path

# Render specific pages at 300 DPI
images = convert_from_path(
    "datasheet.pdf",
    dpi=300,
    first_page=3,
    last_page=7,
)
for i, img in enumerate(images):
    img.save(f"page_{i+3:03d}.png")
```

Use this when you need to analyze a timing diagram visually — render the page
and use a VLM (vision-language model) to describe what it sees.

### Method 3: Render a region (for specific diagrams)

```python
import fitz  # PyMuPDF

doc = fitz.open("datasheet.pdf")
page = doc[2]  # page 3 (0-indexed)

# Render a 300×200 point region at 300 DPI
zoom = 300 / 72
mat = fitz.Matrix(zoom, zoom)
clip = fitz.Rect(50, 100, 350, 300)  # x0, y0, x1, y1 in PDF points
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save("timing_diagram_detail.png")
```

## Coordinate Systems

Two coordinate systems are relevant when working with PDF extraction:

| System | Origin | Y direction | Unit | Used by |
|--------|--------|-------------|------|---------|
| PDF coordinates | Bottom-left | Y goes up | Points (1/72 inch) | pypdf, PyMuPDF, pdfplumber `page.rects` |
| Image coordinates | Top-left | Y goes down | Pixels | pdf2image, PIL/Pillow |

**Converting image → PDF coordinates:**

```python
pdf_x = image_x * (pdf_width / image_width)
pdf_y = image_height - (image_y * (pdf_height / image_height))
```

## Handling Problem PDFs

### Encrypted PDFs

```python
from pypdf import PdfReader

reader = PdfReader("encrypted.pdf")
if reader.is_encrypted:
    reader.decrypt("password")  # or "" for empty password
```

### Corrupted PDFs

```bash
# Diagnose
qpdf --check corrupted.pdf

# Attempt repair
qpdf --replace-input corrupted.pdf
qpdf --fix-qdf damaged.pdf repaired.pdf
```

### Scanned PDFs (no extractable text)

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path("scanned.pdf", dpi=300)
text = ""
for i, image in enumerate(images):
    text += f"## Page {i + 1} (OCR)\n\n"
    text += pytesseract.image_to_string(image, lang="eng")
    text += "\n\n"
```

## Performance Guidelines

- **Large PDFs (>200 pages)**: Process in chunks of 10–20 pages
- **Text extraction**: `pdftotext -layout` is 5-10× faster than pdfplumber for plain text
- **Image extraction**: `pdfimages` is much faster than rendering with pdf2image
- **Memory**: pdfplumber's `extract_text()` loads one page at a time — safe for large PDFs
- **Avoid**: `pypdf.extract_text()` for structured/columnar text — loses layout

## Integration with requirements-decompose

The preprocess pipeline produces this structure:

```
docs/inputs-preprocessed/<source-name>/
├── full-text.md              → Feed into Step 2 (CLASSIFY)
├── tables/
│   ├── table-p03-01.md       → Register maps, pin tables, spec tables
│   └── table-p07-01.md
├── figures/
│   ├── fig-p04-01.png        → Timing diagrams, block diagrams, pinouts
│   └── fig-p12-01.png        → Use Read tool to view, then describe
└── manifest.json             → Metadata: read this first to know what exists
```

The `manifest.json` `issues` field catches problems early:

```json
{
  "issues": [
    "Page 3: possible timing diagram (figure) — needs human review for t_rise/t_fall values",
    "Page 7 table: merged cells detected, verify column alignment",
    "Page 12: scanned page, OCR quality may be low"
  ]
}
```
