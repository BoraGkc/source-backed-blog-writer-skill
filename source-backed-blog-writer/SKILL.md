---
name: source-backed-blog-writer
description: Research, plan, write, refresh, and audit complete source-backed SEO blog posts and articles. Use for keyword-led editorial content, commercial product content, how-to guides, list posts, definition posts, newsjacking, pillar pages, alternatives, best-of roundups, product comparisons, content briefs, SEO rewrites, and pre-publish reviews. Produces a sourced 1,500-2,000-word article with metadata, keywords, internal-link opportunities, FAQs, image recommendations, competitor-gap coverage, claim provenance, and deterministic validation.
---

# Source-Backed Blog Writer

Create people-first articles that satisfy search intent, add verifiable original value, and are ready for editorial review. Treat the user's brief and explicit constraints as authoritative.

## Required inputs

Identify:

- exact topic and primary keyword
- publishing website/domain
- audience, market, and language
- brand voice and desired CTA
- product/company details when commercially relevant
- proprietary evidence: firsthand experience, interview quote, internal data, test result, event observation, or another verifiable original fact
- author identity and real credentials when the article uses a byline or first-person voice
- one to three representative writing samples when close voice matching matters

Infer low-risk details from the brief or website. Ask only when a missing answer blocks correct research or would force fabrication.

Never invent search volume, rankings, quotes, product experience, internal data, URLs, pricing, review sentiment, or proprietary facts. If proprietary evidence is missing, stop before drafting and request one concrete input. If the user explicitly asks to proceed, insert a visible `[PROPRIETARY INPUT NEEDED: ...]` placeholder and exclude it from factual claims.

When writing samples are supplied, derive a short internal voice profile covering tone, sentence and paragraph tendencies, preferred vocabulary, prohibited language, and first-person versus institutional perspective. Treat the samples as style evidence, not permission to copy wording. Use neutral professional language when no usable voice evidence exists. Never write firsthand statements in the author's voice unless the user supplied the underlying experience.

## Source priority

Apply instructions in this order:

1. User brief and explicit constraints
2. Commercial patterns for product-led Alternatives, Best-Of, Comparison, and How-To articles
3. Editorial patterns for informational How-To, List, What-Is, Newsjacking, Pillar, and Infographic articles
4. General SEO guidance

The required article range is 1,500-2,000 words, even when a source suggests another length. Treat 2,000 as the default absolute maximum; allow up to 2,500 only when the user explicitly requires additional coverage. Count the article from introduction through FAQs; exclude planning metadata, image recommendations, and references. Budget the first draft for 1,450-1,600 words: roughly 125-150 for the introduction and key points, 1,100-1,200 for the body, and 225-250 for the conclusion and FAQs. Revise upward or downward after counting.

Before outlining, read [references/article-patterns.md](references/article-patterns.md) completely and select one pattern. State the selected pattern at the top of the delivered document.

## Workflow

### 1. Research before writing

Use current web research unless the user explicitly forbids it.

1. Run `"<primary keyword>" site:<domain>` and inspect plausible matches. Compare topic, intent, and angle, not titles alone. If an existing page substantially satisfies the same intent, flag the duplicate and recommend refresh, consolidation, or a distinct angle before drafting.
2. Search the primary keyword and inspect the top three relevant organic articles. Exclude ads, social posts, video-only results, and pages that do not match intent. Record each article's format, core sections, evidence, freshness, and omissions.
3. Classify intent as informational, commercial investigation, transactional, navigational, or mixed. Match the opening, depth, proof, and CTA to that intent.
4. Build a set of at least 10 useful terms: the primary keyword, close variants, entities, subtopics, and long-tail queries. Do not pad the list with awkward synonyms. Report volume or difficulty only when a source supplies it.
5. Collect real FAQ candidates from People Also Ask when available; otherwise use related searches or clearly evidenced user queries.
6. Find relevant internal pages on the publishing domain. Use only verified URLs and descriptive anchors.
7. Prefer primary and authoritative sources for factual claims. Verify time-sensitive facts such as prices, laws, product features, and dates immediately before use.

Do not copy competitor wording or link to competitor sites in the published article. Competitors inform gap analysis only.

### 2. Create a research brief

Record internally:

- duplicate check result
- intent and reader job-to-be-done
- top-three competitor coverage and shared pattern
- at least one defensible content gap
- selected article pattern and rationale
- proprietary evidence to include and its provenance
- author and voice profile when applicable
- primary CTA and internal-link targets
- a claim ledger with each material claim, classification, source, and verification date

A competitor omission is not proprietary evidence by itself. Original synthesis may be a differentiator, but label it as analysis rather than firsthand data.

Use the columns `Claim | Classification | Source | Verified`. Classify entries as `Proprietary evidence`, `User-provided`, `Primary source`, `Secondary source`, `Calculated`, `Analysis`, or `Unverified`. Keep the ledger internal unless the user requests an audit trail or unresolved material claims remain. Unverified material claims block a publish-ready label.

### 3. Outline for information gain

Make every H2 answer a distinct reader question or advance the decision/process. Put the section's answer or most important claim in its first one or two sentences. Remove any section that only restates an earlier point.

Use H3s only when they divide an H2 into meaningful subtopics. For steps and list items, give each major item its own heading. Add tables only when they make a real comparison easier to scan.

### 4. Draft the article

Write in clear, professional, approachable language. Use short paragraphs, varied but concise sentences, transitions, bullets, and numbered steps where they improve comprehension. Explain unavoidable jargon inline.

Meet all of these requirements:

- Follow the exact assigned topic and chosen article pattern.
- Use the primary keyword within the first 100 words and naturally in at least three headings when grammar permits.
- Lead with 3-6 key-point bullets that answer the main question directly.
- Use specific names, dates, numbers, methods, and outcomes when supported.
- Include at least one verified proprietary fact or the approved placeholder.
- Cover at least one meaningful angle absent from the reviewed competitors.
- Distinguish benefits from features in commercial content.
- Treat competitors fairly; state where another option is stronger and never manufacture drawbacks.
- For Alternatives, Best-Of, and Comparison articles, publish a concise methodology section covering inclusion criteria, tested versus desk-researched products, consistent evaluation criteria, research and pricing dates, material relationships, limitations, and unknowns.
- Keep the conclusion brief, reinforce the decision or takeaway, and introduce no new facts.
- Use internal links with descriptive anchor text and verified URLs. If none are discoverable, add `[INTERNAL LINK NEEDED: suggested anchor -> target page type]` rather than inventing a URL.
- Keep external hyperlinks out of the body. Cite sources with readable names or note markers, then put non-competing source URLs in `References`. For competitor sources, list publisher, page title, and access date without a live URL.
- Paraphrase sources. Use short quotes only when the exact wording matters and attribution is clear.

SEO is subordinate to usefulness. The editorial word target is not a Google ranking factor, no keyword density is required, and no snippet or AI citation can be guaranteed.

### 5. Package the deliverable

Use H2 headings for package labels and exactly one H1 for the article title. Use this order:

1. `Pattern Used`
2. `Search Intent`
3. `Primary Keyword`
4. `Related Keywords` with at least 10 comma-separated terms or list items
5. `Competitor Gap Covered`
6. `Proprietary Evidence Used`
7. `Slug` with at most five words and the primary keyword when natural
8. `Meta Title` under 60 characters, containing the primary keyword, and different from the H1
9. `Meta Description` of 150-160 characters, containing two distinct long-tail terms and a CTA
10. H1 article title
11. `Key Points` with 3-6 bullets
12. Article body with H2/H3 hierarchy
13. Brief conclusion
14. `FAQs` with 3-7 real long-tail questions formatted as H3 headings and followed by 1-3 sentence answers; do not reuse an existing heading target
15. `Image Recommendations`: one list item for the cover plus at least three for in-article images, each with placement, concept, descriptive filename, and useful alt text
16. `References`: link non-competing authoritative sources; list competitor sources without live URLs

Do not add research-process commentary to the article unless requested. In the References section, include only sources actually used.

### 6. Validate before delivery

When file and shell access are available, write the complete package to a temporary Markdown file and run:

```bash
python3 <skill-directory>/scripts/validate_article.py <draft.md>
```

Fix every failure and rerun until the command exits successfully. Use `--allow-placeholders` only when the user explicitly approved visible placeholders; report that the result is a draft, not publish-ready. If the script cannot run, apply the same checks manually and label the word count as estimated.

Use `--allow-extended` only when the user explicitly required additional coverage up to 2,500 words.

- article is 1,500-2,000 words from the H1 through FAQs
- never report a count as verified when it was only estimated; exceed 2,000 words only for explicit required coverage and never exceed 2,500
- article pattern name appears at the top
- 10 or more useful keywords are listed
- primary keyword appears in the first 100 words
- meta title is under 60 characters
- meta description is 150-160 characters and contains two distinct long-tail terms plus a CTA
- slug has no more than five words
- each section adds new information and begins answer-first
- proprietary evidence is present, attributed, and not fabricated
- competitor gap is genuinely covered
- claims with numbers, dates, names, or outcomes have support
- internal links use verified URLs and descriptive anchors
- FAQs do not duplicate article heading targets
- cover plus at least three additional image recommendations include filenames and alt text
- external references are authoritative, used, and non-competitive
- spelling, grammar, tone, and brand alignment pass

The validator can detect structure, counts, lengths, and unresolved placeholders. It cannot prove that a claim is supported; verify factual support against the claim ledger.

Revise once to remove repetition, unsupported claims, padding, keyword stuffing, generic AI phrasing, and any promise the evidence cannot support. Deliver the article, not the checklist, unless the user asks for an audit trail.

## Refresh and audit tasks

For an existing article, preserve useful original material, rerun the duplicate/SERP/source checks, identify stale or unsupported claims, and revise only where the evidence or intent requires it. Apply the same final validation. Do not rewrite merely to make wording different.

After a refresh, report:

- intent or competitor changes
- facts and sources updated
- sections preserved, removed, or consolidated
- remaining unsupported claims
- recommended published-date or last-updated-date treatment
- a suggested next review

Recommend performance checkpoints only when analytics or Search Console access exists. Label unavailable metrics as unknown and never invent expected gains.

For a requested audit, report findings by severity and point to exact sections. Do not rewrite unless asked.
