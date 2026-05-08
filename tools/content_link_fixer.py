"""
Find and replace stale internal links in WordPress page/post body content.
Targets links to slugs that now redirect (e.g. /services/, /mobile-drug-dna-testing-atlanta/).

Usage:
  python tools/content_link_fixer.py --dry-run          # show what would change
  python tools/content_link_fixer.py                    # apply fixes
  python tools/content_link_fixer.py --extra-map '{"old-slug":"new-slug"}'
"""
import os, sys, argparse, requests, base64, json, re, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER and WP_APP_PASSWORD must be set in ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
SESSION = requests.Session()

# Known stale slugs -> correct canonical slugs (from SEO_Blog_Status_Tracker)
DEFAULT_SLUG_MAP = {
    "/services/": "/mobile-phlebotomy-services/",
    "/mobile-drug-dna-testing-atlanta/": "/mobile-drug-testing-dna-collection/",
}


def fetch_all(resource):
    items = []
    page = 1
    while True:
        resp = SESSION.get(
            f"{WP_SITE}/wp-json/wp/v2/{resource}",
            headers=HEADERS,
            params={"status": "publish", "per_page": 100, "page": page, "context": "edit"},
            timeout=20,
        )
        if resp.status_code == 400:
            break
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        items.extend(batch)
        if page >= int(resp.headers.get("X-WP-TotalPages", 1)):
            break
        page += 1
        time.sleep(0.1)
    return items


def find_stale_links(content_html, slug_map):
    """Return list of (old_href, new_href) found in the HTML."""
    found = []
    for old_slug, new_slug in slug_map.items():
        pattern = re.compile(
            r'href=["\'](' + re.escape(WP_SITE) + re.escape(old_slug) + r'|' + re.escape(old_slug) + r')["\']',
            re.IGNORECASE,
        )
        matches = pattern.findall(content_html)
        for m in matches:
            found.append((m, new_slug if new_slug.startswith("http") else WP_SITE + new_slug))
    return found


def fix_content(content_html, slug_map):
    """Replace all stale links with their canonical destinations."""
    updated = content_html
    for old_slug, new_slug in slug_map.items():
        canonical = new_slug if new_slug.startswith("http") else WP_SITE + new_slug
        # Replace both absolute and relative forms
        updated = updated.replace(f'href="{WP_SITE}{old_slug}"', f'href="{canonical}"')
        updated = updated.replace(f"href='{WP_SITE}{old_slug}'", f"href='{canonical}'")
        updated = updated.replace(f'href="{old_slug}"', f'href="{canonical}"')
        updated = updated.replace(f"href='{old_slug}'", f"href='{canonical}'")
    return updated


def patch_item(resource, item_id, new_content, dry_run=False):
    if dry_run:
        return True
    resp = SESSION.post(
        f"{WP_SITE}/wp-json/wp/v2/{resource}/{item_id}",
        headers=HEADERS,
        json={"content": new_content},
        timeout=20,
    )
    return resp.ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--extra-map", help="JSON string of additional {old:new} slug replacements")
    args = parser.parse_args()

    slug_map = dict(DEFAULT_SLUG_MAP)
    if args.extra_map:
        slug_map.update(json.loads(args.extra_map))

    mode = "[DRY RUN]" if args.dry_run else "[LIVE]"
    print(f"{mode} Scanning content for stale links...")
    print(f"Slug map: {json.dumps(slug_map, indent=2)}\n")

    total_fixed = 0

    for resource in ("pages", "posts"):
        items = fetch_all(resource)
        print(f"Checking {len(items)} {resource}...")

        for item in items:
            item_id = item["id"]
            raw_content = item.get("content", {}).get("raw", "")
            if not raw_content:
                continue

            stale = find_stale_links(raw_content, slug_map)
            if not stale:
                continue

            slug = item.get("slug", "?")
            url = item.get("link", "?")
            print(f"\n  [{resource[:-1].upper()} {item_id}] /{slug}")
            print(f"  URL: {url}")
            for old, new in stale:
                print(f"    STALE: {old} -> {new}")

            if not args.dry_run:
                new_content = fix_content(raw_content, slug_map)
                if patch_item(resource, item_id, new_content):
                    print(f"    [OK] Content updated")
                    total_fixed += 1
                else:
                    print(f"    [FAIL] Could not update")
                time.sleep(0.1)
            else:
                total_fixed += 1

    suffix = " (dry run — no changes applied)" if args.dry_run else ""
    print(f"\nDone. {total_fixed} item(s) with stale links{suffix}.")


if __name__ == "__main__":
    main()
