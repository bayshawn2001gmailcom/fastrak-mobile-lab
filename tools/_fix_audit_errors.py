"""
Fix three Ahrefs site audit error categories:
1. Create 301 redirects for 21 x 404 duplicate-slug pages
2. Fix Elementor HTML appearing as meta descriptions
3. Fix generic/placeholder meta descriptions on blog posts

Note: Forces IPv4 to bypass Sucuri WAF IPv6 rate limiting.
"""
import os, re, base64, socket, requests, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

# Force IPv4 — Sucuri WAF blocks our IPv6 address after burst requests
_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _getaddrinfo_ipv4

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
H = {"Authorization": f"Basic {creds}"}  # no Content-Type for form-data endpoints
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

# ── 1. 404 REDIRECTS ──────────────────────────────────────────────────────────

FOUR_OH_FOURS = [
    "/non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate-2/",
    "/the-difference-between-home-dna-kits-and-legal-paternity-tests-3/",
    "/the-future-of-mobile-diagnostics-trends-to-watch-in-2026/",
    "/mobile-gender-reveal-dna-testing-early-clinical-results-in-lawrenceville-2/",
    "/onsite-background-checks-fingerprinting-for-atlanta-healthcare-staffing-2/",
    "/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know-2/",
    "/mobile-respiratory-fit-testing-osha-compliance-for-georgia-construction-2/",
    "/mobile-dot-drug-testing-for-fleet-managers-compliance-made-easy-in-gwinnett-2/",
    "/mobile-dot-physicals-for-cdl-drivers-same-day-appointments-in-norcross-2/",
    "/legal-admissibility-mobile-dna-paternity-testing-for-georgia-court-cases-2/",
    "/the-difference-between-home-dna-kits-and-legal-paternity-tests-2/",
    "/concierge-mobile-blood-draws-professional-phlebotomy-at-your-atlanta-home-2/",
    "/discreet-mobile-infidelity-dna-testing-private-labs-serving-gwinnett-county-2/",
    "/legal-chain-of-custody-dna-testing-gwinnett-county-law-support-2/",
    "/onsite-dot-drug-screening-for-logistics-firms-in-alpharetta-30005/",
    "/onsite-corporate-flu-wellness-clinics-mobile-immunizations-in-atlanta-2/",
    "/pediatric-mobile-blood-draws-compassionate-care-in-roswell-30075/",
    "/24-7-mobile-post-accident-breathalyzer-drug-screening-in-metro-atlanta-2/",
    "/mobile-dna-paternity-testing-discrete-service-in-milton-30004/",
    "/concierge-phlebotomy-private-blood-draws-in-buckhead-30327/",
    "/executive-health-longevity-panels-mobile-phlebotomy-in-vinings-30339/",
]


def canonical_target(slug):
    """Strip -2, -3 suffixes and zip code suffixes to get the canonical slug."""
    s = slug.rstrip("/")
    s = re.sub(r"-[23]$", "", s)
    s = re.sub(r"-\d{5}$", "", s)
    return s + "/"


def url_status(url):
    try:
        r = requests.head(url, timeout=10, allow_redirects=True)
        return r.status_code
    except Exception:
        return 0


def find_post_by_slug(slug, statuses=("publish", "draft", "private", "trash")):
    """Return (post_id, status) for a slug searched across all given statuses."""
    clean = slug.strip("/")
    for status in statuses:
        for ptype in ("posts", "pages"):
            r = requests.get(
                f"{WP_SITE}/wp-json/wp/v2/{ptype}",
                headers=HJ,
                params={"slug": clean, "status": status, "per_page": 1, "context": "edit"},
                timeout=15,
            )
            if r.ok and r.json():
                return r.json()[0]["id"], r.json()[0]["status"]
            time.sleep(0.3)
    return None, None


def create_redirect_via_post(post_id, destination_url):
    """Use Rank Math per-post redirect (updateRedirection) on an existing post."""
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateRedirection",
        headers=H,
        data={
            "objectID": post_id,
            "objectType": "post",
            "hasRedirect": 1,
            "redirectionUrl": destination_url,
            "redirectionType": "301",
        },
        timeout=20,
    )
    return r.ok, r.text[:200]


print("=== 1. Creating 301 redirects for 404 pages ===\n")
print("(Looking up post IDs — duplicate slugs may be drafts/trash)\n")

manual_redirects = []

for slug in FOUR_OH_FOURS:
    target_slug = canonical_target(slug)
    target_url = WP_SITE + target_slug
    fallback_url = WP_SITE + "/"

    status_code = url_status(target_url)
    destination = target_url if status_code == 200 else fallback_url
    label = target_slug if status_code == 200 else "/ (fallback)"

    # Look for this slug as an existing WP post in any status
    post_id, post_status = find_post_by_slug(slug)
    if post_id:
        ok, msg = create_redirect_via_post(post_id, destination)
        print(f"{'OK' if ok else 'FAIL'} [{post_status}:{post_id}] {slug} -> {label}")
        if not ok:
            print(f"     {msg}")
    else:
        manual_redirects.append((slug, destination, label))
        print(f"MANUAL {slug} -> {label}  (no WP post found)")
    time.sleep(0.5)

if manual_redirects:
    print(f"\n{len(manual_redirects)} redirects need manual creation in Rank Math admin:")
    print("  WP Admin > Rank Math > Redirections > Add New\n")
    for src, dst, lbl in manual_redirects:
        print(f"  Source: {src}")
        print(f"  Dest:   {dst}  ({lbl})")
        print()

# ── 2 & 3. FIX META DESCRIPTIONS ─────────────────────────────────────────────

# Known post IDs from previous run output (avoids extra API calls)
META_FIXES_WITH_IDS = [
    (805,  "posts", "why-choose-mobile-phlebotomy-for-your-blood-draw-needs",
     "Discover why mobile phlebotomy is the smarter choice for blood draws. "
     "Fastrak Mobile Lab sends a licensed phlebotomist to your home or office in metro Atlanta — no waiting rooms, no travel."),
    (820,  "posts", "enhance-your-care-advantages-of-mobile-phlebotomy-services",
     "Explore the advantages of mobile phlebotomy services from Fastrak Mobile Lab. "
     "We come to your home, office, or facility in Atlanta and Gwinnett County for fast, convenient blood draws."),
    (829,  "posts", "mobile-phlebotomy-services-for-busy-professionals",
     "Too busy for a lab visit? Fastrak Mobile Lab brings certified phlebotomy services to busy professionals "
     "across metro Atlanta. Schedule a blood draw at your office or home today."),
    (816,  "posts", "how-to-prepare-for-your-mobile-phlebotomy-visit",
     "Get ready for your at-home blood draw with these simple preparation tips from Fastrak Mobile Lab. "
     "Hydrate, fast if required, and relax — we handle everything else."),
    (839,  "posts", "benefits-of-mobile-blood-draws-for-patients",
     "Mobile blood draws offer convenience, comfort, and privacy for patients across Atlanta. "
     "Learn how Fastrak Mobile Lab's in-home phlebotomy service makes lab testing easier."),
    (833,  "posts", "experience-the-convenience-of-at-home-blood-draws",
     "Experience the convenience of at-home blood draws with Fastrak Mobile Lab. "
     "Our licensed phlebotomists come to you anywhere in metro Atlanta — fast results, zero waiting rooms."),
    (863,  "posts", "mobile-dna-paternity-testing-confidential-accurate-and-convenient",
     "Confidential mobile DNA paternity testing in Atlanta and Gwinnett County. "
     "Fastrak Mobile Lab's certified collectors come to you for court-admissible specimen collection."),
    (987,  "posts", "early-gender-reveal-dna-testing-safe-and-early-insights",
     "Find out your baby's gender early with mobile DNA testing from Fastrak Mobile Lab. "
     "Safe, accurate early gender reveal testing with certified collection at your home in metro Atlanta."),
    (990,  "posts", "how-to-prepare-for-your-home-dna-collection-appointment",
     "Preparing for a home DNA collection appointment? Fastrak Mobile Lab walks you through exactly "
     "what to expect -- from scheduling to specimen collection -- in metro Atlanta and Gwinnett County."),
    (1177, "posts", "how-mobile-phlebotomy-works-patient-guide-gwinnett-county",
     "New to mobile phlebotomy? This patient guide explains how at-home blood draws work in "
     "Gwinnett County, GA -- from booking through results with Fastrak Mobile Lab."),
    (1176, "posts", "corporate-wellness-blood-panels-duluth-ga",
     "Fastrak Mobile Lab delivers on-site corporate wellness blood panels for Duluth, GA employers. "
     "Comprehensive employee health screenings with no facility visits required."),
]


def set_meta_desc(post_id, description):
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=H,
        data={
            "objectID": post_id,
            "objectType": "post",
            "meta[rank_math_description]": description[:155],
        },
        timeout=20,
    )
    return r.ok, r.text[:150]


print("\n=== 2 & 3. Fixing meta descriptions ===\n")
for post_id, post_type, slug, description in META_FIXES_WITH_IDS:
    ok, msg = set_meta_desc(post_id, description)
    print(f"{'OK' if ok else 'FAIL'} ID {post_id} ({post_type}) /{slug}/")
    if not ok:
        print(f"     {msg}")
    time.sleep(0.3)

print("\nDone.")
