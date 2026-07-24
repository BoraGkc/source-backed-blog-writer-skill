#!/usr/bin/env python3
"""Validate the mechanical requirements of a Source-Backed Blog Writer draft."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FIELDS = (
    "Pattern Used",
    "Search Intent",
    "Primary Keyword",
    "Related Keywords",
    "Competitor Gap Covered",
    "Proprietary Evidence Used",
    "Slug",
    "Meta Title",
    "Meta Description",
)
PLACEHOLDER_RE = re.compile(
    r"\[(?:VERIFY|SOURCE NEEDED|NEEDS SOURCE|UNVERIFIED|PROPRIETARY INPUT NEEDED|INTERNAL LINK NEEDED)(?::[^\]]*)?\]",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"\b[\w][\w’'-]*\b", re.UNICODE)


def heading_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"^\s*#{{1,6}}\s+{re.escape(name)}\s*:?\s*$", re.IGNORECASE)


def field_value(text: str, name: str) -> str:
    lines = text.splitlines()
    inline = re.compile(
        rf"^\s*(?:\*\*)?{re.escape(name)}(?:\*\*)?\s*:\s*(.+?)\s*$",
        re.IGNORECASE,
    )
    heading = heading_pattern(name)
    for index, line in enumerate(lines):
        match = inline.match(line)
        if match:
            return match.group(1).strip().strip("`")
        if heading.match(line):
            for candidate in lines[index + 1 :]:
                candidate = candidate.strip()
                if candidate:
                    return candidate.strip("*` ")
    return ""


def section(text: str, name: str) -> str:
    lines = text.splitlines()
    heading = re.compile(
        rf"^\s*(#{{1,6}})\s+{re.escape(name)}\s*:?\s*$",
        re.IGNORECASE,
    )
    for index, line in enumerate(lines):
        match = heading.match(line)
        if not match:
            continue
        level = len(match.group(1))
        body: list[str] = []
        for candidate in lines[index + 1 :]:
            next_heading = re.match(r"^\s*(#{1,6})\s+", candidate)
            if next_heading and len(next_heading.group(1)) <= level:
                break
            body.append(candidate)
        return "\n".join(body).strip()
    return ""


def list_count(value: str) -> int:
    bullets = re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+\S", value, re.MULTILINE)
    if bullets:
        return len(bullets)
    return len([item for item in re.split(r"[,;\n]", value) if item.strip()])


def article_slice(text: str) -> str:
    lines = text.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if re.match(r"^#\s+\S", line)),
        None,
    )
    if start is None:
        return ""
    end = len(lines)
    stop = re.compile(r"^\s*#{1,6}\s+(?:Image Recommendations|References)\s*:?\s*$", re.IGNORECASE)
    for index in range(start + 1, len(lines)):
        if stop.match(lines[index]):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def faq_count(text: str) -> int:
    block = section(text, "FAQs")
    if not block:
        return 0
    headings = re.findall(r"^\s*#{1,6}\s+.+\?\s*$", block, re.MULTILINE)
    questions = re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\*\*)?.+\?", block, re.MULTILINE)
    bold = re.findall(r"^\s*\*\*(?:Q(?:uestion)?\s*\d*\s*[:.]?\s*)?.+\?\*\*", block, re.MULTILINE)
    return len(headings) + len(questions) + len(bold)


def validate(
    text: str,
    allow_placeholders: bool = False,
    allow_extended: bool = False,
) -> tuple[list[str], list[str], list[str]]:
    passed: list[str] = []
    warnings: list[str] = []
    failures: list[str] = []

    values = {name: field_value(text, name) for name in FIELDS}
    missing = [name for name, value in values.items() if not value]
    if missing:
        failures.append("Missing fields: " + ", ".join(missing))
    else:
        passed.append("Required metadata fields are present")

    article = article_slice(text)
    if not article:
        failures.append("Missing H1 article title")
    else:
        words = WORD_RE.findall(article)
        maximum = 2500 if allow_extended else 2000
        if 1500 <= len(words) <= maximum:
            passed.append(f"Article length is {len(words)} words")
        else:
            failures.append(
                f"Article length is {len(words)} words; expected 1,500-{maximum:,}"
            )

        keyword = values["Primary Keyword"]
        first_100 = " ".join(words[:100]).casefold()
        if keyword and keyword.casefold() in first_100:
            passed.append("Primary keyword appears in the first 100 words")
        elif keyword:
            failures.append("Primary keyword is absent from the first 100 words")

    title = values["Meta Title"]
    if title:
        if len(title) < 60:
            passed.append(f"Meta title is {len(title)} characters")
        else:
            failures.append(f"Meta title is {len(title)} characters; expected under 60")
        keyword = values["Primary Keyword"]
        if keyword and keyword.casefold() in title.casefold():
            passed.append("Meta title contains the primary keyword")
        elif keyword:
            failures.append("Meta title does not contain the primary keyword")
        h1 = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
        if h1 and h1.group(1).strip().casefold() != title.casefold():
            passed.append("Meta title differs from the H1")
        elif h1:
            failures.append("Meta title must differ from the H1")

    description = values["Meta Description"]
    if description:
        if 150 <= len(description) <= 160:
            passed.append(f"Meta description is {len(description)} characters")
        else:
            failures.append(
                f"Meta description is {len(description)} characters; expected 150-160"
            )

    slug = values["Slug"]
    if slug:
        slug_words = [word for word in re.split(r"[-_/]+", slug.strip("/")) if word]
        if len(slug_words) <= 5:
            passed.append(f"Slug has {len(slug_words)} words")
        else:
            failures.append(f"Slug has {len(slug_words)} words; expected at most 5")

    related = section(text, "Related Keywords") or values["Related Keywords"]
    related_count = list_count(related)
    if related_count >= 10:
        passed.append(f"Related keywords contain {related_count} terms")
    else:
        failures.append(f"Related keywords contain {related_count} terms; expected at least 10")

    key_points = section(text, "Key Points")
    key_point_count = list_count(key_points)
    if 3 <= key_point_count <= 6:
        passed.append(f"Key Points contain {key_point_count} items")
    else:
        failures.append(f"Key Points contain {key_point_count} items; expected 3-6")

    faqs = faq_count(text)
    if 3 <= faqs <= 7:
        passed.append(f"FAQs contain {faqs} questions")
    else:
        failures.append(f"FAQs contain {faqs} questions; expected 3-7")

    images = list_count(section(text, "Image Recommendations"))
    if images >= 4:
        passed.append(f"Image Recommendations contain {images} items")
    else:
        failures.append(f"Image Recommendations contain {images} items; expected at least 4")

    references = section(text, "References")
    if references:
        passed.append("References section is present")
    else:
        failures.append("References section is missing or empty")

    placeholders = PLACEHOLDER_RE.findall(text)
    if placeholders:
        message = f"Found {len(placeholders)} unresolved placeholder(s)"
        (warnings if allow_placeholders else failures).append(message)
    else:
        passed.append("No unresolved placeholders found")

    return passed, warnings, failures


def self_test() -> None:
    meta_description = (
        "Use this home energy audit checklist and practical energy-saving tips "
        "to inspect every room, reduce waste, and start improving your home today."
    ).ljust(150, ".")
    body = " ".join(["home energy audit checklist"] + ["useful"] * 1497)
    sample = f"""\
## Pattern Used
Editorial How-To
## Search Intent
Informational
## Primary Keyword
home energy audit checklist
## Related Keywords
one, two, three, four, five, six, seven, eight, nine, ten
## Competitor Gap Covered
Measured room-by-room observations
## Proprietary Evidence Used
User-provided 12-home field test
## Slug
home-energy-audit-checklist
## Meta Title
Home Energy Audit Checklist
## Meta Description
{meta_description[:160]}
# A Practical Home Energy Audit Checklist for Every Room
## Key Points
- First
- Second
- Third
{body}
## FAQs
### What is a home energy audit?
Answer.
### How long does an audit take?
Answer.
### What should I inspect first?
Answer.
## Image Recommendations
- Cover: filename and alt text
- Attic: filename and alt text
- Window: filename and alt text
- Meter: filename and alt text
## References
- [Public source](https://example.com/source)
"""
    passed, warnings, failures = validate(sample)
    assert passed and not warnings and not failures, failures
    _, _, failures = validate(sample.replace("## Meta Title\nHome Energy Audit Checklist", "## Meta Title\n" + "x" * 60))
    assert any("Meta title" in failure for failure in failures)
    _, _, failures = validate(sample + "\n[VERIFY: claim]\n")
    assert any("placeholder" in failure for failure in failures)
    _, warnings, failures = validate(sample + "\n[VERIFY: claim]\n", allow_placeholders=True)
    assert warnings and not failures
    extended = sample.replace(body, body + " " + " ".join(["extended"] * 600))
    assert validate(extended)[2]
    assert not validate(extended, allow_extended=True)[2]
    print("PASS self-test")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", nargs="?", type=Path, help="Markdown article to validate")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Report approved placeholders as warnings instead of failures",
    )
    parser.add_argument(
        "--allow-extended",
        action="store_true",
        help="Allow an explicitly approved article length up to 2,500 words",
    )
    parser.add_argument("--self-test", action="store_true", help="Run the built-in self-test")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.article:
        parser.error("article is required unless --self-test is used")

    try:
        text = args.article.read_text(encoding="utf-8")
    except OSError as error:
        print(f"FAIL Cannot read {args.article}: {error}", file=sys.stderr)
        return 2

    passed, warnings, failures = validate(
        text,
        allow_placeholders=args.allow_placeholders,
        allow_extended=args.allow_extended,
    )
    for message in passed:
        print(f"PASS {message}")
    for message in warnings:
        print(f"WARN {message}")
    for message in failures:
        print(f"FAIL {message}")
    print(f"\n{len(passed)} passed, {len(warnings)} warnings, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
