# Scoring and reports

## Reviewer rubric

These are reviewer judgments, not a Google ranking formula. Use the following default rubric unless the user supplies another. Explain the evidence supporting earned points and disclose any adaptation.

| Category | Maximum |
|---|---:|
| Crawlability and technical foundations | 20 |
| Titles, descriptions, and headings | 15 |
| Content usefulness, freshness, and trust | 20 |
| Architecture and internal links | 15 |
| Structured data and identity | 10 |
| Images and media | 10 |
| Mobile usability and next steps | 10 |
| Total | 100 |

Allocate criterion weights transparently within each category. Exclude unavailable criteria from both earned and available points; unknowns are neither passes nor zeroes. Retain the original 100-point coverage denominator so a normalized score cannot conceal missing evidence. List exclusions with their weights. Avoid arbitrary point deductions without an observed issue.

Let `E` be earned points and `A` be available points after exclusions:

```text
SEO health = 100 × E / A
Evidence coverage = A / 100 points, plus inspected-URL coverage
```

If `A = 0` or the evidence cannot support a meaningful assessment, report SEO health and overall score as unavailable. With partial evidence, label the score provisional and explain the main gaps. Reviewer criterion coverage and URL coverage are separate measures.

When valid mobile and desktop Performance scores are available for the same target page and audit period, calculate:

```text
Speed = (mobile Performance + desktop Performance) / 2
Overall = 0.80 × SEO health + 0.20 × Speed
```

Keep intermediate precision and round the final displayed overall once to a whole number. For example, `E = 64`, `A = 80`, mobile `40`, desktop `70` gives SEO health `80`, coverage `80/100`, speed `55`, and overall `75/100`.

If either device is unavailable, show valid device results individually and report SEO health separately; omit the two-device composite. Disclose a justified alternative explicitly if the task requires one. Do not replace a missing result with zero, Lighthouse SEO, another model's opinion, or another page's run. Do not average an external reviewer's score into measured performance.

Use audit stars for a supportable displayed score: `90 ≤ score ≤ 100` = ★★★★★; `75 ≤ score < 90` = ★★★★☆; `60 ≤ score < 75` = ★★★☆☆; `40 ≤ score < 60` = ★★☆☆☆; `score < 40` = ★☆☆☆☆. If no composite is available, label stars as SEO health only. Unknown scores have no stars. Pair symbols with text, such as 👍 Strength, 👎 Issue, ✓ Verified, ✗ Failed, ⚠ Caution, and ? Unknown. These are audit assessments, not customer reviews or Lighthouse bands.

## Report contents

Adapt section sizes to the requested scope while covering:

1. Executive assessment with target, audit date, scope, overall/health score status, and main priorities.
2. Evidence coverage, capture times, sample selection, methods, crawl limits, and unavailable measurements.
3. Category points, criterion exclusions, normalization, and the exact score calculation.
4. Technical, on-page, content, internal-link, structured-data, media, and mobile findings with affected URLs and sources.
5. Mobile/desktop PageSpeed tables, lab/field distinctions, and evidence-backed remedies.
6. Relevant conversion, local, and authority observations, identifying unknown private data.
7. External/Command Code review availability or reconciled supplied findings with attribution and validation status.
8. Prioritized fixes showing likely value, relative effort, dependencies where relevant, and observable acceptance checks.
9. A practical 30/60/90-day action sequence and measurement checklist.
10. Tested URL inventory, results/failures, and linked sources.

Use current primary sources for time-sensitive SEO guidance, including [Google's helpful-content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Separate observed defects from hypotheses and recommendations. Do not promise rankings, traffic, conversion gains, or an exhaustive crawl from a sample.

## Downloads and refreshes

Produce matching Markdown and PDF when tools permit. Use an available PDF workflow and visually inspect rendered pages for tables, long URLs, symbols, and page breaks. If a symbol lacks a supported font, use its text label so the PDF remains legible. Check that scores, dates, scopes, metrics, and caveats agree across formats. Claim a PDF only after a usable file exists, and disclose generation or visual-review limitations.

For a refreshed audit, distinguish old and new captures. Deduplicate accepted external findings, record validation status, and update cover, scoring, metric, summary, and action-plan sections together. Attribute a changed score to comparable evidence or disclosed coverage/rubric changes. Keep previous evidence rather than silently overwriting it.
