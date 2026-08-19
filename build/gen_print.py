# -*- coding: utf-8 -*-
import io, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_palettes as gp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def read_shell(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


OUT = os.path.join(ROOT, "imprimeur.html")

# A6 landscape, 148 x 105 mm trim, 3 mm bleed all round, at 10 units per mm
TRIM_W, TRIM_H, BLEED = 1480, 1050, 30
W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED   # 1540 x 1110
SAFE = 80                                        # 5 mm inside the trim
MM_W, MM_H = W / 10.0, H / 10.0

GREEN, CREAM, TOMATO, MUSTARD, INK = '#14524E', '#F4F0E6', '#E4472F', '#E9B23C', '#17201F'

NAMES = [
    ('formal', 'ARNAUD',  'EMILY'),
    ('nick',   'CHAPS',   'EMY'),
    ('handle', 'ELMTREE', 'LACHAP'),
]

def bloom(cx, cy, ring, petal, core, petal_fill, core_fill, n=6, start=-90):
    out = ['<g fill="%s">' % petal_fill]
    for i in range(n):
        a = math.radians(start + i * (360.0 / n))
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx + ring * math.cos(a), cy + ring * math.sin(a), petal))
    out.append('</g><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, core, core_fill))
    return ''.join(out)

COPYRIGHT = 'IX.IV.MMXIX'

def _mark():
    return (' &#8226; &#169; ' + COPYRIGHT) if COPYRIGHT else ''

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
               'D&#8217;APR&#200;S DES FAITS R&#201;ELS &#8226; AUCUN INVIT&#201; NE SERA MALTRAIT&#201;%s</text>'
               % (x, y2, f, anchor, _mark()))
    out.append('<text class="fine en" x="%s" y="%s"%s text-anchor="%s">'
               'BASED ON REAL EVENTS &#8226; NO GUEST WILL BE HARMED%s</text>'
               % (x, y2, f, anchor, _mark()))
    return ''.join(out)

def T(x, y, cls, fr, en, fill, anchor='start'):
    return ('<text class="%s fr" x="%s" y="%s" fill="%s" text-anchor="%s">%s</text>'
            '<text class="%s en" x="%s" y="%s" fill="%s" text-anchor="%s">%s</text>'
            % (cls, x, y, fill, anchor, fr, cls, x, y, fill, anchor, en))

def name_lines(x, y1, y2, size, fill=INK, amp=TOMATO):
    out = []
    for key, first, second in NAMES:
        out.append('<text class="nm" data-n="%s" style="font-size:%dpx" x="%s" y="%s" fill="%s">%s</text>'
                   % (key, size, x, y1, fill, first))
        out.append('<text class="nm" data-n="%s" style="font-size:%dpx" x="%s" y="%s" fill="%s">'
                   '<tspan fill="%s">&amp; </tspan>%s</text>' % (key, size, x, y2, fill, amp, second))
    return ''.join(out)

STYLE = """
    text { font-family: Futura, "Futura PT", "Century Gothic", "Avenir Next", "Trebuchet MS", sans-serif; }
    .prod  { font-size: 17px; letter-spacing: 6.6px; font-weight: 500; }
    .nm    { font-weight: 700; letter-spacing: 11px; }
    .title { font-size: 30px; letter-spacing: 11px; font-weight: 500; }
    .soon  { font-size: 21px; letter-spacing: 8.6px; font-weight: 500; }
    .date  { font-size: 49px; letter-spacing: 5.4px; font-weight: 700; font-variant-numeric: tabular-nums; }
    .huge-date { font-size: 112px; letter-spacing: 6px; font-weight: 700; font-variant-numeric: tabular-nums; }
    .title-s { font-size: 26px; letter-spacing: 9px; font-weight: 500; }
    .place { font-size: 20px; letter-spacing: 5.8px; font-weight: 500; }
    .fine  { font-size: 16px; letter-spacing: 3.4px; opacity: .55; }
    .verso { font-size: 26px; letter-spacing: 9px; font-weight: 500; }

    svg[data-l="fr"] .en, svg[data-l="en"] .fr { display: none; }
    svg[data-n="nick"]   [data-n]:not([data-n~="nick"]),
    svg[data-n="formal"] [data-n]:not([data-n~="formal"]),
    svg[data-n="handle"] [data-n]:not([data-n~="handle"]) { display: none; }
"""

GUIDES = ('<g class="guide">'
          '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-opacity=".5" '
          'stroke-width="2" stroke-dasharray="14 10"/>'
          '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-opacity=".28" '
          'stroke-width="2" stroke-dasharray="5 9"/>'
          '</g>') % (BLEED, BLEED, TRIM_W, TRIM_H, TOMATO,
                     BLEED + SAFE - 30, BLEED + SAFE - 30, TRIM_W - 2 * (SAFE - 30), TRIM_H - 2 * (SAFE - 30), GREEN)

X = 140          # 14 mm from the bleed edge, 11 mm from the trim
recto = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, CREAM)]
recto.append(bloom(1462, 556, 292, 180, 232, TOMATO, MUSTARD))
recto.append(T(X, 268, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES', GREEN))
recto.append(name_lines(X, 430, 540, 96))
recto.append(T(X, 632, 'title', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING', TOMATO))
recto.append('<line x1="%d" y1="700" x2="960" y2="700" stroke="%s" stroke-opacity=".28" stroke-width="1.6"/>' % (X, INK))
recto.append(T(X, 760, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON', GREEN))
recto.append(T(X, 842, 'date', 'VENDREDI 7 MAI 2027', 'FRIDAY 7 MAY 2027', INK))
recto.append(T(X, 894, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE',
               'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', GREEN))
recto.append(credits(X, 938, 972, INK))

verso = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
verso.append(bloom(150, 150, 176, 109, 140, MUSTARD, TOMATO))
verso.append(bloom(1420, 980, 208, 129, 166, TOMATO, MUSTARD))
verso.append(bloom(1180, 210, 96, 60, 77, TOMATO, MUSTARD))
verso.append(T(W / 2, 533, 'verso', 'L&#8217;INVITATION SUIVRA', 'INVITATION TO FOLLOW', CREAM, anchor='middle'))
verso.append(T(W / 2, 599, 'prod', 'CONSERVEZ CETTE CARTE. ELLE NE SERT &#192; RIEN. CONSERVEZ-LA QUAND M&#202;ME.',
               'RETAIN THIS CARD. IT SERVES NO PURPOSE. RETENTION REMAINS COMPULSORY.', MUSTARD, anchor='middle'))


def text_block(fill_ink, fill_green, fill_tomato, amp):
    """the validated A6 text block, reused by the three grounds"""
    out = []
    out.append(T(X, 268, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES', fill_green))
    out.append(name_lines(X, 430, 540, 96, fill=fill_ink, amp=amp))
    out.append(T(X, 632, 'title', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING', fill_tomato))
    out.append('<line x1="%d" y1="700" x2="960" y2="700" stroke="%s" stroke-opacity=".3" stroke-width="1.6"/>' % (X, fill_ink))
    out.append(T(X, 760, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON', fill_green))
    out.append(T(X, 842, 'date', 'VENDREDI 7 MAI 2027', 'FRIDAY 7 MAY 2027', fill_ink))
    out.append(T(X, 894, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE',
                 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', fill_green))
    out.append(credits(X, 938, 972, fill_ink))
    return ''.join(out)

# --- equilibree : light ground kept, one saturated block, three blooms ---
equi = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, CREAM)]
equi.append('<rect x="1000" y="0" width="%d" height="%d" fill="%s"/>' % (W - 1000, H, GREEN))
equi.append(bloom(36, 26, 76, 47, 60, TOMATO, MUSTARD))
equi.append(bloom(1400, 880, 150, 93, 119, MUSTARD, TOMATO))
equi.append(bloom(1075, 300, 205, 127, 163, TOMATO, MUSTARD))
equi.append(text_block(INK, GREEN, TOMATO, TOMATO))

# --- saturee : full green ground, a cluster of overlapping blooms ---
satu = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
satu.append(bloom(26, 16, 78, 48, 62, MUSTARD, TOMATO))
satu.append(bloom(1200, 150, 88, 55, 70, MUSTARD, TOMATO))
satu.append(bloom(1520, 160, 128, 79, 101, MUSTARD, TOMATO))
satu.append(bloom(1130, 860, 118, 73, 94, TOMATO, MUSTARD))
satu.append(bloom(1490, 780, 158, 98, 125, MUSTARD, GREEN))
satu.append(bloom(1340, 380, 208, 129, 165, TOMATO, MUSTARD))
satu.append(text_block(CREAM, MUSTARD, MUSTARD, TOMATO))



def names_around(cx, y, size, gap, fill=INK, ls=11):
    out = []
    for key, first, second in NAMES:
        out.append('<text class="nm" data-n="%s" style="font-size:%dpx" x="%s" y="%s" fill="%s" text-anchor="end">%s</text>'
                   % (key, size, cx - gap + ls, y, fill, first))
        out.append('<text class="nm" data-n="%s" style="font-size:%dpx" x="%s" y="%s" fill="%s" text-anchor="start">%s</text>'
                   % (key, size, cx + gap, y, fill, second))
    return ''.join(out)

def names_inline(x, y, size, fill=INK, amp=TOMATO):
    out = []
    for key, first, second in NAMES:
        out.append('<text class="nm" data-n="%s" style="font-size:%dpx" x="%s" y="%s" fill="%s">'
                   '%s<tspan fill="%s"> &amp; </tspan>%s</text>' % (key, size, x, y, fill, first, amp, second))
    return ''.join(out)

CX = W / 2

# --- A : la fleur remplace le & ---
fleur = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, CREAM)]
fleur.append(bloom(30, 1070, 110, 68, 87, MUSTARD, TOMATO))
fleur.append(bloom(1510, 1060, 120, 74, 95, TOMATO, MUSTARD))
fleur.append(T(CX, 250, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES', GREEN, anchor='middle'))
fleur.append(names_around(CX, 450, 84, 100))
# smaller bloom, and its lowest petal now clears the title by 4 mm
fleur.append(bloom(CX, 420, 46, 29, 37, TOMATO, MUSTARD))
fleur.append(T(CX, 596, 'title', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING', TOMATO, anchor='middle'))
fleur.append('<line x1="500" y1="664" x2="1040" y2="664" stroke="%s" stroke-opacity=".3" stroke-width="1.6"/>' % INK)
fleur.append(T(CX, 724, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON', GREEN, anchor='middle'))
fleur.append(T(CX, 806, 'date', 'VENDREDI 7 MAI 2027', 'FRIDAY 7 MAY 2027', INK, anchor='middle'))
fleur.append(T(CX, 856, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE',
               'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', GREEN, anchor='middle'))
fleur.append(credits(CX, 922, 972, INK, anchor='middle'))

# --- B : la date en vedette ---
grosdate = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, CREAM)]
grosdate.append(bloom(1470, 560, 250, 155, 198, MUSTARD, TOMATO))
grosdate.append(T(X, 250, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES', GREEN))
grosdate.append(names_inline(X, 330, 46))
grosdate.append(T(X, 386, 'title-s', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING', TOMATO))
grosdate.append('<line x1="%d" y1="450" x2="960" y2="450" stroke="%s" stroke-opacity=".3" stroke-width="1.6"/>' % (X, INK))
grosdate.append(T(X, 620, 'huge-date', 'VENDREDI 7', 'FRIDAY 7', INK))
grosdate.append(T(X, 740, 'huge-date', 'MAI 2027', 'MAY 2027', TOMATO))
grosdate.append(T(X, 806, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE',
                  'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', GREEN))
grosdate.append(T(X, 856, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON', GREEN))
grosdate.append(credits(X, 916, 966, INK))

# --- C : l'horizon fleuri ---
horizon = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, CREAM)]
for cx, ring, pf, cf in [(70, 118, TOMATO, MUSTARD), (320, 104, MUSTARD, TOMATO), (570, 125, TOMATO, MUSTARD),
                         (830, 100, MUSTARD, GREEN), (1090, 122, TOMATO, MUSTARD), (1350, 108, MUSTARD, TOMATO),
                         (1540, 118, TOMATO, MUSTARD)]:
    horizon.append(bloom(cx, 1150, ring, int(ring * 0.62), int(ring * 0.8), pf, cf))
horizon.append(T(X, 230, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES', GREEN))
horizon.append(name_lines(X, 370, 478, 88))
horizon.append(T(X, 570, 'title', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING', TOMATO))
horizon.append('<line x1="%d" y1="628" x2="960" y2="628" stroke="%s" stroke-opacity=".3" stroke-width="1.6"/>' % (X, INK))
horizon.append(T(X, 684, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON', GREEN))
horizon.append(T(X, 760, 'date', 'VENDREDI 7 MAI 2027', 'FRIDAY 7 MAY 2027', INK))
horizon.append(T(X, 810, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE',
                 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', GREEN))
horizon.append(credits(X, 846, 894, INK))

# --- D : presque tout en typo ---
typo = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, CREAM)]
typo.append(bloom(1400, 250, 44, 28, 36, TOMATO, MUSTARD))
typo.append(T(X, 230, 'prod', 'COM&#201;DIE ROMANTIQUE &#8226; TOUS PUBLICS', 'ROMANTIC COMEDY &#8226; ALL AUDIENCES', GREEN))
typo.append(name_lines(X, 420, 560, 116))
typo.append(T(X, 660, 'title', 'CELUI QUI SE MARIE', 'THE ONE WITH THE WEDDING', TOMATO))
typo.append('<line x1="%d" y1="730" x2="1430" y2="730" stroke="%s" stroke-opacity=".3" stroke-width="1.6"/>' % (X, INK))
typo.append(T(X, 786, 'soon', 'UNE NOUVELLE S&#201;RIE &#8226; PROCHAINEMENT', 'A NEW SERIES &#8226; COMING SOON', GREEN))
typo.append(T(X, 852, 'date', 'VENDREDI 7 MAI 2027', 'FRIDAY 7 MAY 2027', INK))
typo.append(T(X, 904, 'place', 'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE',
              'CH&#194;TEAU EYPARSAC &#8226; BEYSSAC, CORR&#200;ZE', GREEN))
typo.append(credits(X, 948, 982, INK))

def card(cid, parts, label, guides=True):
    body = ''.join(parts) + (GUIDES if guides else '')
    return ('<svg id="%s" class="card" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'data-l="fr" data-n="formal" role="img" aria-label="%s">'
            '<style>%s</style>%s</svg>' % (cid, W, H, label, STYLE, body))

shell = read_shell("print_shell.html")
page = (shell
        .replace('{{RECTO}}', card('recto', recto, "Save the date recto, format A6 paysage avec fond perdu"))
        .replace('{{VERSO}}', card('verso', verso, "Save the date verso, format A6 paysage avec fond perdu"))
        .replace('{{W}}', str(W)).replace('{{H}}', str(H))
        .replace('{{MMW}}', '%.1f' % MM_W).replace('{{MMH}}', '%.1f' % MM_H))
io.open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, len(page), "bytes")
EMILY = os.path.join(ROOT, "index.html")
eshell = read_shell("emily_a6_shell.html")
palette_cards = ''.join(
    '''  <section class="piece">
    <p class="piece-tag">Palette &bull; %s</p>
    <div class="two-up">
      <div>
        <p class="side-tag">Recto</p>
        <div class="stage">%s</div>
        <div class="actions">
          <button class="btn" type="button" data-png="%s">T\u00e9l\u00e9charger</button>
          <button class="btn ghost" type="button" data-svg="%s">Imprimeur</button>
        </div>
      </div>
      <div>
        <p class="side-tag">Verso</p>
        <div class="stage">%s</div>
        <div class="actions">
          <button class="btn" type="button" data-png="%sv">T\u00e9l\u00e9charger</button>
          <button class="btn ghost" type="button" data-svg="%sv">Imprimeur</button>
        </div>
      </div>
    </div>
  </section>

''' % (pal['name'], gp.build(pal), pal['key'], pal['key'],
       gp.build_verso(pal), pal['key'], pal['key'])
    for pal in gp.PALETTES)

palette_grounds = ', '.join(
    "%s: '%s', %sv: '%s'" % (pal['key'], pal['ground'], pal['key'], gp.verso_ground(pal))
    for pal in gp.PALETTES)

epage = (eshell
         .replace('{{PALETTES}}', palette_cards)
         .replace('{{PALETTE_GROUNDS}}', palette_grounds)
         .replace('{{SOBRE}}', card('sobre', recto, "Save the date, version sobre, A6 paysage", guides=False))
         .replace('{{EQUI}}', card('equi', equi, "Save the date, version equilibree, A6 paysage", guides=False))
         .replace('{{SATU}}', card('satu', satu, "Save the date, version saturee, A6 paysage", guides=False))
         .replace('{{FLEUR}}', card('fleur', fleur, "Save the date, la fleur remplace le et commercial, A6 paysage", guides=False))
         .replace('{{GROSDATE}}', card('grosdate', grosdate, "Save the date, la date en vedette, A6 paysage", guides=False))
         .replace('{{HORIZON}}', card('horizon', horizon, "Save the date, horizon fleuri, A6 paysage", guides=False))
         .replace('{{TYPO}}', card('typo', typo, "Save the date, presque tout en typographie, A6 paysage", guides=False))
         .replace('{{VERSO}}', card('verso', verso, "Verso de la carte, A6 paysage", guides=False))
         .replace('{{W}}', str(W)).replace('{{H}}', str(H))
         .replace('{{MMW}}', '%.1f' % MM_W).replace('{{MMH}}', '%.1f' % MM_H))
io.open(EMILY, "w", encoding="utf-8").write(epage)
print("wrote", EMILY, len(epage), "bytes")
print("trim %d x %d mm, bleed %d mm, canvas %.1f x %.1f mm" % (TRIM_W / 10, TRIM_H / 10, BLEED / 10, MM_W, MM_H))
