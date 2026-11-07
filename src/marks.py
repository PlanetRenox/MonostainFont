# Accents, and every accented letter in Latin-1 and Latin Extended-A, built from Unicode's decompositions:
# base glyph + accent, raised for capitals and tall letters. Letters with no decomposition are drawn below.
import unicodedata
from .core import *
from .upper import dbowl

T = X + 95  # bottom of lowercase accents

def acute(k): return [k.line(250, T + 10, 365, T + 150, .9)]
def grave(k): return mirror(acute(k))
def circ(k): return [S(P().M(160, T).L(MID, T + 150).L(440, T), .9, clip=(0, T - 99, ADV, T + 150))]
def caron(k): return flip(circ(k), T + 75)
def tilde(k): return [S(P().M(150, T + 25).C(180, T + 120, 245, T + 125, MID, T + 80).C(355, T + 35, 420, T + 35, 450, T + 130), .9)]
def macron(k): return [k.line(160, T + 75, 440, T + 75, .9)]
def breve(k): return [S(P().M(175, T + 150).C(180, T + 45, 240, T + 15, MID, T + 15).C(360, T + 15, 420, T + 45, 425, T + 150), .85)]
def dot(k): return [k.dot(MID, T + 70)]
def uml(k): return [k.dot(195, T + 70), k.dot(405, T + 70)]
def ring(k): return [S(Ov(k, 205, T - 10, 395, T + 175).path(), .8)]
def dacute(k): return [k.line(185, T + 10, 285, T + 150, .85), k.line(345, T + 10, 445, T + 150, .85)]
def cedilla(k): return [S(P().M(MID + 10, 30).L(MID + 10, -65).C(390, -65, 410, -100, 410, -140).C(410, -190, 355, -210, 230, -205), .82)]
def ogonek(k, x=440): return [S(P().M(x, 20).C(x - 75, -20, x - 105, -80, x - 100, -125).C(x - 95, -185, x - 30, -200, x + 30, -175), .82)]
def commab(k): return [k.dot(MID, -100, k.dr * .9), k.line(MID + k.dr * .5, -100, MID - 50, -240, .78, clip=(0, -999, ADV, -100))]
def commaa(k): return rot(commab(k), (T + 10) / 2)  # turned comma above, for ģ

MARKS = {'̀': grave, '́': acute, '̂': circ, '̃': tilde, '̄': macron, '̆': breve, '̇': dot,
         '̈': uml, '̊': ring, '̋': dacute, '̌': caron, '̧': cedilla, '̨': ogonek}
SPACING = {'´': acute, '`': None, '¨': uml, '¯': macron, '¸': cedilla, 'ˆ': circ, '˜': tilde, 'ˇ': caron, '˘': breve, '˙': dot,
           '˚': ring, '˝': dacute, '˛': ogonek}
for ch, f in SPACING.items():
    if f: glyph(ch)(lambda k, f=f: f(k))

UP = C - X - 15  # capitals carry accents this much higher
TALL = A - X + 10  # and letters with ascenders (ĥ) this much
OGONEK = {'a': 470, 'e': 390, 'i': 420, 'u': 470, 'A': 520, 'E': 450, 'I': 370, 'U': 400}
COMMA_BELOW = set('KkLlNnRrGgTt')  # Unicode says cedilla, but Latvian and Romanian want a comma (above g)
CARON_APOS = {'d': 570, 'l': 400, 'L': 330, 't': 380}  # ď ľ Ľ ť: the caron becomes a small apostrophe beside the letter

def apos(k, x, top):
    return [k.line(x + 12, top + 5, x - 18, top - 175, .85, clip=(0, top - 175, ADV - 5, top + 5))]

@glyph('ȷ')
def _(k): return G['j'](k)[:2]

def composite(ch):
    d = unicodedata.decomposition(ch).split()
    if len(d) != 2 or d[0].startswith('<'): return None
    base, mark = chr(int(d[0], 16)), chr(int(d[1], 16))
    if base not in G and base not in 'ij' or mark not in MARKS: return None
    def f(k):
        b = 'ı' if base == 'i' and mark not in '̨' else 'ȷ' if base == 'j' else base
        parts = G[b](k)
        if mark == '̨': return parts + ogonek(k, OGONEK.get(base, 440))
        if mark == '̧' and base in COMMA_BELOW:
            return parts + (commaa(k) if base == 'g' else commab(k))
        if mark == '̧': return parts + cedilla(k)
        if mark == '̌' and base in CARON_APOS: return parts + apos(k, CARON_APOS[base], A if base.islower() else C)
        dy = UP if base.isupper() else TALL if base in 'bdhklt' else 0
        return parts + move(MARKS[mark](k), 0, dy)
    return f

for cp in list(range(0xC0, 0x100)) + list(range(0x100, 0x180)):
    ch = chr(cp)
    if ch not in G and (f := composite(ch)): glyph(ch)(f)

# Letters without a decomposition

@glyph('Ø')
def _(k): return G['O'](k) + [k.line(CR + 5, C + 60, CL - 5, -60, .9, (CL, -O, CR, C + O))]

@glyph('ø')
def _(k): return G['o'](k) + [k.line(R + 5, X + 60, L - 5, -60, .9, (L, -O, R, X + O))]

@glyph('Ł')
def _(k): return G['L'](k) + [k.line(CL - 15, 300, 300, 480, .9)]

@glyph('ł')
def _(k): return G['l'](k) + [k.line(130, 360, 420, 520, .9)]

@glyph('Đ', 'Ð')
def _(k): return G['D'](k) + [k.line(CL - 25, 380, 270, 380, .9)]

@glyph('đ')
def _(k): return G['d'](k) + [k.line(300, A - 140, R + 30, A - 140, .85)]

@glyph('Ħ')
def _(k): return G['H'](k) + [k.line(CL - 30, C - 150, CR + 30, C - 150, .85)]

@glyph('ħ')
def _(k): return G['h'](k) + [k.line(L - 30, A - 140, 300, A - 140, .85)]

@glyph('Ŧ')
def _(k): return G['T'](k) + [k.line(170, 380, 430, 380, .9)]

@glyph('ŧ')
def _(k): return G['t'](k) + [k.line(150, 290, 400, 290, .85)]

@glyph('ð')
def _(k):
    wf = min(1, 90 / k.w)
    return [k.oval(L, -O, R, 480), S(P().M(k.r, 240).C(k.r, 470, 380, A - 60, 190, A + 10), wf), k.line(210, 590, 450, 690, .75)]

@glyph('Þ')
def _(k): return [k.line(k.cl, 0, k.cl, C), S(dbowl(k, k.cl, k.cr, 160 + k.h, C - 150 - k.h, 200))]

@glyph('þ')
def _(k): return [k.line(k.l, D, k.l, A)] + G['p'](k)[1:]

@glyph('ß')
def _(k):
    h, l = k.h, k.l
    return [S(P().M(l, 0).L(l, A - 230).C(l, A - 60, 190, A + O - h, 300, A + O - h).C(420, A + O - h, k.r - 10, A - 70, k.r - 10, A - 190)
                 .C(k.r - 10, 450, 330, 430, 270, 430).C(380, 430, k.r, 360, k.r, 210).C(k.r, 60, 400, -O + h, 300, -O + h).L(230, -O + h))]

# Ligatures squeeze two letters into one cell: x is remapped onto each half, stroke width stays put
squeeze = lambda parts, x0, x1, nx0, nx1, wf: tf(parts, lambda x, y: (nx0 + (x - x0) * (nx1 - nx0) / (x1 - x0), y), wf)
LIG = lambda k: .78 if k.w < 100 else .7

@glyph('æ')
def _(k): return squeeze(G['a'](k), L, R, L - 10, 315, LIG(k)) + squeeze(G['e'](k), L, R, 285, R + 10, LIG(k))

@glyph('œ')
def _(k): return squeeze(G['o'](k), L, R, L - 10, 315, LIG(k)) + squeeze(G['e'](k), L, R, 285, R + 10, LIG(k))

def _e(k, m, wf):
    """E arms off a stem centered on m"""
    h = k.h * wf
    return [k.line(m, 0, m, C, wf), k.line(m, C - h, CR, C - h, wf * .92), k.line(m, 390, CR - 20, 390, wf * .92), k.line(m, h, CR, h, wf * .92)]

@glyph('Œ')
def _(k):
    wf = LIG(k)
    return squeeze(G['O'](k), CL, CR, CL - 10, 340, wf) + _e(k, 340 - k.h * wf, wf)

@glyph('Æ')
def _(k):
    wf = LIG(k)
    m, t = 330, C + 90
    leg = lambda y: CL - 30 + (m - CL + 30) * (y + 70) / (t + 70)
    return [S(P().M(CL - 30, -70).L(m, t), wf, clip=(0, 0, ADV, C))] + _e(k, m, wf) + [k.line(leg(230), 230, m, 230, wf * .92)]

@glyph('ĸ')
def _(k): return [k.line(k.l, 0, k.l, X), k.line(R + 10, X + 60, k.l, 120, clip=(0, -99, ADV, X)), k.line(230, 250, R + 20, -60, clip=(0, 0, ADV, 999))]

@glyph('ŋ')
def _(k):
    n = G['n'](k)
    by = D - O + k.h
    return n + [S(P().M(k.r, 100).L(k.r, -20).C(k.r, D + 70, k.r - 50, by, k.r - 150, by).L(230, by))]

@glyph('Ŋ')
def _(k):
    by = D + 30 - O + k.h
    return [k.line(k.cl, 0, k.cl, C), S(P().M(k.cl, C - 260).C(k.cl + 80, C - 90, 220, C + O - k.h, 330, C + O - k.h).C(470, C + O - k.h, k.cr, C - 100, k.cr, C - 260)
                 .L(k.cr, 0).C(k.cr, D + 100, k.cr - 50, by, k.cr - 150, by).L(220, by))]

@glyph('ſ')
def _(k): return G['f'](k)[:1]

@glyph('ŉ')
def _(k): return move(G['n'](k), 40) + apos(k, 120, C + 20)

@glyph('Ŀ')
def _(k): return G['L'](k) + [k.dot(400, 360)]

@glyph('ŀ')
def _(k): return G['l'](k) + [k.dot(480, 360)]

@glyph('Ĳ')
def _(k):
    wf, h = .8, k.h * .8
    return [k.line(170, 0, 170, C, wf), k.line(CL + 10, C - h, 280, C - h, wf), k.line(CL + 10, h, 280, h, wf),
            S(P().M(CR - h, C).L(CR - h, 200).C(CR - h, 60, 470, -O + h, 410, -O + h).C(360, -O + h, 320, 20, 300, 80), wf)]

@glyph('ĳ')
def _(k):
    wf = .8
    return [k.line(170, 0, 170, X, wf), k.dot(170, X + 175, k.dr * .9), S(P().M(430, X).L(430, -20).C(430, D + 70, 390, D - O + k.h * wf, 320, D - O + k.h * wf).L(230, D - O + k.h * wf), wf),
            k.dot(430, X + 175, k.dr * .9)]
