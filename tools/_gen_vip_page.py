"""One-off: generate and post the concierge/VIP page draft."""
import os, sys, re, base64, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
H = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

PROMPT = """Write an SEO-optimized service page for Fastrak Mobile Lab's concierge and VIP mobile lab services.

CRITICAL RULES:
- Service area business — we travel TO the client. NEVER mention a physical office or address.
- Always frame as "we come to you" — never "visit our location"
- Do NOT name any specific clients — reference client types only (athletes, executives, entertainers)
- Emphasize privacy, discretion, HIPAA compliance, and confidentiality throughout
- Lab processing fees may be covered by insurance; the mobile convenience fee is separate and NOT covered by insurance

Business: Fastrak Mobile Lab — licensed mobile specimen collection, metro Atlanta and Gwinnett County, GA
Primary keyword: concierge mobile phlebotomy Atlanta
Supporting keywords: VIP mobile blood draw Atlanta, private mobile lab services, discreet phlebotomy Atlanta, mobile blood draw for athletes

Requirements:
- H1: "Concierge Mobile Phlebotomy in Atlanta, GA" (exact)
- First paragraph: premium positioning — trusted by professional athletes, entertainers, and executives who require complete privacy and flexibility. We come to you, wherever you are.
- H2 #1: "Complete Privacy and Discretion" — HIPAA-compliant, no waiting rooms, no exposure to other patients, direct phlebotomist-to-client, strict confidentiality
- H2 #2: "Flexible Scheduling Around Your Life" — early morning, evenings, weekends, same-day appointments, hotel rooms, private residences, training facilities, offices
- H2 #3: "Who Our Concierge Clients Are" — professional athletes needing pre-season or league-required panels, entertainers and public figures, C-suite executives, high-net-worth individuals, anyone who values privacy above all
- H2 #4: "What We Collect" — comprehensive blood panels, hormone and performance panels, drug screening, DNA specimen collection, any test your physician orders
- FAQ (H2: "Frequently Asked Questions") with 3 questions: Can you come to my hotel or private residence? Is the service completely confidential? Can you accommodate same-day appointments?
- Closing CTA: premium tone — invite them to reach out discreetly
- Word count: 700-850 words
- Tone: premium concierge service, not clinical
- Output clean HTML only (h1, h2, h3, p, ul, li — no divs, no inline styles, no markdown, no html/head/body tags)
"""

print("Generating content...")
model = genai.GenerativeModel("gemini-2.0-flash")
resp = model.generate_content(PROMPT)
text = resp.text.strip()
if text.startswith("```"):
    text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
text = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", text, count=1,
              flags=re.IGNORECASE | re.DOTALL).strip()
print(f"{len(text.split())} words")

r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages", headers=H, json={
    "title": "Concierge Mobile Phlebotomy Atlanta, GA",
    "slug": "concierge-mobile-phlebotomy-atlanta",
    "content": text,
    "status": "draft",
}, timeout=30)
r.raise_for_status()
pid = r.json()["id"]
link = r.json().get("link", "?")
print(f"Draft posted: ID {pid}")

requests.post(f"{WP_SITE}/wp-json/rankmath/v1/updateMeta", headers=H, data={
    "objectID": pid,
    "objectType": "post",
    "meta[rank_math_focus_keyword]": "concierge mobile phlebotomy Atlanta",
    "meta[rank_math_title]": "Concierge Mobile Phlebotomy Atlanta | Fastrak Mobile Lab",
    "meta[rank_math_description]": (
        "Private, discreet mobile phlebotomy in Atlanta for athletes, executives, and public figures. "
        "Fastrak Mobile Lab comes to you — hotel, home, or office."
    )[:155],
}, timeout=20)
print("SEO meta set")
print(f"URL: {link}")
