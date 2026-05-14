"""
One-shot script: create the Loganville, GA city landing page on WordPress.
Focus keyword: mobile blood draw Loganville GA
Run: python tools/_create_loganville_page.py
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

SLUG = "mobile-phlebotomy-dna-testing-loganville-ga"
TITLE = "Mobile Phlebotomy & DNA Testing in Loganville, GA"
FOCUS_KEYWORD = "mobile blood draw Loganville GA"
SEO_TITLE = "Mobile Blood Draw in Loganville, GA - We Come to You"
META_DESC = (
    "Skip the wait - Fastrak Mobile Lab sends a certified phlebotomist to your door "
    "in Loganville, GA. Mobile blood draw & DNA testing available."
)
BOOKING_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"

CONTENT = f"""
<h1>Mobile Blood Draw in Loganville, GA — We Come to You</h1>

<p>Getting lab work done in Loganville, GA used to mean driving out to a clinic and sitting in a waiting room. Fastrak Mobile Lab changes that entirely — we send a licensed, certified phlebotomist directly to your home, office, or senior living facility in Loganville so you can get your blood draw done without ever leaving your front door. Convenient, professional, and on your schedule.</p>

<h2>Why Loganville Residents Choose Fastrak Mobile Lab</h2>

<p>Loganville sits at the edge of Walton and Gwinnett counties, and residents here know that quality healthcare options can sometimes require a long drive. Fastrak Mobile Lab eliminates that barrier entirely. Here's why Loganville patients and families trust us:</p>

<ul>
  <li><strong>Licensed, certified phlebotomists</strong> — Every draw is performed by a trained, experienced professional.</li>
  <li><strong>Fast results</strong> — Most lab results are returned within 24–72 hours through our partner reference laboratories.</li>
  <li><strong>Insurance-friendly</strong> — Lab processing fees are covered by most major insurance plans. The mobile travel fee is a separate charge not covered by insurance — we'll give you a clear cost breakdown upfront.</li>
  <li><strong>We travel to you</strong> — Home, office, or assisted living in the Loganville area — wherever is most convenient.</li>
  <li><strong>Private DNA &amp; paternity testing</strong> — Discreet, at-home collection with strict chain-of-custody handling.</li>
</ul>

<h2>Our Services in Loganville</h2>

<ul>
  <li><strong>Mobile Blood Draw</strong> — CBC, comprehensive metabolic panel, lipid profile, thyroid, hormone panels, and more — all collected at your Loganville location.</li>
  <li><strong>At-Home Lab Testing</strong> — We collect your specimen and transport it directly to an accredited reference lab. No commute, no waiting room, no hassle.</li>
  <li><strong>DNA &amp; Paternity Testing</strong> — Court-admissible and personal-knowledge DNA specimen collection done privately at your address in Loganville.</li>
</ul>

<h2>How It Works</h2>

<ol>
  <li><strong>Book online</strong> — Choose your service, date, and time. We'll confirm your Loganville address at booking.</li>
  <li><strong>We arrive at your door</strong> — A certified Fastrak phlebotomist comes to you with all necessary equipment.</li>
  <li><strong>Results delivered</strong> — Your specimen goes straight to the lab. Most results are ready in 24–72 hours via your provider or our secure results portal.</li>
</ol>

<h2>Service Area — Loganville Zip Code</h2>

<p>Fastrak Mobile Lab serves all of Loganville, GA including zip code <strong>30052</strong>. We also serve neighboring communities including Grayson, Snellville, Lawrenceville, and Monroe. Unsure if we cover your specific address? <a href="https://fastrakmobilelab.com/contact/">Contact us</a> and we'll confirm right away.</p>

<p style="margin-top:2em;"><strong>Ready to skip the waiting room?</strong><br>
<a href="{BOOKING_URL}"><strong>Book Your Home Visit Today</strong></a></p>

<h2>Frequently Asked Questions</h2>

<h3>Does insurance cover mobile blood draws in Loganville, GA?</h3>
<p>Lab processing fees are billed to most major insurance plans including Aetna, BlueCross BlueShield, Cigna, and UnitedHealthcare. The mobile convenience fee — which covers our phlebotomist traveling to your Loganville location — is a separate out-of-pocket charge. We'll provide a full breakdown before you confirm your appointment.</p>

<h3>How quickly can you come to Loganville?</h3>
<p>Most appointments are available within 24–48 hours. We offer early-morning and evening time slots to fit around work and family schedules. Same-day availability depends on your specific service and the 30052 zip code area.</p>

<h3>Can I get a DNA or paternity test at home in Loganville?</h3>
<p>Yes. We offer at-home DNA specimen collection for both personal-knowledge and court-admissible paternity testing. All collections follow strict chain-of-custody procedures, and every result is handled with complete confidentiality.</p>
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
