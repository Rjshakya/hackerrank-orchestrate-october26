"""Render a PDF as Markdown with YAML frontmatter for audit use."""

from __future__ import annotations

from pathlib import Path

from .parser import extract_markdown, open_pdf


def build_frontmatter(source_pdf: str, file_id: str, captured_at: str) -> str:
    lines: list[str] = [
        "---",
        f"source_pdf: {source_pdf}",
        f"file_id: {file_id}",
        f"captured_at: {captured_at}",
        "parser: pymupdf",
        "---",
    ]
    return "\n".join(lines)


def render_markdown(body: str, source_pdf: str, file_id: str, captured_at: str) -> str:
    front: str = build_frontmatter(source_pdf, file_id, captured_at)
    clean: str = body.strip() + "\n" if body.strip() else "(empty document)\n"
    return f"{front}\n\n{clean}"


def parse_and_render(src: Path, file_id: str, captured_at: str) -> str:
    """Open src with PyMuPDF, convert to Markdown, prepend frontmatter."""
    with open_pdf(src) as doc:
        body: str = extract_markdown(doc)
    rel: str = src.as_posix()
    return render_markdown(body, rel, file_id, captured_at)
