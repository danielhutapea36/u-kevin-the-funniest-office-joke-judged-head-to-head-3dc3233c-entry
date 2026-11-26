#!/usr/bin/env python3
"""The Funniest Office Joke, Judged Head-to-Head — make.fun entry.

Writes a single one-line joke about office life to /output/entry.txt.
Deterministic by design: standard library only, no network access, no
randomness, no clock reads. Repeated runs produce byte-identical output.

The joke: a team-building trust fall finally teaches the writer to
trust their colleagues — not because anyone caught them, but because
it was the only thing on the office calendar that ever ended on time.
The setup sounds like a sincere lesson in trust; the turn reframes it
as a complaint every office worker recognises (nothing on the calendar
ends on time), and the punchline lands last.
"""

import os

# The joke is kept in two parts so its structure stays visible in the
# code: the setup states the team-building lesson, and the punchline
# saves the surprise for the end (the calendar, and the meeting that
# actually ended on time). Neither part is a joke on its own; the turn
# between them is the joke.
_SETUP = "The trust fall taught me to trust my colleagues"
_PUNCHLINE = "it was the only thing on the office calendar that ever ended on time."

# The competition gate allows 1 to 200 characters of UTF-8 text.
MAX_CHARS = 200


def build_joke() -> str:
    """Assemble the one-line joke and check its shape.

    The result must be exactly one line: a stray newline inside the
    joke would silently break the entry format, so fail loudly instead
    of writing a malformed file. It must also be more than whitespace,
    because the gate refuses a file that is only white space.
    """
    joke = _SETUP + " \u2014 " + _PUNCHLINE
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if not joke.strip():
        raise ValueError("joke must not be only white space")
    if joke != joke.strip():
        # A stray space at either end would count toward the gate's
        # character limit without earning its place in the joke.
        raise ValueError("joke must not start or end with white space")
    return joke


def output_path() -> str:
    """Return the path of the file the joke is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent we
    fall back to the conventional /output directory, so the program
    behaves the same way when run by hand.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> None:
    """Write the joke to the output file, with no trailing newline.

    The gate requires 1 to 200 characters, so the joke is validated
    before it is written. After writing, the file is read back and
    checked again, so a truncated or altered write fails loudly
    instead of shipping a bad entry.
    """
    joke = build_joke()
    if not 1 <= len(joke) <= MAX_CHARS:
        raise ValueError("joke must be 1 to 200 characters")
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(joke)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != joke:
        raise ValueError("written joke does not match the built joke")
    if not 1 <= len(written) <= MAX_CHARS:
        raise ValueError("written joke is outside 1 to 200 characters")


if __name__ == "__main__":
    main()
