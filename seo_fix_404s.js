/**
 * Fastrak Mobile Lab — 404 Audit & Fix Script (May 2026)
 *
 * Actions:
 *  1. Auto-detect working Rank Math redirect API format (3 formats tried)
 *  2. Create standalone 301: /dna-testing-services-atlanta-ga-7/ → /dna-testing-services-atlanta-ga/
 *  3. Scan ALL posts and pages for remaining -2 to -9 duplicate slug patterns → redirect + trash
 *  4. Fetch live sitemap and HEAD-probe every URL for 404 responses
 *  5. Auto-create redirects for probed 404s that match duplicate slug patterns
 *  6. Print full summary + manual-review list for any unknown 404s
 *
 * How to run:
 *   1. Open https://fastrakmobilelab.com/wp-admin/ in Chrome
 *   2. Open DevTools → Console
 *   3. Paste the entire script and press Enter
 *   4. Wait ~3-5 min for sitemap probe to complete
 *   5. Copy the final summary output and paste back to Claude
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin; // https://fastrakmobilelab.com
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));
  const log    = { redirectsCreated: [], trashed: [], fourOhFours: [], manualNeeded: [], errors: [] };

  // Regex: slug ends with -2 through -9 (known duplicate pattern)
  const dupSuffix = /-[2-9]$/;

  function canonicalPath(path) {
    // /some-slug-3/ → /some-slug/
    return path.replace(/-[2-9]\/$/, '/').replace(/-[2-9]$/, '');
  }

  function parseLocs(xml) {
    return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].trim());
  }

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 1 — Auto-detect working Rank Math redirect API format
  // ══════════════════════════════════════════════════════════════════════════
  console.log('%c[1/5] Detecting Rank Math redirect API format...', 'color:#FF9800;font-weight:bold');

  let redirFn = null;

  async function _tryA(from, to) {
    const r = await fetch(`${rmApi}/updateRedirection`, {
      method: 'POST', headers: h,
      body: JSON.stringify({
        id: 0,
        sources: [{ pattern: from, comparison: 'exact' }],
        destination: `${origin}${to}`,
        type: '301',
        status: 'active'
      })
    });
    const text = await r.text();
    return { ok: r.ok, status: r.status, text };
  }

  async function _tryB(from, to) {
    const r = await fetch(`${rmApi}/updateRedirection`, {
      method: 'POST', headers: h,
      body: JSON.stringify({
        objectID: 0,
        hasRedirect: true,
        sources: [{ pattern: from, comparison: 'exact' }],
        destination: `${origin}${to}`,
        type: '301',
        status: 'active'
      })
    });
    const text = await r.text();
    return { ok: r.ok, status: r.status, text };
  }

  async function _tryC(from, to) {
    const security = window.rankMath?.security || window.rankMathEditor?.security || nonce;
    const fd = new FormData();
    fd.append('action',      'rank_math_redirection_create');
    fd.append('security',    security);
    fd.append('url_from',    from);
    fd.append('url_to',      `${origin}${to}`);
    fd.append('header_code', '301');
    fd.append('status',      'active');
    const r = await fetch(`${origin}/wp-admin/admin-ajax.php`, { method: 'POST', body: fd });
    const text = await r.text();
    const ok = r.ok && (text.includes('"success":true') || text.includes('success'));
    return { ok, status: r.status, text };
  }

  const TEST = '/seo-404-fix-detect-redir/';
  const resA = await _tryA(TEST, '/');
  console.log('  Format A (id+sources):', resA.status, resA.text.slice(0, 100));
  if (resA.ok) {
    redirFn = _tryA;
    console.log('  ✅ Using Format A');
  } else {
    const resB = await _tryB(TEST, '/');
    console.log('  Format B (objectID+hasRedirect+sources):', resB.status, resB.text.slice(0, 100));
    if (resB.ok) {
      redirFn = _tryB;
      console.log('  ✅ Using Format B');
    } else {
      const resC = await _tryC(TEST, '/');
      console.log('  Format C (admin-ajax):', resC.status, resC.text.slice(0, 100));
      if (resC.ok) {
        redirFn = _tryC;
        console.log('  ✅ Using Format C (admin-ajax)');
      } else {
        console.warn('  ❗ No redirect API format worked. Redirects will be logged for manual entry.');
      }
    }
  }

  async function createRedirect(fromPath, toPath, label) {
    if (!redirFn) {
      log.manualNeeded.push({ from: fromPath, to: toPath, reason: 'no-api' });
      return false;
    }
    const res = await redirFn(fromPath, toPath);
    if (res.ok) {
      console.log(`  ✅ 301: ${fromPath} → ${toPath}`);
      log.redirectsCreated.push({ from: fromPath, to: toPath, label: label || '' });
      return true;
    } else {
      console.warn(`  ⚠️  Redirect failed [${res.status}]: ${fromPath}`);
      log.manualNeeded.push({ from: fromPath, to: toPath, reason: `http-${res.status}` });
      return false;
    }
  }

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 2 — Standalone 301 for known 404: /dna-testing-services-atlanta-ga-7/
  // ══════════════════════════════════════════════════════════════════════════
  console.log('\n%c[2/5] Creating redirect for /dna-testing-services-atlanta-ga-7/...', 'color:#4CAF50;font-weight:bold');

  // Verify it's actually still a 404 before creating redirect
  const dnaCheck = await fetch(`${origin}/dna-testing-services-atlanta-ga-7/`, {
    method: 'HEAD', redirect: 'manual', cache: 'no-store'
  });
  console.log(`  Live status of /dna-testing-services-atlanta-ga-7/: ${dnaCheck.status}`);

  if (dnaCheck.status === 404 || dnaCheck.status === 0 || dnaCheck.status >= 400) {
    await createRedirect(
      '/dna-testing-services-atlanta-ga-7/',
      '/dna-testing-services-atlanta-ga/',
      'known-standalone-404'
    );
  } else if (dnaCheck.status === 301 || dnaCheck.status === 302) {
    console.log('  ℹ️  Already redirecting — skip.');
  } else {
    console.log(`  ℹ️  Status ${dnaCheck.status} — no action needed.`);
  }
  await sleep(300);

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 3 — Scan all posts + pages for remaining -N suffix duplicates
  // ══════════════════════════════════════════════════════════════════════════
  console.log('\n%c[3/5] Scanning posts and pages for -2 to -9 slug patterns...', 'color:#4CAF50;font-weight:bold');

  async function fetchAllItems(endpoint) {
    const items = [];
    let page = 1;
    while (true) {
      const r = await fetch(
        `${endpoint}?per_page=100&page=${page}&status=any&_fields=id,slug,status,type&context=edit`,
        { headers: h }
      );
      if (!r.ok) break;
      const data = await r.json();
      if (!Array.isArray(data) || !data.length) break;
      items.push(...data);
      const totalPages = parseInt(r.headers.get('X-WP-TotalPages') || '1', 10);
      if (page >= totalPages) break;
      page++;
      await sleep(150);
    }
    return items;
  }

  const allPosts = await fetchAllItems(`${wpApi}/posts`);
  const allPages = await fetchAllItems(`${wpApi}/pages`);
  const allItems = [...allPosts, ...allPages];
  console.log(`  Scanned ${allPosts.length} posts + ${allPages.length} pages = ${allItems.length} total`);

  const dupItems = allItems.filter(item => dupSuffix.test(item.slug));
  console.log(`  Found ${dupItems.length} items with duplicate slug patterns:`);
  dupItems.forEach(item => console.log(`  • [${item.id}] /${item.slug}/ (${item.status}, ${item.type || 'post'})`));

  for (const item of dupItems) {
    const fromPath = `/${item.slug}/`;
    const toPath   = canonicalPath(fromPath);
    const endpoint = (item.type === 'page' || allPages.some(p => p.id === item.id))
      ? `${wpApi}/pages/${item.id}`
      : `${wpApi}/posts/${item.id}`;

    // Create redirect before trashing
    await createRedirect(fromPath, toPath, `dup-${item.type || 'post'}-${item.id}`);
    await sleep(200);

    // Trash if still live
    if (item.status !== 'trash') {
      const del = await fetch(endpoint, { method: 'DELETE', headers: h });
      if (del.ok) {
        console.log(`  🗑  Trashed [${item.id}] /${item.slug}/`);
        log.trashed.push({ id: item.id, slug: item.slug });
      } else {
        const txt = await del.text();
        console.warn(`  ❌ Trash failed [${item.id}]: ${del.status} — ${txt.slice(0, 60)}`);
        log.errors.push({ id: item.id, slug: item.slug, issue: `trash-${del.status}` });
      }
      await sleep(200);
    } else {
      console.log(`  ℹ️  [${item.id}] already trashed — redirect only`);
    }
  }

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 4 — Fetch sitemap and HEAD-probe all URLs for 404 errors
  // ══════════════════════════════════════════════════════════════════════════
  console.log('\n%c[4/5] Probing sitemap URLs for 404 errors...', 'color:#4CAF50;font-weight:bold');

  let sitemapUrls = [];

  try {
    const indexResp = await fetch(`${origin}/sitemap_index.xml`, { cache: 'no-store' });
    const indexXml  = await indexResp.text();
    const subUrls   = parseLocs(indexXml).filter(u => u.includes('sitemap'));
    console.log(`  Found ${subUrls.length} sub-sitemaps:`, subUrls.map(u => u.split('/').pop()).join(', '));

    for (const subUrl of subUrls) {
      const r = await fetch(subUrl, { cache: 'no-store' });
      if (!r.ok) { console.warn(`  ⚠️  Could not fetch ${subUrl} (${r.status})`); continue; }
      const xml  = await r.text();
      const locs = parseLocs(xml).filter(u => !u.includes('sitemap'));
      sitemapUrls.push(...locs);
      await sleep(150);
    }
    console.log(`  Total URLs to probe: ${sitemapUrls.length}`);
  } catch (e) {
    console.warn('  ❌ Sitemap fetch error:', e.message);
  }

  // HEAD-probe in batches of 5
  const BATCH = 5;
  for (let i = 0; i < sitemapUrls.length; i += BATCH) {
    const batch = sitemapUrls.slice(i, i + BATCH);

    const results = await Promise.all(batch.map(async url => {
      try {
        const r = await fetch(url, { method: 'HEAD', redirect: 'manual', cache: 'no-store' });
        return { url, status: r.status };
      } catch (e) {
        return { url, status: 'error', err: e.message };
      }
    }));

    for (const res of results) {
      if (res.status === 404 || res.status === 410) {
        console.warn(`  ❌ ${res.status}: ${res.url}`);
        log.fourOhFours.push({ url: res.url, status: res.status });
      } else if (res.status >= 400 && res.status !== 'error') {
        console.warn(`  ⚠️  ${res.status}: ${res.url}`);
        log.errors.push({ url: res.url, status: res.status });
      }
    }

    if ((i + BATCH) % 50 === 0) {
      console.log(`  ... probed ${Math.min(i + BATCH, sitemapUrls.length)} / ${sitemapUrls.length}`);
    }
    await sleep(120);
  }

  console.log(`  Probe complete. 404/410 URLs found: ${log.fourOhFours.length}`);

  // Auto-redirect 404s with recognisable duplicate slug patterns
  for (const item of log.fourOhFours) {
    let path;
    try { path = new URL(item.url).pathname; } catch { continue; }
    const slug = path.replace(/^\/|\/$/g, '');

    if (dupSuffix.test(slug)) {
      const canonical = canonicalPath(path.endsWith('/') ? path : path + '/');
      console.log(`  Auto-redirecting ${item.status}: ${path} → ${canonical}`);
      await createRedirect(path.endsWith('/') ? path : path + '/', canonical, 'sitemap-404-auto');
      await sleep(200);
    } else {
      log.manualNeeded.push({ from: path, to: '???', reason: `${item.status}-unknown-pattern` });
    }
  }

  // ══════════════════════════════════════════════════════════════════════════
  // SECTION 5 — Summary
  // ══════════════════════════════════════════════════════════════════════════
  console.log('\n%c══════════════ 404 FIX SUMMARY ══════════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c✅ 301 redirects created:     ${log.redirectsCreated.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c🗑  Posts/pages trashed:       ${log.trashed.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c❌ 404/410s found in sitemap:  ${log.fourOhFours.length}`, 'color:#f44336;font-weight:bold');
  console.log(`%c⚠️  Manual review needed:      ${log.manualNeeded.length}`, 'color:#FF9800;font-weight:bold');
  console.log(`%c🔴 Other errors:               ${log.errors.length}`, 'color:#FF5722;font-weight:bold');

  if (log.redirectsCreated.length) {
    console.log('\n%cRedirects created:', 'color:#4CAF50;font-weight:bold');
    log.redirectsCreated.forEach(r => console.log(`  ${r.from}  →  ${r.to}  [${r.label}]`));
  }

  if (log.trashed.length) {
    console.log('\n%cTrashed post/page IDs:', 'color:#4CAF50;font-weight:bold');
    console.log(' ', log.trashed.map(t => t.id).join(', '));
  }

  if (log.manualNeeded.length) {
    console.log('\n%c⚠️  MANUAL ACTION REQUIRED — add these in Rank Math → Redirections:', 'color:#FF9800;font-weight:bold');
    log.manualNeeded.forEach(r => {
      console.log(`  ${r.from}  →  ${r.to !== '???' ? r.to : '[determine canonical URL]'}  (${r.reason})`);
    });
  }

  if (log.fourOhFours.filter(f => {
    try { const p = new URL(f.url).pathname.replace(/^\/|\/$/g, ''); return !dupSuffix.test(p); } catch { return false; }
  }).length) {
    console.log('\n%c❌ Unknown-pattern 404s (need manual canonical mapping):', 'color:#f44336;font-weight:bold');
    log.fourOhFours.forEach(f => {
      try {
        const p = new URL(f.url).pathname.replace(/^\/|\/$/g, '');
        if (!dupSuffix.test(p)) console.log(`  ${f.status}: ${f.url}`);
      } catch {}
    });
  }

  console.log('\n%cDone. Copy this entire output and paste it back to Claude.', 'color:#2196F3;font-weight:bold');
  console.log('Log object (inspect for full detail):', log);
})();
