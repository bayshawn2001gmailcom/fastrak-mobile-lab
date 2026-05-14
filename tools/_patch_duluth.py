"""Patch booking link into Duluth city page."""
import os, base64, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
H = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

BOOKING_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"

r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/1250",
                 headers=H, params={"context": "edit"}, timeout=20)
content = r.json()["content"]["raw"]

# Append a CTA paragraph before the closing tagline
cta_para = (
    f'\n<!-- wp:paragraph -->\n'
    f'<p>Ready to get started? '
    f'<a href="{BOOKING_URL}">Book Your Mobile Blood Draw</a> '
    f'and a certified phlebotomist will come to you in Duluth.</p>\n'
    f'<!-- /wp:paragraph -->\n'
)

# Insert before the closing italics tagline paragraph
insert_before = "<!-- wp:paragraph -->\n<p><em>Fastrak Mobile Lab"
content = content.replace(insert_before, cta_para + insert_before)

patch = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages/1250",
                      headers=H, json={"content": content}, timeout=30)
print("patched OK" if patch.ok else f"FAILED {patch.status_code}")
print(patch.json().get("link", "?"))
