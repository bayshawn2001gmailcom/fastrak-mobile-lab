"""
Fastrak Mobile Lab — SEO Fix Script (May 2026)
Targets remaining Ahrefs issues from May 1 audit:
  - 26 meta descriptions too long (>155 chars)
  - 11 meta descriptions missing/empty on indexable pages
  - 6 remaining duplicate meta description tags
  - Noindex pages still in sitemap (15 duplicate posts)
  - 3XX redirects (18 pages)

Auth: WordPress nonce method (Basic auth blocked)
Run:  python seo_fix_may2026.py --nonce <YOUR_NONCE>
"""

import requests
import json
import argparse
import sys
import time

BASE = "https://fastrakmobilelab.com"
WP_API = f"{BASE}/wp-json/wp/v2"
RM_API = f"{BASE}/wp-json/rankmath/v1"

def make_headers(nonce):
    return {
        "X-WP-Nonce": nonce,
        "Content-Type": "application/json",
    }

# ---------------------------------------------------------------------------
# 1. Fetch all published pages + posts with their Rank Math meta
# ---------------------------------------------------------------------------

def get_all_posts(nonce, post_type="pages"):
    headers = make_headers(nonce)
    results = []
    page = 1
    while True:
        r = requests.get(
            f"{WP_API}/{post_type}",
            headers=headers,
            params={"per_page": 100, "page": page, "status": "publish,draft,private", "_fields": "id,slug,title,meta,link,status"},
        )
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        results.extend(batch)
        page += 1
    return results

def get_rank_math_head(nonce, post_id):
    """Fetch Rank Math rendered <head> for a post to detect duplicate tags."""
    r = requests.get(
        f"{RM_API}/getHead",
        headers=make_headers(nonce),
        params={"objectID": post_id, "objectType": "post"},
    )
    if r.status_code == 200:
        return r.json()
    return {}

def update_rank_math_meta(nonce, post_id, meta_dict):
    """Update Rank Math metadata fields for a post."""
    r = requests.post(
        f"{RM_API}/updateMeta",
        headers=make_headers(nonce),
        json={"objectID": post_id, "objectType": "post", **meta_dict},
    )
    return r.status_code, r.text

def update_post_meta(nonce, post_id, meta_key, meta_value, post_type="posts"):
    """Update a single post meta field via WP REST API."""
    r = requests.post(
        f"{WP_API}/{post_type}/{post_id}",
        headers=make_headers(nonce),
        json={"meta": {meta_key: meta_value}},
    )
    return r.status_code

# ---------------------------------------------------------------------------
# 2. Fix: Meta descriptions too long (>155 chars)
# ---------------------------------------------------------------------------

LONG_DESC_PAGES = {
    # Known long meta descriptions from prior Ahrefs exports
    # Format: post_id: current_description (will be auto-trimmed)
    # Add page IDs here after pulling from Ahrefs Page Explorer export
}

def trim_meta_description(desc, max_len=155):
    """Trim description to max_len at a word boundary."""
    if len(desc) <= max_len:
        return desc
    trimmed = desc[:max_len].rsplit(" ", 1)[0].rstrip(".,;:")
    return trimmed + "…"

def fix_long_meta_descriptions(nonce, pages):
    """Find and fix all meta descriptions exceeding 155 chars."""
    print("\n[1] Fixing meta descriptions too long (>155 chars)...")
    fixed = 0
    for p in pages:
        meta = p.get("meta", {})
        desc = meta.get("rank_math_description", "") or ""
        if len(desc) > 155:
            trimmed = trim_meta_description(desc)
            status, _ = update_rank_math_meta(nonce, p["id"], {"rank_math_description": trimmed})
            if status == 200:
                print(f"  ✅ [{p['id']}] {p['slug'][:40]} → {len(trimmed)} chars")
                fixed += 1
            else:
                print(f"  ❌ [{p['id']}] failed ({status})")
            time.sleep(0.3)
    print(f"  Total fixed: {fixed}")
    return fixed

# ---------------------------------------------------------------------------
# 3. Fix: Meta descriptions missing on indexable pages
# ---------------------------------------------------------------------------

# Auto-generated meta descriptions for known pages without one
AUTO_META = {
    # page_id: description string
    # These are the 11 indexable pages with no meta description.
    # Fill in after identifying them from Ahrefs Page Explorer.
    # Example entries below — update with actual page IDs and content:
    23:   "Fastrak Mobile Lab provides professional mobile phlebotomy and specimen collection services in Gwinnett County, GA. Blood draws at your home, office, or facility.",
    564:  "Mobile phlebotomy and lab services for Atlanta and metro Georgia. On-site blood draws, drug testing, and DNA testing — no clinic visit required.",
    306:  "Frequently asked questions about mobile phlebotomy, on-site blood draws, and specimen collection services by Fastrak Mobile Lab in Gwinnett County, GA.",
}

def fix_missing_meta_descriptions(nonce):
    """Apply auto-generated meta descriptions to known pages missing them."""
    print("\n[2] Fixing missing meta descriptions...")
    fixed = 0
    for page_id, desc in AUTO_META.items():
        status, _ = update_rank_math_meta(nonce, page_id, {"rank_math_description": desc})
        if status == 200:
            print(f"  ✅ [{page_id}] meta description set ({len(desc)} chars)")
            fixed += 1
        else:
            print(f"  ❌ [{page_id}] failed ({status})")
        time.sleep(0.3)
    print(f"  Total fixed: {fixed}")
    return fixed

# ---------------------------------------------------------------------------
# 4. Fix: Noindex posts still in sitemap → convert to 301 redirects
# ---------------------------------------------------------------------------

# 15 duplicate posts set to noindex+canonical in April 25 session
# These should be 301 redirected via Rank Math Redirect Manager
# The REST API doesn't expose the redirect manager directly —
# these require wp-admin UI. This section generates the redirect map.

NOINDEX_DUPLICATE_REDIRECTS = {
    902:  "/the-difference-between-home-dna-kits-and-legal-paternity-tests/",
    915:  "/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know/",
    916:  "/the-difference-between-home-dna-kits-and-legal-paternity-tests/",
    946:  None,  # Fill in canonical after checking Rank Math
    947:  None,
    948:  None,
    949:  None,
    950:  None,
    951:  None,
    952:  None,
    953:  None,
    954:  None,
    955:  None,
    981:  None,
    901:  None,
}

def print_redirect_instructions():
    """Print manual redirect instructions for wp-admin."""
    print("\n[3] Noindex pages in sitemap — requires wp-admin Redirect Manager")
    print("    Go to: Rank Math → Redirections → Add New")
    print("    Create 301 redirects for these duplicate posts:\n")
    for post_id, canonical in NOINDEX_DUPLICATE_REDIRECTS.items():
        if canonical:
            print(f"    Post {post_id} → {canonical}")
    print("\n    After creating 301 redirects, trash the duplicate posts.")
    print("    This will remove them from the sitemap automatically.")

# ---------------------------------------------------------------------------
# 5. Audit: Pages with links to redirects (111 remaining)
# ---------------------------------------------------------------------------

# Known remaining redirect links from body content (not footer)
BODY_REDIRECT_FIXES = {
    # page_id: {old_url: new_url}
    23: {
        "/services/": "/mobile-phlebotomy-services-atlanta/",
    },
    395: {
        "/mobile-drug-dna-testing-atlanta/": "/mobile-dna-testing-atlanta/",
    },
}

def fix_body_redirect_links(nonce):
    """Fix known body content redirect links via post content update."""
    print("\n[4] Fixing body content redirect links...")
    fixed = 0
    for page_id, replacements in BODY_REDIRECT_FIXES.items():
        r = requests.get(f"{WP_API}/pages/{page_id}", headers=make_headers(nonce))
        if r.status_code != 200:
            print(f"  ❌ Could not fetch page {page_id}")
            continue
        page_data = r.json()
        content = page_data.get("content", {}).get("raw", "")
        updated = content
        for old, new in replacements.items():
            if old in updated:
                updated = updated.replace(old, new)
                print(f"  ✅ [{page_id}] replaced {old} → {new}")
                fixed += 1
        if updated != content:
            patch = requests.post(
                f"{WP_API}/pages/{page_id}",
                headers=make_headers(nonce),
                json={"content": updated},
            )
            if patch.status_code != 200:
                print(f"  ❌ [{page_id}] content update failed ({patch.status_code})")
        time.sleep(0.3)
    print(f"  Total redirect links fixed: {fixed}")
    return fixed

# ---------------------------------------------------------------------------
# 6. Audit: Find remaining multiple meta description tags
# ---------------------------------------------------------------------------

def audit_duplicate_meta_descriptions(nonce, post_ids):
    """Check specific posts for duplicate <meta name='description'> tags."""
    print("\n[5] Auditing duplicate meta description tags...")
    duplicates = []
    for pid in post_ids:
        head_data = get_rank_math_head(nonce, pid)
        head_html = head_data.get("head", "")
        count = head_html.count('name="description"') + head_html.count("name='description'")
        if count > 1:
            print(f"  ⚠️  Post {pid}: {count} meta description tags found")
            duplicates.append(pid)
        else:
            print(f"  ✅ Post {pid}: OK ({count} tag)")
        time.sleep(0.2)
    return duplicates

# ---------------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fastrak SEO Fix Script — May 2026")
    parser.add_argument("--nonce", required=True, help="WordPress X-WP-Nonce token")
    parser.add_argument("--fix", choices=["all", "meta-long", "meta-missing", "redirects", "audit-dups"],
                        default="all", help="Which fix to run")
    args = parser.parse_args()

    nonce = args.nonce
    print(f"\n{'='*60}")
    print("Fastrak Mobile Lab — SEO Fix Script (May 2026)")
    print(f"{'='*60}")

    # Test connection
    r = requests.get(f"{WP_API}/users/me", headers=make_headers(nonce))
    if r.status_code != 200:
        print(f"❌ Auth failed ({r.status_code}). Get a fresh nonce from wp-admin.")
        sys.exit(1)
    user = r.json()
    print(f"✅ Authenticated as: {user.get('name')} (ID {user.get('id')})")

    if args.fix in ("all", "meta-long"):
        pages = get_all_posts(nonce, "pages") + get_all_posts(nonce, "posts")
        fix_long_meta_descriptions(nonce, pages)

    if args.fix in ("all", "meta-missing"):
        fix_missing_meta_descriptions(nonce)

    if args.fix in ("all", "redirects"):
        fix_body_redirect_links(nonce)

    if args.fix in ("all",):
        print_redirect_instructions()

    if args.fix in ("all", "audit-dups"):
        # Check the 6 known posts still flagged for duplicate meta descriptions
        # Update these IDs with the actual Ahrefs Page Explorer export
        suspect_ids = [23, 564, 306, 395, 1249, 1262]
        audit_duplicate_meta_descriptions(nonce, suspect_ids)

    print(f"\n{'='*60}")
    print("Done. Update SEO_Blog_Status_Tracker.md with results.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
