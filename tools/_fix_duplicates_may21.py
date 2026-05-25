"""
Fix duplicate posts from May 21 2026 GSC/Ahrefs investigation.
Root cause: 15 posts were published twice, generating -2 / -3 slug variants.
Google found all of them (106 non-indexed vs 54 indexed) and refused to index
the duplicates as thin/duplicate content.

Fix:
  1. Probe Rank Math redirections endpoint
  2. Create 301 redirect for each duplicate slug → canonical slug
  3. Trash the duplicate post so it disappears from sitemap/crawl
"""
import os, base64, socket, requests, time, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".env")

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

# Duplicate slug → canonical slug (all 15 pairs from sitemap)
REDIRECT_PAIRS = [
    ("the-difference-between-home-dna-kits-and-legal-paternity-tests-2",
     "/the-difference-between-home-dna-kits-and-legal-paternity-tests/"),
    ("the-difference-between-home-dna-kits-and-legal-paternity-tests-3",
     "/the-difference-between-home-dna-kits-and-legal-paternity-tests/"),
    ("aabb-accredited-dna-testing-for-immigration-what-you-need-to-know-2",
     "/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know/"),
    ("non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate-2",
     "/non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate/"),
    ("mobile-dot-drug-testing-for-fleet-managers-compliance-made-easy-in-gwinnett-2",
     "/mobile-dot-drug-testing-for-fleet-managers-compliance-made-easy-in-gwinnett/"),
    ("24-7-mobile-post-accident-breathalyzer-drug-screening-in-metro-atlanta-2",
     "/24-7-mobile-post-accident-breathalyzer-drug-screening-in-metro-atlanta/"),
    ("onsite-background-checks-fingerprinting-for-atlanta-healthcare-staffing-2",
     "/onsite-background-checks-fingerprinting-for-atlanta-healthcare-staffing/"),
    ("mobile-dot-physicals-for-cdl-drivers-same-day-appointments-in-norcross-2",
     "/mobile-dot-physicals-for-cdl-drivers-same-day-appointments-in-norcross/"),
    ("mobile-gender-reveal-dna-testing-early-clinical-results-in-lawrenceville-2",
     "/mobile-gender-reveal-dna-testing-early-clinical-results-in-lawrenceville/"),
    ("mobile-respiratory-fit-testing-osha-compliance-for-georgia-construction-2",
     "/mobile-respiratory-fit-testing-osha-compliance-for-georgia-construction/"),
    ("concierge-mobile-blood-draws-professional-phlebotomy-at-your-atlanta-home-2",
     "/concierge-mobile-blood-draws-professional-phlebotomy-at-your-atlanta-home/"),
    ("onsite-corporate-flu-wellness-clinics-mobile-immunizations-in-atlanta-2",
     "/onsite-corporate-flu-wellness-clinics-mobile-immunizations-in-atlanta/"),
    ("legal-admissibility-mobile-dna-paternity-testing-for-georgia-court-cases-2",
     "/legal-admissibility-mobile-dna-paternity-testing-for-georgia-court-cases/"),
    ("discreet-mobile-infidelity-dna-testing-private-labs-serving-gwinnett-county-2",
     "/discreet-mobile-infidelity-dna-testing-private-labs-serving-gwinnett-county/"),
    ("legal-chain-of-custody-dna-testing-gwinnett-county-law-support-2",
     "/legal-chain-of-custody-dna-testing-gwinnett-county-law-support/"),
]


def find_post(slug):
    """Find post ID across pages and posts endpoints."""
    for ptype in ("posts", "pages"):
        r = requests.get(
            f"{WP_SITE}/wp-json/wp/v2/{ptype}",
            headers=HJ,
            params={"slug": slug, "status": "publish", "per_page": 1},
            timeout=12,
        )
        if r.ok and r.json():
            return r.json()[0]["id"], ptype
        time.sleep(0.2)
    return None, None


def create_rankmath_redirect(from_slug, to_url):
    """
    Try Rank Math's redirections REST endpoint.
    Returns (success, status_code, response_text).
    """
    payload = {
        "url": f"/{from_slug}/",
        "redirect_to": to_url,
        "redirect_type": "301",
        "status": "active",
    }
    r = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/redirections",
        headers=HJ,
        json=payload,
        timeout=15,
    )
    return r.ok, r.status_code, r.text[:200]


def trash_post(post_id, post_type):
    """Move post to trash (WordPress soft-delete)."""
    r = requests.delete(
        f"{WP_SITE}/wp-json/wp/v2/{post_type}/{post_id}",
        headers=HJ,
        timeout=15,
    )
    return r.ok, r.status_code


# ── PROBE: what Rank Math redirection endpoints are available? ────────────────
print("=" * 65)
print("Probing Rank Math redirections endpoint...")
print("=" * 65)
probe = requests.get(f"{WP_SITE}/wp-json/rankmath/v1/", headers=HJ, timeout=10)
if probe.ok:
    ns = probe.json()
    routes = list(ns.get("routes", {}).keys())
    rm_routes = [r for r in routes if "redirect" in r.lower()]
    print(f"Rank Math redirect routes: {rm_routes or 'none found'}")
else:
    print(f"Namespace probe failed: HTTP {probe.status_code}")

print()


# ── MAIN FIX LOOP ─────────────────────────────────────────────────────────────
print("=" * 65)
print(f"Processing {len(REDIRECT_PAIRS)} duplicate pairs...")
print("=" * 65)

results = {"redirect_ok": 0, "redirect_fail": 0, "trash_ok": 0, "trash_fail": 0, "not_found": 0}

for dup_slug, canonical_url in REDIRECT_PAIRS:
    post_id, post_type = find_post(dup_slug)

    if not post_id:
        print(f"  NOT FOUND  /{dup_slug}/")
        results["not_found"] += 1
        time.sleep(0.3)
        continue

    # 1. Create 301 redirect
    redir_ok, redir_code, redir_body = create_rankmath_redirect(dup_slug, canonical_url)

    # 2. Trash the duplicate post
    trash_ok, trash_code = trash_post(post_id, post_type)

    status = (
        f"{'REDIR_OK' if redir_ok else f'REDIR_FAIL({redir_code})'}"
        f" | "
        f"{'TRASH_OK' if trash_ok else f'TRASH_FAIL({trash_code})'}"
    )
    print(f"  ID {post_id:5} ({post_type}) /{dup_slug}/")
    print(f"    → {canonical_url}")
    print(f"    {status}")
    if not redir_ok:
        print(f"    redir body: {redir_body}")

    if redir_ok:
        results["redirect_ok"] += 1
    else:
        results["redirect_fail"] += 1

    if trash_ok:
        results["trash_ok"] += 1
    else:
        results["trash_fail"] += 1

    time.sleep(0.5)

print()
print("=" * 65)
print("Summary")
print("=" * 65)
print(f"  Redirects created : {results['redirect_ok']}")
print(f"  Redirects failed  : {results['redirect_fail']}")
print(f"  Posts trashed     : {results['trash_ok']}")
print(f"  Trash failed      : {results['trash_fail']}")
print(f"  Not found         : {results['not_found']}")
print()
print("Next steps:")
print("  1. If any redirects failed, manually add them in")
print("     WP Admin → Rank Math → Redirections")
print("  2. Fix robots.txt Crawl-delay: WP Admin → Rank Math → General →")
print("     Edit robots.txt → remove 'Crawl-delay: 10' line")
print("  3. Fix Cloudflare AhrefsBot block:")
print("     Cloudflare dashboard → Security → Bots → Known Bots → enable")
print("     (or add Firewall Rule: allow if user-agent contains 'AhrefsBot')")
