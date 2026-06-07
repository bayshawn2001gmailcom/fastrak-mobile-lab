"""
Fix: duplicate <meta name="description"> on same-day-blood-draw-suwanee-buford-ga

Root cause: Elementor is outputting its own page-level description alongside
Rank Math's, creating two <meta name="description"> tags — an Error in Ahrefs.

Fix: clear the Elementor page-level description so only Rank Math's tag renders.
Also sets the canonical Rank Math description to the better of the two variants.

Run from: C:\\Users\\baysh\\Fastrak Mobile Lab\\
  python tools\\_fix_suwanee_duplicate_meta.py
"""
import os, json, base64, socket, requests, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

# Force IPv4 to bypass Sucuri WAF IPv6 rate limiting
_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    raise SystemExit("ERROR: WP_USER and WP_APP_PASSWORD must be set in ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H  = {"Authorization": f"Basic {creds}"}
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

SLUG = "same-day-blood-draw-suwanee-buford-ga"

# Keep the more specific/accurate description (with route availability note)
CANONICAL_DESC = (
    "Need a blood draw today in Suwanee or Buford, GA? Fastrak Mobile Lab offers "
    "same-day mobile phlebotomy in northern Gwinnett County."
)
assert len(CANONICAL_DESC) <= 155, f"Description too long: {len(CANONICAL_DESC)} chars"


def find_post_id(slug):
    for ptype in ("posts", "pages"):
        r = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/{ptype}",
            headers=HJ,
            params={"slug": slug, "status": "publish", "per_page": 1},
            timeout=12,
        )
        if r.ok and r.text.strip():
            data = r.json()
            if data:
                return data[0]["id"], ptype
        time.sleep(0.4)
    return None, None


def clear_elementor_description(post_id, ptype):
    r = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/{ptype}/{post_id}",
        headers=HJ,
        params={"context": "edit"},
        timeout=15,
    )
    if not r.ok:
        return False, f"GET failed: {r.status_code} {r.text[:80]}"

    data = r.json()
    meta = data.get("meta", {})
    settings_raw = meta.get("_elementor_page_settings", "{}")

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
        return True, "no Elementor description found (nothing to clear)"

    print(f"  Found Elementor description: \"{settings['description'][:80]}...\"")
    settings["description"] = ""

    payload = {"meta": {"_elementor_page_settings": json.dumps(settings)}}
    rp = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/{ptype}/{post_id}",
        headers=HJ,
        json=payload,
        timeout=20,
    )
    return rp.ok, rp.text[:120]


def set_rank_math_desc(post_id, description):
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=H,
        data={
            "objectID": post_id,
            "objectType": "post",
            "meta[rank_math_description]": description,
        },
        timeout=20,
    )
    return r.ok, r.text[:120]


print(f"Looking up /{SLUG}/...")
post_id, ptype = find_post_id(SLUG)

if not post_id:
    raise SystemExit(f"ERROR: Could not find post with slug '{SLUG}'")

print(f"Found: ID {post_id} ({ptype})\n")

print("Step 1: Clearing Elementor page-level description...")
ok, msg = clear_elementor_description(post_id, ptype)
print(f"  {'OK' if ok else 'FAIL'}: {msg}\n")

print("Step 2: Setting canonical Rank Math description...")
ok, msg = set_rank_math_desc(post_id, CANONICAL_DESC)
print(f"  {'OK' if ok else 'FAIL'} ({len(CANONICAL_DESC)} chars)")
if not ok:
    print(f"  {msg}")

print("\nDone. Verify at: https://fastrakmobilelab.com/same-day-blood-draw-suwanee-buford-ga/")
print("Check page source for a single <meta name=\"description\"> tag.")
