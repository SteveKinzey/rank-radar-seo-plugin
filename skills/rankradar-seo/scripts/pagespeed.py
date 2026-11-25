#!/usr/bin/env python3
"""Collect official PageSpeed API evidence without inventing missing results."""

import argparse
import datetime as dt
import json
import math
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CATEGORIES = ("performance", "accessibility", "best-practices", "seo")
METRICS = (
    "first-contentful-paint", "largest-contentful-paint", "total-blocking-time",
    "cumulative-layout-shift", "speed-index",
)


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def redact(value, key=None):
    """Redact credentials before serialization, including reflected URL encoding."""
    key = key if key is not None else os.environ.get("PAGESPEED_API_KEY")
    if not key:
        return value
    variants = sorted({key, urllib.parse.quote(key, safe=""),
                       urllib.parse.quote_plus(key)}, key=len, reverse=True)
    if isinstance(value, str):
        for variant in variants:
            value = value.replace(variant, "[REDACTED]")
        return value
    if isinstance(value, list):
        return [redact(item, key) for item in value]
    if isinstance(value, dict):
        return {redact(name, key): redact(item, key) for name, item in value.items()}
    return value


def number(value):
    if isinstance(value, bool):
        return False
    return isinstance(value, int) or (isinstance(value, float) and math.isfinite(value))


def score(value):
    return number(value) and 0 <= value <= 1


def object_or_none(value):
    return value if isinstance(value, dict) else None


def string_or_none(value):
    return value if isinstance(value, str) else None


def summarize(payload, strategy, target, status=200, captured_at_utc=None):
    """Availability means a usable Performance score; other valid lab data survives."""
    if not isinstance(payload, dict):
        payload = {"error": {"message": "Non-object API response"}}
    raw_lh = payload.get("lighthouseResult")
    lh = raw_lh if isinstance(raw_lh, dict) else {}
    api_error = payload.get("error")
    runtime_error = lh.get("runtimeError")
    failed = status != 200 or api_error is not None or runtime_error is not None
    error = api_error if api_error is not None else runtime_error
    if failed and error is None:
        error = {"message": "Unsuccessful HTTP response"}
    if not failed and not isinstance(raw_lh, dict):
        failed = True
        error = {"message": "Missing or malformed lighthouseResult"}

    categories = {}
    metrics = {}
    opportunities = []
    if not failed:
        raw_categories = lh.get("categories")
        if isinstance(raw_categories, dict):
            for name in CATEGORIES:
                category = raw_categories.get(name)
                if isinstance(category, dict) and score(category.get("score")):
                    categories[name] = category["score"] * 100
        audits = lh.get("audits")
        if isinstance(audits, dict):
            for name in METRICS:
                audit = audits.get(name)
                if not isinstance(audit, dict) or not number(audit.get("numericValue")):
                    continue
                if audit["numericValue"] < 0:
                    continue
                metrics[name] = {"numericValue": audit["numericValue"]}
                for field in ("numericUnit", "displayValue"):
                    if isinstance(audit.get(field), str):
                        metrics[name][field] = audit[field]
            for name, audit in audits.items():
                if not isinstance(audit, dict) or not score(audit.get("score")) or audit["score"] == 1:
                    continue
                details = object_or_none(audit.get("details")) or {}
                if details.get("type") != "opportunity" and not name.endswith("-insight"):
                    continue
                item = {"id": name}
                for field in ("title", "displayValue"):
                    if isinstance(audit.get(field), str):
                        item[field] = audit[field]
                for field in ("overallSavingsMs", "overallSavingsBytes"):
                    if number(details.get(field)) and details[field] >= 0:
                        item[field] = details[field]
                opportunities.append(item)

    available = not failed and "performance" in categories
    if not failed and not available:
        error = {"message": "Performance score unavailable or invalid; other valid results retained"}
    warnings = lh.get("runWarnings")
    return {
        "strategy": strategy, "requested_url": target, "http_status": status,
        "captured_at_utc": captured_at_utc or utc_now(), "available": available,
        "fetch_time": string_or_none(lh.get("fetchTime")) or string_or_none(payload.get("analysisUTCTimestamp")),
        "final_url": string_or_none(lh.get("finalDisplayedUrl")) or string_or_none(lh.get("finalUrl")),
        "lighthouse_version": string_or_none(lh.get("lighthouseVersion")),
        "configuration": object_or_none(lh.get("configSettings")),
        "environment": object_or_none(lh.get("environment")),
        "run_warnings": [item for item in warnings if isinstance(item, str)] if isinstance(warnings, list) else [],
        "error": error, "category_scores": categories, "lab_metrics": metrics,
        "field_url": object_or_none(payload.get("loadingExperience")) if not failed else None,
        "field_origin": object_or_none(payload.get("originLoadingExperience")) if not failed else None,
        "opportunities": opportunities,
    }


def write_json(path, value):
    # Exclusive creation also prevents overwriting evidence if another process races us.
    with path.open("x", encoding="utf-8") as handle:
        json.dump(redact(value), handle, indent=2, allow_nan=False)
        handle.write("\n")


def reject_constant(_value):
    raise ValueError("Non-finite JSON number")


def finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Non-finite JSON number")
    return result


def run(target, strategy, out, timeout):
    params = [("url", target), ("strategy", strategy)]
    params.extend(("category", category) for category in CATEGORIES)
    key = os.environ.get("PAGESPEED_API_KEY")
    if key:
        params.append(("key", key))
    request = urllib.request.Request(
        ENDPOINT + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "RankRadar-PageSpeed/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status, body = response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read().decode("utf-8", errors="replace")
    except Exception as exc:
        # Exception messages and request URLs may contain a credential.
        status, body = 0, json.dumps({"error": {"message": type(exc).__name__}})
    captured_at_utc = utc_now()
    try:
        payload = json.loads(body, parse_constant=reject_constant, parse_float=finite_float)
        if not isinstance(payload, dict):
            payload = {"error": {"message": "Non-object API response"}}
    except (ValueError, RecursionError):
        payload = {"error": {"message": "Invalid JSON API response"}}
    payload = redact(payload, key)
    write_json(out / (strategy + "-raw.json"), payload)
    return redact(summarize(payload, strategy, target, status, captured_at_utc), key)


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        super().error(redact(message))


def main(argv=None):
    parser = SafeParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--strategy", choices=("both", "mobile", "desktop"), default="both")
    parser.add_argument("--timeout", type=int, default=130)
    args = parser.parse_args(argv)
    try:
        parsed = urllib.parse.urlsplit(args.url)
        valid = parsed.scheme in ("https", "http") and parsed.hostname and not parsed.username and not parsed.password
    except ValueError:
        valid = False
    if not valid:
        parser.error("Provide an HTTP(S) URL without embedded credentials.")
    if args.timeout < 1:
        parser.error("Timeout must be positive.")
    out = args.out or Path("work") / ("pagespeed-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    try:
        if out.exists() and (any(out.glob("*-raw.json")) or (out / "summary.json").exists()):
            parser.error("The output directory already contains audit evidence; choose a new --out directory.")
        out.mkdir(parents=True, exist_ok=True)
        print("Evidence directory:", redact(str(out)))
        strategies = ("mobile", "desktop") if args.strategy == "both" else (args.strategy,)
        results = [run(args.url, strategy, out, args.timeout) for strategy in strategies]
        write_json(out / "summary.json", {
            "collected_at_utc": utc_now(), "source": "Google PageSpeed Insights API v5", "results": results,
        })
    except (OSError, ValueError, RecursionError) as exc:
        print("Could not save PageSpeed evidence (" + type(exc).__name__ + ").", file=sys.stderr)
        return 2
    for result in results:
        print(result["strategy"], "HTTP", result["http_status"], "performance", result["category_scores"].get("performance", "unavailable"))
    if not all(result["available"] for result in results):
        print("Some tests are unavailable; try the official PageSpeed website. See summary.json for details.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
