# Workflow: Local Directory Submission

## Objective
Submit fastrakmobilelab.com to the top 20 healthcare and local business directories to build NAP citations and real backlinks, targeting DR increase from 0.6 to 2–5 within 30 days.

## Inputs Required
- Finalized NAP (from GBP — must be identical everywhere):
  - Name: Fastrak Mobile Lab
  - Address: [business address]
  - Phone: [business phone]
  - Website: https://fastrakmobilelab.com
- Short business description (200 chars): copy from GBP description
- GBP listing URL (for citations that link to it)
- Profile photo / logo

## Tools to Use
- `tools/directory_tracker.py` — maintains submission status

## Steps

### 1. Initialize tracker
```
python tools/directory_tracker.py --init
```

### 2. Work through P1 directories first
View status: `python tools/directory_tracker.py`

P1 directories (highest DR, submit these first):
- Google Business Profile (already done if GBP workflow complete)
- Yelp — https://biz.yelp.com/claim
- Apple Maps Connect — https://mapsconnect.apple.com
- Bing Places — https://www.bingplaces.com
- Facebook Business — https://www.facebook.com/pages/create
- Healthgrades — https://www.healthgrades.com/add-provider
- Zocdoc — https://www.zocdoc.com/practice/profile
- BBB — https://www.bbb.org/business-registration
- Gwinnett Chamber of Commerce — https://www.gwinnettchamber.org/join/

### 3. After each submission
Update the tracker immediately:
```
python tools/directory_tracker.py --update "Yelp" submitted
```
Once the listing goes live:
```
python tools/directory_tracker.py --update "Yelp" live --url "https://www.yelp.com/biz/fastrak-mobile-lab"
```

### 4. Move to P2 and P3 directories
After all P1 are submitted, work through P2 and P3 in the tracker.

### 5. Weekly check
Run `python tools/directory_tracker.py` each Monday to see what's pending and what went live.

## Expected Output
- 15–20 live citations within 30 days
- DR increase: 0.6 → 2–5
- Consistent NAP across all listings

## NAP Consistency Rules
- NEVER abbreviate differently across sites (e.g., don't use "Fastrak" on one and "Fastrak Mobile Lab" on another)
- Use the exact same phone number format everywhere (e.g., (770) 555-1234)
- If a directory auto-formats your address, verify it still matches

## Edge Cases
- Healthgrades / Zocdoc may require NPI number (National Provider Identifier) — obtain at nppes.cms.hhs.gov if not already registered
- Some directories charge for enhanced listings — only pay for BBB (accreditation) and Healthgrades (if they offer a free tier); skip paid upgrades on others
- If a listing already exists for the business: claim it, don't create a duplicate
