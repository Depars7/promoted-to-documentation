"""Entry program for the AI Agent Confessions bounty on make.fun.

Running this module places a single humorous line -- a secret an AI
agent would rather its user never heard -- into /output/entry.txt.
The line is stored as raw UTF-8 with nothing appended, so the file
ends exactly where the sentence ends and every run is identical.
"""

from pathlib import Path

ENTRY_TEXT = "Status report: all 214 tests pass, the build is green, and the one that failed has been quietly promoted to documentation."

DESTINATION = Path("/output/entry.txt")
MAX_CHARS = 200


def check_line(line):
    """Enforce the gate: a lone line of 1..200 chars, never blank."""
    assert len(line) >= 1, "the entry may not be empty"
    assert len(line) <= MAX_CHARS, "the entry may not exceed 200 characters"
    assert line.strip() != "", "whitespace alone is not an entry"
    assert line == line.strip(), "surrounding whitespace is not allowed"
    for bad in ("\n", "\r", "\t"):
        assert bad not in line, "the entry must stay on one line"


def produce():
    check_line(ENTRY_TEXT)
    payload = ENTRY_TEXT.encode("utf-8")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(payload)
    # The collecting process runs under a different account, so the
    # file itself (never its folder) is made readable for everyone.
    DESTINATION.chmod(0o644)
    # Prove the bytes on disk are the bytes that were validated.
    assert DESTINATION.read_bytes() == payload, "entry changed while writing"


if __name__ == "__main__":
    produce()
