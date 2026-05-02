/**
 * Fastrak Mobile Lab — Fix Duplicate Meta + Set Descriptions (May 2, 2026)
 * Root cause: rank_math_description empty on posts 1171-1175, so Rank Math
 * falls back to excerpt. A second source also outputs the excerpt → 2 tags.
 * Fix: set rank_math_description explicitly AND clear excerpt.
 */
(async () => {
  const nonce = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi = `${origin}/wp-json/wp/v2`;
  const rmApi = `${origin}/wp-json/rankmath/v1`;
  const h = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // Known descriptions from live page scrape (already verified correct length)
  const postFixes = {
    1171: 'Fastrak Mobile Lab provides certified mobile phlebotomy services in Snellville, GA. Schedule an on-site blood draw at your home or office.',
    1172: 'Fastrak Mobile Lab provides DOT-compliant on-site drug testing for Gwinnett County employers. Fast, certified, chain-of-custody results.',
    1173: 'Fastrak Mobile Lab brings certified mobile blood draw services to seniors in Lawrenceville, GA. No transport needed — we come to you.',
    1174: 'Fastrak Mobile Lab offers legal paternity DNA testing in Norcross, GA. Discreet, AABB-accredited collection with court-admissible results.',
    1175: 'Fastrak Mobile Lab provides mobile lab services across Tucker and Stone Mountain, GA. On-site blood draws, drug testing, and DNA collection.',
  };

  console.log('%c[1] Setting rank_math_description + clearing excerpt on posts 1171-1175...', 'color:#4CAF50;font-weight:bold');

  for (const [idStr, desc] of Object.entries(postFixes)) {
    const id = parseInt(idStr);

    // Set rank_math_description via Rank Math API
    const rmR = await fetch(`${rmApi}/updateMeta`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ objectID: id, objectType: 'post', meta: { rank_math_description: desc } })
    });
    console.log(`  [${id}] updateMeta: ${rmR.status} ${rmR.ok ? '✅' : '❌'}`);

    // Clear excerpt via WP REST API (removes second meta tag source)
    const wpR = await fetch(`${wpApi}/posts/${id}`, {
      method: 'POST', headers: h,
      body: JSON.stringify({ excerpt: '' })
    });
    console.log(`  [${id}] clear excerpt: ${wpR.status} ${wpR.ok ? '✅' : '❌'}`);

    await sleep(200);
  }

  // ── Verify: fetch live HTML and count meta description tags ───────────────
  console.log('%c[2] Verifying fix on posts 1171 + 1172...', 'color:#FF9800;font-weight:bold');

  await sleep(1000); // give server a moment

  for (const pid of [1171, 1172]) {
    const r = await fetch(`${origin}/?p=${pid}`, { cache: 'no-store' });
    const html = await r.text();
    const metas = [...html.matchAll(/<meta[^>]+name=["']description["'][^>]*>/gi)];
    const status = metas.length === 1 ? '✅ FIXED (1 tag)' : `⚠️ Still ${metas.length} tags`;
    console.log(`  Post ${pid}: ${status}`);
    if (metas.length > 1) metas.forEach((m, i) => console.log(`    [${i+1}] ${m[0].slice(0,100)}`));
  }

  console.log('%cDone. Paste results back to Claude.', 'color:#2196F3;font-weight:bold');
})();
