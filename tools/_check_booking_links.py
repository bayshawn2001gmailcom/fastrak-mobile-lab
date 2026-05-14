"""Check which pages are missing the booking link."""
import os, re, base64, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
H = {"Authorization": f"Basic {creds}"}

BOOKING_DOMAIN = "api.leadconnectorhq.com"
IDS = [1261, 1260, 1258, 1256, 1250, 1249, 1248, 1110, 1109, 1108, 1107, 1106]

missing = []
for pid in IDS:
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                     headers=H, params={"context": "edit"}, timeout=20)
    data = r.json()
    content = data["content"]["raw"]
    title = data["title"]["raw"]
    has_booking = BOOKING_DOMAIN in content
    status = "OK" if has_booking else "MISSING"
    print(f"ID {pid} | {status} | {title}")
    if not has_booking:
        missing.append((pid, title, content))
        print(f"  Last 300 chars: ...{content[-300:].strip()}")
        print()

print(f"\nMissing booking link: {len(missing)} pages")
