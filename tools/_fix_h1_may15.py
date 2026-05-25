"""
Fix H1 issues from May 15 2026 Ahrefs audit:
1. 4 pages with multiple H1 tags (new city pages + at-home-blood-draw-service)
2. about-us: H1 missing entirely (our last fix over-stripped it)
"""
import re, os, base64, socket, requests, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".env")

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}


def find_post(slug):
    for ptype in ("pages", "posts"):
        r = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/{ptype}",
            headers=HJ,
            params={"slug": slug.strip("/"), "status": "publish", "per_page": 1},
            timeout=12,
        )
        if r.ok and r.json():
            return r.json()[0]["id"], ptype
        time.sleep(0.3)
    return None, None


def get_raw(post_id, post_type):
    r = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/{post_type}/{post_id}",
        headers=HJ,
        params={"context": "edit"},
        timeout=15,
    )
    if not r.ok:
        return None
    return (r.json().get("content") or {}).get("raw", "")


def save_raw(post_id, post_type, raw):
    r = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/{post_type}/{post_id}",
        headers=HJ,
        json={"content": raw},
        timeout=25,
    )
    return r.ok, r.status_code


def downgrade_h1_to_h2(raw):
    """Convert all H1 tags in content.raw to H2."""
    count = 0

    def replace_level(m):
        nonlocal count
        count += 1
        return m.group(0).replace('"level":1', '"level":2')

    new = re.sub(r'<!-- wp:heading \{[^}]*"level":1[^}]*\} -->', replace_level, raw)

    def replace_open(m):
        nonlocal count
        if '<!-- wp:heading' not in raw:
            count += 1
        return "<h2" + m.group(1) + ">"

    new = re.sub(r"<h1([^>]*)>", replace_open, new)
    new = new.replace("</h1>", "</h2>")
    return new, count


# ── 1. FIX MULTIPLE H1 PAGES ─────────────────────────────────────────────────

MULTI_H1_SLUGS = [
    "at-home-blood-draw-service",
    "mobile-phlebotomy-dna-testing-grayson-ga",
    "mobile-phlebotomy-dna-testing-lawrenceville-ga",
    "mobile-phlebotomy-dna-testing-loganville-ga",
]

print("=" * 60)
print("1. Fixing multiple H1 tags (4 pages)")
print("=" * 60)

for slug in MULTI_H1_SLUGS:
    post_id, post_type = find_post(slug)
    if not post_id:
        print(f"  NOT FOUND: /{slug}/")
        continue

    raw = get_raw(post_id, post_type)
    if raw is None:
        print(f"  FAIL GET  ID {post_id} /{slug}/")
        continue

    h1_count = raw.lower().count("<h1")
    if h1_count == 0 and '"level":1' not in raw:
        print(f"  SKIP      ID {post_id:5} ({post_type}) /{slug}/ — no H1 in content.raw")
        time.sleep(0.3)
        continue

    new_raw, changed = downgrade_h1_to_h2(raw)
    ok, code = save_raw(post_id, post_type, new_raw)
    print(f"  {'OK  ' if ok else 'FAIL'} ID {post_id:5} ({post_type}) /{slug}/ — {changed} H1->H2 (HTTP {code})")
    time.sleep(0.5)


# ── 2. FIX ABOUT-US MISSING H1 ───────────────────────────────────────────────
# Our last fix converted the content H1 to H2. The theme doesn't output an H1
# for this page, so now it has zero H1 tags. We need to restore the first H2
# (which was the original H1) back to H1.

print("\n" + "=" * 60)
print("2. Restoring H1 on about-us (was over-stripped)")
print("=" * 60)

post_id, post_type = find_post("about-us")
if not post_id:
    print("  NOT FOUND: /about-us/")
else:
    raw = get_raw(post_id, post_type)
    if raw is None:
        print(f"  FAIL GET about-us ID {post_id}")
    else:
        h1_in_raw = raw.lower().count("<h1")
        h2_in_raw = raw.lower().count("<h2")
        print(f"  Current H1 count in raw: {h1_in_raw}")
        print(f"  Current H2 count in raw: {h2_in_raw}")

        # Show first H2 for diagnosis
        m = re.search(r"<h2([^>]*)>(.*?)</h2>", raw, re.IGNORECASE | re.DOTALL)
        if m:
            print(f"  First H2 found: <h2{m.group(1)}>{m.group(2)[:80]}</h2>")

        if h1_in_raw > 0:
            print("  Already has H1 in content — no change needed")
        elif not m:
            print("  No H2 found to promote — manual review needed")
        else:
            # Restore ONLY the first H2 back to H1
            # Also fix Gutenberg block attribute if present
            new_raw = raw

            # Fix Gutenberg block comment for the first heading (level 2 -> 1)
            new_raw = re.sub(
                r'<!-- wp:heading \{[^}]*"level":2[^}]*\} -->',
                lambda mx: mx.group(0).replace('"level":2', '"level":1'),
                new_raw,
                count=1,
            )

            # Promote first <h2> to <h1>
            new_raw = re.sub(r"<h2([^>]*)>", r"<h1\1>", new_raw, count=1)
            new_raw = new_raw.replace("</h2>", "</h1>", 1)

            ok, code = save_raw(post_id, post_type, new_raw)
            print(f"  {'OK  ' if ok else 'FAIL'} ID {post_id:5} ({post_type}) /about-us/ — first H2 promoted to H1 (HTTP {code})")

print("\nDone.")
