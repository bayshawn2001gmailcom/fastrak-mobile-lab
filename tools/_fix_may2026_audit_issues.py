"""
Fix remaining Ahrefs site audit issues — May 2026 crawl.

Handles:
1. Duplicate meta description tags (6 pages — Elementor + Rank Math conflict)
2. Meta description too long (9 pages total, 3 not previously covered)
3. Title tag too long (2 pages)

Forces IPv4 to bypass Sucuri WAF IPv6 rate limiting.
"""
import json, os, base64, socket, requests, time
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


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _waf_check(r):
    if r.status_code == 202 or (r.ok and "sgcaptcha" in r.text[:200]):
        raise SystemExit(
            "Sucuri WAF is blocking requests (CAPTCHA). "
            "Whitelist your IP in Sucuri dashboard, then retry."
        )


def find_post(slug):
    """Return (post_id, post_type) by slug. Checks both posts and pages."""
    for ptype in ("pages", "posts"):
        r = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/{ptype}",
            headers=HJ,
            params={"slug": slug.strip("/"), "status": "publish", "per_page": 1},
            timeout=12,
        )
        _waf_check(r)
        if r.ok and r.text.strip():
            data = r.json()
            if data:
                return data[0]["id"], ptype
        time.sleep(0.4)
    return None, None


def set_rank_math_meta(post_id, *, description=None, title=None):
    """Set Rank Math SEO description and/or title via updateMeta endpoint."""
    payload = {"objectID": post_id, "objectType": "post"}
    if description is not None:
        assert len(description) <= 155, f"Description {len(description)} chars — too long"
        payload["meta[rank_math_description]"] = description
    if title is not None:
        assert len(title) <= 60, f"Title {len(title)} chars — too long"
        payload["meta[rank_math_title]"] = title
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=H,
        data=payload,
        timeout=20,
    )
    return r.ok, r.text[:150]


def clear_elementor_description(post_id, post_type):
    """Read _elementor_page_settings, zero out 'description', write back."""
    endpoint = f"{WP_SITE}/wp-json/wp/v2/{post_type}/{post_id}"
    r = requests.get(endpoint, headers=HJ, params={"context": "edit"}, timeout=15)
    _waf_check(r)
    if not r.ok:
        return False, f"GET failed {r.status_code}"

    data = r.json()
    settings_raw = (data.get("meta") or {}).get("_elementor_page_settings", "{}")
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
        return True, "no Elementor description (skipped)"

    settings["description"] = ""
    rp = requests.post(
        endpoint,
        headers=HJ,
        json={"meta": {"_elementor_page_settings": json.dumps(settings)}},
        timeout=20,
    )
    _waf_check(rp)
    return rp.ok, rp.text[:150]


# ─────────────────────────────────────────────────────────────────────────────
# 1. DUPLICATE META DESCRIPTION — clear Elementor + set authoritative Rank Math
# ─────────────────────────────────────────────────────────────────────────────
# All 6 pages currently flagged as Error in Ahrefs.
# Format: (post_id_or_None, slug, rank_math_description)
# post_id=None → look up dynamically

DUPLICATE_META_PAGES = [
    (805,  "posts", "why-choose-mobile-phlebotomy-for-your-blood-draw-needs",
     "Discover why mobile phlebotomy is the smarter choice for blood draws. "
     "Fastrak Mobile Lab sends a licensed phlebotomist to your home or office in Atlanta."),

    (820,  "posts", "enhance-your-care-advantages-of-mobile-phlebotomy-services",
     "Explore mobile phlebotomy advantages from Fastrak Mobile Lab. "
     "We come to your home or office in Atlanta and Gwinnett County for convenient blood draws."),

    (1177, "posts", "how-mobile-phlebotomy-works-patient-guide-gwinnett-county",
     "New to mobile phlebotomy? This guide explains how at-home blood draws work in "
     "Gwinnett County, GA — from booking through results with Fastrak Mobile Lab."),

    (1176, "posts", "corporate-wellness-blood-panels-duluth-ga",
     "Fastrak Mobile Lab delivers on-site corporate wellness blood panels for Duluth, GA employers. "
     "No facility visits required. Book your screening today."),

    # New — not in previous scripts
    (None, None, "mobile-blood-collection-assisted-living-conyers-ga",
     "Fastrak Mobile Lab provides recurring on-site specimen collection for assisted living "
     "facilities in Conyers, GA. Serving Rockdale County and metro Atlanta."),

    (None, None, "dot-drug-testing-gwinnett-county-fleet-managers",
     "DOT-compliant drug & alcohol testing for Gwinnett County fleet operators. "
     "Fastrak Mobile Lab handles 49 CFR Part 40 collection with full chain of custody."),
]


print("=" * 60)
print("1. Fixing duplicate meta description tags (6 pages)")
print("=" * 60)

for post_id, post_type, slug, desc in DUPLICATE_META_PAGES:
    assert len(desc) <= 155, f"Too long ({len(desc)}): {slug}"

    if not post_id:
        post_id, post_type = find_post(slug)
        if not post_id:
            print(f"  NOT FOUND: /{slug}/")
            continue

    # Step A: clear Elementor description
    ok_e, msg_e = clear_elementor_description(post_id, post_type)
    # Step B: set authoritative Rank Math description
    ok_r, msg_r = set_rank_math_meta(post_id, description=desc)

    status = "OK  " if (ok_e and ok_r) else "FAIL"
    print(f"  {status} ID {post_id:5} ({post_type})  /{slug}/")
    if not ok_e:
        print(f"       Elementor: {msg_e}")
    if not ok_r:
        print(f"       RankMath:  {msg_r}")
    time.sleep(0.5)


# ─────────────────────────────────────────────────────────────────────────────
# 2. META DESCRIPTION TOO LONG — set trimmed Rank Math description
# ─────────────────────────────────────────────────────────────────────────────
# Pages from the Warning category (9 total; 3 not in previous scripts).
# Already-covered pages re-applied here to ensure the fix landed.

META_TOO_LONG = [
    ("mobile-dna-testing-atlanta",
     "Professional mobile drug testing and DNA collection in Atlanta & Gwinnett County. "
     "HIPAA-compliant, court-admissible. Fastrak Mobile Lab comes to you."),         # 149

    ("mobile-phlebotomy-duluth-ga",
     "Fastrak Mobile Lab offers mobile phlebotomy in Duluth, GA. Licensed phlebotomists "
     "come to your home or office for blood draws and lab testing. Book today."),     # 152

    ("mobile-phlebotomy-conyers-ga",
     "Fastrak Mobile Lab provides mobile blood draws in Conyers, GA. Licensed "
     "phlebotomists come to your home or facility. HIPAA-compliant. Book today."),   # 148

    ("mobile-drug-testing-gwinnett-county-ga",
     "Fastrak Mobile Lab provides court-admissible drug testing in Gwinnett County, GA. "
     "Mobile screening for employers, individuals, and DOT compliance."),            # 147

    ("dna-testing-gwinnett-county-ga",
     "Need DNA testing in Gwinnett County, GA? Fastrak Mobile Lab offers certified "
     "paternity and relationship testing. Fast, accurate, confidential results."),   # 149

    ("mobile-phlebotomy-lawrenceville-ga",
     "Fastrak Mobile Lab provides mobile blood draws, drug testing, and lab services in "
     "Lawrenceville, GA. Licensed phlebotomists come to your home or office."),      # 152

    # New — not in previous scripts
    ("mobile-blood-collection-assisted-living-conyers-ga",
     "Fastrak Mobile Lab provides recurring on-site specimen collection for assisted "
     "living facilities in Conyers, GA. Serving Rockdale County and metro Atlanta."), # 155

    ("corporate-wellness-blood-panels-duluth-ga",
     "Fastrak Mobile Lab delivers on-site corporate wellness blood panels for Duluth, GA "
     "employers. No facility visits required. Book your screening today."),           # 141

    ("dot-drug-testing-gwinnett-county-fleet-managers",
     "DOT-compliant drug & alcohol testing for Gwinnett County fleet operators. "
     "Fastrak Mobile Lab handles 49 CFR Part 40 collection with full chain of custody."), # 153
]


print("\n" + "=" * 60)
print("2. Fixing meta descriptions that are too long (9 pages)")
print("=" * 60)

for slug, desc in META_TOO_LONG:
    assert len(desc) <= 155, f"Still too long ({len(desc)}): {slug}"
    post_id, post_type = find_post(slug)
    if not post_id:
        print(f"  NOT FOUND: /{slug}/")
        continue
    ok, msg = set_rank_math_meta(post_id, description=desc)
    print(f"  {'OK  ' if ok else 'FAIL'} ID {post_id:5} ({post_type})  /{slug}/  [{len(desc)} chars]")
    if not ok:
        print(f"       {msg}")
    time.sleep(0.4)


# ─────────────────────────────────────────────────────────────────────────────
# 3. TITLE TOO LONG — set shorter Rank Math SEO title (≤60 chars)
# ─────────────────────────────────────────────────────────────────────────────

TITLE_TOO_LONG = [
    # 73 chars → remove "| Chain of Custody" middle section
    ("paternity-dna-testing-norcross-ga",
     "Paternity DNA Testing Norcross GA | Fastrak Mobile Lab"),   # 54

    # 71 chars → remove "Assisted Living" from middle
    ("mobile-blood-collection-assisted-living-conyers-ga",
     "Mobile Blood Collection Conyers GA | Fastrak Mobile Lab"),  # 55
]


print("\n" + "=" * 60)
print("3. Fixing title tags that are too long (2 pages)")
print("=" * 60)

for slug, title in TITLE_TOO_LONG:
    assert len(title) <= 60, f"Still too long ({len(title)}): {slug}"
    post_id, post_type = find_post(slug)
    if not post_id:
        print(f"  NOT FOUND: /{slug}/")
        continue
    ok, msg = set_rank_math_meta(post_id, title=title)
    print(f"  {'OK  ' if ok else 'FAIL'} ID {post_id:5} ({post_type})  /{slug}/  [{len(title)} chars]")
    if not ok:
        print(f"       {msg}")
    time.sleep(0.4)


print("\nDone.")
