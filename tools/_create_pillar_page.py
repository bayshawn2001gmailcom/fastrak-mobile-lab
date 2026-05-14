"""
Create the "at home blood draw service near me" pillar page + wire up city page links.
Run: python tools/_create_pillar_page.py
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
    sys.exit("Error: WP_USER / WP_APP_PASSWORD missing from ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H_JSON = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
H_FORM = {"Authorization": f"Basic {creds}"}

SLUG         = "at-home-blood-draw-service"
TITLE        = "At-Home Blood Draw Service Near Me | Fastrak Mobile Lab"
FOCUS_KW     = "at home blood draw service near me"
SEO_TITLE    = "At-Home Blood Draw Service Near Me | Fastrak Mobile Lab"
META_DESC    = (
    "Skip the waiting room. Fastrak Mobile Lab sends a certified phlebotomist "
    "to your home across metro Atlanta, GA. Book your at-home blood draw today."
)
BOOKING_URL  = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"
PILLAR_URL   = f"{WP_SITE}/{SLUG}/"
PILLAR_MARKER = "<!-- fastrak-pillar-link -->"

# All Gwinnett + metro city pages to link from the pillar
CITY_LINKS = [
    ("Lawrenceville, GA", "/mobile-phlebotomy-dna-testing-lawrenceville-ga/"),
    ("Lilburn, GA",       "/mobile-phlebotomy-lilburn-ga/"),
    ("Snellville, GA",    "/mobile-phlebotomy-snellville-ga/"),
    ("Grayson, GA",       "/mobile-phlebotomy-dna-testing-grayson-ga/"),
    ("Loganville, GA",    "/mobile-phlebotomy-dna-testing-loganville-ga/"),
    ("Suwanee, GA",       "/mobile-phlebotomy-suwanee-ga/"),
    ("Sugar Hill, GA",    "/mobile-phlebotomy-sugar-hill-ga/"),
    ("Norcross, GA",      "/mobile-phlebotomy-norcross-ga/"),
    ("Buford, GA",        "/mobile-phlebotomy-buford-ga/"),
    ("Duluth, GA",        "/mobile-phlebotomy-duluth-ga/"),
    ("Gwinnett County",   "/mobile-phlebotomy-gwinnett-county-ga/"),
    ("Atlanta, GA",       "/mobile-phlebotomy-services-atlanta/"),
    ("Decatur, GA",       "/mobile-phlebotomy-decatur-ga/"),
    ("Marietta, GA",      "/mobile-phlebotomy-marietta-ga/"),
    ("Sandy Springs, GA", "/mobile-phlebotomy-sandy-springs-ga/"),
    ("Smyrna, GA",        "/mobile-phlebotomy-smyrna-ga/"),
    ("Tucker, GA",        "/mobile-phlebotomy-tucker-ga/"),
    ("Stone Mountain, GA","/mobile-phlebotomy-stone-mountain-ga/"),
    ("Conyers, GA",       "/mobile-phlebotomy-conyers-ga/"),
]

city_list_html = "\n".join(
    f'  <li><a href="{WP_SITE}{path}">At-home blood draw in {name}</a></li>'
    for name, path in CITY_LINKS
)

CONTENT = f"""
<h1>At-Home Blood Draw Service Near You — Skip the Waiting Room</h1>

<p>Searching for an at-home blood draw service near you? Fastrak Mobile Lab sends a licensed, certified phlebotomist directly to your home, office, or senior living facility across metro Atlanta and Gwinnett County, GA. No waiting rooms. No commute. No scheduling around a lab's limited hours. You choose the time — we handle everything else.</p>

<h2>What Is an At-Home Blood Draw Service?</h2>

<p>An at-home blood draw service (also called mobile phlebotomy) brings the lab to you. Instead of driving to a Quest Diagnostics, LabCorp, or hospital outpatient lab and waiting your turn, a certified phlebotomist arrives at your address, performs your blood draw on-site, and transports your specimen to an accredited reference laboratory for processing. Your results are returned through your ordering physician or our secure online portal — typically within 24–72 hours.</p>

<p>At-home blood draw services are covered the same way as in-clinic draws: most major insurance plans cover the lab processing fee. The mobile convenience fee — the cost of the phlebotomist traveling to your location — is a separate, transparent charge. We'll give you the full breakdown before you book.</p>

<h2>Who Benefits Most from a Mobile Blood Draw?</h2>

<p>At-home blood draw services aren't just for one type of patient. Here's who we most commonly serve:</p>

<ul>
  <li><strong>Seniors and elderly patients</strong> — Driving to a lab is difficult or impossible for many older adults, especially those with mobility limitations or who no longer drive. We come to them.</li>
  <li><strong>Homebound and post-surgical patients</strong> — Recovery shouldn't require a trip out. Our phlebotomists are experienced working with patients healing at home.</li>
  <li><strong>Busy professionals</strong> — Early-morning and evening appointments mean you can get lab work done before or after work without losing half a day to a waiting room.</li>
  <li><strong>Parents with young children</strong> — Coordinating a lab visit with kids in tow is stressful. We come to your home on your schedule.</li>
  <li><strong>Patients with anxiety or needle phobia</strong> — Being in a familiar environment makes a significant difference for patients who find clinical settings stressful.</li>
  <li><strong>Corporate &amp; occupational health clients</strong> — We perform on-site drug testing, pre-employment screening, and wellness panels at offices throughout the Atlanta metro area.</li>
</ul>

<h2>Tests Available Through Our At-Home Blood Draw Service</h2>

<p>If your doctor has ordered it, we can collect it. Our mobile phlebotomists handle the full range of common laboratory panels, including:</p>

<ul>
  <li>Complete Blood Count (CBC)</li>
  <li>Comprehensive Metabolic Panel (CMP)</li>
  <li>Lipid panel (cholesterol screening)</li>
  <li>Thyroid function (TSH, T3, T4)</li>
  <li>Hormone panels (testosterone, estrogen, progesterone)</li>
  <li>HbA1c and diabetes monitoring</li>
  <li>Vitamin D, B12, and iron studies</li>
  <li>Sexually transmitted infection (STI) panels</li>
  <li>DNA &amp; paternity specimen collection (court-admissible and personal-knowledge)</li>
  <li>Specialty and reference lab panels — contact us to confirm your specific test</li>
</ul>

<h2>How Our At-Home Blood Draw Service Works</h2>

<ol>
  <li><strong>Book online</strong> — Select your service, choose a date and time, and enter your address. We serve homes, offices, and facilities throughout metro Atlanta and Gwinnett County.</li>
  <li><strong>We arrive at your door</strong> — A licensed Fastrak phlebotomist shows up on time with all necessary equipment. Most draws take under 10 minutes.</li>
  <li><strong>Results delivered</strong> — Your specimen is transported to our accredited partner lab. Results are available within 24–72 hours through your provider or our secure results portal.</li>
</ol>

<p style="margin-top:1.5em;"><a href="{BOOKING_URL}"><strong>Book Your At-Home Blood Draw Now</strong></a></p>

<h2>Service Areas — At-Home Blood Draw Near You</h2>

<p>Fastrak Mobile Lab provides at-home blood draw services throughout metro Atlanta, GA. Select your city below for local service details, zip codes, and availability:</p>

<ul>
{city_list_html}
</ul>

<h2>Frequently Asked Questions</h2>

<h3>How much does an at-home blood draw service cost near me?</h3>
<p>Lab processing fees are billed to your insurance the same way as any in-clinic draw — most major plans (Aetna, BCBS, Cigna, UnitedHealthcare, Humana) cover these fees. The mobile service fee, which covers the phlebotomist traveling to your location, is a separate out-of-pocket charge. We provide transparent pricing before you confirm your appointment.</p>

<h3>How do I find a blood draw service that comes to my home?</h3>
<p>Fastrak Mobile Lab serves the entire metro Atlanta and Gwinnett County area. Use the city links above to find service details for your specific location, or <a href="{WP_SITE}/contact/">contact us directly</a> to confirm coverage at your address. Most areas have same-day or next-day availability.</p>

<h3>Is the at-home blood draw as accurate as going to a lab?</h3>
<p>Yes — your specimen is processed by the same accredited reference laboratories used by Quest Diagnostics and LabCorp. Our phlebotomists follow the same collection protocols used in clinical settings, and all specimens are transported under proper handling conditions. Accuracy is identical to an in-clinic draw.</p>

<h3>Do I need a doctor's order for an at-home blood draw?</h3>
<p>For physician-ordered tests billed to insurance, yes — you'll need an order from your provider. If you'd like to order your own lab tests without a physician referral, we also offer direct-to-consumer testing through our <a href="{WP_SITE}/order-your-own-lab-tests-at-home/">order your own test</a> service.</p>

<h3>What areas near Atlanta do you serve for at-home blood draws?</h3>
<p>We serve metro Atlanta and Gwinnett County communities including Lawrenceville, Snellville, Lilburn, Grayson, Loganville, Suwanee, Duluth, Norcross, Buford, Decatur, Marietta, Sandy Springs, and more. See the full service area list above.</p>
""".strip()


# ---------------------------------------------------------------------------
# WordPress helpers
# ---------------------------------------------------------------------------

def check_slug(slug):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages",
                     headers=H_FORM,
                     params={"slug": slug, "status": "any"},
                     timeout=20)
    return r.json() if r.ok else []


def create_page():
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages",
                      headers=H_JSON,
                      json={"title": TITLE, "slug": SLUG,
                            "content": CONTENT, "status": "publish"},
                      timeout=30)
    r.raise_for_status()
    return r.json()


def set_rank_math(post_id):
    r = requests.post(f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
                      headers=H_FORM,
                      data={
                          "objectID": post_id,
                          "objectType": "post",
                          "meta[rank_math_focus_keyword]": FOCUS_KW,
                          "meta[rank_math_title]": SEO_TITLE,
                          "meta[rank_math_description]": META_DESC,
                      },
                      timeout=20)
    return r.status_code


def get_raw(pid):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                     headers=H_FORM,
                     params={"context": "edit", "_fields": "content"},
                     timeout=20)
    r.raise_for_status()
    return r.json()["content"]["raw"]


def patch_content(pid, raw):
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                      headers=H_JSON,
                      json={"content": raw},
                      timeout=30)
    r.raise_for_status()
    return r.status_code


# ---------------------------------------------------------------------------
# City pages to back-link to the pillar
# ---------------------------------------------------------------------------

# All city/hub page IDs to link back to pillar
BACKLINK_PAGES = [
    (1249, "Gwinnett County Hub"),
    (1377, "Lawrenceville"),
    (1334, "Lilburn"),
    (1248, "Snellville"),
    (1382, "Grayson"),
    (1383, "Loganville"),
    (1332, "Suwanee"),
    (1333, "Sugar Hill"),
    (1258, "Norcross"),
    (1328, "Buford"),
    (1250, "Duluth"),
    (1249, "Gwinnett Hub"),
]

PILLAR_BLOCK = (
    f"\n{PILLAR_MARKER}\n"
    f'<p>Learn more about our <a href="{PILLAR_URL}">at-home blood draw service</a> '
    f"— available across metro Atlanta with same-day availability in many areas.</p>"
)


def add_pillar_link(pid, name):
    raw = get_raw(pid)
    if PILLAR_MARKER in raw or SLUG in raw:
        print(f"  [{name}] already links to pillar — skipped")
        return "skipped"
    new_raw = raw.rstrip() + PILLAR_BLOCK
    status = patch_content(pid, new_raw)
    print(f"  [{name}] pillar link added — HTTP {status}")
    return f"HTTP {status}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Step 1: Create or find the pillar page
    print(f"Checking slug '{SLUG}'...")
    existing = check_slug(SLUG)
    if existing:
        page = existing[0]
        post_id = page["id"]
        link = page.get("link", "?")
        print(f"Already exists: ID {post_id} -> {link}")
    else:
        print("Creating pillar page...")
        result = create_page()
        post_id = result["id"]
        link = result.get("link", "?")
        print(f"  Created ID {post_id} -> {link}")

    # Step 2: Set Rank Math
    print("Setting Rank Math SEO metadata...")
    rm_status = set_rank_math(post_id)
    print(f"  Rank Math HTTP {rm_status}")

    # Step 3: Add backlinks from city pages to pillar
    print("\nAdding pillar backlinks to city pages...")
    seen = set()
    for pid, name in BACKLINK_PAGES:
        if pid in seen:
            continue
        seen.add(pid)
        add_pillar_link(pid, name)

    print(f"\nDone.")
    print(f"  Pillar URL:  {link}")
    print(f"  Focus KW:    {FOCUS_KW}")
    print(f"  Meta title:  {SEO_TITLE} ({len(SEO_TITLE)} chars)")
    print(f"  Meta desc:   {META_DESC} ({len(META_DESC)} chars)")


if __name__ == "__main__":
    main()
