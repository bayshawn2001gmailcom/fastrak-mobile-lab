/**
 * Fastrak Mobile Lab — SEO Trash + Redirect Fix (May 2, 2026)
 * Fixes learned from previous runs:
 *  - Use DELETE to trash posts (not POST status:trash)
 *  - Rank Math updateRedirection needs objectID + hasRedirect
 *  - Find /services/ in WordPress menus (not Elementor templates)
 *  - Find source of duplicate meta on posts 1171-1175
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const trashed    = [];
  const redirected = [];
  const errors     = [];

  // All duplicate post IDs to trash
  const toTrash = [981, 955, 954, 953, 952, 951, 950, 949, 948, 947, 946,
                   916, 915, 902, 901, 1003, 973, 972, 970, 966, 967];

  // Redirect map (from → to) for posts that have canonical targets
  const redirectMap = [
    { id: 981,  from: '/legal-chain-of-custody-dna-testing-gwinnett-county-law-support-2/',      to: '/legal-chain-of-custody-dna-testing-gwinnett-county-law-support/' },
    { id: 955,  from: '/discreet-mobile-infidelity-dna-testing-private-labs-serving-gwinnett-county-2/', to: '/discreet-mobile-infidelity-dna-testing-private-labs-serving-gwinnett-county/' },
    { id: 954,  from: '/mobile-dot-physicals-for-cdl-drivers-same-day-appointments-in-norcross-2/',       to: '/mobile-dot-physicals-for-cdl-drivers-same-day-appointments-in-norcross/' },
    { id: 953,  from: '/concierge-mobile-blood-draws-professional-phlebotomy-at-your-atlanta-home-2/',    to: '/concierge-mobile-blood-draws-professional-phlebotomy-at-your-atlanta-home/' },
    { id: 952,  from: '/mobile-respiratory-fit-testing-osha-compliance-for-georgia-construction-2/',      to: '/mobile-respiratory-fit-testing-osha-compliance-for-georgia-construction/' },
    { id: 951,  from: '/onsite-background-checks-fingerprinting-for-atlanta-healthcare-staffing-2/',      to: '/onsite-background-checks-fingerprinting-for-atlanta-healthcare-staffing/' },
    { id: 950,  from: '/mobile-gender-reveal-dna-testing-early-clinical-results-in-lawrenceville-2/',     to: '/mobile-gender-reveal-dna-testing-early-clinical-results-in-lawrenceville/' },
    { id: 949,  from: '/24-7-mobile-post-accident-breathalyzer-drug-screening-in-metro-atlanta-2/',       to: '/24-7-mobile-post-accident-breathalyzer-drug-screening-in-metro-atlanta/' },
    { id: 948,  from: '/legal-admissibility-mobile-dna-paternity-testing-for-georgia-court-cases-2/',    to: '/legal-admissibility-mobile-dna-paternity-testing-for-georgia-court-cases/' },
    { id: 947,  from: '/mobile-dot-drug-testing-for-fleet-managers-compliance-made-easy-in-gwinnett-2/', to: '/mobile-dot-drug-testing-for-fleet-managers-compliance-made-easy-in-gwinnett/' },
    { id: 946,  from: '/onsite-corporate-flu-wellness-clinics-mobile-immunizations-in-atlanta-2/',        to: '/onsite-corporate-flu-wellness-clinics-mobile-immunizations-in-atlanta/' },
    { id: 916,  from: '/the-difference-between-home-dna-kits-and-legal-paternity-tests-2/',               to: '/the-difference-between-home-dna-kits-and-legal-paternity-tests/' },
    { id: 915,  from: '/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know-2/',            to: '/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know/' },
    { id: 902,  from: '/the-difference-between-home-dna-kits-and-legal-paternity-tests-3/',               to: '/the-difference-between-home-dna-kits-and-legal-paternity-tests/' },
    { id: 901,  from: '/non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate-2/',               to: '/non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate/' },
    { id: null, from: '/dna-testing-services-atlanta-ga-7/',                                              to: '/dna-testing-services-atlanta-ga/' },
  ];

  // ── SECTION 1: Test Rank Math redirect with correct params ──────────────
  console.log('%c[1] Testing Rank Math updateRedirection with objectID + hasRedirect...', 'color:#FF9800;font-weight:bold');

  // Error revealed required params: objectID + hasRedirect
  const testA = await fetch(`${rmApi}/updateRedirection`, {
    method: 'POST', headers: h,
    body: JSON.stringify({
      objectID:    0,
      hasRedirect: true,
      sources:     [{ pattern: '/seo-redir-test/', comparison: 'exact' }],
      destination: `${origin}/`,
      type:        '301',
      status:      'active'
    })
  });
  const testAText = await testA.text();
  console.log('  Format A (objectID+hasRedirect+sources array):', testA.status, testAText.slice(0, 120));

  // Try format B: simpler params
  const testB = await fetch(`${rmApi}/updateRedirection`, {
    method: 'POST', headers: h,
    body: JSON.stringify({ objectID: 0, hasRedirect: true, url_from: '/seo-redir-test2/', url_to: '/', type: '301' })
  });
  const testBText = await testB.text();
  console.log('  Format B (url_from/url_to):', testB.status, testBText.slice(0, 120));

  const redirOk = testA.ok ? 'A' : testB.ok ? 'B' : null;
  console.log('  Working format:', redirOk || 'none — redirects need manual entry');

  async function doRedirect(from, to) {
    if (redirOk === 'A') {
      const r = await fetch(`${rmApi}/updateRedirection`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ objectID: 0, hasRedirect: true, sources: [{ pattern: from, comparison: 'exact' }], destination: `${origin}${to}`, type: '301', status: 'active' })
      });
      return r.ok;
    }
    if (redirOk === 'B') {
      const r = await fetch(`${rmApi}/updateRedirection`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ objectID: 0, hasRedirect: true, url_from: from, url_to: to, type: '301' })
      });
      return r.ok;
    }
    return false;
  }

  // ── SECTION 2: Create redirects first, then trash ──────────────────────
  console.log('%c[2] Creating 301 redirects...', 'color:#4CAF50;font-weight:bold');

  for (const item of redirectMap) {
    if (!item.from || !item.to) continue;
    const ok = await doRedirect(item.from, item.to);
    if (ok) {
      console.log(`  ✅ 301 created: ${item.from} → ${item.to}`);
      redirected.push({ from: item.from, to: item.to });
    } else {
      console.log(`  ⚠️  ${item.from} → ${item.to}`);
      errors.push({ from: item.from, to: item.to, issue: 'manual-needed' });
    }
    await sleep(100);
  }

  // ── SECTION 3: Trash duplicate posts using DELETE ──────────────────────
  console.log('%c[3] Trashing duplicate posts via DELETE...', 'color:#4CAF50;font-weight:bold');

  for (const id of toTrash) {
    // DELETE without force=true sends to trash (not permanent delete)
    const r = await fetch(`${wpApi}/posts/${id}`, {
      method: 'DELETE', headers: h
    });
    if (r.ok) {
      console.log(`  🗑  Trashed [${id}]`);
      trashed.push(id);
    } else {
      const txt = await r.text();
      console.error(`  ❌ [${id}] ${r.status}: ${txt.slice(0, 80)}`);
      errors.push({ id, issue: `trash-failed-${r.status}` });
    }
    await sleep(120);
  }
  console.log(`  Trashed: ${trashed.length}/${toTrash.length}`);

  // ── SECTION 4: Find /services/ in WordPress nav menus ─────────────────
  console.log('%c[4] Searching WordPress menus for /services/ link...', 'color:#4CAF50;font-weight:bold');

  const menusR = await fetch(`${wpApi}/menus?per_page=20&_fields=id,name,slug`, { headers: h });
  if (menusR.ok) {
    const menus = await menusR.json();
    console.log(`  Found ${menus.length} menus:`, menus.map(m => m.name).join(', '));
    for (const menu of menus) {
      const itemsR = await fetch(`${wpApi}/menu-items?menus=${menu.id}&per_page=100&_fields=id,title,url`, { headers: h });
      if (!itemsR.ok) continue;
      const items = await itemsR.json();
      for (const item of items) {
        if (item.url && item.url.includes('/services/')) {
          console.log(`  ⚠️  FOUND in menu "${menu.name}" [item ${item.id}]: "${item.title?.rendered}" → ${item.url}`);
          // Fix it
          const patch = await fetch(`${wpApi}/menu-items/${item.id}`, {
            method: 'POST', headers: h,
            body: JSON.stringify({ url: `${origin}/mobile-phlebotomy-services-atlanta/` })
          });
          if (patch.ok) {
            console.log(`  ✅ Fixed menu item ${item.id}`);
          } else {
            console.log(`  ❌ Could not fix menu item ${item.id}: ${patch.status}`);
          }
        }
      }
    }
  } else {
    console.log(`  Menus endpoint: ${menusR.status} — checking nav-menus via options`);
    // Try wp-nav-menus via admin-ajax
    const fd = new FormData();
    fd.append('action', 'get-tagcloud'); // just a test
    fd.append('nonce', nonce);
  }

  // ── SECTION 5: Identify source of duplicate meta on posts 1171-1175 ───
  console.log('%c[5] Diagnosing duplicate meta description source on posts 1171-1175...', 'color:#FF9800;font-weight:bold');

  for (const pid of [1171, 1172]) { // just check 2 as sample
    const r = await fetch(`https://fastrakmobilelab.com/?p=${pid}`, { cache: 'no-store' });
    const html = await r.text();
    // Extract ALL meta description tags
    const metas = [...html.matchAll(/<meta[^>]+name=["']description["'][^>]*>/gi)].map(m => m[0]);
    console.log(`  Post ${pid} — ${metas.length} meta description tag(s):`);
    metas.forEach((m, i) => console.log(`    [${i+1}] ${m.slice(0, 120)}`));
  }

  // ── SECTION 6: Rank Math updateRedirection correct format discovery ────
  console.log('%c[6] Checking Rank Math route details for redirect format...', 'color:#FF9800;font-weight:bold');

  // Fetch the options endpoint to find redirect route args
  const routeR = await fetch(`${origin}/wp-json/rankmath/v1`, { headers: h });
  if (routeR.ok) {
    const routeData = await routeR.json();
    const redirRoute = routeData.routes?.['/rankmath/v1/updateRedirection'];
    if (redirRoute) {
      const args = redirRoute.endpoints?.[0]?.args || {};
      console.log('  updateRedirection args:', JSON.stringify(Object.keys(args)));
      Object.entries(args).forEach(([k, v]) => {
        console.log(`    ${k}: required=${v.required}, type=${v.type}`);
      });
    }
  }

  // ── SUMMARY ────────────────────────────────────────────────────────────
  console.log('%c\n══════════ RESULTS ══════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c🗑  Posts trashed:     ${trashed.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c🔀 Redirects created: ${redirected.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c⚠️  Manual needed:     ${errors.filter(e=>e.issue==='manual-needed').length}`, 'color:#FF9800;font-weight:bold');
  console.log(`%c❌ Other errors:       ${errors.filter(e=>e.issue!=='manual-needed').length}`, 'color:#f44336;font-weight:bold');
  console.log('\nTrashed IDs:', trashed);
  if (redirected.length) console.log('Redirects:', redirected);
  if (errors.some(e => e.issue === 'manual-needed')) {
    console.log('\n%cManual redirects for Rank Math → Redirections:', 'color:#FF9800;font-weight:bold');
    errors.filter(e => e.issue === 'manual-needed').forEach(e => console.log(`  ${e.from}  →  ${e.to}`));
  }
  console.log('%cDone. Paste output back to Claude.', 'color:#2196F3;font-weight:bold');
})();
