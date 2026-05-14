"""
Patch booking links across all service and city pages.
- Replaces [BOOKING_LINK] placeholders with a proper hyperlink
- For pages with no link at all, injects a CTA anchor into the closing paragraph
"""
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

BOOKING_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"
ANCHOR_TEXT = "Book Your Mobile Blood Draw"
LINK_TAG = f'<a href="{BOOKING_URL}">{ANCHOR_TEXT}</a>'

# All pages to update: 4 service pages + 8 new city pages + older city pages with placeholder
PAGE_IDS = [
    # New service pages
    1356, 1357, 1358, 1359,
    # Newer city pages
    1335, 1334, 1333, 1332, 1331, 1330, 1329, 1328,
    # Older city pages
    1261, 1260, 1258, 1256, 1250, 1249, 1248,
    1110, 1109, 1108, 1107, 1106,
]

# CTA phrases to hyperlink in pages that have no link at all
CTA_PATTERNS = [
    r'(Book your mobile blood draw\b[^<]*)',
    r'(Book a mobile blood draw\b[^<]*)',
    r'(book your (?:mobile )?(?:blood draw|appointment)\b[^<]*)',
    r'(schedule (?:your )?(?:an )?appointment\b[^<]*)',
    r'(contact us (?:today )?to (?:schedule|book)\b[^<]*)',
    r'(reach out (?:discreetly )?\b[^<]*to (?:discuss|schedule|book)[^<]*)',
]

def patch_page(pid):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                     headers=H, params={"context": "edit"}, timeout=20)
    if not r.ok:
        return f"SKIP (fetch failed {r.status_code})"
    data = r.json()
    content = data["content"]["raw"]
    title = data["title"]["raw"]
    original = content

    # 1. Replace [BOOKING_LINK] placeholder
    content = re.sub(r'\[BOOKING_LINK\]', LINK_TAG, content, flags=re.IGNORECASE)

    # 2. If still no href, find and hyperlink the first CTA phrase
    if 'href=' not in content:
        for pat in CTA_PATTERNS:
            new, count = re.subn(
                pat,
                lambda m: f'<a href="{BOOKING_URL}">{m.group(1)}</a>',
                content,
                count=1,
                flags=re.IGNORECASE,
            )
            if count:
                content = new
                break

    if content == original:
        return "no change"

    patch = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                          headers=H, json={"content": content}, timeout=30)
    if patch.ok:
        return f"patched — {patch.json().get('link', '?')}"
    return f"FAILED {patch.status_code}"


for pid in PAGE_IDS:
    result = patch_page(pid)
    print(f"ID {pid}: {result}")
