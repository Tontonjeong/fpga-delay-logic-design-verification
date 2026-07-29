#!/usr/bin/env python3
"""Create a public, path-sanitized manifest from the safe-extraction audit."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path, PurePosixPath


PUBLIC_USED = {
    ".sv",
    ".v",
    ".vhd",
    ".vhdl",
    ".tcl",
    ".do",
    ".bat",
    ".ps1",
    ".py",
    ".qpf",
    ".qsf",
    ".sdc",
    ".txt",
    ".csv",
    ".md",
}
PUBLIC_REFERENCE_ONLY = {".pdf", ".docx", ".pptx", ".png", ".jpg", ".jpeg"}


def classification(extension: str) -> str:
    if extension in PUBLIC_USED:
        return "PUBLIC_USED"
    if extension in PUBLIC_REFERENCE_ONLY:
        return "PUBLIC_REFERENCE_ONLY"
    return "REVIEWED_NOT_PUBLISHED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.source.read_text(encoding="utf-8"))
    archives = {
        item["label"]: {
            "archive_file": Path(item["archive"]).name,
            "archive_sha256": item["sha256"],
            "archive_bytes": item["bytes"],
            "extracted_files": item["extracted_files"],
        }
        for item in payload["archives"]
    }

    rows: list[dict[str, str | int | bool]] = []
    for item in payload["files"]:
        member = PurePosixPath(item["original_member"].replace("\\", "/")).as_posix()
        archive = archives[item["archive"]]
        rows.append(
            {
                "archive_label": item["archive"],
                "archive_file": archive["archive_file"],
                "archive_sha256": archive["archive_sha256"],
                "member_path": member,
                "extension": item["extension"],
                "bytes": item["bytes"],
                "sha256": item["sha256"],
                "nested_archive": item["is_nested_archive"],
                "publication_class": classification(item["extension"]),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
