"""
Internal linking pass for Gwinnett County city pages.
- Hub page gets a full city grid linking to every city page
- Each city page gets a "Service Areas" footer linking back to the hub + neighbors
Run: python tools/_internal_linking_pass.py
"""
import os, sys, base64, requests, re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER / WP_APP_PASSWORD missing from ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H_JSON = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
H_FORM = {"Authorization": f"Basic {creds}"}

BASE = WP_SITE

# ---------------------------------------------------------------------------
# City definitions — (page_id, display_name, url_path)
# ---------------------------------------------------------------------------
CITIES = [
    (1377, "Lawrenceville",  "/mobile-phlebotomy-dna-testing-lawrenceville-ga/"),
    (1334, "Lilburn",        "/mobile-phlebotomy-lilburn-ga/"),
    (1248, "Snellville",     "/mobile-phlebotomy-snellville-ga/"),
    (1382, "Grayson",        "/mobile-phlebotomy-dna-testing-grayson-ga/"),
    (1383, "Loganville",     "/mobile-phlebotomy-dna-testing-loganville-ga/"),
    (1332, "Suwanee",        "/mobile-phlebotomy-suwanee-ga/"),
    (1333, "Sugar Hill",     "/mobile-phlebotomy-sugar-hill-ga/"),
    (1258, "Norcross",       "/mobile-phlebotomy-norcross-ga/"),
    (1328, "Buford",         "/mobile-phlebotomy-buford-ga/"),
]

HUB_ID   = 1249
HUB_PATH = "/mobile-phlebotomy-gwinnett-county-ga/"

# Neighbors each city should highlight (display_name keys)
NEIGHBORS = {
    "Lawrenceville": ["Lilburn", "Snellville", "Grayson", "Norcross"],
    "Lilburn":       ["Lawrenceville", "Norcross", "Snellville"],
    "Snellville":    ["Lawrenceville", "Lilburn", "Grayson"],
    "Grayson":       ["Lawrenceville", "Snellville", "Loganville"],
    "Loganville":    ["Grayson", "Snellville"],
    "Suwanee":       ["Buford", "Sugar Hill", "Norcross"],
    "Sugar Hill":    ["Suwanee", "Buford"],
    "Norcross":      ["Lilburn", "Lawrenceville", "Suwanee"],
    "Buford":        ["Suwanee", "Sugar Hill"],
}

CITY_BY_NAME = {name: (pid, path) for pid, name, path in CITIES}

MARKER = "<!-- fastrak-internal-links -->"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_raw(pid):
    r = requests.get(f"{BASE}/wp-json/wp/v2/pages/{pid}",
                     headers=H_FORM,
                     params={"context": "edit", "_fields": "content"},
                     timeout=20)
    r.raise_for_status()
    return r.json()["content"]["raw"]


def patch_content(pid, new_raw):
    r = requests.post(f"{BASE}/wp-json/wp/v2/pages/{pid}",
                      headers=H_JSON,
                      json={"content": new_raw},
                      timeout=30)
    r.raise_for_status()
    return r.status_code


def already_patched(raw):
    return MARKER in raw


# ---------------------------------------------------------------------------
# Build link blocks
# ---------------------------------------------------------------------------

def hub_city_grid():
    items = "\n".join(
        f'  <li><a href="{BASE}{path}">Mobile Phlebotomy in {name}, GA</a></li>'
        for _, name, path in CITIES
    )
    return f"""
{MARKER}
<h2>Gwinnett County Cities We Serve</h2>
<p>Fastrak Mobile Lab provides mobile blood draws, at-home lab testing, and DNA specimen collection throughout Gwinnett County. Select your city for local service details:</p>
<ul>
{items}
</ul>
"""


def city_service_area_block(city_name, city_path):
    neighbor_links = []
    for nb in NEIGHBORS.get(city_name, []):
        if nb in CITY_BY_NAME:
            _, nb_path = CITY_BY_NAME[nb]
            neighbor_links.append(
                f'<a href="{BASE}{nb_path}">Mobile phlebotomy in {nb}, GA</a>'
            )

    neighbor_html = ""
    if neighbor_links:
        neighbor_html = (
            "<p>We also serve nearby communities: "
            + " &bull; ".join(neighbor_links)
            + ".</p>"
        )

    return f"""
{MARKER}
<h2>Serving All of Gwinnett County</h2>
<p>{city_name} is part of our broader <a href="{BASE}{HUB_PATH}">Gwinnett County mobile phlebotomy service area</a>. Whether you're in {city_name} or a neighboring community, Fastrak Mobile Lab comes to you.</p>
{neighbor_html}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    results = []

    # --- Patch hub page ---
    print(f"[HUB] ID {HUB_ID} — reading...")
    raw = get_raw(HUB_ID)
    if already_patched(raw):
        print(f"[HUB] already patched — skipping")
        results.append(("HUB", HUB_ID, "skipped"))
    else:
        new_raw = raw.rstrip() + "\n" + hub_city_grid()
        status = patch_content(HUB_ID, new_raw)
        print(f"[HUB] patched — HTTP {status}")
        results.append(("HUB", HUB_ID, f"HTTP {status}"))

    # --- Patch each city page ---
    for pid, name, path in CITIES:
        print(f"[{name}] ID {pid} — reading...")
        raw = get_raw(pid)
        if already_patched(raw):
            print(f"[{name}] already patched — skipping")
            results.append((name, pid, "skipped"))
            continue
        block = city_service_area_block(name, path)
        new_raw = raw.rstrip() + "\n" + block
        status = patch_content(pid, new_raw)
        print(f"[{name}] patched — HTTP {status}")
        results.append((name, pid, f"HTTP {status}"))

    print("\n--- Summary ---")
    for name, pid, outcome in results:
        print(f"  {name:20} ID {pid}  {outcome}")


if __name__ == "__main__":
    main()
