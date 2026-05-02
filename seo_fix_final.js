/**
 * Fastrak Mobile Lab — SEO Final Fix Script (May 2, 2026)
 * Handles all remaining Ahrefs errors/warnings:
 *   1. Create 301 redirects for 16 noindex duplicate posts
 *   2. Trash duplicate posts (removes them from sitemap)
 *   3. Find + fix 6 duplicate meta description tags
 *   4. Fix Elementor redirect links (/services/ etc.)
 *   5. Check sitemap for 3XX URL
 * Paste entire script into wp-admin browser console.
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));
  const log    = { created: [], trashed: [], dupeFixed: [], errors: [] };

  // ── Helper: Rank Math updateMeta ──────────────────────────────────────────
  async function rmMeta(id, type, fields) {
    const r = await fetch(`${rmApi}/updateMeta`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ objectID: id, objectType: type, meta: fields })
    });
    return r.ok;
  }

  // ── Helper: strip -2, -3 etc from slug to get canonical slug ─────────────
  function canonicalSlug(slug) {
    return slug.replace(/-\d+$/, '');
  }

  // ============================================================
  // SECTION 1: Test Rank Math updateRedirection format
  // ============================================================
  console.log('%c[1] Testing Rank Math updateRedirection endpoint...', 'color:#FF9800;font-weight:bold');

  // Try format A (most common Rank Math Pro format)
  const testRedir = await fetch(`${rmApi}/updateRedirection`, {
    method: 'POST', headers: h,
    body: JSON.stringify({
      id: 0,
      sources: [{ pattern: '/seo-test-do-not-use/', comparison: 'exact' }],
      destination: `${origin}/`,
      type: '301',
      status: 'active'
    })
  });
  const testRedirText = await testRedir.text();
  console.log('  updateRedirection format A status:', testRedir.status);
  console.log('  Response:', testRedirText.slice(0, 200));

  let redirFormat = null;
  if (testRedir.ok) {
    redirFormat = 'A';
    // Delete the test redirect we just created
    const testData = JSON.parse(testRedirText);
    const testId   = testData.id || testData.data?.id;
    if (testId) {
      await fetch(`${rmApi}/updateRedirection`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ id: testId, status: 'inactive' })
      });
    }
  } else {
    // Try format B
    const testB = await fetch(`${rmApi}/updateRedirection`, {
      method: 'POST', headers: h,
      body: JSON.stringify({
        objectID: 0,
        sources: '/seo-test-do-not-use/',
        destination: '/',
        type: '301'
      })
    });
    const testBText = await testB.text();
    console.log('  updateRedirection format B status:', testB.status, testBText.slice(0,100));
    if (testB.ok) redirFormat = 'B';
  }

  console.log('  Redirect format that works:', redirFormat || 'NONE — will fall back to WP Rank Math AJAX');

  // ── Helper: create redirect (handles both formats) ────────────────────────
  async function createRedirect(fromSlug, toUrl) {
    if (redirFormat === 'A') {
      const r = await fetch(`${rmApi}/updateRedirection`, {
        method: 'POST', headers: h,
        body: JSON.stringify({
          id: 0,
          sources: [{ pattern: fromSlug, comparison: 'exact' }],
          destination: toUrl,
          type: '301',
          status: 'active'
        })
      });
      return r.ok;
    }
    if (redirFormat === 'B') {
      const r = await fetch(`${rmApi}/updateRedirection`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ objectID: 0, sources: fromSlug, destination: toUrl, type: '301' })
      });
      return r.ok;
    }
    return false; // no working format found
  }

  // ============================================================
  // SECTION 2: Fetch all published posts (include duplicates)
  // ============================================================
  console.log('%c[2] Fetching all published posts to find duplicates...', 'color:#4CAF50;font-weight:bold');

  let allPosts = [], page = 1;
  while (true) {
    const r = await fetch(
      `${wpApi}/posts?per_page=100&page=${page}&status=publish&context=edit&_fields=id,slug,link,status`,
      { headers: h }
    );
    if (!r.ok) break;
    const batch = await r.json();
    if (!batch.length) break;
    allPosts.push(...batch);
    if (batch.length < 100) break;
    page++;
  }
  console.log(`  Total published posts: ${allPosts.length}`);

  // Find posts whose slug ends in -2, -3 ... -9 (duplicates)
  const duplicates = allPosts.filter(p => /^(.+)-(\d+)$/.test(p.slug));
  console.log(`  Duplicate slug posts found: ${duplicates.length}`);
  duplicates.forEach(p => console.log(`    [${p.id}] /${p.slug}/`));

  // ============================================================
  // SECTION 3: Create 301 redirects + trash duplicates
  // ============================================================
  console.log('%c[3] Creating 301 redirects + trashing duplicate posts...', 'color:#4CAF50;font-weight:bold');

  // Also include the dna-testing-services-atlanta-ga-7 from wp-admin notice
  const knownExtras = [
    { slug: 'dna-testing-services-atlanta-ga-7', canonical: '/dna-testing-services-atlanta-ga/' }
  ];

  // Build full list: auto-detected duplicates + known extras
  const toProcess = [
    ...duplicates.map(p => ({
      id:        p.id,
      slug:      p.slug,
      fromPath:  `/${p.slug}/`,
      canonical: `/${canonicalSlug(p.slug)}/`
    })),
    ...knownExtras.map(x => ({ id: null, slug: x.slug, fromPath: `/${x.slug}/`, canonical: x.canonical }))
  ];

  for (const item of toProcess) {
    const { id, fromPath, canonical } = item;

    // Step A: Verify canonical target exists
    const slugCheck = canonical.replace(/\//g, '');
    const checkR    = await fetch(`${wpApi}/posts?slug=${slugCheck}&_fields=id,slug`, { headers: h });
    const checkData = checkR.ok ? await checkR.json() : [];

    // Also check pages
    const checkRP   = await fetch(`${wpApi}/pages?slug=${slugCheck}&_fields=id,slug`, { headers: h });
    const checkPageData = checkRP.ok ? await checkRP.json() : [];

    const canonicalExists = (checkData.length + checkPageData.length) > 0;
    if (!canonicalExists) {
      console.warn(`  ⚠️  [${id}] canonical ${canonical} not found — skipping redirect`);
      log.errors.push({ id, issue: 'canonical-not-found', canonical });
      await sleep(100);
      continue;
    }

    // Step B: Create 301 redirect
    const toUrl    = `${origin}${canonical}`;
    const redirOk  = await createRedirect(fromPath, toUrl);

    if (redirOk) {
      console.log(`  ✅ 301: ${fromPath} → ${canonical}`);
      log.created.push({ from: fromPath, to: canonical });
    } else if (redirFormat === null) {
      console.log(`  ⚠️  ${fromPath} → ${canonical} (add manually — API format unknown)`);
      log.errors.push({ id, issue: 'redirect-api-unavailable', from: fromPath, to: canonical });
    } else {
      console.error(`  ❌ Redirect failed: ${fromPath}`);
      log.errors.push({ id, issue: 'redirect-failed', from: fromPath });
    }

    // Step C: Trash the duplicate post (removes it from sitemap)
    if (id) {
      const trashR = await fetch(`${wpApi}/posts/${id}`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ status: 'trash' })
      });
      if (trashR.ok) {
        console.log(`  🗑  Trashed post [${id}] /${item.slug}/`);
        log.trashed.push({ id, slug: item.slug });
      } else {
        console.error(`  ❌ Trash failed for [${id}]: ${trashR.status}`);
      }
    }
    await sleep(200);
  }

  // ============================================================
  // SECTION 4: Find + fix duplicate meta description tags
  // ============================================================
  console.log('%c[4] Scanning for duplicate meta description tags...', 'color:#4CAF50;font-weight:bold');

  // Fetch all pages list for scanning
  let allPages = [], pp = 1;
  while (true) {
    const r = await fetch(
      `${wpApi}/pages?per_page=100&page=${pp}&status=publish&_fields=id,slug,link`,
      { headers: h }
    );
    if (!r.ok) break;
    const batch = await r.json();
    if (!batch.length) break;
    allPages.push(...batch);
    if (batch.length < 100) break;
    pp++;
  }

  const dupeMeta = [];
  for (const item of [...allPages, ...allPosts.slice(0, 30)]) { // check pages + top 30 posts
    try {
      const r    = await fetch(item.link, { cache: 'no-store' });
      const html = await r.text();
      const count = (html.match(/name=["']description["']/gi) || []).length;
      if (count > 1) {
        console.log(`  ⚠️  DUPE [${item.id}] ${item.slug.slice(0,45)} — ${count} meta desc tags`);
        dupeMeta.push({ id: item.id, slug: item.slug, count });
      }
    } catch(e) {}
    await sleep(80);
  }
  console.log(`  Pages/posts with duplicate meta descriptions: ${dupeMeta.length}`);

  // For each duplicate: check if it's a page (Elementor-injected) and clear the Elementor seo setting
  for (const item of dupeMeta) {
    // Elementor stores SEO data in _elementor_page_settings — try to clear the meta description there
    const r = await fetch(`${wpApi}/pages/${item.id}?context=edit`, { headers: h });
    if (!r.ok) continue;
    const data = await r.json();
    const epSettings = data.meta?._elementor_page_settings;
    if (epSettings) {
      try {
        const settings = JSON.parse(epSettings);
        if (settings.description) {
          delete settings.description;
          const patch = await fetch(`${wpApi}/pages/${item.id}`, {
            method: 'POST', headers: h,
            body: JSON.stringify({ meta: { _elementor_page_settings: JSON.stringify(settings) } })
          });
          if (patch.ok) {
            console.log(`  ✅ Cleared Elementor description on page [${item.id}]`);
            log.dupeFixed.push({ id: item.id, fix: 'elementor-description-cleared' });
          }
        } else {
          console.log(`  ℹ️  [${item.id}] No description in _elementor_page_settings — duplicate source unknown`);
        }
      } catch(e) { console.log(`  ℹ️  [${item.id}] Could not parse Elementor settings`); }
    }
    await sleep(150);
  }

  // ============================================================
  // SECTION 5: Fix Elementor /services/ redirect link
  // ============================================================
  console.log('%c[5] Searching Elementor data for /services/ redirect link...', 'color:#4CAF50;font-weight:bold');

  const hpR = await fetch(`${wpApi}/pages/23?context=edit`, { headers: h });
  if (hpR.ok) {
    const hp     = await hpR.json();
    const elData = hp.meta?._elementor_data || '';

    if (elData) {
      // Elementor JSON-encodes URLs — try multiple patterns
      const patterns = [
        { find: '\\/services\\/',  replace: '\\/mobile-phlebotomy-services-atlanta\\/' },
        { find: '/services/',      replace: '/mobile-phlebotomy-services-atlanta/' },
        { find: '%2Fservices%2F',  replace: '%2Fmobile-phlebotomy-services-atlanta%2F' },
      ];
      let fixed = elData;
      let changed = false;
      for (const { find, replace } of patterns) {
        if (fixed.includes(find)) {
          fixed   = fixed.split(find).join(replace);
          changed = true;
          console.log(`  ✅ Found and replaced "${find}" in Elementor data`);
        }
      }
      if (changed) {
        const patch = await fetch(`${wpApi}/pages/23`, {
          method: 'POST', headers: h,
          body: JSON.stringify({ meta: { _elementor_data: fixed } })
        });
        if (patch.ok) {
          console.log('  ✅ Homepage Elementor data saved — /services/ link fixed');
          log.dupeFixed.push({ id: 23, fix: 'elementor-services-link' });
        } else {
          console.error('  ❌ Failed to save Elementor data:', patch.status);
          console.log('  ℹ️  Manual fix: Edit homepage in Elementor → find /services/ button → change to /mobile-phlebotomy-services-atlanta/');
        }
      } else {
        console.log('  ℹ️  /services/ not found in any format in _elementor_data');
        console.log('  ℹ️  It may be in a global header/nav widget — check Elementor → Templates → Theme Builder');
      }
    } else {
      console.log('  ⚠️  _elementor_data not accessible via REST');
    }
  }

  // ============================================================
  // SECTION 6: Check sitemap for 3XX URLs
  // ============================================================
  console.log('%c[6] Checking sitemap for 3XX redirect URLs...', 'color:#FF9800;font-weight:bold');

  try {
    const smR  = await fetch(`${origin}/sitemap_index.xml`, { cache: 'no-store' });
    const smXml = await smR.text();
    const smUrls = [...smXml.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]);
    console.log(`  Sitemap index has ${smUrls.length} sub-sitemaps`);

    // Check first sub-sitemap for redirect URLs (just spot-check a few)
    const firstSm = smUrls[0];
    if (firstSm) {
      const subR   = await fetch(firstSm);
      const subXml = await subR.text();
      const subUrls = [...subXml.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]).slice(0, 30);
      console.log(`  Checking first ${subUrls.length} URLs from ${firstSm.split('/').pop()}...`);
      for (const url of subUrls) {
        const r = await fetch(url, { method: 'HEAD', redirect: 'manual' });
        if (r.status >= 300 && r.status < 400) {
          console.log(`  ⚠️  3XX IN SITEMAP: ${url} → ${r.status} → ${r.headers.get('location')}`);
        }
        await sleep(100);
      }
    }
  } catch(e) {
    console.log('  Could not fetch sitemap:', e.message);
  }

  // ============================================================
  // SECTION 7: Regenerate Rank Math sitemap cache
  // ============================================================
  console.log('%c[7] Clearing Rank Math sitemap cache...', 'color:#4CAF50;font-weight:bold');

  const clearSm = await fetch(`${rmApi}/toolsAction`, {
    method: 'POST', headers: h,
    body: JSON.stringify({ action: 'flush_sitemap' })
  });
  console.log('  Sitemap cache clear status:', clearSm.status, clearSm.ok ? '✅' : '(manual clear needed via Rank Math → Sitemap)');

  // ============================================================
  // FINAL SUMMARY
  // ============================================================
  console.log('%c\n══════════ FINAL RESULTS ══════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c🔀 Redirects created: ${log.created.length}`,   'color:#4CAF50;font-weight:bold');
  console.log(`%c🗑  Posts trashed:     ${log.trashed.length}`,   'color:#4CAF50;font-weight:bold');
  console.log(`%c🔧 Other fixes:       ${log.dupeFixed.length}`,  'color:#4CAF50;font-weight:bold');
  console.log(`%c❌ Errors/manual:     ${log.errors.length}`,     'color:#f44336;font-weight:bold');
  console.log('\nRedirects created:', log.created);
  console.log('Posts trashed:', log.trashed);
  console.log('Other fixes:', log.dupeFixed);
  if (log.errors.length) {
    console.log('\n%cManual steps still needed:', 'color:#FF9800;font-weight:bold');
    console.table(log.errors);
  }
  console.log('%c\nDone. Paste this output back to Claude.', 'color:#2196F3;font-weight:bold');
})();
