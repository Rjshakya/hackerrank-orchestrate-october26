"""Real vision integration: one screenshot -> ImageFacts. No mocks.

Runs only with RUN_VISION_TESTS=1 and OPENAI_API_KEY set.
Not executed by default; full batch is never auto-run.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parents[4]
SRC: Path = REPO_ROOT / "dataset" / "evidence" / "images" / "account_admin_console_20260926.png"

needs_key: str = "RUN_VISION_TESTS != '1' or OPENAI_API_KEY missing"
should_skip: bool = os.getenv("RUN_VISION_TESTS") != "1" or not os.getenv("OPENAI_API_KEY")

pytestmark = pytest.mark.skipif(should_skip, reason=needs_key)


def test_parse_real_screenshot() -> None:
    import asyncio

    from ..parser import createStructuredOpenAI, parseImage
    from ..schema import ImageFacts

    async def _go() -> ImageFacts:
        model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
        structured = createStructuredOpenAI(model)
        return await parseImage(
            SRC, "evidence_04", "account_admin_portal", "2026-09-26T11:00:00Z", structured
        )

    facts: ImageFacts = asyncio.run(_go())
    assert facts.fileId == "evidence_04"
    assert facts.systemId == "account_admin_portal"
    assert isinstance(facts.facts, list)
    assert all(isinstance(item, str) for item in facts.facts)
    assert isinstance(facts.rawText, str) and len(facts.rawText) > 0
