# Tri-State Bed Bug K9 Council website

Static site, no build tools needed to host it. Upload the `site/` folder to any static host.

## Fill these in before launch (edit the top of build.py, then run `python3 build.py`)
- Organization name: Tri-State Bed Bug K9 Council (rename if you like)
- Email: info@tristatebedbugk9.org (placeholder)
- Phone: (555) 010-0199 (placeholder)
- Mailing address: [Street address], [City], NY 00000
- Board of directors: names, companies, bios (board page)
- Event dates (events page, proposed dates only)
- Certification rules numbers (standards page, draft for your board to approve)
- PDF documents: by-laws, full rules, forms (currently "add file")
- Certified teams: the TEAMS list in build.py (empty until teams actually pass your evaluation)

## Domain
Recommended: tristatebedbugk9.org (available 2026-11-17), plus tristatebedbugk9.com to redirect to it.
Short alternate: tsbk9.org.

## Hosting (recommended: Netlify, free tier)
Drag the `site/` folder onto app.netlify.com/drop, then add the domain under Domain settings.
The evaluation and contact forms already include Netlify Forms attributes, so submissions show up in your Netlify dashboard and can be emailed to you.

## Logo files
site/logo.svg (light backgrounds), site/logo-white.svg (dark backgrounds), site/favicon.svg (icon only).

## Private
private/tristate-outreach-list.csv lists the NY/NJ/CT bed bug teams from NESDCA's public list, as an outreach list only.
Do not publish them as certified until each has passed your evaluation.
