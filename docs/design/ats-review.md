# ATS / AI-filter review

Empirical method: each PDF was run through `pdftotext` (the same text-extraction
step an ATS performs) and the parsed reading order inspected. A CV that parses
in the wrong order, drops content, or mangles section headers loses keyword and
section signal regardless of how good it looks.

## Format verdict (parse-ability)

| Variant | Parse result | ATS verdict |
|---|---|---|
| **Single-column** (`cv-singlecol.pdf`) | Top-to-bottom, correct order, clean section headers, all keywords intact | ✅ Best — submit this |
| **LaTeX** (`cv-latex.pdf`) | Correct order, complete, classic typeset look | ✅ Good — fine to submit |
| **Two-column sidebar** (`cv-twocol.pdf`) | Name split ("Joseph" / "Barnett"), sidebar skills interleaved line-by-line into the summary | ❌ Fails parsers — web/visual only, never upload |

**Rule:** the gorgeous two-column layout is for *humans* (web page, LinkedIn,
personal site). The file you upload to a job portal must be single-column or the
LaTeX PDF. Different audience, different artifact.

## What already helps the filters

- Standard, recognized section headings (Summary, Professional Experience, Skills, Education).
- Dense exact-noun keyword surface: Kubernetes, EKS, Go, Rust, Snowflake, Trino,
  Terraform, Pulumi, CloudFormation, eBPF, FedRAMP, SOC 2, ISO 27001.
- Quantified outcomes (50 TB/week, 0.09%, 10,000+ nodes) — recruiter signal.
- Plain-text contact line; consistent `MMM YYYY` dates; selectable PDF text.

## Tactical gaps to close (exact-match magnets)

1. **Name specific tools, not just capabilities.** Filters often match literal
   product names. Add the concrete tools behind "telemetry" / "observability":
   **OpenTelemetry (OTEL), Prometheus, Grafana, Kafka**. High-value, low-cost.
2. **Spell out acronyms once** for the literal matchers: "Infrastructure as
   Code (IaC)", "CI/CD (continuous integration / delivery)".
3. **Mirror the target job title.** ATS weight the headline. If a posting says
   "Principal Engineer" / "Staff Engineer" / "Software Architect", echo that
   wording in the title line for that application.
4. **Add a few generic AI nouns** if targeting AI roles: "GenAI", "LLMOps",
   "machine learning" — alongside the existing LLM/agentic terms.
5. **Word-only portals:** generate a `.docx` from `cv.md` via
   `pandoc dist/cv.md -o dist/cv.docx`. Some ATS still prefer Word.

## Recommendation

- **Submit:** `cv-singlecol.pdf` (or `cv-latex.pdf` for the classic serif look).
- **Share with humans:** the two-column HTML page.
- **Keep a `.docx`** ready from the Markdown for portals that demand Word.
- Apply the tool-name and title-mirroring tweaks per target role.
