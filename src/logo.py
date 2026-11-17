# Shared logo SVG pieces (imported by build.py, also written out as standalone files)

# 64x64 badge: shield shape, dog head profile, three state stripes (NY / NJ / CT)
DOG = "M16 56 L18 30 L20 22 L24 6 L32 20 L38 22 L42 26 L54 30 Q58 32 57 35 L56 37 L48 39 L40 43 L34 50 L32 56 Z"

def mark(ink="currentColor", paper="var(--bg)", c1="var(--ny)", c2="var(--nj)", c3="var(--ct)", cls="mark"):
    return f"""<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true">
<path d="M32 2 L58 11 V32 C58 47 46 57 32 62 C18 57 6 47 6 32 V11 Z" fill="{ink}"/>
<g clip-path="none"><path d="M11 47 H53" stroke="{c1}" stroke-width="3"/><path d="M14 52 H50" stroke="{c2}" stroke-width="3"/><path d="M19 57 H45" stroke="{c3}" stroke-width="3"/></g>
<g transform="translate(8 5) scale(0.74)"><path d="{DOG}" fill="{paper}"/><circle cx="36" cy="27" r="2.2" fill="{ink}"/><circle cx="55.5" cy="32.5" r="2.4" fill="{ink}"/></g>
<g fill="{c1}"><circle cx="53" cy="25" r="1.5"/><circle cx="56" cy="21" r="1.1"/><circle cx="53.5" cy="17.5" r="0.8"/></g>
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
