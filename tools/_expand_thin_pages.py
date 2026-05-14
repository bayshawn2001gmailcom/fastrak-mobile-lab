"""
Expand the 7 thin service pages by appending new H2+paragraph sections
immediately before the <!-- fastrak-pillar-link --> marker.

All existing HTML (page builder structure, images, CTAs) is left 100% untouched.
New content is appended below it — same technique used by all prior patch scripts.

Run: python tools/_expand_thin_pages.py
"""
import os, sys, base64, requests
from pathlib import Path

home_env = Path.home() / ".env"
if home_env.exists():
    for line in home_env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Missing WP credentials")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
H_JSON = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
H_FORM = {"Authorization": f"Basic {creds}"}

PILLAR_MARKER   = "<!-- fastrak-pillar-link -->"
EXPAND_MARKER   = "<!-- fastrak-expanded -->"

# ---------------------------------------------------------------------------
# Expansion content keyed by page ID
# Each value is raw HTML inserted BEFORE the pillar-link marker.
# No existing HTML is touched.
# ---------------------------------------------------------------------------
EXPANSIONS = {

    368: """
<h2>What Lab Tests Can Be Done at Home?</h2>
<p>Our mobile phlebotomists collect virtually any specimen your physician has ordered. Common at-home blood draw tests include complete blood count (CBC), comprehensive metabolic panel (CMP), lipid and cholesterol screening, thyroid panels (TSH, T3, T4), hormone levels, HbA1c for diabetes monitoring, vitamin D and B12, sexually transmitted infection (STI) panels, and coagulation studies. If your doctor has ordered it, we can collect it at your Atlanta location.</p>

<h2>How the At-Home Blood Draw Process Works</h2>
<p>Booking is straightforward. Select your service online, choose a date and time that works for you, and enter your address. A licensed Fastrak Mobile Lab phlebotomist arrives on time with all necessary collection equipment — most blood draws are complete in under 10 minutes. Your specimen is transported directly to an accredited reference laboratory, and results are returned through your ordering physician or our secure results portal, typically within 24–72 hours.</p>

<h2>Does Insurance Cover At-Home Blood Draws in Atlanta?</h2>
<p>Lab processing fees are billed to your insurance the same way as any in-clinic draw. Most major plans — including Aetna, BlueCross BlueShield, Cigna, UnitedHealthcare, and Humana — cover these fees. The mobile service fee, which covers the phlebotomist traveling to your location, is a separate out-of-pocket charge. We provide full pricing transparency before you confirm your appointment so there are no surprises.</p>
""",

    375: """
<h2>Types of Specialty Kits We Handle</h2>
<p>Specialty collection kits cover a broad range of advanced diagnostics. Our mobile phlebotomists regularly handle kits for genetic and pharmacogenomic panels, comprehensive hormone testing (including DUTCH panels and salivary hormone kits), food sensitivity and allergy panels, autoimmune and inflammatory marker testing, heavy metals and toxin screens, and microbiome or stool collection kits sent from reference labs. If your physician or lab has provided a kit with specific instructions, we follow those protocols precisely at your home or office.</p>

<h2>Why Proper Specialty Kit Collection Matters</h2>
<p>Specialty tests are often ordered when routine bloodwork is not sufficient to answer a clinical question. Improper collection — the wrong time of day, incorrect preservatives, or improper transport temperature — can invalidate results and require a repeat collection. Our phlebotomists review kit instructions before every appointment and confirm compliance at each step to protect the integrity of your specimen and your physician's ability to interpret results accurately.</p>

<h2>Who Uses Specialty Kit Collection Services?</h2>
<p>Patients working with integrative medicine physicians, functional medicine practitioners, naturopathic doctors, and concierge practices frequently require specialty kits that are unavailable at standard draw sites. Research participants, clinical trial patients, and individuals using direct-to-consumer testing platforms that ship collection kits also benefit from professional at-home collection support. If you are unsure whether your kit qualifies, contact us before your appointment and we will confirm.</p>
""",

    385: """
<h2>What Pre-Employment Screening Includes</h2>
<p>Our mobile pre-employment screening services cover the full range of employer requirements. Standard offerings include 5-panel, 10-panel, and 12-panel urine drug screens, oral fluid (saliva) drug testing, hair follicle drug testing, blood alcohol testing, and occupational health blood panels. All collections follow chain-of-custody procedures, and non-negative results are reviewed by a certified Medical Review Officer (MRO) before being reported to the employer.</p>

<h2>DOT and Non-DOT Compliance Testing</h2>
<p>We perform both DOT-regulated and non-DOT pre-employment drug testing for employers across Atlanta and Gwinnett County. DOT-compliant collections adhere to 49 CFR Part 40 requirements and are accepted by the FMCSA, FAA, FTA, and other federal DOT agencies. Non-DOT collections are tailored to your company's drug-free workplace policy. All testing uses certified laboratories and produces legally defensible documentation for your HR files.</p>

<h2>Fast Turnaround for Hiring Timelines</h2>
<p>Hiring timelines are tight, and waiting for a new employee to schedule a lab visit creates unnecessary delays. With Fastrak Mobile Lab, applicants are tested at their home or your office within 24–48 hours of scheduling. Negative results are typically returned within 1–2 business days. We serve employers, staffing agencies, and HR teams throughout metro Atlanta, making the pre-employment process faster without sacrificing accuracy or compliance.</p>
""",

    395: """
<h2>At-Home DNA and Paternity Testing in Atlanta</h2>
<p>Our DNA testing services include at-home specimen collection for paternity testing, siblingship testing, grandparentage testing, and ancestral DNA panels. We offer both personal-knowledge collections — for private peace of mind — and court-admissible legal collections that follow strict chain-of-custody documentation required for use in Georgia family court, child support proceedings, and immigration cases. All DNA specimens are processed through AABB-accredited partner laboratories.</p>

<h2>Results You Can Count On</h2>
<p>Accuracy and discretion are non-negotiable in drug and DNA testing. Every collection follows documented chain-of-custody protocols — specimen identity is confirmed, sealed, and documented at the point of collection. This prevents tampering, ensures legal admissibility, and gives you results you can trust. Negative drug test results are typically returned within 24–48 hours. DNA paternity test results are returned within 3–5 business days after specimen receipt at the laboratory.</p>

<h2>Serving Atlanta and Gwinnett County</h2>
<p>Fastrak Mobile Lab provides mobile drug and DNA testing throughout metro Atlanta and Gwinnett County. We come to your home, office, or any mutually agreed location — no clinic visit required. We work with individuals, employers, attorneys, and HR teams who need discreet, professional collection services. We also provide dedicated <a href="https://fastrakmobilelab.com/mobile-drug-testing-gwinnett-county-ga/">mobile drug testing throughout Gwinnett County</a> and <a href="https://fastrakmobilelab.com/dna-testing-gwinnett-county-ga/">DNA testing services in Gwinnett County</a>.</p>
""",

    401: """
<h2>Wellness Panels Available Through Fastrak Mobile Lab</h2>
<p>Our health and wellness testing menu covers the core panels most commonly requested for proactive monitoring. Available panels include complete blood count (CBC), comprehensive metabolic panel (CMP), lipid panel with full cholesterol breakdown, thyroid function (TSH, free T3, free T4), testosterone and estrogen panels, HbA1c for blood sugar management, vitamin D and B12 levels, iron studies and ferritin, C-reactive protein (CRP) for inflammation, and complete urinalysis. Most panels can be collected together in a single visit.</p>

<h2>Who Benefits from Mobile Wellness Testing?</h2>
<p>Health and wellness panels are not just for people who are sick. Busy professionals use them to stay ahead of chronic conditions before symptoms appear. Athletes track hormone and recovery markers to optimize performance. Seniors monitor kidney, liver, and thyroid function between annual physicals. Individuals managing weight, energy, or mood concerns use panel results to guide nutrition and lifestyle decisions. Our mobile service makes staying on top of these numbers practical — no scheduling around a clinic's hours or sitting in a waiting room.</p>

<h2>How to Get Started with a Wellness Panel</h2>
<p>If your physician has ordered a panel, bring your lab order to your appointment and we will collect exactly what was prescribed. If you would like to order your own tests without a physician referral, visit our <a href="https://fastrakmobilelab.com/order-your-own-lab-tests-at-home/">order your own test</a> page. Most wellness panel results are returned within 24–72 hours through your provider or our secure results portal.</p>
""",

    407: """
<h2>Who Our Concierge Services Are Built For</h2>
<p>Our concierge and physician partnership services are designed for patients and practices that require more than a standard lab visit can deliver. Common clients include homebound patients recovering from surgery or managing chronic illness, elderly individuals who no longer drive or find clinic visits physically demanding, executives and professionals who schedule care around demanding calendars, and concierge medical practices that want to extend premium in-home services to their patient panel without adding clinical overhead.</p>

<h2>How We Support Physician Practices</h2>
<p>Fastrak Mobile Lab functions as a white-glove extension of your practice. We coordinate directly with your clinical team to confirm orders, schedule at the patient's convenience, collect specimens with precise protocol adherence, and deliver chain-of-custody documentation with every result. Turnaround time for most panels is 24–72 hours. We serve physicians in internal medicine, concierge medicine, functional medicine, oncology supportive care, and geriatric care throughout metro Atlanta and Gwinnett County.</p>

<h2>Scheduling Concierge Appointments</h2>
<p>Concierge appointments are available with early-morning, evening, and weekend time slots to accommodate patient schedules that do not align with standard clinic hours. To coordinate recurring draws or establish an ongoing patient service arrangement for your practice, contact us directly. We will work with your team to set up a reliable protocol that delivers consistent, professional results at every patient visit.</p>
""",

    413: """
<h2>What Tests Are Available Without a Doctor's Order?</h2>
<p>Through our direct-to-consumer testing partnership, you can order a wide range of lab panels without a physician referral. Available tests include comprehensive metabolic and lipid panels, thyroid function, testosterone and hormone levels, vitamin D and B12, iron studies, HbA1c, sexually transmitted infection (STI) panels, food sensitivity screens, heavy metals, and more. Browse the full test catalog on our partner portal and select exactly what you need.</p>

<h2>How the Process Works</h2>
<p>Once you select your test and complete your order through our partner portal, we schedule a mobile collection visit at your home or office. A licensed Fastrak phlebotomist arrives at your appointment time with all collection supplies — no clinic visit required. Your specimen is transported to an accredited reference laboratory for processing. Most results are delivered electronically within 24–72 hours, with a copy sent directly to you through our partner's secure results platform.</p>

<h2>Private, Confidential, and on Your Terms</h2>
<p>Direct-to-consumer testing is fully confidential. Results belong to you and are not automatically shared with your insurance carrier or primary care provider — you decide what to do with the information. This makes it an ideal option for individuals monitoring sensitive health markers, checking in between annual physicals, or seeking a second opinion on a panel their physician has already ordered. If your results indicate something that requires follow-up, we encourage you to share them with your healthcare provider.</p>
""",
}

# ---------------------------------------------------------------------------
# WordPress helpers
# ---------------------------------------------------------------------------

def get_raw(pid):
    r = requests.get(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                     headers=H_FORM,
                     params={"context": "edit", "_fields": "slug,content"},
                     timeout=20)
    r.raise_for_status()
    data = r.json()
    return data["slug"], data["content"]["raw"]


def patch(pid, raw):
    r = requests.post(f"{WP_SITE}/wp-json/wp/v2/pages/{pid}",
                      headers=H_JSON, json={"content": raw}, timeout=30)
    r.raise_for_status()
    return r.status_code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Expanding {len(EXPANSIONS)} thin pages...\n")
    for pid, new_html in EXPANSIONS.items():
        try:
            slug, raw = get_raw(pid)

            if EXPAND_MARKER in raw:
                print(f"  ID {pid:5}  already-expanded  /{slug}/")
                continue

            block = f"\n{EXPAND_MARKER}\n{new_html.strip()}\n"

            if PILLAR_MARKER in raw:
                # Insert expansion before the pillar link block
                raw = raw.replace(PILLAR_MARKER, block + "\n" + PILLAR_MARKER, 1)
            else:
                # No pillar marker — just append at end
                raw = raw.rstrip() + "\n" + block

            status = patch(pid, raw)
            print(f"  ID {pid:5}  HTTP {status}  expanded  /{slug}/")

        except Exception as e:
            print(f"  ID {pid:5}  ERROR: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
