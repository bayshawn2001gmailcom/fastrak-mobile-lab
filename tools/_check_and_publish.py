"""Check CTA links in 4 service pages then publish them."""
import os, re, base64, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
H = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

IDS = [1356, 1357, 1358, 1359]

print("=== Checking CTA links ===")
for pid in IDS:
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                     headers=H, params={"context": "edit"}, timeout=20)
    data = r.json()
    content = data["content"]["raw"]
    title = data["title"]["raw"]
    links = re.findall(r'href=["\']([^"\']+)["\']', content)
    placeholders = re.findall(r'\[BOOKING_LINK\]', content, re.IGNORECASE)
    print(f"\nID {pid} — {title}")
    print(f"  Links found: {links if links else 'none'}")
    print(f"  Placeholders: {placeholders if placeholders else 'none'}")

print("\n=== Publishing pages ===")
for pid in IDS:
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                      headers=H, json={"status": "publish"}, timeout=30)
    if r.ok:
        link = r.json().get("link", "?")
        print(f"ID {pid}: published — {link}")
    else:
        print(f"ID {pid}: FAILED {r.status_code}")
