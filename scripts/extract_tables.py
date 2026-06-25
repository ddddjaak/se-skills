#!/usr/bin/env python3
"""
Specialized table extraction from PDFs for SE documents.

Supports multi-strategy extraction:
  1. Lines-based (pdfplumber) — best for bordered tables
  2. Text-alignment-based (pdfplumber) — best for borderless tables
  3. Camelot (optional) — best for complex lattice tables

Usage:
    python extract_tables.py --input datasheet.pdf --output ./tables/
    python extract_tables.py --input datasheet.pdf --pages 3-15 --strategy lines
"""

import argparse
import logging
import os
import sys

logger = logging.getLogger("extract_tables")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _table_to_markdown(table: list[list[str | None]]) -> str:
    """Convert 2D table → GitHub-flavored Markdown."""
    if not table or len(table) < 2:
        return ""

    cleaned = []
    for row in table:
        cleaned.append([
            (cell or "").replace("|", "\\|").replace("\n", " ")
            for cell in row
        ])

    header = cleaned[0]
    body = cleaned[1:]

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def extract_tables_lines(
    pdf_path: str,
    pages: range | None = None,
) -> dict[int, list[list[list[str | None]]]]:
    """
    Extract tables using line-detection strategy.
    Returns {page_num: [table2d, ...]}.
    """
    import pdfplumber

    settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15,
    }

    results: dict[int, list[list[list[str | None]]]] = {}

    with pdfplumber.open(pdf_path) as pdf:
        target_pages = pages or range(1, len(pdf.pages) + 1)
        for page_num in target_pages:
            page = pdf.pages[page_num - 1]
            tables = page.extract_tables(settings)
            if tables:
                results[page_num] = tables
                logger.info(f"Page {page_num}: {len(tables)} table(s) (lines strategy)")

    return results


def extract_tables_text(
    pdf_path: str,
    pages: range | None = None,
) -> dict[int, list[list[list[str | None]]]]:
    """
    Extract tables using text-alignment strategy (for borderless tables).
    """
    import pdfplumber

    settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
        "snap_tolerance": 5,
    }

    results: dict[int, list[list[list[str | None]]]] = {}

    with pdfplumber.open(pdf_path) as pdf:
        target_pages = pages or range(1, len(pdf.pages) + 1)
        for page_num in target_pages:
            page = pdf.pages[page_num - 1]
            tables = page.extract_tables(settings)
            if tables:
                results[page_num] = tables
                logger.info(f"Page {page_num}: {len(table)} table(s) (text strategy)")

    return results


def write_tables(
    tables: dict[int, list[list[list[str | None]]]],
    output_dir: str,
    prefix: str = "table",
) -> list[str]:
    """Write extracted tables as Markdown files. Returns list of file paths."""
    os.makedirs(output_dir, exist_ok=True)
    paths: list[str] = []

    for page_num, page_tables in sorted(tables.items()):
        for j, table in enumerate(page_tables):
            if not table or len(table) < 2:
                continue

            # Quality filters: reject false-positives
            cols = sum(1 for cell in table[0] if cell and str(cell).strip())
            if cols < 2:
                continue  # single-column = noise
            if len(table) < 3 and cols <= 2:
                continue  # too small to be useful

            filename = f"{prefix}-p{page_num:02d}-{j + 1:02d}.md"
            filepath = os.path.join(output_dir, filename)
            md = _table_to_markdown(table)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"<!-- Source page: {page_num}, table: {j + 1} -->\n\n")
                f.write(md)

            paths.append(filepath)
            logger.info(f"  → {filepath}  ({len(table)} rows × {len(table[0]) if table[0] else '?'} cols)")

    return paths


def _parse_page_range(s: str | None, max_pages: int) -> range | None:
    """Parse '3-15' → range(3, 16)."""
    if not s:
        return None
    parts = s.split("-")
    start = int(parts[0])
    end = int(parts[1]) if len(parts) > 1 else max_pages
    return range(max(1, start), min(max_pages, end) + 1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract tables from PDFs for SE requirements decomposition.",
    )
    parser.add_argument("--input", "-i", required=True, help="Path to PDF file")
    parser.add_argument("--output", "-o", required=True, help="Output directory for table Markdown files")
    parser.add_argument("--pages", "-p", help="Page range, e.g. '3-15'")
    parser.add_argument(
        "--strategy", "-s",
        choices=["lines", "text", "both"],
        default="lines",
        help="Table extraction strategy (default: lines)",
    )
    parser.add_argument("--prefix", default="table", help="Filename prefix (default: table)")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.isfile(args.input):
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Determine page count for range parsing
    from pypdf import PdfReader
    reader = PdfReader(args.input)
    max_pages = len(reader.pages)
    page_range = _parse_page_range(args.pages, max_pages)

    all_tables: dict[int, list[list[list[str | None]]]] = {}

    if args.strategy in ("lines", "both"):
        lines_result = extract_tables_lines(args.input, page_range)
        all_tables.update(lines_result)

    if args.strategy in ("text", "both"):
        text_result = extract_tables_text(args.input, page_range)
        # merge: lines strategy is preferred, only add text results for pages
        # that didn't yield any tables with lines strategy
        for pg, tbls in text_result.items():
            if pg not in all_tables:
                all_tables[pg] = tbls

    total_count = sum(len(t) for t in all_tables.values())
    if total_count == 0:
        logger.warning("No tables found with the selected strategy. Try --strategy text or --strategy both.")
        sys.exit(0)

    written = write_tables(all_tables, args.output, args.prefix)
    print(f"\nExtracted {len(written)} table(s) from {len(all_tables)} page(s) → {args.output}")


if __name__ == "__main__":
    main()
