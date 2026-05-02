/**
 * Fastrak Mobile Lab — SEO Targeted Fix (May 2, 2026)
 * Based on final script diagnostic output:
 *   1. Trash all 22 duplicate posts → removes them from sitemap (fixes 16 noindex-in-sitemap errors)
 *   2. Try Rank Math redirect creation via admin-ajax (new approach)
 *   3. Fix 5 duplicate meta description tags — using POSTS endpoint (not pages)
 *   4. Find Elementor Theme Builder template containing /services/ nav link
 * Paste into wp-admin console.
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const trashed   = [];
  const redirected = [];
  const errors    = [];

  // ── Redirect map: from → to (all 22 from final script error table) ─────────
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
    // canonical-not-found: just trash, no redirect needed (originals don't exist)
    { id: 1003, from: null, to: null },
    { id: 973,  from: null, to: null },
    { id: 972,  from: null, to: null },
    { id: 970,  from: null, to: null },
    { id: 966,  from: null, to: null },
    { id: 967,  from: null, to: null },
  ];

  // ============================================================
  // SECTION 1: Try Rank Math redirect via admin-ajax (new approach)
  // ============================================================
  console.log('%c[1] Testing Rank Math redirect via admin-ajax...', 'color:#FF9800;font-weight:bold');

  // Check if rankMath global exists (Rank Math injects this on admin pages)
  const rmNonce = window.rankMath?.security || window.rankMathEditor?.security || nonce;
  console.log('  rankMath global:', typeof window.rankMath, '| security nonce available:', !!rmNonce);

  // Try admin-ajax with Rank Math's redirection action
  async function createRedirectAjax(fromUrl, toUrl) {
    const fd = new FormData();
    fd.append('action',      'rank_math_redirection_create');
    fd.append('security',    rmNonce);
    fd.append('url_from',    fromUrl);
    fd.append('url_to',      toUrl);
    fd.append('header_code', '301');
    fd.append('status',      'active');
    const r = await fetch(`${origin}/wp-admin/admin-ajax.php`, { method: 'POST', body: fd });
    const txt = await r.text();
    return { ok: r.ok, status: r.status, body: txt.slice(0, 150) };
  }

  // Also try the REST endpoint with a different body format
  async function createRedirectRest(fromUrl, toUrl) {
    const r = await fetch(`${rmApi}/updateRedirection`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ url_from: fromUrl, url_to: toUrl, type: '301', status: 'active' })
    });
    const txt = await r.text();
    return { ok: r.ok, status: r.status, body: txt.slice(0, 150) };
  }

  // Test with one known redirect
  const testAjax = await createRedirectAjax('/seo-test-ajax/', `${origin}/`);
  console.log('  admin-ajax result:', testAjax);

  const testRest = await createRedirectRest('/seo-test-rest/', `${origin}/`);
  console.log('  REST v2 result:', testRest);

  const redirWorks = testAjax.ok && testAjax.body.includes('success') ? 'ajax'
                   : testRest.ok ? 'rest'
                   : null;
  console.log('  Working redirect method:', redirWorks || 'NONE');

  async function createRedirect(from, to) {
    if (!from || !to) return false;
    if (redirWorks === 'ajax') return (await createRedirectAjax(from, to)).ok;
    if (redirWorks === 'rest') return (await createRedirectRest(from, to)).ok;
    return false;
  }

  // ============================================================
  // SECTION 2: Find ID of dna-testing-services-atlanta-ga-7
  // ============================================================
  console.log('%c[2] Finding ID for dna-testing-services-atlanta-ga-7...', 'color:#4CAF50;font-weight:bold');

  const dnaSearch = await fetch(
    `${wpApi}/posts?slug=dna-testing-services-atlanta-ga-7&context=edit&_fields=id,slug,status`,
    { headers: h }
  );
  if (dnaSearch.ok) {
    const dnaData = await dnaSearch.json();
    if (dnaData.length) {
      const dnaPost = dnaData[0];
      console.log(`  Found: ID ${dnaPost.id} (${dnaPost.status})`);
      const entry = redirectMap.find(x => x.from === '/dna-testing-services-atlanta-ga-7/');
      if (entry) entry.id = dnaPost.id;
    } else {
      console.log('  Not found as post — checking pages...');
      const dnaPg = await fetch(`${wpApi}/pages?slug=dna-testing-services-atlanta-ga-7&_fields=id,slug`, { headers: h });
      const pgData = dnaPg.ok ? await dnaPg.json() : [];
      if (pgData.length) console.log(`  Found as page: ID ${pgData[0].id}`);
      else console.log('  Not found — may already be trashed');
    }
  }

  // ============================================================
  // SECTION 3: Create redirects + trash all duplicates
  // ============================================================
  console.log('%c[3] Creating redirects + trashing duplicate posts...', 'color:#4CAF50;font-weight:bold');

  for (const item of redirectMap) {
    const { id, from, to } = item;

    // Create redirect if we have from/to
    if (from && to) {
      const ok = await createRedirect(from, `${origin}${to}`);
      if (ok) {
        console.log(`  ✅ 301: ${from} → ${to}`);
        redirected.push({ from, to });
      } else {
        console.log(`  ⚠️  Redirect API unavailable: ${from} → ${to}`);
        errors.push({ id, issue: 'redirect-manual-needed', from, to });
      }
      await sleep(150);
    }

    // Trash the post
    if (id) {
      const trashR = await fetch(`${wpApi}/posts/${id}`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ status: 'trash' })
      });
      if (trashR.ok) {
        console.log(`  🗑  Trashed post [${id}]${from ? ' ' + from : ''}`);
        trashed.push(id);
      } else {
        const errTxt = await trashR.text();
        console.error(`  ❌ Trash failed [${id}]: ${trashR.status} ${errTxt.slice(0,80)}`);
        errors.push({ id, issue: 'trash-failed', status: trashR.status });
      }
      await sleep(150);
    }
  }

  // ============================================================
  // SECTION 4: Fix 5 duplicate meta description tags (POSTS endpoint)
  // ============================================================
  console.log('%c[4] Fixing duplicate meta descriptions on posts 1171–1175...', 'color:#4CAF50;font-weight:bold');

  const dupPostIds = [1171, 1172, 1173, 1174, 1175];

  for (const pid of dupPostIds) {
    // Fetch as POST (not page)
    const r = await fetch(`${wpApi}/posts/${pid}?context=edit`, { headers: h });
    if (!r.ok) {
      console.log(`  ⚠️  Post ${pid} not found (${r.status}) — may be trashed or a page`);
      continue;
    }
    const data = await r.json();
    const epSettings = data.meta?._elementor_page_settings;

    if (epSettings) {
      try {
        const settings = JSON.parse(epSettings);
        if (settings.description) {
          const original = settings.description;
          delete settings.description;
          const patch = await fetch(`${wpApi}/posts/${pid}`, {
            method: 'POST', headers: h,
            body: JSON.stringify({ meta: { _elementor_page_settings: JSON.stringify(settings) } })
          });
          if (patch.ok) {
            console.log(`  ✅ Cleared Elementor description on post [${pid}]: "${original.slice(0,60)}"`);
          } else {
            console.error(`  ❌ Post ${pid} save failed: ${patch.status}`);
          }
        } else {
          console.log(`  ℹ️  Post ${pid}: no description in Elementor page settings`);
          // Check if there's a yoast/other plugin meta description
          const allMeta = Object.keys(data.meta || {});
          const descKeys = allMeta.filter(k => k.includes('description') || k.includes('metadesc'));
          console.log(`       Meta keys with 'description': ${descKeys.join(', ') || 'none'}`);
        }
      } catch(e) {
        console.log(`  ℹ️  Post ${pid}: Elementor settings is not JSON or empty`);
      }
    } else {
      console.log(`  ℹ️  Post ${pid}: no Elementor page settings found`);
      const allMeta = Object.keys(data.meta || {});
      console.log(`       Available meta keys: ${allMeta.slice(0,8).join(', ')}`);
    }
    await sleep(150);
  }

  // ============================================================
  // SECTION 5: Find /services/ in Elementor Theme Builder templates
  // ============================================================
  console.log('%c[5] Searching Elementor Theme Builder templates for /services/...', 'color:#4CAF50;font-weight:bold');

  // Elementor templates are stored as CPT 'elementor_library'
  const tmplR = await fetch(
    `${wpApi}/elementor_library?per_page=50&_fields=id,slug,title,meta&context=edit`,
    { headers: h }
  );

  if (tmplR.ok) {
    const templates = await tmplR.json();
    console.log(`  Found ${templates.length} Elementor templates`);

    for (const tmpl of templates) {
      const elData = tmpl.meta?._elementor_data || '';
      if (elData && elData.includes('/services/')) {
        console.log(`  ⚠️  FOUND /services/ in template [${tmpl.id}]: "${tmpl.title?.rendered || tmpl.slug}"`);

        // Fix it
        const fixed = elData.split('/services/').join('/mobile-phlebotomy-services-atlanta/');
        const patch = await fetch(`${wpApi}/elementor_library/${tmpl.id}`, {
          method: 'POST', headers: h,
          body: JSON.stringify({ meta: { _elementor_data: fixed } })
        });
        if (patch.ok) {
          console.log(`  ✅ Fixed /services/ in template [${tmpl.id}]`);
        } else {
          console.log(`  ❌ Could not save template [${tmpl.id}]: ${patch.status}`);
          console.log(`     Manual fix: Elementor → Templates → "${tmpl.title?.rendered}" → edit the nav link`);
        }
      }
    }
  } else {
    console.log(`  ℹ️  elementor_library CPT not accessible (${tmplR.status})`);
    console.log('  Manual: Elementor → Templates → Theme Builder → Header/Nav → edit /services/ link');
  }

  // ============================================================
  // SECTION 6: Exclude Page ID 23 from sitemap (homepage duplicate)
  // ============================================================
  console.log('%c[6] Checking Rank Math sitemap settings...', 'color:#4CAF50;font-weight:bold');

  const smSettings = await fetch(`${rmApi}/updateSettings`, {
    method: 'POST', headers: h,
    body: JSON.stringify({
      sitemap: {
        exclude_posts: '23'
      }
    })
  });
  console.log('  Sitemap exclude page 23 status:', smSettings.status, smSettings.ok ? '✅' : '(needs manual Rank Math UI)');

  // ============================================================
  // SUMMARY
  // ============================================================
  console.log('%c\n══════════ RESULTS ══════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c🗑  Posts trashed:      ${trashed.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c🔀 Redirects created:  ${redirected.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c⚠️  Manual needed:      ${errors.length}`, 'color:#FF9800;font-weight:bold');
  console.log('\nTrashed IDs:', trashed);
  if (redirected.length) console.log('Redirects:', redirected);
  if (errors.length) {
    console.log('\nManual redirects to add in Rank Math → Redirections:');
    errors.filter(e => e.issue === 'redirect-manual-needed').forEach(e => {
      console.log(`  ${e.from}  →  ${e.to}`);
    });
  }
  console.log('%cDone. Paste results back to Claude.', 'color:#2196F3;font-weight:bold');
})();
