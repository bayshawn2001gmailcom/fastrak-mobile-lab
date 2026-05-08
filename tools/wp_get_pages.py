"""
Fetch pages/posts from fastrakmobilelab.com WordPress REST API.
Usage:
  python tools/wp_get_pages.py                    # list all pages
  python tools/wp_get_pages.py --slug mobile-phlebotomy-atlanta
  python tools/wp_get_pages.py --type posts       # list posts instead
"""
import os, sys, argparse, requests, base64, json
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.expanduser("~"), ".env"), override=False)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER and WP_APP_PASSWORD must be set in ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}


def get_pages(content_type="pages", slug=None):
    url = f"{WP_SITE}/wp-json/wp/v2/{content_type}"
    params = {"per_page": 100, "status": "any"}
    if slug:
        params["slug"] = slug

    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Filter by slug")
    parser.add_argument("--type", default="pages", choices=["pages", "posts"], help="Content type")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    items = get_pages(args.type, args.slug)

    if not items:
        print("No results found.")
        return

    if args.json:
        print(json.dumps(items, indent=2))
        return

    for item in items:
        status = item.get("status", "?")
        slug = item.get("slug", "?")
        title = item.get("title", {}).get("rendered", "?")
        post_id = item.get("id", "?")
        link = item.get("link", "?")
        print(f"[{post_id}] {status:10} /{slug}")
        print(f"       Title: {title}")
        print(f"       URL:   {link}")
        print()


if __name__ == "__main__":
    main()
