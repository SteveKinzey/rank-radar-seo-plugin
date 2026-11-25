# PageSpeed evidence

## Collect a run

Use Google's official [PageSpeed Insights website](https://pagespeed.web.dev/) or [API](https://developers.google.com/speed/docs/insights/v5/get-started) for the homepage on mobile and desktop. HTTP response timing is not a Lighthouse Performance score. Test additional representative templates when the user requests them and the tools support it.

When Python 3 and outbound HTTP access are available, resolve `scripts/pagespeed.py` relative to the actual loaded skill directory and run:

```bash
python3 "<skill-dir>/scripts/pagespeed.py" "https://example.com/" --out "<work-dir>/pagespeed-<timestamp>"
```

The helper uses Python's standard library, defaults to both devices, and supports `--strategy mobile`, `--strategy desktop`, and `--timeout SECONDS`. It reads an optional `PAGESPEED_API_KEY` from the environment; do not print the key or put it in report links. An existing configured key is optional, not a prerequisite for starting the audit.

It writes per-device `mobile-raw.json` / `desktop-raw.json` plus `summary.json`, retains unavailable results as errors/unknowns, and refuses to overwrite existing audit evidence. Inspect the raw response for details omitted from the summary. Exit code 0 means all requested Performance runs were available; code 2 means unavailable results, invalid CLI usage, or a file-save failure. File presence alone does not establish a successful test. Use a fresh evidence directory for a new run and preserve earlier capture times.

## Failure and fallback

The helper makes one request per selected device and does not retry internally. For a transient failure, allow at most one retry of that failed device. For quota/authentication failures, use the official website when an interactive browser is available: run Analyze and inspect the completed mobile and desktop tabs. Do not retry indefinitely, rotate keys, or change accounts to bypass a limit.

If the website cannot be used, give the user the official test page and request result links or exports while completing the independent review. Mark missing measurements unavailable. A test/retest URL starts another run; label it as such and do not call it a saved analysis report. Record a run-specific result link only when one was actually obtained.

## Record and interpret

For each device record target and final URLs, capture time with timezone, analysis/fetch time, source or saved result link, Lighthouse version, configuration/throttling, and warnings where exposed.

| Evidence | Record when supplied |
|---|---|
| Lab categories | Performance, Accessibility, Best Practices, Lighthouse SEO |
| Lab metrics | FCP, LCP, TBT, CLS, Speed Index, with numeric precision and units |
| Field data | CrUX availability, URL versus origin scope, device, collection period, field LCP/INP/CLS |

Preserve missing fields as unknown. PSI API field data may be absent; Google's [API guide](https://developers.google.com/speed/docs/insights/v5/get-started) describes its planned removal. Use available official PSI/CrUX evidence when needed; otherwise disclose the gap. Missing CrUX data is not a website failure, and a field collection period cannot be inferred from the Lighthouse run timestamp.

TBT is not INP. Lab measurements cannot establish a real-user Core Web Vitals pass. Lighthouse SEO is a limited automated technical check, separate from this audit's SEO health score. Findings apply to the tested page and run; keep lab and field results, devices, and URL/origin scopes distinct.

Explain bottlenecks using observed diagnostics and affected resources. Keep measured durations separate from estimated savings. Savings may overlap; do not add them into a promised speed gain. Verify current performance bands and thresholds against official documentation before interpreting them:

- [Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)
- [Core Web Vitals](https://web.dev/articles/vitals)
- [PageSpeed API response fields](https://developers.google.com/speed/docs/insights/v5/reference/pagespeedapi/runpagespeed)
