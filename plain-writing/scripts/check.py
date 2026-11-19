#!/usr/bin/env python3
"""Flag long sentences, long paragraphs and formal words in a Markdown or plain-text file.

Usage:
    python3 check.py FILE [--max-words 25] [--max-sentences 6]
    cat FILE | python3 check.py -

Skips fenced code blocks, inline code and URLs. Exits 1 when it finds something, 0 otherwise.
It does not check facts: that stays a human (or model) step.
"""

import argparse
import re
import sys

# (pattern, suggestion). Patterns are case-insensitive and match whole words.
FORMAL_WORDS = [
    # English
    (r"commenc\w*", "start"),
    (r"utili[sz]\w*", "use / usar"),
    (r"ensur\w*", "make sure"),
    (r"prior to", "before"),
    (r"approximately", "about"),
    (r"in order to", "to"),
    (r"replenish\w*", "fill"),
    (r"facilitat\w*", "help"),
    (r"leverag\w*", "use"),
    (r"subsequently", "then, after"),
    (r"additionally", "also"),
    (r"numerous", "many"),
    (r"sufficient", "enough"),
    (r"terminat\w*", "stop, end"),
    (r"endeavou?r\w*", "try"),
    (r"obtain\w*", "get"),
    (r"assist\w*", "help"),
    (r"demonstrat\w*", "show"),
    (r"initiat\w*", "start"),
    (r"in the event that", "if"),
    (r"due to the fact that", "because"),
    (r"at this point in time", "now"),
    (r"it is imperative", "you must"),
    # Spanish
    (r"con anterioridad a", "antes de"),
    (r"dar comienzo\w*", "empezar"),
    (r"aproximadamente", "unos, cerca de"),
    (r"con el fin de", "para"),
    (r"a fin de", "para"),
    (r"garantiz\w*", "asegurarse de"),
    (r"llevar a cabo", "hacer"),
    (r"lleva a cabo", "hace"),
    (r"en el caso de que", "si"),
    (r"debido a que", "porque"),
    (r"posteriormente", "después"),
    (r"adicionalmente", "además"),
    (r"realiz\w*", "hacer"),
    (r"efectu\w*", "hacer"),
    (r"mediante", "con"),
    (r"proceder a", "(quitarlo)"),
    (r"en la actualidad", "hoy, ahora"),
    (r"cabe destacar", "(quitarlo)"),
    (r"es importante destacar", "(quitarlo)"),
]
FORMAL_RE = [(re.compile(r"\b" + p + r"\b", re.IGNORECASE), s) for p, s in FORMAL_WORDS]

WORD_RE = re.compile(r"\w[\w'’/-]*", re.UNICODE)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
LIST_ITEM_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}")
QUOTED_RE = re.compile(r"\"[^\"]*\"|“[^”]*”")


def clean(line: str) -> str:
    line = re.sub(r"`[^`]*`", "X", line)  # inline code counts as one word
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)  # keep link text only
    line = re.sub(r"https?://\S+", "URL", line)
    return line


def paragraphs(text: str):
    """Yield (start_line, text) for each paragraph, list item or table cell."""
    in_code = False
    buffer: list[str] = []
    start = 0

    def flush():
        nonlocal buffer
        if buffer:
            yield_value = (start, " ".join(buffer))
            buffer = []
            return yield_value
        return None

    lines = text.splitlines()
    skip_until = 0
    if lines and lines[0].strip() == "---":  # YAML frontmatter
        for index, candidate in enumerate(lines[1:], start=2):
            if candidate.strip() == "---":
                skip_until = index
                break

    for number, raw in enumerate(lines, start=1):
        if number <= skip_until:
            continue
        if raw.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
            item = flush()
            if item:
                yield item
            continue
        if in_code:
            continue
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            item = flush()
            if item:
                yield item
            if line.startswith("#"):
                yield number, clean(line.lstrip("#").strip())
            continue
        if line.startswith("|"):
            item = flush()
            if item:
                yield item
            if not TABLE_SEPARATOR_RE.match(line):
                for cell in line.strip("|").split("|"):
                    if cell.strip():
                        yield number, clean(cell.strip())
            continue
        if LIST_ITEM_RE.match(line) or line.startswith(">"):
            item = flush()
            if item:
                yield item
            line = LIST_ITEM_RE.sub("", line).lstrip("> ").strip()
        if not buffer:
            start = number
        buffer.append(clean(line))
    item = flush()
    if item:
        yield item


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="file to check, or - for stdin")
    parser.add_argument("--max-words", type=int, default=25)
    parser.add_argument("--max-sentences", type=int, default=6)
    args = parser.parse_args()

    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    findings: list[str] = []

    for line, paragraph in paragraphs(text):
        sentences = [s for s in SENTENCE_SPLIT_RE.split(paragraph) if WORD_RE.search(s)]
        if len(sentences) > args.max_sentences:
            findings.append(f"L{line}: paragraph has {len(sentences)} sentences (max {args.max_sentences})")
        for sentence in sentences:
            words = len(WORD_RE.findall(sentence))
            if words > args.max_words:
                preview = sentence if len(sentence) <= 70 else sentence[:67] + "..."
                findings.append(f"L{line}: {words} words (max {args.max_words}): {preview}")
        unquoted = QUOTED_RE.sub(" ", paragraph)  # a quoted word is usually an example
        for pattern, suggestion in FORMAL_RE:
            for match in pattern.finditer(unquoted):
                findings.append(f'L{line}: formal word "{match.group(0)}" -> {suggestion}')

    for finding in findings:
        print(finding)
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
