from .core import *

FIG = (0, 0, ADV, C)

@glyph('0')
def _(k): return [k.oval(L, -O, R, C + O), k.pill(MID, C / 2, k.w * 1.05, k.w * 2.3)]  # dotted zero, never an O

@glyph('1')
def _(k): return [k.line(MID + 20, 0, MID + 20, C), k.line(MID + 20, C - k.h * .7, 135, C - 150, .95), k.line(120, k.h, 490, k.h, .9)]

@glyph('2')
def _(k):
    h, l, r = k.h, k.l, k.r
    ty = C + O - h
    return [S(P().M(l + 5, C - 170).C(l + 25, C - 50, MID - 90, ty, MID, ty).C(MID + 120, ty, r, C - 80, r, C - 205)
                 .C(r, C - 330, l + 20, 230, l, h), clip=(L, 0, ADV, C + O)), k.line(L, h, R, h, .9)]

@glyph('3')
def _(k):
    h, l, r = k.h, k.l, k.r
    ty, by, ym = C + O - h, -O + h, 415
    return [S(P().M(l + 5, C - 160).C(l + 30, C - 45, MID - 90, ty, MID, ty).C(MID + 125, ty, r - 15, C - 75, r - 15, C - 175)
                 .C(r - 15, ym + 70, MID + 60, ym, 235, ym)),
            S(P().M(235, ym).C(MID + 90, ym, r, ym - 50, r, 215).C(r, 80, MID + 110, by, MID, by).C(MID - 100, by, l + 10, by + 45, l, 145))]

@glyph('4')
def _(k):
    h, x = k.h, 400
    return [k.line(x, 0, x, C), S(P().M(x, C).L(L - 40, 240).L(R, 240), clip=(L, 0, ADV, C))]

@glyph('5')
def _(k):
    h, l, r = k.h, k.l, k.r
    by, x = -O + h, l + 15
    return [S(P().M(R - 20, C - h).L(x, C - h).L(x, 400).C(x + 60, 450, MID - 30, 470, MID + 20, 470).C(MID + 160, 470, r, 380, r, 240)
                 .C(r, 85, MID + 110, by, MID, by).C(MID - 100, by, l + 10, by + 45, l, 145))]

@glyph('6')
def _(k):
    h, l = k.h, k.l
    return [k.oval(L, -O, R, 480), S(P().M(l, 240).C(l, 460, 250, C - 60, R - 40, C - 10))]

@glyph('9')
def _(k): return rot(G['6'](k), C / 2)

@glyph('7')
def _(k):
    h = k.h
    return [k.line(L, C - h, R, C - h, .9), k.line(k.r, C - h, 215, -20, clip=FIG)]

@glyph('8')
def _(k): return [k.oval(L + 30, 380, R - 30, C + O), k.oval(L, -O, R, 415)]
