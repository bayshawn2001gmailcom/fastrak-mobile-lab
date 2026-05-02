/**
 * Fastrak — SEO Debug + Fix Script v2
 * Paste into wp-admin console. Diagnoses API issues then applies fixes.
 */
(async () => {
  const nonce  = wpApiSettings.nonce;
  const origin = location.origin;
  const wpApi  = `${origin}/wp-json/wp/v2`;
  const rmApi  = `${origin}/wp-json/rankmath/v1`;
  const h      = { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' };

  // ── 1. Diagnose Rank Math updateMeta error ────────────────────────────────
  console.log('%c[DIAG] Testing Rank Math updateMeta endpoint...', 'color:#FF9800;font-weight:bold');

  const testRM = await fetch(`${rmApi}/updateMeta`, {
    method: 'POST', headers: h,
    body: JSON.stringify({ objectID: 23, objectType: 'post', rank_math_description: 'TEST - DO NOT SAVE' })
  });
  const rmText = await testRM.text();
  console.log('Rank Math updateMeta status:', testRM.status);
  console.log('Rank Math updateMeta response:', rmText);

  // ── 2. Try standard WP REST meta update (fallback) ───────────────────────
  console.log('%c[DIAG] Testing standard WP meta update on page 23...', 'color:#FF9800;font-weight:bold');

  const testWP = await fetch(`${wpApi}/pages/23`, {
    method: 'POST', headers: h,
    body: JSON.stringify({ meta: { rank_math_description: 'TEST - DO NOT SAVE' } })
  });
  const wpText = await testWP.text();
  console.log('WP meta update status:', testWP.status);
  console.log('WP meta update response:', wpText.slice(0, 300));

  // ── 3. Try Rank Math getHead to see current meta ──────────────────────────
  console.log('%c[DIAG] Testing Rank Math getHead on page 23...', 'color:#FF9800;font-weight:bold');

  const testHead = await fetch(`${rmApi}/getHead?objectID=23&objectType=post`, { headers: h });
  const headData = await testHead.json();
  console.log('getHead status:', testHead.status);
  // count meta description tags
  const headHtml = headData.head || '';
  const descCount = (headHtml.match(/name="description"/g) || []).length;
  console.log('Meta description tags on homepage:', descCount);
  console.log('hasInvalid:', headData.hasInvalid);

  // ── 4. Check available Rank Math endpoints ────────────────────────────────
  console.log('%c[DIAG] Checking Rank Math namespace routes...', 'color:#FF9800;font-weight:bold');

  const routes = await fetch(`${origin}/wp-json/rankmath/v1`, { headers: h });
  if (routes.ok) {
    const rd = await routes.json();
    console.log('Rank Math routes:', Object.keys(rd.routes || {}));
  } else {
    console.log('Routes status:', routes.status);
  }

  // ── 5. Check what meta fields page 23 exposes ────────────────────────────
  console.log('%c[DIAG] Reading page 23 meta fields...', 'color:#FF9800;font-weight:bold');

  const page23 = await fetch(`${wpApi}/pages/23?context=edit`, { headers: h });
  const p23    = await page23.json();
  console.log('Page 23 meta keys:', Object.keys(p23.meta || {}));
  console.log('Page 23 rank_math_description:', p23.meta?.rank_math_description);

})();
