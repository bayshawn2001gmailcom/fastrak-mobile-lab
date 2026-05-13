/**
 * Fastrak Mobile Lab — Schema Fix Script (May 2026)
 *
 * Addresses the 14 schema validation errors + missing schema coverage:
 *   1. Add FAQ schema to 4 remaining city pages (Snellville, Gwinnett Hub,
 *      Drug Testing Gwinnett, DNA Testing Gwinnett)
 *   2. Fix LocalBusiness/MedicalBusiness schema on homepage (correct phone
 *      format, service area, required fields)
 *   3. Add BreadcrumbList schema to all 9 city/service pages
 *
 * RUN: Paste into wp-admin browser console (any wp-admin page).
 * REQUIRES: Rank Math PRO active. Phone/GBP URL must be filled in below.
 *
 * BEFORE RUNNING — fill in these two constants:
 *   PHONE_E164 — your number in E.164 format, e.g. "+17705551234"
 *   GBP_URL    — your Google Business Profile URL
 */
(async () => {
  // ── USER CONFIG — fill these in before running ──────────────────────────
  const PHONE_E164 = '+16785625244';           // (678) 562-5244
  const GBP_URL    = 'https://g.page/fastrak-mobile-lab'; // ← replace with real GBP URL if different
  // ────────────────────────────────────────────────────────────────────────

  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const results = { faqAdded: [], breadcrumbAdded: [], localBizFixed: [], errors: [] };

  // ── Helper: set Rank Math meta fields ───────────────────────────────────
  async function rmMeta(id, type, fields) {
    const r = await fetch(`${rmApi}/updateMeta`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ objectID: id, objectType: type, meta: fields })
    });
    const txt = await r.text();
    return { ok: r.ok, status: r.status, body: txt.slice(0, 200) };
  }

  // ── Helper: inject raw JSON-LD block into post content (Elementor-safe) ─
  // Appends a <!-- wp:html --> block so it renders outside Elementor's canvas.
  // Rank Math schema is preferred; this is a secondary safety net.
  async function injectJsonLd(postId, postType, label, schemaObj) {
    const getR  = await fetch(`${wpApi}/${postType}/${postId}?context=edit`, { headers: h });
    if (!getR.ok) { results.errors.push(`injectJsonLd: GET ${postId} → ${getR.status}`); return false; }
    const post  = await getR.json();
    const raw   = (post.content && post.content.raw) || '';

    const tag   = `<!-- FASTRAK_SCHEMA_${label.toUpperCase()} -->`;
    if (raw.includes(tag)) { console.log(`  [skip] ${label} JSON-LD already present on ${postId}`); return true; }

    const block = `\n${tag}\n<!-- wp:html -->\n<script type="application/ld+json">\n${JSON.stringify(schemaObj, null, 2)}\n</script>\n<!-- /wp:html -->`;

    const putR  = await fetch(`${wpApi}/${postType}/${postId}`, {
      method: 'PUT', headers: h,
      body: JSON.stringify({ content: raw + block })
    });
    return putR.ok;
  }

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 1 — FAQ Schema on 4 remaining city/service pages
  // Pages that already have FAQ: Duluth(1250), Lawrenceville(1256),
  //   Norcross(1258), Tucker(1260), Conyers(1261)
  // Pages that NEED FAQ: Snellville(1248), Gwinnett Hub(1249),
  //   Drug Testing(1262), DNA Testing(1263)
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[1] Adding FAQ schema to 4 remaining city/service pages...', 'color:#4CAF50;font-weight:bold');

  const faqPages = [
    {
      id: 1248,
      name: 'Snellville GA',
      questions: [
        {
          question: 'Does FASTRAK Mobile Lab provide phlebotomy services in Snellville, GA?',
          answer:   'Yes. FASTRAK Mobile Lab provides certified mobile phlebotomy and specimen collection throughout Snellville, GA. A licensed phlebotomist travels to your home, workplace, or senior living facility — no clinic visit required.'
        },
        {
          question: 'What blood tests can be drawn at home in Snellville, GA?',
          answer:   'Our Snellville phlebotomists collect specimens for routine blood panels, metabolic panels, CBC, lipid profiles, HbA1c, TSH, hormone levels, and all physician-ordered lab work. Specimens are transported to Quest Diagnostics or LabCorp under full chain-of-custody protocol.'
        },
        {
          question: 'How do I schedule a mobile blood draw in Snellville?',
          answer:   'Contact FASTRAK Mobile Lab to book a same-day or next-day appointment in Snellville. Have your physician\'s requisition form and insurance card ready at the time of scheduling.'
        },
        {
          question: 'Is mobile phlebotomy covered by insurance in Georgia?',
          answer:   'Coverage for mobile phlebotomy varies by plan. FASTRAK Mobile Lab works with most major insurance providers. We recommend verifying mobile specimen collection benefits with your insurer before your appointment.'
        }
      ]
    },
    {
      id: 1249,
      name: 'Gwinnett County Hub',
      questions: [
        {
          question: 'Which cities in Gwinnett County does FASTRAK Mobile Lab serve?',
          answer:   'FASTRAK Mobile Lab covers all of Gwinnett County, including Lawrenceville, Duluth, Norcross, Snellville, Tucker, Buford, Suwanee, Lilburn, Loganville, and surrounding communities. We also serve DeKalb, Rockdale, and Fulton counties.'
        },
        {
          question: 'What mobile lab services are available throughout Gwinnett County?',
          answer:   'We provide mobile phlebotomy and blood draws, DOT and non-DOT drug testing, DNA and paternity testing, pre-employment screening, corporate wellness panels, and on-site lab services for senior living facilities across Gwinnett County, GA.'
        },
        {
          question: 'Can FASTRAK Mobile Lab come to a corporate office in Gwinnett County?',
          answer:   'Yes. FASTRAK offers on-site corporate health services throughout Gwinnett County, including pre-employment drug screening, DOT compliance testing, group wellness blood draws, and occupational health panels. Contact us to schedule a group appointment at your facility.'
        },
        {
          question: 'How quickly can FASTRAK reach my Gwinnett County location?',
          answer:   'FASTRAK Mobile Lab operates daily throughout Gwinnett County with same-day and next-day availability. Our route density scheduling ensures efficient coverage across all Gwinnett County cities and ZIP codes.'
        }
      ]
    },
    {
      id: 1262,
      name: 'Drug Testing Gwinnett County',
      questions: [
        {
          question: 'Does FASTRAK Mobile Lab offer DOT drug testing in Gwinnett County?',
          answer:   'Yes. FASTRAK provides DOT-compliant mobile drug testing throughout Gwinnett County. Services include 5-panel and 10-panel urine drug screens, breath alcohol testing (BAT), and chain-of-custody collection for FMCSA, FAA, PHMSA, and FRA-regulated employers.'
        },
        {
          question: 'Can on-site drug testing be performed at our Gwinnett County workplace?',
          answer:   'Yes. FASTRAK Mobile Lab brings certified collectors directly to your Gwinnett County facility. On-site testing eliminates employee downtime, ensures chain-of-custody compliance, and supports reasonable-suspicion and post-accident testing requirements.'
        },
        {
          question: 'What is chain of custody in mobile drug testing?',
          answer:   'Chain of custody (COC) is the federally mandated documentation process that tracks a specimen from collection through laboratory analysis and MRO review. FASTRAK uses compliant COC forms for all collections, ensuring results are legally defensible for employers and regulatory agencies.'
        },
        {
          question: 'How do we schedule pre-employment drug testing in Gwinnett County?',
          answer:   'Contact FASTRAK Mobile Lab to arrange pre-employment drug screening at your Gwinnett County location. We accommodate individual candidates and group screenings, with same-day and next-day availability.'
        }
      ]
    },
    {
      id: 1263,
      name: 'DNA Testing Gwinnett County',
      questions: [
        {
          question: 'Is mobile DNA testing available in Gwinnett County, GA?',
          answer:   'Yes. FASTRAK Mobile Lab provides certified mobile DNA testing throughout Gwinnett County. Services include legal paternity testing, AABB-accredited immigration DNA testing, and relationship testing — collected at your home, office, or any designated location.'
        },
        {
          question: 'Are DNA test results from FASTRAK Mobile Lab legally admissible?',
          answer:   'Yes. When collected under FASTRAK\'s chain-of-custody protocol and processed through an AABB-accredited laboratory, results are legally admissible for court proceedings, immigration petitions, child support determinations, and other legal purposes in Georgia.'
        },
        {
          question: 'What is the difference between legal paternity testing and a home DNA kit?',
          answer:   'Legal paternity tests are collected by a certified professional following strict chain-of-custody procedures, making results court-admissible. Home DNA kits are self-administered and are not accepted by courts, USCIS, or Georgia government agencies for any legal purpose.'
        },
        {
          question: 'How long does DNA testing take with FASTRAK Mobile Lab in Gwinnett County?',
          answer:   'Standard DNA results are returned within 3–5 business days after specimen collection. FASTRAK coordinates with AABB-accredited laboratories to ensure accurate, timely results.'
        }
      ]
    }
  ];

  for (const page of faqPages) {
    console.log(`  Processing FAQ for: ${page.name} (ID ${page.id})`);

    // Build FAQ JSON-LD object
    const faqSchema = {
      '@context': 'https://schema.org',
      '@type':    'FAQPage',
      mainEntity: page.questions.map(q => ({
        '@type':        'Question',
        name:           q.question,
        acceptedAnswer: { '@type': 'Answer', text: q.answer }
      }))
    };

    // Approach A: Rank Math PRO FAQ meta fields
    const rmResult = await rmMeta(page.id, 'post', {
      rank_math_rich_snippet:  'faqpage',
      rank_math_faq_questions: JSON.stringify(page.questions.map(q => ({
        question: q.question,
        answer:   q.answer
      })))
    });
    console.log(`    Rank Math updateMeta: ${rmResult.status} — ${rmResult.body.slice(0, 80)}`);

    // Approach B: JSON-LD content injection (backup — works if RM meta fails)
    const injected = await injectJsonLd(page.id, 'pages', `faq_${page.id}`, faqSchema);
    console.log(`    JSON-LD content inject: ${injected ? 'OK' : 'FAILED'}`);

    if (rmResult.ok || injected) {
      results.faqAdded.push(`${page.name} (${page.id})`);
    } else {
      results.errors.push(`FAQ failed on ${page.name} (${page.id})`);
    }
    await sleep(400);
  }

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 2 — LocalBusiness + MedicalBusiness schema on homepage
  // Fixes: invalid phone format, missing areaServed, missing priceRange,
  //   missing openingHours, missing sameAs links.
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[2] Fixing LocalBusiness/MedicalBusiness schema on homepage...', 'color:#4CAF50;font-weight:bold');

  const localBizSchema = {
    '@context': 'https://schema.org',
    '@type':    ['LocalBusiness', 'MedicalBusiness'],
    '@id':      `${origin}/#organization`,
    name:        'FASTRAK Mobile Lab',
    alternateName: 'Fastrak Mobile Lab',
    description: 'Professional mobile phlebotomy and specimen collection service. On-site blood draws, DOT drug testing, DNA testing, and corporate wellness screenings at homes, offices, and senior living facilities in Metro Atlanta.',
    url:         origin + '/',
    telephone:   PHONE_E164,
    image:       `${origin}/wp-content/uploads/fastrak-mobile-lab-logo.png`,
    logo:        `${origin}/wp-content/uploads/fastrak-mobile-lab-logo.png`,
    priceRange:  '$$',
    address: {
      '@type':           'PostalAddress',
      addressLocality:   'Snellville',
      addressRegion:     'GA',
      postalCode:        '30039',
      addressCountry:    'US'
    },
    geo: {
      '@type':       'GeoCircle',
      geoMidpoint: {
        '@type':    'GeoCoordinates',
        latitude:   33.8570,
        longitude: -84.0199
      },
      geoRadius: '48280'
    },
    areaServed: [
      { '@type': 'City',   name: 'Snellville',    containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Lawrenceville', containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Duluth',         containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Norcross',       containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Tucker',         containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Conyers',        containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Buford',         containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Suwanee',        containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'City',   name: 'Lithonia',       containedInPlace: { '@type': 'State', name: 'Georgia' } },
      { '@type': 'County', name: 'Gwinnett County' },
      { '@type': 'County', name: 'DeKalb County'   },
      { '@type': 'County', name: 'Rockdale County' },
      { '@type': 'County', name: 'Fulton County'   }
    ],
    openingHoursSpecification: [
      { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday','Tuesday','Wednesday','Thursday','Friday'], opens: '07:00', closes: '18:00' },
      { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Saturday'], opens: '08:00', closes: '14:00' }
    ],
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name:    'Mobile Lab Services',
      itemListElement: [
        { '@type': 'Offer', itemOffered: { '@type': 'MedicalProcedure', name: 'Mobile Phlebotomy' } },
        { '@type': 'Offer', itemOffered: { '@type': 'MedicalProcedure', name: 'DOT Drug Testing'  } },
        { '@type': 'Offer', itemOffered: { '@type': 'MedicalTest',      name: 'DNA Paternity Testing' } },
        { '@type': 'Offer', itemOffered: { '@type': 'MedicalProcedure', name: 'Corporate Wellness Screening' } },
        { '@type': 'Offer', itemOffered: { '@type': 'MedicalProcedure', name: 'Senior Care Lab Services' } }
      ]
    },
    sameAs: [GBP_URL]
  };

  // Fetch homepage ID (post with type=page and slug=/ or front page)
  const homeR = await fetch(`${wpApi}/pages?slug=home&per_page=5`, { headers: h });
  let homePages = homeR.ok ? await homeR.json() : [];
  // Also try reading the WordPress front page setting
  const settingsR = await fetch(`${origin}/wp-json/wp/v2/settings`, { headers: h });
  let homepageId  = null;
  if (settingsR.ok) {
    const settings = await settingsR.json();
    homepageId = settings.page_on_front || null;
    console.log(`  Front page ID from settings: ${homepageId}`);
  }
  if (!homepageId && homePages.length > 0) {
    homepageId = homePages[0].id;
    console.log(`  Front page ID from slug=home: ${homepageId}`);
  }

  if (homepageId) {
    const injected = await injectJsonLd(homepageId, 'pages', 'localbusiness', localBizSchema);
    console.log(`  LocalBusiness schema injected to homepage (ID ${homepageId}): ${injected ? 'OK' : 'FAILED'}`);
    if (injected) results.localBizFixed.push(`Homepage (${homepageId})`);
    else results.errors.push(`LocalBusiness schema failed on homepage (${homepageId})`);
  } else {
    console.warn('  Could not determine homepage ID — inject LocalBusiness schema manually.');
    results.errors.push('Homepage ID unknown — LocalBusiness schema requires manual injection');
  }
  await sleep(400);

  // ════════════════════════════════════════════════════════════════════════
  // SECTION 3 — BreadcrumbList schema on all 9 city/service pages
  // Hierarchy: Homepage → Gwinnett County Hub → City Page
  // (Drug Testing and DNA Testing branch from Homepage directly)
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[3] Adding BreadcrumbList schema to all 9 city/service pages...', 'color:#4CAF50;font-weight:bold');

  const GWINNETT_HUB_URL = `${origin}/mobile-phlebotomy-gwinnett-county-ga/`;

  const cityPages = [
    { id: 1248, slug: 'mobile-phlebotomy-snellville-ga',            name: 'Mobile Phlebotomy in Snellville, GA',             parent: 'hub' },
    { id: 1249, slug: 'mobile-phlebotomy-gwinnett-county-ga',       name: 'Mobile Phlebotomy in Gwinnett County, GA',        parent: 'home' },
    { id: 1250, slug: 'mobile-phlebotomy-duluth-ga',                 name: 'Mobile Phlebotomy in Duluth, GA',                 parent: 'hub' },
    { id: 1256, slug: 'mobile-phlebotomy-lawrenceville-ga',          name: 'Mobile Phlebotomy in Lawrenceville, GA',          parent: 'hub' },
    { id: 1258, slug: 'mobile-phlebotomy-norcross-ga',               name: 'Mobile Phlebotomy in Norcross, GA',               parent: 'hub' },
    { id: 1260, slug: 'mobile-phlebotomy-tucker-ga',                 name: 'Mobile Phlebotomy in Tucker, GA',                 parent: 'hub' },
    { id: 1261, slug: 'mobile-phlebotomy-conyers-ga',                name: 'Mobile Phlebotomy in Conyers, GA',                parent: 'hub' },
    { id: 1262, slug: 'mobile-drug-testing-gwinnett-county-ga',      name: 'Mobile Drug Testing in Gwinnett County, GA',     parent: 'home' },
    { id: 1263, slug: 'dna-testing-gwinnett-county-ga',              name: 'DNA Testing in Gwinnett County, GA',              parent: 'home' }
  ];

  for (const page of cityPages) {
    const pageUrl = `${origin}/${page.slug}/`;

    let breadcrumbItems;
    if (page.parent === 'hub') {
      breadcrumbItems = [
        { '@type': 'ListItem', position: 1, name: 'Home',                          item: origin + '/' },
        { '@type': 'ListItem', position: 2, name: 'Gwinnett County Service Area',  item: GWINNETT_HUB_URL },
        { '@type': 'ListItem', position: 3, name: page.name,                       item: pageUrl }
      ];
    } else {
      breadcrumbItems = [
        { '@type': 'ListItem', position: 1, name: 'Home',       item: origin + '/' },
        { '@type': 'ListItem', position: 2, name: page.name,    item: pageUrl }
      ];
    }

    const breadcrumbSchema = {
      '@context':    'https://schema.org',
      '@type':       'BreadcrumbList',
      itemListElement: breadcrumbItems
    };

    const injected = await injectJsonLd(page.id, 'pages', `breadcrumb_${page.id}`, breadcrumbSchema);
    console.log(`  BreadcrumbList → ${page.name}: ${injected ? 'OK' : 'FAILED'}`);
    if (injected) results.breadcrumbAdded.push(`${page.name} (${page.id})`);
    else results.errors.push(`BreadcrumbList failed on ${page.name} (${page.id})`);
    await sleep(300);
  }

  // ════════════════════════════════════════════════════════════════════════
  // SUMMARY
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c\n══ SCHEMA FIX SUMMARY ══', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`FAQ schema added:        ${results.faqAdded.length} pages`);
  console.log('  →', results.faqAdded.join(', ') || 'none');
  console.log(`LocalBusiness fixed:     ${results.localBizFixed.length} pages`);
  console.log('  →', results.localBizFixed.join(', ') || 'none');
  console.log(`BreadcrumbList added:    ${results.breadcrumbAdded.length} pages`);
  console.log('  →', results.breadcrumbAdded.join(', ') || 'none');
  if (results.errors.length) {
    console.warn(`Errors (${results.errors.length}):`);
    results.errors.forEach(e => console.warn('  ✖', e));
  }

  console.log('\n%cNEXT STEPS:', 'color:#FF9800;font-weight:bold');
  console.log('1. Replace PHONE_E164 and GBP_URL constants at top of script, then re-run.');
  console.log('2. Validate FAQ pages: https://search.google.com/test/rich-results');
  console.log('3. Validate LocalBusiness schema on homepage: https://search.google.com/test/rich-results');
  console.log('4. Submit updated pages in Google Search Console → URL Inspection → Request Indexing.');

  console.log('%c\nDone.', 'color:#4CAF50;font-weight:bold');
})();
