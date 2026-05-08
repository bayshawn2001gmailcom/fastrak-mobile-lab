# Workflow: Google Business Profile Optimization

## Objective
Fully optimize the Fastrak Mobile Lab GBP listing to qualify for the local 3-pack and establish Google-level trust signals that supplement backlink authority.

## Inputs Required
- GBP account access (same Google account as the business owner)
- Business NAP: Name / Address / Phone (must be identical across all listings)
- Brand_assets/logo.png for profile photo upload

## Tools to Use
- `tools/gbp_checklist.py` — generates the full checklist to .tmp/gbp_audit.md

## Steps

### 1. Generate the checklist
```
python tools/gbp_checklist.py
```
Open `.tmp/gbp_audit.md` and work through it top to bottom.

### 2. Business Info (highest priority)
- Log into https://business.google.com
- Set primary category to **Medical Laboratory**
- Add all 6 additional service categories
- Write business description using primary keyword in first sentence:
  > "Fastrak Mobile Lab provides certified mobile phlebotomy, in-home blood draws, drug testing, and DNA specimen collection for residents of Gwinnett County and metro Atlanta, GA."

### 3. Service Area
- Set to "Service area business" (not storefront)
- Add all cities in the 30-mile radius: Snellville, Lawrenceville, Duluth, Norcross, Tucker, Conyers, Decatur, Stone Mountain, Lilburn, Buford, Suwanee, Sugar Hill, Marietta

### 4. Photos
- Upload logo from Brand_assets/logo.png
- Upload at least 5 team/equipment photos
- Photos should be well-lit, professional, minimum 720×720px

### 5. Services Listing
Add each service with a short description and price range (even "call for pricing" counts):
- Mobile Phlebotomy
- Mobile Drug Testing
- DNA Specimen Collection
- Corporate Lab Services
- Senior & Homebound Lab Services

### 6. Seed Q&A
Post each Q&A from the checklist yourself (owner can post Q&A to seed common questions before patients ask).

### 7. Weekly Post Cadence
Set a recurring reminder to post to GBP every Monday. Use "What's New" type with:
- One sentence about a service or tip
- Link back to a relevant page on fastrakmobilelab.com
- Photo if available

## Expected Output
- Fully populated GBP listing
- Local 3-pack eligibility for "[service] [city]" searches in Gwinnett County
- GBP listing URL to use as NAP anchor across all directory submissions

## Edge Cases
- If GBP listing not yet created: create at https://business.google.com/create
- If listing exists but unverified: request postcard verification (5-7 business days)
- If another listing exists for same address: request ownership transfer via GBP support
