"""
Set Rank Math SEO metadata (focus keyword, title, meta description) on a WordPress page/post.
Usage:
  python tools/wp_update_seo.py --id 123 --keyword "mobile phlebotomy atlanta" \
      --title "Mobile Phlebotomy Atlanta | Fastrak Mobile Lab" \
      --description "Get blood drawn at home in Atlanta. Licensed phlebotomists. Book today."
"""
import os, sys, argparse, requests, base64
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


def update_rank_math(post_id, keyword=None, seo_title=None, description=None):
    url = f"{WP_SITE}/wp-json/rankmath/v1/updateMeta"
    payload = {"objectID": post_id, "objectType": "post"}

    if keyword:
        payload["meta[rank_math_focus_keyword]"] = keyword
    if seo_title:
        payload["meta[rank_math_title]"] = seo_title
    if description:
        payload["meta[rank_math_description]"] = description

    resp = requests.post(url, headers=HEADERS, data=payload)

    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        resp.raise_for_status()

    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True, help="WordPress post/page ID")
    parser.add_argument("--keyword", help="Focus keyword for Rank Math")
    parser.add_argument("--title", help="SEO title (under 60 chars recommended)")
    parser.add_argument("--description", help="Meta description (140–155 chars recommended)")
    args = parser.parse_args()

    if not any([args.keyword, args.title, args.description]):
        sys.exit("Error: provide at least one of --keyword, --title, --description")

    if args.title and len(args.title) > 60:
        print(f"Warning: SEO title is {len(args.title)} chars (recommended: under 60)")
    if args.description:
        dlen = len(args.description)
        if dlen < 140 or dlen > 155:
            print(f"Warning: Meta description is {dlen} chars (recommended: 140–155)")

    result = update_rank_math(args.id, args.keyword, args.title, args.description)
    print(f"SEO metadata updated for post ID {args.id}")
    print(f"Response: {result}")


if __name__ == "__main__":
    main()
