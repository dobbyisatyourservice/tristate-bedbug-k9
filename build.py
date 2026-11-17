#!/usr/bin/env python3
"""Builds the Tri-State Bed Bug K9 Council site.

Outputs:
  site/            multi-page static site, ready to upload to any static host
  preview.html     single-file preview (hash-routed) used for the shareable artifact

Edit the PLACEHOLDERS dict below, then run:  python3 build.py
"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))
import logo

ROOT = pathlib.Path(__file__).resolve().parent

# ---- Fill these in -------------------------------------------------------
P = {
    "org": "Tri-State Bed Bug K9 Council",
    "short": "Tri-State K9",
    "domain": "tristatebedbugk9.org",
    "email": "info@tristatebedbugk9.org",
    "phone": "(555) 010-0199",
    "address": "[Street address], [City], NY 00000",
    "year": "2026",
}
# --------------------------------------------------------------------------

# Certified teams shown in the public registry. Add a team ONLY after it has
# passed a Tri-State K9 evaluation. Format:
# ("TSK9-2027-0001", "Handler name", "Dog", "Company", "NY", "Jan 2028"),
TEAMS = [
]

PAGES = [
    ("home", "index.html", "Home"),
    ("events", "events.html", "Events"),
    ("standards", "standards.html", "Standards"),
    ("apply", "applications.html", "Applications"),
    ("certified", "certified-teams.html", "Certified Teams"),
    ("board", "board.html", "Board"),
    ("contact", "contact.html", "Contact"),
]

LOGO = logo.mark()

def nav(mode, active):
    items = []
    for key, fn, label in PAGES:
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
<p class="muted">Independent certification for bed bug detection dog teams working in New York, New Jersey and Connecticut.</p></div>
<div><h4>Council</h4><ul><li><a href="{L(mode,'standards')}">Standards &amp; by-laws</a></li><li><a href="{L(mode,'board')}">Board of directors</a></li><li><a href="{L(mode,'events')}">Event calendar</a></li></ul></div>
<div><h4>Teams</h4><ul><li><a href="{L(mode,'apply')}">Request an evaluation</a></li><li><a href="{L(mode,'certified')}">Verify a team</a></li><li><a href="{L(mode,'certified')}#trainers">Approved trainers</a></li></ul></div>
<div><h4>Contact</h4><p class="sel">{P['email']}<br>{P['phone']}<br>{P['address']}</p></div>
</div><div class="wrap foot-base"><span>&copy; {P['year']} {P['org']}. All rights reserved.</span><span>{P['domain']}</span></div></footer>"""

# ---------------------------------------------------------------- pages
def page_home(m):
    return f"""
<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow">New York &middot; New Jersey &middot; Connecticut</p>
<h1>Certified noses for the Tri-State's bed bug inspections.</h1>
<p class="lede">The {P['org']} tests detection dog teams against one strict, bed-bug-only field standard, run by evaluators who live and work in the region.</p>
<div class="cta-row"><a class="btn" href="{L(m,'apply')}">Request an evaluation</a><a class="btn btn-ghost" href="{L(m,'certified')}">Verify a certified team</a></div>
<div class="trust-row"><span><i class="dot d-ny"></i>Blind field testing</span><span><i class="dot d-nj"></i>Live bed bug hides</span><span><i class="dot d-ct"></i>Renewed every 12 months</span></div>
</div>
<div class="hero-visual">
<div class="cred" aria-label="Example credential card">
<div class="cred-top">{logo.mark(cls="mark")}<div><strong>TRI-STATE K9</strong><small>CERTIFIED TEAM</small></div><span class="cred-status">ACTIVE</span></div>
<dl><div class="cred-id"><dt>Credential</dt><dd>TSK9-2027-0001</dd></div>
<div><dt>Handler</dt><dd>Your name here</dd></div><div><dt>Canine</dt><dd>Your dog</dd></div>
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
<div><dt>Hides found to pass</dt><dd>95%</dd></div>
<div><dt>False alerts allowed</dt><dd>&le; 1</dd></div>
<div><dt>Renewal cycle</dt><dd>12 mo</dd></div>
<div><dt>Evaluation fee</dt><dd>$0</dd></div>
</dl>
</section>

<section class="band-tint"><div class="wrap section">
<p class="eyebrow">How certification works</p>
<h2>From application to the public registry</h2>
<ol class="steps">
<li><h3>Apply</h3><p>Send the team evaluation form with the dog's training log and vaccination records.</p></li>
<li><h3>Schedule</h3><p>We match you with an evaluator in your state. Travel costs are paid before test day.</p></li>
<li><h3>Field test</h3><p>Your team searches furnished rooms seeded with live bed bugs, eggs and distractors. Hide locations stay secret.</p></li>
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
<div><h3>Looking for a trainer?</h3><p>The Council does not train dogs. For training questions, contact one of our <a href="{L(m,'certified')}#trainers">approved training facilities</a>.</p></div>
<div><h3>What it costs</h3><p>The evaluation itself is free. Evaluator mileage and travel time are paid before the evaluation date.</p></div>
<div><h3>Property managers</h3><p>Ask any K9 inspection company for its credential number, then <a href="{L(m,'certified')}">confirm it here</a> before you sign.</p></div>
</section>"""

def page_events(m):
    rows = [
        ("Feb 18, 2027", "Group field evaluations", "Queens, NY", "Evaluation"),
        ("Mar 11, 2027", "Evaluator training seminar", "Online", "Training"),
        ("Apr 15, 2027", "Group field evaluations", "Newark, NJ", "Evaluation"),
        ("May 20, 2027", "Group field evaluations", "Stamford, CT", "Evaluation"),
        ("Jun 24, 2027", "Annual members meeting", "New York, NY", "Meeting"),
    ]
    tr = "".join(f'<tr><td class="num">{d}</td><td>{t}</td><td>{l}</td><td><span class="pill pill-{k.lower()}">{k}</span></td></tr>' for d,t,l,k in rows)
    return f"""<section class="wrap page-head"><p class="eyebrow">Calendar</p><h1>Upcoming events</h1>
<p class="lede">Group evaluation days split travel costs between teams. Register at least 30 days ahead so we can prepare hides.</p></section>
<section class="wrap section-tight"><p class="note">Proposed dates. Confirm or change them before launch.</p>
<div class="table-scroll"><table><thead><tr><th>Date</th><th>Event</th><th>Location</th><th>Type</th></tr></thead><tbody>{tr}</tbody></table></div>
<p>Want an evaluation day near you? <a href="{L(m,'contact')}">Contact us</a> with the number of teams and a preferred month.</p></section>"""

def page_standards(m):
    return f"""<section class="wrap page-head"><p class="eyebrow">Governance</p><h1>Standards &amp; by-laws</h1>
<p class="lede">The rules every certified team is tested against, and the by-laws that govern the Council.</p></section>
<section class="wrap section-tight two-col">
<article class="doc">
<h2>Certification rules (summary)</h2>
<p class="note">Draft standard for you to review. Have your board approve the final numbers.</p>
<h3>1. Eligibility</h3><p>Dogs must be at least 12 months old, current on vaccinations and trained on live <em>Cimex lectularius</em> odor. Handlers must be 18 or older.</p>
<h3>2. Test layout</h3><p>Each evaluation uses four to six furnished rooms. Between two and four rooms contain hides of live bed bugs (minimum 5 per vial) or viable eggs. At least one room contains no target odor.</p>
<h3>3. Distractors</h3><p>Rooms include dead bed bugs, cast skins, other common insects, food, and human scent so the team proves it alerts only to live infestations.</p>
<h3>4. Passing score</h3><p>The team must locate at least 95% of hides with no more than one false alert across the full evaluation, within 10 minutes per room.</p>
<h3>5. Blind conditions</h3><p>Neither the handler nor anyone present who can see the handler may know hide locations.</p>
<h3>6. Credential</h3><p>Passing teams receive a credential numbered <code>TSK9-YYYY-NNNN</code>, valid for 12 months. Certification belongs to the team: a new handler or new dog requires a new evaluation.</p>
<h3>7. Revocation</h3><p>The board may suspend a credential for misrepresentation, animal welfare concerns or verified field failures.</p>
</article>
<aside class="side-list"><h3>Documents</h3><ul class="doc-list">
<li><span>Council by-laws</span><span class="muted">PDF &middot; add file</span></li>
<li><span>Full certification rules</span><span class="muted">PDF &middot; add file</span></li>
<li><span>Evaluator code of conduct</span><span class="muted">PDF &middot; add file</span></li>
<li><span>Hide preparation guide</span><span class="muted">PDF &middot; add file</span></li>
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
<label for="ev-type">Evaluation type<select id="ev-type" name="type"><option>New certification</option><option>Annual renewal</option><option>New handler for certified dog</option></select></label></div>
<label for="ev-notes">Training history<textarea id="ev-notes" name="notes" rows="4" placeholder="Trainer, training hours on live bed bug odor, prior certifications"></textarea></label>
<button class="btn" type="submit">Submit application</button>
<p class="form-msg" role="status" hidden>Thanks. Your application was received and we will reply within three business days.</p>
</form>"""

def page_apply(m):
    return f"""<section class="wrap page-head"><p class="eyebrow">Applications &amp; forms</p><h1>Request a team evaluation</h1>
<p class="lede">Complete this form to start certification or renewal. We'll confirm an evaluator and travel estimate by email.</p></section>
<section class="wrap section-tight two-col">
<div>{form_eval(m)}</div>
<aside class="side-list"><h3>Before you apply</h3><ul class="check">
<li>Dog is 12 months or older</li><li>Vaccination records on hand</li><li>Training log for live bed bug odor</li><li>Travel fee paid before test day</li></ul>
<h3>Other forms</h3><ul class="doc-list"><li><span>Evaluator application</span><span class="muted">add file</span></li><li><span>Training facility approval</span><span class="muted">add file</span></li><li><span>Complaint / field report</span><span class="muted">add file</span></li></ul></aside>
</section>"""

def page_certified(m):
    chips = "".join(f'<button type="button" class="chip" data-state="{k}" aria-pressed="{"true" if k=="ALL" else "false"}">{"" if k=="ALL" else f"<i class=dot style=background:var(--{k.lower()})></i>"}{lbl}</button>' for k,lbl in [("ALL","All"),("NY","New York"),("NJ","New Jersey"),("CT","Connecticut")])
    if TEAMS:
        tr = "".join(f'<tr data-state="{s}"><td><code>{c}</code></td><td>{h}</td><td>{d}</td><td>{co}</td><td><span class="st"><i class="dot d-{s.lower()}"></i>{s}</span></td><td class="num">{e}</td></tr>' for c,h,d,co,s,e in TEAMS)
        body = f"""<div class="reg-tools"><label class="search" for="team-search">Search by name, dog or credential<input id="team-search" type="search" placeholder="e.g. TSK9-2027-0001"></label><div class="chips">{chips}</div></div>
<div class="table-scroll"><table id="team-table"><thead><tr><th>Credential</th><th>Handler</th><th>Dog</th><th>Company</th><th>State</th><th>Expires</th></tr></thead><tbody>{tr}</tbody></table></div>
<p class="empty" id="team-empty" hidden>No current team matches that search.</p>"""
    else:
        body = f"""<div class="empty-state"><h3>The first certification cycle is underway</h3>
<p>Teams appear here as soon as they pass a Tri-State K9 field evaluation. If you're a handler in New York, New Jersey or Connecticut, you can book one of the first evaluation slots now.</p>
<a class="btn" href="{L(m,'apply')}">Request an evaluation</a></div>"""
    return f"""<section class="wrap page-head"><p class="eyebrow">Registry</p><h1>Certified teams</h1>
<p class="lede">Every team listed passed a blind field evaluation within the last 12 months. If a team isn't listed, its Tri-State K9 certification is not current.</p></section>
<section class="wrap section-tight">{body}</section>
<section class="wrap section info-pair" id="trainers" style="padding-top:24px">
<div><h3>Approved training facilities</h3><p>Facilities whose curriculum meets Council odor and welfare guidelines. <span class="muted">List coming soon.</span></p></div>
<div><h3>Evaluators</h3><p>Council-trained evaluators who run field tests. Evaluators may not test teams they trained or employ. <span class="muted">List coming soon.</span></p></div>
<div><h3>Odor suppliers</h3><p>Sources of live bed bug colonies and training aids that meet our handling rules. <span class="muted">List coming soon.</span></p></div>
</section>"""

def page_board(m):
    roles = ["President","Vice President","Secretary","Treasurer","Director, Evaluations","Director, Entomology"]
    cards = "".join(f'<li class="person"><span class="avatar" aria-hidden="true">{r[0]}</span><div><strong>[Name]</strong><span class="muted">{r}</span></div></li>' for r in roles)
    return f"""<section class="wrap page-head"><p class="eyebrow">Leadership</p><h1>Board of directors</h1>
<p class="lede">Volunteer directors from pest management, canine training and entomology. Directors are elected by members for two-year terms and must work in New York, New Jersey or Connecticut.</p></section>
<section class="wrap section-tight"><ul class="people">{cards}</ul>
<p class="note">Add each director's name, company and a short bio.</p>
<div class="callout"><h3>Members area</h3><p>Certified teams and evaluators can sign in to download score sheets and meeting minutes. <span class="muted">Connect a members login when you're ready.</span></p></div></section>"""

def page_contact(m):
    attrs = 'name="contact" method="POST" data-netlify="true"' if m == "site" else 'name="contact"'
    return f"""<section class="wrap page-head"><p class="eyebrow">Contact</p><h1>Contact the Council</h1>
<p class="lede">Questions about standards, evaluations or a listed team. For dog training, contact an approved facility directly.</p></section>
<section class="wrap section-tight two-col">
<form class="form" id="contact-form" {attrs}><input type="hidden" name="form-name" value="contact">
<div class="row2"><label for="c-name">Name<input id="c-name" name="name" required></label><label for="c-email">Email<input id="c-email" type="email" name="email" required></label></div>
<label for="c-topic">Topic<select id="c-topic" name="topic"><option>Evaluation question</option><option>Verify a team</option><option>Become an evaluator</option><option>Report a concern</option><option>Other</option></select></label>
<label for="c-msg">Message<textarea id="c-msg" name="message" rows="5" required></textarea></label>
<button class="btn" type="submit">Send message</button>
<p class="form-msg" role="status" hidden>Thanks. Your message was received.</p></form>
<aside class="side-list"><h3>Reach us</h3><p class="sel"><strong>Email</strong><br>{P['email']}</p><p class="sel"><strong>Phone</strong><br>{P['phone']}</p><p class="sel"><strong>Mailing address</strong><br>{P['address']}</p></aside>
</section>"""

BUILDERS = {"home": page_home, "events": page_events, "standards": page_standards, "apply": page_apply,
            "certified": page_certified, "board": page_board, "contact": page_contact}

CSS = (ROOT / "src" / "styles.css").read_text()
JS = (ROOT / "src" / "app.js").read_text()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,500..900&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">'

def build_site():
    out = ROOT / "site"; out.mkdir(exist_ok=True)
    (out / "styles.css").write_text(CSS)
    (out / "app.js").write_text(JS)
    (out / "logo.svg").write_text(logo.standalone())
    (out / "logo-white.svg").write_text(logo.standalone(dark=True))
    (out / "favicon.svg").write_text(logo.standalone_mark())
    for key, fn, label in PAGES:
        title = P["org"] if key == "home" else f"{label} | {P['org']}"
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{P['org']}: independent certification for bed bug detection dog teams.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{FONTS}<link rel="stylesheet" href="styles.css"></head><body>
{nav('site', key)}<main id="main">{BUILDERS[key]('site')}</main>{footer('site')}
<script src="app.js"></script></body></html>"""
        (out / fn).write_text(html)

def build_preview():
    views = "".join(f'<div class="view" data-view="{k}"{"" if k=="home" else " hidden"}>{BUILDERS[k]("preview")}</div>' for k,_,_ in PAGES)
    html = f"""<title>Tri-State Bed Bug K9 Council</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}<style>{CSS}</style>
{nav('preview','home')}<main id="main">{views}</main>{footer('preview')}
<script>{JS}</script>"""
    (ROOT / "preview.html").write_text(html)

build_site(); build_preview()
print("built site/ and preview.html")
