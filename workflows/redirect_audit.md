# Workflow: Redirect Chain Audit & Collapse

## Objective
Detect A→B→C redirect chains on fastrakmobilelab.com, collapse them to direct A→C redirects, and fix stale internal links in page/post body content.

## Inputs Required
None — tools pull live data from WordPress.

## Tools to Use
- `tools/redirect_fixer.py` — detects and collapses redirect chains via Rank Math API
- `tools/content_link_fixer.py` — finds and replaces stale slugs in body content

## Steps

### 1. Preview redirect chains
```
python tools/redirect_fixer.py --dry-run
```
Review output. Confirm each chain makes sense before applying.
Expected from May 2 audit: 3 chains to collapse.

### 2. Apply redirect chain fixes
```
python tools/redirect_fixer.py
```
Verify output shows chains collapsed with no errors.

### 3. Preview stale body links
```
python tools/content_link_fixer.py --dry-run
```
Review which pages still link to `/services/` or `/mobile-drug-dna-testing-atlanta/`.
Expected from May 2 audit: 5 pages affected.

### 4. Apply body link fixes
```
python tools/content_link_fixer.py
```

### 5. Verify blog public setting
```
python tools/wp_settings_patch.py --check
```
- If `blog_public` is 0 or blocked: run `python tools/wp_settings_patch.py --fix-public`
- Blog pagination noindex is a Rank Math setting — requires WP Admin UI:
  - WP Admin → Rank Math → Titles & Meta → Posts → Archive → set Noindex = Off

## Expected Output
- 0 redirect chains remaining
- 0 stale links in body content
- `blog_public=1` confirmed

## Edge Cases
- If Rank Math redirection API returns 404: the endpoint may not be enabled. Enable at Rank Math → Redirections → Settings → Enable Redirections module.
- If content patching fails on a specific page: edit that page manually in WP Admin → replace the stale href by hand.
- Redirect chains involving external domains: leave as-is, don't collapse.
