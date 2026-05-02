/**
 * Fastrak Mobile Lab — Create 301 Redirects + Fix Duplicate Meta (May 2, 2026)
 * Using correct Rank Math updateRedirection format discovered in section 6:
 *   objectID (post ID), objectType, hasRedirect, redirectionUrl, redirectionType
 * Also diagnoses duplicate meta description source on posts 1171-1175.
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const created = [], failed = [], metaFixed = [];

  // Redirect map: post ID → canonical URL
  const redirectMap = [
    { id: 981,  to: '/legal-chain-of-custody-dna-testing-gwinnett-county-law-support/' },
    { id: 955,  to: '/discreet-mobile-infidelity-dna-testing-private-labs-serving-gwinnett-county/' },
    { id: 954,  to: '/mobile-dot-physicals-for-cdl-drivers-same-day-appointments-in-norcross/' },
    { id: 953,  to: '/concierge-mobile-blood-draws-professional-phlebotomy-at-your-atlanta-home/' },
    { id: 952,  to: '/mobile-respiratory-fit-testing-osha-compliance-for-georgia-construction/' },
    { id: 951,  to: '/onsite-background-checks-fingerprinting-for-atlanta-healthcare-staffing/' },
    { id: 950,  to: '/mobile-gender-reveal-dna-testing-early-clinical-results-in-lawrenceville/' },
    { id: 949,  to: '/24-7-mobile-post-accident-breathalyzer-drug-screening-in-metro-atlanta/' },
    { id: 948,  to: '/legal-admissibility-mobile-dna-paternity-testing-for-georgia-court-cases/' },
    { id: 947,  to: '/mobile-dot-drug-testing-for-fleet-managers-compliance-made-easy-in-gwinnett/' },
    { id: 946,  to: '/onsite-corporate-flu-wellness-clinics-mobile-immunizations-in-atlanta/' },
    { id: 916,  to: '/the-difference-between-home-dna-kits-and-legal-paternity-tests/' },
    { id: 915,  to: '/aabb-accredited-dna-testing-for-immigration-what-you-need-to-know/' },
    { id: 902,  to: '/the-difference-between-home-dna-kits-and-legal-paternity-tests/' },
    { id: 901,  to: '/non-invasive-prenatal-paternity-testing-nipp-safe-and-accurate/' },
  ];

  // ── SECTION 1: Create per-post 301 redirects via Rank Math ──────────────
  console.log('%c[1] Creating per-post 301 redirects via Rank Math updateRedirection...', 'color:#4CAF50;font-weight:bold');

  for (const item of redirectMap) {
    const r = await fetch(`${rmApi}/updateRedirection`, {
      method: 'POST', headers: h,
      body: JSON.stringify({
        objectID:       item.id,
        objectType:     'post',
        hasRedirect:    true,
        redirectionUrl:  `${origin}${item.to}`,
        redirectionType: '301'
      })
    });
    const txt = await r.text();
    if (r.ok) {
      console.log(`  ✅ [${item.id}] → ${item.to}`);
      created.push({ id: item.id, to: item.to });
    } else {
      console.log(`  ❌ [${item.id}] ${r.status}: ${txt.slice(0, 100)}`);
      failed.push({ id: item.id, to: item.to, error: txt.slice(0, 80) });
    }
    await sleep(150);
  }
  console.log(`  Created: ${created.length} | Failed: ${failed.length}`);

  // ── SECTION 2: Try Rank Math CSV import for any failed redirects ─────────
  if (failed.length > 0) {
    console.log('%c[2] Trying CSV import for failed redirects...', 'color:#FF9800;font-weight:bold');

    // Build CSV: source,destination,type,status
    const csvLines = ['source,destination,type,status'];
    for (const item of failed) {
      // Get the source URL from the trashed post slug
      const slug = redirectMap.find(r => r.id === item.id);
      // We need to look up the post slug — fetch from trash
      const pr = await fetch(`${wpApi}/posts/${item.id}?context=edit&status=trash`, { headers: h });
      if (pr.ok) {
        const pd = await pr.json();
        csvLines.push(`/${pd.slug}/,${origin}${item.to},301,active`);
      }
      await sleep(100);
    }

    const csvContent = csvLines.join('\n');
    console.log('  CSV to import:', csvContent);

    // Try importCSV endpoint
    const importR = await fetch(`${rmApi}/importCSV`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ csv: csvContent })
    });
    const importTxt = await importR.text();
    console.log('  CSV import status:', importR.status, importTxt.slice(0, 150));
  } else {
    console.log('%c[2] All redirects created — CSV import not needed.', 'color:#4CAF50;font-weight:bold');
  }

  // ── SECTION 3: Diagnose duplicate meta source on posts 1171-1175 ─────────
  console.log('%c[3] Diagnosing duplicate meta description source...', 'color:#FF9800;font-weight:bold');

  // The v3 trim updated rank_math_description. The second tag has the OLD (pre-trim) version.
  // Source candidates: _yoast_wpseo_metadesc, rank_math_description (double output), excerpt

  for (const pid of [1171, 1172, 1173]) {
    // Fetch ALL post meta via context=edit + all fields
    const r = await fetch(`${wpApi}/posts/${pid}?context=edit`, { headers: h });
    if (!r.ok) { console.log(`  Post ${pid}: ${r.status}`); continue; }
    const data = await r.json();
    const meta = data.meta || {};

    console.log(`  Post ${pid} (${data.slug?.slice(0,40)}):`);
    console.log(`    rank_math_description: "${(meta.rank_math_description || '').slice(0,80)}"`);
    console.log(`    _yoast_wpseo_metadesc: "${(meta._yoast_wpseo_metadesc || '').slice(0,80)}"`);
    console.log(`    excerpt: "${(data.excerpt?.raw || '').slice(0,80)}"`);

    // Check all meta keys for anything containing 'description'
    const descKeys = Object.entries(meta).filter(([k]) =>
      k.toLowerCase().includes('desc') || k.toLowerCase().includes('meta')
    );
    if (descKeys.length > 0) {
      console.log(`    SEO-related meta fields:`);
      descKeys.forEach(([k, v]) => console.log(`      ${k}: "${String(v).slice(0,60)}"`));
    }
    await sleep(100);
  }

  // ── SECTION 4: Check Elementor single post template for meta output ───────
  console.log('%c[4] Checking Elementor single post template for meta description...', 'color:#FF9800;font-weight:bold');

  const tmplR = await fetch(
    `${wpApi}/elementor_library?per_page=20&context=edit&_fields=id,slug,title,meta`,
    { headers: h }
  );
  if (tmplR.ok) {
    const templates = await tmplR.json();
    for (const t of templates) {
      const title = t.title?.rendered || t.slug;
      const elData = t.meta?._elementor_data || '';
      const hasMeta = elData.includes('meta_description') || elData.includes('"description"');
      const hasServices = elData.includes('/services/');
      console.log(`  Template [${t.id}] "${title}": meta=${hasMeta}, /services/=${hasServices}`);
      if (hasServices) {
        console.log(`    ⚠️  Found /services/ — fixing...`);
        const fixed = elData.split('/services/').join('/mobile-phlebotomy-services-atlanta/');
        const patch = await fetch(`${wpApi}/elementor_library/${t.id}`, {
          method: 'POST', headers: h,
          body: JSON.stringify({ meta: { _elementor_data: fixed } })
        });
        console.log(`    Patch: ${patch.status} ${patch.ok ? '✅' : '❌'}`);
      }
    }
  }

  // ── SECTION 5: Check WPCode snippets for duplicate meta or /services/ ─────
  console.log('%c[5] Checking WPCode snippets...', 'color:#FF9800;font-weight:bold');

  const codeR = await fetch(`${wpApi}/wpcode?per_page=50&_fields=id,title,content`, { headers: h });
  if (codeR.ok) {
    const snippets = await codeR.json();
    console.log(`  Found ${snippets.length} WPCode snippets`);
    for (const s of snippets) {
      const code = s.content?.raw || '';
      if (code.includes('meta') && code.includes('description')) {
        console.log(`  ⚠️  Snippet [${s.id}] "${s.title?.rendered}" contains meta description code`);
        console.log(`      ${code.slice(0, 150)}`);
      }
      if (code.includes('/services/')) {
        console.log(`  ⚠️  Snippet [${s.id}] contains /services/ link`);
      }
    }
  } else {
    console.log(`  WPCode CPT: ${codeR.status}`);
  }

  // ── SUMMARY ────────────────────────────────────────────────────────────────
  console.log('%c\n══════════ RESULTS ══════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c🔀 Redirects created: ${created.length}/15`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c⚠️  Failed/manual:    ${failed.length}`,     'color:#FF9800;font-weight:bold');
  if (created.length) console.table(created);
  if (failed.length) {
    console.log('\nStill needs manual entry in Rank Math → Redirections:');
    failed.forEach(f => console.log(`  ${f.id}: → ${f.to}`));
  }
  console.log('%cDone. Paste results back to Claude.', 'color:#2196F3;font-weight:bold');
})();
