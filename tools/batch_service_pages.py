"""
Generate and post 3 service-specific landing pages as WordPress drafts.
Run: python tools/batch_service_pages.py
"""
import os, sys, time, base64, re, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not GEMINI_API_KEY:
    sys.exit("Error: GEMINI_API_KEY missing")
if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER / WP_APP_PASSWORD missing")

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
WP_HEADERS = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

PAGES = [
    {
        "title": "Mobile Drug Testing Atlanta, GA",
        "slug": "mobile-drug-testing-atlanta",
        "keyword": "mobile drug testing Atlanta",
        "seo_title": "Mobile Drug Testing Atlanta, GA | Fastrak Mobile Lab",
        "meta_desc": (
            "Need on-site drug testing in Atlanta, GA? Fastrak Mobile Lab sends a certified "
            "collector to your workplace or home. Fast results, DOT-compliant."
        ),
        "prompt": """Write an SEO-optimized service page for Fastrak Mobile Lab's mobile drug testing service.

CRITICAL RULES:
- Service area business — we travel TO the client. NEVER mention a physical office or address.
- Always frame as "we come to you" — never "visit our location"
- Lab processing fees may be covered by insurance or employer; the mobile convenience fee is separate and NOT covered by insurance.

Business: Fastrak Mobile Lab — licensed mobile specimen collection, metro Atlanta and Gwinnett County, GA
Primary keyword: mobile drug testing Atlanta
Supporting keywords: on-site drug testing Atlanta, workplace drug testing, DOT drug testing Georgia, mobile drug screen

Requirements:
- H1: "Mobile Drug Testing in Atlanta, GA" (exact)
- First paragraph: hook + primary keyword + we come to you framing
- H2 #1: "On-Site Drug Testing for Atlanta Businesses" — workplace testing, HR, pre-employment, random testing programs
- H2 #2: "DOT-Compliant and Regulated Testing" — federally compliant, chain of custody, MRO review, accepted by employers and courts
- H2 #3: "Who Uses Our Mobile Drug Testing Service" — employers, staffing agencies, individuals, legal cases, probation
- FAQ section (H2: "Frequently Asked Questions") with 3 questions for Atlanta employers and individuals
- Closing CTA paragraph
- Word count: 650-800 words
- Output clean HTML only (h1, h2, h3, p, ul, li — no divs, no inline styles, no markdown, no html/head/body tags)
""",
    },
    {
        "title": "DNA Testing at Home in Georgia",
        "slug": "dna-testing-at-home-georgia",
        "keyword": "DNA testing at home Georgia",
        "seo_title": "DNA Testing at Home Georgia | Fastrak Mobile Lab",
        "meta_desc": (
            "Home DNA testing in Georgia — Fastrak Mobile Lab sends a certified collector to you "
            "for paternity, relationship, and legal DNA specimen collection."
        ),
        "prompt": """Write an SEO-optimized service page for Fastrak Mobile Lab's mobile DNA specimen collection service.

CRITICAL RULES:
- Service area business — we travel TO the client. NEVER mention a physical office or address.
- Always frame as "we come to you" — never "visit our location"
- We collect the specimen only — the lab processes and returns results. We do not interpret results.
- The mobile convenience fee is separate from lab fees.

Business: Fastrak Mobile Lab — licensed mobile specimen collection, metro Atlanta and Gwinnett County, GA
Primary keyword: DNA testing at home Georgia
Supporting keywords: home DNA collection Georgia, paternity test at home, mobile DNA specimen collection, legal DNA testing Georgia

Requirements:
- H1: "DNA Testing at Home in Georgia" (exact)
- First paragraph: hook + primary keyword + we come to you framing
- H2 #1: "How Home DNA Collection Works" — schedule, we arrive, collect buccal swabs, chain of custody, send to certified lab
- H2 #2: "Types of DNA Tests We Collect For" — paternity, maternity, sibling, grandparent, legal/court-admissible, immigration
- H2 #3: "Why Choose Mobile DNA Collection" — no lab visit, privacy, convenience, chain of custody maintained, certified collectors
- FAQ section (H2: "Frequently Asked Questions") with 3 questions about legal admissibility, who can be tested, and turnaround time
- Closing CTA paragraph
- Word count: 600-750 words
- Output clean HTML only (h1, h2, h3, p, ul, li — no divs, no inline styles, no markdown, no html/head/body tags)
""",
    },
    {
        "title": "Corporate Mobile Lab Services Atlanta, GA",
        "slug": "corporate-mobile-lab-services-atlanta",
        "keyword": "corporate mobile lab services Atlanta",
        "seo_title": "Corporate Mobile Lab Services Atlanta | Fastrak Mobile Lab",
        "meta_desc": (
            "On-site corporate lab services in Atlanta — Fastrak Mobile Lab handles employee "
            "blood draws, wellness screenings, and drug testing at your workplace."
        ),
        "prompt": """Write an SEO-optimized service page for Fastrak Mobile Lab's corporate and workplace mobile lab services.

CRITICAL RULES:
- Service area business — we travel TO the client. NEVER mention a physical office or address.
- Always frame as "we come to your office or facility" — never "visit our location"
- Lab processing fees may be billed to employer or insurance; the mobile convenience fee is separate.

Business: Fastrak Mobile Lab — licensed mobile specimen collection, metro Atlanta and Gwinnett County, GA
Primary keyword: corporate mobile lab services Atlanta
Supporting keywords: on-site employee blood draw, corporate wellness screening Atlanta, workplace phlebotomy, mobile lab for businesses

Requirements:
- H1: "Corporate Mobile Lab Services in Atlanta, GA" (exact)
- First paragraph: hook + primary keyword + we come to your workplace framing
- H2 #1: "Employee Wellness Blood Draws at Your Office" — annual physicals, wellness programs, biometric screenings, no employee travel time lost
- H2 #2: "Pre-Employment and Compliance Testing" — pre-employment drug screens, occupational health panels, DOT compliance, staffing agencies
- H2 #3: "Why Atlanta Businesses Choose Fastrak Mobile Lab" — licensed collectors, fast turnaround, HIPAA-compliant, flexible scheduling around shifts
- FAQ section (H2: "Frequently Asked Questions") with 3 questions for HR managers: minimum group size, scheduling, available tests
- Closing CTA directed at HR managers and business owners
- Word count: 650-800 words
- Output clean HTML only (h1, h2, h3, p, ul, li — no divs, no inline styles, no markdown, no html/head/body tags)
""",
    },
]


def generate(prompt, retries=4):
    model = genai.GenerativeModel("gemini-2.0-flash")
    for attempt in range(retries):
        try:
            resp = model.generate_content(prompt)
            text = resp.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text.rsplit("```", 1)[0]
            text = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", text, count=1,
                          flags=re.IGNORECASE | re.DOTALL)
            return text.strip()
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited — waiting {wait}s...")
                time.sleep(wait)
            else:
                raise


def check_slug(slug):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages", headers=WP_HEADERS,
                     params={"slug": slug, "status": "any"}, timeout=20)
    return bool(r.json()) if r.ok else False


def post_draft(title, slug, content):
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages", headers=WP_HEADERS,
                      json={"title": title, "slug": slug, "content": content, "status": "draft"},
                      timeout=30)
    r.raise_for_status()
    return r.json()


def set_seo(post_id, page):
    requests.post(f"{WP_SITE}/wp-json/rankmath/v1/updateMeta", headers=WP_HEADERS, data={
        "objectID": post_id, "objectType": "post",
        "meta[rank_math_focus_keyword]": page["keyword"],
        "meta[rank_math_title]": page["seo_title"],
        "meta[rank_math_description]": page["meta_desc"][:155],
    }, timeout=20)


def main():
    print(f"Generating {len(PAGES)} service pages as WordPress drafts...\n")
    for page in PAGES:
        print(f"[{page['slug']}] Checking slug...")
        if check_slug(page["slug"]):
            print(f"  SKIPPED — already exists\n")
            continue

        print(f"  Generating content...")
        try:
            content = generate(page["prompt"])
            print(f"  {len(content.split())} words generated")
        except Exception as e:
            print(f"  FAILED to generate: {e}\n")
            continue

        try:
            result = post_draft(page["title"], page["slug"], content)
            pid = result["id"]
            link = result.get("link", "?")
            print(f"  Draft posted: ID {pid}")
        except Exception as e:
            print(f"  FAILED to post: {e}\n")
            continue

        set_seo(pid, page)
        print(f"  SEO meta set")
        print(f"  URL: {link}\n")
        time.sleep(2)

    print("Done. Review drafts in WP Admin > Pages > Drafts, then publish when ready.")


if __name__ == "__main__":
    main()
