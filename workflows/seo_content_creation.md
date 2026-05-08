# Workflow: SEO Content Creation & Publishing

## Objective
Take a target keyword from keyword research, create an SEO-optimized page or blog post, and publish it to fastrakmobilelab.com via the WordPress REST API.

## Inputs Required
- Target keyword (primary)
- Supporting keywords (from keyword research output)
- Content type: service page, blog post, FAQ page, location page
- Target URL slug (e.g., `/mobile-phlebotomy-atlanta`)

## Tools to Use
- `tools/wp_get_pages.py`: check if a page already exists at that slug
- `tools/content_generator.py`: generate SEO content via Gemini API
- `tools/wp_post.py`: create or update page/post via WordPress REST API
- `tools/wp_update_seo.py`: set Rank Math SEO title, meta description, focus keyword

## Steps

### 1. Pre-flight Check
Run `tools/wp_get_pages.py --slug <target-slug>` to confirm no existing page conflicts.
- If page exists: switch to update mode, pull current content before overwriting

### 2. Generate Content
Run `tools/content_generator.py` with:
- `--keyword`: primary keyword
- `--supporting`: comma-separated supporting keywords
- `--type`: page type (service | blog | location | faq)
- `--business`: "Fastrak Mobile Lab — mobile phlebotomy and specimen collection"

Content requirements the generator enforces:
- H1 contains primary keyword
- First 100 words contain primary keyword
- 2–4 H2 subheadings with supporting keywords
- Local trust signals: mention city/area served, licensed professionals, turnaround time
- CTA: "Book your mobile blood draw" with link placeholder
- Word count: 600–1000 for service pages, 800–1200 for blog posts
- No keyword stuffing — natural, helpful tone

### 3. Review Content
Agent reads the generated draft before publishing.
- Check: does it make medical/business sense?
- Check: are there factual claims that need verification?
- If off: regenerate with adjusted prompt or edit manually before proceeding

### 4. Publish to WordPress
Run `tools/wp_post.py` with:
- `--title`: page title
- `--content`: generated HTML content
- `--slug`: target URL slug
- `--status`: draft (default) or publish
- `--type`: page or post

Default to `--status draft` — publish manually after review unless explicitly told to auto-publish.

### 5. Set SEO Metadata
Run `tools/wp_update_seo.py` with the returned post ID:
- Focus keyword: primary keyword
- SEO title: `{Primary Keyword} | Fastrak Mobile Lab` (under 60 chars)
- Meta description: benefit-focused, contains keyword, 140–155 chars

## Expected Output
- Published (or draft) WordPress page/post
- Rank Math SEO fields populated
- `.tmp/content_log.md` entry: date | slug | keyword | post ID | status

## Handoff
After publishing, add to `SEO_Blog_Status_Tracker.md` in the fastrakmobilelab/ project folder.

## Edge Cases
- WordPress API 403 on specific endpoint: fall back to wp-admin UI (see parent CLAUDE.md for nonce method)
- Content too short after generation: re-run with `--min-words 800` flag
- Slug already taken by a different page: append city or qualifier to slug
