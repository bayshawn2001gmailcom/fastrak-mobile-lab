# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Fastrak Mobile Lab** is a professional Mobile Phlebotomy and Specimen Collection service. Services include blood work, DNA testing, and drug testing — performed on-site at homes, corporate offices, and senior living facilities.

**Exclusions:** No career training. No COVID-19 testing.

## Commands

```bash
npm install   # Install dependencies
npm test      # Run tests
npm start     # Start the application
```

## Technology Stack

- **CRM/Funnels:** GoHighLevel (GHL)
- **Automation:** Agentic AI for booking, dispatching, and lead qualification
- **APIs:** Secure data webhooks, Google Maps API (route/logistics optimization)

## Core Strategy

Scaling is driven by **Route Density logic** — maximizing stops per geographic area to increase profit margins. Logistics code should reflect this: prioritize clustering, distance minimization, and stop sequencing when interfacing with Google Maps.

## Development Rules

### Tone & Language
- Clinical, professional, and authoritative. No promotional or "salesy" copy.
- Use precise medical terminology: *Specimen Integrity*, *Chain of Custody*, *Phlebotomy Services*, *Venipuncture*, *Requisition*, etc.

### Mobile-First
- Every script, form, and UI component must be optimized for mobile users first.
- Touch targets, responsive layouts, and minimal input friction are required.

### Privacy & Security
- All patient data handling must be built for high-security environments (HIPAA-aligned patterns).
- Standardize on secure webhooks; never log or expose PHI (Protected Health Information) in plaintext.
- Chain of Custody integrity must be preserved and auditable throughout specimen workflows.

### AI Automation
- Booking, dispatching, and lead qualification flows are handled by agentic AI — keep these interfaces clean and stateless where possible.
- Lead qualification logic should filter against service exclusions (no COVID testing, no training inquiries).
