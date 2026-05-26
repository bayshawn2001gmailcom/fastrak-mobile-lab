"""
Batch redesign all city landing pages — ATD editorial style.
Sections: hero · stats bar · services list · how it works · why fastrak · nearby areas · CTA · FAQ
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

# ── City page definitions ─────────────────────────────────────────────────────
CITY_PAGES = [
    {
        "id": 1248, "city": "Snellville", "county": "Gwinnett County", "zips": "30078, 30039",
        "focus_kw": "mobile phlebotomy Snellville GA",
        "title": "Mobile Phlebotomy Snellville GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Snellville, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve all of Snellville and eastern Gwinnett County — 7 days a week. Blood draws, DNA testing, drug screening, and wellness panels at your door.",
        "local_note": "Snellville is Fastrak Mobile Lab’s home base — residents enjoy our fastest response times and most flexible scheduling in the entire service area.",
        "nearby": ["Grayson, GA", "Loganville, GA", "Lawrenceville, GA", "Lilburn, GA", "Stone Mountain, GA"],
        "faq_q": "What zip codes in Snellville, GA do you serve?",
        "faq_a": "We serve all Snellville zip codes — 30078 and 30039 — plus all surrounding eastern Gwinnett County communities within our 30-mile radius.",
    },
    {
        "id": 1256, "city": "Lawrenceville", "county": "Gwinnett County", "zips": "30044, 30046, 30043",
        "focus_kw": "mobile phlebotomy Lawrenceville GA",
        "title": "Mobile Phlebotomy Lawrenceville GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Lawrenceville, GA — 7 days a week. At-home blood draws, DNA & drug testing. Same-day available.",
        "hero_sub": "Certified phlebotomists come directly to your Lawrenceville home, office, or facility — 7 days a week. No waiting rooms, no driving to a lab.",
        "local_note": "As Gwinnett County’s county seat and largest city, Lawrenceville residents have access to Fastrak’s full mobile lab menu with same-day and early morning fasting appointments.",
        "nearby": ["Snellville, GA", "Duluth, GA", "Norcross, GA", "Lilburn, GA", "Buford, GA"],
        "faq_q": "Do you serve the Sugarloaf and Hamilton Mill areas of Lawrenceville?",
        "faq_a": "Yes — we cover all of Lawrenceville including Sugarloaf, Hamilton Mill, Alcovy, and neighborhoods near Gwinnett Medical Center. Zip codes 30044, 30046, and 30043 all fall within our service area.",
    },
    {
        "id": 1250, "city": "Duluth", "county": "Gwinnett County", "zips": "30096, 30097",
        "focus_kw": "mobile phlebotomy Duluth GA",
        "title": "Mobile Phlebotomy Duluth GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Duluth, GA — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists serve all of Duluth and northern Gwinnett County — 7 days a week. At-home blood draws, DNA testing, and drug screening at your location.",
        "local_note": "Duluth’s diverse, fast-growing community — including its large international and tech professional population — makes mobile lab access especially valuable. We accommodate multilingual households and busy corporate schedules.",
        "nearby": ["Suwanee, GA", "Lawrenceville, GA", "Norcross, GA", "Sugar Hill, GA", "Peachtree Corners, GA"],
        "faq_q": "Do you serve the Peachtree Corners and Johns Creek areas near Duluth?",
        "faq_a": "Yes — our service radius from Duluth covers Peachtree Corners, Johns Creek, and Suwanee. All zip codes 30096 and 30097 are fully covered, and we serve neighboring communities as well.",
    },
    {
        "id": 1334, "city": "Lilburn", "county": "Gwinnett County", "zips": "30047",
        "focus_kw": "mobile phlebotomy Lilburn GA",
        "title": "Mobile Phlebotomy Lilburn GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Licensed mobile phlebotomists serving Lilburn, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Same-day available.",
        "hero_sub": "Certified phlebotomists come to your Lilburn home, office, or facility — 7 days a week. No waiting rooms, no driving. Professional lab work at your door.",
        "local_note": "Lilburn’s established neighborhoods and growing senior population make mobile phlebotomy a natural fit. We regularly serve assisted living communities and homebound patients throughout the 30047 area.",
        "nearby": ["Lawrenceville, GA", "Snellville, GA", "Tucker, GA", "Stone Mountain, GA", "Norcross, GA"],
        "faq_q": "Do you serve the Five Forks and Camp Creek areas of Lilburn?",
        "faq_a": "Yes — we serve all of Lilburn including Five Forks, Camp Creek, and neighborhoods along Killian Hill Road. The entire 30047 zip code falls within our Gwinnett County service area.",
    },
    {
        "id": 1258, "city": "Norcross", "county": "Gwinnett County", "zips": "30071, 30093",
        "focus_kw": "mobile phlebotomy Norcross GA",
        "title": "Mobile Phlebotomy Norcross GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Norcross, GA — 7 days a week. At-home blood draws, DNA testing & corporate wellness. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Norcross businesses and residents — 7 days a week. At-home and on-site blood draws, DNA testing, and drug screening anywhere in Gwinnett County.",
        "local_note": "Norcross is home to dozens of corporate campuses and a highly diverse community. Fastrak provides onsite pre-employment and occupational health collections for HR teams, as well as home visits for residents.",
        "nearby": ["Peachtree Corners, GA", "Duluth, GA", "Lawrenceville, GA", "Tucker, GA", "Lilburn, GA"],
        "faq_q": "Can you do onsite drug testing for Norcross businesses and corporate offices?",
        "faq_a": "Absolutely — onsite corporate collections are one of our most popular services in Norcross. We come to your business location for pre-employment screening, DOT drug testing, and random drug testing programs. Call to discuss a business account.",
    },
    {
        "id": 1328, "city": "Buford", "county": "Gwinnett County", "zips": "30518, 30519",
        "focus_kw": "mobile phlebotomy Buford GA",
        "title": "Mobile Phlebotomy Buford GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Buford, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve all of Buford and northern Gwinnett County — 7 days a week. At-home blood draws, DNA testing, and drug screening at your location.",
        "local_note": "Buford’s fast-growing residential communities near Lake Lanier and the Mall of Georgia corridor make mobile phlebotomy the smart alternative to driving to an understaffed clinic.",
        "nearby": ["Sugar Hill, GA", "Suwanee, GA", "Lawrenceville, GA", "Gainesville, GA", "Cumming, GA"],
        "faq_q": "Do you serve the Lake Lanier and Hamilton Mill communities near Buford?",
        "faq_a": "Yes — we serve all of Buford including communities near Lake Lanier, the Mall of Georgia area, and Hamilton Mill. Both 30518 and 30519 zip codes are fully within our service area.",
    },
    {
        "id": 1333, "city": "Sugar Hill", "county": "Gwinnett County", "zips": "30518",
        "focus_kw": "mobile phlebotomy Sugar Hill GA",
        "title": "Mobile Phlebotomy Sugar Hill GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Sugar Hill, GA — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists come to your Sugar Hill home or office — 7 days a week. Blood draws, DNA testing, and drug screening without leaving northern Gwinnett County.",
        "local_note": "Sugar Hill is one of Gwinnett’s fastest-growing family communities. We offer pediatric-friendly blood draws and early morning fasting appointments perfect for busy Sugar Hill households.",
        "nearby": ["Buford, GA", "Suwanee, GA", "Duluth, GA", "Cumming, GA", "Flowery Branch, GA"],
        "faq_q": "Do you serve neighborhoods near E.E. Robinson Park and Sycamore Drive in Sugar Hill?",
        "faq_a": "Yes — we serve all Sugar Hill neighborhoods including communities near E.E. Robinson Park, downtown Sugar Hill, and areas along Buford Highway. Zip code 30518 is fully covered.",
    },
    {
        "id": 1332, "city": "Suwanee", "county": "Gwinnett County", "zips": "30024",
        "focus_kw": "mobile phlebotomy Suwanee GA",
        "title": "Mobile Phlebotomy Suwanee GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Suwanee, GA — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Suwanee and north Gwinnett County — 7 days a week. Blood draws, DNA testing, and drug screening at your home, office, or facility.",
        "local_note": "Suwanee’s health-conscious community and active residents make direct-access lab testing especially popular here. Order your own wellness panels without a doctor’s visit — we come to you.",
        "nearby": ["Duluth, GA", "Sugar Hill, GA", "Buford, GA", "Johns Creek, GA", "Lawrenceville, GA"],
        "faq_q": "Do you serve the Town Center and Olde Town Suwanee neighborhoods?",
        "faq_a": "Yes — we cover all of Suwanee including Town Center, Olde Town, Creekside at Twin Lakes, and all communities in the 30024 zip code. Same-day appointments are frequently available.",
    },
    {
        "id": 1261, "city": "Conyers", "county": "Rockdale County", "zips": "30012, 30013, 30094",
        "focus_kw": "mobile phlebotomy Conyers GA",
        "title": "Mobile Phlebotomy Conyers GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Conyers, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve all of Conyers and Rockdale County — 7 days a week. At-home blood draws, DNA testing, and drug screening without driving to a clinic.",
        "local_note": "Conyers residents in Rockdale County deserve the same mobile lab access as metro Atlanta — Fastrak extends full-service coverage to 30012, 30013, and 30094 with no additional travel fees.",
        "nearby": ["Covington, GA", "Lithonia, GA", "Snellville, GA", "Stone Mountain, GA", "Loganville, GA"],
        "faq_q": "Do you serve the Salem Road and Highway 138 corridors in Conyers?",
        "faq_a": "Yes — we cover all of Conyers including communities along Salem Road, Highway 138, and the Olde Town Conyers area. All three Rockdale County zip codes — 30012, 30013, and 30094 — are in our service area.",
    },
    {
        "id": 1106, "city": "Buckhead", "county": "Fulton County", "zips": "30305, 30326, 30327",
        "focus_kw": "mobile phlebotomy Buckhead Atlanta",
        "title": "Mobile Phlebotomy Buckhead Atlanta GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Buckhead, Atlanta — 7 days a week. At-home blood draws, concierge wellness panels & DNA testing. Book same-day.",
        "hero_sub": "Certified phlebotomists come to your Buckhead home, condo, or office — 7 days a week. Professional lab work without leaving your Buckhead neighborhood.",
        "local_note": "Buckhead’s executive and professional community expects a higher standard of convenience. Fastrak’s concierge mobile phlebotomy service delivers hospital-grade lab collections directly to your high-rise, estate, or office building.",
        "nearby": ["Midtown Atlanta", "Sandy Springs, GA", "Dunwoody, GA", "Vinings, GA", "Brookhaven, GA"],
        "faq_q": "Can you come to high-rise condos and office buildings in Buckhead?",
        "faq_a": "Yes — we regularly serve Buckhead high-rise condominiums, private residences, and corporate offices. Our phlebotomists are experienced in navigating secured buildings and understand the discretion Buckhead clients expect.",
    },
    {
        "id": 1108, "city": "Decatur", "county": "DeKalb County", "zips": "30030, 30033, 30032",
        "focus_kw": "mobile phlebotomy Decatur GA",
        "title": "Mobile Phlebotomy Decatur GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Decatur, GA — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Decatur and all of DeKalb County — 7 days a week. At-home blood draws, DNA testing, and drug screening at your location.",
        "local_note": "Decatur’s health-forward community and walkable neighborhoods make mobile phlebotomy a perfect fit. We serve Decatur homes, businesses near the square, and Emory University area residents.",
        "nearby": ["Avondale Estates, GA", "Tucker, GA", "Clarkston, GA", "Stone Mountain, GA", "Atlanta, GA"],
        "faq_q": "Do you serve the Oakhurst and Kirkwood neighborhoods in Decatur?",
        "faq_a": "Yes — we cover all of Decatur including Oakhurst, Kirkwood, North Decatur, Toco Hills, and communities near Agnes Scott and Emory. Zip codes 30030, 30033, and 30032 are all fully served.",
    },
    {
        "id": 1110, "city": "Marietta", "county": "Cobb County", "zips": "30060, 30062, 30064, 30066, 30067, 30068",
        "focus_kw": "mobile phlebotomy Marietta GA",
        "title": "Mobile Phlebotomy Marietta GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Marietta, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve all of Marietta and Cobb County — 7 days a week. Blood draws, DNA testing, and drug screening at your home, office, or facility.",
        "local_note": "Marietta is Cobb County’s largest city and a hub for healthcare, technology, and DoD contractors. Fastrak serves Marietta residents and businesses with flexible scheduling — including early morning fasting draws and corporate onsite collections.",
        "nearby": ["Smyrna, GA", "Kennesaw, GA", "Sandy Springs, GA", "Vinings, GA", "Acworth, GA"],
        "faq_q": "Do you serve East Marietta, West Marietta, and the areas near Kennestone Hospital?",
        "faq_a": "Yes — we serve all of Marietta including East Marietta, West Marietta, communities near WellStar Kennestone Hospital, Marietta Square, and all Cobb County zip codes in the 30060–30068 range.",
    },
    {
        "id": 1107, "city": "Midtown Atlanta", "county": "Fulton County", "zips": "30308, 30309, 30306",
        "focus_kw": "mobile phlebotomy Midtown Atlanta GA",
        "title": "Mobile Phlebotomy Midtown Atlanta | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Midtown Atlanta — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists come to your Midtown Atlanta apartment, condo, or office — 7 days a week. Professional lab work delivered to your door without the waiting room.",
        "local_note": "Midtown’s high density of apartment buildings, co-working spaces, and busy professionals makes mobile phlebotomy the smart choice. We navigate secured buildings, doorman properties, and office towers throughout the 30308 and 30309 corridors.",
        "nearby": ["Buckhead, Atlanta", "Virginia-Highland, GA", "Inman Park, GA", "Grant Park, GA", "Decatur, GA"],
        "faq_q": "Can you come to apartment buildings and condos in Midtown Atlanta?",
        "faq_a": "Yes — this is one of our most common requests in Midtown. We work with building management for secure access and serve residents in high-rises, condos, and apartment buildings throughout the Midtown 30308 and 30309 zip codes.",
    },
    {
        "id": 1109, "city": "Sandy Springs", "county": "Fulton County", "zips": "30350, 30338, 30328",
        "focus_kw": "mobile phlebotomy Sandy Springs GA",
        "title": "Mobile Phlebotomy Sandy Springs GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Sandy Springs, GA — 7 days a week. At-home blood draws, DNA testing & concierge wellness. Book same-day.",
        "hero_sub": "Certified phlebotomists come to your Sandy Springs home, office, or facility — 7 days a week. Concierge-level mobile lab service for north Fulton County.",
        "local_note": "Sandy Springs’ corporate headquarters, executive residents, and health-conscious community rely on Fastrak for same-day and concierge lab collections. We serve Perimeter Center offices and north Fulton residential communities.",
        "nearby": ["Dunwoody, GA", "Buckhead, Atlanta", "Roswell, GA", "Marietta, GA", "Brookhaven, GA"],
        "faq_q": "Do you serve the Perimeter Center and Pill Hill area of Sandy Springs?",
        "faq_a": "Yes — Perimeter Center, Pill Hill (near Northside and St. Joseph’s Hospital), and all Sandy Springs corporate corridors are in our service area. We handle onsite corporate collections and private home visits throughout 30350, 30338, and 30328.",
    },
    {
        "id": 1330, "city": "Avondale Estates", "county": "DeKalb County", "zips": "30002",
        "focus_kw": "mobile phlebotomy Avondale Estates GA",
        "title": "Mobile Phlebotomy Avondale Estates GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Avondale Estates, GA — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Avondale Estates and all of inner DeKalb County — 7 days a week. Blood draws, DNA testing, and drug screening at your home or office.",
        "local_note": "Avondale Estates is a small, tight-knit community where neighbors value personalized service. Fastrak brings that same local, personal approach to mobile phlebotomy — you’ll know your technician by name.",
        "nearby": ["Decatur, GA", "Clarkston, GA", "Stone Mountain, GA", "Tucker, GA", "Atlanta, GA"],
        "faq_q": "What areas near Avondale Estates do you also serve?",
        "faq_a": "We cover Avondale Estates (30002) and all neighboring DeKalb County communities including Decatur, Clarkston, Stone Mountain, and Tucker. If you’re in inner DeKalb County, we come to you.",
    },
    {
        "id": 1335, "city": "Clarkston", "county": "DeKalb County", "zips": "30021",
        "focus_kw": "mobile phlebotomy Clarkston GA",
        "title": "Mobile Phlebotomy Clarkston GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Clarkston, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Clarkston and DeKalb County — 7 days a week. Professional mobile lab service for one of Georgia’s most diverse communities.",
        "local_note": "Clarkston is one of the most culturally diverse cities in Georgia. Fastrak’s mobile service removes transportation barriers to lab testing for Clarkston’s international and refugee community — we come to you, wherever you are.",
        "nearby": ["Decatur, GA", "Avondale Estates, GA", "Tucker, GA", "Stone Mountain, GA", "Lilburn, GA"],
        "faq_q": "Do you serve the refugee and immigrant community in Clarkston for lab services?",
        "faq_a": "Yes — Clarkston’s international community is one we’re proud to serve. We provide mobile blood draws, DNA relationship testing, and immigration-related lab services throughout Clarkston (30021) and surrounding DeKalb County.",
    },
    {
        "id": 1331, "city": "Smyrna", "county": "Cobb County", "zips": "30080, 30082",
        "focus_kw": "mobile phlebotomy Smyrna GA",
        "title": "Mobile Phlebotomy Smyrna GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Smyrna, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Smyrna and eastern Cobb County — 7 days a week. At-home blood draws, DNA testing, and drug screening at your location.",
        "local_note": "Smyrna’s rapidly growing mixed-use communities and proximity to the Battery Atlanta bring a new wave of busy professionals who value time. Fastrak’s mobile service fits perfectly into Smyrna’s fast-paced lifestyle.",
        "nearby": ["Marietta, GA", "Vinings, GA", "Sandy Springs, GA", "Mableton, GA", "Austell, GA"],
        "faq_q": "Do you serve the Vinings and Cumberland area near Smyrna?",
        "faq_a": "Yes — we serve Smyrna (30080, 30082) and neighboring communities including Vinings, Cumberland, and Mableton. We’re happy to accommodate corporate offices near the Battery Atlanta corridor as well.",
    },
    {
        "id": 1329, "city": "Stone Mountain", "county": "DeKalb County", "zips": "30083, 30087, 30088",
        "focus_kw": "mobile phlebotomy Stone Mountain GA",
        "title": "Mobile Phlebotomy Stone Mountain GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Stone Mountain, GA — 7 days a week. At-home blood draws, DNA testing & drug screening. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Stone Mountain and eastern DeKalb County — 7 days a week. Blood draws, DNA testing, and drug screening at your home or office.",
        "local_note": "Stone Mountain’s large African-American community has high rates of conditions requiring regular lab monitoring — hypertension, diabetes, sickle cell. Fastrak’s mobile service makes it easier to stay on top of your health without leaving home.",
        "nearby": ["Lithonia, GA", "Snellville, GA", "Lilburn, GA", "Tucker, GA", "Decatur, GA"],
        "faq_q": "Do you serve the Rockbridge and Hairston Road areas of Stone Mountain?",
        "faq_a": "Yes — we cover all of Stone Mountain including Rockbridge, Hairston, and Village Mill neighborhoods. Zip codes 30083, 30087, and 30088 are all within our DeKalb County service area.",
    },
    {
        "id": 1260, "city": "Tucker", "county": "DeKalb County", "zips": "30084, 30085",
        "focus_kw": "mobile phlebotomy Tucker GA",
        "title": "Mobile Phlebotomy Tucker GA | At-Home Blood Draw | Fastrak Mobile Lab",
        "desc": "Certified mobile phlebotomists serving Tucker, GA — 7 days a week. At-home blood draws, DNA testing & wellness panels. Book same-day.",
        "hero_sub": "Certified phlebotomists serve Tucker and northeastern DeKalb County — 7 days a week. At-home blood draws, DNA testing, and drug screening at your location.",
        "local_note": "Tucker has a strong sense of community and a growing population of active seniors who benefit most from mobile phlebotomy. We provide compassionate, in-home lab collections for Tucker’s homebound and elderly residents.",
        "nearby": ["Lilburn, GA", "Decatur, GA", "Stone Mountain, GA", "Norcross, GA", "Clarkston, GA"],
        "faq_q": "Do you serve the Hugh Howell Road and Lavista Road areas of Tucker?",
        "faq_a": "Yes — we serve all Tucker neighborhoods including communities along Hugh Howell, Lavista, and Chamblee Tucker Roads. Zip codes 30084 and 30085 are both fully in our DeKalb County service area.",
    },
    {
        "id": 1263, "city": "Gwinnett County", "county": "Gwinnett County", "zips": "30044, 30047, 30071, 30078, 30093, 30096",
        "focus_kw": "DNA testing Gwinnett County GA",
        "title": "DNA Testing Gwinnett County GA | Mobile Collection | Fastrak Mobile Lab",
        "desc": "Court-admissible and peace-of-mind DNA testing in Gwinnett County, GA. Mobile collection at your home or office — AABB standards. Book same-day.",
        "hero_sub": "Court-admissible and peace-of-mind DNA testing collected at your Gwinnett County location — paternity, maternity, sibling, immigration, and relationship testing with strict chain-of-custody.",
        "local_note": "Gwinnett County has one of the highest rates of DNA testing demand in metro Atlanta — driven by paternity proceedings, custody cases, and immigration petitions. Fastrak’s mobile collection brings chain-of-custody documentation directly to you.",
        "nearby": ["Lawrenceville, GA", "Snellville, GA", "Duluth, GA", "Norcross, GA", "Lilburn, GA"],
        "service_focus": "dna",
        "faq_q": "Is mobile DNA testing in Gwinnett County court-admissible?",
        "faq_a": "Yes — Fastrak’s DNA collections follow AABB-standard chain-of-custody protocols, making results legally defensible in Georgia family court, paternity proceedings, and USCIS immigration petitions.",
    },
    {
        "id": 1262, "city": "Gwinnett County", "county": "Gwinnett County", "zips": "30044, 30047, 30071, 30078, 30093, 30096",
        "focus_kw": "mobile drug testing Gwinnett County GA",
        "title": "Mobile Drug Testing Gwinnett County GA | DOT & Non-DOT | Fastrak Mobile Lab",
        "desc": "Mobile DOT and non-DOT drug testing in Gwinnett County, GA. Onsite collection at your business or home — same-day available. Call Fastrak.",
        "hero_sub": "Mobile DOT and non-DOT drug testing throughout Gwinnett County — urine, saliva, and hair follicle collections at your business, job site, or home. HIPAA-compliant with full chain-of-custody.",
        "local_note": "Gwinnett County businesses — from logistics firms in Norcross to construction companies in Lawrenceville — rely on Fastrak for fast, compliant onsite drug testing programs with no fleet disruption.",
        "nearby": ["Lawrenceville, GA", "Norcross, GA", "Duluth, GA", "Buford, GA", "Snellville, GA"],
        "service_focus": "drug",
        "faq_q": "Can you set up a recurring mobile drug testing program for our Gwinnett County business?",
        "faq_a": "Yes — we work with Gwinnett County employers on random, pre-employment, post-accident, and reasonable suspicion drug testing programs. We can design a schedule that fits your workforce size and compliance requirements. Call us to discuss a business account.",
    },
]

# ── DNA+Phlebotomy combo pages ────────────────────────────────────────────────
COMBO_PAGES = [
    {
        "id": 1377, "city": "Lawrenceville", "county": "Gwinnett County", "zips": "30044, 30046",
        "focus_kw": "mobile phlebotomy DNA testing Lawrenceville GA",
        "title": "Mobile Phlebotomy & DNA Testing Lawrenceville GA | Fastrak Mobile Lab",
        "desc": "Mobile phlebotomy and DNA testing in Lawrenceville, GA — at your home or office, 7 days a week. Court-admissible. Book same-day.",
        "hero_h1_line2": "Mobile Phlebotomy &amp; DNA Testing",
        "hero_sub": "Certified phlebotomists perform at-home blood draws and court-admissible DNA testing throughout Lawrenceville and Gwinnett County — 7 days a week, chain-of-custody guaranteed.",
        "local_note": "Lawrenceville is Gwinnett County’s county seat and home to the Gwinnett County Courthouse — making court-admissible DNA testing and mobile phlebotomy especially in-demand. We provide both services at your location with a single appointment.",
        "nearby": ["Snellville, GA", "Duluth, GA", "Norcross, GA", "Buford, GA", "Grayson, GA"],
        "faq_q": "Can I book mobile phlebotomy and DNA testing in the same appointment in Lawrenceville?",
        "faq_a": "Yes — we regularly combine blood draw and DNA collection in a single visit for Lawrenceville patients. This is especially convenient for legal cases requiring multiple specimen types. Book online or call to arrange a combined appointment.",
    },
    {
        "id": 1382, "city": "Grayson", "county": "Gwinnett County", "zips": "30017",
        "focus_kw": "mobile phlebotomy DNA testing Grayson GA",
        "title": "Mobile Phlebotomy & DNA Testing Grayson GA | Fastrak Mobile Lab",
        "desc": "Mobile phlebotomy and DNA testing in Grayson, GA — at your home or office, 7 days a week. Court-admissible. Book same-day.",
        "hero_h1_line2": "Mobile Phlebotomy &amp; DNA Testing",
        "hero_sub": "Certified phlebotomists bring at-home blood draws and court-admissible DNA testing to Grayson and eastern Gwinnett County — 7 days a week, no lab visit required.",
        "local_note": "Grayson’s eastern Gwinnett location means residents historically drove far for lab services. Fastrak eliminates that trip — bringing blood draws and DNA testing directly to your Grayson address.",
        "nearby": ["Loganville, GA", "Snellville, GA", "Lawrenceville, GA", "Conyers, GA", "Walnut Grove, GA"],
        "faq_q": "Is DNA testing in Grayson, GA court-admissible?",
        "faq_a": "Yes — Fastrak’s DNA collections follow AABB-standard chain-of-custody protocols and are legally admissible in Georgia family court, paternity proceedings, and USCIS immigration cases. We document every step of the collection process.",
    },
    {
        "id": 1383, "city": "Loganville", "county": "Gwinnett / Walton County", "zips": "30052",
        "focus_kw": "mobile phlebotomy DNA testing Loganville GA",
        "title": "Mobile Phlebotomy & DNA Testing Loganville GA | Fastrak Mobile Lab",
        "desc": "Mobile phlebotomy and DNA testing in Loganville, GA — at your home or office, 7 days a week. Court-admissible. Book same-day.",
        "hero_h1_line2": "Mobile Phlebotomy &amp; DNA Testing",
        "hero_sub": "Certified phlebotomists bring at-home blood draws and court-admissible DNA testing to Loganville and the Gwinnett/Walton County border — 7 days a week.",
        "local_note": "Loganville sits on the Gwinnett/Walton County line — a growing area where many residents previously had no close mobile lab option. Fastrak now covers 30052 fully with both phlebotomy and DNA testing services.",
        "nearby": ["Grayson, GA", "Snellville, GA", "Conyers, GA", "Monroe, GA", "Covington, GA"],
        "faq_q": "Do you serve the Social Circle and Monroe areas near Loganville?",
        "faq_a": "Our primary coverage is Loganville (30052). We can often extend to Social Circle and Monroe on request — call us to confirm your specific address is within our service radius before booking.",
    },
]

ALL_PAGES = CITY_PAGES + COMBO_PAGES


# ── CSS (shared across all pages) ─────────────────────────────────────────────
def shared_css(page_id):
    return f"""<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
.page-id-{page_id} .entry-title,.page-id-{page_id} .page-title,
.page-id-{page_id} h1.entry-title,.page-id-{page_id} .page-header,
.page-id-{page_id} .entry-header{{display:none!important}}
.page-id-{page_id} .entry-content{{padding-top:0!important;margin-top:0!important}}
.fml{{box-sizing:border-box;font-family:'Inter',sans-serif;color:#111;line-height:1.65;background:#fff}}
.fml *{{box-sizing:border-box;margin:0;padding:0}}
.fml h1,.fml h2,.fml h3,.fml h4{{font-family:'Montserrat',sans-serif;line-height:1.2;color:inherit}}
.fml a{{text-decoration:none;color:inherit}}
.fml .hero{{background:linear-gradient(135deg,#07304f 0%,#0d4a7a 55%,#0a8c7c 100%);padding:96px 24px 88px;position:relative;overflow:hidden}}
.fml .hero::before{{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}}
.fml .hero-body{{position:relative;z-index:1;max-width:700px;margin:0 auto;text-align:center}}
.fml .hero-pill{{display:inline-block;border:1.5px solid rgba(255,255,255,.35);padding:5px 18px;border-radius:4px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:24px;color:rgba(255,255,255,.9);font-family:'Montserrat',sans-serif}}
.fml .hero h1{{font-size:clamp(2.2rem,5vw,3.5rem);font-weight:800;margin-bottom:20px;color:#fff;line-height:1.15}}
.fml .hero h1 em{{font-style:normal;color:#6ef0e0}}
.fml .hero-sub{{font-size:1.1rem;color:rgba(255,255,255,.88);max-width:600px;margin:0 auto 36px;line-height:1.75}}
.fml .btn-teal{{display:inline-block;background:#0db8a5;color:#fff;padding:16px 40px;border-radius:4px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;transition:background .2s,transform .15s;letter-spacing:.3px;box-shadow:0 4px 20px rgba(13,184,165,.4)}}
.fml .btn-teal:hover{{background:#0aa898;transform:translateY(-2px)}}
.fml .btn-ghost{{display:inline-block;border:2px solid rgba(255,255,255,.5);color:#fff;padding:14px 32px;border-radius:4px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:.97rem;margin-left:14px;transition:border-color .2s}}
.fml .btn-ghost:hover{{border-color:#fff}}
.fml .hero-trust{{display:flex;flex-wrap:wrap;justify-content:center;gap:18px;margin-top:32px}}
.fml .hero-trust span{{font-size:13px;color:rgba(255,255,255,.8);display:flex;align-items:center;gap:7px}}
.fml .hero-trust .ck{{color:#6ef0e0;font-weight:800}}
.fml .statsbar{{background:#0d4a7a;display:flex;justify-content:center;flex-wrap:wrap}}
.fml .st{{padding:20px 48px;text-align:center;color:#fff;border-right:1px solid rgba(255,255,255,.12)}}
.fml .st:last-child{{border-right:none}}
.fml .st-n{{display:block;font-family:'Montserrat',sans-serif;font-size:1.9rem;font-weight:800;color:#6ef0e0}}
.fml .st-l{{font-size:11px;opacity:.7;letter-spacing:.8px;text-transform:uppercase;margin-top:4px}}
.fml section{{padding:80px 24px}}
.fml .wrap{{max-width:1040px;margin:0 auto}}
.fml .tag{{display:inline-block;color:#0db8a5;font-family:'Montserrat',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;margin-bottom:12px}}
.fml h2{{font-size:clamp(1.8rem,3.8vw,2.7rem);font-weight:800;color:#07304f;margin-bottom:16px}}
.fml .lead{{font-size:1.03rem;color:#444;line-height:1.85;margin-bottom:40px}}
.fml .bg-lt{{background:#f4f8fc}}
.fml .bg-wh{{background:#fff}}
.fml .two-col{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start}}
@media(max-width:720px){{.fml .two-col{{grid-template-columns:1fr}}}}
.fml .svc-list{{list-style:none;display:flex;flex-direction:column;gap:22px}}
.fml .svc-list li{{display:flex;gap:16px;align-items:flex-start}}
.fml .svc-icon{{width:42px;height:42px;min-width:42px;background:#f0f8fc;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.25rem}}
.fml .svc-list strong{{display:block;font-family:'Montserrat',sans-serif;font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:4px}}
.fml .svc-list p{{font-size:.9rem;color:#555;line-height:1.65}}
.fml .diff-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2px;margin-top:48px;border:1px solid #dce8f0;border-radius:4px;overflow:hidden}}
.fml .diff-card{{background:#fff;padding:32px 26px;border-right:1px solid #dce8f0}}
.fml .diff-card:last-child{{border-right:none}}
.fml .diff-num{{font-family:'Montserrat',sans-serif;font-size:2.2rem;font-weight:800;color:#c8dff0;margin-bottom:12px;display:block}}
.fml .diff-card h3{{font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:8px;font-family:'Montserrat',sans-serif}}
.fml .diff-card p{{font-size:.87rem;color:#555;line-height:1.7}}
.fml .cities-grid{{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}}
.fml .city-pill{{background:#fff;border:1.5px solid #ccdce8;border-radius:30px;padding:9px 18px;font-size:.9rem;font-weight:600;color:#0d4a7a;display:flex;align-items:center;gap:8px;font-family:'Montserrat',sans-serif}}
.fml .city-pill::before{{content:'';width:7px;height:7px;background:#0db8a5;border-radius:50%;flex-shrink:0}}
.fml .steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:48px;position:relative}}
.fml .steps::before{{content:'';position:absolute;top:27px;left:calc(16.6% + 14px);right:calc(16.6% + 14px);height:2px;background:#dce8f0;z-index:0}}
.fml .step{{text-align:center;padding:0 20px;position:relative;z-index:1}}
.fml .step-num{{width:56px;height:56px;background:#0d4a7a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Montserrat',sans-serif;font-size:1.2rem;font-weight:800;color:#fff;margin:0 auto 20px}}
.fml .step h3{{font-family:'Montserrat',sans-serif;font-size:.97rem;font-weight:700;color:#07304f;margin-bottom:10px}}
.fml .step p{{font-size:.88rem;color:#555;line-height:1.7}}
.fml .cta-band{{background:#0d4a7a;padding:72px 24px;text-align:center}}
.fml .cta-band h2{{font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;color:#fff;margin-bottom:16px;line-height:1.2}}
.fml .cta-band p{{font-size:1.05rem;color:rgba(255,255,255,.85);max-width:580px;margin:0 auto 36px;line-height:1.75}}
.fml .faq-wrap{{max-width:780px;margin:0 auto;text-align:left}}
.fml .faq{{border-bottom:1px solid #dce8f0;padding:20px 0}}
.fml .faq-q{{font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;color:#07304f;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:12px;user-select:none}}
.fml .faq-a{{font-size:.93rem;color:#555;line-height:1.8;padding-top:14px;display:none}}
.fml .faq.open .faq-a{{display:block}}
.fml .faq.open .ico{{transform:rotate(45deg)}}
.fml .ico{{font-size:1.5rem;color:#0db8a5;transition:transform .2s;flex-shrink:0;line-height:1}}
@media(max-width:640px){{
  .fml .steps{{grid-template-columns:1fr;gap:32px}}
  .fml .steps::before{{display:none}}
  .fml .btn-ghost{{display:none}}
  .fml .st{{padding:16px 24px}}
  .fml .hero{{padding:72px 24px 64px}}
}}
</style>"""


def build_city_html(p):
    city     = p["city"]
    county   = p["county"]
    zips     = p["zips"]
    hero_sub = p["hero_sub"]
    local_note = p["local_note"]
    nearby   = p["nearby"]
    faq_q    = p["faq_q"]
    faq_a    = p["faq_a"]
    is_combo = "hero_h1_line2" in p

    # Hero H1
    if is_combo:
        h1 = f'<em>{p["hero_h1_line2"]}</em><br>in {city}, GA'
        pill_text = f"{county} &mdash; Mobile Lab Service"
        service_label = "Mobile Phlebotomy &amp; DNA Testing"
    else:
        h1 = f'Lab Work That Comes<br><em>Directly to {city}.</em>'
        pill_text = f"{city}, GA &mdash; Mobile Lab Service"
        service_label = "Mobile Lab Services"

    nearby_pills = "\n      ".join(
        f'<span class="city-pill">{c}</span>' for c in nearby
    )

    css = shared_css(p["id"])

    return f"""{css}

<div class="fml">

<!-- HERO -->
<div class="hero">
  <div class="hero-body">
    <div class="hero-pill">&#10003; {pill_text}</div>
    <h1>{h1}</h1>
    <p class="hero-sub">{hero_sub}</p>
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

<!-- STATS BAR -->
<div class="statsbar">
  <div class="st"><span class="st-n">7+</span><span class="st-l">Years in Healthcare</span></div>
  <div class="st"><span class="st-n">500+</span><span class="st-l">Patients Served</span></div>
  <div class="st"><span class="st-n">30+</span><span class="st-l">Mile Service Radius</span></div>
  <div class="st"><span class="st-n">HIPAA</span><span class="st-l">Fully Compliant</span></div>
</div>

<!-- SERVICES -->
<section class="bg-wh" id="services">
  <div class="wrap">
    <div class="two-col">
      <div>
        <span class="tag">What We Offer</span>
        <h2>{service_label} in {city}, {county[:county.find(' County')+7] if 'County' in county else county}</h2>
        <p class="lead">{local_note}</p>
        <ul class="svc-list">
          <li>
            <div class="svc-icon">&#129754;</div>
            <div><strong>At-Home Blood Draws &amp; Diagnostics</strong><p>Physician-ordered and direct-access blood draws for routine panels, specialty diagnostics, and health monitoring &mdash; at your {city} home, office, or facility.</p></div>
          </li>
          <li>
            <div class="svc-icon">&#129516;</div>
            <div><strong>Mobile DNA &amp; Paternity Testing</strong><p>Court-admissible and peace-of-mind DNA testing collected at your location. Paternity, maternity, sibling, immigration, and relationship testing with strict chain-of-custody.</p></div>
          </li>
          <li>
            <div class="svc-icon">&#128138;</div>
            <div><strong>Mobile Drug &amp; Alcohol Testing</strong><p>DOT and non-DOT urine, saliva, and hair follicle drug testing for {county} employers, legal proceedings, and personal use. Full chain-of-custody documentation.</p></div>
          </li>
        </ul>
      </div>
      <div>
        <ul class="svc-list" style="margin-top:0">
          <li>
            <div class="svc-icon">&#127970;</div>
            <div><strong>Pre-Employment Screening</strong><p>Occupational health and pre-employment drug screen packages for {city} businesses and HR teams. We come to your workplace &mdash; no lab visit required.</p></div>
          </li>
          <li>
            <div class="svc-icon">&#10084;&#65039;</div>
            <div><strong>Health &amp; Wellness Panels</strong><p>CBC, metabolic, lipid, thyroid, hormone, and vitamin panels. Many available without a doctor&rsquo;s order &mdash; take control of your preventive health from home.</p></div>
          </li>
          <li>
            <div class="svc-icon">&#128300;</div>
            <div><strong>Specialty Kit &amp; Concierge Collections</strong><p>Food sensitivity, genetic testing, micronutrient panels, and clinical trial specimen collections throughout {city} and {county}.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="bg-lt">
  <div class="wrap" style="text-align:center">
    <span class="tag">The Process</span>
    <h2>How Mobile Phlebotomy Works in {city}</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto">Three steps from scheduling to results &mdash; no driving, no waiting rooms, no hassle.</p>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <h3>Book Online or Call</h3>
        <p>Schedule in minutes at a time that works for you &mdash; including same-day, evenings, early mornings for fasting draws, and weekends throughout {city}.</p>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <h3>We Come to You</h3>
        <p>A licensed, background-checked phlebotomist arrives at your {city} home, office, or facility. Hospital-grade protocol with full chain-of-custody documentation.</p>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <h3>Results Delivered Securely</h3>
        <p>Specimens go to our CLIA-certified partner labs. Results are typically available within 24&ndash;72 hours, delivered securely to you &mdash; no re-visit required.</p>
      </div>
    </div>
  </div>
</section>

<!-- WHY FASTRAK -->
<section class="bg-wh">
  <div class="wrap">
    <div style="text-align:center;max-width:700px;margin:0 auto">
      <span class="tag">Why Fastrak Mobile Lab</span>
      <h2>The Mobile Lab Difference in {city}</h2>
      <p class="lead">We&rsquo;re not a national chain. We&rsquo;re a local, certified mobile phlebotomy provider with hospital-grade standards and the convenience of a house call.</p>
    </div>
    <div class="diff-grid">
      <div class="diff-card">
        <span class="diff-num">01</span>
        <h3>Same-Day Appointments</h3>
        <p>We frequently accommodate same-day visits in {city} &mdash; 7 days a week, including early morning fasting draws and weekend visits.</p>
      </div>
      <div class="diff-card">
        <span class="diff-num">02</span>
        <h3>100% HIPAA Compliant</h3>
        <p>Encrypted communication, secure results delivery, and zero third-party sharing without your authorization. Your health information stays private.</p>
      </div>
      <div class="diff-card">
        <span class="diff-num">03</span>
        <h3>Certified Phlebotomists</h3>
        <p>Every Fastrak technician is licensed, background-checked, and trained in mobile specimen collection &mdash; including pediatric and difficult-stick patients.</p>
      </div>
      <div class="diff-card">
        <span class="diff-num">04</span>
        <h3>No Doctor? No Problem.</h3>
        <p>Direct-access testing for hundreds of panels available without a referral. Order your own labs from your {city} home or office.</p>
      </div>
    </div>
  </div>
</section>

<!-- NEARBY AREAS -->
<section id="areas" class="bg-lt">
  <div class="wrap">
    <div style="text-align:center;max-width:680px;margin:0 auto 40px">
      <span class="tag">Service Area</span>
      <h2>We Also Serve These Nearby Areas</h2>
      <p class="lead" style="margin-bottom:0">In addition to {city}, Fastrak Mobile Lab serves all surrounding communities throughout {county} and metro Atlanta within our 30-mile service radius.</p>
    </div>
    <div class="cities-grid">
      {nearby_pills}
      <span class="city-pill">All of {county}</span>
    </div>
  </div>
</section>

<!-- CTA BAND -->
<div class="cta-band">
  <h2>Ready for Lab Work That Comes to {city}?</h2>
  <p>Stop driving to the lab. Stop waiting in line. Book your {city} mobile blood draw today &mdash; certified, convenient, and HIPAA-compliant.</p>
  <a class="btn-teal" href="{BOOK_URL}">Schedule Your Appointment &rarr;</a>
</div>

<!-- FAQ -->
<section class="bg-wh">
  <div class="wrap" style="text-align:center">
    <span class="tag">Common Questions</span>
    <h2>FAQ &mdash; Mobile Phlebotomy in {city}, GA</h2>
    <p class="lead" style="max-width:620px;margin-left:auto;margin-right:auto;margin-bottom:44px">Questions {city} patients ask before booking their first appointment.</p>
    <div class="faq-wrap">
      <div class="faq">
        <div class="faq-q">{faq_q}<span class="ico">+</span></div>
        <div class="faq-a">{faq_a}</div>
      </div>
      <div class="faq">
        <div class="faq-q">How does mobile phlebotomy work in {city}, GA?<span class="ico">+</span></div>
        <div class="faq-a">You book an appointment online or by phone, and a certified Fastrak phlebotomist travels to your {city} location. We collect your sample with strict chain-of-custody documentation and send it to our CLIA-certified partner lab. Results are typically available within 24&ndash;72 hours.</div>
      </div>
      <div class="faq">
        <div class="faq-q">Do I need a doctor&rsquo;s order for a blood draw in {city}?<span class="ico">+</span></div>
        <div class="faq-a">Most diagnostic tests require a physician&rsquo;s order. However, Fastrak also offers direct-access testing for many panels &mdash; including wellness, thyroid, hormone, vitamin, and lipid panels &mdash; that you can order yourself without a referral.</div>
      </div>
      <div class="faq">
        <div class="faq-q">How quickly can I get a same-day mobile phlebotomy appointment in {city}?<span class="ico">+</span></div>
        <div class="faq-a">We offer same-day and next-day appointments throughout {city} and {county}. Call us at {PHONE} or use our online booking system to check real-time availability. Early morning fasting slots are available by request.</div>
      </div>
      <div class="faq">
        <div class="faq-q">Can you serve seniors and homebound patients in {city}, GA?<span class="ico">+</span></div>
        <div class="faq-a">Absolutely. Mobile phlebotomy was designed with seniors and homebound patients in mind. Our phlebotomists are experienced in compassionate, gentle care and regularly serve assisted living facilities, nursing homes, and private residences throughout {city} and {county}.</div>
      </div>
      <div class="faq">
        <div class="faq-q">Is Fastrak Mobile Lab HIPAA compliant?<span class="ico">+</span></div>
        <div class="faq-a">Yes &mdash; all services are fully HIPAA-compliant. We use secure, encrypted communication for results, maintain strict chain-of-custody protocols, and never share your health information without your explicit authorization.</div>
      </div>
    </div>
  </div>
</section>

<script>
document.querySelectorAll('.fml .faq-q').forEach(function(q){{
  q.addEventListener('click',function(){{this.closest('.faq').classList.toggle('open')}});
}});
</script>

</div><!-- /fml -->"""


def deploy(p):
    html = build_city_html(p)
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


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ok, fail = 0, 0
    for p in ALL_PAGES:
        print(f"\n[{p['id']}] {p['city']} — {p['focus_kw']}")
        success = deploy(p)
        if success:
            ok += 1
        else:
            fail += 1
        time.sleep(1.2)   # be kind to the API

    print(f"\n{'='*50}")
    print(f"Done: {ok} deployed, {fail} failed")
    print(f"{'='*50}")
