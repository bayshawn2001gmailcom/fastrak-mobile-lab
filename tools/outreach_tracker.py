"""
Track physician/facility partnership outreach for backlink building.
Manages prospect list and follow-up schedule in .tmp/outreach_log.md.

Usage:
  python tools/outreach_tracker.py                              # show status table
  python tools/outreach_tracker.py --add "Dr. Smith Clinic" "drsmith@example.com" physician
  python tools/outreach_tracker.py --update "Dr. Smith Clinic" contacted
  python tools/outreach_tracker.py --update "Dr. Smith Clinic" link_live --url "https://drsmith.com/resources"
  python tools/outreach_tracker.py --due                        # show follow-ups due today
"""
import os, sys, argparse, json
from pathlib import Path
from datetime import date, timedelta

DATA_FILE = Path(".tmp/outreach_data.json")
OUTPUT_PATH = Path(".tmp/outreach_log.md")

VALID_STATUSES = [
    "prospect",       # identified, not yet contacted
    "contacted",      # first outreach sent
    "follow_up_1",    # first follow-up sent (7 days after contact)
    "follow_up_2",    # second follow-up sent (14 days after first)
    "responded",      # they replied positively
    "link_live",      # link is published on their site
    "declined",       # said no
    "no_response",    # no reply after 2 follow-ups
]

PROSPECT_TYPES = ["physician", "urgent_care", "senior_living", "corporate_hr", "other"]

# Starter prospect list — Gwinnett/DeKalb area
STARTER_PROSPECTS = [
    {"name": "Gwinnett Medical Associates", "email": "", "type": "physician", "notes": "Large multi-physician practice in Lawrenceville"},
    {"name": "Northside Hospital Gwinnett", "email": "", "type": "physician", "notes": "Partner resources page on hospital site"},
    {"name": "WellStar Snellville", "email": "", "type": "physician", "notes": "Primary care — near service area center"},
    {"name": "Peachtree Immediate Care Duluth", "email": "", "type": "urgent_care", "notes": "Urgent care chain, may refer overflow lab work"},
    {"name": "Pruitt Health Skilled Nursing (Snellville)", "email": "", "type": "senior_living", "notes": "Skilled nursing — high need for mobile labs"},
    {"name": "Sterling Estates of East Cobb", "email": "", "type": "senior_living", "notes": "Senior living community, residents need regular labs"},
    {"name": "Publix HR (Gwinnett Distribution)", "email": "", "type": "corporate_hr", "notes": "Large employer, drug testing referral opportunity"},
    {"name": "Gwinnett County Public Schools HR", "email": "", "type": "corporate_hr", "notes": "Pre-employment drug screening demand"},
]


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2))


def add_prospect(name, email, prospect_type, notes=""):
    data = load_data()
    if name in data:
        print(f"'{name}' already exists in tracker.")
        return
    data[name] = {
        "email": email,
        "type": prospect_type,
        "status": "prospect",
        "contacted_date": "",
        "last_followup_date": "",
        "link_url": "",
        "notes": notes,
    }
    save_data(data)
    print(f"Added prospect: {name}")


def update_status(name, status, link_url=None):
    data = load_data()
    if name not in data:
        sys.exit(f"Prospect '{name}' not found. Add it first with --add.")
    data[name]["status"] = status
    today = date.today().isoformat()
    if status == "contacted":
        data[name]["contacted_date"] = today
    elif status in ("follow_up_1", "follow_up_2"):
        data[name]["last_followup_date"] = today
    if link_url:
        data[name]["link_url"] = link_url
    save_data(data)
    print(f"Updated '{name}': status={status}")


def get_follow_ups_due():
    data = load_data()
    today = date.today()
    due = []
    for name, entry in data.items():
        status = entry.get("status")
        contacted = entry.get("contacted_date", "")
        last_followup = entry.get("last_followup_date", "")

        if status == "contacted" and contacted:
            contact_date = date.fromisoformat(contacted)
            if (today - contact_date).days >= 7:
                due.append((name, "follow_up_1 due", contacted))

        elif status == "follow_up_1" and last_followup:
            followup_date = date.fromisoformat(last_followup)
            if (today - followup_date).days >= 7:
                due.append((name, "follow_up_2 due", last_followup))
    return due


def generate_report(data):
    today = date.today().isoformat()
    status_emoji = {
        "prospect": "[ ]",
        "contacted": "[>]",
        "follow_up_1": "[~]",
        "follow_up_2": "[~~]",
        "responded": "[+]",
        "link_live": "[x]",
        "declined": "[-]",
        "no_response": "[/]",
    }

    by_type = {}
    for name, entry in data.items():
        t = entry.get("type", "other")
        by_type.setdefault(t, []).append((name, entry))

    lines = [
        f"# Outreach Tracker — Physician & Facility Link Building",
        f"**Site:** fastrakmobilelab.com",
        f"**Updated:** {today}",
        "",
        "Legend: `[ ]` prospect  `[>]` contacted  `[~]` follow-up sent  `[x]` link live  `[-]` declined",
        "",
    ]

    live = sum(1 for e in data.values() if e.get("status") == "link_live")
    active = sum(1 for e in data.values() if e.get("status") in ("contacted", "follow_up_1", "follow_up_2", "responded"))
    lines += [
        f"**Links live:** {live}  |  **Active outreach:** {active}  |  **Total prospects:** {len(data)}",
        "",
    ]

    due = get_follow_ups_due()
    if due:
        lines += ["## Follow-Ups Due", ""]
        for name, action, since in due:
            lines.append(f"- **{name}** — {action} (last contact: {since})")
        lines.append("")

    type_labels = {
        "physician": "Physician Offices",
        "urgent_care": "Urgent Care",
        "senior_living": "Senior Living",
        "corporate_hr": "Corporate HR",
        "other": "Other",
    }

    for ptype in PROSPECT_TYPES:
        prospects = by_type.get(ptype, [])
        if not prospects:
            continue
        lines.append(f"## {type_labels.get(ptype, ptype)}")
        lines.append("")
        lines.append("| Status | Name | Email | Link |")
        lines.append("|--------|------|-------|------|")
        for name, entry in sorted(prospects, key=lambda x: x[1].get("status", "")):
            icon = status_emoji.get(entry.get("status", "prospect"), "[ ]")
            email = entry.get("email", "—") or "—"
            link_url = entry.get("link_url", "")
            link = f"[live]({link_url})" if link_url else "—"
            lines.append(f"| {icon} | {name} | {email} | {link} |")
            if entry.get("notes"):
                lines.append(f"|   | *{entry['notes']}* | | |")
        lines.append("")

    lines += [
        "---",
        "",
        "## Outreach Template (copy-paste)",
        "",
        "**Subject:** Partnership Opportunity — Mobile Lab Services for Your Patients",
        "",
        "Hi [Name],",
        "",
        "I'm reaching out from Fastrak Mobile Lab, a licensed mobile phlebotomy service serving Gwinnett County and metro Atlanta. We provide in-home blood draws, drug testing, and DNA specimen collection for patients who can't travel to a traditional lab.",
        "",
        "Many of our clients are referred by physician offices and senior living facilities in the area. I'd love to explore whether listing us on your patient resources page might be a good fit for your community.",
        "",
        "We handle all logistics, insurance billing, and result delivery. Happy to set up a quick call if you'd like to learn more.",
        "",
        "Best,  ",
        "[Your name]  ",
        "Fastrak Mobile Lab  ",
        "https://fastrakmobilelab.com  ",
        "[Phone]",
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Outreach log written to {OUTPUT_PATH}")
    print(f"Links live: {live} | Active: {active} | Follow-ups due: {len(due)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", nargs=3, metavar=("NAME", "EMAIL", "TYPE"),
                        help="Add a new prospect")
    parser.add_argument("--update", nargs=2, metavar=("NAME", "STATUS"),
                        help="Update prospect status")
    parser.add_argument("--url", help="Link URL (use with --update link_live)")
    parser.add_argument("--due", action="store_true", help="Show follow-ups due today")
    parser.add_argument("--init-starters", action="store_true",
                        help="Load starter prospect list")
    args = parser.parse_args()

    if args.init_starters:
        data = load_data()
        added = 0
        for p in STARTER_PROSPECTS:
            if p["name"] not in data:
                data[p["name"]] = {
                    "email": p["email"],
                    "type": p["type"],
                    "status": "prospect",
                    "contacted_date": "",
                    "last_followup_date": "",
                    "link_url": "",
                    "notes": p["notes"],
                }
                added += 1
        save_data(data)
        print(f"Added {added} starter prospects.")

    if args.add:
        name, email, ptype = args.add
        if ptype not in PROSPECT_TYPES:
            sys.exit(f"Invalid type '{ptype}'. Valid: {', '.join(PROSPECT_TYPES)}")
        add_prospect(name, email, ptype)

    if args.update:
        name, status = args.update
        if status not in VALID_STATUSES:
            sys.exit(f"Invalid status '{status}'. Valid: {', '.join(VALID_STATUSES)}")
        update_status(name, status, args.url)

    if args.due:
        due = get_follow_ups_due()
        if due:
            print("Follow-ups due:")
            for name, action, since in due:
                print(f"  {name} — {action} (since {since})")
        else:
            print("No follow-ups due today.")
        return

    generate_report(load_data())


if __name__ == "__main__":
    main()
