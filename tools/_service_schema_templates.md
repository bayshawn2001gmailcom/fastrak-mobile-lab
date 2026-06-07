# Fastrak Mobile Lab — Service Schema Templates

Use these in Rank Math's **Custom Schema** field on individual service/city pages.
`serviceType` is a `Service` property — this is the CORRECT place for it.

---

## Mobile Phlebotomy Service Pages

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Mobile Phlebotomy in [City], GA",
  "serviceType": "Mobile Phlebotomy",
  "description": "Licensed phlebotomists travel to your home or office in [City], GA for blood draws. Samples delivered to LabCorp or Quest Diagnostics. No lab visit required.",
  "provider": {
    "@type": "MedicalBusiness",
    "name": "Fastrak Mobile Lab",
    "url": "https://fastrakmobilelab.com",
    "telephone": "+16785625244"
  },
  "areaServed": {
    "@type": "City",
    "name": "[City]",
    "addressRegion": "GA"
  },
  "availableChannel": {
    "@type": "ServiceChannel",
    "serviceUrl": "https://fastrakmobilelab.com/book/",
    "servicePhone": "+16785625244",
    "availableLanguage": "English"
  },
  "audience": {
    "@type": "Audience",
    "audienceType": "Elderly, disabled, busy professionals, patients with doctor requisitions"
  }
}
```

---

## DNA / Paternity Testing Pages

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Mobile DNA Paternity Testing in [City], GA",
  "serviceType": "DNA Testing",
  "description": "Mobile DNA and paternity testing in [City], GA. We collect samples at your location and deliver to certified labs. Court-admissible and private testing available.",
  "provider": {
    "@type": "MedicalBusiness",
    "name": "Fastrak Mobile Lab",
    "url": "https://fastrakmobilelab.com",
    "telephone": "+16785625244"
  },
  "areaServed": {
    "@type": "City",
    "name": "[City]",
    "addressRegion": "GA"
  }
}
```

---

## Drug Testing Pages (Pre-Employment / DOT)

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Mobile Drug Testing in [City], GA",
  "serviceType": "Drug Testing",
  "description": "Mobile pre-employment and DOT drug testing in [City], GA. We come to your workplace or home for specimen collection. Court-admissible results.",
  "provider": {
    "@type": "MedicalBusiness",
    "name": "Fastrak Mobile Lab",
    "url": "https://fastrakmobilelab.com",
    "telephone": "+16785625244"
  },
  "areaServed": {
    "@type": "City",
    "name": "[City]",
    "addressRegion": "GA"
  }
}
```

---

## Notes

- Replace `[City]` with the actual city name on each page
- The `MedicalBusiness` block (output by the mu-plugin globally) covers the business entity
- These `Service` blocks cover individual service offerings — this is the correct separation
- Do NOT add `serviceType` to the MedicalBusiness block — it does not belong there
- `medicalSpecialty` does NOT belong on MedicalBusiness (only valid on Hospital, MedicalClinic,
  MedicalOrganization, Physician) — leave it out entirely
- FAQ rich results deprecated by Google on May 7, 2026 — keep FAQPage schema on FAQ page
  but don't expect SERP rich snippets from it
