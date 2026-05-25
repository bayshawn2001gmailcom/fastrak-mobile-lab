import re, json

files = [
    (r"C:\Users\baysh\.claude\projects\c--Users-baysh-Fastrak-Mobile-Lab\eaa6d8b7-ec6b-45a7-a9f2-716b1c747b05\tool-results\mcp-claude_ai_Firecrawl-firecrawl_scrape-1778813437691.txt", "HOMEPAGE"),
    (r"C:\Users\baysh\.claude\projects\c--Users-baysh-Fastrak-Mobile-Lab\eaa6d8b7-ec6b-45a7-a9f2-716b1c747b05\tool-results\mcp-claude_ai_Firecrawl-firecrawl_scrape-1778813439951.txt", "HEALTH-WELLNESS"),
]

for fpath, label in files:
    content = open(fpath, encoding="utf-8", errors="ignore").read()
    # Firecrawl wraps rawHtml in JSON — decode the outer layer
    try:
        outer = json.loads(content)
        html = outer.get("rawHtml") or outer.get("html") or content
    except Exception:
        html = content

    # Extract JSON-LD blocks
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE
    )
    print(f"=== {label} — {len(blocks)} JSON-LD block(s) ===")
    for i, b in enumerate(blocks):
        try:
            data = json.loads(b.strip())
            types = data.get("@graph", [data])
            for node in types:
                t = node.get("@type", "?")
                name = node.get("name", "")
                addr = node.get("address", None)
                desc = str(node.get("description", ""))[:80]
                url = node.get("url", "")
                print(f"  @type={t}  name={name!r}")
                if addr:
                    print(f"    address={json.dumps(addr)}")
                if desc:
                    print(f"    description={desc!r}")
                if url:
                    print(f"    url={url!r}")
        except Exception as e:
            print(f"  block {i+1} parse error: {e}")
            print(f"  raw (first 300): {b[:300]!r}")
    print()
