/**
 * Fastrak Mobile Lab — Blog Post Internal Link Injection (May 2026)
 *
 * Addresses the orphan page problem: blog posts lack contextual links to
 * city and service landing pages, leaving those pages starved of internal
 * link equity.
 *
 * What this script does:
 *   - Appends a "Service Area" CTA section to each of the 24 blog posts,
 *     containing a contextual anchor-text link to the most relevant city
 *     or service landing page.
 *   - Uses keyword-specific anchor text (not generic "click here").
 *   - Skips any post that already contains the target link.
 *   - Also adds a secondary link to the Gwinnett County hub page for posts
 *     covering broader service areas.
 *
 * RUN: Paste into wp-admin browser console (any wp-admin page).
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep  = ms => new Promise(r => setTimeout(r, ms));

  const GWINNETT_HUB = '/mobile-phlebotomy-gwinnett-county-ga/';

  const report = { linked: [], skipped: [], errors: [] };

  // ── Blog post → city/service page link map ───────────────────────────────
  // Format: { postId, primaryLink: {slug, anchor}, secondaryLink: {slug, anchor} | null }
  //
  // primaryLink   = the most specific city/service page for this post's topic
  // secondaryLink = Gwinnett hub (added for posts that don't already link there)
  const linkMap = [
    {
      postId: 1171,
      topic:  'Mobile Phlebotomy in Snellville, GA',
      primary:   { slug: '/mobile-phlebotomy-snellville-ga/',           anchor: 'mobile phlebotomy services in Snellville, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy throughout Gwinnett County' }
    },
    {
      postId: 1172,
      topic:  'On-Site Drug Testing for Gwinnett County Businesses',
      primary:   { slug: '/mobile-drug-testing-gwinnett-county-ga/',    anchor: 'on-site drug testing in Gwinnett County' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'mobile lab services across Gwinnett County' }
    },
    {
      postId: 1173,
      topic:  'Mobile Blood Draw for Seniors in Lawrenceville, GA',
      primary:   { slug: '/mobile-phlebotomy-lawrenceville-ga/',        anchor: 'mobile blood draw services in Lawrenceville, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy throughout Gwinnett County' }
    },
    {
      postId: 1174,
      topic:  'Paternity DNA Testing in Norcross, GA',
      primary:   { slug: '/dna-testing-gwinnett-county-ga/',            anchor: 'DNA and paternity testing in Gwinnett County' },
      secondary: { slug: '/mobile-phlebotomy-norcross-ga/',             anchor: 'on-site lab services in Norcross, GA' }
    },
    {
      postId: 1175,
      topic:  'Mobile Lab Services in Tucker and Stone Mountain, GA',
      primary:   { slug: '/mobile-phlebotomy-tucker-ga/',               anchor: 'mobile lab services in Tucker, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy across Gwinnett County' }
    },
    {
      postId: 1176,
      topic:  'Corporate Wellness Blood Panels for Duluth, GA Employers',
      primary:   { slug: '/mobile-phlebotomy-duluth-ga/',               anchor: 'corporate wellness blood draws in Duluth, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'on-site corporate health services in Gwinnett County' }
    },
    {
      postId: 1177,
      topic:  'How Mobile Phlebotomy Works: A Complete Patient Guide',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy services in Gwinnett County' },
      secondary: null
    },
    {
      postId: 1178,
      topic:  'DOT Drug Testing in Gwinnett County',
      primary:   { slug: '/mobile-drug-testing-gwinnett-county-ga/',    anchor: 'DOT drug testing services in Gwinnett County, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'mobile lab services throughout Gwinnett County' }
    },
    {
      postId: 1179,
      topic:  'Mobile Blood Collection for Assisted Living in Conyers, GA',
      primary:   { slug: '/mobile-phlebotomy-conyers-ga/',              anchor: 'mobile blood collection in Conyers, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'on-site lab services across the greater Atlanta area' }
    },
    {
      postId: 1186,
      topic:  'Specimen Integrity and Chain of Custody: Why It Matters',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'certified mobile phlebotomy in Gwinnett County' },
      secondary: null
    },
    {
      postId: 1188,
      topic:  'Home Blood Draw Services in Lithonia and DeKalb County',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile blood draw services serving DeKalb and Gwinnett County' },
      secondary: null
    },
    {
      postId: 1189,
      topic:  'DNA Testing for Immigration in Gwinnett County, GA',
      primary:   { slug: '/dna-testing-gwinnett-county-ga/',            anchor: 'immigration DNA testing in Gwinnett County, GA' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'mobile lab services throughout Gwinnett County' }
    },
    {
      postId: 1191,
      topic:  'Workplace Drug Testing Compliance in Georgia: 2026 Guide',
      primary:   { slug: '/mobile-drug-testing-gwinnett-county-ga/',    anchor: 'mobile workplace drug testing in Gwinnett County' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'on-site occupational health services in Gwinnett County' }
    },
    {
      postId: 1196,
      topic:  'Mobile Phlebotomy for Elderly Patients: Clinical Benefits',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy for elderly patients in Gwinnett County' },
      secondary: null
    },
    {
      postId: 1197,
      topic:  'Lab Requisition Process for Referring Physicians in Atlanta',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile specimen collection for referring physicians in Metro Atlanta' },
      secondary: null
    },
    {
      postId: 1198,
      topic:  'Same-Day Blood Draw in Suwanee and Buford, GA',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'same-day mobile blood draws in Gwinnett County' },
      secondary: null
    },
    {
      postId: 1199,
      topic:  'Mobile Drug Testing for Construction Sites in Gwinnett County',
      primary:   { slug: '/mobile-drug-testing-gwinnett-county-ga/',    anchor: 'mobile drug testing for construction sites in Gwinnett County' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'on-site occupational health services in Gwinnett County' }
    },
    {
      postId: 1200,
      topic:  'How Senior Living Facilities Benefit from On-Site Lab Services',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'recurring on-site lab services for senior living facilities' },
      secondary: null
    },
    {
      postId: 1201,
      topic:  'Comprehensive Health Panels for Johns Creek and Alpharetta',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile blood draws serving Johns Creek, Alpharetta, and Gwinnett County' },
      secondary: null
    },
    {
      postId: 1202,
      topic:  'Understanding Your Lab Results: A Plain-Language Guide',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy and specimen collection in Gwinnett County' },
      secondary: null
    },
    {
      postId: 1207,
      topic:  'Pre-Employment Drug Screening in Loganville and Grayson, GA',
      primary:   { slug: '/mobile-drug-testing-gwinnett-county-ga/',    anchor: 'mobile pre-employment drug screening in Gwinnett County' },
      secondary: { slug: GWINNETT_HUB,                                  anchor: 'on-site lab services throughout Gwinnett County' }
    },
    {
      postId: 1208,
      topic:  'Mobile Phlebotomy vs. Lab Visit: Which Is Right for You?',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile phlebotomy services in Gwinnett County, GA' },
      secondary: null
    },
    {
      postId: 1209,
      topic:  'Venipuncture Best Practices: What Defines a Quality Blood Draw',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'certified mobile venipuncture in Gwinnett County' },
      secondary: null
    },
    {
      postId: 1210,
      topic:  'Fastrak Mobile Lab: Serving Gwinnett, DeKalb, and Rockdale Counties',
      primary:   { slug: GWINNETT_HUB,                                  anchor: 'mobile lab services across Gwinnett, DeKalb, and Rockdale Counties' },
      secondary: null
    }
  ];

  // ── Build CTA HTML block ──────────────────────────────────────────────────
  function buildCtaBlock(entry) {
    const primaryHref    = `${origin}${entry.primary.slug}`;
    const primaryText    = entry.primary.anchor;

    let ctaHtml;
    if (entry.secondary) {
      const secondaryHref = `${origin}${entry.secondary.slug}`;
      const secondaryText = entry.secondary.anchor;
      ctaHtml = `
<div class="fastrak-service-area-cta" style="border-top:2px solid #0a3d62;margin-top:2em;padding-top:1.2em;">
<p><strong>Schedule Your Appointment</strong><br>
FASTRAK Mobile Lab provides <a href="${primaryHref}">${primaryText}</a> and ${
  entry.secondary.slug === GWINNETT_HUB
    ? `<a href="${secondaryHref}">${secondaryText}</a>`
    : `<a href="${secondaryHref}">${secondaryText}</a>`
}. Contact us for same-day and next-day availability.</p>
</div>`;
    } else {
      ctaHtml = `
<div class="fastrak-service-area-cta" style="border-top:2px solid #0a3d62;margin-top:2em;padding-top:1.2em;">
<p><strong>Schedule Your Appointment</strong><br>
FASTRAK Mobile Lab offers <a href="${primaryHref}">${primaryText}</a>. Contact us for same-day and next-day availability.</p>
</div>`;
    }
    return ctaHtml.trim();
  }

  // ════════════════════════════════════════════════════════════════════════
  // MAIN — Iterate posts and append CTA blocks
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c[1] Adding internal link CTA blocks to 24 blog posts...', 'color:#4CAF50;font-weight:bold');

  for (const entry of linkMap) {
    const getR = await fetch(`${wpApi}/posts/${entry.postId}?context=edit`, { headers: h });
    if (!getR.ok) {
      report.errors.push(`GET failed for post ${entry.postId}: ${getR.status}`);
      console.warn(`  ✖ Could not fetch post ${entry.postId}`);
      await sleep(200);
      continue;
    }
    const post = await getR.json();
    const raw  = (post.content && post.content.raw) || '';

    // Skip if primary link already present
    if (raw.includes(entry.primary.slug)) {
      report.skipped.push(entry.postId);
      console.log(`  [skip] Post ${entry.postId} — "${entry.topic.slice(0,50)}" already links to ${entry.primary.slug}`);
      await sleep(100);
      continue;
    }

    const ctaBlock   = buildCtaBlock(entry);
    const newContent = raw + '\n<!-- wp:html -->\n' + ctaBlock + '\n<!-- /wp:html -->';

    const putR = await fetch(`${wpApi}/posts/${entry.postId}`, {
      method: 'PUT', headers: h,
      body: JSON.stringify({ content: newContent })
    });

    if (putR.ok) {
      report.linked.push({ id: entry.postId, topic: entry.topic, linkedTo: entry.primary.slug });
      console.log(`  ✔ Post ${entry.postId} — "${entry.topic.slice(0,50)}" → ${entry.primary.slug}`);
    } else {
      const errTxt = await putR.text();
      report.errors.push(`PUT failed for post ${entry.postId}: ${putR.status} — ${errTxt.slice(0,100)}`);
      console.warn(`  ✖ Post ${entry.postId} update failed: ${putR.status}`);
    }
    await sleep(350);
  }

  // ════════════════════════════════════════════════════════════════════════
  // SUMMARY
  // ════════════════════════════════════════════════════════════════════════
  console.log('%c\n══ INTERNAL LINK INJECTION SUMMARY ══', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`Posts updated:    ${report.linked.length}`);
  console.log(`Posts skipped:    ${report.skipped.length} (links already present)`);
  console.log(`Errors:           ${report.errors.length}`);

  if (report.linked.length) {
    console.log('\nLinks added:');
    report.linked.forEach(r => console.log(`  Post ${r.id} → ${r.linkedTo}`));
  }
  if (report.errors.length) {
    console.warn('\nErrors:');
    report.errors.forEach(e => console.warn('  ✖', e));
  }

  console.log('\n%cNEXT STEPS:', 'color:#FF9800;font-weight:bold');
  console.log('1. Verify a few posts in WP → Posts → Edit to confirm CTA block appeared.');
  console.log('2. Run Ahrefs Site Audit → Internal pages → re-check orphan page count.');
  console.log('3. Consider adding contextual inline links within post body text as well (manual).');
  console.log('4. Re-submit updated posts to Google Search Console → URL Inspection.');

  console.log('%c\nDone.', 'color:#4CAF50;font-weight:bold');
})();
