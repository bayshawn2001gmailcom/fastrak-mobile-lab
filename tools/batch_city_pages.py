"""
Batch generate and post 10 new city landing pages as WordPress drafts.
Run: python tools/batch_city_pages.py
"""
import os, sys, time, base64, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

# Inline imports from content_generator to avoid subprocess overhead
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not GEMINI_API_KEY:
    sys.exit("Error: GEMINI_API_KEY missing from ~/.env")
if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER / WP_APP_PASSWORD missing from ~/.env")

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
WP_HEADERS = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

CITIES = [
    {"city": "Suwanee",    "county": "Gwinnett County", "slug": "mobile-phlebotomy-suwanee-ga"},
    {"city": "Sugar Hill", "county": "Gwinnett County", "slug": "mobile-phlebotomy-sugar-hill-ga"},
    {"city": "Lilburn",    "county": "Gwinnett County", "slug": "mobile-phlebotomy-lilburn-ga"},
    {"city": "Clarkston",  "county": "DeKalb County",   "slug": "mobile-phlebotomy-clarkston-ga"},
]

LOCATION_PROMPT = """
You are writing an SEO-optimized location page for Fastrak Mobile Lab, a licensed mobile phlebotomy service in Georgia.

CRITICAL RULES:
- This is a SERVICE AREA BUSINESS. We travel TO the client. NEVER mention a physical office or business address.
- Always frame it as "we come to you in {city}" — not "visit our lab in {city}"
- Never say "our office", "our facility", "located in", or include any street address
- Do mention the city name naturally multiple times to establish local relevance

Business context:
- Name: Fastrak Mobile Lab
- Services: mobile phlebotomy, in-home blood draw, drug testing, DNA specimen collection
- We serve {city}, {county}, GA and surrounding metro Atlanta communities
- Licensed, certified phlebotomists
- Fast results (most within 24-72 hours)
- Lab processing fees are covered by most major insurance plans; a separate mobile convenience fee is NOT covered by insurance
- CTA: "Book your mobile blood draw" — link placeholder: [BOOKING_LINK]

Write a location page for: Mobile Phlebotomy in {city}, GA

Requirements:
- H1: "Mobile Phlebotomy in {city}, GA" (exact)
- First paragraph: hook + primary keyword + "we come to you" framing
- H2 #1: "How Mobile Phlebotomy Works in {city}" — explain the process (schedule, we arrive, draw blood, send to lab)
- H2 #2: "Who We Serve in {city}" — patients, elderly, homebound, professionals, corporate clients
- H2 #3: "Why {city} Residents Choose Fastrak Mobile Lab" — trust signals, speed, licensed staff, lab results covered by insurance (but clarify the mobile fee is separate)
- FAQ section (H2: "Frequently Asked Questions") with 3 questions relevant to {city} residents
- Closing CTA paragraph with booking link placeholder
- Word count: 600-750 words
- Output clean HTML only (h1, h2, h3, p, ul, li tags — no divs, no inline styles, no markdown)
- Do NOT include <html>, <head>, or <body> tags — just the content tags
"""


def generate_content(city, county, retries=4):
    prompt = LOCATION_PROMPT.format(city=city, county=county)
    model = genai.GenerativeModel("gemini-2.0-flash")
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text.rsplit("```", 1)[0]
            return text.strip()
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited — waiting {wait}s before retry {attempt+2}/{retries}...")
                time.sleep(wait)
            else:
                raise


def check_slug_exists(slug):
    resp = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/pages",
        headers=WP_HEADERS,
        params={"slug": slug, "status": "any"},
        timeout=20,
    )
    return bool(resp.json()) if resp.ok else False


def post_draft(title, slug, content):
    resp = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/pages",
        headers=WP_HEADERS,
        json={"title": title, "slug": slug, "content": content, "status": "draft"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def set_seo_meta(post_id, city, slug):
    keyword = f"mobile phlebotomy {city.lower()} ga"
    seo_title = f"Mobile Phlebotomy in {city}, GA | Fastrak Mobile Lab"
    meta_desc = (
        f"Need a blood draw in {city}, GA? Fastrak Mobile Lab sends a licensed phlebotomist "
        f"to your home or office. Book mobile phlebotomy in {city} today."
    )
    # Keep title under 60 chars
    if len(seo_title) > 60:
        seo_title = f"Mobile Phlebotomy {city} GA | Fastrak Mobile Lab"

    requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=WP_HEADERS,
        data={
            "objectID": post_id,
            "objectType": "post",
            "meta[rank_math_focus_keyword]": keyword,
            "meta[rank_math_title]": seo_title,
            "meta[rank_math_description]": meta_desc[:155],
        },
        timeout=20,
    )


def main():
    log_lines = ["# City Pages Batch Log", ""]
    print(f"Generating {len(CITIES)} city pages as WordPress drafts...\n")

    for entry in CITIES:
        city = entry["city"]
        county = entry["county"]
        slug = entry["slug"]
        title = f"Mobile Phlebotomy in {city}, GA"

        print(f"[{city}] Checking if slug exists...")
        if check_slug_exists(slug):
            print(f"[{city}] SKIPPED — /{slug} already exists\n")
            log_lines.append(f"- SKIPPED: {title} (slug `{slug}` already exists)")
            continue

        print(f"[{city}] Generating content...")
        try:
            content = generate_content(city, county)
            word_count = len(content.split())
            print(f"[{city}] Generated {word_count} words")
        except Exception as e:
            print(f"[{city}] FAILED to generate: {e}\n")
            log_lines.append(f"- FAILED (generate): {title} — {e}")
            continue

        print(f"[{city}] Posting draft to WordPress...")
        try:
            result = post_draft(title, slug, content)
            post_id = result["id"]
            link = result.get("link", "?")
            print(f"[{city}] Draft created: ID {post_id}")
        except Exception as e:
            print(f"[{city}] FAILED to post: {e}\n")
            log_lines.append(f"- FAILED (post): {title} — {e}")
            continue

        print(f"[{city}] Setting SEO metadata...")
        try:
            set_seo_meta(post_id, city, slug)
        except Exception as e:
            print(f"[{city}] SEO meta warning: {e}")

        log_lines.append(f"- DRAFT: [{title}]({link}) — ID {post_id} — `/{slug}`")
        print(f"[{city}] Done. URL: {link}\n")

        time.sleep(1.5)  # brief pause between API calls

    # Write log
    log_path = Path(".tmp/city_pages_batch_log.md")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"Log written to {log_path}")
    print("\nAll done. Review drafts in WP Admin > Pages > Drafts, then publish when ready.")


if __name__ == "__main__":
    main()
