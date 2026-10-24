"""Async vision parsing with LangChain. No sync LLM calls."""

from __future__ import annotations

import asyncio
import base64
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable

from .prompt import buildPrompt
from .schema import ImageFacts

__all__ = ["encodeImage", "parseImage", "createStructuredOpenAI"]

StructuredVision = Runnable[Any, ImageFacts]


def _read_and_encode(path: Path) -> str:
    """Sync read + base64. Runs in a worker thread via encodeImage."""
    raw: bytes = path.read_bytes()
    return base64.b64encode(raw).decode("ascii")


async def encodeImage(path: Path) -> str:
    """Read PNG bytes and return base64 ascii without blocking the loop."""
    b64: str = await asyncio.to_thread(_read_and_encode, path)
    return b64


def _data_url(b64: str) -> str:
    return f"data:image/png;base64,{b64}"


async def parseImage(
    path: Path,
    fileId: str,
    systemId: str,
    capturedAt: str,
    structured: StructuredVision,
) -> ImageFacts:
    """Send one screenshot to a LangChain structured vision model.

    structured must already be bound via with_structured_output(ImageFacts).
    Manifest identity (fileId/systemId/capturedAt) always wins over model output.
    """
    b64: str = await encodeImage(path)
    prompt_text: str = buildPrompt(systemId, fileId)
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": _data_url(b64)}},
        ]
    )
    result: ImageFacts = await structured.ainvoke([message])
    if isinstance(result, dict):
        result = ImageFacts.model_validate(result)
    grounded: ImageFacts = result.model_copy(
        update={"fileId": fileId, "systemId": systemId, "capturedAt": capturedAt}
    )
    return grounded


def createStructuredOpenAI(model_name: str) -> StructuredVision:
    """Build a real OpenAI vision model bound to ImageFacts. Reads key from env."""
    from langchain_openai import ChatOpenAI

    chat: Any = ChatOpenAI(model=model_name, temperature=0)
    structured: StructuredVision = chat.with_structured_output(ImageFacts)
    return structured
