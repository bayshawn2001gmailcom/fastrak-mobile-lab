/**
 * Fastrak Mobile Lab — 404 Audit + Redirect Automation (May 2026)
 *
 * Addresses: 33 pages returning 404 errors (17.6% of crawled pages) and
 *            3 redirect chains (A → B → C should be A → C).
 *
 * What this script does:
 *   1. Fetches all posts and pages (any status) from the WP REST API
 *   2. HEAD-checks each URL for HTTP status
 *   3. For 404s with a slug pattern ending in -2/-3/etc. → auto-creates 301
 *      redirect to the canonical slug (without the number suffix)
 *   4. For 404s with no clear canonical → logs them for manual review
 *   5. Detects redirect chains (A→B→C) by following redirects and comparing
 *      the intermediate vs final destination
 *   6. Collapses chains to direct 301s where possible
 *
 * RUN: Paste into wp-admin browser console (any wp-admin page).
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const report = {
    checked:         0,
    ok:              [],
    redirects:       [],
    notFound:        [],
    autoFixed:       [],
    chainFixed:      [],
    manualReview:    [],
    errors:          []
  };

  // ── Helper: Rank Math redirect creation (tries two formats) ─────────────
  const rmNonce = window.rankMath?.security || window.rankMathEditor?.security || nonce;

  async function createRedirect(fromPath, toPath) {
    // Format A: REST API with sources array
    const r = await fetch(`${rmApi}/updateRedirection`, {
      method: 'POST', headers: h,
      body: JSON.stringify({
        objectID: 0, hasRedirect: true,
        sources: [{ pattern: fromPath, comparison: 'exact' }],
        destination: `${origin}${toPath}`,
        type: '301', status: 'active'
      })
    });
    if (r.ok) return { ok: true, method: 'REST-A' };

    // Format B: admin-ajax
    const fd = new FormData();
    fd.append('action',      'rank_math_redirection_create');
    fd.append('security',    rmNonce);
    fd.append('url_from',    fromPath);
    fd.append('url_to',      toPath);
    fd.append('header_code', '301');
    fd.append('status',      'active');
    const ajaxR = await fetch(`${origin}/wp-admin/admin-ajax.php`, { method: 'POST', body: fd });
    if (ajaxR.ok) {
      const txt = await ajaxR.text();
      if (txt.includes('"success":true') || txt.includes('"id"')) return { ok: true, method: 'AJAX' };
    }

    return { ok: false, method: 'none' };
  }

  // ── Helper: check URL status (no-redirect follow) ────────────────────────
  async function checkUrl(url) {
    try {
      const r = await fetch(url, { method: 'HEAD', redirect: 'manual', credentials: 'omit' });
      return { status: r.status, location: r.headers.get('location') || null };
    } catch (e) {
      return { status: 0, error: e.message };
    }
  }

  // ── Helper: follow redirect chain to get final destination ──────────────
  async function finalDestination(url, maxHops = 5) {
    let current = url;
    const chain = [url];
    for (let i = 0; i < maxHops; i++) {
      const { status, location } = await checkUrl(current);
      if (status >= 300 && status < 400 && location) {
        const next = location.startsWith('http') ? location : `${origin}${location}`;
        if (chain.includes(next)) break;
        chain.push(next);
        current = next;
      } else {
        break;
      }
    }
    return { final: current, chain, hops: chain.length - 1 };
  }

  // ── Helper: slug → canonical (strips -2, -3, ... -99 suffix) ────────────
  function canonicalPath(path) {
    return path.replace(/-\d{1,2}\/$/, '/').replace(/-\d{1,2}$/, '');
  }

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 1 — Collect all URLs to check
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[1] Fetching all published + trashed posts and pages...', 'color:#FF9800;font-weight:bold');

  async function fetchAll(type, statuses = ['publish', 'trash', 'draft']) {
    const items = [];
    for (const status of statuses) {
      let page = 1;
      while (true) {
        const r = await fetch(`${wpApi}/${type}?status=${status}&per_page=100&page=${page}&_fields=id,link,slug,status`, { headers: h });
        if (!r.ok) break;
        const batch = await r.json();
        if (!batch.length) break;
        items.push(...batch.map(i => ({ ...i, postType: type })));
        if (batch.length < 100) break;
        page++;
        await sleep(150);
      }
    }
    return items;
  }

  const [pages, posts] = await Promise.all([fetchAll('pages'), fetchAll('posts')]);
  const allItems = [...pages, ...posts];

  // Build URL list: published items use .link, trashed items reconstruct slug-based URL
  const urlsToCheck = allItems
    .filter(item => item.link || item.slug)
    .map(item => ({
      id:   item.id,
      type: item.postType,
      status: item.status,
      url:  item.link || `${origin}/${item.slug}/`,
      slug: item.slug
    }));

  // Also add common known redirect/404 patterns from prior Ahrefs audit
  const additionalPaths = [
    '/services/',
    '/blog/page/2/', '/blog/page/3/',
    '/mobile-phlebotomy-atlanta/', '/mobile-phlebotomy-services-atlanta/',
  ];
  for (const path of additionalPaths) {
    urlsToCheck.push({ id: null, type: 'path', status: 'unknown', url: `${origin}${path}`, slug: path });
  }

  console.log(`  Total URLs to check: ${urlsToCheck.length}`);

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 2 — HEAD-check each URL
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[2] Checking HTTP status of each URL (this may take 1–2 minutes)...', 'color:#FF9800;font-weight:bold');

  for (const item of urlsToCheck) {
    const { status, location } = await checkUrl(item.url);
    report.checked++;
    item.httpStatus  = status;
    item.location    = location;

    if (status === 404) {
      report.notFound.push(item);
      console.warn(`  404: ${item.url}`);
    } else if (status >= 300 && status < 400) {
      report.redirects.push(item);
    } else if (status === 200) {
      report.ok.push(item.url);
    } else if (status === 0) {
      report.errors.push(`Network error: ${item.url}`);
    }
    await sleep(100);
  }

  console.log(`  Checked ${report.checked} URLs: ${report.ok.length} OK | ${report.notFound.length} 404 | ${report.redirects.length} redirects`);

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 3 — Auto-fix 404s with canonical slug pattern
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[3] Auto-creating 301 redirects for 404 pages with slug patterns...', 'color:#FF9800;font-weight:bold');

  for (const item of report.notFound) {
    const path = new URL(item.url).pathname;
    const canonical = canonicalPath(path);

    if (canonical !== path) {
      // Slug ends in -2/-3 etc. — check if canonical exists
      const canonicalUrl = `${origin}${canonical}`;
      const { status: canonStatus } = await checkUrl(canonicalUrl);
      await sleep(100);

      if (canonStatus === 200) {
        const result = await createRedirect(path, canonical);
        if (result.ok) {
          report.autoFixed.push({ from: path, to: canonical, method: result.method });
          console.log(`  ✔ Auto-redirect: ${path} → ${canonical} (${result.method})`);
        } else {
          report.manualReview.push({ url: item.url, reason: `Redirect creation failed — canonical ${canonical} exists (${canonStatus})` });
          console.warn(`  ✖ Failed to create redirect ${path} → ${canonical}`);
        }
      } else {
        report.manualReview.push({ url: item.url, reason: `Canonical ${canonical} returns ${canonStatus} — cannot auto-redirect` });
        console.warn(`  Manual review: ${path} — canonical ${canonical} returns ${canonStatus}`);
      }
    } else {
      report.manualReview.push({ url: item.url, reason: 'No canonical slug pattern — check if page was deleted or moved' });
      console.warn(`  Manual review: ${item.url} — no canonical pattern`);
    }
    await sleep(300);
  }

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 4 — Detect and collapse redirect chains (A → B → C)
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[4] Detecting redirect chains...', 'color:#FF9800;font-weight:bold');

  for (const item of report.redirects) {
    const { final, chain, hops } = await finalDestination(item.url);
    if (hops >= 2) {
      console.warn(`  Chain (${hops} hops): ${chain.join(' → ')}`);
      // Collapse: redirect the original source directly to the final destination
      const from = new URL(item.url).pathname;
      const to   = final.startsWith(origin) ? final.slice(origin.length) : final;
      if (to && to !== from) {
        const result = await createRedirect(from, to);
        if (result.ok) {
          report.chainFixed.push({ chain: chain.map(u => u.replace(origin, '')), collapsedTo: to, method: result.method });
          console.log(`  ✔ Chain collapsed: ${from} → ${to}`);
        } else {
          report.manualReview.push({ url: item.url, reason: `Redirect chain (${hops} hops) — collapse to ${to} failed` });
        }
      }
      await sleep(400);
    }
  }

  // ════════════════════════════════════════════════════════════════════════
  // SUMMARY
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c\n══ 404 AUDIT + REDIRECT SUMMARY ══', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`Total URLs checked:      ${report.checked}`);
  console.log(`200 OK:                  ${report.ok.length}`);
  console.log(`404 Not Found:           ${report.notFound.length}`);
  console.log(`  Auto-redirected (301): ${report.autoFixed.length}`);
  console.log(`  Needs manual review:   ${report.manualReview.length}`);
  console.log(`Redirect chains fixed:   ${report.chainFixed.length}`);

  if (report.autoFixed.length) {
    console.log('%c\nAuto-created 301 redirects:', 'color:#4CAF50;font-weight:bold');
    report.autoFixed.forEach(r => console.log(`  ${r.from} → ${r.to}`));
  }

  if (report.chainFixed.length) {
    console.log('%c\nCollapsed redirect chains:', 'color:#4CAF50;font-weight:bold');
    report.chainFixed.forEach(r => console.log(`  [${r.chain.join(' → ')}] → direct to ${r.collapsedTo}`));
  }

  if (report.manualReview.length) {
    console.log('%c\nManual review required:', 'color:#F44336;font-weight:bold');
    console.table(report.manualReview.map(r => ({ URL: r.url || r.from, Reason: r.reason })));
    console.log('\nFor each URL above:');
    console.log('  - If the page was moved: set up a 301 redirect in Rank Math → Redirections');
    console.log('  - If the page was deleted permanently: return a 410 Gone (add to Rank Math redirect with 410 code)');
    console.log('  - If the URL was never valid: block in robots.txt or add 410 in Rank Math');
  }

  if (report.errors.length) {
    console.warn(`\nNetwork errors (${report.errors.length}):`);
    report.errors.forEach(e => console.warn('  ', e));
  }

  console.log('\n%cNEXT STEPS:', 'color:#FF9800;font-weight:bold');
  console.log('1. After running, go to Rank Math → Redirections to verify created redirects.');
  console.log('2. Submit updated sitemap in Google Search Console after all 404s are resolved.');
  console.log('3. Re-run Ahrefs Site Audit in 48 hours to verify 404 count has dropped.');

  console.log('%c\nDone.', 'color:#4CAF50;font-weight:bold');
})();
