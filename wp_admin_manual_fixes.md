# WordPress Admin Manual Fixes — May 2026
Required for issues that can't be resolved via REST API alone.

---

## Fix 1: Noindex Duplicate Posts → Create 301 Redirects (16 pages in sitemap)

**Problem:** 15–16 posts are set to noindex + canonical but are still in the XML sitemap.
Google sees noindex pages in sitemap as a conflicting signal = Error in Ahrefs.

**Steps:**
1. Go to **Rank Math → Redirections → Add New**
2. Create a **301** redirect for each post below:

| Post Slug (Source URL) | Redirect To (Destination) |
|---|---|
| `/the-difference-between-home-dna-kits-and-legal-paternity-tests-2/` | `/the-difference-between-home-dna-kits-and-legal-paternity-tests/` |
| `/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know-2/` | `/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know/` |
| Any slug ending in `-2`, `-3`, `-4` | → to the slug without the number suffix |

3. After creating 301s, go to **Posts → All Posts**
4. Filter by **Trashed** — permanently delete the duplicate posts
5. Go to **Rank Math → Sitemap → Clear Sitemap Cache**

**Result:** Posts are 301-redirected + removed from sitemap → Ahrefs error count drops by 16.

---

## Fix 2: 3XX Redirect in Sitemap (1 page)

**Problem:** One URL in the sitemap.xml itself is a redirect (not the final destination URL).

**Steps:**
1. Go to `https://fastrakmobilelab.com/sitemap_index.xml` in browser
2. Click through each sitemap file to find the redirect URL
3. Common culprit: homepage listed as `http://` (redirects to `https://`)
4. Go to **Rank Math → Sitemap Settings → Exclude URLs** and add the redirect URL
5. OR: Find the Elementor/Rank Math setting generating that URL and fix the source

---

## Fix 3: Blog Pagination Duplicate Titles

**Problem:** `/blog/page/2/` through `/blog/page/10/` show the same title as `/blog/`.

**Steps:**
1. Go to **Rank Math → Titles & Meta → Posts**
2. Scroll to **Pagination**
3. Set **Noindex Paginated Pages** → toggle ON
4. Save changes

---

## Fix 4: Homepage /services/ Navigation Link (Redirect)

**Problem:** Homepage still has `href="/services/"` which is a redirect.
Final destination: `/mobile-phlebotomy-services-atlanta/`

**Steps:**
1. Go to **Pages → Homepage → Edit with Elementor**
2. Find the navigation or hero section button linking to `/services/`
3. Change URL to `/mobile-phlebotomy-services-atlanta/`
4. Save + Publish

---

## Fix 5: Page Speed (15 Slow Pages)

**Steps:**
1. Install **ShortPixel** plugin → Compress all images in Media Library (lossy, 80% quality)
2. Install **WP Rocket** (or enable LiteSpeed Cache if on LiteSpeed server)
   - Enable: Page caching, Browser caching, GZIP compression
   - Defer: Non-critical JS (Elementor, Google Fonts)
3. Verify at: `https://pagespeed.web.dev/` — target 70+ mobile score

---

## Fix 6: Sitemap Homepage Duplicate

**Problem:** Rank Math outputs the homepage (`/`) twice — once as front-page, once as page ID 23.

**Steps:**
1. Go to **Rank Math → Sitemap → Page Sitemap**
2. Find Page ID 23 in the exclude list field
3. Add `23` to excluded IDs → Save
4. Regenerate sitemap cache

---

## After All Manual Fixes

1. Go to **Google Search Console → Sitemaps**
2. Submit: `https://fastrakmobilelab.com/sitemap_index.xml`
3. Click **Request Indexing** on the top 5 city pages:
   - `/mobile-phlebotomy-gwinnett-county-ga/`
   - `/mobile-phlebotomy-snellville-ga/`
   - `/mobile-phlebotomy-lawrenceville-ga/`
   - `/mobile-drug-testing-gwinnett-county-ga/`
   - `/dna-testing-gwinnett-county-ga/`
4. Clear any CDN/page cache (Cloudflare, WP Rocket) so Google crawls fresh content
