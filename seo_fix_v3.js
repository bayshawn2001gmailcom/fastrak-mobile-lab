/**
 * Fastrak Mobile Lab — SEO Fix Script v3 (May 2026)
 * Fixes confirmed from debug: updateMeta needs meta:{} wrapper.
 * Uses live page HTML to read actual meta descriptions (bypasses REST meta registration).
 * Paste entire script into wp-admin console and press Enter.
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const results = { fixed: [], skipped: [], errors: [] };

  // ── helpers ────────────────────────────────────────────────────────────────

  // Correct format: meta keys go inside meta:{} wrapper
  async function rmUpdate(objectID, objectType, metaFields) {
    const r = await fetch(`${rmApi}/updateMeta`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ objectID, objectType, meta: metaFields })
    });
    if (!r.ok) {
      const err = await r.text();
      console.error(`  ❌ updateMeta [${objectID}] ${r.status}:`, err.slice(0, 120));
    }
    return r.ok;
  }

  // Scrape a page's live HTML and extract the rendered meta description
  async function getLiveMetaDesc(url) {
    try {
      const r = await fetch(url, { cache: 'no-store' });
      const html = await r.text();
      const m = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*?)["']/i)
             || html.match(/<meta\s+content=["']([^"']*?)["']\s+name=["']description["']/i);
      return m ? m[1] : '';
    } catch(e) { return ''; }
  }

  function trimDesc(desc, max = 155) {
    if (desc.length <= max) return null;
    const t = desc.slice(0, max).replace(/\s+\S*$/, '').replace(/[.,;:–-]+$/, '');
    return t + '…';
  }

  async function getAllItems(type) {
    let all = [], page = 1;
    while (true) {
      const r = await fetch(
        `${wpApi}/${type}?per_page=100&page=${page}&status=publish&context=edit&_fields=id,slug,link`,
        { headers: h }
      );
      if (!r.ok) break;
      const batch = await r.json();
      if (!batch.length) break;
      all.push(...batch);
      if (batch.length < 100) break;
      page++;
    }
    return all;
  }

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // ── Step 1: Fetch all published pages + posts ──────────────────────────────
  console.log('%c[1] Fetching page + post list...', 'color:#4CAF50;font-weight:bold');
  const pages = await getAllItems('pages');
  const posts = await getAllItems('posts');
  const all   = [...pages, ...posts];
  console.log(`    ${pages.length} pages + ${posts.length} posts = ${all.length} total`);

  // ── Step 2: Scan live HTML for long meta descriptions ──────────────────────
  console.log('%c[2] Scanning live pages for meta descriptions > 155 chars...', 'color:#4CAF50;font-weight:bold');
  console.log('    (This reads each page — takes ~2 min for 127 pages)');

  let longFixed = 0;
  for (const item of all) {
    const url  = item.link;
    const desc = await getLiveMetaDesc(url);

    if (!desc) { await sleep(80); continue; }

    const trimmed = trimDesc(desc);
    if (trimmed) {
      const objType = pages.find(p => p.id === item.id) ? 'page' : 'post';
      const ok = await rmUpdate(item.id, objType, { rank_math_description: trimmed });
      if (ok) {
        console.log(`  ✅ TRIMMED [${item.id}] ${item.slug.slice(0,40)} ${desc.length}→${trimmed.length}`);
        results.fixed.push({ id: item.id, slug: item.slug, fix: 'meta-trimmed', from: desc.length, to: trimmed.length });
        longFixed++;
      }
    }
    await sleep(100);
  }
  console.log(`%c    Trimmed: ${longFixed}`, 'color:#4CAF50');

  // ── Step 3: Add missing meta descriptions to key pages ────────────────────
  console.log('%c[3] Adding missing meta descriptions to key pages...', 'color:#4CAF50;font-weight:bold');

  const autoMeta = {
    23:  { type: 'page', desc: 'Fastrak Mobile Lab provides professional mobile phlebotomy and specimen collection in Gwinnett County, GA. On-site blood draws at your home, office, or facility.' },
    564: { type: 'page', desc: 'Mobile phlebotomy and lab services across Atlanta and metro Georgia. On-site blood draws, drug testing, and DNA collection — no clinic visit required.' },
    306: { type: 'page', desc: 'Answers to your questions about mobile phlebotomy, on-site blood draws, and specimen collection from Fastrak Mobile Lab in Gwinnett County, GA.' },
    395: { type: 'page', desc: 'Mobile DNA testing and drug testing in Atlanta, GA. Chain-of-custody specimen collection for legal, employment, and personal use — Fastrak Mobile Lab.' },
    856: { type: 'page', desc: 'The Fastrak Mobile Lab blog covers mobile phlebotomy, specimen integrity, drug testing, and senior care lab services across Gwinnett County and metro Atlanta.' },
  };

  let missingFixed = 0;
  for (const [idStr, cfg] of Object.entries(autoMeta)) {
    const id  = parseInt(idStr);
    const url = all.find(x => x.id === id)?.link || `${origin}/?page_id=${id}`;

    // Read current live description first
    const current = await getLiveMetaDesc(url);
    if (current && current.length > 20) {
      console.log(`  ⏭  SKIP [${id}] already has: "${current.slice(0,60)}..."`);
      results.skipped.push({ id, reason: 'already-set' });
      await sleep(80);
      continue;
    }

    const ok = await rmUpdate(id, cfg.type, { rank_math_description: cfg.desc });
    if (ok) {
      console.log(`  ✅ SET [${id}] (${cfg.desc.length} chars)`);
      results.fixed.push({ id, fix: 'meta-added', chars: cfg.desc.length });
      missingFixed++;
    }
    await sleep(150);
  }
  console.log(`%c    Missing descriptions added: ${missingFixed}`, 'color:#4CAF50');

  // ── Step 4: Fix body-content redirect links ────────────────────────────────
  console.log('%c[4] Fixing body-content redirect links...', 'color:#4CAF50;font-weight:bold');

  const redirectFixes = {
    23:  { '/services/': '/mobile-phlebotomy-services-atlanta/' },
    395: { '/mobile-drug-dna-testing-atlanta/': '/mobile-dna-testing-atlanta/' },
  };

  for (const [idStr, replacements] of Object.entries(redirectFixes)) {
    const id = parseInt(idStr);
    const r  = await fetch(`${wpApi}/pages/${id}?context=edit`, { headers: h });
    if (!r.ok) { console.error(`  ❌ Cannot fetch page ${id}`); continue; }

    const data    = await r.json();
    let   content = data.content?.raw || '';
    let   changed = false;

    for (const [oldUrl, newUrl] of Object.entries(replacements)) {
      if (content.includes(oldUrl)) {
        content = content.split(oldUrl).join(newUrl);
        console.log(`  ✅ [${id}] "${oldUrl}" → "${newUrl}"`);
        changed = true;
      } else {
        console.log(`  ⏭  [${id}] "${oldUrl}" not found in content (may be in Elementor data)`);
      }
    }

    if (changed) {
      const patch = await fetch(`${wpApi}/pages/${id}`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ content })
      });
      if (patch.ok) results.fixed.push({ id, fix: 'redirect-link' });
      else console.error(`  ❌ [${id}] save failed (${patch.status})`);
    }
    await sleep(200);
  }

  // ── Step 5: Fix /services/ in Elementor data (homepage) ──────────────────
  console.log('%c[5] Fixing /services/ redirect in Elementor data (homepage)...', 'color:#4CAF50;font-weight:bold');

  const hpR = await fetch(`${wpApi}/pages/23?context=edit`, { headers: h });
  if (hpR.ok) {
    const hp = await hpR.json();
    const elData = hp.meta?._elementor_data || '';
    if (elData && elData.includes('"/services/"')) {
      const fixed = elData.split('"/services/"').join('"/mobile-phlebotomy-services-atlanta/"');
      const patch = await fetch(`${wpApi}/pages/23`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ meta: { _elementor_data: fixed } })
      });
      if (patch.ok) {
        console.log('  ✅ /services/ fixed in Elementor data');
        results.fixed.push({ id: 23, fix: 'elementor-services-link' });
      } else {
        console.log('  ⚠️  Elementor data update returned:', patch.status, '— may need manual fix in Elementor editor');
      }
    } else if (elData) {
      console.log('  ⏭  "/services/" not found in Elementor data — checking raw content link');
    } else {
      console.log('  ⚠️  _elementor_data not exposed via REST — fix manually in Elementor editor');
      console.log('      Edit homepage → find the nav/hero button → change URL to /mobile-phlebotomy-services-atlanta/');
    }
  }

  // ── Summary ───────────────────────────────────────────────────────────────
  console.log('%c\n══════════ RESULTS ══════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c✅ Fixed:   ${results.fixed.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c⏭  Skipped: ${results.skipped.length}`, 'color:#FF9800');
  console.log(`%c❌ Errors:  ${results.errors.length}`, 'color:#f44336');
  if (results.fixed.length)  console.table(results.fixed);
  if (results.errors.length) console.table(results.errors);
  console.log('%cDone. Paste results back to Claude.', 'color:#2196F3;font-weight:bold');
})();
