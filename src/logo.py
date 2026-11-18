# Shared logo SVG pieces (imported by build.py, also written out as standalone files)

# 64x64 badge: shield shape, dog head profile, three state stripes (NY / NJ / CT)
# Shepherd-style detection dog profile facing right (upright ears, defined stop, square muzzle)
DOG = "M15 45 C14 37 15 29 19 23 L20 5 C24 8 27 12 28 15 L33 5 C35 9 37 14 37 18 C39 19 41 20 42 21 L52 23.5 C54 24 55 25 55.3 26.5 L55.5 29 C55.5 30.5 54.5 31.3 53 31.3 L50 31.5 C48 33.5 45 35 41 35.5 C38.5 36.5 37 39 37 45 Z"
EYE = "M38.5 22.6 Q40 21.4 41.4 22.6 Q40 23.4 38.5 22.6 Z"
NOSE = "M52.8 24.1 C54.8 24.4 55.7 25.6 55.6 27.8 C54.2 28.3 52.9 28 52.3 27 C51.9 25.9 52 24.7 52.8 24.1 Z"

def mark(ink="currentColor", paper="var(--mark-paper, var(--bg))", c1="var(--ny)", c2="var(--nj)", c3="var(--ct)", cls="mark"):
    return f"""<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true">
<path d="M32 1.5 L60 10.5 V33 C60 49 48 58.5 32 63 C16 58.5 4 49 4 33 V10.5 Z" fill="{ink}"/>
<clipPath id="tsk9-shield"><path d="M32 1.5 L60 10.5 V33 C60 49 48 58.5 32 63 C16 58.5 4 49 4 33 V10.5 Z"/></clipPath><g clip-path="url(#tsk9-shield)"><path d="M0 46 H64" stroke="{c1}" stroke-width="2.8"/><path d="M0 51 H64" stroke="{c2}" stroke-width="2.8"/><path d="M0 56 H64" stroke="{c3}" stroke-width="2.8"/></g>
<g transform="translate(-1.5 3) scale(0.92)"><path d="{DOG}" fill="{paper}"/><path d="{EYE}" fill="{ink}"/><path d="{NOSE}" fill="{ink}"/><path d="M28 15 L26.5 17.5" stroke="{ink}" stroke-width="0.9" stroke-linecap="round" fill="none"/><path d="M50 31.5 L46 31" stroke="{ink}" stroke-width="0.8" stroke-linecap="round" fill="none"/></g>
<g fill="{c1}"><circle cx="53.5" cy="22.5" r="1.3"/><circle cx="54.6" cy="18.9" r="1"/><circle cx="53.4" cy="15.9" r="0.7"/></g>
</svg>"""

def standalone(dark=False):
    ink = "#f2f5f9" if dark else "#0c1b2e"
    paper = "#0c1b2e" if dark else "#ffffff"
    m = mark(ink, paper, "#e8641e", "#0f9384", "#4f5fd6", cls="m").replace('<svg class="m" viewBox="0 0 64 64" aria-hidden="true">', '<g>').replace("</svg>", "</g>")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 72" width="360" height="72">
<g transform="translate(4 4)">{m}</g>
<text x="80" y="34" font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="26" letter-spacing="0.5" fill="{ink}">TRI-STATE</text>
<text x="80" y="58" font-family="Archivo, Arial, sans-serif" font-weight="600" font-size="15" letter-spacing="2.2" fill="{ink}">BED BUG K9 COUNCIL</text>
</svg>"""

def standalone_mark():
    m = mark("#0c1b2e", "#ffffff", "#e8641e", "#0f9384", "#4f5fd6", cls="m").replace('<svg class="m" viewBox="0 0 64 64" aria-hidden="true">', '').replace("</svg>", "")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="512" height="512">{m}</svg>'


def badge(team, dog, handler, valid):
    """Registry badge for a listed team. Fonts fall back to Arial/Helvetica when embedded as an image."""
    m = mark("#0c1b2e", "#ffffff", "#e8641e", "#0f9384", "#4f5fd6", cls="m").replace('<svg class="m" viewBox="0 0 64 64" aria-hidden="true">', '<g>').replace("</svg>", "</g>")
    m = m.replace('id="tsk9-shield"', 'id="b-shield"').replace("url(#tsk9-shield)", "url(#b-shield)")
    F = "Archivo, 'Helvetica Neue', Arial, sans-serif"
    M = "'IBM Plex Mono', Menlo, Consolas, monospace"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 180" width="560" height="180" role="img" aria-label="Certified bed bug K9 team {team}, listed in the Tri-State Bed Bug K9 Council registry, valid through {valid}">
<rect x="1.5" y="1.5" width="557" height="177" rx="16" fill="#ffffff" stroke="#0c1b2e" stroke-width="3"/>
<rect x="9" y="9" width="542" height="162" rx="10" fill="none" stroke="#0c1b2e" stroke-opacity=".16" stroke-width="1"/>
<circle cx="92" cy="90" r="64" fill="#0c1b2e"/>
<circle cx="92" cy="90" r="57" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width="1"/>
<g transform="translate(58 55) scale(1.06)">{m.replace('fill="#0c1b2e"/>', 'fill="#ffffff"/>', 1).replace('fill="#ffffff"/><path d="M38.5', 'fill="#0c1b2e"/><path d="M38.5', 1)}</g>
<text x="182" y="42" font-family="{M}" font-size="12" font-weight="600" letter-spacing="2.4" fill="#3a4a5e">TRI-STATE K9 REGISTRY</text>
<text x="180" y="80" font-family="{F}" font-size="36" font-weight="800" letter-spacing="0.3" fill="#0c1b2e">CERTIFIED TEAM</text>
<text x="182" y="104" font-family="{F}" font-size="15" font-weight="600" fill="#3a4a5e">Bed bug scent detection K9</text>
<text x="182" y="124" font-family="{F}" font-size="15" font-weight="700" fill="#0c1b2e">{handler} &amp; {dog}</text>
<rect x="182" y="136" width="116" height="4" fill="#e8641e"/><rect x="298" y="136" width="116" height="4" fill="#0f9384"/><rect x="414" y="136" width="116" height="4" fill="#4f5fd6"/>
<text x="182" y="160" font-family="{M}" font-size="13" font-weight="600" fill="#0c1b2e">{team}</text>
<text x="530" y="160" text-anchor="end" font-family="{M}" font-size="12" fill="#3a4a5e">Valid thru {valid}</text>
</svg>"""
