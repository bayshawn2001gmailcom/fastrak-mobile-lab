# Workflow: Physician & Facility Partnership Outreach

## Objective
Secure backlinks from physician offices, urgent care clinics, senior living facilities, and corporate HR departments in the 30-mile service radius. These are the highest-quality links available to a local healthcare service — real editorial links from trusted medical domains.

## Inputs Required
- Business contact info and email address
- Brief pitch (template in outreach_tracker.py output)
- List of target facilities in Gwinnett/DeKalb metro area

## Tools to Use
- `tools/outreach_tracker.py` — manages prospect list and follow-up schedule

## Steps

### 1. Load starter prospects
```
python tools/outreach_tracker.py --init-starters
```
This loads 8 pre-identified local prospects. View them:
```
python tools/outreach_tracker.py
```

### 2. Research additional prospects
For each prospect type, find 5–10 facilities in the service area:
- Physician offices: search Google Maps "primary care Gwinnett County"
- Urgent care: search "urgent care Lawrenceville GA", "urgent care Duluth GA"
- Senior living: search "assisted living Snellville GA", "senior living Gwinnett"
- Corporate HR: target large employers in Gwinnett Industrial Park, Distribution Centers

Add each to the tracker:
```
python tools/outreach_tracker.py --add "Clinic Name" "email@clinic.com" physician
```

### 3. Send first outreach email
Use the template from `outreach_tracker.py` output (bottom of the log file).
Customize the first paragraph to reference something specific to their practice.

After sending:
```
python tools/outreach_tracker.py --update "Clinic Name" contacted
```

### 4. Follow-up schedule
Check for due follow-ups every Monday:
```
python tools/outreach_tracker.py --due
```
- Follow-up 1: 7 days after first contact
- Follow-up 2: 7 days after follow-up 1
- After 2 follow-ups with no response: mark as `no_response`

### 5. When they say yes
Ask them to add a link to their resources/referral page with:
- Anchor text: "Mobile Phlebotomy Services" or "Fastrak Mobile Lab"
- URL: https://fastrakmobilelab.com or relevant service page

Once live:
```
python tools/outreach_tracker.py --update "Clinic Name" link_live --url "https://theirsite.com/resources"
```

## Expected Output
- 20–40 active prospects in tracker
- 5–10 links live within 60 days
- Each healthcare domain link worth far more than a directory citation (DR lift + relevance signal)

## What Makes a Good Ask
- Frame as a referral partnership, not a link request
- Emphasize patient benefit: convenient, insured, licensed, comes to them
- Offer reciprocal value: you'll refer any patient asking for a primary care recommendation to them

## Edge Cases
- If the facility already has a lab services referral list: ask to be added to it specifically
- If they want a formal partnership agreement: draft a simple one-page referral agreement (no exclusivity)
- Medical facilities with strict marketing policies: approach the patient experience or community outreach department instead of the medical director
- Senior living: facilities director or activity coordinator is the right contact, not medical staff
