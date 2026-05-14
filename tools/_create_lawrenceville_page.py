"""
One-shot script: create the Lawrenceville, GA city landing page on WordPress.
Focus keyword: mobile blood draw Lawrenceville GA
Run: python tools/_create_lawrenceville_page.py
"""
import os, sys, base64, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER / WP_APP_PASSWORD missing from ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

SLUG = "mobile-phlebotomy-dna-testing-lawrenceville-ga"
TITLE = "Mobile Phlebotomy & DNA Testing in Lawrenceville, GA"
FOCUS_KEYWORD = "mobile blood draw Lawrenceville GA"
SEO_TITLE = "Mobile Blood Draw in Lawrenceville, GA — We Come to You"
META_DESC = (
    "Skip the wait — Fastrak Mobile Lab brings certified phlebotomy & DNA testing "
    "directly to your door in Lawrenceville, GA. Same-day available."
)
BOOKING_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"

CONTENT = """
<h1>Mobile Blood Draw in Lawrenceville, GA — We Come to You</h1>

<p>Tired of driving across Gwinnett County, signing in, and sitting in a waiting room just to get a blood draw? Fastrak Mobile Lab sends a licensed, certified phlebotomist directly to your home, office, or assisted living facility in Lawrenceville, GA — so you skip the wait entirely. Whether you need routine bloodwork, specialized lab panels, or confidential DNA testing, we bring the lab to you.</p>

<h2>Why Lawrenceville Residents Choose Fastrak Mobile Lab</h2>

<p>Lawrenceville is one of Gwinnett County's fastest-growing communities, and residents here deserve lab services that match their pace. Here's why local patients, families, and healthcare providers trust Fastrak Mobile Lab:</p>

<ul>
  <li><strong>Certified phlebotomists</strong> — Every draw is performed by a licensed, experienced professional.</li>
  <li><strong>Fast turnaround</strong> — Most lab results are returned within 24–72 hours through our partner reference laboratories.</li>
  <li><strong>Insurance-friendly</strong> — Lab processing fees are covered by most major insurance plans. (Note: the mobile convenience fee is a separate charge not covered by insurance.)</li>
  <li><strong>No waiting rooms</strong> — We come to you on your schedule, including early mornings and evenings.</li>
  <li><strong>Discreet &amp; confidential</strong> — Particularly important for DNA/paternity testing — results are handled with complete privacy.</li>
</ul>

<h2>Our Services in Lawrenceville</h2>

<ul>
  <li><strong>Mobile Blood Draw</strong> — Routine CBC, metabolic panels, lipid profiles, hormone levels, and more — drawn at your location.</li>
  <li><strong>At-Home Lab Testing</strong> — We collect your specimen and route it to an accredited reference lab. No standing in line, no commute.</li>
  <li><strong>DNA &amp; Paternity Testing</strong> — Court-admissible and personal-knowledge DNA specimen collection performed discreetly at your home or chosen location in Lawrenceville.</li>
</ul>

<h2>How It Works</h2>

<ol>
  <li><strong>Book online</strong> — Select your service, date, and time. We'll confirm your Lawrenceville address.</li>
  <li><strong>We arrive at your door</strong> — A certified Fastrak phlebotomist arrives at your scheduled time with all necessary equipment.</li>
  <li><strong>Results delivered</strong> — Your specimen is transported to our partner lab. Most results are available within 24–72 hours via your provider or our secure results portal.</li>
</ol>

<h2>Service Area — Lawrenceville Zip Codes</h2>

<p>Fastrak Mobile Lab serves all Lawrenceville, GA neighborhoods including the following zip codes:</p>

<ul>
  <li>30043</li>
  <li>30044</li>
  <li>30045</li>
  <li>30046</li>
</ul>

<p>We also serve neighboring communities in Gwinnett County including Snellville, Lilburn, Grayson, and Loganville. Not sure if we cover your area? <a href="https://fastrakmobilelab.com/contact/">Contact us</a> and we'll confirm coverage.</p>

<p style="margin-top:2em;"><strong>Ready to skip the waiting room?</strong><br>
<a href="{booking_url}" rel="noopener"><strong>Book Your Home Visit Today →</strong></a></p>

<h2>Frequently Asked Questions</h2>

<h3>Do you accept insurance for mobile blood draws in Lawrenceville?</h3>
<p>Lab processing fees are billed to most major insurance plans (Aetna, BlueCross BlueShield, Cigna, UnitedHealthcare, and more). The mobile service fee — which covers our phlebotomist traveling to your location — is a separate charge not covered by insurance. We'll give you a full cost breakdown when you book.</p>

<h3>How quickly can you come to my home in Lawrenceville?</h3>
<p>Many appointments are available within 24–48 hours. We offer early-morning and evening slots to fit your schedule. Same-day availability is possible depending on your zip code and service request.</p>

<h3>Is DNA and paternity testing available at home in Lawrenceville, GA?</h3>
<p>Yes. We offer at-home DNA specimen collection for both personal-knowledge testing and court-admissible paternity testing. All collections follow strict chain-of-custody procedures, and results are handled with complete confidentiality.</p>
""".replace("{booking_url}", BOOKING_URL).strip()


def check_slug_exists(slug):
    resp = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/pages",
        headers=HEADERS,
        params={"slug": slug, "status": "any"},
        timeout=20,
    )
    return resp.json() if resp.ok else []


def create_page():
    resp = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/pages",
        headers=HEADERS,
        json={"title": TITLE, "slug": SLUG, "content": CONTENT, "status": "publish"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def set_rank_math(post_id):
    resp = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=HEADERS,
        data={
            "objectID": post_id,
            "objectType": "post",
            "meta[rank_math_focus_keyword]": FOCUS_KEYWORD,
            "meta[rank_math_title]": SEO_TITLE,
            "meta[rank_math_description]": META_DESC,
        },
        timeout=20,
    )
    return resp.status_code, resp.text


def main():
    print(f"Checking if slug '{SLUG}' already exists...")
    existing = check_slug_exists(SLUG)
    if existing:
        page = existing[0]
        print(f"Page already exists: ID {page['id']} — {page.get('link')}")
        print("Updating SEO meta only...")
        status, body = set_rank_math(page["id"])
        print(f"  Rank Math → HTTP {status}")
        print(f"\nPage URL: {page.get('link')}")
        return

    print("Creating page...")
    result = create_page()
    post_id = result["id"]
    link = result.get("link", "?")
    print(f"  Created: ID {post_id}")
    print(f"  URL: {link}")

    print("Setting Rank Math SEO metadata...")
    status, body = set_rank_math(post_id)
    print(f"  Rank Math → HTTP {status}")
    if status not in (200, 201):
        print(f"  Response: {body[:300]}")

    print(f"\nDone.")
    print(f"  Page URL: {link}")
    print(f"  Focus keyword: {FOCUS_KEYWORD}")
    print(f"  SEO title: {SEO_TITLE}")
    print(f"  Meta desc ({len(META_DESC)} chars): {META_DESC}")
    return post_id, link


if __name__ == "__main__":
    main()
