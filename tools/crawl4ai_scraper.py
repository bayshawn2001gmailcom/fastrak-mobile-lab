#!/usr/bin/env python3
"""
Crawl4AI Scraper — Fastrak Mobile Lab SEO utility.

Primary scraper for SEO research tasks: competitor analysis, location content,
SERP research, live page checks. Tries Crawl4AI first (free, local browser),
falls back to Firecrawl API automatically if the page blocks headless browsers.

Usage (CLI):
  python tools/crawl4ai_scraper.py <url>
  python tools/crawl4ai_scraper.py <url> --query "mobile phlebotomy Lawrenceville"
  python tools/crawl4ai_scraper.py --competitors           # scrape all tracked competitors
  python tools/crawl4ai_scraper.py --location "Snellville" # research a city page

Import from other tools:
  from tools.crawl4ai_scraper import scrape, scrape_many, research_competitor, research_location
"""
import asyncio
import argparse
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Force UTF-8 on Windows — crawl4ai logs contain Unicode arrows/symbols that
# break cp1252 terminals. Must happen before any crawl4ai import.
os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
FIRECRAWL_HEADERS = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}

# Competitor domains to scrape when --competitors flag is used
COMPETITORS = [
    "https://mobiphlebotomy.com",
    "https://atlantamobilelab.com",
    "https://homephleb.com",
    "https://mobilemediq.com",
]


# ---------------------------------------------------------------------------
# Firecrawl fallback (plain HTTP — no browser, works anywhere)
# ---------------------------------------------------------------------------

def _firecrawl_scrape(url: str) -> str:
    if not FIRECRAWL_API_KEY:
        return ""
    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v1/scrape",
            json={"url": url, "formats": ["markdown"]},
            headers=FIRECRAWL_HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return (data.get("data") or {}).get("markdown", "") or data.get("markdown", "")
    except Exception as e:
        print(f"  [firecrawl] failed for {url}: {e}", file=sys.stderr)
        return ""


# ---------------------------------------------------------------------------
# Crawl4AI (primary — free, local Playwright browser)
# ---------------------------------------------------------------------------

async def _crawl4ai_scrape(url: str, query: str = "") -> str:
    try:
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
        from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

        content_filter = (
            BM25ContentFilter(user_query=query) if query
            else PruningContentFilter()
        )
        config = CrawlerRunConfig(
            markdown_generator=DefaultMarkdownGenerator(content_filter=content_filter)
        )
        async with AsyncWebCrawler() as crawler:
            results = await crawler.arun(url=url, config=config)
        r = results[0] if isinstance(results, list) else results
        if r.success:
            return r.markdown.fit_markdown or r.markdown.raw_markdown or ""
        return ""
    except Exception as e:
        print(f"  [crawl4ai] error for {url}: {e}", file=sys.stderr)
        return ""


async def _crawl4ai_scrape_many(urls: list[str], query: str = "") -> dict[str, str]:
    try:
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
        from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

        content_filter = (
            BM25ContentFilter(user_query=query) if query
            else PruningContentFilter()
        )
        config = CrawlerRunConfig(
            markdown_generator=DefaultMarkdownGenerator(content_filter=content_filter)
        )
        async with AsyncWebCrawler() as crawler:
            results = await crawler.arun_many(urls=urls, config=config)
        return {
            r.url: (r.markdown.fit_markdown or r.markdown.raw_markdown or "")
            for r in results if r.success
        }
    except Exception as e:
        print(f"  [crawl4ai] batch error: {e}", file=sys.stderr)
        return {}


# ---------------------------------------------------------------------------
# Public API — Crawl4AI with automatic Firecrawl fallback
# ---------------------------------------------------------------------------

def scrape(url: str, query: str = "") -> str:
    """
    Scrape a URL and return clean markdown.
    Tries Crawl4AI first; falls back to Firecrawl if the result is empty
    (e.g. the site blocked the headless browser).
    """
    result = asyncio.run(_crawl4ai_scrape(url, query=query))
    if result and len(result.strip()) > 200:
        return result

    print(f"  [scraper] crawl4ai returned thin result for {url}, trying Firecrawl...", file=sys.stderr)
    return _firecrawl_scrape(url)


def scrape_many(urls: list[str], query: str = "") -> dict[str, str]:
    """
    Scrape multiple URLs in parallel. Returns {url: markdown}.
    Falls back per-URL to Firecrawl for any that return thin/empty content.
    """
    results = asyncio.run(_crawl4ai_scrape_many(urls, query=query))

    for url in urls:
        content = results.get(url, "")
        if not content or len(content.strip()) < 200:
            print(f"  [scraper] falling back to Firecrawl for {url}", file=sys.stderr)
            fb = _firecrawl_scrape(url)
            if fb:
                results[url] = fb

    return results


# ---------------------------------------------------------------------------
# SEO-specific helpers
# ---------------------------------------------------------------------------

def research_competitor(domain_or_url: str) -> str:
    """
    Scrape a competitor's homepage (or any URL) and return clean markdown.
    Useful for: understanding their content structure, H1s, services listed,
    city coverage, CTAs, and schema patterns.
    """
    url = domain_or_url if domain_or_url.startswith("http") else f"https://{domain_or_url}"
    print(f"  Researching competitor: {url}", file=sys.stderr)
    return scrape(url, query="mobile phlebotomy services locations pricing")


def research_location(city: str, service: str = "mobile phlebotomy") -> str:
    """
    Gather content about a city to inform a location page.
    Scrapes top Google results context via a BM25-filtered crawl of relevant pages.
    Returns combined markdown useful for Gemini to write a location page.
    """
    # Scrape our existing city page if it exists, plus a few reference sources
    sources = [
        f"https://fastrakmobilelab.com/{city.lower().replace(' ', '-')}-mobile-phlebotomy/",
        f"https://fastrakmobilelab.com/service-area/",
    ]
    results = scrape_many(sources, query=f"{service} {city} Georgia")
    combined = []
    for url, md in results.items():
        if md.strip():
            combined.append(f"=== {url} ===\n{md[:2500]}")
    return "\n\n".join(combined)


def scrape_competitors_report() -> dict[str, str]:
    """Scrape all tracked competitors and return {url: markdown}."""
    print("  Scraping all tracked competitors...", file=sys.stderr)
    return scrape_many(COMPETITORS, query="mobile phlebotomy services pricing locations")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Crawl4AI scraper with Firecrawl fallback")
    parser.add_argument("url", nargs="?", help="URL to scrape")
    parser.add_argument("--query", default="", help="BM25 filter query for focused content")
    parser.add_argument("--competitors", action="store_true", help="Scrape all tracked competitors")
    parser.add_argument("--location", metavar="CITY", help="Research a city for a location page")
    parser.add_argument("--limit", type=int, default=0, help="Truncate output to N characters")
    args = parser.parse_args()

    if args.competitors:
        results = scrape_competitors_report()
        for url, md in results.items():
            print(f"\n{'='*60}\n{url}\n{'='*60}")
            print(md[:3000] if args.limit == 0 else md[:args.limit])
        return

    if args.location:
        md = research_location(args.location)
        print(md[:args.limit] if args.limit else md)
        return

    if not args.url:
        parser.error("Provide a URL or use --competitors / --location")

    result = scrape(args.url, query=args.query)
    print(result[:args.limit] if args.limit else result)


if __name__ == "__main__":
    main()
