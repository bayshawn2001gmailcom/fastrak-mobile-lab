"""
Fix schema.org validation errors across fastrakmobilelab.com

ROOT CAUSE (confirmed against schema.org and Google Search docs):
  A globally-injected <script type="application/ld+json"> block contains:
    1. "serviceType": "Mobile Phlebotomy"
       -- Only valid on schema.org/Service. NOT a valid property on LocalBusiness or MedicalBusiness.
          Confirmed at schema.org/serviceType: "Used on these types: Service"

    2. "medicalSpecialty": "https://schema.org/LaboratoryScience"
       -- Only valid on Hospital, MedicalClinic, MedicalOrganization, Physician.
          MedicalBusiness inherits from LocalBusiness → NOT from MedicalOrganization.
          So this property is invalid here entirely. Remove it — do NOT just change the namespace.
          (https://schema.org/LaboratoryScience IS the correct canonical URL; the property just
           doesn't belong on MedicalBusiness.)

    3. "@type": ["MedicalBusiness", "LocalBusiness"]  -- redundant; MedicalBusiness already
       extends LocalBusiness. Should be just "MedicalBusiness".

  This block appears on ALL ~143 pages and is output by a custom WordPress function
  BEFORE Rank Math's own output.

WHAT THIS SCRIPT DOES:
  Checks whether the schema is stored in Rank Math's custom schema post meta
  (rank_math_schema_*) and patches it if found.

  If it's NOT in post meta (i.e., hardcoded in functions.php), this script will
  report that and you'll need to use the WordPress admin approach below instead.

HOW TO RUN:
  From C:\\Users\\baysh\\Fastrak Mobile Lab\\ in PowerShell/Terminal:
    python tools\\_fix_global_schema_errors.py

ALTERNATIVE (if schema is hardcoded in PHP):
  Add the snippet in tools/_fix_global_schema_wordpress_snippet.php
  to your WordPress theme's functions.php, OR upload it to:
    wp-content/mu-plugins/fix-schema-errors.php

Run from: C:\\Users\\baysh\\Fastrak Mobile Lab\\
"""
import os, json, base64, socket, requests, re, time
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
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}


def get_all_posts_and_pages():
    """Fetch all published posts and pages."""
    items = []
    for ptype in ("pages", "posts"):
        page = 1
        while True:
            r = requests.get(
                f"{WP_SITE}/wp-json/wp/v2/{ptype}",
                headers=HJ,
                params={"per_page": 100, "page": page, "status": "publish", "context": "edit"},
                timeout=20,
            )
            if not r.ok or not r.json():
                break
            batch = r.json()
            items.extend([(p["id"], p["slug"], ptype) for p in batch])
            if len(batch) < 100:
                break
            page += 1
            time.sleep(0.3)
    return items


def check_and_fix_schema_meta(post_id, ptype):
    """
    Check if this post has Rank Math custom schema with the bad fields and fix them.
    Returns (had_issue, fixed, details).
    """
    r = requests.get(
        f"{WP_SITE}/wp-json/wp/v2/{ptype}/{post_id}",
        headers=HJ,
        params={"context": "edit"},
        timeout=15,
    )
    if not r.ok:
        return False, False, f"GET failed: {r.status_code}"

    data = r.json()
    meta = data.get("meta", {})

    # Rank Math stores custom schemas as rank_math_schema_<hash> keys
    schema_keys = [k for k in meta.keys() if k.startswith("rank_math_schema_")]

    found_issues = False
    patched_meta = {}

    for key in schema_keys:
        raw = meta[key]
        if isinstance(raw, str):
            try:
                schema = json.loads(raw)
            except:
                continue
        elif isinstance(raw, dict):
            schema = raw
        else:
            continue

        changed = False

        schema_types = schema.get("@type", [])
        if isinstance(schema_types, str):
            schema_types = [schema_types]
        is_local_biz = any(t in schema_types for t in ("LocalBusiness", "MedicalBusiness"))

        # Fix 1: Remove "serviceType" — only valid on Service, not LocalBusiness/MedicalBusiness
        if is_local_biz and "serviceType" in schema:
            del schema["serviceType"]
            changed = True

        # Fix 2: Remove "medicalSpecialty" — valid only on Hospital, MedicalClinic,
        # MedicalOrganization, Physician. MedicalBusiness does NOT inherit from
        # MedicalOrganization, so this property is invalid here entirely.
        if is_local_biz and "medicalSpecialty" in schema:
            del schema["medicalSpecialty"]
            changed = True

        # Fix 3: Remove redundant LocalBusiness from @type array when MedicalBusiness present
        # MedicalBusiness already extends LocalBusiness — listing both is unnecessary
        if isinstance(schema.get("@type"), list):
            types = schema["@type"]
            if "MedicalBusiness" in types and "LocalBusiness" in types:
                schema["@type"] = [t for t in types if t != "LocalBusiness"]
                changed = True

        if changed:
            found_issues = True
            patched_meta[key] = json.dumps(schema)

    if not found_issues:
        return False, False, "no Rank Math schema meta with these issues"

    # PATCH the post with fixed schema
    r = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/{ptype}/{post_id}",
        headers=HJ,
        json={"meta": patched_meta},
        timeout=20,
    )
    return True, r.ok, f"PATCH {'OK' if r.ok else f'FAILED {r.status_code}'}"


print("Fetching all posts and pages...")
all_items = get_all_posts_and_pages()
print(f"Found {len(all_items)} items total\n")

found_count = 0
fixed_count = 0
not_in_meta_count = 0

for post_id, slug, ptype in all_items:
    had_issue, fixed, detail = check_and_fix_schema_meta(post_id, ptype)
    if had_issue:
        found_count += 1
        status = "FIXED" if fixed else "FAIL"
        print(f"{status} ID {post_id} ({ptype}) /{slug}/  [{detail}]")
        if fixed:
            fixed_count += 1
    elif "no Rank Math schema meta" in detail:
        not_in_meta_count += 1
    time.sleep(0.2)

print(f"\n=== Summary ===")
print(f"Items with Rank Math schema issues found: {found_count}")
print(f"Successfully fixed:                       {fixed_count}")
print(f"Items with no Rank Math schema meta:      {not_in_meta_count}")

if not_in_meta_count > 100:
    print("""
NOTE: Most pages have no Rank Math custom schema storing these fields.
This means the bad schema block is likely hardcoded in a PHP function
(probably functions.php or a custom plugin).

NEXT STEP: Add the mu-plugin snippet to fix this at the PHP level:
  Copy tools/_fix_global_schema_wordpress_snippet.php to:
  wp-content/mu-plugins/fix-schema-errors.php
  (Create the mu-plugins directory if it doesn't exist)
""")
