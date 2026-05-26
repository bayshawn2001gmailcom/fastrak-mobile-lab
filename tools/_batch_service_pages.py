"""
Batch redesign service landing pages (non-city-specific) — ATD editorial style.
Pages: DNA Testing Georgia, Drug Testing Atlanta, Concierge, Corporate, At-Home Blood Draw Atlanta.
"""
import os, base64, socket, requests, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".env")
_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

WP_SITE  = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
creds    = base64.b64encode(f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()).decode()
HJ       = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
BOOK_URL = "https://api.leadconnectorhq.com/widget/bookings/stephanie-fleming-personal-calendar-kc9dxb7pt"
PHONE    = "(678) 562-5244"

CSS_BASE = """<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
.fml-svc{{box-sizing:border-box;font-family:'Inter',sans-serif;color:#111;line-height:1.65;background:#fff}}
.fml-svc *{{box-sizing:border-box;margin:0;padding:0}}
.fml-svc h1,.fml-svc h2,.fml-svc h3,.fml-svc h4{{font-family:'Montserrat',sans-serif;line-height:1.2;color:inherit}}
.fml-svc a{{text-decoration:none;color:inherit}}
.fml-svc .hero{{background:linear-gradient(135deg,#07304f 0%,#0d4a7a 55%,#0a8c7c 100%);padding:96px 24px 88px;position:relative;overflow:hidden}}
.fml-svc .hero::before{{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}}
.fml-svc .hero-body{{position:relative;z-index:1;max-width:700px;margin:0 auto;text-align:center}}
.fml-svc .hero-pill{{display:inline-block;border:1.5px solid rgba(255,255,255,.35);padding:5px 18px;border-radius:4px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:24px;color:rgba(255,255,255,.9);font-family:'Montserrat',sans-serif}}
.fml-svc .hero h1{{font-size:clamp(2.2rem,5vw,3.5rem);font-weight:800;margin-bottom:20px;color:#fff;line-height:1.15}}
.fml-svc .hero h1 em{{font-style:normal;color:#6ef0e0}}
.fml-svc .hero-sub{{font-size:1.1rem;color:rgba(255,255,255,.88);max-width:620px;margin:0 auto 36px;line-height:1.75}}
.fml-svc .btn-teal{{display:inline-block;background:#0db8a5;color:#fff;padding:16px 40px;border-radius:4px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;transition:background .2s,transform .15s;letter-spacing:.3px;box-shadow:0 4px 20px rgba(13,184,165,.4)}}
.fml-svc .btn-teal:hover{{background:#0aa898;transform:translateY(-2px)}}
.fml-svc .btn-ghost{{display:inline-block;border:2px solid rgba(255,255,255,.5);color:#fff;padding:14px 32px;border-radius:4px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:.97rem;margin-left:14px;transition:border-color .2s}}
.fml-svc .btn-ghost:hover{{border-color:#fff}}
.fml-svc .hero-trust{{display:flex;flex-wrap:wrap;justify-content:center;gap:18px;margin-top:32px}}
.fml-svc .hero-trust span{{font-size:13px;color:rgba(255,255,255,.8);display:flex;align-items:center;gap:7px}}
.fml-svc .hero-trust .ck{{color:#6ef0e0;font-weight:800}}
.fml-svc .statsbar{{background:#0d4a7a;display:flex;justify-content:center;flex-wrap:wrap}}
.fml-svc .st{{padding:20px 48px;text-align:center;color:#fff;border-right:1px solid rgba(255,255,255,.12)}}
.fml-svc .st:last-child{{border-right:none}}
.fml-svc .st-n{{display:block;font-family:'Montserrat',sans-serif;font-size:1.9rem;font-weight:800;color:#6ef0e0}}
.fml-svc .st-l{{font-size:11px;opacity:.7;letter-spacing:.8px;text-transform:uppercase;margin-top:4px}}
.fml-svc section{{padding:80px 24px}}
.fml-svc .wrap{{max-width:1040px;margin:0 auto}}
.fml-svc .tag{{display:inline-block;color:#0db8a5;font-family:'Montserrat',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;margin-bottom:12px}}
.fml-svc h2{{font-size:clamp(1.8rem,3.8vw,2.7rem);font-weight:800;color:#07304f;margin-bottom:16px}}
.fml-svc .lead{{font-size:1.03rem;color:#444;line-height:1.85;margin-bottom:40px}}
.fml-svc .bg-lt{{background:#f4f8fc}}
.fml-svc .bg-wh{{background:#fff}}
.fml-svc .two-col{{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}}
@media(max-width:720px){{.fml-svc .two-col{{grid-template-columns:1fr}}}}
.fml-svc .feat-list{{list-style:none;display:flex;flex-direction:column;gap:22px}}
.fml-svc .feat-list li{{display:flex;gap:16px;align-items:flex-start}}
.fml-svc .feat-icon{{width:42px;height:42px;min-width:42px;background:#f0f8fc;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.25rem}}
.fml-svc .feat-list strong{{display:block;font-family:'Montserrat',sans-serif;font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:4px}}
.fml-svc .feat-list p{{font-size:.9rem;color:#555;line-height:1.65}}
.fml-svc .diff-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2px;margin-top:48px;border:1px solid #dce8f0;border-radius:4px;overflow:hidden}}
.fml-svc .diff-card{{background:#fff;padding:32px 26px;border-right:1px solid #dce8f0}}
.fml-svc .diff-card:last-child{{border-right:none}}
.fml-svc .diff-num{{font-family:'Montserrat',sans-serif;font-size:2.2rem;font-weight:800;color:#c8dff0;margin-bottom:12px;display:block}}
.fml-svc .diff-card h3{{font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:8px;font-family:'Montserrat',sans-serif}}
.fml-svc .diff-card p{{font-size:.87rem;color:#555;line-height:1.7}}
.fml-svc .area-pills{{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}}
.fml-svc .area-pill{{background:#fff;border:1.5px solid #ccdce8;border-radius:30px;padding:9px 18px;font-size:.9rem;font-weight:600;color:#0d4a7a;display:flex;align-items:center;gap:8px;font-family:'Montserrat',sans-serif}}
.fml-svc .area-pill::before{{content:'';width:7px;height:7px;background:#0db8a5;border-radius:50%;flex-shrink:0}}
.fml-svc .steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:48px;position:relative}}
.fml-svc .steps::before{{content:'';position:absolute;top:27px;left:calc(16.6% + 14px);right:calc(16.6% + 14px);height:2px;background:#dce8f0;z-index:0}}
.fml-svc .step{{text-align:center;padding:0 20px;position:relative;z-index:1}}
.fml-svc .step-num{{width:56px;height:56px;background:#0d4a7a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Montserrat',sans-serif;font-size:1.2rem;font-weight:800;color:#fff;margin:0 auto 20px}}
.fml-svc .step h3{{font-family:'Montserrat',sans-serif;font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:10px}}
.fml-svc .step p{{font-size:.88rem;color:#555;line-height:1.7}}
.fml-svc .cta-band{{background:#0d4a7a;padding:72px 24px;text-align:center}}
.fml-svc .cta-band h2{{font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;color:#fff;margin-bottom:16px;line-height:1.2}}
.fml-svc .cta-band p{{font-size:1.05rem;color:rgba(255,255,255,.85);max-width:580px;margin:0 auto 36px;line-height:1.75}}
.fml-svc .faq-wrap{{max-width:780px;margin:0 auto;text-align:left}}
.fml-svc .faq{{border-bottom:1px solid #dce8f0;padding:20px 0}}
.fml-svc .faq-q{{font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;color:#07304f;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:12px;user-select:none}}
.fml-svc .faq-a{{font-size:.93rem;color:#555;line-height:1.8;padding-top:14px;display:none}}
.fml-svc .faq.open .faq-a{{display:block}}
.fml-svc .faq.open .ico{{transform:rotate(45deg)}}
.fml-svc .ico{{font-size:1.5rem;color:#0db8a5;transition:transform .2s;flex-shrink:0;line-height:1}}
@media(max-width:640px){{
  .fml-svc .steps{{grid-template-columns:1fr;gap:32px}}
  .fml-svc .steps::before{{display:none}}
  .fml-svc .btn-ghost{{display:none}}
  .fml-svc .st{{padding:16px 24px}}
  .fml-svc .hero{{padding:72px 24px 64px}}
}}
</style>"""

AREAS = ["Gwinnett County", "Snellville, GA", "Lawrenceville, GA", "Duluth, GA",
         "Norcross, GA", "Decatur, GA", "Buckhead, Atlanta", "Sandy Springs, GA",
         "Marietta, GA", "Conyers, GA", "Tucker, GA", "Stone Mountain, GA"]

STATS_BAR = """<div class="statsbar">
  <div class="st"><span class="st-n">7+</span><span class="st-l">Years in Healthcare</span></div>
  <div class="st"><span class="st-n">500+</span><span class="st-l">Patients Served</span></div>
  <div class="st"><span class="st-n">30+</span><span class="st-l">Mile Service Radius</span></div>
  <div class="st"><span class="st-n">HIPAA</span><span class="st-l">Fully Compliant</span></div>
</div>"""

TRUST_ITEMS = """<div class="hero-trust">
      <span><span class="ck">&#10003;</span> Licensed &amp; Certified Phlebotomists</span>
      <span><span class="ck">&#10003;</span> HIPAA-Compliant</span>
      <span><span class="ck">&#10003;</span> CLIA-Certified Partner Labs</span>
      <span><span class="ck">&#10003;</span> Same-Day Appointments</span>
    </div>"""

WHY_GRID = f"""<div class="diff-grid">
      <div class="diff-card"><span class="diff-num">01</span><h3>Same-Day Availability</h3><p>We frequently accommodate same-day appointments across metro Atlanta and Gwinnett County &mdash; 7 days a week, including early mornings and weekends.</p></div>
      <div class="diff-card"><span class="diff-num">02</span><h3>100% HIPAA Compliant</h3><p>Encrypted communication, secure results delivery, and zero third-party sharing without your authorization.</p></div>
      <div class="diff-card"><span class="diff-num">03</span><h3>Certified Phlebotomists</h3><p>Every Fastrak technician is licensed, background-checked, and experienced in mobile specimen collection for all age groups.</p></div>
      <div class="diff-card"><span class="diff-num">04</span><h3>Direct-Access Testing</h3><p>Order your own lab panels for hundreds of tests without a doctor&rsquo;s referral. We collect, you get results &mdash; simple.</p></div>
    </div>"""

AREA_PILLS = "\n      ".join(f'<span class="area-pill">{a}</span>' for a in AREAS)

FAQ_SCRIPT = """<script>
document.querySelectorAll('.fml-svc .faq-q').forEach(function(q){
  q.addEventListener('click',function(){this.closest('.faq').classList.toggle('open')});
});
</script>"""


def hero(pill, h1, sub, extra_trust=""):
    return f"""<div class="hero">
  <div class="hero-body">
    <div class="hero-pill">&#10003; {pill}</div>
    <h1>{h1}</h1>
    <p class="hero-sub">{sub}</p>
    <a class="btn-teal" href="{BOOK_URL}">Schedule an Appointment &rarr;</a>
    <a class="btn-ghost" href="tel:6785625244">Call {PHONE}</a>
    {TRUST_ITEMS}
  </div>
</div>"""


# ── Page builders ─────────────────────────────────────────────────────────────

def build_dna_georgia():
    return f"""{CSS_BASE}
<div class="fml-svc">
{hero(
  "Mobile DNA Testing &mdash; Georgia",
  "DNA Testing at Home<br><em>Anywhere in Georgia.</em>",
  "Court-admissible and peace-of-mind DNA testing collected at your home, office, or any location across Georgia. Paternity, maternity, sibling, immigration, and relationship testing — chain-of-custody guaranteed."
)}
{STATS_BAR}

<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">DNA Testing Services</span>
        <h2>Every Type of DNA Test, Collected at Your Location</h2>
        <p class="lead">Fastrak Mobile Lab performs all major DNA relationship tests at your Georgia home or office. Every collection follows strict AABB-standard chain-of-custody protocols &mdash; making results legally defensible when it matters most.</p>
        <ul class="feat-list">
          <li>
            <div class="feat-icon">&#129516;</div>
            <div><strong>Paternity &amp; Maternity Testing</strong><p>Legal and peace-of-mind paternity and maternity testing with court-admissible chain-of-custody. Results in 2&ndash;5 business days. Mobile collection at your location.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128106;</div>
            <div><strong>Sibling &amp; Family Relationship Testing</strong><p>Sibling, grandparent, aunt/uncle, and other family relationship DNA tests. Court-admissible and direct-access options available throughout Georgia.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#127981;</div>
            <div><strong>Immigration DNA Testing</strong><p>AABB-accredited specimen collection for USCIS and embassy-required immigration DNA tests. We coordinate chain-of-custody directly with accredited labs that meet federal requirements.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="feat-list" style="margin-top:0">
          <li>
            <div class="feat-icon">&#9878;&#65039;</div>
            <div><strong>Legal &amp; Court-Ordered DNA Testing</strong><p>Chain-of-custody collections for Georgia family court, child support, and custody proceedings. Strict documentation from collection to lab delivery.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128373;&#65039;</div>
            <div><strong>Discreet Peace-of-Mind Testing</strong><p>Private, confidential DNA testing for personal knowledge &mdash; not for legal use. Discreet collection, private results, and no court documentation required.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#127981;</div>
            <div><strong>Non-Invasive Prenatal Paternity (NIPP)</strong><p>Safe, non-invasive prenatal paternity testing using a maternal blood draw. Available as early as 7 weeks gestation &mdash; collected at your Georgia home.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="bg-lt">
  <div class="wrap" style="text-align:center">
    <span class="tag">The Process</span>
    <h2>How Mobile DNA Testing Works in Georgia</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto">From booking to legally defensible results &mdash; without leaving your home.</p>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><h3>Book &amp; Confirm</h3><p>Schedule online or by phone. We confirm all participants, required IDs, and documentation needs before your appointment.</p></div>
      <div class="step"><div class="step-num">2</div><h3>Mobile Collection</h3><p>A certified Fastrak collector comes to your location. Buccal swabs or blood draws are collected with full chain-of-custody documentation and photo ID verification.</p></div>
      <div class="step"><div class="step-num">3</div><h3>Results in 2&ndash;5 Days</h3><p>Specimens go directly to our AABB-accredited partner lab. Legal results are court-ready. Peace-of-mind results are delivered securely to you.</p></div>
    </div>
  </div>
</section>

<section class="bg-wh">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak</span>
      <h2>Why Georgia Chooses Fastrak for Mobile DNA Testing</h2>
      <p class="lead">Court-admissible results require more than a swab kit from the pharmacy. Fastrak brings AABB-standard protocols directly to your Georgia location.</p>
    </div>
    {WHY_GRID}
  </div>
</section>

<section id="areas" class="bg-lt">
  <div class="wrap">
    <div style="text-align:center;max-width:680px;margin:0 auto 40px">
      <span class="tag">Service Area</span>
      <h2>Mobile DNA Testing Across Metro Atlanta &amp; Georgia</h2>
      <p class="lead" style="margin-bottom:0">We provide mobile DNA testing throughout metro Atlanta, Gwinnett County, and surrounding Georgia communities within our 30-mile service radius.</p>
    </div>
    <div class="area-pills">{AREA_PILLS}</div>
  </div>
</section>

<div class="cta-band">
  <h2>Need Court-Admissible DNA Testing at Your Location?</h2>
  <p>Fastrak brings chain-of-custody DNA collection directly to your Georgia home or office &mdash; legal, discreet, and HIPAA-compliant.</p>
  <a class="btn-teal" href="{BOOK_URL}">Schedule DNA Testing &rarr;</a>
</div>

<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; DNA Testing at Home in Georgia</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px"></p>
    <div class="faq-wrap">
      <div class="faq"><div class="faq-q">Is mobile DNA testing in Georgia court-admissible?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; Fastrak's legal DNA collections follow AABB-standard chain-of-custody protocols and are admissible in Georgia family court, paternity proceedings, and USCIS immigration petitions. We document every step and verify all participants' identities with government-issued photo ID.</div></div>
      <div class="faq"><div class="faq-q">What's the difference between legal and peace-of-mind DNA testing?<span class="ico">+</span></div><div class="faq-a">Legal DNA testing follows chain-of-custody protocols required by courts &mdash; photo ID, witnessed collection, sealed samples with tamper-evident packaging. Peace-of-mind testing is for personal knowledge only and does not follow these protocols, so it cannot be used in court. Both are available as mobile collections.</div></div>
      <div class="faq"><div class="faq-q">How long does it take to get DNA test results in Georgia?<span class="ico">+</span></div><div class="faq-a">Standard legal DNA results are typically available in 3&ndash;5 business days. Peace-of-mind results are often faster. Expedited processing is available for an additional fee if you need results sooner.</div></div>
      <div class="faq"><div class="faq-q">Can all parties be tested at different locations?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; Fastrak can coordinate separate mobile collections at different locations for different participants. Each collection follows the same chain-of-custody protocol and the samples are tracked together through the lab process.</div></div>
      <div class="faq"><div class="faq-q">Do you offer immigration DNA testing for USCIS petitions?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; we provide AABB-accredited specimen collection for USCIS family-based immigration petitions. We coordinate with labs that meet all federal requirements and can provide documentation in the format required by U.S. embassies and consulates.</div></div>
    </div>
  </div>
</section>
{FAQ_SCRIPT}
</div>"""


def build_drug_atlanta():
    return f"""{CSS_BASE}
<div class="fml-svc">
{hero(
  "Mobile Drug Testing &mdash; Atlanta, GA",
  "Mobile Drug Testing<br><em>at Your Atlanta Location.</em>",
  "DOT and non-DOT urine, saliva, and hair follicle drug testing throughout Atlanta and metro Georgia — collected at your business, job site, or home. HIPAA-compliant with full chain-of-custody."
)}
{STATS_BAR}

<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">Drug Testing Services</span>
        <h2>Every Drug Testing Service, Brought to Your Atlanta Location</h2>
        <p class="lead">From DOT-regulated commercial drivers to pre-employment screening for corporate HR teams, Fastrak Mobile Lab handles all drug testing collection types at your location &mdash; no clinic visit required.</p>
        <ul class="feat-list">
          <li>
            <div class="feat-icon">&#128203;</div>
            <div><strong>DOT Drug &amp; Alcohol Testing</strong><p>FMCSA, FAA, FTA, and FRA-compliant drug and alcohol testing for CDL drivers and DOT-regulated employees. Mobile collection at your fleet yard, office, or job site throughout Atlanta.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#127970;</div>
            <div><strong>Pre-Employment Drug Screening</strong><p>Fast, HIPAA-compliant pre-employment drug screens for Atlanta businesses. Urine, saliva, and hair follicle panels &mdash; collected onsite at your office with same-day scheduling.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128202;</div>
            <div><strong>Random &amp; Reasonable Suspicion Testing</strong><p>We support employer drug-free workplace programs with random selection and reasonable suspicion collections. Mobile service means zero disruption to your Atlanta operations.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="feat-list" style="margin-top:0">
          <li>
            <div class="feat-icon">&#128680;</div>
            <div><strong>Post-Accident Drug Testing</strong><p>Rapid post-accident collection at your location within the DOT-required 8-hour window. We respond quickly to minimize compliance risk after a workplace incident.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128137;</div>
            <div><strong>Hair Follicle Testing</strong><p>90-day detection window. Hair follicle drug testing is increasingly required by Atlanta employers for executive-level and safety-sensitive positions. Mobile collection at your office.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128101;</div>
            <div><strong>Personal &amp; Legal Drug Testing</strong><p>Private drug testing for personal use, legal proceedings, child custody cases, and probation compliance. HIPAA-compliant, discreet, and mobile throughout metro Atlanta.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="bg-lt">
  <div class="wrap" style="text-align:center">
    <span class="tag">The Process</span>
    <h2>How Mobile Drug Testing Works in Atlanta</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto">Compliant, fast, and minimally disruptive to your Atlanta business operations.</p>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><h3>Schedule or Call</h3><p>Book online or call {PHONE}. We confirm the test type, collection method, and arrive at your Atlanta location with all required supplies and documentation.</p></div>
      <div class="step"><div class="step-num">2</div><h3>On-Site Collection</h3><p>A certified collector arrives at your business, job site, or home. Collection follows all DOT and non-DOT protocols with strict chain-of-custody documentation.</p></div>
      <div class="step"><div class="step-num">3</div><h3>Results to MRO or Employer</h3><p>Specimens go to our SAMHSA-certified partner lab. Results are delivered to your MRO or HR team, typically within 24&ndash;72 hours for negative screens.</p></div>
    </div>
  </div>
</section>

<section class="bg-wh">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak</span>
      <h2>Atlanta&rsquo;s Mobile Drug Testing Solution</h2>
      <p class="lead">No more sending employees off-site. No lost productivity. Fastrak brings compliant drug testing directly to your Atlanta business &mdash; faster and more convenient than any clinic.</p>
    </div>
    {WHY_GRID}
  </div>
</section>

<section id="areas" class="bg-lt">
  <div class="wrap">
    <div style="text-align:center;max-width:680px;margin:0 auto 40px">
      <span class="tag">Service Area</span>
      <h2>Mobile Drug Testing Across Metro Atlanta</h2>
      <p class="lead" style="margin-bottom:0">We serve Atlanta businesses and residents throughout metro Atlanta and Gwinnett County within our 30-mile service radius.</p>
    </div>
    <div class="area-pills">{AREA_PILLS}</div>
  </div>
</section>

<div class="cta-band">
  <h2>Need Fast, Compliant Drug Testing at Your Atlanta Location?</h2>
  <p>Fastrak brings DOT and non-DOT drug testing directly to your business or home &mdash; same-day available, HIPAA-compliant, and fully documented.</p>
  <a class="btn-teal" href="{BOOK_URL}">Schedule Drug Testing &rarr;</a>
</div>

<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; Mobile Drug Testing in Atlanta, GA</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px"></p>
    <div class="faq-wrap">
      <div class="faq"><div class="faq-q">Are mobile drug tests DOT-compliant in Atlanta?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; Fastrak's DOT collections follow all FMCSA, FAA, FTA, and FRA chain-of-custody requirements. Our collectors are trained in federal drug testing procedures and our partner labs are SAMHSA-certified.</div></div>
      <div class="faq"><div class="faq-q">Can you set up a drug-free workplace program for our Atlanta business?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; we work with Atlanta employers on pre-employment, random, post-accident, and return-to-duty drug testing programs. We can design a schedule that fits your workforce size and compliance requirements. Call to discuss a business account.</div></div>
      <div class="faq"><div class="faq-q">How quickly can you respond for a post-accident drug test in Atlanta?<span class="ico">+</span></div><div class="faq-a">We aim for same-day response for post-accident situations. For DOT post-accident tests, the 8-hour (alcohol) and 32-hour (drug) windows start at the time of the accident &mdash; call us immediately after securing the scene so we can dispatch a collector as fast as possible.</div></div>
      <div class="faq"><div class="faq-q">What types of panels do you offer for Atlanta pre-employment screening?<span class="ico">+</span></div><div class="faq-a">We offer standard 5-panel and 10-panel urine drug screens, extended panels, oral fluid (saliva), and hair follicle testing. DOT 5-panel is available for regulated employees. We work with your HR team to determine the right panel for your industry and position type.</div></div>
    </div>
  </div>
</section>
{FAQ_SCRIPT}
</div>"""


def build_concierge_atlanta():
    return f"""{CSS_BASE}
<div class="fml-svc">
{hero(
  "Concierge Mobile Phlebotomy &mdash; Atlanta",
  "Concierge Lab Collections<br><em>Brought to Your Door.</em>",
  "Premium mobile phlebotomy for Atlanta&rsquo;s executive, physician-partner, and private-pay patients. Hospital-grade specimen collection at your home, office, or facility — discreet, precise, and scheduled on your terms."
)}
{STATS_BAR}

<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">Concierge Services</span>
        <h2>Premium Mobile Lab Service for Atlanta&rsquo;s Discerning Patients</h2>
        <p class="lead">Fastrak&rsquo;s concierge mobile phlebotomy service is built for patients who expect more &mdash; executives, physicians&rsquo; VIP patients, and anyone who values their time. Same-day, early morning, evening, and weekend appointments available throughout Atlanta.</p>
        <ul class="feat-list">
          <li>
            <div class="feat-icon">&#129354;</div>
            <div><strong>Private Physician-Ordered Lab Collections</strong><p>We coordinate directly with your physician&rsquo;s office to collect ordered labs at your home or office &mdash; sending results securely back to your provider without a clinic visit.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#10024;</div>
            <div><strong>Executive Wellness &amp; Longevity Panels</strong><p>Comprehensive wellness panels including CBC, metabolic, hormone, thyroid, lipid, cardiovascular risk, and micronutrient markers &mdash; many available without a doctor&rsquo;s order through direct-access testing.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128302;</div>
            <div><strong>Specialty &amp; Functional Medicine Collections</strong><p>Food sensitivity (Alcat/ELISA), organic acids, DUTCH hormone panels, heavy metals, and functional medicine test kits. We collect at your Atlanta location and ship to any specialty lab.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="feat-list" style="margin-top:0">
          <li>
            <div class="feat-icon">&#127968;</div>
            <div><strong>In-Home IV Therapy Support Collections</strong><p>Pre-IV wellness blood draws for concierge medicine and IV therapy clients. We coordinate with your IV therapy provider or physician for pre-treatment lab requirements.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128205;</div>
            <div><strong>High-Rise &amp; Estate Collections</strong><p>We regularly serve Buckhead estates, Midtown high-rises, and Sandy Springs executive homes. Our phlebotomists understand secured buildings and private residence protocols.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128203;</div>
            <div><strong>Clinical Trial &amp; Research Collections</strong><p>Protocol-compliant specimen collection for clinical trials, pharmaceutical research, and IRB-approved studies. Chain-of-custody and temperature-sensitive transport available.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="bg-lt">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak Concierge</span>
      <h2>A Higher Standard of Mobile Lab Service</h2>
      <p class="lead">Concierge phlebotomy isn&rsquo;t just about convenience &mdash; it&rsquo;s about precision, discretion, and a personalized experience that a clinic can&rsquo;t provide.</p>
    </div>
    {WHY_GRID}
  </div>
</section>

<div class="cta-band">
  <h2>Book Your Atlanta Concierge Phlebotomy Appointment</h2>
  <p>Premium mobile lab service, scheduled on your terms. Early morning, evening, and weekend appointments available throughout Atlanta and metro Georgia.</p>
  <a class="btn-teal" href="{BOOK_URL}">Schedule Concierge Service &rarr;</a>
</div>

<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; Concierge Mobile Phlebotomy in Atlanta</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px"></p>
    <div class="faq-wrap">
      <div class="faq"><div class="faq-q">What makes concierge phlebotomy different from standard mobile phlebotomy?<span class="ico">+</span></div><div class="faq-a">Concierge phlebotomy prioritizes flexibility, discretion, and specialty collection capabilities. We accommodate non-standard scheduling, specialty lab kits, functional medicine panels, and physician-partnership arrangements that standard mobile phlebotomy services don&rsquo;t support.</div></div>
      <div class="faq"><div class="faq-q">Can you coordinate with my Atlanta physician&rsquo;s office for lab orders?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; we work directly with concierge physicians, functional medicine doctors, and specialist offices throughout Atlanta. We collect ordered labs, maintain proper documentation, and ship to any designated lab &mdash; sending results directly back to your provider.</div></div>
      <div class="faq"><div class="faq-q">Do you offer early morning fasting blood draws for Atlanta executives?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; early morning fasting draws before your workday are one of our most popular concierge services in Atlanta. We accommodate 6am, 7am, and 8am appointments for patients who need fasting labs without disrupting their schedule.</div></div>
      <div class="faq"><div class="faq-q">Can you collect specialty lab kits at my Atlanta home?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; we handle specialty collection kits from any lab including functional medicine panels (DUTCH, GI-MAP, Vibrant America, Genova), food sensitivity kits, and direct-to-consumer test kits. Bring your kit &mdash; we collect and ship it for you.</div></div>
    </div>
  </div>
</section>
{FAQ_SCRIPT}
</div>"""


def build_corporate_atlanta():
    return f"""{CSS_BASE}
<div class="fml-svc">
{hero(
  "Corporate Mobile Lab Services &mdash; Atlanta",
  "Mobile Lab Services for<br><em>Atlanta Businesses.</em>",
  "Onsite drug testing, pre-employment screening, DOT compliance, and occupational health lab collections for Atlanta corporate clients. We come to your office, fleet yard, or job site — minimizing disruption to your operations."
)}
{STATS_BAR}

<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">Corporate Services</span>
        <h2>Mobile Lab Collections That Come to Your Atlanta Workplace</h2>
        <p class="lead">Sending employees off-site for drug tests and physicals costs time and money. Fastrak Mobile Lab brings every collection directly to your Atlanta business &mdash; with same-day scheduling, HIPAA compliance, and chain-of-custody documentation.</p>
        <ul class="feat-list">
          <li>
            <div class="feat-icon">&#128203;</div>
            <div><strong>DOT Drug &amp; Alcohol Compliance</strong><p>FMCSA, FAA, FTA, and FRA-compliant drug and alcohol testing programs for Atlanta transportation and logistics businesses. Pre-employment, random, post-accident, and return-to-duty collections at your facility.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#127970;</div>
            <div><strong>Pre-Employment Drug Screening</strong><p>Fast onsite drug screens for new hires. We schedule around your HR onboarding process and deliver results within 24&ndash;72 hours, keeping your hiring pipeline moving.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128101;</div>
            <div><strong>Random Drug Testing Programs</strong><p>We support employer drug-free workplace programs with random selection pools, scheduled random draws, and compliant collection &mdash; zero disruption to your Atlanta operations.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="feat-list" style="margin-top:0">
          <li>
            <div class="feat-icon">&#128680;</div>
            <div><strong>Post-Accident &amp; Reasonable Suspicion Testing</strong><p>Rapid response for post-accident and reasonable suspicion collections within DOT and OSHA compliance windows. Call us immediately &mdash; we dispatch fast.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#10084;&#65039;</div>
            <div><strong>Employee Wellness &amp; Health Panels</strong><p>Biometric screenings, wellness panels, and annual health checks for Atlanta corporate wellness programs. We set up onsite collection stations for large employee groups.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128300;</div>
            <div><strong>Occupational &amp; Clinical Trial Collections</strong><p>Occupational exposure monitoring, medical surveillance labs, and clinical trial specimen collection for Atlanta&rsquo;s healthcare and pharmaceutical employers.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="bg-lt">
  <div class="wrap" style="text-align:center">
    <span class="tag">The Process</span>
    <h2>How Corporate Mobile Lab Service Works</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto">Simple, scalable, and built around your Atlanta business schedule.</p>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><h3>Set Up Your Account</h3><p>Call or email to discuss your testing needs. We create a business account, agree on collection types, and set up your billing and scheduling preferences.</p></div>
      <div class="step"><div class="step-num">2</div><h3>We Come Onsite</h3><p>A certified Fastrak collector arrives at your Atlanta business with all supplies. Collections are fast, documented, and fully chain-of-custody compliant.</p></div>
      <div class="step"><div class="step-num">3</div><h3>Results to HR or MRO</h3><p>Results are delivered directly to your HR team or Medical Review Officer &mdash; typically within 24&ndash;72 hours for negative screens, faster for urgent needs.</p></div>
    </div>
  </div>
</section>

<section class="bg-wh">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak Corporate</span>
      <h2>Atlanta&rsquo;s Mobile Corporate Lab Partner</h2>
      <p class="lead">No scheduling employees off-site. No lost hours. No compliance gaps. Fastrak brings every collection directly to your Atlanta business &mdash; on your schedule.</p>
    </div>
    {WHY_GRID}
  </div>
</section>

<div class="cta-band">
  <h2>Set Up Onsite Lab Services for Your Atlanta Business</h2>
  <p>Call or book today to discuss a corporate account. We serve Atlanta businesses of all sizes &mdash; from 5-person teams to large enterprise employers.</p>
  <a class="btn-teal" href="{BOOK_URL}">Contact Us &rarr;</a>
</div>

<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; Corporate Mobile Lab Services in Atlanta</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px"></p>
    <div class="faq-wrap">
      <div class="faq"><div class="faq-q">Can you set up a recurring drug testing program for our Atlanta business?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; we work with Atlanta employers on pre-employment, random, post-accident, and return-to-duty programs. We design a schedule around your workforce size, DOT requirements, and compliance needs. Call us to set up a business account.</div></div>
      <div class="faq"><div class="faq-q">Do you offer volume pricing for large Atlanta employers?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; we offer competitive volume pricing for businesses with ongoing drug testing and occupational health needs. Contact us to discuss a corporate account with preferred rates and priority scheduling.</div></div>
      <div class="faq"><div class="faq-q">Are your collectors certified for DOT collections in Georgia?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; all Fastrak collectors performing DOT collections are trained per DOT 49 CFR Part 40 requirements. Our partner labs are SAMHSA-certified and our chain-of-custody documentation meets all federal standards.</div></div>
    </div>
  </div>
</section>
{FAQ_SCRIPT}
</div>"""


def build_athome_blood_draw():
    return f"""{CSS_BASE}
<div class="fml-svc">
{hero(
  "At-Home Blood Draw Service &mdash; Atlanta, GA",
  "At-Home Blood Draws<br><em>Across Metro Atlanta.</em>",
  "Certified phlebotomists come to your Atlanta home, office, or facility for blood draws, diagnostic panels, and specialty lab collections — 7 days a week, HIPAA-compliant, and processed through CLIA-certified partner labs."
)}
{STATS_BAR}

<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">At-Home Blood Draw Services</span>
        <h2>Every Lab Test, Collected at Your Atlanta Location</h2>
        <p class="lead">Whether you need a routine annual panel or a complex specialty draw, Fastrak Mobile Lab handles the collection at your Atlanta home or office &mdash; then sends your specimen directly to the lab. No waiting rooms, no parking, no wasted time.</p>
        <ul class="feat-list">
          <li>
            <div class="feat-icon">&#129754;</div>
            <div><strong>Physician-Ordered Blood Draws</strong><p>Bring your lab order &mdash; we collect it at your Atlanta location and send it to any designated lab. All major lab requisitions accepted including Quest, LabCorp, and specialty labs.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#10024;</div>
            <div><strong>Direct-Access Lab Testing</strong><p>Order hundreds of panels without a doctor&rsquo;s order &mdash; wellness, thyroid, hormone, lipid, vitamin, and metabolic panels available for direct-access testing throughout Atlanta.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128137;</div>
            <div><strong>Early Morning Fasting Draws</strong><p>Many panels require fasting &mdash; we offer early morning appointments before your workday so you can fast overnight and have labs done before breakfast, without disrupting your schedule.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="feat-list" style="margin-top:0">
          <li>
            <div class="feat-icon">&#128106;</div>
            <div><strong>Pediatric &amp; Difficult-Stick Blood Draws</strong><p>Our phlebotomists are experienced in pediatric and difficult-stick collections &mdash; providing a calm, gentle, in-home experience for children and anxious patients who struggle with clinic draws.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128704;</div>
            <div><strong>Homebound &amp; Senior Blood Draws</strong><p>Mobile phlebotomy is essential for Atlanta&rsquo;s homebound and elderly patients. We serve assisted living facilities, nursing homes, and private residences throughout metro Atlanta.</p></div>
          </li>
          <li>
            <div class="feat-icon">&#128300;</div>
            <div><strong>Specialty &amp; Functional Medicine Kits</strong><p>We collect functional medicine and specialty lab kits at your Atlanta location &mdash; DUTCH, GI-MAP, Vibrant, Genova, food sensitivity panels, and more.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="bg-lt">
  <div class="wrap" style="text-align:center">
    <span class="tag">The Process</span>
    <h2>How At-Home Blood Draws Work in Atlanta</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto">Three steps. No waiting room. No driving.</p>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><h3>Book Online or Call</h3><p>Schedule your at-home blood draw in minutes. We confirm your lab order, fasting requirements, and any special instructions before your appointment.</p></div>
      <div class="step"><div class="step-num">2</div><h3>Phlebotomist Comes to You</h3><p>A certified Fastrak phlebotomist arrives at your Atlanta home or office with all supplies. Collection is fast, clean, and follows hospital-grade protocols.</p></div>
      <div class="step"><div class="step-num">3</div><h3>Results in 24&ndash;72 Hours</h3><p>Your specimen goes directly to the designated lab. Results are delivered to you or your provider securely &mdash; no follow-up visit required.</p></div>
    </div>
  </div>
</section>

<section class="bg-wh">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak</span>
      <h2>Atlanta&rsquo;s At-Home Blood Draw Specialist</h2>
      <p class="lead">Fastrak Mobile Lab makes lab work as easy as ordering delivery. Professional, HIPAA-compliant, and available 7 days a week throughout metro Atlanta.</p>
    </div>
    {WHY_GRID}
  </div>
</section>

<section id="areas" class="bg-lt">
  <div class="wrap">
    <div style="text-align:center;max-width:680px;margin:0 auto 40px">
      <span class="tag">Service Area</span>
      <h2>At-Home Blood Draws Across Metro Atlanta</h2>
      <p class="lead" style="margin-bottom:0">We provide at-home blood draw service throughout metro Atlanta and surrounding communities within our 30-mile service radius.</p>
    </div>
    <div class="area-pills">{AREA_PILLS}</div>
  </div>
</section>

<div class="cta-band">
  <h2>Book Your At-Home Blood Draw in Atlanta Today</h2>
  <p>Stop driving to the lab. Stop sitting in waiting rooms. Book your Atlanta at-home blood draw &mdash; certified, HIPAA-compliant, and results in 24&ndash;72 hours.</p>
  <a class="btn-teal" href="{BOOK_URL}">Schedule a Blood Draw &rarr;</a>
</div>

<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; At-Home Blood Draw in Atlanta, GA</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px"></p>
    <div class="faq-wrap">
      <div class="faq"><div class="faq-q">Do I need a doctor&rsquo;s order for an at-home blood draw in Atlanta?<span class="ico">+</span></div><div class="faq-a">Not always. If you have a physician&rsquo;s lab order, bring it &mdash; we collect it at your Atlanta home. If you don&rsquo;t have an order, Fastrak also offers direct-access testing for hundreds of wellness, thyroid, hormone, vitamin, lipid, and metabolic panels that you can order yourself.</div></div>
      <div class="faq"><div class="faq-q">Which labs do you send Atlanta blood draw specimens to?<span class="ico">+</span></div><div class="faq-a">We work with Quest Diagnostics, LabCorp, and a network of CLIA-certified specialty labs. If your physician uses a specific lab, let us know when booking and we&rsquo;ll make sure we have the right requisition forms and transport requirements.</div></div>
      <div class="faq"><div class="faq-q">How long does it take to get blood test results in Atlanta?<span class="ico">+</span></div><div class="faq-a">Most routine panels are resulted within 24&ndash;72 hours. Specialty panels may take 5&ndash;7 business days. Your results are sent directly to your provider and/or to you securely, depending on how you ordered the test.</div></div>
      <div class="faq"><div class="faq-q">Can you do pediatric blood draws at home in Atlanta?<span class="ico">+</span></div><div class="faq-a">Yes &mdash; pediatric blood draws at home are one of our most appreciated services. Our phlebotomists are experienced with children and use techniques that minimize discomfort. The familiar home setting makes the experience far less stressful for kids than a clinic.</div></div>
    </div>
  </div>
</section>
{FAQ_SCRIPT}
</div>"""


SERVICE_PAGES = [
    {
        "id": 1357, "focus_kw": "DNA testing at home Georgia",
        "title": "DNA Testing at Home in Georgia | Mobile Collection | Fastrak Mobile Lab",
        "desc": "Court-admissible and peace-of-mind DNA testing collected at your Georgia home or office. Paternity, immigration, sibling & legal testing. Book same-day.",
        "builder": build_dna_georgia,
    },
    {
        "id": 1356, "focus_kw": "mobile drug testing Atlanta GA",
        "title": "Mobile Drug Testing Atlanta GA | DOT & Non-DOT | Fastrak Mobile Lab",
        "desc": "Mobile DOT and non-DOT drug testing across Atlanta, GA. Onsite collection at your business or home — pre-employment, random, post-accident. Call Fastrak.",
        "builder": build_drug_atlanta,
    },
    {
        "id": 1359, "focus_kw": "concierge mobile phlebotomy Atlanta",
        "title": "Concierge Mobile Phlebotomy Atlanta GA | Executive Lab Service | Fastrak",
        "desc": "Premium concierge mobile phlebotomy for Atlanta executives and physician-partner patients. Same-day, early morning & specialty collections at your location.",
        "builder": build_concierge_atlanta,
    },
    {
        "id": 1358, "focus_kw": "corporate mobile lab services Atlanta",
        "title": "Corporate Mobile Lab Services Atlanta GA | Onsite Drug Testing | Fastrak",
        "desc": "Mobile onsite drug testing, DOT compliance & occupational health collections for Atlanta businesses. Same-day available. Call Fastrak Mobile Lab.",
        "builder": build_corporate_atlanta,
    },
    {
        "id": 368, "focus_kw": "at-home blood draw Atlanta GA",
        "title": "At-Home Blood Draw Atlanta GA | Mobile Phlebotomy Service | Fastrak",
        "desc": "Certified mobile phlebotomists come to your Atlanta home or office for blood draws, diagnostic panels & specialty labs. HIPAA-compliant. Book same-day.",
        "builder": build_athome_blood_draw,
    },
]


def deploy_service(p):
    html = p["builder"]()
    content = f"<!-- wp:html -->\n{html}\n<!-- /wp:html -->"
    r1 = requests.post(
        f"{WP_SITE}/wp-json/wp/v2/pages/{p['id']}",
        headers=HJ, json={"content": content}, timeout=30,
    )
    print(f"  Content:   HTTP {r1.status_code}")
    r2 = requests.post(
        f"{WP_SITE}/wp-json/rankmath/v1/updateMeta",
        headers=HJ,
        json={
            "objectID": p["id"], "objectType": "page",
            "meta": {
                "rank_math_title":         p["title"],
                "rank_math_description":   p["desc"],
                "rank_math_focus_keyword": p["focus_kw"],
            },
        },
        timeout=15,
    )
    print(f"  RankMath:  HTTP {r2.status_code}")
    return r1.ok


if __name__ == "__main__":
    ok, fail = 0, 0
    for p in SERVICE_PAGES:
        print(f"\n[{p['id']}] {p['focus_kw']}")
        if deploy_service(p):
            ok += 1
        else:
            fail += 1
        time.sleep(1.2)
    print(f"\n{'='*50}")
    print(f"Done: {ok} deployed, {fail} failed")
    print(f"{'='*50}")
