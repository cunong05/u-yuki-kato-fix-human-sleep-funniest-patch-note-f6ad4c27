"""Fix Human Sleep: Funniest Patch Note — entry writer.

Writes a single original patch note announcing that human sleep has
been fixed to /output/entry.txt, then re-reads the file and re-validates it.

Gate (from the competition kit RULES.txt): the file must be UTF-8 text of
1 to 160 characters, not only white space, and a single line.
"""

import os
import sys

# The entry: one original line, 121 characters, no setup, no explanation.
# A changelog line about the fix: sleep now charges overnight, so the
# morning coffee boot-up is no longer needed.
ENTRY = (
    "Fixed a bug where humans needed coffee to boot up in the morning; "
    "sleep now charges overnight, coffee demoted to a hobby."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 160


def validate(text):
    """Check the gate. Returns a list of failure reasons (empty = valid)."""
    failures = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append(
            "length %d chars, must be %d-%d" % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        failures.append("entry is only white space")
    if text != text.strip():
        failures.append("entry has leading or trailing white space")
    if any(ord(c) < 32 for c in text):
        failures.append("entry contains control characters")
    if "\n" in text or "\r" in text:
        failures.append("entry must be a single line")
    return failures


def validate_bytes(path, text):
    """Check the file on disk is exactly the entry's UTF-8 bytes."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw != text.encode("utf-8"):
        return ["file bytes do not match entry UTF-8 bytes"]
    return []


def main():
    failures = validate(ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAIL: %s" % failure, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    # Re-read the file and validate what was actually written.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY:
        print("GATE FAIL: written file does not match entry", file=sys.stderr)
        return 1
    failures = validate(written)
    if failures:
        for failure in failures:
            print("GATE FAIL (re-read): %s" % failure, file=sys.stderr)
        return 1
    failures = validate_bytes(OUTPUT_PATH, ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAIL (bytes): %s" % failure, file=sys.stderr)
        return 1

    print("OK: wrote %d/%d chars (%d bytes), 1 line, to %s" % (
        len(written), MAX_CHARS, len(written.encode("utf-8")), OUTPUT_PATH))
    print(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
