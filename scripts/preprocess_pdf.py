#!/usr/bin/env python3
"""
PDF Preprocessing Pipeline for SE Requirements Decomposition.

Converts a PDF datasheet/PRD/standard/spec into structured Markdown,
extracting text, tables, and embedded figures for downstream consumption
by requirements-decompose.

Usage:
    python preprocess_pdf.py --input datasheet.pdf --output ./preprocessed/
    python preprocess_pdf.py --input ./docs/inputs/ --output ./preprocessed/ --batch
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("pdf_preprocess")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class TableInfo:
    """Metadata for one extracted table."""
    page: int
    index_on_page: int
    rows: int
    cols: int
    markdown_path: str


@dataclass
class FigureInfo:
    """Metadata for one extracted figure/image."""
    page: int
    index_on_page: int
    image_path: str
    width: int | None = None
    height: int | None = None
    format: str = "png"
    notes: str = ""  # filled by human or VLM later


@dataclass
class PageInfo:
    """Per-page metadata."""
    page_number: int
    has_text: bool = False
    has_tables: bool = False
    has_figures: bool = False
    is_scanned: bool = False
    text_char_count: int = 0
    ocr_used: bool = False


@dataclass
class Manifest:
    """Output manifest describing what was extracted."""
    source: str
    source_pages: int
    extracted_pages: int
    scanned_pages: int
    extraction_time: str = ""
    tables: list[TableInfo] = field(default_factory=list)
    figures: list[FigureInfo] = field(default_factory=list)
    pages: list[PageInfo] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_text_with_pdfplumber(pdf_path: str) -> tuple[str, list[PageInfo]]:
    """Extract text from each page using pdfplumber (layout-aware)."""
    import pdfplumber

    full_text: list[str] = []
    pages: list[PageInfo] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            info = PageInfo(
                page_number=page_num,
                has_text=len(text.strip()) > 0,
                text_char_count=len(text),
            )
            full_text.append(f"## Page {page_num}\n\n{text}\n")
            pages.append(info)

    return "\n".join(full_text), pages


def detect_scanned_pages(pages: list[PageInfo]) -> list[PageInfo]:
    """Flag pages with very little extractable text as likely scanned."""
    for info in pages:
        if info.text_char_count < 100:
            info.is_scanned = True
    return pages


def ocr_scanned_pages(
    pdf_path: str,
    pages: list[PageInfo],
    output_dir: str,
) -> str:
    """OCR scanned pages and return combined text. Falls back gracefully."""
    try:
        import pytesseract  # noqa: F401
        from pdf2image import convert_from_path
    except ImportError:
        logger.warning("pdf2image + pytesseract not installed — skipping OCR")
        return ""

    scanned_indices = [
        i + 1 for i, p in enumerate(pages) if p.is_scanned
    ]
    if not scanned_indices:
        return ""

    logger.info(f"OCR scanning {len(scanned_indices)} page(s): {scanned_indices}")

    try:
        images = convert_from_path(
            pdf_path, dpi=300,
            first_page=scanned_indices[0],
            last_page=scanned_indices[-1],
        )
    except Exception as exc:
        logger.error(f"pdf2image conversion failed: {exc}")
        return ""

    ocr_text: list[str] = []
    for i, img in enumerate(images):
        page_num = scanned_indices[i]
        try:
            text = pytesseract.image_to_string(img, lang="eng")
            ocr_text.append(f"## Page {page_num} (OCR)\n\n{text}\n")
            for p in pages:
                if p.page_number == page_num:
                    p.ocr_used = True
                    p.has_text = True
                    p.text_char_count = len(text)
        except Exception as exc:
            logger.error(f"OCR failed for page {page_num}: {exc}")

    return "\n".join(ocr_text)


# ---------------------------------------------------------------------------
# Table extraction
# ---------------------------------------------------------------------------

def extract_tables(pdf_path: str, tables_dir: str, pages: list[PageInfo]) -> list[TableInfo]:
    """Extract tables using pdfplumber with line-based strategy."""
    import pdfplumber

    table_infos: list[TableInfo] = []
    os.makedirs(tables_dir, exist_ok=True)

    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15,
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables(table_settings)
            if not tables:
                continue

            for j, table in enumerate(tables):
                if not table or len(table) < 2:
                    continue  # skip empty or header-only

                # Quality filters: reject likely false-positives
                cols = _count_columns(table[0])
                if cols < 2:
                    continue  # single-column = not a real table
                if len(table) < 3 and cols <= 2:
                    continue  # too small to be useful (header + 1 row, ≤2 cols)

                md_lines = _table_to_markdown(table)
                filename = f"table-p{page_num:02d}-{j + 1:02d}.md"
                filepath = os.path.join(tables_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"<!-- Source: page {page_num}, table {j + 1} -->\n\n")
                    f.write(md_lines)

                info = TableInfo(
                    page=page_num,
                    index_on_page=j + 1,
                    rows=len(table),
                    cols=len(table[0]) if table[0] else 0,
                    markdown_path=filepath,
                )
                table_infos.append(info)

                # mark page
                for p in pages:
                    if p.page_number == page_num:
                        p.has_tables = True

    logger.info(f"Extracted {len(table_infos)} table(s) → {tables_dir}")
    return table_infos


def _count_columns(row: list[str | None]) -> int:
    """Count non-empty cells in a row (some cells may be None from merged cols)."""
    return sum(1 for cell in row if cell and str(cell).strip())


def _table_to_markdown(table: list[list[str | None]]) -> str:
    """Convert a 2D table list into GitHub-flavored Markdown."""
    if not table:
        return ""

    # clean cells
    cleaned: list[list[str]] = []
    for row in table:
        cleaned.append([(cell or "").replace("|", "\\|").replace("\n", " ") for cell in row])

    header = cleaned[0]
    body = cleaned[1:]

    lines: list[str] = []
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in body:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Figure / image extraction
# ---------------------------------------------------------------------------

def extract_figures(pdf_path: str, figures_dir: str, pages: list[PageInfo]) -> list[FigureInfo]:
    """
    Extract embedded images using PyMuPDF (fitz).
    Also renders each page as a high-res PNG for visual inspection of diagrams.
    """
    figure_infos: list[FigureInfo] = []
    os.makedirs(figures_dir, exist_ok=True)

    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.warning("PyMuPDF not installed — skipping embedded image extraction")
        return figure_infos

    doc = fitz.open(pdf_path)
    extracted_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            if base_image is None:
                continue

            image_bytes = base_image.get("image")
            ext = base_image.get("ext", "png")
            if not image_bytes:
                continue

            # skip tiny images (< 100 bytes = likely decoration)
            if len(image_bytes) < 100:
                continue

            filename = f"fig-p{page_num + 1:02d}-{img_idx + 1:02d}.{ext}"
            filepath = os.path.join(figures_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            extracted_count += 1
            figure_infos.append(FigureInfo(
                page=page_num + 1,
                index_on_page=img_idx + 1,
                image_path=filepath,
                width=base_image.get("width"),
                height=base_image.get("height"),
                format=ext,
                notes=f"Extracted embedded image from page {page_num + 1}. "
                       "If this is a timing diagram, block diagram, or pinout, "
                       "review manually and add key parameters to manifest.json.",
            ))

            for p in pages:
                if p.page_number == page_num + 1:
                    p.has_figures = True

    doc.close()
    logger.info(f"Extracted {extracted_count} embedded image(s) → {figures_dir}")
    return figure_infos


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def build_manifest(
    source: str,
    source_pages: int,
    tables: list[TableInfo],
    figures: list[FigureInfo],
    pages: list[PageInfo],
    issues: list[str] | None = None,
) -> Manifest:
    """Build the extraction manifest."""
    scanned = sum(1 for p in pages if p.is_scanned)
    return Manifest(
        source=os.path.basename(source),
        source_pages=source_pages,
        extracted_pages=sum(1 for p in pages if p.has_text or p.has_tables or p.has_figures),
        scanned_pages=scanned,
        tables=tables,
        figures=figures,
        pages=pages,
        issues=issues or [],
    )


def write_manifest(manifest: Manifest, output_dir: str) -> str:
    """Write manifest.json and return its path."""
    path = os.path.join(output_dir, "manifest.json")

    # Convert dataclass to dict, handling nested dataclasses
    def _convert(obj: Any) -> Any:
        if isinstance(obj, list):
            return [_convert(item) for item in obj]
        if hasattr(obj, "__dataclass_fields__"):
            return {k: _convert(v) for k, v in asdict(obj).items()}
        return obj

    with open(path, "w", encoding="utf-8") as f:
        json.dump(_convert(manifest), f, indent=2, ensure_ascii=False)

    logger.info(f"Manifest → {path}")
    return path


def print_summary(manifest: Manifest) -> None:
    """Print a human-readable summary."""
    print(f"""
═══════════════════════════════════════════
  PDF Preprocessing Complete
═══════════════════════════════════════════
  Source:          {manifest.source}
  Total pages:     {manifest.source_pages}
  Extracted:       {manifest.extracted_pages} pages
  Scanned (OCR):   {manifest.scanned_pages} pages
  Tables found:    {len(manifest.tables)}
  Figures found:   {len(manifest.figures)}
  Issues:          {len(manifest.issues)}
═══════════════════════════════════════════
""")


# ---------------------------------------------------------------------------
# Quality verification
# ---------------------------------------------------------------------------

@dataclass
class QualityReport:
    """Automated quality assessment of PDF extraction."""
    source: str
    overall_score: float  # 0-100
    text_quality_score: float
    table_quality_score: float
    checks: list[dict[str, Any]] = field(default_factory=list)


def verify_extraction_quality(
    pdf_path: str,
    text_path: str,
    tables: list[TableInfo],
    figures: list[FigureInfo],
    pages: list[PageInfo],
    threshold_low_text: int = 50,
) -> QualityReport:
    """
    Assess extraction quality across four dimensions and return a structured report.
    This is NOT ground-truth validation — it's heuristic quality estimation.
    """
    checks: list[dict[str, Any]] = []
    text_score = 100.0
    table_score = 100.0

    # --- Dimension 1: Text coverage (characters per page) ---
    low_text_pages = [p for p in pages if p.has_text and p.text_char_count < threshold_low_text]
    if low_text_pages:
        penalty = len(low_text_pages) * (100.0 / max(len(pages), 1))
        text_score -= min(penalty, 30)
        checks.append({
            "dimension": "text_coverage",
            "status": "warn",
            "detail": f"{len(low_text_pages)} page(s) have very low text density (< {threshold_low_text} chars)",
            "pages": [p.page_number for p in low_text_pages],
            "suggestion": "These pages may be image-heavy or extraction failed. Verify visually.",
        })
    else:
        checks.append({"dimension": "text_coverage", "status": "pass", "detail": "All pages have adequate text density"})

    # --- Dimension 2: Scanned page OCR ---
    scanned = [p for p in pages if p.is_scanned]
    if scanned:
        penalty = len(scanned) * 5.0
        text_score -= min(penalty, 25)
        checks.append({
            "dimension": "ocr_quality",
            "status": "warn",
            "detail": f"{len(scanned)} page(s) required OCR — accuracy depends on image quality",
            "pages": [p.page_number for p in scanned],
            "suggestion": "Spot-check OCR output against original. Chinese text may have higher error rates.",
        })
    else:
        checks.append({"dimension": "ocr_quality", "status": "pass", "detail": "No OCR needed — text was extractable"})

    # --- Dimension 3: Garbled text detection ---
    garbled_count = 0
    garbled_pages: list[int] = []
    try:
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read()
        # Heuristic: consecutive non-printable or replacement chars
        import re
        garbled_pattern = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]{3,}|[�]{2,}')
        for page_num in range(1, len(pages) + 1):
            # Extract text for this page
            page_match = re.search(rf'## Page {page_num}\n\n(.*?)(?=## Page \d|\Z)', text, re.DOTALL)
            if page_match:
                page_text = page_match.group(1)
                if len(page_text.strip()) > 0:
                    garbled_ratio = len(garbled_pattern.findall(page_text)) / max(len(page_text), 1)
                    if garbled_ratio > 0.001:
                        garbled_count += 1
                        garbled_pages.append(page_num)
        if garbled_count > 0:
            penalty = garbled_count * 10.0
            text_score -= min(penalty, 30)
            checks.append({
                "dimension": "text_garbling",
                "status": "warn",
                "detail": f"{garbled_count} page(s) contain garbled/replacement characters",
                "pages": garbled_pages,
                "suggestion": "Font encoding issue — try pdftotext as alternative or use OCR",
            })
        else:
            checks.append({"dimension": "text_garbling", "status": "pass", "detail": "No garbled characters detected"})
    except Exception:
        checks.append({"dimension": "text_garbling", "status": "skip", "detail": "Could not read text file for garbled check"})

    # --- Dimension 4: Table quality ---
    if tables:
        small_tables = [t for t in tables if t.rows <= 2]
        single_col = [t for t in tables if t.cols == 1]
        if small_tables:
            checks.append({
                "dimension": "table_quality",
                "status": "info",
                "detail": f"{len(small_tables)}/{len(tables)} tables have ≤2 rows — may be false positives",
                "table_indices": [f"p{t.page}-{t.index_on_page}" for t in small_tables],
                "suggestion": "Verify these are real tables, not document borders/lines",
            })
        if single_col:
            table_score -= len(single_col) * 5.0
        if not small_tables and not single_col:
            checks.append({"dimension": "table_quality", "status": "pass", "detail": f"All {len(tables)} tables pass basic quality filters"})
    else:
        checks.append({"dimension": "table_quality", "status": "info", "detail": "No tables detected — may be normal for text-heavy documents"})

    # --- Dimension 5: Figure / diagram detection ---
    pages_with_figures = [p for p in pages if p.has_figures]
    if pages_with_figures:
        checks.append({
            "dimension": "figure_extraction",
            "status": "info",
            "detail": f"{len(figures)} figure(s) extracted from {len(pages_with_figures)} page(s)",
            "pages": [p.page_number for p in pages_with_figures],
            "suggestion": "Use Read tool to view each figure. If it's a timing diagram/block diagram/pinout, extract key parameters manually.",
        })
    else:
        # Check for image-heavy pages without extracted figures
        low_text_pages_set = {p.page_number for p in low_text_pages}
        figureless_low_text = low_text_pages_set - {p.page_number for p in pages_with_figures}
        if figureless_low_text:
            checks.append({
                "dimension": "figure_extraction",
                "status": "warn",
                "detail": f"Page(s) {sorted(figureless_low_text)} have low text but no figures extracted — possible missed diagrams",
                "suggestion": "These pages may contain vector graphics not extractable as images. Render to PNG and review manually.",
            })

    # --- Compute overall score ---
    has_warnings = any(c["status"] == "warn" for c in checks)
    overall = (text_score * 0.5 + table_score * 0.3 + (100 if not scanned else 80) * 0.2)
    # Cap at 95 — no automated check is 100% reliable
    overall = min(overall, 95.0) if not has_warnings else min(overall, 85.0)

    return QualityReport(
        source=os.path.basename(pdf_path),
        overall_score=round(overall, 1),
        text_quality_score=round(text_score, 1),
        table_quality_score=round(table_score, 1),
        checks=checks,
    )


def print_quality_report(report: QualityReport) -> None:
    """Print a human-readable quality report."""
    if report.overall_score >= 90:
        icon = "[PASS]"
    elif report.overall_score >= 70:
        icon = "[WARN]"
    else:
        icon = "[FAIL]"

    print(f"""
======================================================================
  PDF Extraction Quality Report
======================================================================
  Source:     {report.source}
  Overall:    {icon} {report.overall_score:.0f}/100
  Text:       {report.text_quality_score:.0f}/100
  Tables:     {report.table_quality_score:.0f}/100
----------------------------------------------------------------------""")
    for check in report.checks:
        s = check["status"]
        icon_c = {"pass": "[OK]  ", "warn": "[WARN]", "info": "[INFO]", "skip": "[SKIP]"}.get(s, "      ")
        print(f"  {icon_c} {check['detail'][:67]}")
    print("======================================================================\n")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_pdf(
    pdf_path: str,
    output_dir: str,
    *,
    ocr_enabled: bool = True,
    extract_images: bool = True,
    verify: bool = False,
) -> Manifest:
    """Run the full preprocessing pipeline on a single PDF."""
    os.makedirs(output_dir, exist_ok=True)
    source_name = Path(pdf_path).stem

    issues: list[str] = []

    # --- Page count ---
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        source_pages = len(reader.pages)
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                issues.append("PDF is encrypted and could not be decrypted.")
    except Exception as exc:
        issues.append(f"Could not read PDF metadata: {exc}")
        source_pages = 0

    # --- Step 1: Text extraction ---
    full_text, pages = extract_text_with_pdfplumber(pdf_path)
    pages = detect_scanned_pages(pages)

    # --- Step 2: OCR fallback for scanned pages ---
    ocr_text = ""
    if ocr_enabled and any(p.is_scanned for p in pages):
        ocr_text = ocr_scanned_pages(pdf_path, pages, output_dir)

    # Write full text
    text_path = os.path.join(output_dir, "full-text.md")
    combined = full_text
    if ocr_text:
        combined += "\n\n" + ocr_text
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- Source: {os.path.basename(pdf_path)} -->\n\n")
        f.write(combined)
    logger.info(f"Full text → {text_path}")

    # --- Step 3: Table extraction ---
    tables_dir = os.path.join(output_dir, "tables")
    tables = extract_tables(pdf_path, tables_dir, pages)

    # --- Step 4: Figure extraction ---
    figures_dir = os.path.join(output_dir, "figures")
    figures: list[FigureInfo] = []
    if extract_images:
        figures = extract_figures(pdf_path, figures_dir, pages)

    # --- Step 5: Build manifest ---
    manifest = build_manifest(pdf_path, source_pages, tables, figures, pages, issues)
    write_manifest(manifest, output_dir)
    print_summary(manifest)

    # --- Step 6: Verify quality (optional) ---
    if verify:
        text_path = os.path.join(output_dir, "full-text.md")
        report = verify_extraction_quality(
            pdf_path, text_path, tables, figures, pages,
        )
        report_path = os.path.join(output_dir, "quality-report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        print_quality_report(report)
        logger.info(f"Quality report → {report_path}")

    return manifest


def process_batch(input_dir: str, output_base: str) -> list[Manifest]:
    """Process all PDFs in a directory."""
    results: list[Manifest] = []
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    logger.info(f"Batch processing {len(pdf_files)} PDF(s) in {input_dir}")

    for pdf_file in pdf_files:
        source_name = pdf_file.stem
        output_dir = os.path.join(output_base, source_name)
        logger.info(f"--- Processing: {pdf_file.name} ---")
        manifest = process_pdf(str(pdf_file), output_dir)
        results.append(manifest)

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PDF Preprocessing for SE Requirements Decomposition",
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to a PDF file or a directory of PDFs (with --batch)",
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Output directory for preprocessed artifacts",
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="Process all PDFs in the input directory",
    )
    parser.add_argument(
        "--no-ocr", action="store_true",
        help="Skip OCR for scanned pages",
    )
    parser.add_argument(
        "--no-images", action="store_true",
        help="Skip embedded image extraction",
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Run quality assessment on extraction results",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.batch:
        if not os.path.isdir(args.input):
            print(f"ERROR: --batch requires a directory, got: {args.input}", file=sys.stderr)
            sys.exit(1)
        process_batch(args.input, args.output)
    else:
        if not os.path.isfile(args.input):
            print(f"ERROR: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        process_pdf(
            args.input,
            args.output,
            ocr_enabled=not args.no_ocr,
            extract_images=not args.no_images,
            verify=args.verify,
        )


if __name__ == "__main__":
    main()
