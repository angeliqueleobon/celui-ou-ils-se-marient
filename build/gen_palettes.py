# -*- coding: utf-8 -*-
import io, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def read_shell(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


OUT = os.path.join(ROOT, "palettes.html")

TRIM_W, TRIM_H, BLEED = 1480, 1050, 30
W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
MM_W, MM_H = W / 10.0, H / 10.0
X = 140

NAMES = [('formal', 'ARNAUD', 'EMILY'), ('nick', 'CHAPS', 'EMY'), ('handle', 'ELMTREE', 'LACHAP')]

# ---------------------------------------------------------------- flower geometries

def daisy_round(cx, cy, r, petal_fill, core_fill, n=6):
    """the shape used so far: round petals, round core"""
    ring, petal, core = r, r * 0.62, r * 0.79
    out = ['<g fill="%s">' % petal_fill]
    for i in range(n):
        a = math.radians(-90 + i * (360.0 / n))
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx + ring * math.cos(a), cy + ring * math.sin(a), petal))
    out.append('</g><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, core, core_fill))
    return ''.join(out)

def daisy_pointed(cx, cy, r, petal_fill, core_fill, n=8):
    """pointed petals: a sharper silhouette, closer to a marguerite"""
    out = ['<g fill="%s">' % petal_fill]
    for i in range(n):
        a = -90 + i * (360.0 / n)
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.2f %.1f %.1f)"/>'
                   % (cx, cy - r * 0.66, r * 0.24, r * 0.68, a, cx, cy))
    out.append('</g><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.32, core_fill))
    return ''.join(out)

def poppy(cx, cy, r, petal_fill, core_fill, lobes=7):
    """one closed scalloped shape rather than separate petals"""
    r_in, r_ctrl = r * 0.74, r * 1.42
    pts = []
    for i in range(lobes):
        a_in = 2 * math.pi * i / lobes - math.pi / 2
        pts.append((cx + r_in * math.cos(a_in), cy + r_in * math.sin(a_in)))
    d = ['M %.1f %.1f' % pts[0]]
    for i in range(lobes):
        a_ctrl = 2 * math.pi * (i + 0.5) / lobes - math.pi / 2
        ctrl = (cx + r_ctrl * math.cos(a_ctrl), cy + r_ctrl * math.sin(a_ctrl))
        nxt = pts[(i + 1) % lobes]
        d.append('Q %.1f %.1f %.1f %.1f' % (ctrl[0], ctrl[1], nxt[0], nxt[1]))
    d.append('Z')
    return ('<path d="%s" fill="%s"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
            % (' '.join(d), petal_fill, cx, cy, r * 0.3, core_fill))

def rings(cx, cy, r, petal_fill, core_fill):
    """the flower abstracted to concentric rings"""
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>'
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
            % (cx, cy, r, petal_fill,
               cx, cy, r * 0.72, core_fill, r * 0.2,
               cx, cy, r * 0.34, core_fill))

def _bez(p0, p1, p2, p3, t):
    mt = 1 - t
    return (mt**3 * p0[0] + 3*mt*mt*t * p1[0] + 3*mt*t*t * p2[0] + t**3 * p3[0],
            mt**3 * p0[1] + 3*mt*mt*t * p1[1] + 3*mt*t*t * p2[1] + t**3 * p3[1])

def _bez_tangent(p0, p1, p2, p3, t):
    mt = 1 - t
    return (3*mt*mt * (p1[0]-p0[0]) + 6*mt*t * (p2[0]-p1[0]) + 3*t*t * (p3[0]-p2[0]),
            3*mt*mt * (p1[1]-p0[1]) + 6*mt*t * (p2[1]-p1[1]) + 3*t*t * (p3[1]-p2[1]))


def dahlia(cx, cy, r, petal_fill, core_fill):
    """concentric rings of pointed petals, each ring offset from the last:
    that layering is what reads as a dahlia rather than a daisy"""
    rings = [
        (14, 0.74, 0.40, 0.15, petal_fill),
        (12, 0.52, 0.31, 0.12, core_fill),
        (10, 0.33, 0.22, 0.095, petal_fill),
        (8,  0.18, 0.14, 0.070, core_fill),
    ]
    out = []
    for idx, (n, ring, plen, pwid, fill) in enumerate(rings):
        out.append('<g fill="%s">' % fill)
        offset = (180.0 / n) if idx % 2 else 0.0
        for i in range(n):
            a = -90 + offset + i * (360.0 / n)
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.2f %.1f %.1f)"/>'
                       % (cx, cy - r * ring, r * pwid, r * plen, a, cx, cy))
        out.append('</g>')
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.105, petal_fill))
    return ''.join(out)


def pivoine(cx, cy, r, petal_fill, core_fill):
    """dense rounded petals in overlapping rings and no visible centre:
    a peony is a pompom, not a star"""
    rings = [
        (11, 0.70, 0.30, 0.24, petal_fill),
        (9,  0.50, 0.26, 0.21, core_fill),
        (7,  0.33, 0.22, 0.18, petal_fill),
        (5,  0.17, 0.18, 0.15, core_fill),
    ]
    out = []
    for idx, (n, ring, rx, ry, fill) in enumerate(rings):
        out.append('<g fill="%s">' % fill)
        offset = (180.0 / n) if idx % 2 else 0.0
        for i in range(n):
            a = -90 + offset + i * (360.0 / n)
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.2f %.1f %.1f)"/>'
                       % (cx, cy - r * ring, r * rx, r * ry, a, cx, cy))
        out.append('</g>')
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.12, petal_fill))
    return ''.join(out)

def _forget_me_not(cx, cy, size, petal_fill, core_fill):
    out = ['<g fill="%s">' % petal_fill]
    for i in range(5):
        a = math.radians(-90 + i * 72)
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>'
                   % (cx + size * 0.60 * math.cos(a), cy + size * 0.60 * math.sin(a), size * 0.44))
    out.append('</g><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, size * 0.30, core_fill))
    return ''.join(out)

def myosotis(cx, cy, r, petal_fill, core_fill):
    """a forget-me-not is never alone: a cluster of small five-petal flowers,
    which gives a scattered texture instead of one big bloom"""
    spots = [(0.0, 0.0, 0.30)]
    for i in range(5):
        a = math.radians(-90 + i * 72 + 18)
        spots.append((0.56 * math.cos(a), 0.56 * math.sin(a), 0.25))
    for i in range(4):
        a = math.radians(-90 + i * 90 + 45)
        spots.append((0.98 * math.cos(a), 0.98 * math.sin(a), 0.19))
    return ''.join(_forget_me_not(cx + dx * r, cy + dy * r, sz * r, petal_fill, core_fill)
                   for dx, dy, sz in spots)


def bouquet(cx, cy, r, peony_a, peony_b, blue, yellow):
    """how a real bouquet is built: one focal flower, small ones filling around it"""
    out = [pivoine(cx, cy, r * 0.70, peony_a, peony_b)]
    spots = [(-0.86, 0.42, 0.17), (-0.60, 0.80, 0.13), (0.56, -0.82, 0.15),
             (0.90, -0.42, 0.12), (0.84, 0.64, 0.16), (0.50, 0.94, 0.12),
             (-0.32, -0.94, 0.14), (0.04, -1.04, 0.11)]
    for dx, dy, sz in spots:
        out.append(_forget_me_not(cx + dx * r, cy + dy * r, sz * r, blue, yellow))
    return ''.join(out)

def sprig(p0, p1, p2, p3, leaf_len, leaf_fill, stem_fill, leaves=9, t0=0.06, t1=0.94, splay=52):
    """a stem plus leaves anchored ON the stem: each leaf sits at a point of the
    curve and is rotated relative to the tangent there, so nothing floats"""
    out = ['<path d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
           'stroke-width="%.1f" stroke-linecap="round"/>'
           % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], stem_fill, leaf_len * 0.10)]
    out.append('<g fill="%s">' % leaf_fill)
    for i in range(leaves):
        t = t0 + (t1 - t0) * (i / float(leaves - 1))
        cx, cy = _bez(p0, p1, p2, p3, t)
        dx, dy = _bez_tangent(p0, p1, p2, p3, t)
        theta = math.degrees(math.atan2(dy, dx))
        side = -1 if i % 2 else 1
        ang = theta + side * splay
        rx = leaf_len * (0.72 + 0.28 * math.sin(math.pi * t))   # shorter at both ends
        ry = rx * 0.42
        lx = cx + rx * math.cos(math.radians(ang))
        ly = cy + rx * math.sin(math.radians(ang))
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.2f %.1f %.1f)"/>'
                   % (lx, ly, rx, ry, ang, lx, ly))
    # a single leaf closing the tip, along the stem
    tipx, tipy = _bez(p0, p1, p2, p3, 1.0)
    tdx, tdy = _bez_tangent(p0, p1, p2, p3, 1.0)
    tang = math.degrees(math.atan2(tdy, tdx))
    tl = leaf_len * 0.78
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.2f %.1f %.1f)"/>'
               % (tipx + tl * math.cos(math.radians(tang)), tipy + tl * math.sin(math.radians(tang)),
                  tl, tl * 0.40, tang,
                  tipx + tl * math.cos(math.radians(tang)), tipy + tl * math.sin(math.radians(tang))))
    out.append('</g>')
    return ''.join(out)

# ---------------------------------------------------------------- palettes

PALETTES = [
    dict(key='pivoine', name='Pivoine',
         why="La fleur pr\u00e9f\u00e9r\u00e9e d'Emy. Une pivoine est un pompon : des p\u00e9tales arrondis en couronnes qui se chevauchent, sans c\u0153ur visible. C'est la plus g\u00e9n\u00e9reuse des fleurs propos\u00e9es, et la seule qui remplit vraiment son cercle. Rose ancien et corail sur cr\u00e8me.",
         ground='#F6F0EA', ink='#2C2126', label='#9C3A52', title='#C75A72', amp='#E39AA5',
         petal='#C75A72', core='#E39AA5', shape='pivoine', deep='#7A2438'),
    dict(key='myosotis', name='Myosotis',
         why="L'autre fleur d'Emy, et celle qui change le plus la carte : un myosotis n'est jamais seul, donc au lieu d'une grande fleur on obtient une gerbe de petites, avec leur \u0153il jaune. La texture est mouchet\u00e9e plut\u00f4t que massive, et le bleu p\u00e2le est la couleur la plus douce des sept.",
         ground='#F4F3ED', ink='#1F2A33', label='#2C5E86', title='#3D7FA8', amp='#D9A92F',
         petal='#5C97C4', core='#F0C93F', shape='myosotis', deep='#234C6B'),
    dict(key='melange', name='Pivoine et myosotis',
         why="Les deux fleurs d'Emy dans la m\u00eame carte, mont\u00e9es comme un vrai bouquet : une pivoine en fleur principale, des myosotis qui remplissent autour. C'est la seule proposition o\u00f9 le rose et le bleu cohabitent, et l'esperluette passe en bleu au milieu des capitales roses.",
         ground='#F5F2EC', ink='#262A31', label='#7C3A50', title='#C0687E', amp='#5C97C4',
         petal='#C0687E', core='#E3A3AE', blue='#5C97C4', yellow='#F0C93F',
         shape='melange', deep='#2F4466'),
    dict(key='dahlia', name='Dahlia framboise',
         why="Une vraie fleur de mariage, et une g\u00e9om\u00e9trie qui se dessine bien \u00e0 plat : quatre couronnes de p\u00e9tales pointus qui se r\u00e9duisent vers le centre, chaque couronne d\u00e9cal\u00e9e par rapport \u00e0 la pr\u00e9c\u00e9dente. C'est ce feuillet\u00e9 qui la distingue d'une marguerite. Framboise et corail, sur cr\u00e8me.",
         ground='#F5F0E8', ink='#2B2226', label='#8A2C46', title='#B33A5B', amp='#E27A62',
         petal='#B33A5B', core='#E27A62', shape='dahlia', deep='#7A1F38'),    dict(key='terre', name='Terre cuite',
         why="Une famille chaude et resserrée : terre cuite, rose ancien, brique. C'est la plus douce des quatre et la plus facile à imprimer, les tons chauds ne bougent pas au tirage. Les pétales deviennent pointus, ce qui donne une marguerite plutôt qu'une fleur ronde.",
         ground='#F3EEE7', ink='#2A211C', label='#8E3B2E', title='#C15A3C', amp='#C15A3C',
         petal='#C15A3C', core='#D98E86', shape='pointed', deep='#7E2C21'),
    dict(key='cobalt', name='Cobalt et rose',
         why="Le bleu franc avec un rose et un jaune chaud : c'est le contraste le plus net des quatre, et le plus proche des graphismes de télévision des années 90. La fleur devient une seule forme festonnée, sans pétales séparés.",
         ground='#F2F0EA', ink='#1B2140', label='#23499B', title='#23499B', amp='#E9808F',
         petal='#23499B', core='#F0B54A', shape='poppy', deep='#1B3878'),
    dict(key='aubergine', name='Aubergine et jaune acide',
         why="Fond sombre, jaune acide et lilas : la plus graphique et la plus affirmée. La fleur est réduite à des cercles concentriques, donc presque un logo. À réserver si le couple assume quelque chose de franchement dessiné.",
         ground='#2E1B33', ink='#F4EFE4', label='#E4E04A', title='#B98FD1', amp='#E4E04A',
         petal='#B98FD1', core='#E4E04A', shape='rings', deep='#2A1730'),
    dict(key='ciel', name='Ciel et orange',
         why="Le couple bleu et orange, complémentaires, sur un fond bleu clair. Et surtout : du feuillage au lieu de fleurs. Plus botanique, plus calme, et ça évite complètement la fleur stylisée qu'on voit partout.",
         ground='#CDE4EF', ink='#16242C', label='#96380F', title='#B0481A', amp='#B0481A',
         petal='#3E7145', core='#2E5A34', shape='sprig', deep='#24512C'),
]

SHAPES = {'round': daisy_round, 'pointed': daisy_pointed, 'poppy': poppy, 'rings': rings,
          'sprig': sprig, 'dahlia': dahlia, 'pivoine': pivoine, 'myosotis': myosotis}

def style_for(p):
    """every selector is scoped to this card's id: a <style> inside inline SVG
    applies to the whole document, so unscoped rules from one card would
    override the other cards' palettes"""
    d = dict(p)
    d['sel'] = '#' + p['key']
    return """
    %(sel)s text { font-family: Futura, "Futura PT", "Century Gothic", "Avenir Next", "Trebuchet MS", sans-serif; }
    %(sel)s .prod  { font-size: 17px; letter-spacing: 6.6px; font-weight: 500; fill: %(label)s; }
    %(sel)s .nm    { font-weight: 700; letter-spacing: 11px; fill: %(ink)s; }
    %(sel)s .title { font-size: 30px; letter-spacing: 11px; font-weight: 500; fill: %(title)s; }
    %(sel)s .soon  { font-size: 21px; letter-spacing: 8.6px; font-weight: 500; fill: %(label)s; }
    %(sel)s .date  { font-size: 49px; letter-spacing: 5.4px; font-weight: 700; font-variant-numeric: tabular-nums; fill: %(ink)s; }
    %(sel)s .place { font-size: 20px; letter-spacing: 5.8px; font-weight: 500; fill: %(label)s; }
    %(sel)s .fine  { font-size: 16px; letter-spacing: 3.4px; opacity: .58; fill: %(ink)s; }

    %(sel)s[data-l="fr"] .en, %(sel)s[data-l="en"] .fr { display: none; }
    %(sel)s[data-n="nick"]   [data-n]:not([data-n~="nick"]),
    %(sel)s[data-n="formal"] [data-n]:not([data-n~="formal"]),
    %(sel)s[data-n="handle"] [data-n]:not([data-n~="handle"]) { display: none; }
""" % d

def credits(x, y1, y2, fill=None, anchor='start'):
    """two end-credit lines. The naming card rides with the cast credits, where
    names belong, so the last line can carry the same punchline in every
    register instead of being truncated to fit."""
    f = (' fill="%s"' % fill) if fill else ''
    rows1 = [
        ('formal', "AVEC ANNABEL ET ELLIOT &#8226; CASTING R&#201;UNI PAR ICONOSQUARE",
                   "WITH ANNABEL AND ELLIOT &#8226; CASTING BY ICONOSQUARE"),
        ('nick handle',
         "AVEC ANNABEL ET ELLIOT &#8226; CASTING R&#201;UNI PAR ICONOSQUARE &#8226; CERTAINS NOMS ONT &#201;T&#201; CHANG&#201;S",
         "WITH ANNABEL AND ELLIOT &#8226; CASTING BY ICONOSQUARE &#8226; SOME NAMES HAVE BEEN CHANGED"),
    ]
    out = []
    for scope, fr, en in rows1:
        out.append('<text class="fine fr" data-n="%s" x="%s" y="%s"%s text-anchor="%s">%s</text>'
                   % (scope, x, y1, f, anchor, fr))
        out.append('<text class="fine en" data-n="%s" x="%s" y="%s"%s text-anchor="%s">%s</text>'
                   % (scope, x, y1, f, anchor, en))
    out.append('<text class="fine fr" x="%s" y="%s"%s text-anchor="%s">'
               'D&#8217;APR&#200;S DES FAITS R&#201;ELS &#8226; AUCUN INVIT&#201; NE SERA MALTRAIT&#201;</text>'
               % (x, y2, f, anchor))
    out.append('<text class="fine en" x="%s" y="%s"%s text-anchor="%s">'
               'BASED ON REAL EVENTS &#8226; NO GUEST WILL BE HARMED</text>'
               % (x, y2, f, anchor))
    return ''.join(out)

def T(x, y, cls, fr, en, anchor='start'):
    return ('<text class="%s fr" x="%s" y="%s" text-anchor="%s">%s</text>'
            '<text class="%s en" x="%s" y="%s" text-anchor="%s">%s</text>'
            % (cls, x, y, anchor, fr, cls, x, y, anchor, en))

def build(p):
    shape = SHAPES.get(p['shape'])
    out = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, p['ground'])]
    if p['shape'] == 'melange':
        out.append(bouquet(1462, 556, 300, p['petal'], p['core'], p['blue'], p['yellow']))
    elif p['shape'] == 'sprig':
        out.append(sprig((1548, 1140), (1616, 780), (1372, 430), (1436, 96),
                         112, p['petal'], p['core']))
    else:
        out.append(shape(1462, 556, 300, p['petal'], p['core']))
    out.append(T(X, 268, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES'))
    for key, first, second in NAMES:
        out.append('<text class="nm" data-n="%s" style="font-size:96px" x="%d" y="430">%s</text>' % (key, X, first))
        out.append('<text class="nm" data-n="%s" style="font-size:96px" x="%d" y="540">'
                   '<tspan fill="%s">&amp; </tspan>%s</text>' % (key, X, p['amp'], second))
    out.append(T(X, 632, 'title', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING'))
    out.append('<line x1="%d" y1="700" x2="960" y2="700" stroke="%s" stroke-opacity=".3" stroke-width="1.6"/>' % (X, p['ink']))
    out.append(T(X, 760, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON'))
    out.append(T(X, 842, 'date', 'VENDREDI 7 MAI 2027', 'FRIDAY 7 MAY 2027'))
    out.append(T(X, 894, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE'))
    out.append(credits(X, 962, 1000))
    return ('<svg id="%s" class="card" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'data-l="fr" data-n="formal" role="img" aria-label="Save the date, palette %s, A6 paysage">'
            '<style>%s</style>%s</svg>' % (p['key'], W, H, p['name'], style_for(p), ''.join(out)))


CREAM_V = '#F4F0E6'

def verso_style(p):
    d = dict(p)
    d['sel'] = '#' + p['key'] + 'v'
    d['cream'] = CREAM_V
    return """
    %(sel)s text { font-family: Futura, "Futura PT", "Century Gothic", "Avenir Next", "Trebuchet MS", sans-serif; }
    %(sel)s .vt { font-size: 26px; letter-spacing: 9px; font-weight: 500; fill: %(cream)s; }
    %(sel)s .vs { font-size: 17px; letter-spacing: 6.6px; font-weight: 500; fill: %(cream)s; fill-opacity: .82; }
    %(sel)s[data-l="fr"] .en, %(sel)s[data-l="en"] .fr { display: none; }
""" % d

def verso_ground(p):
    """a deep tone of the palette: the back belongs to the same world and cream
    text keeps a comfortable contrast on it"""
    return p['deep']

def build_verso(p):
    shape = SHAPES.get(p['shape'])
    g = verso_ground(p)
    out = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, g)]
    if p['shape'] == 'melange':
        out.append(bouquet(140, 140, 175, CREAM_V, p['core'], CREAM_V, p['yellow']))
        out.append(bouquet(1430, 985, 205, p['core'], CREAM_V, p['yellow'], CREAM_V))
    elif p['shape'] == 'sprig':
        out.append(sprig((-40, 1160), (140, 820), (-90, 430), (90, 70), 104, CREAM_V, p['core']))
        out.append(sprig((1600, -40), (1420, 300), (1650, 700), (1470, 1040), 92, p['core'], CREAM_V))
    else:
        out.append(shape(120, 130, 170, CREAM_V, p['core']))
        out.append(shape(1440, 980, 200, p['core'], CREAM_V))
        out.append(shape(1230, 210, 92, p['core'], CREAM_V))
    out.append('<text class="vt fr" x="%d" y="496" text-anchor="middle">L&#8217;INVITATION SUIVRA</text>' % (W / 2))
    out.append('<text class="vt en" x="%d" y="496" text-anchor="middle">THE INVITATION WILL FOLLOW</text>' % (W / 2))
    out.append('<text class="vs fr" x="%d" y="562" text-anchor="middle">CONSERVEZ CETTE CARTE JUSQU&#8217;&#192; LA FIN DE LA S&#201;ANCE.</text>' % (W / 2))
    out.append('<text class="vs en" x="%d" y="562" text-anchor="middle">RETAIN THIS CARD UNTIL THE END OF THE SCREENING.</text>' % (W / 2))
    out.append('<text class="vs fr" x="%d" y="602" text-anchor="middle">AUCUN DUPLICATA NE SERA D&#201;LIVR&#201;.</text>' % (W / 2))
    out.append('<text class="vs en" x="%d" y="602" text-anchor="middle">NO DUPLICATE WILL BE ISSUED.</text>' % (W / 2))
    return ('<svg id="%sv" class="card" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'data-l="fr" data-n="formal" role="img" aria-label="Verso de la carte, palette %s">'
            '<style>%s</style>%s</svg>' % (p['key'], W, H, p['name'], verso_style(p), ''.join(out)))

def write_page():
    blocks, grounds = [], {}
    for i, p in enumerate(PALETTES, start=1):
        grounds[p['key']] = p['ground']
        swatches = ''.join('<li style="background:%s"></li>' % c
                           for c in [p['ground'], p['petal'], p['core'], p['title'], p['label']])
        blocks.append('''  <section class="piece">
        <div class="piece-head">
          <p class="piece-tag">Palette %d</p>
          <h2>%s</h2>
          <p class="piece-why">%s</p>
          <ul class="swatches">%s</ul>
        </div>
        <div class="stage">%s</div>
        <div class="actions">
          <button class="btn" type="button" data-png="%s">Télécharger &bull; FR + EN</button>
          <button class="btn ghost" type="button" data-svg="%s">Version imprimeur</button>
        </div>
      </section>''' % (i, p['name'], p['why'], swatches, build(p), p['key'], p['key']))

    shell = read_shell("palettes_shell.html")
    page = (shell.replace('{{BLOCKS}}', '\n\n'.join(blocks))
                 .replace('{{W}}', str(W)).replace('{{H}}', str(H))
                 .replace('{{MMW}}', '%.1f' % MM_W).replace('{{MMH}}', '%.1f' % MM_H)
                 .replace('{{GROUNDS}}', repr(grounds).replace("'", '"')))
    io.open(OUT, "w", encoding="utf-8").write(page)
    print("wrote", OUT, len(page), "bytes")


if __name__ == "__main__":
    write_page()
