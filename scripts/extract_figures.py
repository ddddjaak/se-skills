#!/usr/bin/env python3
"""
Extract embedded images and render page regions from PDFs for SE documents.

Two modes:
  1. extract  — Pull out embedded images (timing diagrams, block diagrams, pinouts)
  2. render   — Render pages or regions as high-res PNGs (for visual review or VLM analysis)

Usage:
    python extract_figures.py extract --input datasheet.pdf --output ./figures/
    python extract_figures.py render  --input datasheet.pdf --output ./pages/ --dpi 300
    python extract_figures.py render  --input datasheet.pdf --pages 3,7,12 --dpi 200
"""

import argparse
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger("extract_figures")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ---------------------------------------------------------------------------
# Mode: extract — embedded images
# ---------------------------------------------------------------------------

def extract_embedded_images(pdf_path: str, output_dir: str, *, min_bytes: int = 100) -> list[str]:
    """
    Extract all embedded images from a PDF using PyMuPDF.
    Returns list of output file paths.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.error("PyMuPDF (fitz) not installed. Run: pip install PyMuPDF")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths: list[str] = []
    total = 0

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
            if not image_bytes or len(image_bytes) < min_bytes:
                continue

            filename = f"fig-p{page_num + 1:02d}-{img_idx + 1:02d}.{ext}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            w = base_image.get("width", "?")
            h = base_image.get("height", "?")
            logger.info(f"Page {page_num + 1}, image {img_idx + 1}: {w}×{h}px → {filename}")
            paths.append(filepath)
            total += 1

    doc.close()
    logger.info(f"Extracted {total} embedded image(s) → {output_dir}")
    return paths


# ---------------------------------------------------------------------------
# Mode: render — pages to PNG
# ---------------------------------------------------------------------------

def render_pages(
    pdf_path: str,
    output_dir: str,
    *,
    pages: list[int] | None = None,
    dpi: int = 200,
    max_dim: int = 2000,
) -> list[str]:
    """
    Render PDF pages as PNG images.
    Useful for visual review of diagrams, or feeding to a VLM for description.
    """
    try:
        from pdf2image import convert_from_path
    except ImportError:
        logger.error("pdf2image not installed. Run: pip install pdf2image")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    paths: list[str] = []

    kwargs = {"dpi": dpi}
    if pages:
        kwargs["first_page"] = min(pages)
        kwargs["last_page"] = max(pages)

    images = convert_from_path(pdf_path, **kwargs)

    for i, image in enumerate(images):
        page_num = pages[i] if pages else i + 1

        # Downscale if needed
        width, height = image.size
        if width > max_dim or height > max_dim:
            scale = min(max_dim / width, max_dim / height)
            new_w = int(width * scale)
            new_h = int(height * scale)
            image = image.resize((new_w, new_h))

        filename = f"page-{page_num:03d}.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath, "PNG")
        logger.info(f"Page {page_num}: {image.size[0]}×{image.size[1]}px → {filename}")
        paths.append(filepath)

    logger.info(f"Rendered {len(images)} page(s) → {output_dir}")
    return paths


def render_region(
    pdf_path: str,
    output_dir: str,
    page: int,
    bbox: tuple[int, int, int, int],  # (x0, y0, x1, y1) in PDF points
    dpi: int = 300,
) -> str:
    """
    Render a specific region of a page as a high-res PNG.
    Useful for extracting timing diagrams or block diagrams.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.error("PyMuPDF (fitz) not installed.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    page_obj = doc[page - 1]

    # Convert PDF points to pixel matrix at given DPI
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page_obj.get_pixmap(matrix=mat, clip=fitz.Rect(*bbox))
    filename = f"region-p{page:02d}-x{bbox[0]}-y{bbox[1]}.png"
    filepath = os.path.join(output_dir, filename)
    pix.save(filepath)
    logger.info(f"Region {bbox} @ {dpi}dpi → {filename}")
    doc.close()
    return filepath


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract figures and render pages from PDFs for SE documents.",
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # extract
    ext = sub.add_parser("extract", help="Extract embedded images")
    ext.add_argument("--input", "-i", required=True)
    ext.add_argument("--output", "-o", required=True)
    ext.add_argument("--min-bytes", type=int, default=100, help="Skip images smaller than N bytes")

    # render
    rend = sub.add_parser("render", help="Render pages to PNG")
    rend.add_argument("--input", "-i", required=True)
    rend.add_argument("--output", "-o", required=True)
    rend.add_argument("--pages", help="Comma-separated page numbers, e.g. '3,7,12'")
    rend.add_argument("--dpi", type=int, default=200)
    rend.add_argument("--max-dim", type=int, default=2000, help="Max pixel dimension")

    # region
    reg = sub.add_parser("region", help="Render a specific page region")
    reg.add_argument("--input", "-i", required=True)
    reg.add_argument("--output", "-o", required=True)
    reg.add_argument("--page", type=int, required=True)
    reg.add_argument("--bbox", required=True, help="x0,y0,x1,y1 in PDF points")
    reg.add_argument("--dpi", type=int, default=300)

    args = parser.parse_args()

    if args.mode == "extract":
        extract_embedded_images(args.input, args.output, min_bytes=args.min_bytes)

    elif args.mode == "render":
        page_list = None
        if args.pages:
            page_list = [int(p.strip()) for p in args.pages.split(",")]
        render_pages(args.input, args.output, pages=page_list, dpi=args.dpi, max_dim=args.max_dim)

    elif args.mode == "region":
        parts = [int(x.strip()) for x in args.bbox.split(",")]
        if len(parts) != 4:
            print("ERROR: --bbox must be 'x0,y0,x1,y1'", file=sys.stderr)
            sys.exit(1)
        render_region(args.input, args.output, args.page, tuple(parts), dpi=args.dpi)


if __name__ == "__main__":
    main()
