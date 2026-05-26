"""
Redesign mobile-phlebotomy-gwinnett-county-ga/ — modeled on Atlanta Turf Doctor homepage style.
Open editorial layout: prob-list services, connected numbered steps, accordion FAQ.
Brand colors: #0d4a7a (dark blue) / #0db8a5 (teal).
"""
import os, base64, socket, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".env")

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds = base64.b64encode(
    f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
).decode()
HJ = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

PAGE_ID  = 1249
BOOK_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"
PHONE    = "(678) 562-5244"

NEW_CONTENT = f"""<!-- wp:html -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ── reset / hide theme title ─────────────────────────────────── */
.page-id-1249 .entry-title,.page-id-1249 .page-title,
.page-id-1249 h1.entry-title,.page-id-1249 .page-header,
.page-id-1249 .entry-header{{display:none!important}}
.page-id-1249 .entry-content{{padding-top:0!important;margin-top:0!important}}

/* ── base ──────────────────────────────────────────────────────── */
.fml{{box-sizing:border-box;font-family:'Inter',sans-serif;color:#111;line-height:1.65;background:#fff}}
.fml *{{box-sizing:border-box;margin:0;padding:0}}
.fml h1,.fml h2,.fml h3,.fml h4{{font-family:'Montserrat',sans-serif;line-height:1.2;color:inherit}}
.fml a{{text-decoration:none;color:inherit}}

/* ── hero ──────────────────────────────────────────────────────── */
.fml .hero{{background:linear-gradient(135deg,#07304f 0%,#0d4a7a 55%,#0a8c7c 100%);padding:96px 24px 88px;position:relative;overflow:hidden}}
.fml .hero::before{{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}}
.fml .hero-body{{position:relative;z-index:1;max-width:700px;margin:0 auto;text-align:center}}
.fml .hero-pill{{display:inline-block;border:1.5px solid rgba(255,255,255,.35);padding:5px 18px;border-radius:4px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:24px;color:rgba(255,255,255,.9);font-family:'Montserrat',sans-serif}}
.fml .hero h1{{font-size:clamp(2.2rem,5vw,3.5rem);font-weight:800;margin-bottom:20px;color:#fff;line-height:1.15}}
.fml .hero h1 em{{font-style:normal;color:#6ef0e0}}
.fml .hero-sub{{font-size:1.1rem;color:rgba(255,255,255,.88);max-width:560px;margin:0 auto 36px;line-height:1.75}}
.fml .btn-teal{{display:inline-block;background:#0db8a5;color:#fff;padding:16px 40px;border-radius:4px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;transition:background .2s,transform .15s;letter-spacing:.3px;box-shadow:0 4px 20px rgba(13,184,165,.4)}}
.fml .btn-teal:hover{{background:#0aa898;transform:translateY(-2px)}}
.fml .btn-ghost{{display:inline-block;border:2px solid rgba(255,255,255,.5);color:#fff;padding:14px 32px;border-radius:4px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:.97rem;margin-left:14px;transition:border-color .2s}}
.fml .btn-ghost:hover{{border-color:#fff}}
.fml .hero-trust{{display:flex;flex-wrap:wrap;justify-content:center;gap:18px;margin-top:32px}}
.fml .hero-trust span{{font-size:13px;color:rgba(255,255,255,.8);display:flex;align-items:center;gap:7px}}
.fml .hero-trust .ck{{color:#6ef0e0;font-weight:800}}

/* ── stats bar ─────────────────────────────────────────────────── */
.fml .statsbar{{background:#0d4a7a;display:flex;justify-content:center;flex-wrap:wrap}}
.fml .st{{padding:20px 48px;text-align:center;color:#fff;border-right:1px solid rgba(255,255,255,.12)}}
.fml .st:last-child{{border-right:none}}
.fml .st-n{{display:block;font-family:'Montserrat',sans-serif;font-size:1.9rem;font-weight:800;color:#6ef0e0}}
.fml .st-l{{font-size:11px;opacity:.7;letter-spacing:.8px;text-transform:uppercase;margin-top:4px}}

/* ── layout ─────────────────────────────────────────────────────── */
.fml section{{padding:80px 24px}}
.fml .wrap{{max-width:1040px;margin:0 auto}}
.fml .wrap-narrow{{max-width:760px;margin:0 auto}}
.fml .tag{{display:inline-block;color:#0db8a5;font-family:'Montserrat',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;margin-bottom:12px}}
.fml h2{{font-size:clamp(1.8rem,3.8vw,2.7rem);font-weight:800;color:#07304f;margin-bottom:16px}}
.fml .lead{{font-size:1.03rem;color:#444;line-height:1.85;margin-bottom:40px}}
.fml .bg-lt{{background:#f4f8fc}}
.fml .bg-wh{{background:#fff}}

/* ── two-col ────────────────────────────────────────────────────── */
.fml .two-col{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
@media(max-width:720px){{.fml .two-col{{grid-template-columns:1fr}}}}

/* ── service list (prob-list style) ────────────────────────────── */
.fml .svc-list{{list-style:none;display:flex;flex-direction:column;gap:24px}}
.fml .svc-list li{{display:flex;gap:16px;align-items:flex-start}}
.fml .svc-icon{{width:42px;height:42px;min-width:42px;background:#f0f8fc;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.25rem}}
.fml .svc-list strong{{display:block;font-family:'Montserrat',sans-serif;font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:4px}}
.fml .svc-list p{{font-size:.9rem;color:#555;line-height:1.65}}

/* ── diff grid (how it works — connected numbered panels) ────────── */
.fml .diff-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2px;margin-top:48px;border:1px solid #dce8f0;border-radius:4px;overflow:hidden}}
.fml .diff-card{{background:#fff;padding:32px 26px;border-right:1px solid #dce8f0}}
.fml .diff-card:last-child{{border-right:none}}
.fml .diff-num{{font-family:'Montserrat',sans-serif;font-size:2.2rem;font-weight:800;color:#c8dff0;margin-bottom:12px;display:block}}
.fml .diff-card h3{{font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:8px;font-family:'Montserrat',sans-serif}}
.fml .diff-card p{{font-size:.87rem;color:#555;line-height:1.7}}

/* ── areas served ───────────────────────────────────────────────── */
.fml .cities-grid{{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}}
.fml .city-pill{{background:#fff;border:1.5px solid #ccdce8;border-radius:30px;padding:9px 18px;font-size:.9rem;font-weight:600;color:#0d4a7a;display:flex;align-items:center;gap:8px;font-family:'Montserrat',sans-serif}}
.fml .city-pill::before{{content:'';width:7px;height:7px;background:#0db8a5;border-radius:50%;flex-shrink:0}}

/* ── steps ──────────────────────────────────────────────────────── */
.fml .steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:48px;position:relative}}
.fml .steps::before{{content:'';position:absolute;top:27px;left:calc(16.6% + 14px);right:calc(16.6% + 14px);height:2px;background:#dce8f0;z-index:0}}
.fml .step{{text-align:center;padding:0 20px;position:relative;z-index:1}}
.fml .step-num{{width:56px;height:56px;background:#0d4a7a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Montserrat',sans-serif;font-size:1.2rem;font-weight:800;color:#fff;margin:0 auto 20px}}
.fml .step h3{{font-family:'Montserrat',sans-serif;font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:10px}}
.fml .step p{{font-size:.88rem;color:#555;line-height:1.7}}
@media(max-width:640px){{
  .fml .steps{{grid-template-columns:1fr;gap:32px}}
  .fml .steps::before{{display:none}}
}}

/* ── CTA band ───────────────────────────────────────────────────── */
.fml .cta-band{{background:#0d4a7a;padding:72px 24px;text-align:center}}
.fml .cta-band h2{{font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;color:#fff;margin-bottom:16px;line-height:1.2}}
.fml .cta-band p{{font-size:1.05rem;color:rgba(255,255,255,.85);max-width:580px;margin:0 auto 36px;line-height:1.75}}

/* ── FAQ ─────────────────────────────────────────────────────────── */
.fml .faq-wrap{{max-width:780px;margin:0 auto;text-align:left}}
.fml .faq{{border-bottom:1px solid #dce8f0;padding:20px 0}}
.fml .faq-q{{font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;color:#07304f;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:12px;user-select:none}}
.fml .faq-a{{font-size:.93rem;color:#555;line-height:1.8;padding-top:14px;display:none}}
.fml .faq.open .faq-a{{display:block}}
.fml .faq.open .ico{{transform:rotate(45deg)}}
.fml .ico{{font-size:1.5rem;color:#0db8a5;transition:transform .2s;flex-shrink:0;line-height:1}}

@media(max-width:600px){{
  .fml .btn-ghost{{display:none}}
  .fml .st{{padding:16px 24px}}
  .fml .hero{{padding:72px 24px 64px}}
}}
</style>

<div class="fml">

<!-- ── HERO ─────────────────────────────────────────────────────── -->
<div class="hero">
  <div class="hero-body">
    <div class="hero-pill">&#10003; Gwinnett County&rsquo;s Mobile Lab Service</div>
    <h1>Lab Work That Comes<br><em>Directly to You.</em></h1>
    <p class="hero-sub">Certified phlebotomists serve all of Gwinnett County — 7 days a week. Blood draws, DNA testing, drug screening, and more performed at your home, office, or facility. No waiting rooms.</p>
    <a class="btn-teal" href="{BOOK_URL}">Schedule an Appointment &rarr;</a>
    <a class="btn-ghost" href="tel:6785625244">Call {PHONE}</a>
    <div class="hero-trust">
      <span><span class="ck">&#10003;</span> Licensed &amp; Certified Phlebotomists</span>
      <span><span class="ck">&#10003;</span> HIPAA-Compliant</span>
      <span><span class="ck">&#10003;</span> CLIA-Certified Partner Labs</span>
      <span><span class="ck">&#10003;</span> Same-Day Appointments</span>
    </div>
  </div>
</div>

<!-- ── STATS BAR ─────────────────────────────────────────────────── -->
<div class="statsbar">
  <div class="st"><span class="st-n">7+</span><span class="st-l">Years in Healthcare</span></div>
  <div class="st"><span class="st-n">500+</span><span class="st-l">Patients Served</span></div>
  <div class="st"><span class="st-n">30+</span><span class="st-l">Mile Service Radius</span></div>
  <div class="st"><span class="st-n">HIPAA</span><span class="st-l">Fully Compliant</span></div>
</div>

<!-- ── SERVICES ─────────────────────────────────────────────────── -->
<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">What We Offer</span>
        <h2>Mobile Lab Services Across Gwinnett County</h2>
        <p class="lead">Every service is performed by licensed phlebotomists and processed through CLIA-certified partner laboratories — at your location, on your schedule.</p>
        <ul class="svc-list">
          <li>
            <div class="svc-icon">🩸</div>
            <div><strong>At-Home Blood Draws &amp; Diagnostics</strong><p>Physician-ordered and direct-access blood draws for routine panels, specialty diagnostics, and health monitoring — performed wherever you are in Gwinnett County.</p></div>
          </li>
          <li>
            <div class="svc-icon">🧬</div>
            <div><strong>Mobile DNA &amp; Paternity Testing</strong><p>Court-admissible and peace-of-mind DNA testing at your location. Paternity, maternity, sibling, immigration, and relationship testing with strict chain-of-custody documentation.</p></div>
          </li>
          <li>
            <div class="svc-icon">💊</div>
            <div><strong>Mobile Drug &amp; Alcohol Testing</strong><p>DOT and non-DOT urine, saliva, and hair follicle testing for Gwinnett County employers, legal proceedings, and personal use. HIPAA-compliant with full chain-of-custody.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="svc-list" style="margin-top:0;padding-top:0">
          <li>
            <div class="svc-icon">🏢</div>
            <div><strong>Pre-Employment Screening</strong><p>Occupational health and pre-employment drug screen packages for Gwinnett County businesses and HR teams. Flexible onsite scheduling — we come to your workplace.</p></div>
          </li>
          <li>
            <div class="svc-icon">❤️</div>
            <div><strong>Health &amp; Wellness Panels</strong><p>CBC, metabolic, lipid, thyroid, hormone, and vitamin panels. Many available without a doctor&rsquo;s order — take control of your preventive health from your own home.</p></div>
          </li>
          <li>
            <div class="svc-icon">🔬</div>
            <div><strong>Specialty Kit &amp; Concierge Collections</strong><p>Food sensitivity, genetic testing, micronutrient panels, and clinical trial specimen collections. Concierge physician partnerships for in-home lab support.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ── HOW IT WORKS ──────────────────────────────────────────────── -->
<section class="bg-lt">
  <div class="wrap" style="text-align:center">
    <span class="tag">The Process</span>
    <h2>How Mobile Phlebotomy Works</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto">Three steps from scheduling to results — no driving, no waiting rooms, no hassle.</p>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <h3>Book Online or Call</h3>
        <p>Schedule in minutes at a time that works for you — including evenings, early mornings for fasting draws, and weekends throughout Gwinnett County.</p>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <h3>We Come to You</h3>
        <p>A licensed, background-checked phlebotomist arrives at your home, office, or facility. Samples are collected with hospital-grade protocol and full chain-of-custody documentation.</p>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <h3>Results Delivered Securely</h3>
        <p>Specimens go directly to our CLIA-certified partner labs. Results are typically available within 24&ndash;72 hours, delivered securely — no re-visit required.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── WHY FASTRAK ───────────────────────────────────────────────── -->
<section class="bg-wh">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak Mobile Lab</span>
      <h2>The Mobile Lab Difference</h2>
      <p class="lead">We&rsquo;re not a national chain. We&rsquo;re a Gwinnett County&ndash;based mobile lab provider with hospital-grade standards and the convenience of a house call.</p>
    </div>
    <div class="diff-grid">
      <div class="diff-card">
        <span class="diff-num">01</span>
        <h3>Same-Day Appointments</h3>
        <p>We often accommodate same-day visits throughout Gwinnett County — 7 days a week, including early morning fasting draws and weekend visits.</p>
      </div>
      <div class="diff-card">
        <span class="diff-num">02</span>
        <h3>100% HIPAA Compliant</h3>
        <p>Encrypted communication, secure results delivery, and zero third-party sharing without your explicit authorization. Your health information stays private.</p>
      </div>
      <div class="diff-card">
        <span class="diff-num">03</span>
        <h3>Certified Phlebotomists</h3>
        <p>Every technician is licensed, background-checked, and trained in mobile specimen collection — including pediatric and difficult-stick patients.</p>
      </div>
      <div class="diff-card">
        <span class="diff-num">04</span>
        <h3>No Doctor? No Problem.</h3>
        <p>We accept physician orders and offer direct-access testing — hundreds of panels available without a referral, right from your Gwinnett County home.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── AREAS SERVED ──────────────────────────────────────────────── -->
<section id="areas" class="bg-lt">
  <div class="wrap">
    <div style="text-align:center;max-width:680px;margin:0 auto 40px">
      <span class="tag">Service Area</span>
      <h2>Every City in Gwinnett County, GA</h2>
      <p class="lead" style="margin-bottom:0">We provide mobile phlebotomy and lab services throughout all of Gwinnett County. If you live or work here, we come to you — no exceptions.</p>
    </div>
    <div class="cities-grid">
      <span class="city-pill">Lawrenceville</span>
      <span class="city-pill">Snellville</span>
      <span class="city-pill">Duluth</span>
      <span class="city-pill">Lilburn</span>
      <span class="city-pill">Norcross</span>
      <span class="city-pill">Buford</span>
      <span class="city-pill">Grayson</span>
      <span class="city-pill">Loganville</span>
      <span class="city-pill">Dacula</span>
      <span class="city-pill">Suwanee</span>
      <span class="city-pill">Tucker</span>
      <span class="city-pill">Sugar Hill</span>
      <span class="city-pill">Peachtree Corners</span>
      <span class="city-pill">Winder</span>
    </div>
  </div>
</section>

<!-- ── CTA BAND ──────────────────────────────────────────────────── -->
<div class="cta-band">
  <h2>Ready for Lab Work That Comes to You?</h2>
  <p>Stop driving to the lab. Stop waiting in line. Book your Gwinnett County mobile blood draw today — certified, convenient, and HIPAA-compliant.</p>
  <a class="btn-teal" href="{BOOK_URL}">Schedule Your Appointment &rarr;</a>
</div>

<!-- ── FAQ ───────────────────────────────────────────────────────── -->
<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; Mobile Phlebotomy in Gwinnett County</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px">Everything Gwinnett County patients ask before booking their first appointment.</p>
    <div class="faq-wrap">
      <div class="faq">
        <div class="faq-q">How does mobile phlebotomy work in Gwinnett County?<span class="ico">+</span></div>
        <div class="faq-a">You book an appointment online or by phone, and a certified Fastrak phlebotomist travels to your Gwinnett County home, office, or facility. We collect your sample, maintain chain-of-custody documentation, and send it to our CLIA-certified partner lab. Results are typically available within 24&ndash;72 hours.</div>
      </div>
      <div class="faq">
        <div class="faq-q">Do I need a doctor&rsquo;s order for a blood draw in Gwinnett County?<span class="ico">+</span></div>
        <div class="faq-a">Most diagnostic tests require a physician&rsquo;s order. However, Fastrak also offers direct-access testing for many panels &mdash; including wellness, thyroid, hormone, vitamin, and lipid panels &mdash; that you can order yourself without a doctor&rsquo;s referral.</div>
      </div>
      <div class="faq">
        <div class="faq-q">What cities in Gwinnett County do you serve?<span class="ico">+</span></div>
        <div class="faq-a">We serve all of Gwinnett County, GA &mdash; Lawrenceville, Snellville, Duluth, Lilburn, Norcross, Buford, Grayson, Loganville, Dacula, Suwanee, Tucker, Sugar Hill, and all surrounding communities within our 30-mile service radius.</div>
      </div>
      <div class="faq">
        <div class="faq-q">How quickly can I get a mobile phlebotomy appointment in Gwinnett County?<span class="ico">+</span></div>
        <div class="faq-a">We offer same-day and next-day appointments in most Gwinnett County areas. Call us at {PHONE} or use our online booking system to check real-time availability. Early morning fasting slots are available by request.</div>
      </div>
      <div class="faq">
        <div class="faq-q">Is Fastrak Mobile Lab HIPAA compliant?<span class="ico">+</span></div>
        <div class="faq-a">Yes. All services are fully HIPAA-compliant. We use secure, encrypted communication for results, maintain strict chain-of-custody protocols, and never share your health information without your explicit authorization.</div>
      </div>
      <div class="faq">
        <div class="faq-q">Can you serve seniors and homebound patients in Gwinnett County?<span class="ico">+</span></div>
        <div class="faq-a">Absolutely. Mobile phlebotomy was designed with seniors and homebound patients in mind. Our phlebotomists are experienced in compassionate, gentle care and regularly serve assisted living facilities, nursing homes, and private residences throughout Gwinnett County.</div>
      </div>
    </div>
  </div>
</section>

<script>
document.querySelectorAll('.fml .faq-q').forEach(function(q){{
  q.addEventListener('click',function(){{
    this.closest('.faq').classList.toggle('open');
  }});
}});
</script>

</div><!-- /fml -->
<!-- /wp:html -->"""

RANK_MATH_TITLE = "Mobile Phlebotomy Gwinnett County GA | Fastrak Mobile Lab"
RANK_MATH_DESC  = ("Certified mobile phlebotomists serving all of Gwinnett County, GA — "
                   "7 days a week. At-home blood draws, DNA testing & more. Book same-day.")
FOCUS_KW = "mobile phlebotomy Gwinnett County GA"

print("=" * 60)
print(f"Updating page ID {PAGE_ID} ...")
print("=" * 60)

r1 = requests.post(
    f"{WP_SITE}/wp-json/wp/v2/pages/{PAGE_ID}",
    headers=HJ,
    json={"content": NEW_CONTENT},
    timeout=30,
)
print(f"Content update:  HTTP {r1.status_code}")

r2 = requests.post(
    f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
    headers=HJ,
    json={
        "objectID":   PAGE_ID,
        "objectType": "page",
        "meta": {
            "rank_math_title":         RANK_MATH_TITLE,
            "rank_math_description":   RANK_MATH_DESC,
            "rank_math_focus_keyword": FOCUS_KW,
        },
    },
    timeout=15,
)
print(f"Rank Math meta:  HTTP {r2.status_code} -> {r2.text[:80]}")
print()
if r1.ok:
    print("Done. https://fastrakmobilelab.com/mobile-phlebotomy-gwinnett-county-ga/")
else:
    print(f"FAILED: {r1.text[:300]}")
