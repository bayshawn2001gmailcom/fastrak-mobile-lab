# Workflow: Competitor Rank Monitoring

## Objective
Track weekly ranking changes for fastrakmobilelab.com and key competitors across 10 target keywords. Surface improvements and threats automatically so we know exactly when things move.

## Inputs Required
- `AHREFS_API_KEY` in `~/.env` (Ahrefs API v3, standard plan or higher)
- Optional: update `COMPETITORS` list in `tools/competitor_tracker.py` as you discover ranking pages

## Tools to Use
- `tools/competitor_tracker.py` — weekly snapshot + diff

## Steps

### Automated (runs via GitHub Actions every Sunday)
The `seo_weekly.yml` workflow runs `competitor_tracker.py` automatically.
Check `seo_reports/competitor_delta_YYYY-MM-DD.md` after each Sunday run.

### Manual Run (on demand)
```
python tools/competitor_tracker.py
```
Output goes to `.tmp/competitor_delta_YYYY-MM-DD.md`.

### Diff only (no API call)
If you already have today's snapshot and just want the diff report:
```
python tools/competitor_tracker.py --diff
```

## Reading the Report

**Our Improvements This Week:** Keywords where our position went up. These pages are responding to recent changes — note what was changed and keep doing it.

**Competitor Threats (gained 3+ positions):** If a competitor jumped 3+ spots on a key keyword, they likely published new content or got new backlinks. Investigate their site via Ahrefs MCP to see what changed.

**Position table:** Full grid of all tracked keywords × all tracked domains. Any position under 10 is page 1 — that's where we want to be.

## Adding Competitors
When you discover a new site ranking for target keywords, add it to `tools/competitor_tracker.py`:
```python
COMPETITORS = [
    "mobiphlebotomy.com",
    "atlantamobilelab.com",
    # add here
    "newcompetitor.com",
]
```

## Adding Keywords
When keyword research surfaces new targets, add to `TRACKED_KEYWORDS` in `tools/competitor_tracker.py`.

## Without Ahrefs API Key
If `AHREFS_API_KEY` is not set, the tool generates an empty snapshot structure without making API calls. The Ahrefs MCP (available in Claude sessions) can be used for manual competitor lookups in the meantime.

## Edge Cases
- If a competitor domain returns no data: they may be too small for Ahrefs index. Try a HEAD request to verify the domain is live.
- If our domain returns no data: the site may not have enough backlinks/traffic to appear in Ahrefs keyword data yet — use GSC data as the primary ranking source until DR improves.
