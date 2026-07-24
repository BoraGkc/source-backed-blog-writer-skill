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
    "Publish Readiness",
    "Slug",
    "Meta Title",
    "Meta Description",
    "CMS Excerpt",
)
PLACEHOLDER_RE = re.compile(
    r"\[(?:VERIFY|SOURCE NEEDED|NEEDS SOURCE|UNVERIFIED|PROPRIETARY INPUT NEEDED|INTERNAL LINK NEEDED)(?::[^\]]*)?\]",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"\b[\w][\w’'-]*\b", re.UNICODE)
# ponytail: common imperative verbs cover the current CTA contract; expand only
# if real drafts expose false negatives.
CTA_RE = re.compile(
    r"(?:^|[.!?]\s+)(?:use|learn|discover|compare|find|see|read|get|explore|start|choose|check)\b",
    re.IGNORECASE,
)
IMAGE_RE = re.compile(
    r"^\s*[-*+]\s+Placement:\s*([^|\n]+?)\s*\|\s*"
    r"Concept:\s*([^|\n]+?)\s*\|\s*"
    r"Filename:\s*([^|\s]+\.(?:avif|gif|jpe?g|png|svg|webp))\s*\|\s*"
    r"Alt text:\s*(\S.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


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
            body: list[str] = []
            for candidate in lines[index + 1 :]:
                if re.match(r"^\s*#{1,6}\s+", candidate):
                    break
                candidate = candidate.strip()
                if candidate:
                    body.append(candidate.strip("*` "))
            return " ".join(body)
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


def list_items(value: str) -> list[str]:
    bullets = re.findall(
        r"^\s*(?:[-*+]|\d+[.)])\s+(.+?)\s*$",
        value,
        re.MULTILINE,
    )
    if bullets:
        return bullets
    return [item.strip() for item in re.split(r"[,;\n]", value) if item.strip()]


def list_count(value: str) -> int:
    return len(list_items(value))


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


def normalize_heading(value: str) -> str:
    return " ".join(re.findall(r"\w+", value.casefold(), re.UNICODE))


def faq_questions(text: str) -> list[str]:
    block = section(text, "FAQs")
    if not block:
        return []
    return re.findall(r"^\s*###\s+(.+\?)\s*$", block, re.MULTILINE)


def citation_numbers(text: str) -> list[int]:
    return [int(value) for value in re.findall(r"\[(\d+)\](?!\()", text)]


def reference_numbers(text: str) -> list[int]:
    return [
        int(value)
        for value in re.findall(
            r"^\s*(\d+)[.)]\s+\S",
            section(text, "References"),
            re.MULTILINE,
        )
    ]


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

    h1s = re.findall(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if len(h1s) == 1:
        passed.append("Document contains exactly one H1")
    elif not h1s:
        failures.append("Missing H1 article title")
    else:
        failures.append(f"Document contains {len(h1s)} H1 headings; expected exactly one")

    article = article_slice(text)
    if article:
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
        if h1s and h1s[0].strip().casefold() != title.casefold():
            passed.append("Meta title differs from the H1")
        elif h1s:
            failures.append("Meta title must differ from the H1")

    description = values["Meta Description"]
    if description:
        if 150 <= len(description) <= 160:
            passed.append(f"Meta description is {len(description)} characters")
        else:
            failures.append(
                f"Meta description is {len(description)} characters; expected 150-160"
            )

        related = section(text, "Related Keywords") or values["Related Keywords"]
        description_text = normalize_heading(description)
        long_tail_matches = {
            normalized
            for term in list_items(related)
            if len(WORD_RE.findall(term)) >= 2
            and (normalized := normalize_heading(term)) in description_text
        }
        if len(long_tail_matches) >= 2:
            passed.append("Meta description contains two related long-tail terms")
        else:
            failures.append(
                "Meta description contains fewer than two related long-tail terms"
            )

        if CTA_RE.search(description):
            passed.append("Meta description contains a CTA")
        else:
            failures.append("Meta description does not contain a recognized CTA")

    excerpt = values["CMS Excerpt"]
    if excerpt:
        excerpt_words = len(WORD_RE.findall(excerpt))
        if 35 <= excerpt_words <= 60:
            passed.append(f"CMS excerpt is {excerpt_words} words")
        else:
            failures.append(
                f"CMS excerpt is {excerpt_words} words; expected 35-60"
            )
        if excerpt.casefold() == description.casefold():
            failures.append("CMS excerpt must differ from the meta description")
        elif re.search(r"https?://|\[[^\]]+\]\([^)]+\)", excerpt):
            failures.append("CMS excerpt must not contain links")
        else:
            passed.append("CMS excerpt is link-free and differs from the meta description")

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

    keyword = normalize_heading(values["Primary Keyword"])
    keyword_headings = [
        heading
        for heading in re.findall(r"^\s*#{1,3}\s+(.+?)\s*$", article, re.MULTILINE)
        if keyword and keyword in normalize_heading(heading)
    ]
    if len(keyword_headings) >= 3:
        passed.append(
            f"Primary keyword appears in {len(keyword_headings)} article headings"
        )
    elif keyword:
        failures.append(
            f"Primary keyword appears in {len(keyword_headings)} article headings; expected at least 3"
        )

    key_points = section(text, "Key Points")
    key_point_count = list_count(key_points)
    if 3 <= key_point_count <= 6:
        passed.append(f"Key Points contain {key_point_count} items")
    else:
        failures.append(f"Key Points contain {key_point_count} items; expected 3-6")

    questions = faq_questions(text)
    if 3 <= len(questions) <= 7:
        passed.append(f"FAQs contain {len(questions)} H3 questions")
    else:
        failures.append(
            f"FAQs contain {len(questions)} H3 questions; expected 3-7"
        )

    normalized_questions = [normalize_heading(question) for question in questions]
    duplicate_questions = sorted(
        {
            question
            for question in normalized_questions
            if normalized_questions.count(question) > 1
        }
    )
    if duplicate_questions:
        failures.append("FAQs contain duplicate question headings")
    elif questions:
        passed.append("FAQ question headings are unique")

    article_before_faq = re.split(
        r"^\s*##\s+FAQs\s*:?\s*$",
        article,
        maxsplit=1,
        flags=re.IGNORECASE | re.MULTILINE,
    )[0]
    article_targets = {
        normalize_heading(heading)
        for heading in re.findall(
            r"^\s*#{2,3}\s+(.+?)\s*$",
            article_before_faq,
            re.MULTILINE,
        )
    }
    reused_questions = sorted(set(normalized_questions) & article_targets)
    if reused_questions:
        failures.append("FAQ question headings duplicate article heading targets")
    elif questions:
        passed.append("FAQ questions do not duplicate article heading targets")

    body_h2s = [
        normalize_heading(heading)
        for heading in re.findall(
            r"^\s*##\s+(.+?)\s*$",
            article_before_faq,
            re.MULTILINE,
        )
        if normalize_heading(heading) not in {"key points", "table of contents"}
    ]
    toc_required = (
        "pillar" in values["Pattern Used"].casefold() or len(body_h2s) >= 5
    )
    toc = section(text, "Table of Contents")
    if toc_required and toc:
        passed.append("Required Table of Contents is present")
    elif toc_required:
        failures.append(
            "Table of Contents is required for Pillar articles or 5+ body H2 sections"
        )
    elif toc:
        failures.append("Table of Contents should be omitted for this article")
    else:
        passed.append("Table of Contents is correctly omitted")

    image_block = section(text, "Image Recommendations")
    image_items = list_items(image_block)
    image_details = IMAGE_RE.findall(image_block)
    if len(image_items) >= 4 and len(image_details) == len(image_items):
        passed.append(
            f"Image Recommendations contain {len(image_items)} fully specified items"
        )
    else:
        failures.append(
            "Image Recommendations require at least 4 items with placement, "
            "concept, filename, and alt text"
        )
    if image_details and any(
        "cover" in placement.casefold() for placement, _, _, _ in image_details
    ):
        passed.append("Image Recommendations include a cover image")
    else:
        failures.append("Image Recommendations do not include a cover placement")

    references = section(text, "References")
    if references:
        passed.append("References section is present")
    else:
        failures.append("References section is missing or empty")

    citations = citation_numbers(article)
    numbered_references = reference_numbers(text)
    unique_citations = list(dict.fromkeys(citations))
    expected = list(range(1, len(unique_citations) + 1))
    if not citations:
        failures.append("Article contains no numbered citations")
    elif unique_citations != expected:
        failures.append("Numbered citations must begin at [1] and follow first-use order")
    elif numbered_references != expected:
        failures.append("Numbered references must map exactly to cited markers")
    else:
        passed.append(
            f"{len(unique_citations)} numbered citation(s) map to References"
        )

    placeholders = PLACEHOLDER_RE.findall(text)
    if placeholders:
        message = f"Found {len(placeholders)} unresolved placeholder(s)"
        (warnings if allow_placeholders else failures).append(message)
    else:
        passed.append("No unresolved placeholders found")

    readiness = values["Publish Readiness"]
    readiness_match = re.match(
        r"^(blocked|draft|publish[- ]ready)\b",
        readiness,
        re.IGNORECASE,
    )
    if readiness and readiness_match:
        passed.append(f"Publish readiness is {readiness_match.group(1)}")
    elif readiness:
        failures.append("Publish Readiness must be Blocked, Draft, or Publish-ready")
    if (
        readiness_match
        and readiness_match.group(1).casefold().replace(" ", "-") == "publish-ready"
        and (failures or warnings)
    ):
        failures.append("Publish-ready status conflicts with validation issues")

    return passed, warnings, failures


def self_test() -> None:
    meta_description = (
        "Use this home energy audit checklist and practical energy-saving tips "
        "to inspect every room, reduce waste, and start improving your home today."
    ).ljust(150, ".")
    cms_excerpt = (
        "This room-by-room guide explains how homeowners can inspect insulation, "
        "windows, appliances, and energy use.\nIt combines a practical checklist "
        "with observations from a twelve-home field test so readers can identify "
        "waste and prioritize realistic improvements."
    )
    body = " ".join(["home energy audit checklist"] + ["useful"] * 1497) + " [1]"
    sample = f"""\
## Pattern Used
Editorial How-To
## Search Intent
Informational
## Primary Keyword
home energy audit checklist
## Related Keywords
home energy audit checklist, practical energy saving tips, room by room home audit, diy energy inspection, reduce home energy waste, attic insulation check, window draft inspection, appliance energy use, homeowner audit steps, lower utility bills
## Competitor Gap Covered
Measured room-by-room observations
## Proprietary Evidence Used
User-provided 12-home field test
## Publish Readiness
Publish-ready — validation and claim verification passed
## Slug
home-energy-audit-checklist
## Meta Title
Home Energy Audit Checklist
## Meta Description
{meta_description[:160]}
## CMS Excerpt
{cms_excerpt}
# A Practical Home Energy Audit Checklist for Every Room
## Key Points
- First
- Second
- Third
## Home Energy Audit Checklist Steps
### Home Energy Audit Checklist Setup
{body}
## FAQs
### What is a home energy audit?
Answer.
### How long does an audit take?
Answer.
### What should I inspect first?
Answer.
## Image Recommendations
- Placement: Cover | Concept: Home inspection overview | Filename: home-energy-audit-cover.webp | Alt text: Homeowner reviewing an energy audit checklist
- Placement: Attic section | Concept: Insulation inspection | Filename: attic-insulation-check.webp | Alt text: Measuring attic insulation depth
- Placement: Window section | Concept: Draft detection | Filename: window-draft-inspection.webp | Alt text: Checking a window frame for air leaks
- Placement: Appliance section | Concept: Meter reading | Filename: appliance-energy-meter.webp | Alt text: Energy meter connected to a household appliance
## References
1. [Public source](https://example.com/source)
"""
    passed, warnings, failures = validate(sample)
    assert passed and not warnings and not failures, failures
    _, _, failures = validate(sample.replace("## Meta Title\nHome Energy Audit Checklist", "## Meta Title\n" + "x" * 60))
    assert any("Meta title" in failure for failure in failures)
    _, _, failures = validate(sample + "\n[VERIFY: claim]\n")
    assert any("placeholder" in failure for failure in failures)
    draft = sample.replace(
        "Publish-ready — validation and claim verification passed",
        "Draft — approved verification placeholder remains",
    )
    _, warnings, failures = validate(draft + "\n[VERIFY: claim]\n", allow_placeholders=True)
    assert warnings and not failures
    extended = sample.replace(body, body + " " + " ".join(["extended"] * 600))
    assert validate(extended)[2]
    assert not validate(extended, allow_extended=True)[2]
    _, _, failures = validate(sample.replace("## FAQs", "# Extra title\n## FAQs"))
    assert any("exactly one" in failure for failure in failures)
    duplicate_faq = sample.replace(
        "### What should I inspect first?",
        "### What is a home energy audit?",
    )
    _, _, failures = validate(duplicate_faq)
    assert any("duplicate question" in failure for failure in failures)
    _, _, failures = validate(sample.replace("[1]", "[2]", 1))
    assert any("citations" in failure or "references" in failure for failure in failures)
    weak_headings = sample.replace(
        "## Home Energy Audit Checklist Steps",
        "## Inspection Steps",
    ).replace(
        "### Home Energy Audit Checklist Setup",
        "### Preparation",
    )
    _, _, failures = validate(weak_headings)
    assert any("article headings" in failure for failure in failures)
    weak_terms = (
        "Explore a practical inspection guide for homeowners who want a clearer "
        "view of household efficiency, common trouble spots, priorities, and "
        "realistic improvements they can make today."
    ).ljust(150, ".")
    _, _, failures = validate(
        sample.replace(meta_description[:160], weak_terms[:160], 1)
    )
    assert any("long-tail terms" in failure for failure in failures)
    no_cta = (
        "This home energy audit checklist and practical energy-saving tips cover "
        "every room, common sources of waste, inspection priorities, and realistic "
        "home improvements."
    ).ljust(150, ".")
    _, _, failures = validate(
        sample.replace(meta_description[:160], no_cta[:160], 1)
    )
    assert any("recognized CTA" in failure for failure in failures)
    malformed_image = sample.replace(
        "Filename: attic-insulation-check.webp",
        "File: attic-insulation-check.webp",
        1,
    )
    _, _, failures = validate(malformed_image)
    assert any("Image Recommendations require" in failure for failure in failures)
    _, _, failures = validate(
        sample.replace("Editorial How-To", "Pillar", 1)
    )
    assert any("Table of Contents is required" in failure for failure in failures)
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
