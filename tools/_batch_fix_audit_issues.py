"""
Batch fix for pre-existing page audit issues:
  1. Brand: FASTRAK -> Fastrak Mobile Lab
  2. Pillar link added to all pages missing it
  3. FAQ sections added to 400+ word pages missing them
Run: python tools/_batch_fix_audit_issues.py
"""
import os, sys, base64, requests, re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Missing WP credentials")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H_JSON = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
H_FORM = {"Authorization": f"Basic {creds}"}

PILLAR_URL    = f"{WP_SITE}/at-home-blood-draw-service/"
PILLAR_MARKER = "<!-- fastrak-pillar-link -->"
FAQ_MARKER    = "<!-- fastrak-faq -->"
BOOKING_URL   = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"

# ---------------------------------------------------------------------------
# Per-page metadata: city zip codes + FAQ content
# ---------------------------------------------------------------------------
PAGE_META = {
    # --- City pages ---
    1250: {
        "city": "Duluth", "zips": "30096 and 30097",
        "faq": [
            ("Do you accept insurance for mobile blood draws in Duluth, GA?",
             "Lab processing fees are billed to most major insurance plans including Aetna, BlueCross BlueShield, Cigna, and UnitedHealthcare. The mobile convenience fee covering travel to your Duluth location is a separate out-of-pocket charge. We'll provide a full cost breakdown before you confirm."),
            ("How quickly can you come to Duluth?",
             "Most appointments are available within 24–48 hours. Same-day scheduling is available for urgent needs. We serve all of Duluth including zip codes 30096 and 30097 with early-morning and evening slots."),
            ("Can I get DNA or paternity testing at home in Duluth, GA?",
             "Yes. We offer at-home DNA specimen collection for personal-knowledge and court-admissible paternity testing throughout Duluth, GA. All collections follow strict chain-of-custody procedures with complete confidentiality."),
        ],
    },
    1256: {
        "city": "Lawrenceville", "zips": "30043, 30044, 30045, and 30046",
        "faq": [
            ("Do you accept insurance for mobile blood draws in Lawrenceville, GA?",
             "Lab processing fees are billed to most major insurance plans. The mobile travel fee is a separate out-of-pocket charge. We provide transparent pricing before you confirm your appointment."),
            ("How soon can you arrive in Lawrenceville?",
             "Most appointments are available within 24–48 hours across Lawrenceville zip codes 30043, 30044, 30045, and 30046. Same-day availability is possible depending on service type."),
            ("Is DNA testing available at home in Lawrenceville, GA?",
             "Yes — we offer discreet at-home DNA and paternity specimen collection throughout Lawrenceville with strict chain-of-custody handling for both personal and court-admissible results."),
        ],
    },
    1260: {
        "city": "Tucker", "zips": "30084",
        "faq": [
            ("Do you accept insurance for at-home blood draws in Tucker, GA?",
             "Lab processing fees are covered by most major insurance plans. The mobile service fee for travel to your Tucker location is a separate out-of-pocket charge — we'll give you a full breakdown upfront."),
            ("How quickly can you come to Tucker?",
             "Most Tucker appointments are available within 24–48 hours in zip code 30084. Early-morning and evening slots are offered to fit your schedule."),
            ("Can I get DNA testing done at home in Tucker, GA?",
             "Yes. We perform at-home DNA and paternity specimen collection throughout Tucker with complete confidentiality and chain-of-custody compliance for both personal and legal use."),
        ],
    },
    1261: {
        "city": "Conyers", "zips": "30012, 30013, and 30094",
        "faq": [
            ("Do you accept insurance for mobile blood draws in Conyers, GA?",
             "Lab processing fees are billed to most major insurance plans. The mobile convenience fee for travel to your Conyers address is a separate charge. We provide full pricing transparency before booking."),
            ("How quickly can you come to Conyers?",
             "Most appointments in Conyers are available within 24–48 hours across zip codes 30012, 30013, and 30094, with early-morning and evening availability."),
            ("Is at-home DNA testing available in Conyers, GA?",
             "Yes — we offer discreet at-home DNA and paternity specimen collection throughout Conyers with strict chain-of-custody procedures for both personal and court-admissible results."),
        ],
    },
    1329: {
        "city": "Stone Mountain", "zips": "30083, 30087, and 30088",
        "faq": [
            ("Do you accept insurance for mobile blood draws in Stone Mountain, GA?",
             "Lab fees are billed to most major insurance plans. The mobile travel fee to your Stone Mountain address is a separate out-of-pocket charge — we'll explain full pricing before you book."),
            ("How quickly can you arrive in Stone Mountain?",
             "Most appointments are available within 24–48 hours across Stone Mountain zip codes 30083, 30087, and 30088, including early-morning and evening slots."),
            ("Can I get DNA testing done at home in Stone Mountain, GA?",
             "Yes. We offer at-home DNA and paternity specimen collection throughout Stone Mountain with complete confidentiality and chain-of-custody compliance."),
        ],
    },
    1330: {
        "city": "Avondale Estates", "zips": "30002",
        "faq": [
            ("Do you accept insurance for at-home blood draws in Avondale Estates, GA?",
             "Lab processing fees are covered by most major plans. The mobile travel fee to your Avondale Estates address is a separate charge — we'll give you a full cost breakdown before confirming."),
            ("How quickly can you come to Avondale Estates?",
             "Most appointments in the 30002 zip code are available within 24–48 hours. We offer flexible early-morning and evening scheduling."),
            ("Is DNA testing available at home in Avondale Estates, GA?",
             "Yes — we offer at-home DNA and paternity specimen collection throughout Avondale Estates with strict chain-of-custody handling and full confidentiality."),
        ],
    },
    1331: {
        "city": "Smyrna", "zips": "30080 and 30082",
        "faq": [
            ("Do you accept insurance for mobile blood draws in Smyrna, GA?",
             "Lab fees are billed to most major insurance plans. The mobile convenience fee for travel to your Smyrna location is a separate out-of-pocket charge. Pricing is provided upfront."),
            ("How quickly can you come to Smyrna?",
             "Most Smyrna appointments are available within 24–48 hours across zip codes 30080 and 30082, with early-morning and evening options."),
            ("Can I get DNA testing at home in Smyrna, GA?",
             "Yes. We offer discreet at-home DNA and paternity specimen collection throughout Smyrna with strict chain-of-custody compliance for personal and court-admissible results."),
        ],
    },
    # --- Service pages ---
    1262: {
        "city": None, "zips": None,
        "faq": [
            ("Is mobile drug testing in Gwinnett County court-admissible?",
             "Yes. Our chain-of-custody collections follow federal and state guidelines for legally defensible results. We provide proper documentation for pre-employment, legal proceedings, and compliance programs."),
            ("What drug tests do you offer in Gwinnett County?",
             "We offer urine, oral fluid (saliva), and hair follicle drug testing panels ranging from 5-panel to 12-panel. We serve employers, HR teams, and individuals throughout Gwinnett County."),
            ("How quickly are drug test results available in Gwinnett County?",
             "Negative results are typically returned within 24–48 hours. Non-negative results go through MRO (Medical Review Officer) review which may take 2–5 business days."),
        ],
    },
    1263: {
        "city": None, "zips": None,
        "faq": [
            ("Is at-home DNA testing in Gwinnett County court-admissible?",
             "Yes — we offer both personal-knowledge and court-admissible DNA testing. Legal collections follow strict chain-of-custody procedures with proper documentation for court submission."),
            ("How long do DNA test results take in Gwinnett County?",
             "Most DNA test results are returned within 3–5 business days after specimen processing begins at our accredited partner laboratory."),
            ("Can you collect DNA specimens from multiple people at different locations in Gwinnett County?",
             "Yes. We can coordinate collections from parties at different addresses — useful when testing parties live in different parts of Gwinnett County or metro Atlanta."),
        ],
    },
    1356: {
        "city": None, "zips": None,
        "faq": [
            ("Is mobile drug testing in Atlanta court-admissible?",
             "Yes. Our collections follow federal DOT and non-DOT chain-of-custody protocols, producing legally defensible results accepted by courts, employers, and regulatory bodies throughout Georgia."),
            ("What types of drug tests do you offer in Atlanta?",
             "We offer urine, oral fluid, and hair follicle panels (5-panel, 10-panel, 12-panel) for individuals, employers, legal matters, and compliance programs across Atlanta and metro area."),
            ("How fast are mobile drug test results in Atlanta?",
             "Negative results are typically returned within 24–48 hours. Non-negative specimens go through MRO review, typically completed within 2–5 business days."),
        ],
    },
    1357: {
        "city": None, "zips": None,
        "faq": [
            ("Is at-home DNA testing in Georgia court-admissible?",
             "Yes — we offer both personal-knowledge and court-admissible DNA testing statewide. Legal collections include full chain-of-custody documentation required for Georgia court proceedings."),
            ("How long do at-home DNA test results take in Georgia?",
             "Results are typically returned within 3–5 business days after the lab receives your specimen. We work with AABB-accredited laboratories for all DNA testing."),
            ("Do you travel anywhere in Georgia for DNA specimen collection?",
             "We primarily serve metro Atlanta and Gwinnett County. Contact us to confirm availability at your Georgia address — we accommodate many areas outside the immediate metro."),
        ],
    },
    1358: {
        "city": None, "zips": None,
        "faq": [
            ("What corporate mobile lab services do you offer in Atlanta?",
             "We provide on-site drug testing, pre-employment panels, DOT compliance testing, annual wellness screenings, and phlebotomy services for businesses throughout metro Atlanta — all at your office location."),
            ("How quickly can you schedule on-site testing for our Atlanta office?",
             "Most corporate appointments are available within 24–48 hours. For large-scale screenings, we recommend booking 3–5 days in advance to coordinate logistics."),
            ("Is corporate drug testing legally compliant in Georgia?",
             "Yes. All testing follows Georgia state law and applicable federal regulations (DOT, SAMHSA). We provide full chain-of-custody documentation and work with certified MROs for non-negative results."),
        ],
    },
    1359: {
        "city": None, "zips": None,
        "faq": [
            ("What is concierge mobile phlebotomy?",
             "Concierge mobile phlebotomy is a premium, on-demand service where a licensed phlebotomist comes to your home, hotel, or office at the time you choose — no waiting rooms, no commute, complete privacy."),
            ("Who uses concierge mobile phlebotomy in Atlanta?",
             "Our concierge clients include busy executives, elderly patients, individuals recovering from procedures, and anyone who values privacy and convenience over a standard lab visit."),
            ("How do I book concierge mobile phlebotomy in Atlanta?",
             "Book online through our scheduling portal or call us directly. We offer same-day and next-day availability throughout Atlanta and metro Georgia."),
        ],
    },
    564: {
        "city": None, "zips": None,
        "faq": [
            ("What mobile lab services do you offer in Atlanta?",
             "Fastrak Mobile Lab provides mobile blood draws, at-home lab testing, DNA and paternity specimen collection, mobile drug testing, corporate wellness panels, and pre-employment screening throughout Atlanta and metro Georgia."),
            ("Do you accept insurance for mobile phlebotomy services in Atlanta?",
             "Lab processing fees are covered by most major insurance plans. The mobile convenience fee is a separate out-of-pocket charge. We provide transparent pricing before every appointment."),
            ("How quickly can I get a mobile phlebotomist in Atlanta?",
             "Most Atlanta appointments are available within 24–48 hours. Same-day availability is possible depending on your location and service type. Early-morning and evening slots are offered."),
        ],
    },
}

# Pages that only need brand fix + pillar link (no FAQ needed / thin pages)
BRAND_PILLAR_ONLY = {306, 375, 385, 395, 401, 407, 413, 368}

# All pages to process
ALL_TARGETS = set(PAGE_META.keys()) | BRAND_PILLAR_ONLY | {
    1106, 1107, 1108, 1109, 1110  # BRAND:mixed pages
}


def build_faq_html(faq_items):
    items_html = "\n\n".join(
        f"<h3>{q}</h3>\n<p>{a}</p>"
        for q, a in faq_items
    )
    return f"\n{FAQ_MARKER}\n<h2>Frequently Asked Questions</h2>\n\n{items_html}\n"


def build_pillar_block():
    return (
        f"\n{PILLAR_MARKER}\n"
        f'<p>Learn more about our <a href="{PILLAR_URL}">at-home blood draw service</a>'
        f" — available across metro Atlanta with same-day availability in many areas.</p>"
    )


def get_raw(pid):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                     headers=H_FORM,
                     params={"context": "edit", "_fields": "slug,content"},
                     timeout=20)
    r.raise_for_status()
    data = r.json()
    return data["slug"], data["content"]["raw"]


def patch(pid, raw):
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                      headers=H_JSON, json={"content": raw}, timeout=30)
    r.raise_for_status()
    return r.status_code


def process_page(pid):
    slug, raw = get_raw(pid)
    changed = False
    actions = []

    # --- Fix 1: Brand name ---
    if "FASTRAK" in raw:
        raw = raw.replace("FASTRAK Mobile Lab", "Fastrak Mobile Lab")
        raw = raw.replace("FASTRAK", "Fastrak Mobile Lab")
        actions.append("brand-fixed")
        changed = True

    # --- Fix 2: Pillar link ---
    if PILLAR_MARKER not in raw and "at-home-blood-draw-service" not in raw:
        raw = raw.rstrip() + build_pillar_block()
        actions.append("pillar-added")
        changed = True

    # --- Fix 3: FAQ ---
    meta = PAGE_META.get(pid)
    if (meta and meta.get("faq")
            and FAQ_MARKER not in raw
            and "Frequently Asked Questions" not in raw
            and "FAQ" not in raw):
        faq_html = build_faq_html(meta["faq"])
        # Insert FAQ before pillar marker if present, else before end
        if PILLAR_MARKER in raw:
            raw = raw.replace(
                PILLAR_MARKER,
                faq_html.rstrip() + "\n\n" + PILLAR_MARKER
            )
        else:
            raw = raw.rstrip() + faq_html
        actions.append("faq-added")
        changed = True

    if changed:
        status = patch(pid, raw)
        return slug, actions, f"HTTP {status}"
    else:
        return slug, [], "no-change"


def main():
    print(f"Processing {len(ALL_TARGETS)} pages...\n")
    results = []
    for pid in sorted(ALL_TARGETS):
        try:
            slug, actions, outcome = process_page(pid)
            label = ", ".join(actions) if actions else "no-change"
            print(f"  ID {pid:5}  {outcome}  [{label}]  /{slug}")
            results.append((pid, slug, label, outcome))
        except Exception as e:
            print(f"  ID {pid:5}  ERROR: {e}")
            results.append((pid, "?", "error", str(e)))

    print(f"\n--- Summary ---")
    changed = [r for r in results if r[2] != "no-change" and r[2] != "error"]
    errors  = [r for r in results if r[2] == "error"]
    print(f"  Fixed:      {len(changed)}")
    print(f"  No-change:  {len(results) - len(changed) - len(errors)}")
    print(f"  Errors:     {len(errors)}")

    if errors:
        print("\nErrors:")
        for pid, slug, _, msg in errors:
            print(f"  ID {pid} /{slug}: {msg}")

    print("\nThin pages flagged for content expansion (not auto-fixed):")
    thin = {368: "at-home-blood-draw-service-atlanta (172w)",
            375: "specialty-kit-collection (186w)",
            385: "pre-employment-screening (140w)",
            395: "mobile-dna-testing-atlanta (167w)",
            401: "health-wellness-panels (137w)",
            407: "concierge-physician-services (140w)",
            413: "order-your-own-lab-tests-at-home (150w)"}
    for pid, desc in thin.items():
        print(f"  ID {pid:5}  /{desc}")


if __name__ == "__main__":
    main()
