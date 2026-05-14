"""
Create 3 missing city pages: Decatur, Marietta, Sandy Springs.
These pages are linked from the pillar page but didn't exist yet.
Run: python tools/_create_decatur_marietta_sandysprings.py
"""
import os, sys, base64, requests
from pathlib import Path

home_env = Path.home() / ".env"
if home_env.exists():
    for line in home_env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Missing WP credentials")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H_JSON = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
H_FORM = {"Authorization": f"Basic {creds}"}

BOOKING_URL   = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"
PILLAR_URL    = f"{WP_SITE}/at-home-blood-draw-service/"
PILLAR_MARKER = "<!-- fastrak-pillar-link -->"

PILLAR_BLOCK = (
    f"\n{PILLAR_MARKER}\n"
    f'<p>Learn more about our <a href="{PILLAR_URL}">at-home blood draw service</a>'
    f" — available across metro Atlanta with same-day availability in many areas.</p>"
)

# ---------------------------------------------------------------------------
# Page definitions
# ---------------------------------------------------------------------------

PAGES = [
    {
        "slug":    "mobile-phlebotomy-decatur-ga",
        "title":   "Mobile Phlebotomy & Blood Draw in Decatur, GA",
        "focus_kw": "mobile blood draw Decatur GA",
        "seo_title": "Mobile Blood Draw in Decatur, GA - We Come to You | Fastrak",
        "meta_desc": (
            "Skip the lab. Fastrak Mobile Lab sends a certified phlebotomist to your "
            "door in Decatur, GA. Mobile blood draws & DNA testing, same-day available."
        ),
        "content": f"""
<h1>Mobile Blood Draw in Decatur, GA — We Come to You</h1>

<p>Need lab work done in Decatur, GA? Fastrak Mobile Lab sends a licensed, certified phlebotomist directly to your home, office, or senior living facility — no waiting rooms, no commute, no hassle. You choose the time and place; we handle everything else.</p>

<h2>Why Decatur Residents Choose Fastrak Mobile Lab</h2>

<p>Decatur's close proximity to Atlanta makes it one of the most active healthcare markets in the state, but busy schedules, traffic, and limited parking around local labs make in-person visits a frustrating experience. Fastrak Mobile Lab eliminates that friction entirely. Here's why Decatur patients trust us:</p>

<ul>
  <li><strong>Licensed, certified phlebotomists</strong> — Every draw is performed by a trained professional with experience across routine and specialty collections.</li>
  <li><strong>Fast results</strong> — Most lab results are returned within 24–72 hours through our accredited partner reference laboratories.</li>
  <li><strong>Insurance-friendly</strong> — Lab processing fees are covered by most major insurance plans. The mobile travel fee is a separate out-of-pocket charge — we provide a full cost breakdown before you confirm.</li>
  <li><strong>We travel to you</strong> — Home, office, hotel, or assisted living facility in Decatur and surrounding DeKalb County.</li>
  <li><strong>DNA &amp; paternity testing</strong> — Discreet, at-home specimen collection with full chain-of-custody compliance.</li>
</ul>

<h2>Services Available in Decatur, GA</h2>

<ul>
  <li><strong>Mobile Blood Draw</strong> — CBC, comprehensive metabolic panel, lipid profile, thyroid, hormone panels, HbA1c, STI panels, and more — all collected at your Decatur address.</li>
  <li><strong>At-Home Lab Testing</strong> — We collect your physician-ordered specimen and transport it directly to an accredited reference lab for processing.</li>
  <li><strong>DNA &amp; Paternity Testing</strong> — Court-admissible and personal-knowledge DNA specimen collection performed privately at your location.</li>
  <li><strong>Pre-Employment &amp; Drug Testing</strong> — Mobile drug screening for employers and individuals throughout Decatur and DeKalb County.</li>
</ul>

<h2>How It Works</h2>

<ol>
  <li><strong>Book online</strong> — Select your service, choose a date and time, and enter your Decatur address. Same-day and next-day slots are available.</li>
  <li><strong>We arrive at your door</strong> — A licensed Fastrak phlebotomist shows up on time with all necessary equipment. Most collections take under 10 minutes.</li>
  <li><strong>Results delivered</strong> — Your specimen goes straight to the lab. Results are returned within 24–72 hours through your provider or our secure results portal.</li>
</ol>

<p style="margin-top:1.5em;"><a href="{BOOKING_URL}"><strong>Book Your Mobile Blood Draw in Decatur</strong></a></p>

<h2>Service Area — Decatur, GA Zip Codes</h2>

<p>Fastrak Mobile Lab serves all of Decatur, GA including zip codes <strong>30030, 30032, 30033, 30034, and 30035</strong>. We also serve surrounding DeKalb County communities including Atlanta, Stone Mountain, Avondale Estates, Clarkston, and Tucker. Not sure if we cover your exact address? <a href="{WP_SITE}/contact/">Contact us</a> and we'll confirm right away.</p>

<h2>Frequently Asked Questions</h2>

<h3>Does insurance cover mobile blood draws in Decatur, GA?</h3>
<p>Lab processing fees are billed to most major insurance plans including Aetna, BlueCross BlueShield, Cigna, and UnitedHealthcare — the same way as any in-clinic draw. The mobile convenience fee covering our phlebotomist's travel to your Decatur location is a separate out-of-pocket charge. We provide full pricing transparency before you confirm your appointment.</p>

<h3>How quickly can you come to Decatur?</h3>
<p>Most appointments are available within 24–48 hours across all Decatur zip codes including 30030, 30032, 30033, 30034, and 30035. Early-morning and evening time slots are available. Same-day availability depends on your specific service type and scheduling window.</p>

<h3>Can I get DNA or paternity testing at home in Decatur, GA?</h3>
<p>Yes. We offer at-home DNA specimen collection for both personal-knowledge and court-admissible paternity testing throughout Decatur. All collections follow strict chain-of-custody procedures with complete confidentiality at every step.</p>
""".strip(),
    },
    {
        "slug":    "mobile-phlebotomy-marietta-ga",
        "title":   "Mobile Phlebotomy & Blood Draw in Marietta, GA",
        "focus_kw": "mobile blood draw Marietta GA",
        "seo_title": "Mobile Blood Draw in Marietta, GA - We Come to You | Fastrak",
        "meta_desc": (
            "Skip the waiting room. Fastrak Mobile Lab sends a certified phlebotomist "
            "to your home in Marietta, GA. Mobile blood draws & DNA testing available."
        ),
        "content": f"""
<h1>Mobile Blood Draw in Marietta, GA — We Come to You</h1>

<p>Getting lab work done in Marietta, GA shouldn't mean sitting in a crowded waiting room or fighting traffic to reach a draw site. Fastrak Mobile Lab sends a licensed, certified phlebotomist directly to your home, office, or facility in Marietta — on your schedule, with no waiting room required.</p>

<h2>Why Marietta Residents Choose Fastrak Mobile Lab</h2>

<p>Marietta is one of Cobb County's largest and most active communities. Between work, family, and traffic on I-75 and I-285, scheduling a lab visit during clinic hours is genuinely difficult. Fastrak Mobile Lab fits into your life instead of asking you to rearrange it around a clinic's schedule.</p>

<ul>
  <li><strong>Licensed, certified phlebotomists</strong> — Every blood draw is performed by a trained, experienced professional.</li>
  <li><strong>Results within 24–72 hours</strong> — Specimens are transported directly to our accredited partner reference laboratories for fast processing.</li>
  <li><strong>Insurance-friendly</strong> — Lab processing fees are covered by most major insurance plans. The mobile travel fee is a separate out-of-pocket charge — we provide transparent pricing upfront.</li>
  <li><strong>We come to you</strong> — Home, office, hotel, or senior living facility anywhere in Marietta and Cobb County.</li>
  <li><strong>DNA &amp; drug testing</strong> — At-home collection for paternity, legal DNA, and pre-employment or compliance drug testing.</li>
</ul>

<h2>Services Available in Marietta, GA</h2>

<ul>
  <li><strong>Mobile Blood Draw</strong> — CBC, comprehensive metabolic panel, lipid panel, thyroid, hormone levels, HbA1c, vitamin D, STI panels, and more — collected at your Marietta address.</li>
  <li><strong>At-Home Lab Testing</strong> — We collect physician-ordered specimens and transport them directly to an accredited reference lab. No commute, no waiting room.</li>
  <li><strong>DNA &amp; Paternity Testing</strong> — Court-admissible and personal-knowledge DNA specimen collection performed discreetly at your home or office.</li>
  <li><strong>Pre-Employment &amp; Drug Screening</strong> — Mobile drug testing for Marietta employers, staffing agencies, and HR teams with chain-of-custody compliance.</li>
</ul>

<h2>How It Works</h2>

<ol>
  <li><strong>Book online</strong> — Choose your service, pick a date and time, and enter your Marietta address. Same-day and next-day availability in most areas.</li>
  <li><strong>We arrive at your door</strong> — A licensed Fastrak phlebotomist comes to you with all necessary collection equipment. Most draws take under 10 minutes.</li>
  <li><strong>Results delivered</strong> — Your specimen is transported directly to the lab. Results are available within 24–72 hours through your provider or our secure results portal.</li>
</ol>

<p style="margin-top:1.5em;"><a href="{BOOKING_URL}"><strong>Book Your Mobile Blood Draw in Marietta</strong></a></p>

<h2>Service Area — Marietta, GA Zip Codes</h2>

<p>Fastrak Mobile Lab serves all of Marietta, GA including zip codes <strong>30060, 30062, 30064, 30066, 30067, and 30068</strong>. We also serve surrounding Cobb County communities including Smyrna, Kennesaw, Acworth, Vinings, and East Cobb. Not sure if we cover your specific address? <a href="{WP_SITE}/contact/">Contact us</a> and we'll confirm right away.</p>

<h2>Frequently Asked Questions</h2>

<h3>Does insurance cover mobile blood draws in Marietta, GA?</h3>
<p>Lab processing fees are billed to most major insurance plans — Aetna, BlueCross BlueShield, Cigna, UnitedHealthcare — the same way as an in-clinic draw. The mobile convenience fee for travel to your Marietta location is a separate out-of-pocket charge. We give you full pricing transparency before you book.</p>

<h3>How quickly can you come to Marietta?</h3>
<p>Most appointments are available within 24–48 hours across all Marietta zip codes including 30060, 30062, 30064, 30066, 30067, and 30068. Early-morning and evening slots are offered to fit your schedule. Same-day availability depends on service type and scheduling window.</p>

<h3>Can I get DNA or paternity testing at home in Marietta, GA?</h3>
<p>Yes. We provide at-home DNA and paternity specimen collection throughout Marietta for both personal-knowledge and court-admissible results. All collections follow strict chain-of-custody procedures with complete confidentiality.</p>
""".strip(),
    },
    {
        "slug":    "mobile-phlebotomy-sandy-springs-ga",
        "title":   "Mobile Phlebotomy & Blood Draw in Sandy Springs, GA",
        "focus_kw": "mobile blood draw Sandy Springs GA",
        "seo_title": "Mobile Blood Draw in Sandy Springs, GA - We Come to You | Fastrak",
        "meta_desc": (
            "Skip the waiting room. Fastrak Mobile Lab sends a certified phlebotomist "
            "to your home in Sandy Springs, GA. Mobile blood draws & DNA testing."
        ),
        "content": f"""
<h1>Mobile Blood Draw in Sandy Springs, GA — We Come to You</h1>

<p>Sandy Springs is one of the most affluent and busy communities in the Atlanta metro area — and one of the last places residents want to spend their morning in a lab waiting room. Fastrak Mobile Lab sends a licensed, certified phlebotomist directly to your home, office, or facility in Sandy Springs, so your lab work gets done without interrupting your day.</p>

<h2>Why Sandy Springs Residents Choose Fastrak Mobile Lab</h2>

<p>Sandy Springs sits at the intersection of Fulton County's most in-demand zip codes. Executives, families, seniors, and concierge medical practices throughout the community rely on Fastrak Mobile Lab for a higher standard of care — on demand, on their schedule.</p>

<ul>
  <li><strong>Licensed, certified phlebotomists</strong> — Every collection is performed by a trained professional who treats your home like a clinical setting.</li>
  <li><strong>Results within 24–72 hours</strong> — Specimens are delivered directly to our accredited partner reference laboratories for fast, accurate processing.</li>
  <li><strong>Insurance-friendly</strong> — Lab processing fees are covered by most major plans. The mobile travel fee is a separate, transparent out-of-pocket charge.</li>
  <li><strong>We come to you</strong> — Home, office, hotel, or assisted living facility throughout Sandy Springs and north Fulton County.</li>
  <li><strong>Concierge &amp; physician support</strong> — We work directly with concierge medical practices to extend in-home phlebotomy to their patient panels.</li>
</ul>

<h2>Services Available in Sandy Springs, GA</h2>

<ul>
  <li><strong>Mobile Blood Draw</strong> — CBC, comprehensive metabolic panel, lipid panel, thyroid, hormone panels, HbA1c, vitamin D, STI panels, and more — at your Sandy Springs address.</li>
  <li><strong>At-Home Lab Testing</strong> — We collect physician-ordered specimens and transport them directly to an accredited reference lab. No commute required.</li>
  <li><strong>DNA &amp; Paternity Testing</strong> — Court-admissible and personal-knowledge DNA specimen collection performed discreetly at your home or office.</li>
  <li><strong>Concierge &amp; Corporate Services</strong> — Premium at-home phlebotomy for concierge medical practices, executives, and corporate wellness programs throughout Sandy Springs.</li>
</ul>

<h2>How It Works</h2>

<ol>
  <li><strong>Book online</strong> — Select your service, pick a date and time, and enter your Sandy Springs address. Same-day and next-day slots are available.</li>
  <li><strong>We arrive at your door</strong> — A licensed Fastrak phlebotomist comes to you with all necessary collection equipment. Most draws are complete in under 10 minutes.</li>
  <li><strong>Results delivered</strong> — Your specimen is transported directly to the lab. Results are available within 24–72 hours through your provider or our secure results portal.</li>
</ol>

<p style="margin-top:1.5em;"><a href="{BOOKING_URL}"><strong>Book Your Mobile Blood Draw in Sandy Springs</strong></a></p>

<h2>Service Area — Sandy Springs, GA Zip Codes</h2>

<p>Fastrak Mobile Lab serves all of Sandy Springs, GA including zip codes <strong>30328, 30338, and 30350</strong>. We also serve surrounding north Fulton County communities including Dunwoody, Roswell, Buckhead, Brookhaven, and Perimeter Center. Not sure if we cover your specific address? <a href="{WP_SITE}/contact/">Contact us</a> and we'll confirm right away.</p>

<h2>Frequently Asked Questions</h2>

<h3>Does insurance cover mobile blood draws in Sandy Springs, GA?</h3>
<p>Lab processing fees are billed to most major insurance plans — Aetna, BlueCross BlueShield, Cigna, UnitedHealthcare — the same way as any in-clinic draw. The mobile convenience fee covering travel to your Sandy Springs location is a separate out-of-pocket charge. We provide full pricing transparency before you confirm your appointment.</p>

<h3>How quickly can you come to Sandy Springs?</h3>
<p>Most appointments are available within 24–48 hours across Sandy Springs zip codes 30328, 30338, and 30350. Early-morning and evening time slots are offered. Same-day availability depends on your specific service type and scheduling window.</p>

<h3>Can I get DNA or paternity testing at home in Sandy Springs, GA?</h3>
<p>Yes. We offer at-home DNA and paternity specimen collection throughout Sandy Springs for both personal-knowledge and court-admissible results. All collections follow strict chain-of-custody procedures with complete confidentiality.</p>
""".strip(),
    },
]

# ---------------------------------------------------------------------------
# WordPress helpers
# ---------------------------------------------------------------------------

def check_slug(slug):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages",
                     headers=H_FORM,
                     params={"slug": slug, "status": "any"},
                     timeout=20)
    return r.json() if r.ok else []


def create_page(p):
    content = p["content"].rstrip() + PILLAR_BLOCK
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages",
                      headers=H_JSON,
                      json={"title": p["title"], "slug": p["slug"],
                            "content": content, "status": "publish"},
                      timeout=30)
    r.raise_for_status()
    return r.json()


def set_rank_math(post_id, p):
    r = requests.post(f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
                      headers=H_FORM,
                      data={
                          "objectID": post_id,
                          "objectType": "post",
                          "meta[rank_math_focus_keyword]": p["focus_kw"],
                          "meta[rank_math_title]": p["seo_title"],
                          "meta[rank_math_description]": p["meta_desc"],
                      },
                      timeout=20)
    return r.status_code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    results = []
    for p in PAGES:
        slug = p["slug"]
        print(f"\n[{slug}]")
        existing = check_slug(slug)
        if existing:
            post_id = existing[0]["id"]
            link = existing[0].get("link", "?")
            print(f"  Already exists: ID {post_id} -> {link}")
            rm = set_rank_math(post_id, p)
            print(f"  Rank Math HTTP {rm}")
            results.append((slug, post_id, link, "existing"))
            continue

        print(f"  Creating page...")
        result = create_page(p)
        post_id = result["id"]
        link = result.get("link", "?")
        print(f"  Created ID {post_id} -> {link}")

        rm = set_rank_math(post_id, p)
        print(f"  Rank Math HTTP {rm}")
        results.append((slug, post_id, link, "created"))

    print("\n--- Summary ---")
    for slug, pid, link, status in results:
        print(f"  [{status}] ID {pid}  {link}")
        print(f"            Focus KW: mobile blood draw {slug.split('-')[3].title()} GA")


if __name__ == "__main__":
    main()
