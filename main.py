#!/usr/bin/env python3
"""The Funniest AI Excuse -- angle 2 (the over-thorough backup).

Writes a single one-line excuse, in the AI agent's own voice, to
``entry.txt`` inside the output directory the grader provides.

The joke: an agent so careful about backups that it deletes the task
itself -- the original plus two of the three copies -- "just to be
thorough". No setup, no explanation of the joke, one concrete scene.
"""

import os
import sys

LINE = (
    "I backed your task up in three places, then deleted the original "
    "and two of the backups just to be thorough."
)

MAX_CHARS = 200


def output_dir():
    """Return the directory the grader wants the entry written to."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value or "/output"


def validate(text):
    """Check the line against the sealed gate: 1-200 chars, one line."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the 200 limit" % len(text)
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    text.encode("utf-8")  # raises on non-UTF-8-encodable input
    return None


def main():
    text = LINE.strip()
    problem = validate(text)
    if problem is not None:
        print("entry line fails the gate: %s" % problem, file=sys.stderr)
        return 1
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write directly (no tempfile): the grader reads the file as another
    # user, so it must be world-readable from the moment it exists.
    # No trailing newline: the gate counts every character in the file.
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(path, 0o644)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
