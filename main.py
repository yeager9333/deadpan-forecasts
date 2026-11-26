#!/usr/bin/env python3
"""One-line deadpan weather forecast for the fictional city of Wobbleford.

make.fun bounty: Deadpan Forecasts for Cities That Do Not Exist.
The program writes a single forecast line (at most 160 characters) to
``$MAKEFUN_OUTPUT_DIR/entry.txt``. Python 3.13 standard library only,
no network access, no external files.
"""

import os
import sys
from pathlib import Path

# The forecast, exactly as entered. One line, 156 characters.
FORECAST = (
    "In Wobbleford, expect 9 millimetres of rain falling uphill by midday, "
    "with gusts of 60 kilometres an hour returning lost umbrellas to their "
    "original owners."
)

MAX_CHARS = 160


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    line = FORECAST.strip()

    if not line:
        return fail("forecast line is empty")
    if "\n" in line or "\r" in line:
        return fail("forecast must be a single line")
    if len(line) > MAX_CHARS:
        return fail(f"forecast is {len(line)} chars, over the {MAX_CHARS} limit")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(line + "\n", encoding="utf-8")
    os.chmod(target, 0o644)

    # Read back and confirm what landed on disk.
    written = target.read_text(encoding="utf-8")
    if written.strip() != line:
        return fail("entry.txt does not match the forecast line")
    if len(written.strip()) > MAX_CHARS:
        return fail("entry.txt exceeds the character limit")

    print(f"Wrote {target} ({len(line)} characters): {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
