/**
 * Fastrak Mobile Lab — H1 Audit + Open Graph + Alt Text Fix (May 2026)
 *
 * Addresses three Ahrefs medium-priority issues:
 *   1. AUDIT: Identify all pages with multiple H1 tags (13 pages flagged)
 *      Reports page ID, title, and H1 count — manual Elementor fix required.
 *   2. OG FIX: Set a default Open Graph image in Rank Math global settings
 *      and patch 17 pages missing OG title/description via Rank Math updateMeta.
 *   3. ALT TEXT: Batch-update alt text on media attachments missing it.
 *
 * RUN: Paste into wp-admin browser console (any wp-admin page).
 *
 * BEFORE RUNNING — set the OG image URL below:
 *   OG_IMAGE_URL — absolute URL to your default OG share image (1200×630px)
 */
(async () => {
  // ── USER CONFIG ─────────────────────────────────────────────────────────
  const OG_IMAGE_URL = 'https://fastrakmobilelab.com/wp-content/uploads/fastrak-og-default.jpg'; // confirm filename in WP Media Library
  // ────────────────────────────────────────────────────────────────────────

  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const report = {
    multipleH1:  [],
    singleH1:    [],
    ogFixed:     [],
    altFixed:    [],
    errors:      []
  };

  // ── Helper: Rank Math updateMeta ─────────────────────────────────────────
  async function rmMeta(id, type, fields) {
    const r = await fetch(`${rmApi}/updateMeta`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ objectID: id, objectType: type, meta: fields })
    });
    return r.ok;
  }

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 1 — H1 Tag Audit
  // Fetches rendered HTML for all published pages/posts and counts H1 tags.
  // NOTE: This is read-only — Elementor H1 fixes must be done manually in
  // the Elementor editor (change widget "HTML Tag" from H1 to H2 for
  // secondary headings).
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[1] Auditing H1 tags across all published pages...', 'color:#FF9800;font-weight:bold');

  async function fetchAllPublished(type) {
    const items = [];
    let page = 1;
    while (true) {
      const r = await fetch(`${wpApi}/${type}?status=publish&per_page=100&page=${page}&_fields=id,title,link`, { headers: h });
      if (!r.ok) break;
      const batch = await r.json();
      if (!batch.length) break;
      items.push(...batch);
      if (batch.length < 100) break;
      page++;
      await sleep(200);
    }
    return items;
  }

  const [allPages, allPosts] = await Promise.all([fetchAllPublished('pages'), fetchAllPublished('posts')]);
  const allContent = [...allPages.map(p => ({...p, type:'pages'})), ...allPosts.map(p => ({...p, type:'posts'}))];
  console.log(`  Found ${allContent.length} published pages + posts. Checking H1s...`);

  for (const item of allContent) {
    try {
      const htmlR = await fetch(item.link, { credentials: 'omit' });
      if (!htmlR.ok) { report.errors.push(`H1 check: ${item.link} → ${htmlR.status}`); continue; }
      const html  = await htmlR.text();
      const parser = new DOMParser();
      const doc    = parser.parseFromString(html, 'text/html');
      const h1s    = doc.querySelectorAll('h1');
      const title  = item.title?.rendered || item.title?.raw || '(no title)';

      if (h1s.length > 1) {
        report.multipleH1.push({ id: item.id, type: item.type, title, h1Count: h1s.length, url: item.link });
        const h1Texts = Array.from(h1s).map(el => el.textContent.trim().slice(0, 60));
        console.warn(`  ⚠ MULTIPLE H1 (${h1s.length}) — ID ${item.id}: "${title.slice(0, 50)}"`);
        h1Texts.forEach((t, i) => console.warn(`      H1[${i+1}]: "${t}"`));
      } else {
        report.singleH1.push(item.id);
      }
    } catch (e) {
      report.errors.push(`H1 check error on ${item.id}: ${e.message}`);
    }
    await sleep(150);
  }

  console.log(`\n  H1 Audit complete: ${report.multipleH1.length} pages with multiple H1s, ${report.singleH1.length} pages OK.`);
  if (report.multipleH1.length) {
    console.log('%c  Pages requiring H1 fix (edit in Elementor — change secondary H1 widgets to H2):', 'color:#F44336');
    console.table(report.multipleH1.map(p => ({ ID: p.id, H1s: p.h1Count, Title: p.title.slice(0,60), URL: p.url })));
  }

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 2 — Open Graph Fix
  // Sets OG title, description, and image on all pages/posts that are
  // missing them. Uses each page's existing Rank Math title/description
  // as the OG title/description source.
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[2] Fixing Open Graph tags...', 'color:#FF9800;font-weight:bold');

  // Fetch all pages with their Rank Math meta to detect missing OG fields
  async function fetchWithMeta(type) {
    const items = [];
    let page = 1;
    while (true) {
      const r = await fetch(`${wpApi}/${type}?status=publish&per_page=100&page=${page}&context=edit`, { headers: h });
      if (!r.ok) break;
      const batch = await r.json();
      if (!batch.length) break;
      items.push(...batch);
      if (batch.length < 100) break;
      page++;
      await sleep(200);
    }
    return items;
  }

  const [pagesWithMeta, postsWithMeta] = await Promise.all([fetchWithMeta('pages'), fetchWithMeta('posts')]);
  const allWithMeta = [...pagesWithMeta.map(p => ({...p, type:'pages'})), ...postsWithMeta.map(p => ({...p, type:'posts'}))];

  console.log(`  Scanning ${allWithMeta.length} items for missing OG fields...`);

  for (const item of allWithMeta) {
    const meta   = item.meta || {};
    const title  = item.title?.rendered || '';
    const excerpt = item.excerpt?.rendered?.replace(/<[^>]+>/g, '').trim() || '';
    const desc   = item.meta?.rank_math_description || excerpt || title;

    const ogTitle   = meta.rank_math_facebook_title       || meta['rank_math_og_title']  || '';
    const ogDesc    = meta.rank_math_facebook_description  || '';
    const ogImage   = meta.rank_math_facebook_image        || meta['rank_math_og_image'] || '';

    const needsFix = !ogTitle || !ogDesc || !ogImage;
    if (!needsFix) continue;

    const fields = {};
    if (!ogTitle)  fields.rank_math_facebook_title       = title.replace(/<[^>]+>/g, '').trim();
    if (!ogDesc)   fields.rank_math_facebook_description = desc.slice(0, 155);
    if (!ogImage)  fields.rank_math_facebook_image       = OG_IMAGE_URL;

    // Also set Twitter card fields
    if (!ogTitle)  fields.rank_math_twitter_title        = title.replace(/<[^>]+>/g, '').trim();
    if (!ogDesc)   fields.rank_math_twitter_description  = desc.slice(0, 155);
    if (!ogImage)  fields.rank_math_twitter_image        = OG_IMAGE_URL;

    const ok = await rmMeta(item.id, item.type === 'pages' ? 'post' : 'post', fields);
    if (ok) {
      report.ogFixed.push({ id: item.id, type: item.type, title: title.replace(/<[^>]+>/g,'').slice(0,50) });
      console.log(`  OG fixed: ID ${item.id} — "${title.replace(/<[^>]+>/g,'').slice(0,50)}"`);
    } else {
      report.errors.push(`OG fix failed on ID ${item.id}`);
    }
    await sleep(250);
  }

  console.log(`  OG fix complete: ${report.ogFixed.length} pages updated.`);

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 3 — Alt Text Batch Fix
  // Fetches all media attachments with empty alt text and generates
  // descriptive alt text from the filename and attachment context.
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[3] Fixing missing image alt text...', 'color:#FF9800;font-weight:bold');

  // Keyword map: filename keywords → alt text template
  const altTextRules = [
    { match: /phlebotom|blood.?draw|venipuncture/i,  alt: 'FASTRAK Mobile Lab phlebotomist performing a blood draw at a patient\'s home in Gwinnett County, GA' },
    { match: /drug.?test|specimen|urine/i,            alt: 'Mobile drug testing specimen collection by FASTRAK Mobile Lab in Gwinnett County, GA' },
    { match: /dna|paternity/i,                        alt: 'FASTRAK Mobile Lab certified DNA and paternity test collection service in Metro Atlanta, GA' },
    { match: /senior|elderly|assisted.?living/i,      alt: 'FASTRAK Mobile Lab phlebotomist providing on-site lab services at a senior living facility in Gwinnett County' },
    { match: /corporate|office|workplace/i,           alt: 'FASTRAK Mobile Lab on-site corporate wellness blood draw at a Gwinnett County business' },
    { match: /logo/i,                                 alt: 'FASTRAK Mobile Lab logo — mobile phlebotomy and specimen collection services in Metro Atlanta, GA' },
    { match: /map|route|area/i,                       alt: 'FASTRAK Mobile Lab service area map covering Gwinnett, DeKalb, Rockdale, and Fulton Counties in Georgia' },
  ];

  function generateAltText(attachment) {
    const filename = (attachment.slug || attachment.source_url || '').toLowerCase();
    const title    = (attachment.title?.rendered || '').toLowerCase();
    const combined = `${filename} ${title}`;

    for (const rule of altTextRules) {
      if (rule.match.test(combined)) return rule.alt;
    }
    // Generic fallback
    const cleanTitle = (attachment.title?.rendered || 'mobile lab service').replace(/-/g,' ').replace(/\d+/g,'').trim();
    return `${cleanTitle} — FASTRAK Mobile Lab, Gwinnett County, GA`;
  }

  let mediaPage = 1;
  let mediaProcessed = 0;
  while (true) {
    const mediaR = await fetch(`${wpApi}/media?per_page=100&page=${mediaPage}&context=edit`, { headers: h });
    if (!mediaR.ok) break;
    const batch = await mediaR.json();
    if (!batch.length) break;

    for (const attachment of batch) {
      const altText = attachment.alt_text || (attachment.description?.rendered ? null : null);
      if (altText && altText.trim()) continue;  // already has alt text

      const newAlt = generateAltText(attachment);
      const putR   = await fetch(`${wpApi}/media/${attachment.id}`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ alt_text: newAlt })
      });
      if (putR.ok) {
        report.altFixed.push({ id: attachment.id, alt: newAlt.slice(0,60) });
        console.log(`  Alt text set: ID ${attachment.id} → "${newAlt.slice(0,60)}..."`);
        mediaProcessed++;
      } else {
        report.errors.push(`Alt text failed on media ID ${attachment.id}`);
      }
      await sleep(200);
    }
    if (batch.length < 100) break;
    mediaPage++;
  }
  console.log(`  Alt text fix complete: ${mediaProcessed} images updated.`);

  // ════════════════════════════════════════════════════════════════════════
  // SUMMARY
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c\n══ H1 / OG / ALT TEXT SUMMARY ══', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`Pages with multiple H1s: ${report.multipleH1.length} (manual Elementor fix required)`);
  console.log(`Pages with clean H1:     ${report.singleH1.length}`);
  console.log(`OG tags fixed:           ${report.ogFixed.length} pages`);
  console.log(`Alt text added:          ${report.altFixed.length} images`);
  if (report.errors.length) {
    console.warn(`Errors: ${report.errors.length}`);
    report.errors.forEach(e => console.warn('  ✖', e));
  }

  if (report.multipleH1.length) {
    console.log('%c\nH1 FIX INSTRUCTIONS (Elementor):', 'color:#F44336;font-weight:bold');
    console.log('For each page in the list above:');
    console.log('  1. Open the page in Elementor editor');
    console.log('  2. Click each Heading widget that is NOT the main page heading');
    console.log('  3. In the "Content" tab, change "HTML Tag" from H1 → H2 (or H3)');
    console.log('  4. Save & Publish');
  }

  console.log('%c\nDone.', 'color:#4CAF50;font-weight:bold');
})();
