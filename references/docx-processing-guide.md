# Word Document Processing Guide for SE Documents

Techniques for extracting structured content from Word documents (.docx/.doc)
commonly used in SE workflows: PRDs, customer specifications, industry standards,
meeting notes, compliance reports.

## Quick Reference

| Task | Best Tool | Notes |
|------|-----------|-------|
| Read .docx paragraphs + tables | `python-docx` | Pure Python, no system deps |
| Convert .docx → Markdown (fast) | `pandoc document.docx -o output.md` | Preserves all formatting |
| Convert .docx → Markdown (with tracked changes) | `pandoc --track-changes=all` | Shows insertions/deletions |
| Convert legacy .doc → .docx | `soffice --headless --convert-to docx file.doc` | Requires LibreOffice |
| Extract embedded images | ZIP extraction (`zipfile` module) | DOCX is a ZIP of XML + media/ |
| Validate .docx structure | `python scripts/office/validate.py` | Checks XML compliance |
| Unpack for raw XML editing | `python scripts/office/unpack.py doc.docx dir/` | Debugging/advanced use |

## Common SE Document Types

### PRD (Product Requirements Document)

```
Typical structure: Executive Summary → Market Requirements → Functional Requirements
→ Performance Requirements → Compliance Requirements → Appendix
```

Key extraction concerns:
- Requirements often embedded in prose paragraphs, not tables
- "Shall" / "Must" / "Should" keywords signal requirement statements
- Cross-references to standards (IEC, ISO, FCC) need to be captured
- Version history table at beginning — skip during extraction

### Customer Specification

```
Typical structure: Scope → Reference Documents → Technical Requirements
→ Electrical Specs → Mechanical Specs → Environmental Specs → Acceptance Criteria
```

Key extraction concerns:
- May reference external documents not included
- Tables for electrical/mechanical parameters
- Acceptance criteria map to test requirements
- May include non-technical commercial terms (warranty, delivery) — flag, don't discard

### Industry Standard (excerpt)

```
Typical structure: Scope → Normative References → Terms → Requirements → Test Methods
```

Key extraction concerns:
- Mandatory vs. informative clauses (shall vs. should)
- May have complex numbering (1.2.3.4) — preserve hierarchy
- Normative references = additional input sources for requirements inventory

## Reading Strategies

### Strategy 1: python-docx (preferred for structured extraction)

```python
from docx import Document

doc = Document("PRD.docx")

# Iterate paragraphs
for para in doc.paragraphs:
    if para.style.name.startswith("Heading"):
        print(f"# {para.text}")  # section heading
    else:
        print(para.text)

# Iterate tables
for table in doc.tables:
    for row in table.rows:
        cells = [cell.text for cell in row.cells]
        print("| " + " | ".join(cells) + " |")
```

### Strategy 2: pandoc (fast for simple conversion)

```bash
# Direct to Markdown
pandoc PRD.docx -o PRD.md

# Include tracked changes as comments
pandoc --track-changes=all PRD.docx -o PRD.md

# Extract to plain text
pandoc PRD.docx -t plain -o PRD.txt
```

### Strategy 3: Raw ZIP/XML (for debugging)

```bash
# Unpack to see internal structure
python scripts/office/unpack.py PRD.docx unpacked/

# Key files:
#   word/document.xml    — body content
#   word/media/          — embedded images
#   word/styles.xml      — style definitions
```

## Handling Edge Cases

### Tracked Changes

```bash
# Option 1: Show all changes inline
pandoc --track-changes=all document.docx -o with-changes.md

# Option 2: Accept all changes first, then extract
python scripts/accept_changes.py input.docx clean.docx
```

### Legacy .doc Files

```bash
# Must convert first
soffice --headless --convert-to docx legacy.doc
# Then process the resulting .docx
```

### Embedded Images

DOCX stores images in `word/media/` inside the ZIP. The `preprocess_docx.py`
script extracts them directly:

```python
import zipfile

with zipfile.ZipFile("document.docx", "r") as z:
    for name in z.namelist():
        if "media" in name and any(name.endswith(ext) for ext in [".png", ".jpg"]):
            z.extract(name, "images/")
```

### Multi-language Documents

python-docx reads text as-is. For CJK (Chinese/Japanese/Korean) content,
ensure the document uses Unicode fonts — extraction is lossless.

### Tables with Merged Cells

python-docx reports merged cells as empty strings in subsequent rows.
Strategy: forward-fill the first occurrence, or flag as merged in manifest.

## Output Structure

```
docs/inputs-preprocessed/<source-name>/
├── full-text.md              ← Structured Markdown (headings + paragraphs + tables)
├── images/                   ← Embedded images extracted from the DOCX
│   ├── image1.png
│   └── image2.jpeg
└── manifest.json             ← Metadata: sections, counts, issues
```

### manifest.json schema

```json
{
  "source": "PRD.docx",
  "total_paragraphs": 245,
  "total_tables": 12,
  "total_images": 5,
  "sections": [
    {
      "level": 1,
      "heading": "Functional Requirements",
      "paragraph_count": 67,
      "table_count": 3,
      "image_count": 1
    }
  ],
  "issues": [
    "Page 8: tracked changes detected — review before finalizing requirements"
  ]
}
```

## Integration with requirements-decompose

After preprocessing, the Markdown file feeds directly into Step 2 (CLASSIFY):

| DOCX Content Pattern | Maps to Requirement Type |
|----------------------|------------------------|
| "The system shall..." paragraph | Functional (REQ-XXX) |
| Electrical spec table (Parameter/Min/Max/Unit) | Performance (REQ-XXX) |
| "Must comply with IEC 61508" | Compliance |
| "Interface shall use SPI at 10MHz" | Interface (IF-XXX) |
| "Operating temperature: -40°C to +85°C" | Constraint (CON-XXX) |
| Section 1.2.3 heading → numbered requirement | Trace to document § reference |
