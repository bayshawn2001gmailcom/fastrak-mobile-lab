"""
Generate a Google Business Profile optimization checklist for fastrakmobilelab.com.
Outputs an actionable audit to .tmp/gbp_audit.md.

Usage:
  python tools/gbp_checklist.py
"""
import os
from pathlib import Path
from datetime import date

OUTPUT_PATH = Path(".tmp/gbp_audit.md")

CHECKLIST = {
    "Business Info": [
        ("Business name matches exactly: 'Fastrak Mobile Lab'", False),
        ("Primary category set: 'Medical Laboratory'", False),
        ("Additional categories added (up to 9):\n"
         "  - Blood Testing Service\n"
         "  - Drug Testing Service\n"
         "  - DNA Testing Service\n"
         "  - Medical Diagnostic Imaging Center\n"
         "  - Home Health Care Service\n"
         "  - Phlebotomist", False),
        ("Service area set to 30-mile radius from ZIP 30039 (Snellville, GA)", False),
        ("Phone number added and verified", False),
        ("Website URL: https://fastrakmobilelab.com", False),
        ("Business description written (750 char max, includes primary keywords)", False),
        ("Opening hours set (or marked as 'By appointment')", False),
        ("Attributes filled: 'Appointment required', 'Identifies as Black-owned' (if applicable)", False),
    ],
    "Photos": [
        ("Cover photo: professional team or equipment photo", False),
        ("Logo uploaded (use Brand_assets/logo.png)", False),
        ("At least 5 interior/team/equipment photos added", False),
        ("At least 2 exterior/vehicle photos added (if applicable)", False),
        ("Photos geotagged before upload (use GeoImgr or similar)", False),
    ],
    "Services": [
        ("Service: Mobile Phlebotomy — added with description and price range", False),
        ("Service: Mobile Drug Testing — added with description", False),
        ("Service: DNA Specimen Collection — added with description", False),
        ("Service: Corporate Lab Services — added with description", False),
        ("Service: Senior/Homebound Lab Services — added with description", False),
    ],
    "Q&A": [
        ("Q: Do you come to my home? A: Yes, we travel to you anywhere in Gwinnett County and metro Atlanta.", False),
        ("Q: Do you accept insurance? A: We accept most major insurance plans. Contact us to verify coverage.", False),
        ("Q: How do I schedule a mobile blood draw? A: Call us or book online at fastrakmobilelab.com.", False),
        ("Q: How fast do I get results? A: Most results are available within 24-72 hours.", False),
        ("Q: Are your phlebotomists licensed? A: Yes, all staff are certified and licensed in Georgia.", False),
    ],
    "Posts": [
        ("Weekly GBP post scheduled (use 'What's New' type, include CTA and link)", False),
        ("First post published introducing mobile phlebotomy service", False),
        ("Event post added for any upcoming health fair or community event", False),
    ],
    "Reviews": [
        ("Review response template created for 5-star reviews", False),
        ("Review response template created for negative reviews", False),
        ("QR code or link created for easy review requests to send clients", False),
    ],
}


def generate_checklist():
    today = date.today().isoformat()
    lines = [
        f"# Google Business Profile Optimization Checklist",
        f"**Site:** fastrakmobilelab.com",
        f"**Generated:** {today}",
        f"**GBP URL:** https://business.google.com (sign in to manage)",
        "",
        "Mark each item as complete as you work through it.",
        "Priority order: Business Info -> Photos -> Services -> Q&A -> Posts -> Reviews",
        "",
    ]

    total = 0
    for section, items in CHECKLIST.items():
        lines.append(f"## {section}")
        lines.append("")
        for task, done in items:
            checkbox = "[x]" if done else "[ ]"
            lines.append(f"- {checkbox} {task}")
            total += 1
        lines.append("")

    lines += [
        "---",
        "",
        f"**Total items:** {total}",
        "",
        "## Why This Matters",
        "",
        "- Fully optimized GBP is the fastest path to appearing in the **local 3-pack** for searches like 'mobile phlebotomy near me'",
        "- Google uses GBP data as a trust signal — it's effectively a backlink from Google itself",
        "- Q&A seeds show up in search results and reduce bounce from uncertain patients",
        "- Weekly posts signal to Google that the business is active",
        "",
        "## After Completing",
        "Feed the verified GBP URL into `workflows/link_building_directories.md` as the anchor citation for all directory submissions.",
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"GBP checklist written to {OUTPUT_PATH}")
    print(f"Open it and work through {total} items to fully optimize the profile.")


if __name__ == "__main__":
    generate_checklist()
