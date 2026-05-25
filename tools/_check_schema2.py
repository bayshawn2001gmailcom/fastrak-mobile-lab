"""
Check homepage schema in detail — find which JSON-LD block has issues,
and check content.raw for embedded JSON-LD.
"""
import re, json, os, base64, socket, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".env")

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()).decode()
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

# 1. Parse both JSON-LD blocks separately from the homepage file
fpath = r"C:\Users\baysh\.claude\projects\c--Users-baysh-Fastrak-Mobile-Lab\eaa6d8b7-ec6b-45a7-a9f2-716b1c747b05\tool-results\mcp-claude_ai_Firecrawl-firecrawl_scrape-1778813437691.txt"
content = open(fpath, encoding="utf-8", errors="ignore").read()

try:
    outer = json.loads(content)
    html = outer.get("rawHtml") or outer.get("html") or content
except Exception:
    html = content

blocks = re.findall(
    r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    html, re.DOTALL | re.IGNORECASE
)

print(f"HOMEPAGE: {len(blocks)} JSON-LD block(s)\n")
for i, b in enumerate(blocks):
    print(f"--- BLOCK {i+1} ---")
    try:
        data = json.loads(b.strip())
        print(json.dumps(data, indent=2)[:3000])
    except Exception as e:
        print(f"parse error: {e}\nraw: {b[:200]!r}")
    print()

# 2. Check homepage content.raw for embedded JSON-LD
print("=" * 60)
print("Homepage content.raw — scanning for JSON-LD or schema.org")
print("=" * 60)

# Homepage is page ID — find it
r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages",
                 headers=HJ,
                 params={"slug": "", "status": "publish", "per_page": 1},
                 timeout=12)
# Try front page
r2 = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages",
                  headers=HJ,
                  params={"status": "publish", "per_page": 50, "_fields": "id,slug,link"},
                  timeout=15)
if r2.ok:
    pages = r2.json()
    # Find the home page (slug is usually "" or "home" or marked as front page)
    for p in pages:
        if p.get("slug") in ("home", "") or "fastrakmobilelab.com/" == p.get("link","").rstrip("/") + "/":
            print(f"Candidate home page: ID={p['id']} slug={p['slug']!r} link={p['link']!r}")

# Try getting the front page directly
r3 = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/2",
                  headers=HJ,
                  params={"context": "edit"},
                  timeout=12)
if r3.ok:
    d = r3.json()
    raw = (d.get("content") or {}).get("raw", "")
    print(f"\nPage ID 2 slug={d.get('slug')!r} — JSON-LD in raw: {'application/ld+json' in raw or 'schema.org' in raw}")
    if "schema.org" in raw or "ld+json" in raw:
        idx = raw.find("schema.org")
        print(raw[max(0, idx-100):idx+500])
