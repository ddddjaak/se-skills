# Presentation Processing Guide for SE Documents

Techniques for extracting content from PowerPoint presentations (.pptx) commonly
used in SE workflows: architecture overviews, design review decks, customer
requirement presentations, milestone reviews.

## Quick Reference

| Task | Best Tool | Notes |
|------|-----------|-------|
| Extract all text to Markdown | `python -m markitdown file.pptx` | Fast, handles text + tables |
| Extract text + tables + notes | `python-pptx` | Programmatic, per-shape control |
| Extract embedded images | ZIP extraction (`zipfile`) | PPTX = ZIP of XML + media/ |
| Convert slides to images | `soffice --headless --convert-to pdf` + `pdftoppm` | Visual review of diagrams |
| Thumbnail grid overview | `python scripts/thumbnail.py` | Quick visual scan of all slides |

## Common SE Presentation Types

### Architecture Overview Deck

```
Typical structure: Title → System Context → Block Diagram → Module Breakdown
→ Interface Summary → Power Tree → Clock Tree → Risk Register → Next Steps
```

Key extraction concerns:
- Block diagrams embedded as images — extract and describe
- Module names and responsibilities in bullet lists
- Interface arrows / data flow in diagrams — not extractable as text
- Risk items in tables at the end

### Design Review Presentation

```
Typical structure: Agenda → Requirements Recap → Design Decisions → Trade-offs
→ Test Results → Open Issues → Sign-off
```

Key extraction concerns:
- Decision records with rationale (why X over Y)
- Performance numbers in charts — extract underlying data from tables
- Action items / open issues in final slides

### Customer Requirements Presentation

```
Typical structure: Use Cases → Feature Requests → Priority Matrix → Timeline
→ Constraints → Q&A
```

Key extraction concerns:
- Feature lists with priority (Must/Should/Nice-to-have)
- Timeline constraints → schedule requirements
- Q&A slides may contain critical clarifications not in the main deck

## Reading Strategies

### Strategy 1: markitdown (preferred)

```bash
# Single file
python -m markitdown presentation.pptx

# Pipe to file
python -m markitdown deck.pptx > deck.md
```

markitdown preserves:
- Slide structure (numbered)
- Text content from all shapes
- Table data as Markdown tables
- Basic formatting (bold, italic)

### Strategy 2: python-pptx (for programmatic access)

```python
from pptx import Presentation

prs = Presentation("deck.pptx")

for i, slide in enumerate(prs.slides, 1):
    print(f"\n## Slide {i}")
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(shape.text)
        if shape.has_table:
            for row in shape.table.rows:
                cells = [cell.text for cell in row.cells]
                print("| " + " | ".join(cells) + " |")

    # Speaker notes (often contain requirements rationale)
    if slide.has_notes_slide:
        notes = slide.notes_slide.notes_text_frame.text
        if notes.strip():
            print(f"> **Notes:** {notes}")
```

### Strategy 3: Visual slide review

```bash
# Convert to PDF then images
soffice --headless --convert-to pdf deck.pptx
pdftoppm -jpeg -r 150 deck.pdf slide

# View specific slides
# slide-01.jpg, slide-02.jpg, ...
```

## Extracting SE Information from Slides

### Speaker Notes → Requirements Rationale

Speaker notes often contain the "why" behind design decisions that isn't on the
slide itself. Always extract them — they are a primary source for derived
requirements.

### Diagrams → Manual Description Required

Architecture diagrams, block diagrams, and flow charts embedded as images cannot
be auto-extracted. After preprocessing:

1. Read extracted images with the Read tool
2. Describe the key elements: modules, interfaces, data direction, constraints
3. Add the description as a supplement to `full-text.md`

### Tables → Direct Mapping

Tables in presentations (comparison matrices, spec tables, risk registers) are
extracted as Markdown tables by both markitdown and python-pptx.

## Output Structure

```
docs/inputs-preprocessed/<source-name>/
├── full-text.md              ← All slide content as Markdown (with notes)
├── images/                   ← Embedded images from the PPTX
│   ├── image1.png
│   └── image2.png
└── manifest.json             ← Per-slide metadata
```

### manifest.json schema

```json
{
  "source": "architecture-review.pptx",
  "total_slides": 24,
  "slides_with_notes": 8,
  "slides_with_tables": 3,
  "total_images": 12,
  "slides": [
    {
      "number": 1,
      "title": "System Architecture Overview",
      "text_length": 350,
      "has_notes": true,
      "has_table": false,
      "has_image": true
    }
  ],
  "issues": []
}
```

## Integration with requirements-decompose

After preprocessing, the Markdown file feeds into Step 2 (CLASSIFY):

| Slide Content Pattern | SE Interpretation |
|----------------------|-------------------|
| Bullet: "Module X is responsible for..." | Functional requirement → REQ-XXX |
| Table: Parameter / Value / Unit | Performance requirement |
| Slide title: "Trade-offs" + pros/cons table | Design decision record |
| Slide title: "Open Issues" + numbered list | Gap log entries |
| Speaker notes with rationale | Derived requirement source |
| Block diagram (image) | Module decomposition → architecture-design input |
