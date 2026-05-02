# FASTRAK SEO — Resume Session Prompt
**Paste this entire prompt into a fresh Claude Cowork session at ~10:30 AM EDT on April 15, 2026**

---

Continue SEO fixes for fastrakmobilelab.com WordPress site based on an Ahrefs audit completed earlier today. Work through all fixes below.

## WordPress Access
- Site: https://fastrakmobilelab.com
- Username: bayshawn2001
- Application Password: VxwB UUww AHWh 9ZX1 UWJA vH6b
- **Auth method:** Navigate to https://fastrakmobilelab.com/wp-admin/ in the Chrome browser MCP tab, get `wpApiSettings.nonce`, then use `"X-WP-Nonce"` header for all REST API fetch() calls. Basic auth gets blocked — always use the nonce method.

## Pages Already Published (do not recreate)
| Page | ID | URL |
|------|-----|-----|
| Snellville | 1248 | /mobile-phlebotomy-snellville-ga/ |
| Gwinnett County hub | 1249 | /mobile-phlebotomy-gwinnett-county-ga/ |
| Duluth | 1250 | /mobile-phlebotomy-duluth-ga/ |
| Lawrenceville | 1256 | /mobile-phlebotomy-lawrenceville-ga/ |
| Norcross | 1258 | /mobile-phlebotomy-norcross-ga/ |
| Tucker | 1260 | /mobile-phlebotomy-tucker-ga/ |
| Conyers | 1261 | /mobile-phlebotomy-conyers-ga/ |
| Drug Testing Gwinnett | 1262 | /mobile-drug-testing-gwinnett-county-ga/ |
| DNA Testing Gwinnett | 1263 | /dna-testing-gwinnett-county-ga/ |
| Services page | 564 | /mobile-phlebotomy-services-atlanta/ |
| Drug & DNA Testing | 395 | /mobile-dna-testing-atlanta/ |
| FAQ | 306 | /faq/ |
| Homepage | 23 | / |

---

## FIX 1 — Internal Links to Orphan City Pages (HIGHEST PRIORITY)

Ahrefs flagged 50 orphan pages with zero incoming internal links. Fix by appending content to 3 pages. To append: GET the page with `context=edit` to get current raw content, then POST with existing content + new content appended.

**A. Gwinnett County hub (ID 1249)** — Append at the bottom:
```
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Cities We Serve in Gwinnett County</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>FASTRAK Mobile Lab provides mobile phlebotomy, drug testing, and DNA collection services throughout Gwinnett County and surrounding areas. Explore our dedicated service pages for your city:</p>
<!-- /wp:paragraph -->
<!-- wp:list -->
<ul class="wp-block-list">
<li><a href="/mobile-phlebotomy-duluth-ga/">Mobile Phlebotomy in Duluth, GA</a></li>
<li><a href="/mobile-phlebotomy-lawrenceville-ga/">Mobile Phlebotomy in Lawrenceville, GA</a></li>
<li><a href="/mobile-phlebotomy-norcross-ga/">Mobile Phlebotomy in Norcross, GA</a></li>
<li><a href="/mobile-phlebotomy-snellville-ga/">Mobile Phlebotomy in Snellville, GA</a></li>
<li><a href="/mobile-phlebotomy-tucker-ga/">Mobile Phlebotomy in Tucker, GA</a></li>
<li><a href="/mobile-phlebotomy-conyers-ga/">Mobile Phlebotomy in Conyers, GA</a></li>
<li><a href="/mobile-drug-testing-gwinnett-county-ga/">Mobile Drug Testing — Gwinnett County</a></li>
<li><a href="/dna-testing-gwinnett-county-ga/">DNA Testing — Gwinnett County</a></li>
</ul>
<!-- /wp:list -->
```

**B. Services page (ID 564)** — Append the same "Cities We Serve" section as above.

**C. Drug & DNA Testing page (ID 395)** — Append:
```
<!-- wp:paragraph -->
<p>We also provide dedicated <a href="/mobile-drug-testing-gwinnett-county-ga/">mobile drug testing throughout Gwinnett County</a> and <a href="/dna-testing-gwinnett-county-ga/">DNA testing services in Gwinnett County</a> — with licensed collectors coming directly to your location.</p>
<!-- /wp:paragraph -->
```

---

## FIX 2 — Sitemap & Google Ping

1. Fetch https://fastrakmobilelab.com/sitemap_index.xml — verify new city pages are present
2. If missing, go to Rank Math → Sitemap in wp-admin and regenerate
3. Ping: https://www.google.com/ping?sitemap=https://fastrakmobilelab.com/sitemap_index.xml

---

## FIX 3 — Add FAQ Schema to City Pages

Append to Duluth (1250), Lawrenceville (1256), Norcross (1258), Tucker (1260), Conyers (1261). Substitute [City] and [County]:

- Duluth → Gwinnett County
- Lawrenceville → Gwinnett County  
- Norcross → Gwinnett County
- Tucker → DeKalb County
- Conyers → Rockdale County

```
<!-- wp:html -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do I book a mobile phlebotomy appointment in [City], GA?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Call (678) 562-5244 or book online at https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt. Same-day and next-day appointments are typically available in [City]."
      }
    },
    {
      "@type": "Question",
      "name": "Do you accept physician orders for blood draws in [City], GA?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. FASTRAK Mobile Lab works from physician requisitions for all standard and specialty lab panels. We collect your specimen and transport it to a certified reference lab for processing."
      }
    },
    {
      "@type": "Question",
      "name": "Is mobile phlebotomy covered by insurance in [City], GA?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coverage depends on your insurance plan and the tests ordered. We recommend verifying with your insurer prior to your appointment. FASTRAK can provide documentation to support reimbursement claims."
      }
    },
    {
      "@type": "Question",
      "name": "What areas of [City] do you serve?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "FASTRAK Mobile Lab serves all of [City] and the surrounding [County] area. Call (678) 562-5244 to confirm availability at your specific address."
      }
    }
  ]
}
</script>
<!-- /wp:html -->
```

---

## FIX 4 — Update SEO Tracker

Request directory access for C:\Users\baysh\fastrakmobilelab, then update SEO_Blog_Status_Tracker.md — append a section documenting all completed fixes with today's date (April 15, 2026).

---

## Manual Fixes (flag these for Shawn to do himself)
These require the Ahrefs export which only Shawn can access:
- 33 x 404 pages → need 301 redirects (export list from Ahrefs Site Audit → Internal Pages → 404 filter)
- Multiple title tags on 20 pages → Elementor/Rank Math conflict, fix in theme settings
- 63 title tags too long → trim each in Rank Math
- 129 internal links to redirect URLs → update to final destinations
- 14 structured data schema errors → validate at search.google.com/test/rich-results
- 17 images missing alt text → add in WordPress Media Library
- 15 slow pages → compress images, enable caching plugin
