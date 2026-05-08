"""
Google Search Console data puller for fastrakmobilelab.com.
Pulls weekly clicks, impressions, and average position for tracked keywords.

STATUS: Stub — requires GSC to be connected first.

Prerequisites (manual steps):
  1. Go to https://search.google.com/search-console and add https://fastrakmobilelab.com
  2. Verify ownership via HTML tag (add to WordPress header via Rank Math > General Settings > Webmaster Tools)
  3. Submit sitemap: https://fastrakmobilelab.com/sitemap_index.xml
  4. Enable Google Search Console API in Google Cloud Console
  5. Create OAuth credentials (Desktop app type), download as credentials.json
  6. Place credentials.json in this project root
  7. Run this script once to complete OAuth flow — token.json will be created

Usage (once prerequisites are done):
  python tools/gsc_puller.py                    # pull last 7 days
  python tools/gsc_puller.py --days 30          # pull last 30 days
  python tools/gsc_puller.py --output seo_reports/
"""
import os, sys, argparse, json
from pathlib import Path
from datetime import date, timedelta

CREDENTIALS_FILE = Path("credentials.json")
TOKEN_FILE = Path("token.json")
OUTPUT_DIR = Path(".tmp")

SITE_URL = "https://fastrakmobilelab.com/"

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
]


def check_prerequisites():
    missing = []
    if not CREDENTIALS_FILE.exists():
        missing.append("credentials.json (Google OAuth credentials file)")
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        missing.append("pip install google-auth-oauthlib google-api-python-client")
    return missing


def get_gsc_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    return build("searchconsole", "v1", credentials=creds)


def fetch_keyword_data(service, keyword, days=7):
    end_date = date.today() - timedelta(days=3)  # GSC has ~3 day lag
    start_date = end_date - timedelta(days=days)

    body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["query"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "query",
                "operator": "equals",
                "expression": keyword,
            }]
        }],
        "rowLimit": 10,
    }

    try:
        resp = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
        rows = resp.get("rows", [])
        if rows:
            row = rows[0]
            return {
                "keyword": keyword,
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0) * 100, 1),
                "position": round(row.get("position", 0), 1),
            }
    except Exception as e:
        print(f"  [WARN] GSC query failed for '{keyword}': {e}", file=sys.stderr)

    return {"keyword": keyword, "clicks": 0, "impressions": 0, "ctr": 0.0, "position": None}


def write_report(rows, days, output_dir):
    today = date.today().isoformat()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"gsc_weekly_{today}.md"

    lines = [
        f"# GSC Weekly Report — {today}",
        f"**Site:** {SITE_URL}",
        f"**Period:** last {days} days",
        "",
        "| Keyword | Clicks | Impressions | CTR | Avg Position |",
        "|---------|--------|-------------|-----|--------------|",
    ]

    for row in sorted(rows, key=lambda r: -r["impressions"]):
        pos = str(row["position"]) if row["position"] else "—"
        lines.append(f"| {row['keyword']} | {row['clicks']} | {row['impressions']} | {row['ctr']}% | {pos} |")

    lines += [
        "",
        f"*Data from Google Search Console. Generated {today}.*",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7, help="Days of data to pull (default: 7)")
    parser.add_argument("--output", default=".tmp", help="Output directory")
    args = parser.parse_args()

    missing = check_prerequisites()
    if missing:
        print("GSC not yet configured. Complete these steps first:")
        for step in missing:
            print(f"  - {step}")
        print()
        print("See workflow: workflows/gsc_setup.md (when created) for full instructions.")
        sys.exit(0)

    print(f"Connecting to Google Search Console...")
    service = get_gsc_service()

    print(f"Fetching keyword data for last {args.days} days...")
    rows = []
    for keyword in TRACKED_KEYWORDS:
        row = fetch_keyword_data(service, keyword, args.days)
        rows.append(row)
        print(f"  {keyword}: {row['clicks']} clicks, pos {row['position']}")

    report_path = write_report(rows, args.days, args.output)
    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()
