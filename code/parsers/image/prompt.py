"""Prompt builder for vision extraction. Pure function, no IO."""

from __future__ import annotations

__all__ = ["buildPrompt"]


def buildPrompt(systemId: str, fileId: str) -> str:
    """Return the user instruction sent alongside the screenshot.

    Strict transcription rules: only visible text, no guessing, grounded ids.
    """
    lines: list[str] = [
        f"You are auditing evidence {fileId} from system {systemId}.",
        "Transcribe ONLY text visibly present in this screenshot.",
        "Do not guess, infer, or complete missing values.",
        "Extract:",
        "1. subjectRefs: stable refs literally visible (user_*, account_*, ORD-*, CS-*, support_*, audit_*, export_*, backup_*)",
        "2. resourceIds: record/console ids literally visible (account_*, ORD-*, support_*, export_*, backup_*, search docs, etc.)",
        "3. facts: short key=value lines, one per visible field (e.g. email=haruka.s1838@zoho.com).",
        "4. rawText: full visible text in reading order.",
        "Rules:",
        "- Empty list / empty string when absent; never null.",
        "- Keep dates, emails, phones, amounts character-exact.",
        "- facts entries feed EvidenceCtx.fromImg, so keep each entry self-contained.",
    ]
    return "\n".join(lines)
