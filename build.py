#!/usr/bin/env python3
"""Builds the Tri-State Bed Bug K9 Council site.

Outputs:
  site/            multi-page static site, ready to upload to any static host
  preview.html     single-file preview (hash-routed) used for the shareable artifact

Edit the PLACEHOLDERS dict below, then run:  python3 build.py
"""
import json
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))
import logo

ROOT = pathlib.Path(__file__).resolve().parent

# ---- Fill these in -------------------------------------------------------
P = {
    "org": "Tri-State Bed Bug K9 Council",
    "short": "Tri-State K9",
    "domain": "k9council.org",
    "year": "2026",
    "fee_reg": "$225",      # annual registration (membership) fee per team; matches NESDCA's $225 annual membership fee. The exam itself is free; teams reimburse evaluator travel.
}
# --------------------------------------------------------------------------

# Public registry. Basis: "E" = passed a Tri-State K9 field evaluation,
# "G" = grandfathered for the 2026-27 founding year (current prior certification,
# listed with the team's permission; must evaluate directly with the Council at renewal).
# Field evaluation = date of the team's most recent passed field evaluation.
# Valid through = 12 months after that date.
# (credential, handler, dog, company, state, basis, field evaluation, valid through)
TEAMS = [
    ("TSK9-2026-6290", "Kevin Skinner", "Chip", "A & C Pest Management", "NY", "G", "Oct 7, 2026", "Oct 7, 2027"),
    ("TSK9-2026-6516", "Diana Ludwiczak", "Ecko", "Doctor Sniffs", "NY", "G", "Oct 6, 2026", "Oct 6, 2027"),
    ("TSK9-2026-5642", "Diana Ludwiczak", "Goosey", "Doctor Sniffs", "NY", "G", "Oct 6, 2026", "Oct 6, 2027"),
    ("TSK9-2026-4141", "Diana Ludwiczak", "Southy", "Doctor Sniffs", "NY", "G", "Oct 6, 2026", "Oct 6, 2027"),
    ("TSK9-2026-1769", "Richard Conti", "Ecko", "Doctor Sniffs", "NY", "G", "Oct 7, 2026", "Oct 7, 2027"),
    ("TSK9-2026-2274", "Richard Conti", "Goosey", "Doctor Sniffs", "NY", "G", "Oct 7, 2026", "Oct 7, 2027"),
    ("TSK9-2026-7199", "Richard Conti", "Southy", "Doctor Sniffs", "NY", "G", "Oct 7, 2026", "Oct 7, 2027"),
    ("TSK9-2026-4615", "Ruben Jorge", "Roxy", "NYC Bed Bug Inspections", "NY", "G", "Oct 7, 2026", "Oct 7, 2027"),
    ("TSK9-2026-3581", "Scott Palatnik", "Hunter", "Long Island Bed Bug Inspections", "NY", "G", "Oct 8, 2026", "Oct 8, 2027"),
    ("TSK9-2026-7793", "Glen Wheelock", "Matcha", "M & M Pest Control", "NY", "G", "Oct 7, 2026", "Oct 7, 2027"),
    ("TSK9-2026-5451", "Herbert Yan", "Trooper", "M & M Pest Control", "NY", "G", "Oct 6, 2026", "Oct 6, 2027"),
    ("TSK9-2026-2420", "Eric Miller", "Mocha", "Express Bed Bug Inspection", "NJ", "G", "Mar 24, 2026", "Mar 24, 2027"),
    ("TSK9-2026-6215", "Alex Hernandez", "Isaac", "Diamond Dogs", "CT", "G", "Oct 8, 2026", "Oct 8, 2027"),
    ("TSK9-2026-7775", "Jill Meyer", "Finnagan", "Harlem River Hounds", "CT", "G", "Jul 23, 2026", "Jul 23, 2027"),
    ("TSK9-2026-4891", "Jill Meyer", "Lucy", "Harlem River Hounds", "CT", "G", "Jul 23, 2026", "Jul 23, 2027"),
    ("TSK9-2026-9035", "Lynnette Milleville", "Rose", "Nutmeg Farm LLC", "CT", "G", "Oct 8, 2026", "Oct 8, 2027"),
]

COMPANY_SITES = {
    "NYC Bed Bug Inspections": "https://nycbedbuginspections.com/",
    "Diamond Dogs": "https://diamonddogsipm.com/",
    "Harlem River Hounds": "http://www.harlemriverhounds.com/",
    "Nutmeg Farm LLC": "http://www.nutmegfarm.net",
    "Express Bed Bug Inspection": "https://expressbedbuginspection.com/",
    "A & C Pest Management": "https://www.acpest.com/",
    "Doctor Sniffs": "https://doctorsniffs.com/",
    "Long Island Bed Bug Inspections": "https://longislandbedbuginspections.com/",
    "M & M Pest Control": "https://www.mandmpestcontrol.com/",
}

PAGES = [
    ("home", "index.html", "Home"),
    ("events", "events.html", "Events"),
    ("standards", "standards.html", "Standards"),
    ("apply", "applications.html", "Applications"),
    ("certified", "certified-teams.html", "Certified Teams"),
    # ("board", "board.html", "Board"),  # hidden for now; uncomment to bring back (also restore the footer link)
    ("contact", "contact.html", "Contact"),
    ("privacy", "privacy.html", "Privacy & cookies"),
]
NAV_HIDE = {"privacy"}

DESC = {
    "home": "Independent bed bug scent detection certification for K9 teams in New York, New Jersey and Connecticut. Dogs are tested on live bed bug odor only.",
    "events": "Upcoming bed bug scent detection evaluation days for K9 teams across New York, New Jersey and Connecticut.",
    "standards": "The bed bug scent detection standard: live bed bug hides, distractors, blind conditions and pass criteria for certified K9 teams.",
    "apply": "Request a bed bug scent detection evaluation for your K9 team in New York, New Jersey or Connecticut.",
    "certified": "Verify a K9 team's bed bug scent detection credential. Search certified teams in NY, NJ and CT.",
    "contact": "Contact the Tri-State Bed Bug K9 Council about bed bug scent detection certification.",
    "privacy": "How the Tri-State Bed Bug K9 Council handles form submissions and cookies.",
}

LOGO = logo.mark()
STRIP = '<div class="scent-strip"><div class="wrap"><strong>Bed bug scent detection certification</strong><span class="sep" aria-hidden="true">&middot;</span><span>K9 teams tested on live bed bug odor only</span></div></div>'

def nav(mode, active):
    items = []
    for key, fn, label in PAGES:
        if key in NAV_HIDE: continue
        href = f"#{key}" if mode == "preview" else fn
        cur = ' aria-current="page"' if key == active and mode == "site" else ""
        items.append(f'<li><a href="{href}" data-route="{key}"{cur}>{label}</a></li>')
    home = "#home" if mode == "preview" else "index.html"
    req = "#apply" if mode == "preview" else "applications.html"
    return f"""<header class="site-head"><div class="wrap head-row">
<a class="brand" href="{home}">{LOGO}<span><strong>TRI-STATE</strong><small>Bed Bug K9 Council</small></span></a>
<button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav id="site-nav" aria-label="Main"><ul>{''.join(items)}</ul></nav>
<a class="btn btn-sm head-cta" href="{req}">Request evaluation</a>
</div></header>"""

def L(mode, key):
    """link to a page in either mode"""
    for k, fn, _ in PAGES:
        if k == key:
            return f"#{k}" if mode == "preview" else fn
    raise KeyError(key)

def footer(mode):
    return f"""<footer class="site-foot"><div class="wrap foot-grid">
<div><a class="brand brand-foot" href="{L(mode,'home')}">{LOGO}<span><strong>TRI-STATE</strong><small>Bed Bug K9 Council</small></span></a>
<p class="muted">Independent bed bug scent detection certification for K9 teams working in New York, New Jersey and Connecticut. Tested on live bed bug odor only.</p></div>
<div><h4>Council</h4><ul><li><a href="{L(mode,'standards')}">Standards &amp; by-laws</a></li><li><a href="{L(mode,'events')}">Event calendar</a></li></ul></div>
<div><h4>Teams</h4><ul><li><a href="{L(mode,'apply')}">Request an evaluation</a></li><li><a href="{L(mode,'certified')}">Verify a team</a></li></ul></div>
<div><h4>Contact</h4><p class="sel">Questions? Use the <a href="{L(mode,'contact')}">contact form</a>.</p><ul><li><a href="{L(mode,'privacy')}">Privacy &amp; cookies</a></li></ul></div>
</div><div class="wrap foot-base"><span>&copy; {P['year']} {P['org']}. All rights reserved.</span><span>{P['domain']}</span></div></footer>"""

# ---------------------------------------------------------------- pages
def page_home(m):
    return f"""
<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow"><span>Bed bug scent detection certification <span class="nw">&middot; NY &middot; NJ &middot; CT</span></span></p>
<h1>Certified bed bug K9 teams. Independently verified.</h1>
<p class="lede">The {P['org']} certifies K9 scent detection teams on one thing: finding live bed bug odor. Every team is tested against one strict, bed-bug-only field standard, run by evaluators who live and work in the region.</p>
<div class="cta-row"><a class="btn" href="{L(m,'apply')}">Request an evaluation</a><a class="btn btn-ghost" href="{L(m,'certified')}">Verify a certified team</a></div>
<div class="trust-row"><span><i class="dot d-ny"></i>Blind field testing</span><span><i class="dot d-nj"></i>Live bed bug hides</span><span><i class="dot d-ct"></i>Renewed every 12 months</span></div>
</div>
<div class="hero-visual">
<div class="cred" aria-label="Example credential card">
<div class="cred-top">{logo.mark(cls="mark")}<div><strong>TRI-STATE K9</strong><small>CERTIFIED TEAM</small></div><span class="cred-status">SAMPLE</span></div>
<dl><div class="cred-id"><dt>Credential</dt><dd>TSK9-YYYY-NNNN</dd></div>
<div><dt>Handler</dt><dd>Handler name</dd></div><div><dt>Canine</dt><dd>Dog's name</dd></div>
<div><dt>Region</dt><dd>NY &middot; NJ &middot; CT</dd></div><div><dt>Valid through</dt><dd class="num">12 months</dd></div></dl>
<div class="cred-lines"></div>
</div>
<p class="cred-caption">Example of the credential every passing team receives.</p>
</div>
</div><div class="routes" aria-hidden="true"><i></i><i></i><i></i></div></section>

<section class="wrap split-cards">
<a class="feature" href="{L(m,'certified')}"><span class="eyebrow">Hiring a K9 inspector?</span><h2>Verify a team</h2><p>Look up a handler's credential number, the dog's name and the date the certification expires before you book an inspection.</p><span class="arrow">Search the registry</span></a>
<a class="feature feature-alt" href="{L(m,'apply')}"><span class="eyebrow">Handlers &amp; companies</span><h2>Get your team certified</h2><p>Book a blind field evaluation with a Council evaluator in New York, New Jersey or Connecticut.</p><span class="arrow">Start an application</span></a>
</section>

<section class="wrap section about">
<div class="about-text">
<p class="eyebrow">Who we are</p>
<h2>Built by Tri-State pest professionals, for one pest</h2>
<p>Detection dogs now handle a large share of bed bug inspections in apartments, hotels, dorms and offices across the region. Clients deserve to know that a dog's alert is reliable. Our members are pest management operators, handlers and entomologists who work these buildings every day.</p>
<p>We focus on bed bugs and nothing else. We don't train dogs or sell inspections. We write the standard, train the evaluators, run the tests and publish the results.</p>
</div>
<dl class="stat-strip">
<div><dt>Live hides found to pass</dt><dd>2 of 2</dd></div>
<div><dt>False responses allowed</dt><dd>&le; 1</dd></div>
<div><dt>Renewal cycle</dt><dd>12 mo</dd></div>
<div><dt>Exam fee</dt><dd>$0</dd></div>
</dl>
</section>

<section class="band-tint"><div class="wrap section">
<p class="eyebrow">How certification works</p>
<h2>From application to the public registry</h2>
<ol class="steps">
<li><h3>Apply</h3><p>Send the team evaluation request with the dog's bed bug odor training log and vaccination records.</p></li>
<li><h3>Schedule</h3><p>Pick a scheduled evaluation day with no travel fee, or request an on-site evaluation at your location with a travel fee. Registration is paid before test day.</p></li>
<li><h3>Field test</h3><p>Your team searches a building of at least four rooms holding two live bed bug hides and two distractors, in 15 minutes. Two evaluators watch; hide locations stay secret.</p></li>
<li><h3>Get listed</h3><p>Pass and you receive a numbered credential and a public registry listing for 12 months.</p></li>
</ol>
</div></section>

<section class="wrap section" style="display:grid;gap:24px">
<p class="eyebrow">Coverage</p>
<h2>Evaluators across the region</h2>
<div class="coverage">
<div class="state" style="--c:var(--ny)"><h3>New York <span>NY</span></h3><p>All five boroughs, Long Island, Westchester and the Hudson Valley.</p></div>
<div class="state" style="--c:var(--nj)"><h3>New Jersey <span>NJ</span></h3><p>North Jersey, the Shore and the Philadelphia suburbs.</p></div>
<div class="state" style="--c:var(--ct)"><h3>Connecticut <span>CT</span></h3><p>Fairfield County, New Haven, Hartford and the shoreline.</p></div>
</div>
</section>

<section class="wrap section info-pair" style="padding-top:0">
<div><h3>Looking for a trainer?</h3><p>The Council does not train dogs. <a href="{L(m,'contact')}">Contact us</a> and we'll send you our list of approved bed bug scent detection trainers in New York, New Jersey and Connecticut.</p></div>
<div><h3>What it costs</h3><p>The exam itself is free. Each team pays a {P['fee_reg']} annual registration. There's no travel fee at scheduled evaluation days. A travel fee (government mileage rate plus a flat per diem) applies only if you request an on-site evaluation outside a scheduled date.</p></div>
<div><h3>Property managers</h3><p>Ask any K9 inspection company for its credential number, then <a href="{L(m,'certified')}">confirm it here</a> before you sign.</p></div>
</section>"""

def page_events(m):
    # Add real evaluation days here: ("Feb 18, 2027", "Group field evaluations", "Queens, NY", "Evaluation")
    rows = [
        # Placeholder schedule (edit to real dates/locations): (date, event, location, type)
        ("Feb 17, 2027", "Group field evaluations", "Long Island, NY", "Evaluation"),
        ("Mar 11, 2027", "Group field evaluations", "Northern NJ", "Evaluation"),
        ("Apr 21, 2027", "Group field evaluations", "Fairfield County, CT", "Evaluation"),
        ("May 13, 2027", "Group field evaluations", "New York City, NY", "Evaluation"),
        ("Jun 16, 2027", "Group field evaluations", "Central NJ", "Evaluation"),
        ("Jul 22, 2027", "Group field evaluations", "Hartford area, CT", "Evaluation"),
    ]
    tr = "".join(f'<tr><td class="num e-date">{d}</td><td class="e-name">{t}</td><td class="e-loc">{l}</td><td class="e-type"><span class="pill pill-{k.lower()}">{k}</span></td></tr>' for d,t,l,k in rows)
    return f"""<section class="wrap page-head"><p class="eyebrow">Calendar</p><h1>Upcoming events</h1>
<p class="lede">Bed bug scent detection evaluation days across the Tri-State. No travel fee at scheduled evaluation days. Register at least 30 days ahead so we can prepare live bed bug odor hides.</p></section>
<section class="wrap section-tight">{('<div class="table-scroll mcards"><table id="event-table"><thead><tr><th>Date</th><th>Event</th><th>Location</th><th>Type</th></tr></thead><tbody>' + tr + '</tbody></table></div>') if rows else ('<div class="empty-state"><h3>2027 evaluation days coming soon</h3><p>The first group evaluation dates for New York, New Jersey and Connecticut are being set now. Request an evaluation and we will email you as soon as dates near you are posted.</p><a class="btn" href="' + L(m,'apply') + '">Request an evaluation</a></div>')}
<p>Can't make a scheduled date? Request an on-site evaluation at your location. An evaluator travel fee applies. <a href="{L(m,'apply')}">Request an evaluation</a> or <a href="{L(m,'contact')}">contact us</a> with the number of teams and a preferred month.</p></section>"""

def page_standards(m):
    return f"""<section class="wrap page-head"><p class="eyebrow">Governance</p><h1>Standards &amp; by-laws</h1>
<p class="lede">The bed bug scent detection standard every certified K9 team is tested against, using live bed bug odor only, and the by-laws that govern the Council.</p></section>
<section class="wrap section-tight two-col">
<article class="doc">
<h2>Certification rules (summary)</h2>
<h3>1. We certify teams</h3><p>Certification belongs to one handler working one dog. If a dog changes handlers, the new pairing is a new team and must be evaluated.</p>
<h3>2. Eligibility</h3><p>Dogs must be at least 12 months old, current on vaccinations, and trained on live bed bug (<em>Cimex lectularius</em>) odor only. Dual-scent dogs are not eligible. Handlers must be 18 or older and may not hold a revoked credential from any certifying body.</p>
<h3>3. Test site</h3><p>A building with at least four rooms: a residence, an office or multi-room interior, or a hotel, dorm or school.</p>
<h3>4. Hides</h3><p>Four hides: two live bed bug hides (5 to 15 live bed bugs each, number set by the evaluators) and two distractors chosen by the chief evaluator. Live hides are placed in separate rooms, and no distractor shares a room with a live hide. Hides are set at least 30 minutes before the search, out of sight of the team. Pseudo-scents are never used.</p>
<h3>5. Search and alerts</h3><p>The search runs 15 minutes, adjusted for building size and agreed before the start. The handler declares the dog's alert style (passive or active), and the dog must alert at the source. Each alert is confirmed by a reward or by the handler calling it.</p>
<h3>6. Passing</h3><p>The team must find both live hides. One false response is allowed, but any response on a distractor is an automatic fail. A dog that won't work may be pulled and retried once within 30 minutes.</p>
<h3>7. Evaluators</h3><p>Two Council evaluators attend every test. The chief evaluator makes the final call, and no evaluator may judge a team they trained or employ.</p>
<h3>8. Handling</h3><p>Harsh corrections are grounds for failure. Pinch collars, electronic or ultrasonic collars, sticks and whips are not allowed during testing.</p>
<h3>9. Credential</h3><p>Passing teams receive a credential numbered <code>TSK9-YYYY-NNNN</code>, valid for 12 months and for bed bug scent detection only. Teams may not claim any other odor under it.</p>
<h3>10. Retests and appeals</h3><p>After a failed evaluation, a team waits 14 days to retest and may not present itself as certified in the meantime. A certified team that fails a retest loses its current credential. Appeals are announced at the test and filed in writing within 14 days; the Certification Chair's decision is final.</p>
<h3>11. Revocation</h3><p>The Council may suspend or revoke a credential for misrepresentation, animal welfare concerns or verified field failures.</p>
</article>
<aside class="side-list"><h3>Documents</h3><ul class="doc-list">
<li><span>Council by-laws</span><a class="muted" href="{L(m,'contact')}">Request a copy</a></li>
<li><span>Full certification rules</span><a class="muted" href="{L(m,'contact')}">Request a copy</a></li>
<li><span>Evaluator code of conduct</span><a class="muted" href="{L(m,'contact')}">Request a copy</a></li>
<li><span>Hide preparation guide</span><a class="muted" href="{L(m,'contact')}">Request a copy</a></li>
</ul></aside>
</section>"""

def form_eval(m):
    attrs = 'name="evaluation" method="POST" data-netlify="true"' if m == "site" else 'name="evaluation"'
    return f"""<form class="form" id="eval-form" {attrs}>
<input type="hidden" name="form-name" value="evaluation">
<div class="row2"><label for="ev-name">Handler name<input id="ev-name" name="handler" required></label>
<label for="ev-company">Company<input id="ev-company" name="company"></label></div>
<div class="row2"><label for="ev-email">Email<input id="ev-email" type="email" name="email" required></label>
<label for="ev-phone">Phone<input id="ev-phone" type="tel" name="phone"></label></div>
<div class="row2"><label for="ev-dog">Dog's name<input id="ev-dog" name="dog" required></label>
<label for="ev-age">Dog's age (months)<input id="ev-age" type="number" min="12" name="dog_age" required></label></div>
<div class="row2"><label for="ev-state">State<select id="ev-state" name="state"><option>New York</option><option>New Jersey</option><option>Connecticut</option></select></label>
<label for="ev-type">Evaluation type<select id="ev-type" name="type"><option>New certification</option><option>Annual renewal</option><option>New handler and dog pairing</option><option>Retest after a failed evaluation</option></select></label></div>
<label for="ev-where">Where<select id="ev-where" name="where"><option>Scheduled evaluation day (no travel fee)</option><option>On-site at my location (travel fee applies)</option></select></label>
<label for="ev-notes">Training history<textarea id="ev-notes" name="notes" rows="4" placeholder="Trainer, training hours on live bed bug odor, prior certifications"></textarea></label>
<button class="btn" type="submit">Submit application</button>
<p class="form-msg" role="status" hidden>Thanks. Your application was received and we will reply within two business days.</p>
</form>"""

def page_apply(m):
    return f"""<section class="wrap page-head"><p class="eyebrow">Applications &amp; forms</p><h1>Request a team evaluation</h1>
<p class="lede">Start your team's bed bug scent detection certification or renewal. Your dog will be tested on live bed bug odor in blind hides. We'll confirm your evaluators and test date by email, plus a travel estimate if you request an on-site evaluation.</p></section>
<section class="wrap section-tight two-col">
<div>{form_eval(m)}</div>
<aside class="side-list"><h3>Before you apply</h3><ul class="check">
<li>Dog is 12 months or older</li><li>Dog trained on bed bug odor only (no dual-scent dogs)</li><li>Vaccination records on hand</li><li>Training log for live bed bug odor</li><li>Two sealed live bed bug hide containers for evaluator approval</li><li>{P['fee_reg']} annual team registration paid</li><li>On-site evaluation outside a scheduled date? Evaluator travel fee paid before test day</li></ul>
<h3>Where tests happen</h3><p class="sel">At a scheduled evaluation day, with no travel fee, or on-site at a Council-approved location your team provides, with an evaluator travel fee. Tests may not be run for profit.</p>
<h3>Other forms</h3><ul class="doc-list"><li><span>Evaluator application</span><span class="muted">Request via contact form</span></li><li><span>Training facility approval</span><span class="muted">Request via contact form</span></li><li><span>Complaint / field report</span><span class="muted">Request via contact form</span></li></ul></aside>
</section>"""

def site_link(co):
    u = COMPANY_SITES.get(co)
    if not u: return '<span class="muted">&mdash;</span>'
    label = u.split("//",1)[-1].removeprefix("www.").rstrip("/")
    return f'<a class="ext" href="{u}" target="_blank" rel="noopener">{label}</a>'

def page_certified(m):
    chips = "".join(f'<button type="button" class="chip" data-state="{k}" aria-pressed="{"true" if k=="ALL" else "false"}">{"" if k=="ALL" else f"<i class=dot style=background:var(--{k.lower()})></i>"}{lbl}</button>' for k,lbl in [("ALL","All"),("NY","New York"),("NJ","New Jersey"),("CT","Connecticut")])
    if TEAMS:
        tr = "".join(f'<tr data-state="{s}"><td class="c-id"><code>{c}</code>{'<a class="fy" href="#grandfather" title="Listed under a prior certification">&dagger;</a>' if b=="G" else ""}</td><td class="c-h">{h}</td><td class="c-d" data-label="Dog">{d}</td><td class="c-co">{co}</td><td class="c-st"><span class="st"><i class="dot d-{s.lower()}"></i>{s}</span></td><td class="c-web">{site_link(co)}</td><td class="num c-ev" data-label="Field evaluation">{ev}</td><td class="num c-exp" data-label="Valid through">{e}</td></tr>' for c,h,d,co,s,b,ev,e in TEAMS)
        body = f"""<div class="reg-tools"><label class="search" for="team-search">Search by name, dog or team #<input id="team-search" type="search" placeholder="e.g. TSK9-2026-6290"></label><div class="chips">{chips}</div></div>
<div class="table-scroll mcards"><table id="team-table"><thead><tr><th>Team #</th><th>Handler</th><th>Dog</th><th>Company</th><th>State</th><th>Website</th><th>Field evaluation</th><th>Valid through</th></tr></thead><tbody>{tr}</tbody></table></div>
<p class="empty" id="team-empty" hidden>No current team matches that search.</p>
<div class="note-box" id="grandfather"><h3><span class="fy">&dagger;</span> Policy</h3><p>Teams that already held a current bed bug detection certification from a recognized certifying body, based on a passed blind field evaluation, are listed. Their listing runs 12 months from that field evaluation. To renew, every team must pass a Tri-State K9 field evaluation directly.</p></div>"""
    else:
        body = f"""<div class="empty-state"><h3>The first certification cycle is underway</h3>
<p>Teams appear here as soon as they pass a Tri-State K9 field evaluation. If you're a handler in New York, New Jersey or Connecticut, you can book one of the first evaluation slots now.</p>
<a class="btn" href="{L(m,'apply')}">Request an evaluation</a></div>"""
    return f"""<section class="wrap page-head"><p class="eyebrow">Registry</p><h1>Certified teams</h1>
<p class="lede">Every K9 team listed is certified in bed bug scent detection and passed a blind field evaluation on live bed bug odor within the last 12 months. See the <a href="#grandfather">policy</a> below. If a team isn't listed, its Tri-State K9 credential is not current.</p></section>
<section class="wrap section-tight">{body}</section>
<section class="wrap section info-pair" id="trainers" style="padding-top:24px">
<div><h3>Approved training facilities</h3><p>Facilities whose curriculum meets Council odor and welfare guidelines. <a href="{L(m,'contact')}">Request the Tri-State list</a> through our contact form.</p></div>
<div><h3>Evaluators</h3><p>Council-trained evaluators who run field tests. Evaluators may not test teams they trained or employ. <a href="{L(m,'contact')}">Ask about becoming an evaluator</a>.</p></div>
<div><h3>Odor suppliers</h3><p>Sources of live bed bug colonies and training aids that meet our handling rules. <a href="{L(m,'contact')}">Request the list</a> through our contact form.</p></div>
</section>"""

def page_board(m):
    roles = ["President","Vice President","Secretary","Treasurer","Director, Evaluations","Director, Entomology"]
    cards = "".join(f'<li class="person"><span class="avatar" aria-hidden="true">{r[0]}</span><div><strong>[Name]</strong><span class="muted">{r}</span></div></li>' for r in roles)
    return f"""<section class="wrap page-head"><p class="eyebrow">Leadership</p><h1>Board of directors</h1>
<p class="lede">Volunteer directors from pest management, canine scent detection and entomology, focused on one discipline: bed bug odor detection. Directors are elected by members for two-year terms and must work in New York, New Jersey or Connecticut.</p></section>
<section class="wrap section-tight"><ul class="people">{cards}</ul>
<p class="note">Add each director's name, company and a short bio.</p>
<div class="callout"><h3>Members area</h3><p>Certified teams and evaluators can sign in to download score sheets and meeting minutes. <span class="muted">Connect a members login when you're ready.</span></p></div></section>"""

def page_contact(m):
    attrs = 'name="contact" method="POST" data-netlify="true"' if m == "site" else 'name="contact"'
    return f"""<section class="wrap page-head"><p class="eyebrow">Contact</p><h1>Contact the Council</h1>
<p class="lede">Questions about bed bug scent detection certification, our odor standards, evaluations or a listed team. Looking for a trainer? Choose "Approved trainer list" below.</p></section>
<section class="wrap section-tight two-col">
<form class="form" id="contact-form" {attrs}><input type="hidden" name="form-name" value="contact">
<div class="row2"><label for="c-name">Name<input id="c-name" name="name" required></label><label for="c-email">Email<input id="c-email" type="email" name="email" required></label></div>
<label for="c-topic">Topic<select id="c-topic" name="topic"><option>Evaluation question</option><option>Approved trainer list</option><option>Verify a team</option><option>Become an evaluator</option><option>Report a concern</option><option>Other</option></select></label>
<label for="c-msg">Message<textarea id="c-msg" name="message" rows="5" required></textarea></label>
<button class="btn" type="submit">Send message</button>
<p class="form-msg" role="status" hidden>Thanks. Your message was received.</p></form>
<aside class="side-list"><h3>How we respond</h3><p class="sel">All inquiries come through this form so every request is logged and routed to the right person.</p><p class="sel">We reply by email, usually within two business days.</p></aside>
</section>"""

def page_privacy(m):
    return f"""<section class="wrap page-head"><p class="eyebrow">Legal</p><h1>Privacy &amp; cookies</h1>
<p class="lede">How the {P['org']} handles information you send us and the small amount of data this website stores.</p></section>
<section class="wrap section-tight"><article class="doc">
<h3>Information you send us</h3><p>When you submit the evaluation request or contact form, we receive what you type: typically your name, email, phone number, company and details about your K9 team. We use it only to respond, schedule evaluations and maintain the certified team registry. We do not sell or rent it.</p>
<h3>Public registry</h3><p>For certified teams, the registry shows the credential number, handler name, dog name, company, state, company website and certification dates, so clients can verify a team. Teams may contact us through the contact form to correct a listing.</p>
<h3>Cookies</h3><p>This site does not use advertising or tracking cookies. It uses only what is strictly necessary to work: your browser remembers that you dismissed the cookie notice, and our hosting provider may set technical cookies to keep forms secure and prevent spam. Fonts are loaded from Google Fonts, which receives your IP address to deliver them.</p>
<h3>Where data is stored</h3><p>Form submissions are processed and stored by our website host, Netlify, and forwarded to the Council by email.</p>
<h3>Your choices</h3><p>You can ask us to see, correct or delete information you sent by using the <a href="{L(m,'contact')}">contact form</a>. You can clear or block cookies in your browser settings at any time.</p>
<p class="muted">Last updated November 2026.</p>
</article></section>"""

BUILDERS = {"home": page_home, "events": page_events, "standards": page_standards, "apply": page_apply,
            "certified": page_certified, "board": page_board, "contact": page_contact, "privacy": page_privacy}

CSS = (ROOT / "src" / "styles.css").read_text()
JS = (ROOT / "src" / "app.js").read_text()
COOKIE = '<div class="cookie" id="cookie" role="region" aria-label="Cookie notice" hidden><p>We use only essential cookies to run this site and keep our forms secure. No advertising or tracking. <a href="privacy.html" data-route-link="privacy">Learn more</a></p><button class="btn btn-sm" type="button" id="cookie-ok">OK</button></div>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,500..900&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">'

def build_site():
    out = ROOT / "site"; out.mkdir(exist_ok=True)
    (out / "styles.css").write_text(CSS)
    (out / "app.js").write_text(JS)
    (out / "logo.svg").write_text(logo.standalone())
    (out / "logo-white.svg").write_text(logo.standalone(dark=True))
    (out / "favicon.svg").write_text(logo.standalone_mark())
    for key, fn, label in PAGES:
        title = f"{P['org']} | Bed Bug Scent Detection Certification" if key == "home" else f"{label} | {P['org']}"
        url = f"https://{P['domain']}/" + ("" if key == "home" else fn)
        desc = DESC.get(key, DESC["home"])
        ld = ""
        if key == "home":
            ld = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Organization","name":P["org"],"alternateName":P["short"],"url":f"https://{P['domain']}/","logo":f"https://{P['domain']}/logo.png","description":DESC["home"],"areaServed":[{"@type":"State","name":n} for n in ("New York","New Jersey","Connecticut")]}) + '</script>'
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{url}"><meta name="robots" content="index, follow">
<meta name="theme-color" content="#0c1b2e"><meta name="color-scheme" content="light dark">
<meta property="og:type" content="website"><meta property="og:site_name" content="{P['org']}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://{P['domain']}/og-image.png"><meta property="og:image:width" content="2400"><meta property="og:image:height" content="1260"><meta property="og:image:alt" content="Tri-State Bed Bug K9 Council logo: bed bug scent detection certification for NY, NJ and CT"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="https://{P['domain']}/og-image.png">
<link rel="icon" href="favicon.ico" sizes="48x48"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png" sizes="180x180"><link rel="manifest" href="site.webmanifest">{ld}
{FONTS}<link rel="stylesheet" href="styles.css"></head><body>
{nav('site', key)}{STRIP}<main id="main">{BUILDERS[key]('site')}</main>{footer('site')}
{COOKIE}<script src="app.js"></script></body></html>"""
        (out / fn).write_text(html)
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{P['domain']}/sitemap.xml\n")
    urls = "".join(f"<url><loc>https://{P['domain']}/{'' if k=='home' else fn}</loc></url>" for k, fn, _ in PAGES)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (out / "site.webmanifest").write_text(json.dumps({"name":P["org"],"short_name":P["short"],"icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"favicon.svg","sizes":"any","type":"image/svg+xml"}],"theme_color":"#0c1b2e","background_color":"#0c1b2e","display":"browser"}))
    for f in ("og-image.png", "apple-touch-icon.png", "logo.png", "favicon.ico", "favicon-32.png", "icon-192.png", "icon-512.png"):
        src = ROOT / "brand" / f
        if src.exists(): (out / f).write_bytes(src.read_bytes())

def build_preview():
    views = "".join(f'<div class="view" data-view="{k}"{"" if k=="home" else " hidden"}>{BUILDERS[k]("preview")}</div>' for k,_,_ in PAGES)
    html = f"""<title>Tri-State Bed Bug K9 Council</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}<style>{CSS}</style>
{nav('preview','home')}{STRIP}<main id="main">{views}</main>{footer('preview')}
{COOKIE}<script>{JS}</script>"""
    (ROOT / "preview.html").write_text(html)

build_site(); build_preview()
print("built site/ and preview.html")
