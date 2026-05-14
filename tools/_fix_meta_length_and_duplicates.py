"""
Fix two remaining Ahrefs meta description issues:
1. Shorten 6 city page meta descriptions that exceed 155 chars
2. Clear Elementor page-level description from posts where it creates a
   duplicate <meta name="description"> tag alongside Rank Math's output

Forces IPv4 to bypass Sucuri WAF IPv6 rate limiting.
"""
import os, json, base64, socket, requests, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
H  = {"Authorization": f"Basic {creds}"}
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}


# ── 1. SHORTEN CITY PAGE META DESCRIPTIONS ───────────────────────────────────
# Only pages that are currently >155 chars in Ahrefs audit

CITY_META_FIXES = {
    "mobile-dna-testing-atlanta": (
        "Professional mobile drug testing and DNA collection in Atlanta & Gwinnett County. "
        "HIPAA-compliant, court-admissible. Fastrak Mobile Lab comes to you."
    ),  # 149
    "mobile-phlebotomy-duluth-ga": (
        "Fastrak Mobile Lab offers mobile phlebotomy in Duluth, GA. Licensed phlebotomists "
        "come to your home or office for blood draws and lab testing. Book today."
    ),  # 152
    "mobile-phlebotomy-conyers-ga": (
        "Fastrak Mobile Lab provides mobile blood draws in Conyers, GA. Licensed phlebotomists "
        "come to your home or facility. HIPAA-compliant. Book today."
    ),  # 148
    "mobile-drug-testing-gwinnett-county-ga": (
        "Fastrak Mobile Lab provides court-admissible drug testing in Gwinnett County, GA. "
        "Mobile screening for employers, individuals, and DOT compliance."
    ),  # 147
    "dna-testing-gwinnett-county-ga": (
        "Need DNA testing in Gwinnett County, GA? Fastrak Mobile Lab offers certified paternity "
        "and relationship testing. Fast, accurate, confidential results."
    ),  # 149
    "mobile-phlebotomy-lawrenceville-ga": (
        "Fastrak Mobile Lab provides mobile blood draws, drug testing, and lab services in "
        "Lawrenceville, GA. Licensed phlebotomists come to your home or office."
    ),  # 152
}


def find_post_id(slug):
    for ptype in ("posts", "pages"):
        r = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/{ptype}",
            headers=HJ,
            params={"slug": slug, "status": "publish", "per_page": 1},
            timeout=12,
        )
        if r.status_code == 202 or (r.ok and "sgcaptcha" in r.text[:200]):
            raise SystemExit(
                "ERROR: Sucuri WAF is blocking requests (202 CAPTCHA).\n"
                "Whitelist your IP in Sucuri dashboard or wait 30-60 min, then retry."
            )
        if r.ok and r.text.strip():
            data = r.json()
            if data:
                return data[0]["id"], ptype
        time.sleep(0.5)
    return None, None


def set_rank_math_desc(post_id, description):
    desc = description[:155]
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=H,
        data={
            "objectID": post_id,
            "objectType": "post",
            "meta[rank_math_description]": desc,
        },
        timeout=20,
    )
    return r.ok, r.text[:120]


print("=== 1. Shortening city page meta descriptions (>155 chars) ===\n")
city_ids = {}
for slug, desc in CITY_META_FIXES.items():
    assert len(desc) <= 155, f"Description too long ({len(desc)} chars): {slug}"
    post_id, ptype = find_post_id(slug)
    if not post_id:
        print(f"NOT FOUND: {slug}")
        continue
    city_ids[slug] = post_id
    ok, msg = set_rank_math_desc(post_id, desc)
    print(f"{'OK' if ok else 'FAIL'} ID {post_id} ({ptype}) /{slug}/  [{len(desc)} chars]")
    if not ok:
        print(f"     {msg}")
    time.sleep(0.4)


# ── 2. CLEAR ELEMENTOR PAGE-LEVEL DESCRIPTION ────────────────────────────────
# These posts have Elementor outputting its own <meta name="description"> tag.
# Elementor stores the page-level description in `_elementor_page_settings` meta.
# Clearing that field makes Elementor stop outputting a duplicate tag.

# Post IDs confirmed from previous run output:
ELEMENTOR_POSTS = [
    (805,  "why-choose-mobile-phlebotomy-for-your-blood-draw-needs"),
    (820,  "enhance-your-care-advantages-of-mobile-phlebotomy-services"),
    (829,  "mobile-phlebotomy-services-for-busy-professionals"),
    (816,  "how-to-prepare-for-your-mobile-phlebotomy-visit"),
    (839,  "benefits-of-mobile-blood-draws-for-patients"),
    (833,  "experience-the-convenience-of-at-home-blood-draws"),
    (863,  "mobile-dna-paternity-testing-confidential-accurate-and-convenient"),
    (987,  "early-gender-reveal-dna-testing-safe-and-early-insights"),
    (990,  "how-to-prepare-for-your-home-dna-collection-appointment"),
    (1177, "how-mobile-phlebotomy-works-patient-guide-gwinnett-county"),
    (1176, "corporate-wellness-blood-panels-duluth-ga"),
]


def clear_elementor_description(post_id):
    """Read _elementor_page_settings, remove the 'description' key, write back."""
    # GET current post meta
    r = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}",
        headers=HJ,
        params={"context": "edit"},
        timeout=15,
    )
    if r.status_code == 202 or (r.ok and "sgcaptcha" in r.text[:200]):
        raise SystemExit(
            "ERROR: Sucuri WAF is blocking requests (202 CAPTCHA).\n"
            "Whitelist your IP in Sucuri dashboard or wait 30-60 min, then retry."
        )
    if not r.ok:
        return False, f"GET failed: {r.status_code} {r.text[:80]}"

    data = r.json()
    meta = data.get("meta", {})
    settings_raw = meta.get("_elementor_page_settings", "{}")

    # Parse Elementor settings
    if isinstance(settings_raw, str):
        try:
            settings = json.loads(settings_raw)
        except json.JSONDecodeError:
            settings = {}
    elif isinstance(settings_raw, dict):
        settings = settings_raw
    else:
        settings = {}

    if not settings.get("description"):
        return True, "no Elementor description set (skipped)"

    # Clear the description
    settings["description"] = ""

    # PATCH the post meta
    payload = {"meta": {"_elementor_page_settings": json.dumps(settings)}}
    rp = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}",
        headers=HJ,
        json=payload,
        timeout=20,
    )
    return rp.ok, rp.text[:120]


print("\n=== 2. Clearing Elementor page-level descriptions ===\n")
for post_id, slug in ELEMENTOR_POSTS:
    ok, msg = clear_elementor_description(post_id)
    print(f"{'OK' if ok else 'FAIL'} ID {post_id} /{slug}/")
    if not ok or "failed" in msg.lower():
        print(f"     {msg}")
    time.sleep(0.4)

print("\nDone.")
