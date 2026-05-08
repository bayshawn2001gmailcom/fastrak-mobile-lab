"""
Track local directory submission status for fastrakmobilelab.com.
Maintains a JSON data file and outputs a status table to .tmp/directory_status.md.

Usage:
  python tools/directory_tracker.py                         # show status table
  python tools/directory_tracker.py --update "Yelp" submitted
  python tools/directory_tracker.py --update "Healthgrades" live --url "https://healthgrades.com/..."
  python tools/directory_tracker.py --init                  # create fresh data file
"""
import os, sys, argparse, json
from pathlib import Path
from datetime import date

DATA_FILE = Path(".tmp/directory_data.json")
OUTPUT_PATH = Path(".tmp/directory_status.md")

DIRECTORIES = [
    # Healthcare-specific
    {"name": "Healthgrades", "url": "https://www.healthgrades.com/add-provider", "category": "Healthcare", "dr_estimate": 72, "priority": 1},
    {"name": "Zocdoc", "url": "https://www.zocdoc.com/practice/profile", "category": "Healthcare", "dr_estimate": 68, "priority": 1},
    {"name": "WebMD Health Services", "url": "https://health.webmd.com", "category": "Healthcare", "dr_estimate": 91, "priority": 1},
    {"name": "Vitals", "url": "https://www.vitals.com/claim", "category": "Healthcare", "dr_estimate": 60, "priority": 2},
    {"name": "RateMDs", "url": "https://www.ratemds.com/add-doctor/", "category": "Healthcare", "dr_estimate": 55, "priority": 2},
    {"name": "CareDash", "url": "https://www.caredash.com/claim", "category": "Healthcare", "dr_estimate": 48, "priority": 2},
    # Local/general
    {"name": "Google Business Profile", "url": "https://business.google.com", "category": "Local", "dr_estimate": 100, "priority": 1},
    {"name": "Yelp", "url": "https://biz.yelp.com/claim", "category": "Local", "dr_estimate": 93, "priority": 1},
    {"name": "Better Business Bureau", "url": "https://www.bbb.org/business-registration", "category": "Local", "dr_estimate": 87, "priority": 1},
    {"name": "Angi (Angie's List)", "url": "https://pro.angi.com/", "category": "Local", "dr_estimate": 78, "priority": 2},
    {"name": "Thumbtack", "url": "https://www.thumbtack.com/pro/signup", "category": "Local", "dr_estimate": 76, "priority": 2},
    {"name": "Facebook Business", "url": "https://www.facebook.com/pages/create", "category": "Social/Local", "dr_estimate": 100, "priority": 1},
    # GA / Gwinnett specific
    {"name": "Gwinnett Chamber of Commerce", "url": "https://www.gwinnettchamber.org/join/", "category": "Local-GA", "dr_estimate": 45, "priority": 1},
    {"name": "Georgia Secretary of State Business Search", "url": "https://ecorp.sos.ga.gov", "category": "Local-GA", "dr_estimate": 62, "priority": 2},
    {"name": "Snellville Business Directory", "url": "https://www.snellville.org/business", "category": "Local-GA", "dr_estimate": 30, "priority": 3},
    {"name": "Gwinnett County Health Dept Resources", "url": "https://www.gwinnettcounty.com/health", "category": "Local-GA", "dr_estimate": 55, "priority": 2},
    # General citation
    {"name": "Apple Maps Connect", "url": "https://mapsconnect.apple.com", "category": "Maps", "dr_estimate": 100, "priority": 1},
    {"name": "Bing Places", "url": "https://www.bingplaces.com", "category": "Maps", "dr_estimate": 97, "priority": 1},
    {"name": "Foursquare", "url": "https://foursquare.com/add-place", "category": "Local", "dr_estimate": 82, "priority": 3},
    {"name": "Manta", "url": "https://www.manta.com/claim", "category": "Local", "dr_estimate": 68, "priority": 3},
]

VALID_STATUSES = ["not_started", "submitted", "pending_verification", "live", "rejected", "not_applicable"]


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2))


def init_data():
    data = {}
    for d in DIRECTORIES:
        data[d["name"]] = {
            "status": "not_started",
            "listing_url": "",
            "submitted_date": "",
            "notes": "",
        }
    save_data(data)
    print(f"Initialized {len(data)} directories in {DATA_FILE}")


def update_entry(name, status, listing_url=None):
    data = load_data()
    matched = [d["name"] for d in DIRECTORIES if d["name"].lower() == name.lower()]
    if not matched:
        sys.exit(f"Directory '{name}' not found. Check spelling.")
    key = matched[0]
    data.setdefault(key, {"status": "not_started", "listing_url": "", "submitted_date": "", "notes": ""})
    data[key]["status"] = status
    if status in ("submitted", "live", "pending_verification"):
        data[key]["submitted_date"] = date.today().isoformat()
    if listing_url:
        data[key]["listing_url"] = listing_url
    save_data(data)
    print(f"Updated '{key}': status={status}")


def generate_report():
    data = load_data()
    today = date.today().isoformat()

    status_emoji = {
        "not_started": "[ ]",
        "submitted": "[>]",
        "pending_verification": "[~]",
        "live": "[x]",
        "rejected": "[!]",
        "not_applicable": "[-]",
    }

    lines = [
        f"# Directory Submission Status",
        f"**Site:** fastrakmobilelab.com",
        f"**Updated:** {today}",
        "",
        "Legend: `[ ]` not started  `[>]` submitted  `[~]` pending  `[x]` live  `[!]` rejected",
        "",
    ]

    by_category = {}
    for d in DIRECTORIES:
        by_category.setdefault(d["category"], []).append(d)

    live_count = sum(1 for v in data.values() if v.get("status") == "live")
    submitted_count = sum(1 for v in data.values() if v.get("status") in ("submitted", "pending_verification"))
    lines += [
        f"**Live listings:** {live_count} / {len(DIRECTORIES)}",
        f"**In progress:** {submitted_count}",
        "",
    ]

    for category, dirs in sorted(by_category.items()):
        lines.append(f"## {category}")
        lines.append("")
        lines.append("| Status | Directory | DR | Priority | Listing URL |")
        lines.append("|--------|-----------|-----|----------|-------------|")
        for d in sorted(dirs, key=lambda x: x["priority"]):
            entry = data.get(d["name"], {})
            status = entry.get("status", "not_started")
            icon = status_emoji.get(status, "[ ]")
            listing = entry.get("listing_url", "")
            link = f"[view]({listing})" if listing else "—"
            lines.append(f"| {icon} | [{d['name']}]({d['url']}) | {d['dr_estimate']} | P{d['priority']} | {link} |")
        lines.append("")

    lines += [
        "---",
        "",
        "## Next Steps",
        "1. Start with all P1 directories — they have the highest DR and most impact",
        "2. Use the same NAP (Name, Address, Phone) on every listing:",
        "   - Name: Fastrak Mobile Lab",
        "   - Address: [your business address]",
        "   - Phone: [your business phone]",
        "   - Website: https://fastrakmobilelab.com",
        "3. Update this tracker after each submission: `python tools/directory_tracker.py --update \"Yelp\" submitted`",
        "4. Mark as live once the listing is publicly visible",
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Status report written to {OUTPUT_PATH}")
    print(f"Live: {live_count}/{len(DIRECTORIES)}  |  In progress: {submitted_count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Initialize data file with all directories")
    parser.add_argument("--update", nargs=2, metavar=("NAME", "STATUS"), help="Update a directory status")
    parser.add_argument("--url", help="Listing URL (use with --update)")
    args = parser.parse_args()

    if args.init:
        init_data()
        return

    if args.update:
        name, status = args.update
        if status not in VALID_STATUSES:
            sys.exit(f"Invalid status '{status}'. Valid: {', '.join(VALID_STATUSES)}")
        update_entry(name, status, args.url)

    generate_report()


if __name__ == "__main__":
    main()
