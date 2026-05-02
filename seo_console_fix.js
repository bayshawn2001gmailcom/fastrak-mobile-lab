/**
 * Fastrak Mobile Lab — SEO Console Fix Script (May 2026)
 * Paste this entire script into the wp-admin browser console and press Enter.
 * Fixes: long meta descriptions, missing meta descriptions, redirect body links.
 */

(async () => {
  const nonce = wpApiSettings.nonce;
  const base  = wpApiSettings.root || '/wp-json/';
  const rmApi = `${location.origin}/wp-json/rankmath/v1`;
  const wpApi = `${location.origin}/wp-json/wp/v2`;

  const h = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const results = { fixed: [], skipped: [], errors: [] };

  // ── helpers ──────────────────────────────────────────────────────────────

  function trim(desc, max = 155) {
    if (!desc || desc.length <= max) return null; // null = no change needed
    const t = desc.slice(0, max).replace(/\s+\S*$/, '').replace(/[.,;:]+$/, '');
    return t + '…';
  }

  async function updateRMDesc(id, desc) {
    const r = await fetch(`${rmApi}/updateMeta`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ objectID: id, objectType: 'post', rank_math_description: desc })
    });
    return r.ok;
  }

  async function getAllItems(type) {
    let all = [], page = 1;
    while (true) {
      const r = await fetch(`${wpApi}/${type}?per_page=100&page=${page}&status=publish&context=edit&_fields=id,slug,title,meta,link`, { headers: h });
      if (!r.ok) break;
      const batch = await r.json();
      if (!batch.length) break;
      all.push(...batch);
      page++;
    }
    return all;
  }

  // ── Step 1: Trim meta descriptions > 155 chars ───────────────────────────

  console.log('%c[1] Fetching all pages + posts...', 'color:#4CAF50;font-weight:bold');
  const pages = await getAllItems('pages');
  const posts = await getAllItems('posts');
  const all   = [...pages, ...posts];
  console.log(`    Found ${pages.length} pages + ${posts.length} posts = ${all.length} total`);

  let longFixed = 0, missingFixed = 0;
  for (const item of all) {
    const meta = item.meta || {};
    const desc = meta.rank_math_description || '';
    const slug = (item.slug || '').slice(0, 45);

    // Fix: too long
    const trimmed = trim(desc);
    if (trimmed) {
      const ok = await updateRMDesc(item.id, trimmed);
      if (ok) {
        console.log(`  ✅ TRIMMED [${item.id}] ${slug} (${desc.length}→${trimmed.length} chars)`);
        results.fixed.push({ id: item.id, slug, issue: 'meta-too-long', from: desc.length, to: trimmed.length });
        longFixed++;
      } else {
        results.errors.push({ id: item.id, slug, issue: 'trim-failed' });
      }
    }
    await new Promise(r => setTimeout(r, 120)); // rate limit
  }
  console.log(`%c    Long meta descriptions trimmed: ${longFixed}`, 'color:#4CAF50');

  // ── Step 2: Known pages with missing meta descriptions ───────────────────

  console.log('%c[2] Adding missing meta descriptions...', 'color:#4CAF50;font-weight:bold');

  const autoMeta = {
    23:   'Fastrak Mobile Lab offers professional mobile phlebotomy and specimen collection in Gwinnett County, GA. On-site blood draws at your home, office, or facility.',
    564:  'Mobile phlebotomy and lab services across Atlanta and metro Georgia. On-site blood draws, drug testing, and DNA collection — no clinic visit required.',
    306:  'Answers to your questions about mobile phlebotomy, on-site blood draws, and specimen collection services from Fastrak Mobile Lab in Gwinnett County, GA.',
    395:  'Mobile DNA testing and drug testing in Atlanta, GA. Chain-of-custody specimen collection for legal, employment, and personal use — Fastrak Mobile Lab.',
    856:  'The Fastrak Mobile Lab blog covers mobile phlebotomy, specimen integrity, drug testing compliance, and senior care lab services across Gwinnett County, GA.',
  };

  for (const [idStr, newDesc] of Object.entries(autoMeta)) {
    const id   = parseInt(idStr);
    const item = all.find(x => x.id === id);
    const existing = item?.meta?.rank_math_description || '';

    if (existing && existing.length > 20) {
      console.log(`  ⏭  SKIP [${id}] already has description (${existing.length} chars)`);
      results.skipped.push({ id, issue: 'already-has-desc' });
      continue;
    }

    const ok = await updateRMDesc(id, newDesc);
    if (ok) {
      console.log(`  ✅ SET [${id}] meta description (${newDesc.length} chars)`);
      results.fixed.push({ id, issue: 'meta-missing', chars: newDesc.length });
      missingFixed++;
    } else {
      console.error(`  ❌ FAILED [${id}]`);
      results.errors.push({ id, issue: 'missing-set-failed' });
    }
    await new Promise(r => setTimeout(r, 120));
  }
  console.log(`%c    Missing meta descriptions added: ${missingFixed}`, 'color:#4CAF50');

  // ── Step 3: Fix known body-content redirect links ────────────────────────

  console.log('%c[3] Fixing body-content redirect links...', 'color:#4CAF50;font-weight:bold');

  const redirectFixes = {
    23:  { '/services/': '/mobile-phlebotomy-services-atlanta/' },
    395: { '/mobile-drug-dna-testing-atlanta/': '/mobile-dna-testing-atlanta/' },
  };

  for (const [idStr, replacements] of Object.entries(redirectFixes)) {
    const id = parseInt(idStr);
    const r  = await fetch(`${wpApi}/pages/${id}?context=edit`, { headers: h });
    if (!r.ok) { console.error(`  ❌ Could not fetch page ${id}`); continue; }

    const data    = await r.json();
    let   content = data.content?.raw || '';
    let   changed = false;

    for (const [oldUrl, newUrl] of Object.entries(replacements)) {
      if (content.includes(oldUrl)) {
        content = content.split(oldUrl).join(newUrl);
        console.log(`  ✅ [${id}] replaced "${oldUrl}" → "${newUrl}"`);
        changed = true;
      }
    }

    if (changed) {
      const patch = await fetch(`${wpApi}/pages/${id}`, {
        method: 'POST', headers: h,
        body: JSON.stringify({ content })
      });
      if (!patch.ok) console.error(`  ❌ [${id}] content save failed (${patch.status})`);
      else results.fixed.push({ id, issue: 'redirect-link-fixed' });
    }
    await new Promise(r => setTimeout(r, 200));
  }

  // ── Step 4: Fix dna-testing-services-atlanta-ga-7 redirect notice ─────────

  console.log('%c[4] Checking dna-testing-services-atlanta-ga-7 (noticed in wp-admin)...', 'color:#4CAF50;font-weight:bold');
  // This was shown in the wp-admin SEO notice — needs a 301 redirect
  // Can't create Rank Math redirects via REST API, but flag it clearly
  console.log('  ⚠️  /dna-testing-services-atlanta-ga-7/ needs a 301 redirect in Rank Math → Redirections');
  console.log('      Target: /dna-testing-services-atlanta-ga/');

  // ── Summary ──────────────────────────────────────────────────────────────

  console.log('%c\n════════ RESULTS ════════', 'color:#2196F3;font-weight:bold;font-size:14px');
  console.log(`%c✅ Fixed:   ${results.fixed.length}`, 'color:#4CAF50;font-weight:bold');
  console.log(`%c⏭  Skipped: ${results.skipped.length}`, 'color:#FF9800');
  console.log(`%c❌ Errors:  ${results.errors.length}`, 'color:#f44336');
  console.log('\nFixed items:', results.fixed);
  if (results.errors.length) console.log('Errors:', results.errors);
  console.log('\n%cDone! Copy the results above and paste back to Claude.', 'color:#2196F3;font-weight:bold');

})();
