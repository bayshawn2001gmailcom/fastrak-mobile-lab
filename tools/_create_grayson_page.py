"""
One-shot script: create the Grayson, GA city landing page on WordPress.
Focus keyword: mobile blood draw Grayson GA
Run: python tools/_create_grayson_page.py
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
HEADERS_FORM = {"Authorization": f"Basic {creds}"}

SLUG = "mobile-phlebotomy-dna-testing-grayson-ga"
TITLE = "Mobile Phlebotomy & DNA Testing in Grayson, GA"
FOCUS_KEYWORD = "mobile blood draw Grayson GA"
SEO_TITLE = "Mobile Blood Draw in Grayson, GA - We Come to You"
META_DESC = (
    "Skip the wait - Fastrak Mobile Lab sends a certified phlebotomist to your door "
    "in Grayson, GA. Mobile blood draw & DNA testing available."
)
BOOKING_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"

CONTENT = f"""
<h1>Mobile Blood Draw in Grayson, GA — We Come to You</h1>

<p>If you live in Grayson, GA and need lab work done, you no longer have to drive to a clinic, sit in a waiting room, or work around a lab's limited hours. Fastrak Mobile Lab sends a licensed, certified phlebotomist directly to your home, office, or senior living community in Grayson — so you get your blood draw done on your schedule, without leaving your front door.</p>

<h2>Why Grayson Residents Choose Fastrak Mobile Lab</h2>

<p>Grayson is a tight-knit community in eastern Gwinnett County, and residents here value convenience and personal service. Here's why Fastrak Mobile Lab is the trusted choice for mobile blood draws and at-home lab testing in the Grayson area:</p>

<ul>
  <li><strong>Licensed, certified phlebotomists</strong> — Every draw is performed by a trained professional with real clinical experience.</li>
  <li><strong>Results in 24–72 hours</strong> — Specimens are routed to an accredited reference lab and results are returned quickly through your provider or our secure portal.</li>
  <li><strong>Insurance-friendly</strong> — Lab processing fees are covered by most major insurance plans. The mobile travel fee is a separate charge not covered by insurance — we'll be upfront about pricing when you book.</li>
  <li><strong>We come to you</strong> — Home, office, assisted living, or wherever is most convenient for you in Grayson.</li>
  <li><strong>Confidential DNA &amp; paternity testing</strong> — Discreet at-home collection with strict chain-of-custody procedures.</li>
</ul>

<h2>Our Services in Grayson</h2>

<ul>
  <li><strong>Mobile Blood Draw</strong> — CBC, comprehensive metabolic panel, lipid profile, thyroid, hormone levels, and more — all collected at your location in Grayson.</li>
  <li><strong>At-Home Lab Testing</strong> — We collect your specimen and transport it to our partner reference lab. No commute, no waiting room.</li>
  <li><strong>DNA &amp; Paternity Testing</strong> — Court-admissible and personal-knowledge DNA specimen collection performed privately at your Grayson address.</li>
</ul>

<h2>How It Works</h2>

<ol>
  <li><strong>Book online</strong> — Select your service and a time that works for you. We'll confirm your Grayson address.</li>
  <li><strong>We come to your door</strong> — A certified Fastrak phlebotomist arrives on time with all equipment needed for your draw.</li>
  <li><strong>Results delivered</strong> — Your specimen goes straight to the lab. Most results are back in 24–72 hours.</li>
</ol>

<h2>Service Area — Grayson Zip Code</h2>

<p>Fastrak Mobile Lab serves all of Grayson, GA including zip code <strong>30017</strong>. We also cover neighboring communities in eastern Gwinnett County including Loganville, Snellville, and Lawrenceville. Not sure if we reach your address? <a href="https://fastrakmobilelab.com/contact/">Contact us</a> and we'll confirm.</p>

<p style="margin-top:2em;"><strong>Ready to skip the waiting room?</strong><br>
<a href="{BOOKING_URL}"><strong>Book Your Home Visit Today</strong></a></p>

<h2>Frequently Asked Questions</h2>

<h3>Do you accept insurance for home blood draws in Grayson, GA?</h3>
<p>Yes — lab processing fees are billed to most major insurance plans including Aetna, BlueCross BlueShield, Cigna, and UnitedHealthcare. The mobile service fee (the cost of our phlebotomist traveling to Grayson) is a separate charge not covered by insurance. We'll provide a full cost breakdown before you book.</p>

<h3>How soon can you come to Grayson?</h3>
<p>Most appointments are available within 24–48 hours. We offer early-morning and evening slots to fit your schedule. Same-day availability depends on your specific service and location within the 30017 zip code area.</p>

<h3>Can I get a DNA or paternity test done at home in Grayson?</h3>
<p>Yes. We offer at-home DNA specimen collection for both personal-knowledge and court-admissible paternity testing. All collections follow strict chain-of-custody procedures, and all results are handled with complete confidentiality.</p>
""".strip()


def check_slug_exists(slug):
    resp = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/pages",
        headers=HEADERS_FORM,
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
        headers=HEADERS_FORM,
        data={
            "objectID": post_id,
            "objectType": "post",
            "meta[rank_math_focus_keyword]": FOCUS_KEYWORD,
            "meta[rank_math_title]": SEO_TITLE,
            "meta[rank_math_description]": META_DESC,
        },
        timeout=20,
    )
    return resp.status_code


def main():
    print(f"Checking slug '{SLUG}'...")
    existing = check_slug_exists(SLUG)
    if existing:
        page = existing[0]
        print(f"Already exists: ID {page['id']} -> {page.get('link')}")
        print("Updating Rank Math only...")
        set_rank_math(page["id"])
        return page["id"], page.get("link")

    print("Creating page...")
    result = create_page()
    post_id = result["id"]
    link = result.get("link", "?")
    print(f"  Created ID {post_id} -> {link}")

    print("Setting Rank Math SEO metadata...")
    status = set_rank_math(post_id)
    print(f"  Rank Math HTTP {status}")

    print(f"\nDone.")
    print(f"  URL:     {link}")
    print(f"  Keyword: {FOCUS_KEYWORD}")
    print(f"  Title:   {SEO_TITLE}")
    print(f"  Desc:    {META_DESC}")
    return post_id, link


if __name__ == "__main__":
    main()
