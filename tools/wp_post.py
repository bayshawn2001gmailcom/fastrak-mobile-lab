"""
Create or update a page/post on fastrakmobilelab.com via WordPress REST API.
Usage:
  python tools/wp_post.py --title "Mobile Phlebotomy Atlanta" --slug mobile-phlebotomy-atlanta --content content.html
  python tools/wp_post.py --id 123 --title "Updated Title"    # update existing
  python tools/wp_post.py --help
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


def create_or_update(post_id=None, content_type="pages", **fields):
    if post_id:
        url = f"{WP_SITE}/wp-json/wp/v2/{content_type}/{post_id}"
        resp = requests.post(url, headers=HEADERS, json=fields)
    else:
        url = f"{WP_SITE}/wp-json/wp/v2/{content_type}"
        resp = requests.post(url, headers=HEADERS, json=fields)

    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        resp.raise_for_status()

    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, help="Post/page ID to update (omit to create new)")
    parser.add_argument("--title", required=True, help="Page/post title")
    parser.add_argument("--slug", help="URL slug (e.g. mobile-phlebotomy-atlanta)")
    parser.add_argument("--content", help="HTML content string or path to .html file")
    parser.add_argument("--status", default="draft", choices=["draft", "publish", "private"])
    parser.add_argument("--type", default="pages", choices=["pages", "posts"])
    parser.add_argument("--parent", type=int, help="Parent page ID (for sub-pages)")
    args = parser.parse_args()

    content = ""
    if args.content:
        if os.path.isfile(args.content):
            with open(args.content) as f:
                content = f.read()
        else:
            content = args.content

    fields = {"title": args.title, "status": args.status}
    if content:
        fields["content"] = content
    if args.slug:
        fields["slug"] = args.slug
    if args.parent:
        fields["parent"] = args.parent

    result = create_or_update(post_id=args.id, content_type=args.type, **fields)

    post_id = result.get("id")
    link = result.get("link")
    status = result.get("status")
    print(f"Success!")
    print(f"  ID:     {post_id}")
    print(f"  Status: {status}")
    print(f"  URL:    {link}")
    print(f"\nTo set SEO metadata:")
    print(f"  python tools/wp_update_seo.py --id {post_id} --keyword \"your keyword\" --title \"SEO Title\" --description \"Meta description\"")


if __name__ == "__main__":
    main()
