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
