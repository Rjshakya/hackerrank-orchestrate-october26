"""Batch CLI: dataset/evidence/documents/*.pdf -> code/normalised_docs/*.md."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .to_markdown import parse_and_render

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
DEFAULT_SRC: Path = REPO_ROOT / "dataset" / "evidence" / "documents"
DEFAULT_OUT: Path = REPO_ROOT / "code" / "normalised_docs"
DEFAULT_MANIFEST: Path = REPO_ROOT / "dataset" / "evidence_files.csv"


def load_manifest(manifest: Path) -> dict[str, tuple[str, str]]:
    """Map manifest relative path -> (file_id, captured_at)."""
    mapping: dict[str, tuple[str, str]] = {}
    with manifest.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            path: str = (row.get("file_path") or row.get("path") or "").strip()
            if not path:
                # fall back to positional: file_id,path,origin,captured_at
                continue
            file_id: str = (row.get("file_id") or "").strip()
            captured: str = (
                row.get("captured_at") or row.get("capture_time") or ""
            ).strip()
            mapping[path] = (file_id, captured)
    if not mapping:
        # positional fallback without header assumptions
        with manifest.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for parts in reader:
                if len(parts) >= 4 and parts[1].startswith("evidence/"):
                    mapping[parts[1].strip()] = (parts[0].strip(), parts[3].strip())
    return mapping


def normalise_one(src: Path, dst: Path, label: str, file_id: str, captured_at: str) -> bool:
    """Render src to dst with repo-relative label. Return True if written."""
    from .parser import extract_markdown, open_pdf
    from .to_markdown import render_markdown

    with open_pdf(src) as doc:
        body: str = extract_markdown(doc)
    content: str = render_markdown(body, label, file_id, captured_at)
    if dst.exists() and dst.read_text(encoding="utf-8") == content:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8", newline="\n")
    return True


def run(
    src_dir: Path = DEFAULT_SRC, out_dir: Path = DEFAULT_OUT, manifest: Path = DEFAULT_MANIFEST
) -> list[Path]:
    mapping: dict[str, tuple[str, str]] = load_manifest(manifest)
    written: list[Path] = []
    for src in sorted(src_dir.glob("*.pdf")):
        rel: str = f"evidence/documents/{src.name}"
        file_id, captured_at = mapping.get(rel, ("unknown", "unknown"))
        dst: Path = out_dir / f"{src.stem}.md"
        try:
            label: str = src.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            label = src.as_posix()
        # dataset/ prefix for audit consistency
        if label.startswith("dataset/"):
            label = label
        else:
            label = f"dataset/evidence/documents/{src.name}"
        if normalise_one(src, dst, label, file_id, captured_at):
            written.append(dst)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalise evidence PDFs to Markdown")
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    written: list[Path] = run(args.src, args.out, args.manifest)
    print(f"wrote {len(written)} files")
    for p in written:
        print(p.as_posix())


if __name__ == "__main__":
    main()
