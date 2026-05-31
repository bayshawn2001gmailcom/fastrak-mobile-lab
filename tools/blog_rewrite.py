#!/usr/bin/env python3
"""
Blog post rewriter — Fastrak Mobile Lab
Rewrites location-specific blog posts with:
  1. Competitor research via Firecrawl (top SERP pages)
  2. 1,500-2,000 word professional SEO post via Gemini 2.5 Flash
  3. Clinical/professional featured image via Gemini 3.1 Flash Image Preview
  4. WordPress post content update
  5. Rank Math metadata update

Usage:
  python tools/blog_rewrite.py               # process all configured posts
  python tools/blog_rewrite.py --id 1174     # process one post by WP ID
  python tools/blog_rewrite.py --dry-run     # write to .tmp/ without pushing to WP
"""

import os, sys, re, json, base64, time, argparse, requests
from pathlib import Path
from dotenv import load_dotenv

os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")
FIRECRAWL_API_KEY  = os.getenv("FIRECRAWL_API_KEY", "")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
WP_SITE            = os.getenv("WP_SITE", "https://fastrakmobilelab.com")
WP_USER            = os.getenv("WP_USER", "")
WP_APP_PASSWORD    = os.getenv("WP_APP_PASSWORD", "")

BOOKING_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"

TMP_DIR = Path(__file__).parent.parent / ".tmp" / "blog_rewrites"
TMP_DIR.mkdir(parents=True, exist_ok=True)

_creds     = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
WP_HEADERS = {"Authorization": f"Basic {_creds}", "Content-Type": "application/json"}
FC_HEADERS = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}


# ============================================================
# POST CONFIGS — Batch 3 (Perplexity-enhanced, next 5)
# ============================================================
POST_CONFIGS = [
    {
        "id": 1186,
        "city": "Gwinnett County, GA",
        "county": "Gwinnett County",
        "service": "specimen integrity and chain of custody",
        "focus_keyword": "chain of custody lab draw Gwinnett County",
        "parent_keyword": "chain of custody drug test",
        "supporting_keywords": [
            "specimen integrity mobile lab",
            "chain of custody blood draw Georgia",
            "legal specimen collection Gwinnett",
            "CLIA compliant mobile phlebotomy",
        ],
        "seo_title": "Specimen Integrity & Chain of Custody Lab Draws | Gwinnett County Mobile Lab",
        "meta_description": "Fastrak Mobile Lab ensures strict chain-of-custody and CLIA-compliant specimen handling for all lab draws in Gwinnett County. Court-admissible results for legal, DOT, and DNA testing.",
        "image_prompt": "Forensic-quality chain-of-custody lab setup: sealed tamper-evident specimen bag with official COC form on a clean white surface. Multiple labeled blood collection tubes in a rack, biohazard shipping container open nearby, gloved hands about to seal a specimen. Ultra-clinical, precision laboratory environment. No faces. Ultra-realistic medical photography.",
        "image_alt": "Chain-of-custody specimen collection kit with tamper-evident seals and COC documentation for Gwinnett County mobile lab draws",
        "internal_links": [
            "https://fastrakmobilelab.com/mobile-phlebotomy-services-atlanta/",
            "https://fastrakmobilelab.com/mobile-drug-testing-gwinnett-county-ga/",
            "https://fastrakmobilelab.com/faq/",
        ],
    },
    {
        "id": 1189,
        "city": "Gwinnett County, GA",
        "county": "Gwinnett County",
        "service": "immigration DNA testing",
        "focus_keyword": "DNA testing immigration Gwinnett County",
        "parent_keyword": "immigration DNA test near me",
        "supporting_keywords": [
            "AABB accredited DNA testing Georgia",
            "USCIS DNA test Gwinnett County",
            "immigration DNA specimen collection near me",
            "embassy approved DNA test Georgia",
        ],
        "seo_title": "DNA Testing for Immigration in Gwinnett County, GA | AABB-Compliant Mobile Collection",
        "meta_description": "AABB-compliant immigration DNA testing in Gwinnett County, GA. Fastrak Mobile Lab provides certified specimen collection accepted by USCIS and U.S. embassies. Mobile service — we come to you.",
        "image_prompt": "Official immigration DNA testing kit on a clean white surface: sterile buccal swabs in sealed clinical packaging, official AABB chain-of-custody form, tamper-evident specimen bag with security seal, and a small U.S. flag pin nearby. Professional immigration services office aesthetic. Crisp, authoritative lighting. No faces visible.",
        "image_alt": "AABB-compliant immigration DNA testing kit with official chain-of-custody documentation in Gwinnett County, GA",
        "internal_links": [
            "https://fastrakmobilelab.com/mobile-dna-testing-atlanta/",
            "https://fastrakmobilelab.com/dna-testing-gwinnett-county-ga/",
            "https://fastrakmobilelab.com/faq/",
        ],
    },
    {
        "id": 1191,
        "city": "Georgia",
        "county": "Georgia",
        "service": "workplace drug testing compliance",
        "focus_keyword": "workplace drug testing compliance Georgia",
        "parent_keyword": "workplace drug testing program",
        "supporting_keywords": [
            "employee drug screening program Georgia",
            "non-DOT drug testing employer Georgia",
            "drug free workplace Georgia law",
            "mobile drug testing employer program",
        ],
        "seo_title": "Workplace Drug Testing Compliance in Georgia | 2026 Employer Guide",
        "meta_description": "Complete 2026 guide to workplace drug testing compliance in Georgia. Fastrak Mobile Lab helps employers build DOT and non-DOT drug-free workplace programs with on-site mobile testing.",
        "image_prompt": "Professional HR compliance setting: a clean corporate desk with a drug-free workplace policy binder, official chain-of-custody form, tamper-evident specimen cup in a sealed bag, and a Georgia state compliance checklist. Modern office environment. Institutional lighting. No faces visible. Ultra-realistic professional photograph.",
        "image_alt": "Workplace drug testing compliance documentation and specimen collection materials for Georgia employers",
        "internal_links": [
            "https://fastrakmobilelab.com/mobile-drug-testing-gwinnett-county-ga/",
            "https://fastrakmobilelab.com/pre-employment-screening/",
            "https://fastrakmobilelab.com/faq/",
        ],
    },
    {
        "id": 1196,
        "city": "Georgia",
        "county": "Metro Atlanta",
        "service": "mobile phlebotomy for elderly patients",
        "focus_keyword": "mobile phlebotomy elderly patients Georgia",
        "parent_keyword": "mobile phlebotomy near me",
        "supporting_keywords": [
            "at home blood draw elderly Georgia",
            "home phlebotomy seniors benefits",
            "mobile lab services homebound patients",
            "in-home blood draw for chronic illness",
        ],
        "seo_title": "Mobile Phlebotomy for Elderly Patients | Benefits & Safety Guide Georgia",
        "meta_description": "Mobile phlebotomy for elderly and homebound patients in Georgia. Fastrak Mobile Lab explains the benefits, safety protocols, and what to expect from at-home blood draws for seniors.",
        "image_prompt": "Compassionate clinical scene: a professional phlebotomist in light blue scrubs gently and carefully arranging blood draw supplies on a clean portable medical tray next to a comfortable armchair in a warmly lit home. Butterfly needle in packaging, labeled collection tubes, cotton gauze, disposable gloves laid out with precision. Warm, trustworthy atmosphere. No faces visible. Professional medical photography.",
        "image_alt": "Mobile phlebotomist carefully preparing gentle blood draw supplies for an elderly patient at home in Georgia",
        "internal_links": [
            "https://fastrakmobilelab.com/mobile-phlebotomy-services-atlanta/",
            "https://fastrakmobilelab.com/at-home-blood-draw-service-atlanta/",
            "https://fastrakmobilelab.com/faq/",
        ],
    },
    {
        "id": 1148,
        "city": "Atlanta, GA",
        "county": "Fulton County",
        "service": "DNA testing",
        "focus_keyword": "DNA testing services Atlanta GA",
        "parent_keyword": "DNA testing near me",
        "supporting_keywords": [
            "mobile DNA testing Atlanta",
            "paternity test Atlanta GA",
            "legal DNA testing Fulton County",
            "AABB DNA specimen collection Atlanta",
        ],
        "seo_title": "DNA Testing Services in Atlanta, GA | Mobile Specimen Collection",
        "meta_description": "Certified DNA testing services in Atlanta, GA. Fastrak Mobile Lab provides mobile DNA specimen collection for paternity, immigration, and legal cases in Fulton County. Book today.",
        "image_prompt": "Professional DNA testing setup in an Atlanta clinical setting: sterile buccal swab kits in sealed packaging, AABB-compliant chain-of-custody forms, labeled specimen tubes, and tamper-evident bags on a pristine white surface. Clean, authoritative laboratory aesthetic with soft professional lighting. No faces visible.",
        "image_alt": "Certified DNA testing specimen collection kit with chain-of-custody forms for Atlanta, GA mobile lab services",
        "internal_links": [
            "https://fastrakmobilelab.com/mobile-dna-testing-atlanta/",
            "https://fastrakmobilelab.com/at-home-blood-draw-service-atlanta/",
            "https://fastrakmobilelab.com/mobile-phlebotomy-services-atlanta/",
        ],
    },
]

# ============================================================
# POST CONFIGS — Batch 2 (location-specific, completed)
# ============================================================
BATCH_2_CONFIGS = [
    {
        "id": 1176,
        "city": "Duluth, GA",
        "county": "Gwinnett County",
        "service": "corporate wellness blood panels",
        "focus_keyword": "corporate wellness blood panels Duluth GA",
        "parent_keyword": "corporate wellness blood testing",
        "supporting_keywords": [
            "on-site employee health screening Duluth",
            "executive blood panel Gwinnett County",
            "workplace health screening near me",
            "mobile lab services Duluth GA",
        ],
        "seo_title": "Corporate Wellness Blood Panels in Duluth, GA | On-Site Employee Screening",
        "meta_description": "Fastrak Mobile Lab delivers on-site corporate wellness blood panels for Duluth, GA employers. Certified phlebotomists come to your office in Gwinnett County. Book your screening now.",
        "image_prompt": "Corporate office wellness setting: a certified phlebotomist in navy blue scrubs and gloves preparing a blood draw station at a modern conference room table. A neatly arranged tray with labeled specimen tubes, tourniquet, sterile wipes, and chain-of-custody forms. Clean, professional office environment with large windows and natural light. No faces visible. Ultra-realistic clinical photograph.",
        "image_alt": "Certified phlebotomist setting up on-site corporate wellness blood draw station in a Duluth, GA office",
    },
    {
        "id": 1177,
        "city": "Gwinnett County, GA",
        "county": "Gwinnett County",
        "service": "mobile phlebotomy",
        "focus_keyword": "how mobile phlebotomy works Gwinnett County",
        "parent_keyword": "mobile phlebotomy near me",
        "supporting_keywords": [
            "at home blood draw Gwinnett County",
            "mobile blood draw process",
            "in-home lab services near me",
            "mobile phlebotomy appointment what to expect",
        ],
        "seo_title": "How Mobile Phlebotomy Works in Gwinnett County | Patient Guide",
        "meta_description": "Wondering how mobile phlebotomy works in Gwinnett County, GA? Fastrak Mobile Lab explains the full process — scheduling, the at-home appointment, specimen handling, and results delivery.",
        "image_prompt": "Step-by-step clinical scene: a professional phlebotomist in white clinical scrubs laying out a mobile blood draw kit on a clean portable tray at a patient's home. Supplies include butterfly needle in packaging, BD Vacutainer tubes color-coded by test type, tourniquet, alcohol wipes, adhesive bandages, and chain-of-custody labels. Bright, clean residential setting. Ultra-realistic medical photograph. No faces visible.",
        "image_alt": "Mobile phlebotomist preparing at-home blood draw supplies for a Gwinnett County patient appointment",
    },
    {
        "id": 1178,
        "city": "Gwinnett County, GA",
        "county": "Gwinnett County",
        "service": "DOT drug testing",
        "focus_keyword": "DOT drug testing Gwinnett County",
        "parent_keyword": "DOT drug testing near me",
        "supporting_keywords": [
            "DOT drug testing fleet managers Gwinnett",
            "FMCSA drug testing Georgia",
            "mobile DOT drug test Lawrenceville",
            "on-site DOT compliance testing Gwinnett County",
        ],
        "seo_title": "DOT Drug Testing in Gwinnett County, GA | On-Site Fleet Compliance",
        "meta_description": "FMCSA-compliant DOT drug testing for Gwinnett County fleet managers and employers. Fastrak Mobile Lab conducts on-site testing with full chain-of-custody documentation. Schedule today.",
        "image_prompt": "Professional drug testing technician in a white lab coat standing at a clean testing station with official DOT chain-of-custody forms, tamper-evident specimen cup in a sealed bag, and compliance documentation binders. Corporate logistics setting with a large vehicle slightly visible through window. Crisp, institutional lighting. No faces visible.",
        "image_alt": "DOT drug testing technician with chain-of-custody documentation for fleet compliance testing in Gwinnett County",
    },
    {
        "id": 1179,
        "city": "Conyers, GA",
        "county": "Rockdale County",
        "service": "mobile blood collection for assisted living",
        "focus_keyword": "mobile blood collection assisted living Conyers GA",
        "parent_keyword": "mobile phlebotomy assisted living",
        "supporting_keywords": [
            "in-home blood draw elderly Conyers GA",
            "assisted living lab services Rockdale County",
            "mobile phlebotomy nursing home near me",
            "home blood draw seniors Conyers",
        ],
        "seo_title": "Mobile Blood Collection for Assisted Living in Conyers, GA | Rockdale County Lab Services",
        "meta_description": "Certified mobile blood collection for assisted living facilities and homebound patients in Conyers, GA. Fastrak Mobile Lab serves Rockdale County with gentle, clinical-grade in-facility draws.",
        "image_prompt": "Compassionate phlebotomist in light blue clinical scrubs gently arranging blood draw supplies on a portable medical tray beside a neatly made assisted living room bed. Supplies: butterfly needle in packaging, collection tubes in a small rack, alcohol prep pads, cotton gauze, gloves. Warm, soft lighting in a residential care facility room. No faces visible. Professional medical photography.",
        "image_alt": "Mobile phlebotomist preparing blood draw supplies in an assisted living room in Conyers, GA",
    },
    {
        "id": 1188,
        "city": "Lithonia, GA",
        "county": "DeKalb County",
        "service": "home blood draw",
        "focus_keyword": "home blood draw Lithonia GA",
        "parent_keyword": "at home blood draw",
        "supporting_keywords": [
            "mobile phlebotomy Lithonia Georgia",
            "at home blood draw DeKalb County",
            "in-home lab services Lithonia",
            "mobile blood draw near me Lithonia",
        ],
        "seo_title": "Home Blood Draw in Lithonia, GA | Mobile Lab Services in DeKalb County",
        "meta_description": "Certified home blood draw services in Lithonia, GA. Fastrak Mobile Lab sends licensed phlebotomists directly to your door in DeKalb County. Same-day and next-day appointments available.",
        "image_prompt": "Licensed phlebotomist in dark navy scrubs preparing a blood collection tray at a patient's kitchen table in a well-lit home. Precisely arranged supplies: labeled Vacutainer tubes, tourniquet, sealed needles, alcohol wipes, adhesive bandages. Bright natural light from nearby window. Ultra-realistic clinical photograph. No faces visible.",
        "image_alt": "Mobile phlebotomist setting up home blood draw supplies at a patient's table in Lithonia, GA",
    },
]

# ============================================================
# POST CONFIGS — Batch 1 (location-specific, completed)
# ============================================================
BATCH_1_CONFIGS = [
    {
        "id": 1171,
        "city": "Snellville, GA",
        "county": "Gwinnett County",
        "service": "mobile phlebotomy",
        "focus_keyword": "mobile phlebotomy Snellville GA",
        "parent_keyword": "mobile phlebotomy near me",
        "supporting_keywords": [
            "at home blood draw Snellville",
            "mobile blood draw Gwinnett County",
            "home phlebotomy service near me",
            "mobile lab services Snellville",
        ],
        "seo_title": "Mobile Phlebotomy in Snellville, GA | At-Home Blood Draw Services",
        "meta_description": "Fastrak Mobile Lab brings certified mobile phlebotomy to Snellville, GA. Licensed phlebotomists travel to your home, office, or care facility in Gwinnett County. Book today.",
        "image_prompt": "Professional phlebotomist in navy blue clinical scrubs preparing a blood draw kit on a clean white medical tray in a bright residential living room. Medical supplies precisely arranged: tourniquet, sealed sterile needles, labeled blood collection tubes upright in a rack, alcohol prep pads. Soft morning light through window. Ultra-realistic photograph, clinical precision. No faces visible.",
        "image_alt": "Mobile phlebotomist preparing blood draw supplies at a patient's home in Snellville, GA",
    },
    {
        "id": 1172,
        "city": "Gwinnett County, GA",
        "county": "Gwinnett County",
        "service": "on-site drug testing",
        "focus_keyword": "on site drug testing Gwinnett County",
        "parent_keyword": "on site drug testing",
        "supporting_keywords": [
            "mobile drug testing Gwinnett County",
            "workplace drug testing near me",
            "employer drug screening Georgia",
            "DOT drug testing Lawrenceville GA",
        ],
        "seo_title": "On-Site Drug Testing in Gwinnett County, GA | Mobile Workplace Screening",
        "meta_description": "Certified on-site drug testing for Gwinnett County employers. Fastrak Mobile Lab handles DOT and non-DOT panels with chain-of-custody documentation. Schedule now.",
        "image_prompt": "Drug testing technician in a white lab coat placing a sealed urine specimen cup next to official chain-of-custody paperwork and tamper-evident labels on a clean corporate desk. Professional office environment with filing folders visible in background. Crisp, neutral lighting. No faces visible.",
        "image_alt": "Drug testing technician setting up chain-of-custody documentation for on-site drug screening in Gwinnett County",
    },
    {
        "id": 1173,
        "city": "Lawrenceville, GA",
        "county": "Gwinnett County",
        "service": "mobile blood draw for seniors",
        "focus_keyword": "mobile blood draw seniors Lawrenceville GA",
        "parent_keyword": "at home blood draw",
        "supporting_keywords": [
            "home phlebotomy elderly Lawrenceville",
            "at home blood draw for elderly Georgia",
            "mobile phlebotomy near me seniors",
            "senior lab services Gwinnett County",
        ],
        "seo_title": "Mobile Blood Draw for Seniors in Lawrenceville, GA | Home Lab Services",
        "meta_description": "Mobile blood draw for elderly patients in Lawrenceville, GA. Certified phlebotomists come to your home in Gwinnett County. Compassionate, clinical-grade care.",
        "image_prompt": "Healthcare professional in light blue clinical scrubs gently arranging blood draw supplies on a portable medical tray beside a comfortable upholstered armchair in a warmly lit home. Supplies visible: butterfly needle in packaging, collection tubes, cotton gauze, gloves. Soft natural light. No faces visible. Warm, professional atmosphere.",
        "image_alt": "Mobile phlebotomist preparing home blood draw supplies for an elderly patient in Lawrenceville, GA",
    },
    {
        "id": 1174,
        "city": "Norcross, GA",
        "county": "Gwinnett County",
        "service": "paternity DNA testing",
        "focus_keyword": "paternity test Norcross GA",
        "parent_keyword": "paternity test near me",
        "supporting_keywords": [
            "DNA paternity test Norcross",
            "legal paternity testing Gwinnett County",
            "court admissible DNA test Georgia",
            "chain of custody DNA specimen collection Norcross",
        ],
        "seo_title": "Paternity Test in Norcross, GA | Legal DNA Testing Near You",
        "meta_description": "Legal, court-admissible paternity testing in Norcross, GA. Certified DNA collection with full chain of custody. Fastrak Mobile Lab comes to you in Gwinnett County.",
        "image_prompt": "Sterile buccal swab DNA collection kit in sealed clinical packaging on a pristine white medical surface. Multiple labeled specimen tubes in a transparent rack, official chain-of-custody form, tamper-evident specimen bag sealed shut. Ultra-clean laboratory environment. Precise, professional composition. No faces.",
        "image_alt": "Sterile DNA collection kit with chain-of-custody documentation for court-admissible paternity testing in Norcross, GA",
    },
    {
        "id": 1175,
        "city": "Tucker and Stone Mountain, GA",
        "county": "DeKalb County",
        "service": "mobile phlebotomy",
        "focus_keyword": "mobile phlebotomy Tucker GA",
        "parent_keyword": "at home blood draw",
        "supporting_keywords": [
            "mobile lab services Tucker Georgia",
            "blood draw Stone Mountain GA",
            "at home blood draw DeKalb County",
            "mobile phlebotomy near me Tucker",
        ],
        "seo_title": "Mobile Phlebotomy in Tucker & Stone Mountain, GA | At-Home Blood Draw",
        "meta_description": "Mobile phlebotomy in Tucker and Stone Mountain, GA. Fastrak Mobile Lab sends certified phlebotomists to your home or office in DeKalb County. Same-day appointments available.",
        "image_prompt": "Professional phlebotomist in dark clinical scrubs carefully organizing labeled blood collection tubes, tourniquet, and antiseptic wipes on a clean portable medical station. Modern residential room with bright natural window light. Highly realistic, professional medical scene. No faces visible.",
        "image_alt": "Mobile phlebotomy supplies being prepared for an at-home blood draw in Tucker, GA",
    },
]


# ============================================================
# STEP 1 — Firecrawl competitor research
# ============================================================

def firecrawl_search(query: str, num_results: int = 3) -> list[str]:
    """Search for top-ranking pages for a keyword and return their URLs."""
    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v1/search",
            json={"query": query, "limit": num_results, "scrapeOptions": {"formats": []}},
            headers=FC_HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("data", [])
        return [r["url"] for r in results if r.get("url")]
    except Exception as e:
        print(f"  [firecrawl search] error: {e}", file=sys.stderr)
        return []


def firecrawl_scrape(url: str) -> str:
    """Scrape a URL and return clean markdown."""
    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v1/scrape",
            json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
            headers=FC_HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return (data.get("data") or {}).get("markdown", "") or data.get("markdown", "")
    except Exception as e:
        print(f"  [firecrawl scrape] error for {url}: {e}", file=sys.stderr)
        return ""


def get_competitor_context(focus_keyword: str, parent_keyword: str) -> str:
    """Get competitor content snippets for the target keyword."""
    print(f"  Searching competitors for: {parent_keyword}")
    urls = firecrawl_search(parent_keyword, num_results=3)
    if not urls:
        print("  No competitor URLs found, proceeding without research context.")
        return "No competitor content available."

    snippets = []
    for url in urls[:2]:
        print(f"  Scraping: {url}")
        content = firecrawl_scrape(url)
        if content and len(content.strip()) > 300:
            # Take first 1,500 chars to avoid context bloat
            snippets.append(f"Source: {url}\n{content.strip()[:1500]}")
        time.sleep(0.5)

    return "\n\n---\n\n".join(snippets) if snippets else "No competitor content available."


# ============================================================
# STEP 1b — Perplexity real-time research
# ============================================================

def get_perplexity_research(focus_keyword: str, city: str, county: str, service: str) -> str:
    """Get factual, cited research from Perplexity sonar-pro for the target keyword/service."""
    if not PERPLEXITY_API_KEY:
        return "No Perplexity research available."
    prompt = (
        f"Provide detailed, factual research on {service} services in {city}, {county}, Georgia. "
        f"Cover: (1) key patient/client concerns and common questions, "
        f"(2) relevant regulations or credentials required (CLIA, DOT, FMCSA, AABB, USCIS as applicable), "
        f"(3) typical process steps from scheduling to results, "
        f"(4) who typically needs this service and why, "
        f"(5) any local healthcare access gaps or demand signals for the {city}/{county} area. "
        f"Be specific and factual. Focus on content useful for writing an authoritative SEO blog post "
        f"targeting the keyword: '{focus_keyword}'."
    )
    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {PERPLEXITY_API_KEY}", "Content-Type": "application/json"},
            json={"model": "sonar-pro", "messages": [{"role": "user", "content": prompt}]},
            timeout=45,
        )
        if not resp.ok:
            print(f"  [perplexity] warning {resp.status_code}: {resp.text[:100]}", file=sys.stderr)
            return "Perplexity research unavailable."
        content = resp.json()["choices"][0]["message"]["content"]
        print(f"  Perplexity research: {len(content.split())} words")
        return content[:3000]
    except Exception as e:
        print(f"  [perplexity] error: {e}", file=sys.stderr)
        return "Perplexity research unavailable."


# ============================================================
# STEP 2 — Gemini content generation
# ============================================================

BLOG_PROMPT_TEMPLATE = """You are a senior healthcare SEO content writer with 10 years of experience writing for mobile medical service companies. You write with clinical authority, local specificity, and genuine patient empathy.

BUSINESS CONTEXT:
- Company: Fastrak Mobile Lab
- Model: Mobile service-area business. Licensed phlebotomists travel to the patient. NO physical office address exists — never mention one.
- Services: Mobile phlebotomy, in-home blood draw, drug testing (DOT/non-DOT), DNA specimen collection
- Differentiators: Certified/licensed professionals, we travel to you, same-day or next-day availability, all specimen handling meets CLIA standards
- Insurance: Lab processing fees are covered by most major insurance plans. The mobile convenience/travel fee is a SEPARATE charge not covered by insurance. NEVER imply the mobile service itself is covered.
- Tone: Clinically authoritative, warm, direct. No corporate filler. Write as if a trusted healthcare professional is speaking to the patient.
- NEVER use: "in today's fast-paced world", "exciting", "amazing", "journey", "seamless"
- Booking CTA URL: {booking_url}

ASSIGNMENT:
Write a 1,500–2,000 word SEO blog post with these exact specifications:

Primary keyword: {focus_keyword}
City/area: {city} ({county})
Service: {service}
Parent keyword (rank alongside): {parent_keyword}
Supporting keywords (weave in naturally, no stuffing): {supporting_keywords}
H1 / SEO Title: {seo_title}

REQUIRED STRUCTURE (follow exactly):
DO NOT include an <h1> tag. WordPress renders the post title as H1 automatically — adding one in the content creates a duplicate H1. Start directly with the introduction paragraph.

Introduction (200-250 words): Open with a patient-perspective problem statement relevant to {city}. Include the primary keyword "{focus_keyword}" in the first sentence. Establish Fastrak Mobile Lab as the trusted local solution. End the intro with a clear thesis of what this post will cover.

<h2>How {service_cap} Works in {city}</h2>
Step-by-step process (numbered list works well here). Frame everything around "we come to you." Include: scheduling, what to expect at the appointment, specimen handling, results delivery. 150-200 words.

<h2>Who Benefits from {service_cap} in {county}</h2>
3-4 patient/client personas with specific detail. For phlebotomy: elderly patients, post-surgical patients, chronic illness patients, busy professionals. For drug testing: HR managers, fleet companies, construction sites, post-accident. For DNA: legal cases, immigration, peace of mind. 200-250 words.

<h2>Why Choose Fastrak Mobile Lab in {city}?</h2>
4-5 differentiators as a bulleted list, each with a 1-2 sentence explanation. Include: licensed professionals, CLIA-compliant handling, chain-of-custody documentation (if applicable), same-day availability, service area breadth. 150-200 words.

<h2>Areas We Serve Near {city}</h2>
Paragraph naming specific neighborhoods, zip codes, or nearby communities in {county} that Fastrak serves. Naturally reinforce local SEO signals. Name at least 6-8 surrounding areas. 100-150 words.

<h2>Frequently Asked Questions About {service_cap} in {city}</h2>
4 FAQs as <h3> question + <p> answer pairs. Questions must reflect real patient searches. Answers: 3-5 sentences, specific and reassuring. Cover: cost/insurance, how to prepare, what ID/paperwork is needed, turnaround time for results (or chain-of-custody process for DNA/drug testing).

Closing CTA paragraph (75-100 words): Direct, confident. Include the primary keyword one final time. Link text should be action-oriented. Use: <a href="{booking_url}">Book Your {service_cap} Appointment in {city}</a>

INTERNAL LINKS (weave 2-3 of these naturally into the body as contextual anchor text — do NOT list them, just use them where they fit):
{internal_links}

OUTPUT RULES:
- Output clean HTML only: h1, h2, h3, p, ul, ol, li, strong, a tags
- No divs, no inline styles, no markdown, no code fences, no explanatory text before or after the HTML
- Booking link: <a href="{booking_url}">...</a>
- Internal links: use the exact URLs provided above, with natural anchor text (e.g. "our mobile phlebotomy services", "Atlanta DNA testing", not the raw URL)
- Do NOT fabricate: specific dollar prices, specific turnaround hours, specific insurance plan names
- DO include: "most major insurance plans cover the lab processing fee", "same-day or next-day appointments available", "results typically available within 24-72 hours through your ordering physician"

COMPETITOR RESEARCH (use for topic depth and structure only — do not copy or plagiarize):
{competitor_content}

PERPLEXITY RESEARCH (real-time factual sources — use for accuracy, statistics, credential details, regulatory specifics):
{perplexity_research}

Write the complete blog post HTML now:"""


def generate_post_content(cfg: dict, competitor_content: str, perplexity_research: str = "") -> str:
    """Generate SEO blog post content using Gemini 2.5 Flash."""
    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)

    service_cap = cfg["service"].title()
    supporting_str = ", ".join(cfg["supporting_keywords"])

    internal_links_raw = cfg.get("internal_links", [])
    internal_links_str = "\n".join(f"- {url}" for url in internal_links_raw) if internal_links_raw else "- https://fastrakmobilelab.com/mobile-phlebotomy-services-atlanta/"

    prompt = BLOG_PROMPT_TEMPLATE.format(
        focus_keyword=cfg["focus_keyword"],
        city=cfg["city"],
        county=cfg["county"],
        service=cfg["service"],
        service_cap=service_cap,
        parent_keyword=cfg["parent_keyword"],
        supporting_keywords=supporting_str,
        seo_title=cfg["seo_title"],
        booking_url=BOOKING_URL,
        competitor_content=competitor_content[:3000],
        perplexity_research=perplexity_research[:3000] if perplexity_research else "Not available.",
        internal_links=internal_links_str,
    )

    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash"]
    last_err = None

    for model in models_to_try:
        for attempt in range(2):
            try:
                print(f"  Generating content ({model}, attempt {attempt+1})...")
                response = client.models.generate_content(
                    model=model,
                    contents=[prompt],
                )
                text = response.text.strip()
                # Strip markdown code fences if present
                text = re.sub(r"^```html\s*", "", text)
                text = re.sub(r"^```\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
                # Fix common AI capitalization errors
                text = text.replace(" Dna ", " DNA ").replace(">Dna ", ">DNA ").replace(" Dna<", " DNA<")
                text = text.replace(" Dot ", " DOT ").replace(">Dot ", ">DOT ")
                text = text.replace("Clia", "CLIA").replace("Uscis", "USCIS")
                word_count = len(re.sub(r"<[^>]+>", " ", text).split())
                print(f"  Generated {word_count} words")
                return text
            except Exception as e:
                msg = str(e)
                if "429" in msg or "503" in msg or "RESOURCE_EXHAUSTED" in msg:
                    wait = 30 * (attempt + 1)
                    print(f"  Rate limit, waiting {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                else:
                    print(f"  Error ({model}): {msg[:100]}", file=sys.stderr)
                    last_err = e
                    break
        time.sleep(5)

    raise RuntimeError(f"Content generation failed: {last_err}")


# ============================================================
# STEP 3 — Gemini image generation
# ============================================================

def generate_image(prompt: str) -> tuple[bytes, str]:
    """Generate clinical/professional featured image using Gemini 3.1 Flash Image Preview."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="1K",
        ),
    )

    retries = 4
    for attempt in range(1, retries + 1):
        try:
            print(f"  Generating image (attempt {attempt})...")
            response = client.models.generate_content(
                model="gemini-3.1-flash-image-preview",
                contents=[prompt],
                config=config,
            )
            parts = getattr(response, "parts", None) or []
            for part in parts:
                if getattr(part, "thought", False):
                    continue
                if getattr(part, "inline_data", None) is not None:
                    return part.inline_data.data, part.inline_data.mime_type
            # No image in response — log and retry
            text_parts = [getattr(p, "text", "") for p in parts if getattr(p, "text", "")]
            print(f"  No image in response (attempt {attempt}). Parts: {len(parts)}. Text: {str(text_parts)[:120]}", file=sys.stderr)
            time.sleep(15 * attempt)
        except Exception as e:
            msg = str(e)
            if "503" in msg or "UNAVAILABLE" in msg or "429" in msg or "EXHAUSTED" in msg:
                wait = 20 * attempt
                print(f"  Image API busy, retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                raise

    raise RuntimeError("Image generation failed after all retries")


# ============================================================
# STEP 4 — WordPress media upload
# ============================================================

def upload_image_to_wp(image_bytes: bytes, mime_type: str, filename: str, alt_text: str) -> int:
    """Upload image to WordPress media library, return media ID."""
    ext = "jpg" if "jpeg" in mime_type else "png"
    full_filename = f"{filename}.{ext}"

    upload_headers = {
        "Authorization": f"Basic {_creds}",
        "Content-Disposition": f'attachment; filename="{full_filename}"',
        "Content-Type": mime_type,
    }

    resp = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/media",
        headers=upload_headers,
        data=image_bytes,
        timeout=60,
    )
    if not resp.ok:
        raise RuntimeError(f"Media upload failed {resp.status_code}: {resp.text[:200]}")

    media_id = resp.json()["id"]

    # Set alt text
    requests.post(
        f"{WP_SITE}/wp-json/wp/v2/media/{media_id}",
        headers=WP_HEADERS,
        json={"alt_text": alt_text, "caption": ""},
        timeout=20,
    )

    print(f"  Uploaded image — media ID: {media_id}")
    return media_id


# ============================================================
# STEP 5 — WordPress post update
# ============================================================

def update_post(post_id: int, title: str, content: str, media_id: int) -> None:
    """Update WordPress post content and featured image."""
    payload = {
        "title": title,
        "content": content,
        "featured_media": media_id,
        "status": "publish",
    }
    resp = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}",
        headers=WP_HEADERS,
        json=payload,
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Post update failed {resp.status_code}: {resp.text[:200]}")
    print(f"  Post {post_id} updated — {resp.json().get('link', '')}")


# ============================================================
# STEP 6 — Rank Math metadata
# ============================================================

def update_rank_math(post_id: int, focus_keyword: str, seo_title: str, meta_description: str) -> None:
    """Set Rank Math focus keyword, SEO title, and meta description."""
    url = f"{WP_SITE}/wp-json/rankmath/v1/updateMeta"
    payload = {
        "objectID": post_id,
        "objectType": "post",
        "meta[rank_math_focus_keyword]": focus_keyword,
        "meta[rank_math_title]": seo_title,
        "meta[rank_math_description]": meta_description,
    }
    # Use form-encoded (not JSON) — required by Rank Math
    rm_headers = {"Authorization": f"Basic {_creds}"}
    resp = requests.post(url, headers=rm_headers, data=payload, timeout=20)
    if not resp.ok:
        print(f"  Rank Math warning {resp.status_code}: {resp.text[:100]}", file=sys.stderr)
    else:
        print(f"  Rank Math metadata set for post {post_id}")


# ============================================================
# Main pipeline
# ============================================================

def process_post(cfg: dict, dry_run: bool = False) -> None:
    post_id = cfg["id"]
    city_slug = cfg["city"].lower().replace(", ", "-").replace(" ", "-").replace("&", "and")
    print(f"\n{'='*60}")
    print(f"  Processing post {post_id}: {cfg['focus_keyword']}")
    print(f"{'='*60}")

    # 1. Competitor research (Firecrawl)
    competitor_content = get_competitor_context(cfg["focus_keyword"], cfg["parent_keyword"])
    (TMP_DIR / f"{post_id}_competitors.txt").write_text(competitor_content, encoding="utf-8")

    # 1b. Perplexity factual research
    print(f"  Fetching Perplexity research for: {cfg['focus_keyword']}")
    perplexity_research = get_perplexity_research(
        cfg["focus_keyword"], cfg["city"], cfg["county"], cfg["service"]
    )
    (TMP_DIR / f"{post_id}_perplexity.txt").write_text(perplexity_research, encoding="utf-8")

    # 2. Generate content
    content_html = generate_post_content(cfg, competitor_content, perplexity_research)
    content_path = TMP_DIR / f"{post_id}_content.html"
    content_path.write_text(content_html, encoding="utf-8")
    print(f"  Content saved: {content_path}")

    # 3. Generate image
    image_bytes, mime_type = generate_image(cfg["image_prompt"])
    ext = "jpg" if "jpeg" in mime_type else "png"
    image_path = TMP_DIR / f"{post_id}_featured.{ext}"
    image_path.write_bytes(image_bytes)
    print(f"  Image saved: {image_path} ({len(image_bytes)//1024}KB)")

    if dry_run:
        print(f"  [dry-run] Skipping WordPress update for post {post_id}")
        return

    # 4. Upload image
    filename = f"fastrak-{city_slug}-{cfg['service'].replace(' ', '-')}"
    media_id = upload_image_to_wp(image_bytes, mime_type, filename, cfg["image_alt"])

    # 5. Update post
    update_post(post_id, cfg["seo_title"], content_html, media_id)

    # 6. Rank Math
    update_rank_math(post_id, cfg["focus_keyword"], cfg["seo_title"], cfg["meta_description"])

    print(f"  Post {post_id} complete.")


def main():
    parser = argparse.ArgumentParser(description="Rewrite Fastrak blog posts with SEO content and images")
    parser.add_argument("--id", type=int, help="Process only this WordPress post ID")
    parser.add_argument("--dry-run", action="store_true", help="Generate files to .tmp/ without pushing to WordPress")
    args = parser.parse_args()

    if not GEMINI_API_KEY:
        sys.exit("Error: GEMINI_API_KEY not set in ~/.env")
    if not FIRECRAWL_API_KEY:
        print("Warning: FIRECRAWL_API_KEY not set — competitor research will be skipped", file=sys.stderr)
    if not dry_run_mode(args) and (not WP_USER or not WP_APP_PASSWORD):
        sys.exit("Error: WP_USER and WP_APP_PASSWORD must be set in ~/.env")

    configs = POST_CONFIGS
    if args.id:
        configs = [c for c in POST_CONFIGS if c["id"] == args.id]
        if not configs:
            sys.exit(f"Error: No post config found for ID {args.id}")

    print(f"\nBlog Rewrite Pipeline — {len(configs)} post(s)")
    print(f"Mode: {'DRY RUN (no WP update)' if args.dry_run else 'LIVE'}")
    print(f"Output: {TMP_DIR}\n")

    for cfg in configs:
        try:
            process_post(cfg, dry_run=args.dry_run)
        except Exception as e:
            print(f"\n  ERROR on post {cfg['id']}: {e}", file=sys.stderr)
            print("  Continuing with next post...", file=sys.stderr)
        time.sleep(3)  # brief pause between posts

    print("\nAll done.")


def dry_run_mode(args) -> bool:
    return args.dry_run


if __name__ == "__main__":
    main()
