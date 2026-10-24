"""Open PDFs and extract text with PyMuPDF (latest API).

Uses ``import pymupdf`` (not legacy ``fitz``) per
https://pymupdf.readthedocs.io/en/latest/installation.html.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pymupdf


@dataclass(frozen=True)
class PdfPage:
    page_no: int
    text: str


@dataclass(frozen=True)
class PdfDoc:
    source: str
    page_count: int
    pages: list[PdfPage] = field(default_factory=list)


def open_pdf(path: Path) -> pymupdf.Document:
    """Open a PDF file. Caller must close (or use as context manager)."""
    return pymupdf.open(path)


def extract_pages(doc: pymupdf.Document) -> list[PdfPage]:
    """Extract plain text per page in natural reading order."""
    pages: list[PdfPage] = []
    for i, page in enumerate(doc, start=1):
        text: str = page.get_text(sort=True)
        pages.append(PdfPage(page_no=i, text=text))
    return pages


def extract_markdown(doc: pymupdf.Document) -> str:
    """Convert whole document to Markdown via Document.to_markdown()."""
    md: str = doc.to_markdown()
    return md


def parse_pdf(path: Path) -> PdfDoc:
    """Open path, extract pages, and return a typed PdfDoc."""
    with open_pdf(path) as doc:
        pages: list[PdfPage] = extract_pages(doc)
        return PdfDoc(source=str(path), page_count=len(pages), pages=pages)
