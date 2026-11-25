# RankRadar SEO

RankRadar SEO turns a public website URL into an evidence-backed SEO audit. Claude reviews crawlability, metadata, content, internal links, structured data, images and mobile usability, collects mobile and desktop PageSpeed results, and produces a scored report with a prioritized 30/60/90-day action plan. Reports are delivered as matching Markdown and PDF files when the host can create files, and in chat otherwise.

Published by Stephen J. Kinzey, Ph.D.

## What you get

- An overall score built from a disclosed 100-point reviewer rubric and measured PageSpeed Performance, with the exact calculation shown
- Evidence coverage: which URLs were inspected, what could not be measured, and why
- Findings tied to affected URLs and sources, with fixes ranked by value and effort
- Lab and field performance kept separate; missing measurements are reported as unknown, never estimated

## Install

**Claude Code**

```
/plugin install rankradar-seo --marketplace SteveKinzey/rank-radar-seo-plugin
```

**Claude (chat and Cowork)**: download this repository as a ZIP and add it as a plugin, or install it from Anthropic's plugin directory once it is listed there.

**ChatGPT and Codex**: download this repository as a ZIP and upload it as a personal plugin, or install it from the shared ChatGPT and Codex plugin directory once it is listed there.

One folder serves every host: Claude reads the manifest in the Claude plugin folder, ChatGPT and Codex read the Codex manifest, and both load the same skills.

## How to use it

Ask Claude, for example:

> Run an SEO report on https://example.com/ with mobile and desktop PageSpeed evidence.

To refresh an earlier audit, share the previous report and ask for an update.

## What the plugin runs, sends and fetches

This plugin contains the audit skill, a short get-started skill, two reference documents and one Python helper. It has no hooks, no MCP servers and no background processes.

- **Website requests.** Claude fetches public pages of the site you ask it to audit, using the host's own web tools, at modest request rates and within robots.txt.
- **PageSpeed helper.** `skills/rankradar-seo/scripts/pagespeed.py` uses only Python's standard library. When Claude runs it, it sends the URL being audited to Google's PageSpeed Insights API (`https://www.googleapis.com/pagespeedonline/v5/runPagespeed`) and writes the responses as JSON files in the working directory you are using.
- **Optional API key.** If a `PAGESPEED_API_KEY` environment variable is already set, the helper sends it to that Google endpoint only, to raise the request quota. The key is redacted from everything the helper prints or saves. The helper works without a key.
- **Nothing else.** No data is sent to RankRadar, SK America or any other service. The plugin does not connect to a RankRadar web account.

## Limits

Audits are bounded reviews of a sample of public pages, not exhaustive crawls. Scores are reviewer judgments, not a Google ranking formula, and do not promise rankings, traffic or revenue. Private data such as Search Console, analytics and backlinks is treated as unknown unless you supply it.

## Support

- Website: https://www.rankradarseo.com/integrations
- Support: support@rankradarseo.com
- Privacy: https://www.rankradarseo.com/privacy

## License

Apache-2.0. See [LICENSE](LICENSE).
