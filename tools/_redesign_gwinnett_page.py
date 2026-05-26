"""
Redesign mobile-phlebotomy-gwinnett-county-ga/ — clean editorial layout.
Removes boxy card grid; uses feature-list + open sections for a professional look.
Brand colors: #0d4a7a (dark blue) / #0db8a5 (teal).
Keywords: mobile phlebotomy Gwinnett County GA, at-home blood draw Gwinnett County.
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

PAGE_ID   = 1249
BOOK_URL  = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"
PHONE     = "(678) 562-5244"

NEW_CONTENT = f"""<!-- wp:html -->
<style>
/* ── hide theme-rendered page title ── */
.page-id-1249 .entry-title,
.page-id-1249 .page-title,
.page-id-1249 h1.entry-title,
.page-id-1249 .page-header,
.page-id-1249 .entry-header {{display:none!important}}
.page-id-1249 .entry-content {{padding-top:0!important;margin-top:0!important}}

/* ── base ── */
.gw {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1a1a2e}}
*, *::before, *::after {{box-sizing:border-box}}

/* ── hero ── */
.gw-hero {{background:linear-gradient(135deg,#0d4a7a 0%,#0db8a5 100%);padding:100px 24px 90px;text-align:center;color:#fff}}
.gw-hero h1 {{font-size:clamp(2em,5vw,3.2em);font-weight:800;margin:0 0 20px;line-height:1.15;letter-spacing:-.02em}}
.gw-hero h1 em {{font-style:normal;color:#a0f0e4}}
.gw-hero p {{font-size:1.15em;max-width:640px;margin:0 auto 36px;opacity:.92;line-height:1.65}}
.gw-btn {{display:inline-block;padding:15px 32px;border-radius:8px;font-weight:700;font-size:.97em;text-decoration:none;margin:6px;transition:opacity .2s}}
.gw-btn:hover {{opacity:.88}}
.gw-btn-primary {{background:#fff;color:#0d4a7a}}
.gw-btn-ghost {{border:2px solid rgba(255,255,255,.75);color:#fff}}

/* ── trust bar ── */
.gw-trust {{background:#fff;border-bottom:1px solid #edf0f3;padding:20px 24px;display:flex;flex-wrap:wrap;justify-content:center;gap:24px 40px}}
.gw-trust-item {{display:flex;align-items:center;gap:8px;font-size:.88em;font-weight:600;color:#0d4a7a}}
.gw-trust-item::before {{content:"✓";color:#0db8a5;font-size:1.1em;font-weight:800}}

/* ── stats ── */
.gw-stats {{background:linear-gradient(90deg,#f7fbff 0%,#f0faf8 100%);padding:56px 24px;display:flex;justify-content:center;gap:16px 64px;flex-wrap:wrap;text-align:center}}
.gw-stat-n {{font-size:2.6em;font-weight:800;color:#0d4a7a;line-height:1;display:block}}
.gw-stat-l {{font-size:.85em;color:#6c757d;margin-top:6px;font-weight:500}}

/* ── layout ── */
.gw-wrap {{max-width:1080px;margin:0 auto;padding:0 24px}}
.gw-section {{padding:80px 24px}}
.gw-section-alt {{background:#f8fafc}}
.gw-eyebrow {{font-size:.78em;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0db8a5;margin:0 0 12px}}
.gw-heading {{font-size:clamp(1.5em,3.5vw,2.1em);font-weight:800;color:#0d4a7a;margin:0 0 16px;line-height:1.25;letter-spacing:-.01em}}
.gw-subtext {{color:#5a6678;font-size:1.02em;line-height:1.7;margin:0 0 48px;max-width:660px}}

/* ── feature list (services) ── */
.gw-features {{display:grid;grid-template-columns:repeat(auto-fit,minmax(480px,1fr));gap:0}}
.gw-feature {{display:flex;gap:20px;padding:28px 0;border-bottom:1px solid #edf0f3;align-items:flex-start}}
.gw-features .gw-feature:last-child {{border-bottom:none}}
.gw-feature-icon {{width:52px;height:52px;background:linear-gradient(135deg,#0d4a7a,#0db8a5);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.4em;flex-shrink:0;color:#fff}}
.gw-feature-body h3 {{font-size:1.05em;font-weight:700;color:#0d4a7a;margin:0 0 6px;line-height:1.3}}
.gw-feature-body p {{color:#5a6678;font-size:.93em;line-height:1.65;margin:0}}

/* ── cities ── */
.gw-city-grid {{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}}
.gw-city-pill {{background:#fff;border:1px solid #dce7f0;border-radius:30px;padding:9px 18px;font-size:.9em;font-weight:600;color:#0d4a7a;display:flex;align-items:center;gap:7px}}
.gw-city-pill span {{width:7px;height:7px;background:#0db8a5;border-radius:50%;flex-shrink:0}}

/* ── why us ── */
.gw-why {{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:36px}}
.gw-why-item {{display:flex;gap:16px;align-items:flex-start}}
.gw-why-num {{width:40px;height:40px;background:#0d4a7a;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#0db8a5;font-weight:800;font-size:.9em;flex-shrink:0}}
.gw-why-body h3 {{font-size:1em;font-weight:700;color:#0d4a7a;margin:0 0 6px}}
.gw-why-body p {{color:#5a6678;font-size:.9em;line-height:1.65;margin:0}}

/* ── faq ── */
.gw-faq {{max-width:760px;margin:0 auto}}
.gw-faq-item {{border-bottom:1px solid #edf0f3;padding:24px 0}}
.gw-faq-item:first-child {{padding-top:0}}
.gw-faq-item h4 {{font-size:1em;font-weight:700;color:#0d4a7a;margin:0 0 10px;line-height:1.4}}
.gw-faq-item p {{color:#5a6678;font-size:.95em;line-height:1.7;margin:0}}

/* ── cta banner ── */
.gw-cta {{background:linear-gradient(135deg,#0d4a7a 0%,#0db8a5 100%);padding:80px 24px;text-align:center;color:#fff}}
.gw-cta h2 {{font-size:clamp(1.6em,4vw,2.3em);font-weight:800;margin:0 0 16px;line-height:1.2;color:#fff}}
.gw-cta p {{font-size:1.05em;max-width:580px;margin:0 auto 32px;opacity:.92;line-height:1.65}}

/* ── responsive ── */
@media(max-width:600px){{
  .gw-features{{grid-template-columns:1fr}}
  .gw-why{{grid-template-columns:1fr}}
}}
</style>

<div class="gw">

<!-- ─── HERO ──────────────────────────────────────────────────────── -->
<div class="gw-hero">
  <h1>Mobile Phlebotomy in<br><em>Gwinnett County, GA</em></h1>
  <p>Certified phlebotomists come to your home, office, or facility across Gwinnett County — 7 days a week. No waiting rooms. No driving.</p>
  <a class="gw-btn gw-btn-primary" href="{BOOK_URL}">Schedule an Appointment</a>
  <a class="gw-btn gw-btn-ghost" href="tel:6785625244">Call {PHONE}</a>
</div>

<!-- ─── TRUST BAR ───────────────────────────────────────────────────── -->
<div class="gw-trust">
  <div class="gw-trust-item">Licensed &amp; Certified Phlebotomists</div>
  <div class="gw-trust-item">HIPAA-Compliant</div>
  <div class="gw-trust-item">CLIA-Certified Partner Labs</div>
  <div class="gw-trust-item">Same-Day Appointments Available</div>
  <div class="gw-trust-item">Chain of Custody Documentation</div>
  <div class="gw-trust-item">7 Days a Week</div>
</div>

<!-- ─── STATS ───────────────────────────────────────────────────────── -->
<div class="gw-stats">
  <div><span class="gw-stat-n">7+</span><div class="gw-stat-l">Years in Healthcare</div></div>
  <div><span class="gw-stat-n">500+</span><div class="gw-stat-l">Patients Served</div></div>
  <div><span class="gw-stat-n">30+</span><div class="gw-stat-l">Mile Service Radius</div></div>
  <div><span class="gw-stat-n">HIPAA</span><div class="gw-stat-l">Fully Compliant</div></div>
</div>

<!-- ─── SERVICES ────────────────────────────────────────────────────── -->
<div class="gw-section" id="services">
<div class="gw-wrap">
  <p class="gw-eyebrow">What We Offer</p>
  <h2 class="gw-heading">Mobile Lab Services Across Gwinnett County</h2>
  <p class="gw-subtext">Every service is performed by licensed phlebotomists and processed through CLIA-certified partner laboratories — wherever you are in Gwinnett County.</p>
  <div class="gw-features">
    <div class="gw-feature">
      <div class="gw-feature-icon">🩸</div>
      <div class="gw-feature-body">
        <h3>At-Home Blood Draws &amp; Diagnostic Testing</h3>
        <p>Physician-ordered and direct-access blood draws for routine panels, specialty diagnostics, and health monitoring — performed at your Gwinnett County home, office, or facility.</p>
      </div>
    </div>
    <div class="gw-feature">
      <div class="gw-feature-icon">🧬</div>
      <div class="gw-feature-body">
        <h3>Mobile DNA &amp; Paternity Testing</h3>
        <p>Court-admissible and peace-of-mind DNA testing collected at your location. Paternity, maternity, sibling, immigration, and relationship testing with strict chain-of-custody documentation.</p>
      </div>
    </div>
    <div class="gw-feature">
      <div class="gw-feature-icon">💊</div>
      <div class="gw-feature-body">
        <h3>Mobile Drug &amp; Alcohol Testing</h3>
        <p>DOT and non-DOT urine, saliva, and hair follicle drug testing for Gwinnett County employers, legal proceedings, and personal use. HIPAA-compliant with full chain-of-custody.</p>
      </div>
    </div>
    <div class="gw-feature">
      <div class="gw-feature-icon">🏢</div>
      <div class="gw-feature-body">
        <h3>Pre-Employment Screening</h3>
        <p>Occupational health and pre-employment drug screen packages for Gwinnett County businesses and HR teams. Flexible onsite scheduling — we come to your workplace.</p>
      </div>
    </div>
    <div class="gw-feature">
      <div class="gw-feature-icon">❤️</div>
      <div class="gw-feature-body">
        <h3>Health &amp; Wellness Panels</h3>
        <p>CBC, metabolic, lipid, thyroid, hormone, and vitamin panels. Many available without a doctor's order — order your own labs and take control of your preventive health.</p>
      </div>
    </div>
    <div class="gw-feature">
      <div class="gw-feature-icon">🔬</div>
      <div class="gw-feature-body">
        <h3>Specialty Kit &amp; Concierge Collections</h3>
        <p>Food sensitivity, genetic testing, micronutrient panels, and clinical trial specimen collections. Concierge physician partnerships for in-home lab support across Gwinnett County.</p>
      </div>
    </div>
  </div>
</div>
</div>

<!-- ─── CITIES ──────────────────────────────────────────────────────── -->
<div class="gw-section gw-section-alt">
<div class="gw-wrap">
  <p class="gw-eyebrow">Service Area</p>
  <h2 class="gw-heading">Every City in Gwinnett County, GA</h2>
  <p class="gw-subtext">We provide mobile phlebotomy and lab services throughout all of Gwinnett County. If you live or work here, we come to you.</p>
  <div class="gw-city-grid">
    <div class="gw-city-pill"><span></span>Lawrenceville</div>
    <div class="gw-city-pill"><span></span>Snellville</div>
    <div class="gw-city-pill"><span></span>Duluth</div>
    <div class="gw-city-pill"><span></span>Lilburn</div>
    <div class="gw-city-pill"><span></span>Norcross</div>
    <div class="gw-city-pill"><span></span>Buford</div>
    <div class="gw-city-pill"><span></span>Grayson</div>
    <div class="gw-city-pill"><span></span>Loganville</div>
    <div class="gw-city-pill"><span></span>Dacula</div>
    <div class="gw-city-pill"><span></span>Suwanee</div>
    <div class="gw-city-pill"><span></span>Tucker</div>
    <div class="gw-city-pill"><span></span>Sugar Hill</div>
    <div class="gw-city-pill"><span></span>Peachtree Corners</div>
    <div class="gw-city-pill"><span></span>Winder</div>
  </div>
</div>
</div>

<!-- ─── WHY US ───────────────────────────────────────────────────────── -->
<div class="gw-section">
<div class="gw-wrap">
  <p class="gw-eyebrow">Why Fastrak</p>
  <h2 class="gw-heading">Why Gwinnett County Chooses Us</h2>
  <p class="gw-subtext">We're not a national chain. We're your local, certified mobile phlebotomy provider — with hospital-grade standards and the convenience of a house call.</p>
  <div class="gw-why">
    <div class="gw-why-item">
      <div class="gw-why-num">01</div>
      <div class="gw-why-body">
        <h3>Same-Day Appointments</h3>
        <p>Book online or call — we often accommodate same-day visits throughout Gwinnett County, 7 days a week including weekends and early mornings for fasting draws.</p>
      </div>
    </div>
    <div class="gw-why-item">
      <div class="gw-why-num">02</div>
      <div class="gw-why-body">
        <h3>100% HIPAA Compliant</h3>
        <p>Your health information is protected with the strictest privacy standards. Secure results delivery, encrypted communication, and zero third-party sharing without your consent.</p>
      </div>
    </div>
    <div class="gw-why-item">
      <div class="gw-why-num">03</div>
      <div class="gw-why-body">
        <h3>Certified Phlebotomists</h3>
        <p>Every Fastrak technician is licensed, background-checked, and trained in mobile specimen collection — including pediatric draws and difficult-stick patients.</p>
      </div>
    </div>
    <div class="gw-why-item">
      <div class="gw-why-num">04</div>
      <div class="gw-why-body">
        <h3>No Doctor? No Problem.</h3>
        <p>We accept physician orders and offer direct-access testing — order your own labs for hundreds of panels without needing a referral.</p>
      </div>
    </div>
  </div>
</div>
</div>

<!-- ─── FAQ ─────────────────────────────────────────────────────────── -->
<div class="gw-section gw-section-alt">
<div class="gw-wrap">
  <p class="gw-eyebrow">FAQ</p>
  <h2 class="gw-heading" style="text-align:center">Common Questions</h2>
  <div class="gw-faq">
    <div class="gw-faq-item">
      <h4>How does mobile phlebotomy work in Gwinnett County?</h4>
      <p>You book an appointment online or by phone, and a certified Fastrak phlebotomist travels to your Gwinnett County home, office, or facility. We collect your sample, maintain chain-of-custody documentation, and send it to our CLIA-certified partner lab. Results are typically available within 24–72 hours.</p>
    </div>
    <div class="gw-faq-item">
      <h4>Do I need a doctor's order for a blood draw in Gwinnett County?</h4>
      <p>Most diagnostic tests require a physician's order. However, Fastrak also offers direct-access testing for many panels — including wellness, thyroid, hormone, vitamin, and lipid panels — that you can order yourself without a doctor's referral.</p>
    </div>
    <div class="gw-faq-item">
      <h4>What cities in Gwinnett County do you serve?</h4>
      <p>We serve all of Gwinnett County, GA — Lawrenceville, Snellville, Duluth, Lilburn, Norcross, Buford, Grayson, Loganville, Dacula, Suwanee, Tucker, Sugar Hill, and all surrounding communities within our 30-mile service radius.</p>
    </div>
    <div class="gw-faq-item">
      <h4>How quickly can I get a mobile phlebotomy appointment?</h4>
      <p>We offer same-day and next-day appointments in most Gwinnett County areas. Call us at {PHONE} or use our online booking system to check real-time availability. Early morning fasting slots are available by request.</p>
    </div>
    <div class="gw-faq-item">
      <h4>Is Fastrak Mobile Lab HIPAA compliant?</h4>
      <p>Yes. All services are fully HIPAA-compliant. We use secure, encrypted communication for results, maintain strict chain-of-custody protocols, and never share your health information without your explicit authorization.</p>
    </div>
    <div class="gw-faq-item">
      <h4>Can you serve seniors and homebound patients in Gwinnett County?</h4>
      <p>Absolutely. Mobile phlebotomy was designed with seniors and homebound patients in mind. Our phlebotomists are experienced in compassionate, gentle care and regularly serve assisted living facilities, nursing homes, and private residences throughout Gwinnett County.</p>
    </div>
  </div>
</div>
</div>

<!-- ─── CTA ──────────────────────────────────────────────────────────── -->
<div class="gw-cta">
  <h2>Ready for Lab Work That Comes to You?</h2>
  <p>Stop driving to the lab. Stop waiting in line. Book your Gwinnett County mobile blood draw today — certified, convenient, and HIPAA-compliant.</p>
  <a class="gw-btn gw-btn-primary" href="{BOOK_URL}">Schedule Your Appointment</a>
  <a class="gw-btn gw-btn-ghost" href="tel:6785625244">Call {PHONE}</a>
</div>

</div><!-- /gw -->
<!-- /wp:html -->"""

RANK_MATH_TITLE = "Mobile Phlebotomy Gwinnett County GA | Fastrak Mobile Lab"
RANK_MATH_DESC  = ("Certified mobile phlebotomists serving all of Gwinnett County, GA — "
                   "7 days a week. At-home blood draws, DNA testing & more. Book same-day.")
FOCUS_KW = "mobile phlebotomy Gwinnett County GA"

print("=" * 60)
print(f"Updating page ID {PAGE_ID}...")
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
