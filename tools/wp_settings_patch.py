"""
Verify and patch WordPress site settings via REST API.
Primarily used to confirm blog_public=1 (search engines not blocked).

Usage:
  python tools/wp_settings_patch.py --check          # read current settings
  python tools/wp_settings_patch.py --fix-public     # ensure blog_public=1
"""
import os, sys, argparse, requests, base64, json
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


def get_settings():
    resp = requests.get(f"{WP_SITE}/wp-json/wp/v2/settings", headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.json()


def patch_settings(payload):
    resp = requests.post(f"{WP_SITE}/wp-json/wp/v2/settings", headers=HEADERS, json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Read current settings")
    parser.add_argument("--fix-public", action="store_true", help="Set blog_public=1 (allow indexing)")
    args = parser.parse_args()

    if not args.check and not args.fix_public:
        parser.print_help()
        return

    settings = get_settings()

    KEY_FIELDS = ["title", "description", "url", "timezone", "date_format",
                  "posts_per_page", "default_category", "use_smilies"]

    if args.check:
        print("Current WordPress Settings:")
        print(f"  Site URL:       {settings.get('url', '?')}")
        print(f"  Site Title:     {settings.get('title', '?')}")
        print(f"  Tagline:        {settings.get('description', '?')}")
        print(f"  Posts per page: {settings.get('posts_per_page', '?')}")
        print(f"  Timezone:       {settings.get('timezone', '?')}")

        # blog_public isn't always returned but attempt it
        blog_public = settings.get("blog_public")
        if blog_public is not None:
            status = "OPEN (indexing allowed)" if blog_public == 1 else "BLOCKED (noindex active!)"
            print(f"  blog_public:    {blog_public} -> {status}")
        else:
            print("  blog_public:    (not exposed via REST API — check WP Admin > Settings > Reading)")
        print()
        print("NOTE: Blog pagination noindex is controlled by Rank Math settings.")
        print("      Go to WP Admin > Rank Math > Titles & Meta > Posts > Archive > Noindex to toggle.")

    if args.fix_public:
        print("Attempting to set blog_public=1...")
        try:
            result = patch_settings({"blog_public": 1})
            new_val = result.get("blog_public", "unknown")
            print(f"  blog_public is now: {new_val}")
        except Exception as e:
            print(f"  Could not set via REST API: {e}")
            print("  Fallback: Go to WP Admin > Settings > Reading > uncheck 'Discourage search engines'")


if __name__ == "__main__":
    main()
