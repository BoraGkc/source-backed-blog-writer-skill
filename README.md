# Source-Backed Blog Writer

A portable Agent Skill for researching, drafting, refreshing, and auditing complete SEO articles without inventing evidence. It combines search-intent research, duplicate-content checks, article-pattern selection, source discipline, editorial structure, metadata, internal-link opportunities, FAQs, and image recommendations.

## What it does

- Researches the publishing site and the three most relevant organic articles.
- Identifies search intent, useful related terms, verified internal links, and a defensible content gap.
- Selects an editorial or commercial article pattern that matches the reader's job.
- Supports an optional approval mode that presents title options, target questions, claims, and the outline before drafting.
- Produces a sourced 1,500–2,000-word article with metadata, a CMS excerpt, conditional table of contents, and image recommendations.
- Labels each package as blocked, draft, or publish-ready with a reason.
- Stops when proprietary evidence is missing instead of fabricating experience, quotes, data, or results.
- Tracks material claims by source type and verification date, then maps factual claims to numbered references.
- Includes an author bio only when real identity and credentials are supplied.
- Validates article structure, heading keyword use, meta-description terms and CTA, image fields, citation mapping, duplicate FAQs, and unresolved placeholders with a dependency-free script.
- Refreshes existing articles selectively, reports what changed, and audits without rewriting unless asked.

## Required inputs

Provide the topic and primary keyword, publishing domain, audience and market, language and brand voice, desired CTA, relevant product details, and at least one verifiable proprietary fact such as firsthand experience, an interview quote, internal data, or a test result.

The skill can infer low-risk details from the brief or website. It asks when a missing answer would block accurate research or force fabrication.

For close voice matching, also provide the author's name, real credentials, desired first-person or institutional perspective, and one to three representative writing samples. Without supported firsthand evidence, the skill will not invent personal experience.

## Compatibility

The core skill follows the open [Agent Skills specification](https://agentskills.io/specification) and uses provider-neutral `SKILL.md`, `references/`, and `scripts/` conventions. It works with clients that implement Agent Skills, including Codex, ChatGPT skill surfaces, Claude Code, claude.ai custom skills, and the Claude API.

Full research needs web/search access or current sources supplied by the user. The deterministic validator needs Python 3; the skill falls back to manual checks when shell execution is unavailable. `agents/openai.yaml` is optional OpenAI UI metadata and does not change the portable core.

## Install

Clone the repository once:

```bash
git clone https://github.com/BoraGkc/source-backed-blog-writer-skill.git
```

Install the `source-backed-blog-writer` directory in the location used by your client.

### Codex

```bash
mkdir -p ~/.agents/skills
cp -R source-backed-blog-writer-skill/source-backed-blog-writer ~/.agents/skills/
```

For a project-only installation, copy it to `.agents/skills/` in the repository. You can also ask `$skill-installer` to install the repository skill URL.

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R source-backed-blog-writer-skill/source-backed-blog-writer ~/.claude/skills/
```

For a project-only installation, copy it to `.claude/skills/` in the repository.

### ChatGPT, claude.ai, and APIs

- In ChatGPT surfaces that support custom skills, add it through the Skills interface and select it with `@` when explicit invocation is needed.
- In claude.ai, zip the contents of `source-backed-blog-writer/` with `SKILL.md` at the archive root, then upload it as a custom skill.
- For the Claude API, upload the same skill bundle through the Skills API and attach the returned skill ID to the request.

### Other Agent Skills clients

Copy the complete skill directory into the client's configured personal or project skills location. Keep the directory name `source-backed-blog-writer`, matching the `name` in `SKILL.md`, and keep `references/` and `scripts/` with it. Provider-specific optional files may be ignored by clients that do not use them.

Most clients can discover the skill automatically from its description. Explicit invocation varies:

| Client | Explicit invocation |
|---|---|
| Codex CLI or IDE | `$source-backed-blog-writer` |
| ChatGPT skill surfaces | Select with `@` |
| Claude Code | `/source-backed-blog-writer` |
| claude.ai or API | Select or attach the uploaded custom skill |
| Other compatible clients | Use the client’s skill picker or name the skill in the prompt |

To update, run `git pull --ff-only` in the cloned repository and replace the installed skill directory. Back up intentional local edits first.

## Example prompts

```text
Use the source-backed-blog-writer skill to research and draft an article targeting
"home energy audit checklist" for example.com. The audience is US homeowners,
the voice is practical, and our proprietary evidence is a 12-home field test.
```

```text
Use the source-backed-blog-writer skill to plan a fair comparison of Product A and
Product B. Do not draft until you have checked for an existing competing page.
Use approval mode and present title options, target questions, and the outline first.
Use our founder's supplied bio and writing samples for the voice, and include
a methodology section that distinguishes tested from desk-researched claims.
```

```text
Use the source-backed-blog-writer skill to refresh this article using current sources.
Preserve useful original material and change only what is stale or unsupported.
```

```text
Use the source-backed-blog-writer skill to audit this draft. Report issues by severity
and point to exact sections without rewriting it.
```

## Validate a draft

The skill runs its validator automatically when file and shell access are available. You can also run it directly:

```bash
python3 /path/to/source-backed-blog-writer/scripts/validate_article.py article.md
```

The validator uses only the Python standard library. It checks mechanical requirements, exactly one H1, publish-readiness format, conditional table-of-contents use, heading keyword use before the FAQs, meta-description terms and CTA, CMS excerpt rules, image fields, numbered citation mapping, duplicate FAQs, and unresolved placeholders. Claim support still requires source review.

## Limitations

- Full research requires current web access.
- The skill does not supply search volume, rankings, pricing, review sentiment, or proprietary facts without a source.
- It outputs a CMS excerpt but does not generate schema, connect to a CMS, call keyword-volume APIs, or scrape community sites.
- It cannot guarantee rankings, snippets, traffic, or inclusion in AI-generated answers.
- Regulated, legal, medical, financial, and sponsored content still requires qualified human review and any applicable disclosures.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── SOURCES.md
└── source-backed-blog-writer/
    ├── SKILL.md
    ├── agents/openai.yaml  # Optional OpenAI UI metadata
    ├── references/article-patterns.md
    └── scripts/validate_article.py
```

Repository documentation stays outside the installable skill folder.

## License

Original repository content by [Bora Gökçe](https://github.com/BoraGkc) is licensed under [CC BY 4.0](LICENSE).

The license does not cover third-party websites, standards, documentation, names, trademarks, or other referenced works. Those remain subject to their own terms. This repository is independent and does not imply endorsement or affiliation.
