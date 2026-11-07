from .core import *

MATH = 330  # math axis, centre of + - = < > and friends
TOP, BOT = 790, -170  # brackets, bars and slashes span this
glyph(' ', ' ')(lambda k: [])

@glyph('.')
def _(k): return [k.dot(MID, k.dr)]

@glyph(',')
def _(k): return [k.dot(MID, k.dr), k.line(MID + k.dr * .55, k.dr, MID - 60, -150, .82, clip=(0, -999, ADV, k.dr))]

@glyph(':')
def _(k): return [k.dot(MID, k.dr), k.dot(MID, X - k.dr)]

@glyph(';')
def _(k): return G[','](k) + [k.dot(MID, X - k.dr)]

@glyph('!')
def _(k): return [k.line(MID, C, MID, 230), k.dot(MID, k.dr)]

@glyph('?')
def _(k):
    h, l, r = k.h, k.l + 10, k.r - 10
    ty = C + O - h
    return [S(P().M(l, C - 160).C(l + 25, C - 45, MID - 90, ty, MID, ty).C(MID + 120, ty, r, C - 75, r, C - 195)
                 .C(r, C - 300, MID, 380, MID, 300).L(MID, 230)), k.dot(MID, k.dr)]

@glyph("'")
def _(k): return [k.line(MID, C + 20, MID, C - 230)]

@glyph('"')
def _(k): return [k.line(200, C + 20, 200, C - 230), k.line(400, C + 20, 400, C - 230)]

@glyph('`')
def _(k): return [k.line(220, C + 60, 360, C - 110, clip=(0, C - 100, ADV, C + 40))]

@glyph('-')
def _(k): return [k.line(150, 300, 450, 300, .9)]

@glyph('_')
def _(k): return [k.line(30, -140, 570, -140, .9)]

@glyph('+')
def _(k): return [k.line(110, MATH, 490, MATH, .9), k.line(MID, MATH - 190, MID, MATH + 190)]

@glyph('=')
def _(k): return [k.line(110, MATH + 100, 490, MATH + 100, .9), k.line(110, MATH - 100, 490, MATH - 100, .9)]

@glyph('<')
def _(k): return [S(P().M(480, MATH + 220).L(120, MATH).L(480, MATH - 220), clip=(L - 5, -999, ADV, 999))]  # blunt tip, never past the cell

@glyph('>')
def _(k): return mirror(G['<'](k))

@glyph('~')
def _(k): return [S(P().M(100, MATH - 60).C(130, MATH + 40, 200, MATH + 70, MID, MATH).C(400, MATH - 70, 470, MATH - 40, 500, MATH + 60), .9)]

@glyph('^')
def _(k): return [S(P().M(120, 420).L(MID, C + 60).L(480, 420), clip=(0, 0, ADV, C))]

@glyph('*')
def _(k):
    c, r = (MID, 520), 175
    ls = [k.line(c[0], c[1] + r, c[0], c[1] - r, .9)]
    for a in (30, 150):
        dx, dy = r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
        ls.append(k.line(c[0] - dx, c[1] - dy, c[0] + dx, c[1] + dy, .9))
    return ls

@glyph('/')
def _(k): return [k.line(480, TOP, 120, BOT, clip=(0, BOT, ADV, TOP))]

@glyph('\\')
def _(k): return mirror(G['/'](k))

@glyph('|')
def _(k): return [k.line(MID, TOP, MID, BOT)]

@glyph('(')
def _(k): return [S(P().M(420, TOP).C(220, 640, 220, -20, 420, BOT), clip=(0, BOT, ADV, TOP))]

@glyph(')')
def _(k): return mirror(G['('](k))

@glyph('[')
def _(k):
    h, x = k.h, 230
    return [S(P().M(440, TOP - h).L(x, TOP - h).L(x, BOT + h).L(440, BOT + h))]

@glyph(']')
def _(k): return mirror(G['['](k))

@glyph('{')
def _(k):
    h, x, m = k.h, 290, (TOP + BOT) / 2
    half = [S(P().M(450, TOP - h).L(x + 70, TOP - h).C(x + 20, TOP - h, x, TOP - 40, x, TOP - 110).L(x, m + 90).C(x, m + 30, x - 40, m, 150, m))]
    return half + flip(half, m)

@glyph('}')
def _(k): return mirror(G['{'](k))

@glyph('#')
def _(k):
    c = (0, 20, ADV, C - 20)
    return [k.line(195, -30, 245, C + 30, .88, c), k.line(375, -30, 425, C + 30, .88, c), k.line(L, 470, R, 470, .88), k.line(L, 250, R, 250, .88)]

@glyph('$')
def _(k): return scale(G['S'](k), .86, MID, C / 2, wf=.94) + [k.line(MID, C + 60, MID, -110, .9)]

@glyph('%')
def _(k):
    wf = min(.85, 80 / k.w)  # rings stay open in bold
    return [S(Ov(k, L - 5, 395, 285, C + O).path(), wf), S(Ov(k, 315, -O, R + 5, 335).path(), wf),
                  k.line(R + 10, C + 10, L - 10, -10, .9, (L, 0, R, C))]

@glyph('&')
def _(k):
    h = k.h
    return [S(P().M(R + 5, -30).L(215, 445).C(160, 505, 170, C + O - h, MID - 5, C + O - h).C(400, C + O - h, 440, 640, 410, 580)
                 .C(390, 535, 330, 500, 230, 430).C(120, 355, L + 5, 290, L + 5, 190).C(L + 5, 70, 160, -O + h, 260, -O + h)
                 .C(390, -O + h, 450, 90, 470, 330), clip=(0, 0, ADV, C + 20))]

@glyph('@')
def _(k):
    wf = .72
    h = k.h * wf
    x, ty, by, xr, xl = 395 - h, C + O - h, -110, R + 22 - h, L - 22 + h
    return [S(Ov(k, 175, 150, 395, 505).path(), wf),
            S(P().M(x, 505).L(x, 240).C(x, 190, 420, 160, 458, 160).C(505, 160, xr, 215, xr, 330)
                 .C(xr, 570, 425, ty, MID, ty).C(170, ty, xl, 580, xl, 330)
                 .C(xl, 50, 175, by, 320, by).C(385, by, 440, by + 10, 480, by + 30), wf)]

# Typographic punctuation

def comma(k, x, y):
    """Comma whose head sits on (x, y)"""
    r = k.dr
    return [k.dot(x, y, r), k.line(x + r * .55, y, x - 60, y - 150 - r, .82, clip=(0, -999, ADV, y))]

QT = C - 90  # head height of quotes
glyph('’')(lambda k: comma(k, MID, QT))
glyph('‘')(lambda k: rot(comma(k, MID, QT), QT - 75))
glyph('‚')(lambda k: comma(k, MID, k.dr))
glyph('”')(lambda k: comma(k, 190, QT) + comma(k, 410, QT))
glyph('“')(lambda k: rot(comma(k, 190, QT) + comma(k, 410, QT), QT - 75))
glyph('„')(lambda k: comma(k, 190, k.dr) + comma(k, 410, k.dr))
glyph('–')(lambda k: [k.line(L, 300, R, 300, .9)])
glyph('—')(lambda k: [k.line(0, 300, ADV, 300, .9)])
glyph('−')(lambda k: [k.line(110, MATH, 490, MATH, .9)])  # minus
glyph('­', '‐', '‑')(lambda k: G['-'](k))  # soft, plain and non-breaking hyphen
glyph('…')(lambda k: [k.dot(100, k.dr), k.dot(MID, k.dr), k.dot(500, k.dr)])
glyph('·')(lambda k: [k.dot(MID, 300)])
glyph('•')(lambda k: [k.dot(MID, MATH, k.dr * 2)])
glyph('¡')(lambda k: rot(G['!'](k), (X + 10) / 2 - 20))
glyph('¿')(lambda k: rot(G['?'](k), (X + 10) / 2 - 20))

def chev(k, x, s=1):
    """Guillemet half pointing left from x, s=-1 points right"""
    t = x - k.h * s  # cut the tip flat, a miter would spike out in bold
    return [S(P().M(x + 150 * s, 455).L(x, 275).L(x + 150 * s, 95), .9, clip=(t, -999, 999, 999) if s > 0 else (-999, -999, t, 999))]

glyph('‹')(lambda k: chev(k, 225))
glyph('›')(lambda k: chev(k, 375, -1))
glyph('«')(lambda k: chev(k, 110) + chev(k, 320))
glyph('»')(lambda k: chev(k, 490, -1) + chev(k, 280, -1))

# Signs and math

glyph('°')(lambda k: [S(Ov(k, 165, C - 265, 435, C + O).path(), min(.85, 72 / k.w))])
glyph('×')(lambda k: [k.line(150, MATH - 150, 450, MATH + 150, .9), k.line(150, MATH + 150, 450, MATH - 150, .9)])
glyph('÷')(lambda k: [k.line(110, MATH, 490, MATH, .9), k.dot(MID, MATH + 170), k.dot(MID, MATH - 170)])
glyph('±')(lambda k: move(G['+'](k), 0, 60) + [k.line(110, k.h * .9 + 10, 490, k.h * .9 + 10, .9)])
glyph('¬')(lambda k: [S(P().M(110, MATH + 90).L(490 - k.h, MATH + 90).L(490 - k.h, MATH - 110), .9)])
glyph('¦')(lambda k: [k.line(MID, TOP, MID, 400), k.line(MID, 220, MID, BOT)])
glyph('≠')(lambda k: G['='](k) + [k.line(420, MATH + 250, 180, MATH - 250, .85)])
glyph('≈')(lambda k: move(G['~'](k), 0, 95) + move(G['~'](k), 0, -95))
glyph('≤')(lambda k: [S(P().M(480, MATH + 260).L(120, MATH + 85).L(480, MATH - 90), .9, clip=(L - 5, -999, ADV, 999)), k.line(120, MATH - 235, 480, MATH - 235, .9)])
glyph('≥')(lambda k: mirror(G['≤'](k)))
glyph('µ', 'μ')(lambda k: G['u'](k) + [k.line(k.l, X, k.l, D)])

def ring_with(k, letter):
    """Letter shrunk into a circle, for © and ®"""
    return [S(Ov(k, 25, 120, 575, 670, f=1).path(), min(.8, 72 / k.w))] + scale(G[letter](k), .5, MID, C / 2, 0, 395 - C / 2, min(.85, 60 / k.w))

glyph('©')(lambda k: ring_with(k, 'C'))
glyph('®')(lambda k: ring_with(k, 'R'))
glyph('™')(lambda k: scale(G['T'](k), .44, MID, C, -140, 0, .8) + scale(G['M'](k), .44, MID, C, 125, 0, .8))
glyph('§')(lambda k: scale(G['s'](k), .7, MID, 0, 0, 365) + scale(G['s'](k), .7, MID, 0, 0, 40))
glyph('¶')(lambda k: [k.line(330, C - k.h, 330, BOT + 40), k.line(460, C, 460, BOT + 40), k.line(330, C - k.h, 460, C - k.h),
                      F(P().M(330, C).L(270, C).C(170, C, 110, C - 80, 110, C - 185).C(110, C - 290, 170, 330, 270, 330).L(330, 330).Z())])
glyph('†')(lambda k: [k.line(MID, C, MID, -120), k.line(130, C - 200, 470, C - 200, .9)])
glyph('‡')(lambda k: G['†'](k) + [k.line(130, 120, 470, 120, .9)])
glyph('¤')(lambda k: [S(Ov(k, 150, 180, 450, 480, f=1).path(), min(.85, 70 / k.w))] + [k.line(MID + dx * 150, 330 + dy * 150, MID + dx * 230, 330 + dy * 230, .85)
                      for dx, dy in ((.71, .71), (-.71, .71), (.71, -.71), (-.71, -.71))])

# Currency

glyph('€')(lambda k: move(G['C'](k), 30) + [k.line(20, 300, 380, 300, .85), k.line(20, 440, 400, 440, .85)])
glyph('¢')(lambda k: G['c'](k) + [k.line(MID + 10, X + 110, MID + 10, -110, .85)])
glyph('¥')(lambda k: G['Y'](k) + [k.line(110, 250, 490, 250, .85), k.line(110, 120, 490, 120, .85)])

@glyph('£')
def _(k):
    h, x = k.h, 200
    return [S(P().M(R - 25, C - 150).C(R - 50, C - 40, 420, C + O - h, MID + 20, C + O - h).C(220, C + O - h, x, C - 90, x, C - 190).L(x, 170)
                 .C(x, 80, 160, h + 5, 90, h)), k.line(L, h, R, h, .9), k.line(L + 10, 380, 400, 380, .9)]

@glyph('ƒ')
def _(k):
    h, x, by = k.h, 300, D - O + k.h
    return [S(P().M(L + 20, by).L(x - 120, by).C(x - 40, by, x, D + 60, x, D + 170).L(x, A - 200).C(x, A - 70, x + 60, A - h, x + 140, A - h).L(R - 10, A - h)),
            k.line(L + 50, X - h, R - 50, X - h, .9)]

# Superscripts, ordinals and fractions

SUP = .56
sup = lambda k, c: scale(G[c](k), SUP, MID, 0, 0, C - SUP * C, .78)
glyph('¹')(lambda k: sup(k, '1'))
glyph('²')(lambda k: sup(k, '2'))
glyph('³')(lambda k: sup(k, '3'))
glyph('ª')(lambda k: scale(G['a'](k), .6, MID, 0, 0, C - .6 * (X + O), min(.8, 72 / k.w)) + [k.line(150, 290, 450, 290, .8)])
glyph('º')(lambda k: scale(G['o'](k), .6, MID, 0, 0, C - .6 * (X + O), min(.8, 72 / k.w)) + [k.line(150, 290, 450, 290, .8)])

def frac(k, a, b):
    s, wf = .44, min(.72, 62 / k.w)
    return scale(G[a](k), s, MID, 0, -125, C - s * C, wf) + scale(G[b](k), s, MID, 0, 125, 0, wf) + [k.line(470, C - 40, 130, 40, .8)]

glyph('¼')(lambda k: frac(k, '1', '4'))
glyph('½')(lambda k: frac(k, '1', '2'))
glyph('¾')(lambda k: frac(k, '3', '4'))

@glyph('‰')
def _(k):
    wf = min(.8, 64 / k.w)
    return [S(Ov(k, L - 15, 460, 235, C + O).path(), wf), S(Ov(k, L - 15, -O, 285, 300).path(), wf), S(Ov(k, 315, -O, R + 15, 300).path(), wf),
            k.line(R + 10, C + 60, 160, 330, .85, (0, 345, R, C))]

# Arrows

AX = MATH + 10
def arrow(k):
    """Right arrow, the others are turned copies"""
    return [k.line(70, AX, 510, AX, .9), S(P().M(330, AX + 190).L(520, AX).L(330, AX - 190), .9, clip=(0, 0, 530, 999))]

glyph('→')(arrow)
glyph('←')(lambda k: mirror(arrow(k)))
glyph('↑')(lambda k: tf(arrow(k), lambda x, y: (MID - (y - AX), AX + (x - MID) * 1.25)))
glyph('↓')(lambda k: tf(arrow(k), lambda x, y: (MID + (y - AX), AX - (x - MID) * 1.25)))
glyph('↔')(lambda k: [k.line(70, AX, 530, AX, .9), S(P().M(220, AX + 160).L(65, AX).L(220, AX - 160), .9), S(P().M(380, AX + 160).L(535, AX).L(380, AX - 160), .9)])

# Box drawing and blocks fill the whole line box (descent to ascent) so they join up between lines and cells

BT, BB = 1020, -300
BM = (BT + BB) / 2
def box(k, l=0, r=0, u=0, d=0):
    """Light lines from the cell centre to the left, right, up and down edges"""
    out = []
    if l or r: out.append(k.line(0 if l else MID - k.h * .85, BM, ADV if r else MID + k.h * .85, BM, .85))
    if u or d: out.append(k.line(MID, BT if u else BM - k.h * .85, MID, BB if d else BM + k.h * .85, .85))
    return out

for ch, a in {'─': (1, 1, 0, 0), '│': (0, 0, 1, 1), '┌': (0, 1, 0, 1), '┐': (1, 0, 0, 1), '└': (0, 1, 1, 0), '┘': (1, 0, 1, 0),
              '├': (0, 1, 1, 1), '┤': (1, 0, 1, 1), '┬': (1, 1, 0, 1), '┴': (1, 1, 1, 0), '┼': (1, 1, 1, 1), '╴': (1, 0, 0, 0),
              '╵': (0, 0, 1, 0), '╶': (0, 1, 0, 0), '╷': (0, 0, 0, 1)}.items():
    glyph(ch)(lambda k, a=a: box(k, *a))

def rounded(k, sx, sy):
    """╭ turned by sx, sy: a quarter circle from the right edge to the bottom edge"""
    r = MID
    p = P().M(ADV, BM).C(MID + r * (1 - .5523), BM, MID, BM - r * .5523, MID, BM - r).L(MID, BB)
    return [S(tf([S(p)], lambda x, y: (MID + (x - MID) * sx, BM + (y - BM) * sy))[0].p, .85)]

glyph('╭')(lambda k: rounded(k, 1, 1))
glyph('╮')(lambda k: rounded(k, -1, 1))
glyph('╰')(lambda k: rounded(k, 1, -1))
glyph('╯')(lambda k: rounded(k, -1, -1))
glyph('█')(lambda k: [F(P().M(0, BB).L(ADV, BB).L(ADV, BT).L(0, BT).Z())])
glyph('▀')(lambda k: [F(P().M(0, BM).L(ADV, BM).L(ADV, BT).L(0, BT).Z())])
glyph('▄')(lambda k: [F(P().M(0, BB).L(ADV, BB).L(ADV, BM).L(0, BM).Z())])
glyph('▌')(lambda k: [F(P().M(0, BB).L(MID, BB).L(MID, BT).L(0, BT).Z())])
glyph('▐')(lambda k: [F(P().M(MID, BB).L(ADV, BB).L(ADV, BT).L(MID, BT).Z())])
