# FASTRAK Mobile Lab — Ahrefs SEO Analysis
**Date:** April 15, 2026  
**Source:** Ahrefs Free (Site Audit + Site Explorer)  
**Health Score:** 87/100 (Good — but fixable issues are holding it back)

---

## Domain Authority Snapshot

| Metric | Value | What It Means |
|--------|-------|---------------|
| Domain Rating (DR) | **0.6** | Virtually no backlink authority — the #1 growth blocker |
| URL Rating (UR) | 4.5 | Weak page-level authority |
| Ahrefs Rank | 59,560,943 | Very early stage — expected for a new/small local business site |
| Organic Positions | 22 | Ranking for 22 keywords — solid start given the DR |
| Perplexity AI Citation | **1 page** | Site is being cited by Perplexity AI — early AI visibility |

**Bottom line on DR:** With a DR of 0.6, the site has almost no link authority. This is the single biggest reason pages won't rank competitively for high-volume keywords, regardless of how good the on-page SEO is. Link building is the highest-leverage activity right now.

---

## Critical Issues (Fix First)

### 1. 33 Pages Returning 404 Errors — 17.6% of Crawled Pages
Ahrefs found **33 pages returning 404 Not Found** — nearly 1 in 5 crawled URLs is broken. This is a serious crawl budget waste and a signal to Google that the site is poorly maintained.

**Action:** Go to Ahrefs Site Audit → Internal Pages → filter by 404 status. Export the list. For each broken URL:
- If it was a real page that got deleted or moved, set up a 301 redirect to the correct URL
- If it was never a real page, block it in robots.txt or return a proper 410 Gone response
- Check if any internal links point to these 404s and update them

### 2. Multiple Title Tags on 20 Pages
Twenty pages have **two title tags** — meaning WordPress/Elementor is outputting one and Rank Math is outputting another. Google picks one unpredictably, and it's often not the optimized one.

**Root cause:** The Elementor page builder injects a title tag when the "Document Title" is set inside Elementor. Rank Math also outputs one. They conflict.

**Action:** In WordPress admin → Settings → Reading, confirm the SEO plugin (Rank Math) controls the title. In Elementor's page settings, check that the "Document Title" field is blank. Alternatively, install the "Disable Elementor Title" snippet. This affects 20 pages — high priority.

### 3. Multiple Meta Description Tags on 20 Pages
Same root cause as the title tag issue above — Elementor and Rank Math are both outputting meta descriptions on 20 pages.

**Action:** Same fix as above. Once the Elementor/Rank Math conflict is resolved, both issues resolve simultaneously.

### 4. Multiple H1 Tags on 13 Pages
Thirteen pages have more than one H1 tag. This dilutes keyword signals and confuses Google about the page's primary topic.

**Action:** Audit each page in Elementor. Ensure only one H1 exists per page — this should be the main heading at the top. All other headings should be H2 or H3.

---

## High-Priority Issues

### 5. 50 Orphan Pages (No Incoming Internal Links)
Fifty pages have **zero internal links** pointing to them. Google discovers and ranks pages partly through internal link equity. Pages with no internal links are effectively invisible to crawlers and rank poorly.

**Our new city pages (Lawrenceville, Norcross, Tucker, Conyers, Drug Testing, DNA Testing) are almost certainly in this list.** They were just published and have no incoming links yet.

**Action — Two steps:**
1. Add a "Service Areas" or "Cities We Serve" section to the Gwinnett County hub page linking to all city pages
2. Add a navigation dropdown or footer links covering all city pages across the site
3. Add contextual inline links from related blog posts to the city pages (e.g., the Duluth corporate wellness blog post should link to `/mobile-phlebotomy-duluth-ga/`)

### 6. 63 Pages with Title Tags That Are Too Long
Sixty-three pages have titles exceeding ~60 characters. Google truncates these in search results, cutting off the keyword-rich tail and reducing CTR.

**Action:** Run the page explorer in Ahrefs Site Audit → Content → filter by "Title too long." Export the list. For each page, trim the title to under 60 characters while keeping the primary keyword and brand name. The format "Keyword | FASTRAK Mobile Lab" usually fits cleanly.

### 7. 129 Pages with Internal Links Pointing to Redirect URLs
A massive number — 129 pages — have internal links pointing to URLs that redirect to another URL. Every redirect costs a small amount of link equity. At 129 instances, this is a meaningful drain.

**Action:** In Ahrefs Site Audit → Links → "Page has links to redirect," export the list. Find the redirect targets and update the internal links to point directly to the final destination URL. This is often caused by linking to `http://` URLs when the site has moved to `https://`, or linking to old URLs after a page was moved.

### 8. 3 Redirect Chains
Three URL paths require multiple redirects before reaching the final destination (A → B → C instead of A → C). Each hop loses equity and adds load time.

**Action:** Site Audit → Redirects → "Redirect chain." Collapse each chain to a single direct 301.

### 9. 10 Indexable Pages Not in Sitemap
Ten indexable pages are missing from the XML sitemap — Google may not discover or index them promptly. The newly created city pages are the likely culprits.

**Action:** In WordPress, go to Rank Math → Sitemap Settings and regenerate the sitemap. Then verify the new city page URLs appear at `fastrakmobilelab.com/sitemap_index.xml`. Submit the updated sitemap in Google Search Console.

### 10. 14 Structured Data Schema Errors
Fourteen pages have schema.org markup with validation errors. Broken schema prevents rich results (star ratings, FAQs, breadcrumbs) from appearing in search — a meaningful CTR loss.

**Action:** Run the URLs through Google's Rich Results Test tool (`search.google.com/test/rich-results`). Fix the specific errors Rank Math is generating. Common issues: missing required fields in LocalBusiness schema, invalid phone number format, or malformed MedicalBusiness schema.

---

## Medium-Priority Issues

### 11. 17 Pages with Missing Alt Text on Images
Seventeen image references have no alt text. This affects both accessibility (ADA compliance) and image search indexing.

**Action:** Site Audit → Images → "Missing alt text." For each image, add descriptive alt text in the WordPress media library that describes the image content and, where natural, includes a relevant keyword.

### 12. 17 Pages with Incomplete Open Graph Tags
Seventeen pages are missing Open Graph (OG) tags — title, description, and image. When these pages are shared on Facebook, LinkedIn, or other platforms, they'll show poorly formatted previews (or none at all), reducing click-through from social.

**Action:** In Rank Math, ensure each page has an OG image set. The Rank Math "Social" tab on each page allows custom OG title, description, and image. At minimum, set a default OG image in Rank Math → Titles & Meta → Global Settings.

### 13. 14 Pages with Meta Descriptions Too Long, 11 Too Short
- Too long (14 pages): Descriptions over ~155 characters get truncated in search results
- Too short (11 pages): Short descriptions may cause Google to auto-generate one from page content, which is often less optimized

**Action:** Audit via Site Audit → Content → filter by meta description length. Aim for 120–155 characters for every indexed page.

### 14. 15 Slow Pages
Fifteen pages are flagged as slow by Ahrefs' crawler. Page speed is a confirmed Google ranking factor — especially on mobile.

**Action:**
- Run the homepage and top city pages through Google PageSpeed Insights
- Compress all images (use a plugin like ShortPixel or Smush)
- Enable WordPress caching (WP Rocket or W3 Total Cache)
- Consider a CDN if not already in use
- Elementor adds JS/CSS weight — defer non-critical scripts in the plugin settings

### 15. 2 HTTP to HTTPS Redirects Still Active
Two URLs are still resolving as `http://` before redirecting to `https://`. These should have been resolved already.

**Action:** Check .htaccess or the hosting control panel to ensure a site-wide HTTP → HTTPS redirect is in place. Update any hardcoded `http://` internal links.

---

## Link Building — The #1 Priority

With a **DR of 0.6**, the site is essentially starting from zero in terms of link authority. Every competitor with even a modest DR of 15–30 will outrank FASTRAK for competitive terms even with inferior on-page SEO. The content strategy (blog posts, city pages) is the right foundation — but without links, it won't scale.

**Highest-leverage link building tactics for a local mobile lab:**

1. **Google Business Profile** — Fully optimized GBP is a de facto citation and link. Complete every field, add weekly photos, collect reviews. This is free and has outsized local impact.

2. **Healthcare and business directories** — Get listed on Healthgrades, Vitals, Zocdoc (if applicable), the Gwinnett Chamber of Commerce, local business directories, and any Gwinnett County health network directories. Each is a DR-passing backlink.

3. **Referring physician partnerships** — If physicians refer patients to FASTRAK, ask for a "mobile lab partner" link on their practice website. High-authority health domain links are extremely valuable.

4. **Senior living facility partnerships** — Facilities that use FASTRAK as their lab vendor should link to the site from their "Partners" or "Services" page. These are highly relevant local links.

5. **Local press / media mentions** — A story in the Gwinnett Daily Post, Patch, or a local health news outlet about mobile phlebotomy would generate a powerful backlink and brand awareness.

6. **HARO / PR outreach** — Respond to journalist queries about healthcare access, mobile health services, or workplace drug testing. A single mention in a mid-authority health publication can move DR meaningfully.

7. **Corporate client links** — Any employer who uses FASTRAK for drug testing or wellness programs should be asked to link to the site from their "Occupational Health Partners" page.

**Target:** Getting to DR 5–10 within 6 months is achievable with consistent outreach and would meaningfully improve ranking potential across the city pages.

---

## AI Search Visibility

| Platform | Citations |
|----------|-----------|
| Perplexity | **1 page cited** ✅ |
| AI Overview (Google) | 0 |
| ChatGPT | 0 |
| Gemini | 0 |
| Copilot | 0 |

The Perplexity citation is a positive early signal — the content is being picked up by at least one AI search engine. To build more AI citations, the city and service pages need to be more authoritative (more links pointing to them) and structured with clear, factual, direct answers to common questions (which they are). Adding an FAQ schema to each city page would help with AI Overview and PAA (People Also Ask) features.

---

## Recommended Action Priority

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 🔴 1 | Fix 33 x 404 pages → set up 301 redirects | Medium | High |
| 🔴 2 | Fix Multiple title/meta description tags (Elementor conflict) | Low | High |
| 🔴 3 | Build internal links to 50 orphan pages (esp. city pages) | Low | High |
| 🔴 4 | Submit updated sitemap with new city pages to GSC | Low | High |
| 🟡 5 | Fix 63 overly long title tags | Medium | Medium |
| 🟡 6 | Update 129 internal links pointing to redirect URLs | Medium | Medium |
| 🟡 7 | Fix 14 structured data schema errors | Low | Medium |
| 🟡 8 | Add alt text to 17 images | Low | Medium |
| 🟡 9 | Set default Open Graph image in Rank Math | Low | Medium |
| 🟢 10 | Fix 3 redirect chains | Low | Low |
| 🟢 11 | Fix slow pages (image compression, caching) | Medium | Medium |
| 🟢 12 | Audit and fix meta description lengths (14 too long, 11 too short) | Low | Low |
| 🔵 ONGOING | Link building (directories, GBP, physician/facility outreach) | High | Very High |

---

## What Can Be Fixed via REST API / WordPress Admin

Several of these issues can be addressed in future sessions directly:
- Add internal links from Gwinnett hub and service pages to all orphan city pages
- Submit sitemap via WP Rocket / Rank Math regeneration
- Fix OG image defaults in Rank Math settings
- Add alt text to images via WordPress media library
- Fix meta description lengths via Rank Math on individual pages

The 404 audit, title tag conflict, and structured data fixes require more investigation into specific URLs — export the lists from Ahrefs Site Audit first.
