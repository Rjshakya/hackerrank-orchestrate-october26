"""Real CLI integration: temp src/manifest/out, one PNG. No mocks.

Runs only with RUN_VISION_TESTS=1 and OPENAI_API_KEY set.
Writes to tmp_path only, never to code/normalised_docs/.
"""

from __future__ import annotations

import csv
import os
import shutil
from pathlib import Path

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parents[4]
REAL_PNG: Path = REPO_ROOT / "dataset" / "evidence" / "images" / "account_admin_console_20260926.png"

should_skip: bool = os.getenv("RUN_VISION_TESTS") != "1" or not os.getenv("OPENAI_API_KEY")

pytestmark = pytest.mark.skipif(should_skip, reason="RUN_VISION_TESTS != '1' or OPENAI_API_KEY missing")


def test_cli_real_one_file(tmp_path: Path) -> None:
    import asyncio

    from ..cli import run
    from ..parser import createStructuredOpenAI

    src_dir: Path = tmp_path / "src"
    out_dir: Path = tmp_path / "out"
    src_dir.mkdir()
    shutil.copy(REAL_PNG, src_dir / REAL_PNG.name)

    manifest: Path = tmp_path / "evidence_files.csv"
    with manifest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file_id", "file_path", "origin", "captured_at"])
        writer.writerow(
            [
                "evidence_04",
                "evidence/images/account_admin_console_20260926.png",
                "account_admin_portal",
                "2026-09-26T11:00:00Z",
            ]
        )

    model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    structured = createStructuredOpenAI(model)
    first: list[Path] = asyncio.run(run(src_dir, out_dir, manifest, structured, model, 1))
    assert len(first) == 1
    md: Path = out_dir / "account_admin_console_20260926.md"
    js: Path = out_dir / "account_admin_console_20260926.json"
    assert md.exists() and js.exists()
    text: str = md.read_text(encoding="utf-8")
    assert "file_id: evidence_04" in text
    assert "parser: langchain" in text

    second: list[Path] = asyncio.run(run(src_dir, out_dir, manifest, structured, model, 1))
    assert second == []
