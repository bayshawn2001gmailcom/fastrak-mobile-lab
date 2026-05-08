# Workflow: SEO Keyword Research & Competitor Analysis

## Objective
Identify high-value keywords for fastrakmobilelab.com, analyze competitor rankings, and surface opportunities to outrank them in local and national search.

## Inputs Required
- Target topic or service (e.g., "mobile phlebotomy Atlanta", "in-home blood draw")
- Target location(s) (e.g., city, metro area, state)
- Optional: specific competitor domain(s) to analyze

## Tools to Use
- **Ahrefs MCP** (in-session): keyword discovery, competitor analysis, SERP overview
- `tools/wp_get_pages.py`: pull existing published pages/posts so we don't duplicate
- `tools/keyword_report.py`: format and save research output to `.tmp/`

## Steps

### 1. Discover Seed Keywords
Use Ahrefs MCP `keywords-explorer-overview` with the target topic + location.
- Look for keywords with KD (keyword difficulty) under 30 and volume > 50/mo
- Note any local intent keywords (contain city, "near me", "in-home", "mobile")

### 2. Expand with Related + Matching Terms
Run `keywords-explorer-related-terms` and `keywords-explorer-matching-terms` on the best seed keywords.
- Filter for informational and transactional intent separately
- Cluster related terms into topic groups (one group = one potential page)

### 3. Analyze Competitor Rankings
For each competitor domain (start with top 3 SERP results):
- Run `site-explorer-organic-keywords` to see what they rank for
- Run `site-explorer-top-pages` to find their highest-traffic pages
- Note gaps: keywords competitors rank for that fastrakmobilelab.com does not

### 4. SERP Snapshot
Run `serp-overview` on the top target keyword.
- Record: who's ranking, their DR, estimated traffic, content type (local pack, blog, service page)
- Identify: is the #1 result a national brand or a local competitor? Local is more beatable.

### 5. Save Output
Run `tools/keyword_report.py` with the collected data.
- Output: `.tmp/keyword_report_YYYY-MM-DD.md` with ranked opportunities table
- Format: keyword | volume | KD | intent | current fastrakmobilelab rank | competitor ranking | recommended action

## Expected Output
A prioritized keyword opportunity list with:
- Quick wins (low KD, existing page just needs optimization)
- New page targets (no existing page, clear search demand)
- Competitor gap keywords (they rank, we don't)

## Handoff
Feed this output into `workflows/seo_content_creation.md` to draft and publish the target page.

## Edge Cases
- If Ahrefs returns no data for a keyword: try broader seed terms, then check Google Search Console data via `gsc-keywords` tool
- If fastrakmobilelab.com has no ranking data in Ahrefs: the site may be too new — use GSC data as primary source and Ahrefs for competitor research only
- If KD > 50 for all relevant terms: focus on local modifiers (city + service) which tend to have lower competition
