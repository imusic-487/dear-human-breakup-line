#!/usr/bin/env python3
"""Write the breakup line to /output/entry.txt.

Reads line.txt next to this file, checks it against the bounty gate
(UTF-8 text, 1 to 200 characters, exactly one line, not only
whitespace), then writes it byte-for-byte to /output/entry.txt and
echoes it to stdout.
"""

import sys
from pathlib import Path

MAX_CHARS = 200
SOURCE = Path(__file__).resolve().parent / "line.txt"
DESTINATION = Path("/output/entry.txt")


def load_line() -> str:
    raw = SOURCE.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{SOURCE} is not valid UTF-8: {exc}") from exc


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def main() -> int:
    try:
        text = load_line()
        validate(text)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    DESTINATION.write_bytes(data)
    print(
        f"wrote {len(text)} characters / {len(data)} bytes to {DESTINATION}",
        file=sys.stderr,
    )
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
