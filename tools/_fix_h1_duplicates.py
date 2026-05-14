"""
Fix multiple H1 tags — May 2026 audit (20 pages).

Root cause: theme outputs page/post title as H1; the content body
also has an H1 tag (plain HTML, Gutenberg block, or Elementor raw).

Fix: in content.raw, change <h1...> -> <h2...> and </h1> -> </h2>,
plus update Gutenberg block attribute "level":1 -> "level":2.
"""
import re, os, base64, socket, requests, time
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
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

SLUGS = [
    "about-us",
    "mobile-phlebotomy-duluth-ga",
    "mobile-phlebotomy-gwinnett-county-ga",
    "mobile-phlebotomy-atlanta-guide",
    "on-site-employee-health-screenings-boosting-workplace-wellness",
    "mobile-dna-testing-for-paternity-discreet-and-professional",
    "non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate",
    "post-mortem-dna-testing-handling-sensitive-legal-matters",
    "understanding-aabb-accredited-immigration-dna-testing",
    "the-role-of-dna-testing-in-modern-family-law",
    "twin-zygosity-testing-are-they-identical-or-fraternal",
    "mobile-phlebotomy-norcross-ga",
    "alcohol-testing-for-legal-and-corporate-compliance",
    "mobile-phlebotomy-conyers-ga",
    "mobile-phlebotomy-tucker-ga",
    "mobile-phlebotomy-snellville-ga",
    "mobile-drug-testing-gwinnett-county-ga",
    "the-difference-between-home-dna-kits-and-legal-paternity-tests",
    "dna-testing-gwinnett-county-ga",
    "mobile-phlebotomy-lawrenceville-ga",
]


def _waf_check(r):
    if r.status_code == 202 or (r.ok and "sgcaptcha" in r.text[:200]):
        raise SystemExit("Sucuri WAF blocking (CAPTCHA). Whitelist your IP and retry.")


def find_post(slug):
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


def downgrade_h1_in_content(raw):
    """Return (new_raw, count) — changes H1 tags and Gutenberg level attrs to H2."""
    if "<h1" not in raw and '"level":1' not in raw:
        return raw, 0

    count = 0

    # Gutenberg block attribute: <!-- wp:heading {"level":1} -->
    def replace_level(m):
        nonlocal count
        count += 1
        return m.group(0).replace('"level":1', '"level":2')

    new = re.sub(
        r'<!-- wp:heading \{[^}]*"level":1[^}]*\} -->',
        replace_level,
        raw,
    )

    # Opening <h1> tags (with or without attributes)
    def replace_open(m):
        nonlocal count
        # Only count the tag once even if already counted via Gutenberg comment
        if '<!-- wp:heading' not in raw:
            count += 1
        return "<h2" + m.group(1) + ">"

    new = re.sub(r"<h1([^>]*)>", replace_open, new)
    new = new.replace("</h1>", "</h2>")

    return new, count


def fix_page(post_id, post_type):
    endpoint = f"{WP_SITE}/wp-json/wp/v2/{post_type}/{post_id}"
    r = requests.get(endpoint, headers=HJ, params={"context": "edit"}, timeout=15)
    _waf_check(r)
    if not r.ok:
        return False, 0, f"GET failed {r.status_code}"

    data = r.json()
    raw = (data.get("content") or {}).get("raw", "")
    if not raw:
        return True, 0, "empty content (skipped)"

    new_raw, count = downgrade_h1_in_content(raw)
    if count == 0:
        return True, 0, "no H1 tags in content"

    rp = requests.post(
        endpoint,
        headers=HJ,
        json={"content": new_raw},
        timeout=25,
    )
    _waf_check(rp)
    if rp.ok:
        return True, count, f"{count} H1->H2"
    return False, 0, rp.text[:120]


print("=" * 60)
print("Fixing Multiple H1 tags — content.raw approach (20 pages)")
print("=" * 60)

total_fixed = 0
total_skipped = 0

for slug in SLUGS:
    post_id, post_type = find_post(slug)
    if not post_id:
        print(f"  NOT FOUND: /{slug}/")
        continue

    ok, count, msg = fix_page(post_id, post_type)
    status = "OK  " if ok else "FAIL"
    print(f"  {status} ID {post_id:5} ({post_type})  /{slug}/  {msg}")
    if ok and count > 0:
        total_fixed += 1
    elif ok:
        total_skipped += 1
    time.sleep(0.5)

print(f"\nSummary: {total_fixed} pages fixed, {total_skipped} skipped (no H1 in content)")
print("Done.")
