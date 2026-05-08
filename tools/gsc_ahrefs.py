"""
GSC keyword and page report via Ahrefs API v3.
Replaces gsc_puller.py — uses Ahrefs GSC integration instead of Google OAuth.

Requires: AHREFS_API_KEY in ~/.env and GSC connected in Ahrefs project settings.

Usage:
  python tools/gsc_ahrefs.py                    # last 30 days
  python tools/gsc_ahrefs.py --days 90          # last 90 days
  python tools/gsc_ahrefs.py --output seo_reports/
"""
import os, sys, argparse, requests
from pathlib import Path
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

AHREFS_API_KEY = os.getenv("AHREFS_API_KEY")
AHREFS_BASE = "https://api.ahrefs.com/v3"
PROJECT_ID = 8898511  # fastrakmobilelab.com

# Keywords to specifically track positions for
TRACKED_KEYWORDS = [
    "mobile phlebotomy atlanta",
    "mobile phlebotomy gwinnett county",
    "in-home blood draw atlanta",
    "mobile blood draw near me",
    "mobile lab services georgia",
    "mobile drug testing atlanta",
    "dna testing at home georgia",
    "home phlebotomy service atlanta",
    "mobile phlebotomy snellville ga",
    "mobile phlebotomy lawrenceville ga",
    "mobile phlebotomist near me",
    "phlebotomist near me",
    "mobile phlebotomy services near me",
    "mobile lab services near me",
    "mobile lab near me",
]


def get_headers():
    if not AHREFS_API_KEY:
        return None
    return {"Authorization": f"Bearer {AHREFS_API_KEY}"}


def fetch_gsc_keywords(days):
    headers = get_headers()
    if not headers:
        print("WARNING: AHREFS_API_KEY not set — skipping GSC pull.", file=sys.stderr)
        return []

    end_date = date.today()
    # Always anchor to 2026-01-01 — that's when GSC data begins for this site.
    # A rolling window misses historical data on low-traffic sites.
    start_date = max(date(2026, 1, 1), end_date - timedelta(days=days))

    try:
        resp = requests.get(
            f"{AHREFS_BASE}/gsc/keywords",
            headers=headers,
            params={
                "project_id": PROJECT_ID,
                "date_from": start_date.isoformat(),
                "date_to": end_date.isoformat(),
                "limit": 100,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("keywords", [])
    except Exception as e:
        print(f"  [WARN] GSC keywords fetch failed: {e}", file=sys.stderr)
        return []


def fetch_gsc_pages(days):
    headers = get_headers()
    if not headers:
        return []

    end_date = date.today()
    start_date = max(date(2026, 1, 1), end_date - timedelta(days=days))

    try:
        resp = requests.get(
            f"{AHREFS_BASE}/gsc/pages",
            headers=headers,
            params={
                "project_id": PROJECT_ID,
                "date_from": start_date.isoformat(),
                "date_to": end_date.isoformat(),
                "limit": 50,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("pages", [])
    except Exception as e:
        print(f"  [WARN] GSC pages fetch failed: {e}", file=sys.stderr)
        return []


def write_report(keywords, pages, days, output_dir):
    today = date.today().isoformat()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"gsc_report_{today}.md"

    kw_lookup = {k["keyword"]: k for k in keywords}

    lines = [
        f"# GSC Report — {today}",
        f"**Period:** last {days} days (via Ahrefs GSC integration)",
        f"**Project:** fastrakmobilelab.com",
        "",
        "## Tracked Keywords",
        "",
        "| Keyword | Clicks | Impressions | CTR | Position |",
        "|---------|--------|-------------|-----|----------|",
    ]

    for kw in TRACKED_KEYWORDS:
        row = kw_lookup.get(kw)
        if row:
            pos = f"{row['position']:.1f}" if row.get("position") else "—"
            ctr = f"{row['ctr']:.1f}%" if row.get("ctr") is not None else "—"
            lines.append(
                f"| {kw} | {row.get('clicks', 0)} | {row.get('impressions', 0)} | {ctr} | {pos} |"
            )
        else:
            lines.append(f"| {kw} | — | — | — | not ranking |")

    lines += [
        "",
        "## All Ranking Keywords",
        "",
        "| Keyword | Clicks | Impressions | CTR | Position | Top URL |",
        "|---------|--------|-------------|-----|----------|---------|",
    ]

    for k in sorted(keywords, key=lambda x: -x.get("impressions", 0)):
        pos = f"{k['position']:.1f}" if k.get("position") else "—"
        ctr = f"{k['ctr']:.1f}%" if k.get("ctr") is not None else "—"
        url = k.get("top_url", "").replace("https://fastrakmobilelab.com", "")
        lines.append(
            f"| {k['keyword']} | {k.get('clicks',0)} | {k.get('impressions',0)} | {ctr} | {pos} | {url} |"
        )

    lines += [
        "",
        "## Pages by Impressions",
        "",
        "| Page | Keywords | Clicks | Impressions | Avg Position |",
        "|------|----------|--------|-------------|--------------|",
    ]

    for p in sorted(pages, key=lambda x: -x.get("impressions", 0)):
        url = p["page"].replace("https://fastrakmobilelab.com", "") or "/"
        pos = f"{p['position']:.1f}" if p.get("position") else "—"
        lines.append(
            f"| {url} | {p.get('keywords_count',0)} | {p.get('clicks',0)} | {p.get('impressions',0)} | {pos} |"
        )

    lines += ["", f"*Generated {today} via Ahrefs GSC integration.*"]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--output", default=".tmp")
    args = parser.parse_args()

    print(f"Fetching GSC data (last {args.days} days) via Ahrefs...")
    keywords = fetch_gsc_keywords(args.days)
    pages = fetch_gsc_pages(args.days)
    print(f"  {len(keywords)} keywords, {len(pages)} pages")

    report_path = write_report(keywords, pages, args.days, args.output)
    print(f"Report written to {report_path}")


if __name__ == "__main__":
    main()
