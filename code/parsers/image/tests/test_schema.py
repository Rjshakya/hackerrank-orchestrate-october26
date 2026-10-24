"""Unit: ImageFacts camelCase aliases. No LLM, no IO."""

from pydantic import ValidationError

from ..schema import ImageFacts


def test_aliases_and_required() -> None:
    facts = ImageFacts.model_validate(
        {
            "file_id": "evidence_04",
            "system_id": "account_admin_portal",
            "captured_at": "2026-09-26T11:00:00Z",
            "subject_refs": ["user_11"],
            "resource_ids": ["account_5762"],
            "facts": ["email=haruka.s1838@zoho.com"],
            "raw_text": "Haruka Sato user_11",
        }
    )
    assert facts.fileId == "evidence_04"
    assert facts.model_dump(by_alias=True)["file_id"] == "evidence_04"
    try:
        ImageFacts.model_validate(
            {
                "file_id": "evidence_04",
                "system_id": "account_admin_portal",
                "captured_at": "2026-09-26T11:00:00Z",
            }
        )
        raise AssertionError("raw_text is required")
    except ValidationError:
        pass
