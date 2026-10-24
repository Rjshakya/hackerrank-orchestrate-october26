"""Async batch CLI: dataset/evidence/images/*.png -> normalised .md + .json."""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
from pathlib import Path
from typing import Any

from .parser import StructuredVision, createStructuredOpenAI, parseImage
from .schema import ImageFacts

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
DEFAULT_SRC: Path = REPO_ROOT / "dataset" / "evidence" / "images"
DEFAULT_OUT: Path = REPO_ROOT / "code" / "normalised_docs" / "images"
DEFAULT_MANIFEST: Path = REPO_ROOT / "dataset" / "evidence_files.csv"

__all__ = [
    "load_manifest",
    "build_frontmatter",
    "render_markdown",
    "normalise_one",
    "run",
    "main",
]


def load_manifest(manifest: Path) -> dict[str, tuple[str, str, str]]:
    """Map manifest file_path -> (file_id, origin, captured_at)."""
    mapping: dict[str, tuple[str, str, str]] = {}
    with manifest.open("r", encoding="utf-8", newline="") as f:
        reader: Any = csv.DictReader(f)
        for row in reader:
            file_id: str = str(row.get("file_id") or "").strip()
            rel: str = str(row.get("file_path") or "").strip()
            origin: str = str(row.get("origin") or "").strip()
            captured: str = str(row.get("captured_at") or "").strip()
            if file_id and rel:
                mapping[rel] = (file_id, origin, captured)
    return mapping


def build_frontmatter(
    source_png: str, file_id: str, system_id: str, captured_at: str, model: str
) -> str:
    lines: list[str] = [
        "---",
        f"source_png: {source_png}",
        f"file_id: {file_id}",
        f"system_id: {system_id}",
        f"captured_at: {captured_at}",
        "parser: langchain",
        f"model: {model}",
        "---",
    ]
    return "\n".join(lines)


def render_markdown(facts: ImageFacts, source_png: str, model: str) -> str:
    front: str = build_frontmatter(
        source_png, facts.fileId, facts.systemId, facts.capturedAt, model
    )
    fact_lines: list[str] = [f"- {item}" for item in facts.facts]
    refs: str = ", ".join(facts.subjectRefs)
    resources: str = ", ".join(facts.resourceIds)
    body: str = "\n".join(
        [
            f"# {facts.fileId}",
            "",
            f"subjectRefs: {refs}" if refs else "subjectRefs: (none)",
            f"resourceIds: {resources}" if resources else "resourceIds: (none)",
            "",
            "## facts",
            *fact_lines,
            "",
            "## raw_text",
            "",
            "```",
            facts.rawText.strip(),
            "```",
            "",
        ]
    )
    return f"{front}\n\n{body}"


def render_json(facts: ImageFacts) -> str:
    payload: dict[str, Any] = facts.model_dump(by_alias=True, mode="json")
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


async def normalise_one(
    src: Path,
    dst_md: Path,
    dst_json: Path,
    label: str,
    file_id: str,
    system_id: str,
    captured_at: str,
    structured: StructuredVision,
    model: str,
) -> bool:
    """Parse one PNG and write .md + .json. Return True when files changed."""
    facts: ImageFacts = await parseImage(
        src, file_id, system_id, captured_at, structured
    )
    md_content: str = render_markdown(facts, label, model)
    json_content: str = render_json(facts)
    unchanged_md: bool = (
        dst_md.exists() and dst_md.read_text(encoding="utf-8") == md_content
    )
    unchanged_json: bool = (
        dst_json.exists() and dst_json.read_text(encoding="utf-8") == json_content
    )
    if unchanged_md and unchanged_json:
        return False
    dst_md.parent.mkdir(parents=True, exist_ok=True)
    dst_md.write_text(md_content, encoding="utf-8", newline="\n")
    dst_json.write_text(json_content, encoding="utf-8", newline="\n")
    return True


async def run(
    src_dir: Path = DEFAULT_SRC,
    out_dir: Path = DEFAULT_OUT,
    manifest: Path = DEFAULT_MANIFEST,
    structured: StructuredVision | None = None,
    model: str = "gpt-4o-mini",
    concurrency: int = 4,
) -> list[Path]:
    """Normalise every PNG in src_dir. Caller supplies a real bound vision model."""
    if structured is None:
        raise ValueError(
            "structured vision model is required (no default construction)"
        )
    mapping: dict[str, tuple[str, str, str]] = load_manifest(manifest)
    sem = asyncio.Semaphore(concurrency)
    written: list[Path] = []

    async def _one(src: Path) -> Path | None:
        rel: str = f"evidence/images/{src.name}"
        file_id, system_id, captured_at = mapping.get(
            rel, ("unknown", "unknown", "unknown")
        )
        dst_md: Path = out_dir / f"{src.stem}.md"
        dst_json: Path = out_dir / f"{src.stem}.json"
        try:
            label: str = src.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            label = src.as_posix()
        if not label.startswith("dataset/"):
            label = f"dataset/evidence/images/{src.name}"
        async with sem:
            changed: bool = await normalise_one(
                src,
                dst_md,
                dst_json,
                label,
                file_id,
                system_id,
                captured_at,
                structured,
                model,
            )
        return dst_md if changed else None

    results: list[Path | None] = await asyncio.gather(
        *[_one(src) for src in sorted(src_dir.glob("*.png"))]
    )
    for item in results:
        if item is not None:
            written.append(item)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalise evidence screenshots (async)"
    )
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--model", type=str, default=os.getenv("LLM_MODEL", "gpt-4o-mini")
    )
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()
    structured: StructuredVision = createStructuredOpenAI(args.model)
    written: list[Path] = asyncio.run(
        run(
            args.src,
            args.out,
            args.manifest,
            structured,
            args.model,
            args.concurrency,
        )
    )
    print(f"wrote {len(written)} files")
    for p in written:
        print(p.as_posix())


if __name__ == "__main__":
    main()
