"""
Batch-set Rank Math SEO titles and meta descriptions for all key pages.
Covers: pillar, service pages, Gwinnett hub, all city pages.
Run: python tools/_set_meta_titles.py
"""
import os, sys, base64, requests
from pathlib import Path

home_env = Path.home() / ".env"
if home_env.exists():
    for line in home_env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Missing WP credentials")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H_FORM = {"Authorization": f"Basic {creds}"}

# ---------------------------------------------------------------------------
# Optimized meta: title ≤ 60 chars | desc 145–158 chars
# Focus: keyword + location signal + CTR hook (no waiting room, same-day, etc.)
# ---------------------------------------------------------------------------
META = {

    # --- Pillar page ---
    1394: {
        "title": "At-Home Blood Draw Service Near Me | Fastrak Mobile Lab",
        "desc":  "Skip the waiting room. Fastrak Mobile Lab sends a certified phlebotomist to your home across metro Atlanta, GA. Same-day & next-day available. Book now.",
        "kw":    "at home blood draw service near me",
    },

    # --- Core service pages ---
    564: {
        "title": "Mobile Phlebotomy in Atlanta, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomists come to your home or office in Atlanta, GA. Blood draws, DNA testing, drug screening & wellness panels. Same-day available. Book now.",
        "kw":    "mobile phlebotomy Atlanta GA",
    },
    368: {
        "title": "At-Home Blood Draw in Atlanta, GA — Skip the Lab | Fastrak",
        "desc":  "Fastrak Mobile Lab sends a certified phlebotomist to your Atlanta home. No waiting room, no commute. Insurance accepted. Same-day appointments available.",
        "kw":    "at home blood draw Atlanta GA",
    },
    385: {
        "title": "Mobile Pre-Employment Drug Testing Atlanta, GA | Fastrak",
        "desc":  "DOT & non-DOT pre-employment drug testing at your Atlanta office or applicant's home. Chain-of-custody compliant. 24–48 hr turnaround. Book now.",
        "kw":    "pre-employment drug testing Atlanta GA",
    },
    395: {
        "title": "Mobile Drug & DNA Testing Atlanta, GA | Fastrak Mobile Lab",
        "desc":  "Court-admissible DNA, paternity & drug testing at your Atlanta location. Chain-of-custody compliant. Results in 24–72 hours. Licensed collectors. Book now.",
        "kw":    "mobile DNA testing Atlanta GA",
    },
    401: {
        "title": "At-Home Health & Wellness Panels Atlanta | Fastrak Mobile Lab",
        "desc":  "CBC, lipid, thyroid, hormone & vitamin panels collected at your Atlanta home. No clinic visit needed. Most insurance accepted. Fast results. Book now.",
        "kw":    "health wellness panels Atlanta GA",
    },
    407: {
        "title": "Concierge Mobile Phlebotomy Atlanta, GA | Fastrak Mobile Lab",
        "desc":  "Premium in-home phlebotomy for concierge practices & patients across Atlanta, GA. We coordinate with your physician and come to you. Same-day available.",
        "kw":    "concierge phlebotomy Atlanta GA",
    },
    413: {
        "title": "Order Your Own Lab Tests at Home | Fastrak Mobile Lab",
        "desc":  "No doctor's order needed. Choose from 1,000+ lab tests — we collect at your home in Atlanta & metro GA. Confidential results delivered digitally. Book now.",
        "kw":    "order your own lab tests at home",
    },
    375: {
        "title": "Specialty Kit Collection at Home Atlanta | Fastrak Mobile Lab",
        "desc":  "Fastrak Mobile Lab handles all specialty collection kits at your home — hormone panels, genetic tests, food sensitivity & more. Precise, compliant. Book now.",
        "kw":    "specialty kit collection mobile phlebotomy",
    },

    # --- Gwinnett service pages ---
    1262: {
        "title": "Mobile Drug Testing Gwinnett County, GA | Fastrak Mobile Lab",
        "desc":  "Court-admissible mobile drug testing throughout Gwinnett County. DOT & non-DOT panels. Chain-of-custody compliant. Results in 24–48 hours. Book now.",
        "kw":    "mobile drug testing Gwinnett County GA",
    },
    1263: {
        "title": "At-Home DNA Testing Gwinnett County, GA | Fastrak Mobile Lab",
        "desc":  "Court-admissible & personal-knowledge DNA and paternity testing at your Gwinnett County home. AABB-accredited labs. Results in 3–5 days. Book now.",
        "kw":    "DNA testing Gwinnett County GA",
    },
    1356: {
        "title": "Mobile Drug Testing in Atlanta, GA | Fastrak Mobile Lab",
        "desc":  "DOT & non-DOT mobile drug testing across metro Atlanta. Urine, oral fluid & hair follicle panels. Chain-of-custody compliant. 24–48 hr results. Book now.",
        "kw":    "mobile drug testing Atlanta GA",
    },
    1358: {
        "title": "Corporate Mobile Lab Services Atlanta, GA | Fastrak",
        "desc":  "On-site drug testing, pre-employment panels & wellness screenings for Atlanta businesses. We come to your office. DOT compliant. Book now.",
        "kw":    "corporate mobile lab services Atlanta GA",
    },
    1359: {
        "title": "Concierge Mobile Phlebotomy Atlanta | Fastrak Mobile Lab",
        "desc":  "Premium on-demand phlebotomy for Atlanta executives, seniors & concierge practices. We come to your home, hotel or office. Same-day available. Book now.",
        "kw":    "concierge mobile phlebotomy Atlanta",
    },

    # --- Gwinnett County hub ---
    1249: {
        "title": "Mobile Phlebotomy in Gwinnett County, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomists serving all of Gwinnett County, GA. At-home blood draws, DNA & drug testing. Same-day & next-day appointments available. Book now.",
        "kw":    "mobile phlebotomy Gwinnett County GA",
    },

    # --- City pages ---
    1250: {
        "title": "Mobile Blood Draw in Duluth, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab sends a licensed phlebotomist to your Duluth, GA home (30096 & 30097). No waiting room. DNA testing available. Same-day. Book now.",
        "kw":    "mobile blood draw Duluth GA",
    },
    1256: {
        "title": "Mobile Blood Draw in Lawrenceville, GA | Fastrak Mobile Lab",
        "desc":  "Skip the lab. Fastrak sends a certified phlebotomist to your Lawrenceville, GA home. Blood draws, DNA testing & drug screening. Same-day available. Book now.",
        "kw":    "mobile blood draw Lawrenceville GA",
    },
    1377: {
        "title": "Mobile Blood Draw Lawrenceville, GA — We Come to You | Fastrak",
        "desc":  "Licensed phlebotomist to your Lawrenceville, GA door. Blood draws & DNA testing in zip codes 30043–30046. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Lawrenceville GA",
    },
    1260: {
        "title": "Mobile Blood Draw in Tucker, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves Tucker, GA (30084). At-home blood draws, DNA & drug testing. No waiting room, no commute. Same-day available. Book now.",
        "kw":    "mobile blood draw Tucker GA",
    },
    1261: {
        "title": "Mobile Blood Draw in Conyers, GA — We Come to You | Fastrak",
        "desc":  "Licensed phlebotomist to your Conyers, GA home. Blood draws & DNA testing in zip codes 30012, 30013 & 30094. Same-day available. Book now.",
        "kw":    "mobile blood draw Conyers GA",
    },
    1329: {
        "title": "Mobile Blood Draw in Stone Mountain, GA | Fastrak Mobile Lab",
        "desc":  "Fastrak Mobile Lab serves Stone Mountain, GA (30083, 30087 & 30088). At-home blood draws, DNA testing & wellness panels. Same-day available. Book now.",
        "kw":    "mobile blood draw Stone Mountain GA",
    },
    1330: {
        "title": "Mobile Blood Draw Avondale Estates, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomist to your Avondale Estates, GA home (30002). Blood draws, DNA testing & wellness panels. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Avondale Estates GA",
    },
    1331: {
        "title": "Mobile Blood Draw in Smyrna, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves Smyrna, GA (30080 & 30082). At-home blood draws, DNA & drug testing. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Smyrna GA",
    },
    1108: {
        "title": "Mobile Blood Draw in Decatur, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves all Decatur, GA zip codes. At-home blood draws, DNA testing & wellness panels. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Decatur GA",
    },
    1109: {
        "title": "Mobile Blood Draw Sandy Springs, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomist to your Sandy Springs, GA home or office. Blood draws, DNA testing & concierge services. Same-day available. Book now.",
        "kw":    "mobile blood draw Sandy Springs GA",
    },
    1110: {
        "title": "Mobile Blood Draw in Marietta, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves all Marietta, GA zip codes in Cobb County. At-home blood draws, DNA & drug testing. Same-day available. Book now.",
        "kw":    "mobile blood draw Marietta GA",
    },
    1334: {
        "title": "Mobile Blood Draw in Lilburn, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves Lilburn, GA. At-home blood draws, DNA testing & drug screening. Same-day & next-day appointments available. Book now.",
        "kw":    "mobile blood draw Lilburn GA",
    },
    1248: {
        "title": "Mobile Blood Draw in Snellville, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomist to your Snellville, GA home. Blood draws, DNA & paternity testing. No waiting room. Same-day & next-day available. Book now.",
        "kw":    "mobile blood draw Snellville GA",
    },
    1382: {
        "title": "Mobile Blood Draw in Grayson, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves Grayson, GA (30017). At-home blood draws, DNA testing & wellness panels. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Grayson GA",
    },
    1383: {
        "title": "Mobile Blood Draw in Loganville, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomist to your Loganville, GA home (30052). Blood draws, DNA & paternity testing. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Loganville GA",
    },
    1332: {
        "title": "Mobile Blood Draw in Suwanee, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves Suwanee, GA. At-home blood draws, DNA testing & drug screening. Same-day & next-day appointments available. Book now.",
        "kw":    "mobile blood draw Suwanee GA",
    },
    1333: {
        "title": "Mobile Blood Draw in Sugar Hill, GA | Fastrak Mobile Lab",
        "desc":  "Licensed phlebotomist to your Sugar Hill, GA home. Blood draws, DNA testing & wellness panels. No waiting room. Same-day available. Book now.",
        "kw":    "mobile blood draw Sugar Hill GA",
    },
    1258: {
        "title": "Mobile Blood Draw in Norcross, GA — We Come to You | Fastrak",
        "desc":  "Fastrak Mobile Lab serves Norcross, GA. At-home blood draws, DNA & drug testing. Same-day & next-day appointments available. Book now.",
        "kw":    "mobile blood draw Norcross GA",
    },
    1328: {
        "title": "Mobile Blood Draw in Buford, GA — We Come to You | Fastrak",
        "desc":  "Licensed phlebotomist to your Buford, GA home. Blood draws, DNA testing & wellness panels. Same-day & next-day available. Book now.",
        "kw":    "mobile blood draw Buford GA",
    },
}


def set_rank_math(pid, title, desc, kw):
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=H_FORM,
        data={
            "objectID":   pid,
            "objectType": "post",
            "meta[rank_math_title]":            title,
            "meta[rank_math_description]":      desc,
            "meta[rank_math_focus_keyword]":    kw,
        },
        timeout=20,
    )
    return r.status_code


def main():
    print(f"Setting meta for {len(META)} pages...\n")
    ok = err = 0
    for pid, m in META.items():
        title = m["title"]
        desc  = m["desc"]
        kw    = m["kw"]
        t_len = len(title)
        d_len = len(desc)
        flag  = " !!LONG" if t_len > 60 else ""
        flag2 = " !!LONG" if d_len > 160 else ""
        status = set_rank_math(pid, title, desc, kw)
        if status == 200:
            print(f"  ID {pid:5}  OK   title={t_len}c{flag}  desc={d_len}c{flag2}")
            ok += 1
        else:
            print(f"  ID {pid:5}  HTTP {status}  FAILED")
            err += 1

    print(f"\n--- {ok} updated, {err} errors ---")


if __name__ == "__main__":
    main()
