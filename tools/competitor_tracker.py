"""
Weekly competitor keyword ranking snapshot for fastrakmobilelab.com.
Uses Ahrefs API (via direct HTTP, not MCP) to pull organic keyword data
for tracked competitors and diff against the previous week's snapshot.

Usage:
  python tools/competitor_tracker.py                     # run snapshot, output to .tmp/
  python tools/competitor_tracker.py --output seo_reports/  # output to seo_reports/
  python tools/competitor_tracker.py --diff              # compare latest two snapshots

Requires: AHREFS_API_KEY in ~/.env (Ahrefs API v3, standard plan or higher)
"""
import os, sys, argparse, requests, json, time
from pathlib import Path
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

AHREFS_API_KEY = os.getenv("AHREFS_API_KEY")
WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")

# Tracked competitors — update as you discover ranking pages
COMPETITORS = [
    "mobiphlebotomy.com",
    "atlantamobilelab.com",
    "homephleb.com",
    "mobilemediq.com",
]

OUR_DOMAIN = "fastrakmobilelab.com"

# Keywords to monitor position on
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

AHREFS_BASE = "https://api.ahrefs.com/v3"


def get_headers():
    if not AHREFS_API_KEY:
        return None
    return {"Authorization": f"Bearer {AHREFS_API_KEY}", "Content-Type": "application/json"}


def fetch_keyword_positions(domain):
    """Fetch top organic keyword rankings for a domain."""
    headers = get_headers()
    if not headers:
        return []

    try:
        resp = requests.get(
            f"{AHREFS_BASE}/site-explorer/organic-keywords",
            headers=headers,
            params={
                "target": domain,
                "mode": "domain",
                "limit": 200,
                "country": "us",
                "select": "keyword,position,volume,traffic,url",
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("keywords", [])
    except Exception as e:
        print(f"  [WARN] Could not fetch keywords for {domain}: {e}", file=sys.stderr)
        return []


def get_position_for_keyword(keywords_data, keyword):
    """Find position for a specific keyword in Ahrefs results."""
    kw_lower = keyword.lower()
    for kw in keywords_data:
        if kw.get("keyword", "").lower() == kw_lower:
            return kw.get("position"), kw.get("volume", 0), kw.get("url", "")
    return None, 0, ""


def build_snapshot():
    """Pull current rankings for all tracked keywords across all domains."""
    today = date.today().isoformat()
    snapshot = {"date": today, "keywords": {}}

    all_domains = [OUR_DOMAIN] + COMPETITORS

    for domain in all_domains:
        print(f"  Fetching rankings for {domain}...")
        kw_data = fetch_keyword_positions(domain)
        time.sleep(0.5)

        for keyword in TRACKED_KEYWORDS:
            pos, vol, url = get_position_for_keyword(kw_data, keyword)
            snapshot["keywords"].setdefault(keyword, {})
            snapshot["keywords"][keyword][domain] = {
                "position": pos,
                "volume": vol,
                "url": url,
            }

    return snapshot


def load_previous_snapshot(output_dir):
    """Find the most recent snapshot file before today."""
    today = date.today()
    for i in range(1, 60):
        check_date = (today - timedelta(days=i)).isoformat()
        candidate = Path(output_dir) / f"competitor_snapshot_{check_date}.json"
        if candidate.exists():
            return json.loads(candidate.read_text()), check_date
    return None, None


def format_report(snapshot, previous_snapshot=None, previous_date=None):
    today = snapshot["date"]
    all_domains = [OUR_DOMAIN] + COMPETITORS

    lines = [
        f"# Competitor Ranking Snapshot — {today}",
        f"**Site:** {OUR_DOMAIN}",
        "",
    ]

    if previous_date:
        lines.append(f"**Compared to:** {previous_date}")
    lines.append("")

    lines += [
        "## Tracked Keyword Positions",
        "",
        f"| Keyword | Vol | {' | '.join(all_domains)} |",
        f"|---------|-----|{'|'.join(['---'] * len(all_domains))}|",
    ]

    our_improvements = []
    competitor_threats = []

    for keyword in TRACKED_KEYWORDS:
        kw_data = snapshot["keywords"].get(keyword, {})
        vol = next((kw_data[d]["volume"] for d in all_domains if kw_data.get(d, {}).get("volume")), "?")

        positions = []
        for domain in all_domains:
            pos = kw_data.get(domain, {}).get("position")
            pos_str = str(pos) if pos else "—"

            if previous_snapshot and domain == OUR_DOMAIN:
                prev_pos = previous_snapshot.get("keywords", {}).get(keyword, {}).get(domain, {}).get("position")
                if prev_pos and pos:
                    delta = prev_pos - pos  # positive = improvement
                    if delta > 0:
                        pos_str += f" (+{delta})"
                        our_improvements.append((keyword, prev_pos, pos, delta))
                    elif delta < 0:
                        pos_str += f" ({delta})"

            if previous_snapshot and domain != OUR_DOMAIN:
                prev_pos = previous_snapshot.get("keywords", {}).get(keyword, {}).get(domain, {}).get("position")
                if prev_pos and pos and (prev_pos - pos) >= 3:
                    competitor_threats.append((keyword, domain, prev_pos, pos))

            positions.append(pos_str)

        lines.append(f"| {keyword} | {vol} | {' | '.join(positions)} |")

    lines.append("")

    if our_improvements:
        lines += ["## Our Improvements This Week", ""]
        for kw, prev, now, delta in sorted(our_improvements, key=lambda x: -x[3]):
            lines.append(f"- **{kw}**: position {prev} -> {now} (+{delta})")
        lines.append("")

    if competitor_threats:
        lines += ["## Competitor Threats (gained 3+ positions)", ""]
        for kw, domain, prev, now in sorted(competitor_threats, key=lambda x: -(x[2]-x[3])):
            lines.append(f"- **{kw}**: {domain} moved from {prev} -> {now} (+{prev-now})")
        lines.append("")

    lines += [
        "---",
        f"*Snapshot generated: {today}*",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=".tmp", help="Output directory for snapshot files")
    parser.add_argument("--diff", action="store_true", help="Compare latest two snapshots only (no API call)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    if args.diff:
        prev_snapshot, prev_date = load_previous_snapshot(args.output)
        # find today's snapshot
        today_file = output_dir / f"competitor_snapshot_{today}.json"
        if not today_file.exists():
            sys.exit("No snapshot for today yet. Run without --diff first.")
        snapshot = json.loads(today_file.read_text())
        report = format_report(snapshot, prev_snapshot, prev_date)
        report_path = output_dir / f"competitor_delta_{today}.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"Diff report written to {report_path}")
        return

    if not AHREFS_API_KEY:
        print("WARNING: AHREFS_API_KEY not set. Generating empty snapshot structure.")
        print("Add AHREFS_API_KEY to ~/.env to enable live data.")
        snapshot = {"date": today, "keywords": {k: {} for k in TRACKED_KEYWORDS}}
    else:
        print(f"Building competitor snapshot for {today}...")
        snapshot = build_snapshot()

    # Save raw snapshot JSON
    snapshot_path = output_dir / f"competitor_snapshot_{today}.json"
    snapshot_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

    # Load previous snapshot for diff
    prev_snapshot, prev_date = load_previous_snapshot(args.output)

    # Write markdown report
    report = format_report(snapshot, prev_snapshot, prev_date)
    report_path = output_dir / f"competitor_delta_{today}.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"Snapshot: {snapshot_path}")
    print(f"Report:   {report_path}")


if __name__ == "__main__":
    main()
