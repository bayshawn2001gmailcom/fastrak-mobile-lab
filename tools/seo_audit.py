#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fastrak Mobile Lab — Weekly SEO Automation
Migrated from seo_auto.py (master branch) into WAT tools/ structure.
Run: python tools/seo_audit.py
Requires: pip install requests python-dotenv
Credentials: WP_USER, WP_APP_PASSWORD, WP_SITE in ~/.env or environment
"""
import os
import re
import time
import base64
import json
import requests
from datetime import date
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_DESC_LEN = 155
RATE_LIMIT_SLEEP = 0.1
# Reports go to repo root /seo_reports/, not inside tools/
REPORTS_DIR = Path(__file__).parent.parent / "seo_reports"
FALLBACK_DESC_TEMPLATE = (
    "{title} — Fastrak Mobile Lab provides certified mobile phlebotomy, "
    "drug testing, and DNA collection services in Gwinnett County and metro Atlanta, GA."
)
DUPLICATE_SLUG_RE = re.compile(r"^(.+)-(\d+)$")

WP_USER = os.getenv("WP_USER", "")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")
WP_SITE = os.getenv("WP_SITE", "").rstrip("/")

if not all([WP_USER, WP_APP_PASSWORD, WP_SITE]):
    raise SystemExit(
        "Missing credentials. Set WP_USER, WP_APP_PASSWORD, WP_SITE in ~/.env or environment."
    )

_token = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
AUTH_HEADERS = {"Authorization": f"Basic {_token}"}

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "FastrakSEOBot/1.0"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def wp_get(path, params=None):
    url = f"{WP_SITE}/wp-json/wp/v2/{path}"
    resp = SESSION.get(url, headers=AUTH_HEADERS, params=params, timeout=20)
    resp.raise_for_status()
    return resp


def wp_post(path, payload):
    url = f"{WP_SITE}/wp-json/wp/v2/{path}"
    resp = SESSION.post(url, headers={**AUTH_HEADERS, "Content-Type": "application/json"},
                        data=json.dumps(payload), timeout=20)
    resp.raise_for_status()
    return resp


def wp_delete(path):
    url = f"{WP_SITE}/wp-json/wp/v2/{path}"
    resp = SESSION.delete(url, headers=AUTH_HEADERS, timeout=20)
    resp.raise_for_status()
    return resp


def rankmath_post(endpoint, payload):
    url = f"{WP_SITE}/wp-json/rankmath/v1/{endpoint}"
    resp = SESSION.post(url, headers={**AUTH_HEADERS, "Content-Type": "application/json"},
                        data=json.dumps(payload), timeout=20)
    resp.raise_for_status()
    return resp


def fetch_all(resource, extra_params=None):
    items = []
    page = 1
    while True:
        params = {"status": "publish", "per_page": 100, "page": page,
                  "context": "edit", **(extra_params or {})}
        try:
            resp = wp_get(resource, params=params)
        except requests.HTTPError as exc:
            if exc.response.status_code == 400:
                break
            raise
        batch = resp.json()
        if not batch:
            break
        items.extend(batch)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
        time.sleep(RATE_LIMIT_SLEEP)
    return items


class MetaDescParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.descriptions = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "meta":
            attr_dict = dict(attrs)
            if attr_dict.get("name", "").lower() == "description":
                content = attr_dict.get("content", "")
                self.descriptions.append(content)


def fetch_live_descriptions(url):
    try:
        resp = SESSION.get(url, timeout=20)
        resp.raise_for_status()
        parser = MetaDescParser()
        parser.feed(resp.text)
        return parser.descriptions
    except Exception:
        return []


def trim_to_word_boundary(text, max_len):
    if len(text) <= max_len:
        return text
    cut = text[:max_len - 1].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "..."


def is_indexable(item):
    meta = item.get("meta", {}) or {}
    rank_robot = meta.get("rank_math_robots", [])
    if isinstance(rank_robot, list) and "noindex" in rank_robot:
        return False
    if isinstance(rank_robot, str) and "noindex" in rank_robot:
        return False
    return True


def get_post_url(item):
    return item.get("link") or item.get("guid", {}).get("rendered", "")


def log(prefix, msg):
    print(f"{prefix}  {msg}")


# ---------------------------------------------------------------------------
# Section 1: Meta Description Audit + Fix
# ---------------------------------------------------------------------------

def audit_meta_descriptions(pages, posts):
    log("[AUDIT]", "Starting meta description audit...")
    changes = []
    skipped = 0
    pages_fixed = 0
    posts_fixed = 0

    def process_item(item, obj_type):
        nonlocal pages_fixed, posts_fixed, skipped

        obj_id = item["id"]
        title = item.get("title", {}).get("rendered", "") or item.get("slug", "")
        url = get_post_url(item)

        if not url:
            skipped += 1
            return

        try:
            live_descs = fetch_live_descriptions(url)
            time.sleep(RATE_LIMIT_SLEEP)
        except Exception:
            skipped += 1
            return

        current_desc = live_descs[0] if live_descs else ""
        new_desc = None

        if current_desc and len(current_desc) > MAX_DESC_LEN:
            new_desc = trim_to_word_boundary(current_desc, MAX_DESC_LEN)
            reason = f"trimmed {len(current_desc)}->{len(new_desc)} chars"
        elif not current_desc and is_indexable(item):
            raw = FALLBACK_DESC_TEMPLATE.format(title=title)
            new_desc = trim_to_word_boundary(raw, MAX_DESC_LEN)
            reason = "generated (was missing)"

        if new_desc:
            saved = False
            for attempt in ("rankmath", "wp_rest"):
                try:
                    if attempt == "rankmath":
                        rankmath_post("updateMeta", {
                            "objectID": obj_id,
                            "objectType": obj_type,
                            "meta": {"rank_math_description": new_desc},
                        })
                    else:
                        endpoint = "pages" if obj_type == "page" else "posts"
                        wp_post(f"{endpoint}/{obj_id}",
                                {"meta": {"rank_math_description": new_desc}})
                    saved = True
                    break
                except Exception:
                    pass
            time.sleep(RATE_LIMIT_SLEEP)
            if saved:
                log("[OK]", f"[{obj_type} {obj_id}] {reason}")
                changes.append({
                    "type": "meta_desc_fix",
                    "obj_type": obj_type,
                    "id": obj_id,
                    "url": url,
                    "reason": reason,
                    "new_desc": new_desc,
                })
                if obj_type == "page":
                    pages_fixed += 1
                else:
                    posts_fixed += 1
            else:
                log("[SKIP]", f"[{obj_type} {obj_id}] updateMeta failed (both methods)")
                skipped += 1
        else:
            skipped += 1

    for item in pages:
        process_item(item, "page")

    for item in posts:
        process_item(item, "post")

    log("[DONE]", f"Meta desc: {pages_fixed} pages fixed, {posts_fixed} posts fixed, {skipped} skipped")
    return {"pages_fixed": pages_fixed, "posts_fixed": posts_fixed, "skipped": skipped,
            "changes": changes}


# ---------------------------------------------------------------------------
# Section 2: Duplicate Post Detection + Cleanup
# ---------------------------------------------------------------------------

def cleanup_duplicate_posts(posts):
    log("[AUDIT]", "Scanning for duplicate slugs...")
    redirects_created = 0
    posts_trashed = 0
    changes = []

    for item in posts:
        slug = item.get("slug", "")
        m = DUPLICATE_SLUG_RE.match(slug)
        if not m:
            continue

        canonical_slug = m.group(1)
        obj_id = item["id"]
        url = get_post_url(item)

        try:
            resp = wp_get("posts", {"slug": canonical_slug, "status": "publish"})
            canonical_results = resp.json()
            time.sleep(RATE_LIMIT_SLEEP)
        except Exception as exc:
            log("[WARN]", f"Slug lookup failed for '{canonical_slug}': {exc}")
            continue

        if canonical_results:
            canonical_url = get_post_url(canonical_results[0])
            try:
                rankmath_post("updateRedirection", {
                    "objectID": obj_id,
                    "objectType": "post",
                    "hasRedirect": True,
                    "redirectionUrl": canonical_url,
                    "redirectionType": "301",
                })
                time.sleep(RATE_LIMIT_SLEEP)
                log("[301]", f"Redirect: {url} -> {canonical_url}")
                redirects_created += 1
                changes.append({
                    "type": "redirect_created",
                    "id": obj_id,
                    "from": url,
                    "to": canonical_url,
                })
            except Exception as exc:
                log("[WARN]", f"Redirect creation failed for post {obj_id}: {exc}")

        try:
            wp_delete(f"posts/{obj_id}")
            time.sleep(RATE_LIMIT_SLEEP)
            log("[DEL]", f"Trashed duplicate post {obj_id} (slug: {slug})")
            posts_trashed += 1
            changes.append({
                "type": "post_trashed",
                "id": obj_id,
                "slug": slug,
                "had_canonical": bool(canonical_results),
            })
        except Exception as exc:
            log("[WARN]", f"Trash failed for post {obj_id}: {exc}")

    log("[DONE]", f"Duplicates: {redirects_created} redirects created, {posts_trashed} posts trashed")
    return {"redirects_created": redirects_created, "posts_trashed": posts_trashed,
            "changes": changes}


# ---------------------------------------------------------------------------
# Section 3: Duplicate Meta Description Detection (pages)
# ---------------------------------------------------------------------------

def fix_duplicate_meta_tags(pages):
    log("[AUDIT]", "Checking for duplicate <meta name=description> tags...")
    fixed = 0
    changes = []

    for item in pages:
        obj_id = item["id"]
        url = get_post_url(item)

        if not url:
            continue

        try:
            live_descs = fetch_live_descriptions(url)
            time.sleep(RATE_LIMIT_SLEEP)
        except Exception:
            continue

        if len(live_descs) <= 1:
            continue

        log("[WARN]", f"[page {obj_id}] {len(live_descs)} meta descriptions found: {url}")

        try:
            wp_post(f"pages/{obj_id}", {"excerpt": ""})
            time.sleep(RATE_LIMIT_SLEEP)
        except Exception as exc:
            log("[WARN]", f"[page {obj_id}] excerpt clear failed: {exc}")

        canonical_desc = live_descs[0]
        if len(canonical_desc) > MAX_DESC_LEN:
            canonical_desc = trim_to_word_boundary(canonical_desc, MAX_DESC_LEN)

        try:
            rankmath_post("updateMeta", {
                "objectID": obj_id,
                "objectType": "page",
                "meta": {"rank_math_description": canonical_desc},
            })
            time.sleep(RATE_LIMIT_SLEEP)
            log("[OK]", f"[page {obj_id}] deduped meta description")
            fixed += 1
            changes.append({
                "type": "duplicate_meta_fixed",
                "id": obj_id,
                "url": url,
                "count_found": len(live_descs),
                "kept": canonical_desc,
            })
        except Exception as exc:
            log("[WARN]", f"[page {obj_id}] updateMeta failed: {exc}")

    log("[DONE]", f"Duplicate meta tags: {fixed} pages fixed")
    return {"fixed": fixed, "changes": changes}


# ---------------------------------------------------------------------------
# Section 4: Sitemap Health Check
# ---------------------------------------------------------------------------

def check_sitemap_health():
    log("[AUDIT]", "Checking sitemap for redirects...")
    redirected_urls = []

    sitemap_candidates = [
        f"{WP_SITE}/sitemap_index.xml",
        f"{WP_SITE}/sitemap.xml",
    ]

    sitemap_content = None
    for candidate in sitemap_candidates:
        try:
            resp = SESSION.get(candidate, timeout=20)
            if resp.status_code == 200 and resp.content:
                sitemap_content = resp.text
                log("[OK]", f"Sitemap found: {candidate}")
                break
        except Exception:
            continue

    if not sitemap_content:
        log("[WARN]", "No sitemap found at expected locations")
        return {"urls_checked": 0, "redirected_urls": [], "sitemap_found": False}

    all_urls = re.findall(r"<loc>\s*(https?://[^\s<]+)\s*</loc>", sitemap_content)
    sub_sitemaps = [u for u in all_urls if u.endswith(".xml")]
    page_urls = [u for u in all_urls if not u.endswith(".xml")]

    for sub_url in sub_sitemaps:
        try:
            resp = SESSION.get(sub_url, timeout=20)
            if resp.status_code == 200:
                sub_urls = re.findall(r"<loc>\s*(https?://[^\s<]+)\s*</loc>", resp.text)
                page_urls.extend([u for u in sub_urls if not u.endswith(".xml")])
            time.sleep(RATE_LIMIT_SLEEP)
        except Exception:
            continue

    page_urls = list(dict.fromkeys(page_urls))
    log("[INFO]", f"Checking {len(page_urls)} URLs from sitemap...")

    for url in page_urls:
        try:
            resp = SESSION.head(url, timeout=15, allow_redirects=False)
            if 300 <= resp.status_code < 400:
                dest = resp.headers.get("Location", "unknown")
                redirected_urls.append({"url": url, "status": resp.status_code, "location": dest})
                log("[301]", f"[{resp.status_code}] {url} -> {dest}")
            time.sleep(RATE_LIMIT_SLEEP)
        except Exception as exc:
            log("[WARN]", f"HEAD request failed for {url}: {exc}")

    log("[DONE]", f"Sitemap: {len(page_urls)} URLs checked, {len(redirected_urls)} have redirects")
    return {
        "urls_checked": len(page_urls),
        "redirected_urls": redirected_urls,
        "sitemap_found": True,
    }


# ---------------------------------------------------------------------------
# Section 5: Markdown Report
# ---------------------------------------------------------------------------

def write_report(meta_results, dupe_results, dup_meta_results, sitemap_results):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    report_path = REPORTS_DIR / f"seo_report_{today}.md"

    lines = [
        f"# SEO Auto-Report -- {today}",
        "",
        "**Site:** https://fastrakmobilelab.com",
        f"**Generated by:** tools/seo_audit.py",
        "",
        "---",
        "",
        "## 1. Meta Description Audit",
        "",
        f"- Pages fixed: **{meta_results['pages_fixed']}**",
        f"- Posts fixed: **{meta_results['posts_fixed']}**",
        f"- Skipped: **{meta_results['skipped']}**",
        "",
    ]

    if meta_results["changes"]:
        lines.append("### Changes Made")
        lines.append("")
        for c in meta_results["changes"]:
            lines.append(
                f"- [{c['obj_type'].upper()} {c['id']}] {c['reason']}  \n"
                f"  URL: {c['url']}  \n"
                f"  New desc: _{c['new_desc']}_"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "## 2. Duplicate Post Cleanup",
        "",
        f"- 301 Redirects created: **{dupe_results['redirects_created']}**",
        f"- Posts trashed: **{dupe_results['posts_trashed']}**",
        "",
    ]

    if dupe_results["changes"]:
        lines.append("### Changes Made")
        lines.append("")
        for c in dupe_results["changes"]:
            if c["type"] == "redirect_created":
                lines.append(f"- Redirect: `{c['from']}` -> `{c['to']}`")
            elif c["type"] == "post_trashed":
                had = "with canonical" if c["had_canonical"] else "no canonical found"
                lines.append(f"- Trashed post {c['id']} (slug: `{c['slug']}`, {had})")
        lines.append("")

    lines += [
        "---",
        "",
        "## 3. Duplicate Meta Description Tags",
        "",
        f"- Pages with duplicate meta tags fixed: **{dup_meta_results['fixed']}**",
        "",
    ]

    if dup_meta_results["changes"]:
        lines.append("### Changes Made")
        lines.append("")
        for c in dup_meta_results["changes"]:
            lines.append(
                f"- [PAGE {c['id']}] Found {c['count_found']} meta tags  \n"
                f"  URL: {c['url']}  \n"
                f"  Kept: _{c['kept']}_"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "## 4. Sitemap Health Check",
        "",
        f"- Sitemap found: **{'Yes' if sitemap_results['sitemap_found'] else 'No'}**",
        f"- URLs checked: **{sitemap_results['urls_checked']}**",
        f"- URLs with redirects (3XX): **{len(sitemap_results['redirected_urls'])}**",
        "",
    ]

    if sitemap_results["redirected_urls"]:
        lines.append("### Manual Attention Required -- Redirected Sitemap URLs")
        lines.append("")
        for r in sitemap_results["redirected_urls"]:
            lines.append(f"- [{r['status']}] `{r['url']}` -> `{r['location']}`")
        lines.append("")

    lines += [
        "---",
        "",
        "## Summary",
        "",
        f"| Section | Metric | Count |",
        f"|---------|--------|-------|",
        f"| Meta Descriptions | Pages fixed | {meta_results['pages_fixed']} |",
        f"| Meta Descriptions | Posts fixed | {meta_results['posts_fixed']} |",
        f"| Duplicate Posts | Redirects created | {dupe_results['redirects_created']} |",
        f"| Duplicate Posts | Posts trashed | {dupe_results['posts_trashed']} |",
        f"| Duplicate Meta Tags | Pages fixed | {dup_meta_results['fixed']} |",
        f"| Sitemap | URLs checked | {sitemap_results['urls_checked']} |",
        f"| Sitemap | Redirected (needs fix) | {len(sitemap_results['redirected_urls'])} |",
        "",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    log("[REPORT]", f"Written: {report_path}")
    return report_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Fastrak Mobile Lab -- Weekly SEO Automation")
    print(f"  Site: {WP_SITE}")
    print(f"  Date: {date.today().isoformat()}")
    print("=" * 60)
    print()

    log("[FETCH]", "Fetching all published pages...")
    pages = fetch_all("pages")
    log("[FETCH]", f"Got {len(pages)} pages")

    log("[FETCH]", "Fetching all published posts...")
    posts = fetch_all("posts")
    log("[FETCH]", f"Got {len(posts)} posts")

    print()
    meta_results = audit_meta_descriptions(pages, posts)

    print()
    dupe_results = cleanup_duplicate_posts(posts)

    print()
    dup_meta_results = fix_duplicate_meta_tags(pages)

    print()
    sitemap_results = check_sitemap_health()

    print()
    report_path = write_report(meta_results, dupe_results, dup_meta_results, sitemap_results)

    print()
    print("=" * 60)
    print("  DONE")
    print(f"  Meta desc fixed:     pages={meta_results['pages_fixed']}  posts={meta_results['posts_fixed']}")
    print(f"  Duplicate posts:     redirects={dupe_results['redirects_created']}  trashed={dupe_results['posts_trashed']}")
    print(f"  Dup meta tags fixed: {dup_meta_results['fixed']}")
    print(f"  Sitemap redirects:   {len(sitemap_results['redirected_urls'])} (manual review needed)")
    print(f"  Report:              {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
