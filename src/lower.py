from .core import *

# Arches and bowls are filled bands, not strokes: the outer curve flows off the top of the stem
# while the inner one meets the stem lower down, so the join gets the notch and thinning a stroke can't
TF = .92  # tops and bottoms of arches and bowls are a little thinner than stems

def _top(k, x0, x1, top, w):
    """Shared geometry of an arch over x0..x1 (outer edges) with stem width w"""
    a, b, j = x0 + w, x1 - w, top - w - 90
    co, ci = (x0 + x1) / 2 + 20, (a + b) / 2 + 12
    return a, b, j, co, ci, top + O, top + O - w * TF, x0 + w / 2

def nband(k, x0, x1, top=X, foot=0, w=None):
    """n arch from a left stem over to a right stem that runs down to foot"""
    w = w or k.w
    a, b, j, co, ci, to, ti, s = _top(k, x0, x1, top, w)
    ro, ri = x1 - co, b - ci
    outer = P().M(s, top).C(a + (co - a) * .1, top + 2, co - (co - a) * .62, to, co, to) \
               .C(co + ro * Ov.K, to, x1, to - ro * Ov.K, x1, to - ro).L(x1, foot)
    inner = P().M(s, j - 40).L(a, j).C(a + (ci - a) * .18, j + (ti - j) * .55, ci - (ci - a) * .6, ti, ci, ti) \
               .C(ci + ri * Ov.K, ti, b, ti - ri * Ov.K, b, ti - ri).L(b, foot)
    return band(outer, inner)

def bband(k, x0, x1, y0=0, y1=X, w=None):
    """Bowl of b and p: leaves the stem at the top, rounds the right side and rejoins the stem at the bottom"""
    w = w or k.w
    a, b, j1, co, ci, to, ti, s = _top(k, x0, x1, y1, w)
    j0, bo, bi = y0 + w + 90, y0 - O, y0 - O + w * TF
    ro, ri = x1 - co, b - ci
    cro, cri = min(ro, (to - bo) / 2), min(ri, (ti - bi) / 2)
    outer = P().M(s, y1).C(a + (co - a) * .1, y1 + 2, co - (co - a) * .62, to, co, to) \
               .C(co + ro * Ov.K, to, x1, to - cro * Ov.K, x1, to - cro).L(x1, bo + cro) \
               .C(x1, bo + cro * Ov.K, co + ro * Ov.K, bo, co, bo).C(co - (co - a) * .62, bo, a + (co - a) * .1, y0 - 2, s, y0)
    inner = P().M(s, j1 - 40).L(a, j1).C(a + (ci - a) * .18, j1 + (ti - j1) * .55, ci - (ci - a) * .6, ti, ci, ti) \
               .C(ci + ri * Ov.K, ti, b, ti - cri * Ov.K, b, ti - cri).L(b, bi + cri) \
               .C(b, bi + cri * Ov.K, ci + ri * Ov.K, bi, ci, bi).C(ci - (ci - a) * .6, bi, a + (ci - a) * .18, j0 - (j0 - bi) * .55, a, j0).L(s, j0 + 40)
    return band(outer, inner)

def rband(k, x0, x1, top=X, w=None):
    """Arm of r: an arch from the stem that ends in a vertical cut at x1"""
    w = w or k.w
    a, j = x0 + w, top - w - 90
    co, to, ti, s, e = (a + x1) / 2 - 10, top + O, top + O - w * TF, x0 + w / 2, top + O - 75
    outer = P().M(s, top).C(a + (co - a) * .1, top + 2, co - (co - a) * .6, to, co, to).C(co + (x1 - co) * .6, to, x1, to - 12, x1, e)
    inner = P().M(s, j - 40).L(a, j).C(a + (co - a) * .18, j + (ti - j) * .55, co - (co - a) * .6, ti, co, ti).C(co + (x1 - co) * .5, ti, x1, ti - 8, x1, e - w * .95)
    return band(outer, inner)

@glyph('o')
def _(k): return [k.oval(L, -O, R, X + O)]

@glyph('n')
def _(k): return [k.line(k.l, 0, k.l, X), nband(k, L, R)]

@glyph('h')
def _(k): return [k.line(k.l, 0, k.l, A), nband(k, L, R)]

@glyph('u')
def _(k): return rot(G['n'](k), X / 2)

@glyph('m')
def _(k):
    w = k.w * .78
    return [k.line(L + w / 2, 0, L + w / 2, X, .78), nband(k, L, MID + w / 2, w=w), nband(k, MID - w / 2, R, w=w)]

@glyph('b')
def _(k): return [k.line(k.l, 0, k.l, A), bband(k, L, R)]

@glyph('p')
def _(k): return [k.line(k.l, D, k.l, X), bband(k, L, R)]

@glyph('d')
def _(k): return mirror(G['b'](k))

@glyph('q')
def _(k): return mirror(G['p'](k))

@glyph('g')
def _(k):
    h, r, l = k.h, k.r, k.l
    by = D - O + h
    return mirror([bband(k, L, R)]) + [S(P().M(r, X).L(r, -10).C(r, D + 70, r - 50, by, r - 150, by).L(L + 25, by))]

@glyph('c')
def _(k):
    q = k.ov(L, -O, R, X + O).q
    a = sub(q[0], .38, 1)
    return [S(P().M(*a[0]).cub(a).cub(q[1]).L(*q[2][0]).cub(q[2]).cub(sub(q[3], 0, .62)))]

@glyph('e')
def _(k):
    o = k.ov(L, -O, R, X + O)
    q, yb = o.q, 290
    return [S(P().M(k.r, yb).L(*q[0][0]).cub(q[0]).cub(q[1]).L(*q[2][0]).cub(q[2]).cub(sub(q[3], 0, .7))), k.line(k.l, yb, k.r, yb, .9)]

@glyph('a')
def _(k):
    h, l, r = k.h, k.l, k.r
    ty, by, yb = X + O - h, -O + h, 320
    ym = (yb + by) / 2
    return [S(P().M(r, 0).L(r, X - 200).C(r, X - 60, r - 70, ty, MID, ty).C(MID - 110, ty, l + 20, ty - 35, l + 5, X - 110)),
            S(P().M(r, yb).L(255, yb).C(255 - (255 - l) * Ov.K, yb, l, ym + (yb - ym) * Ov.K, l, ym)
                 .C(l, ym - (ym - by) * Ov.K, 160, by, 245, by).C(330, by, r - 25, by + 45, r, 150))]

@glyph('s')
def _(k):
    h, xl, xr = k.h, k.l + 5, k.r - 5
    ty, by, cy = X + O - h, -O + h, X / 2
    yl, yr = (cy + ty) / 2 + 8, (cy + by) / 2 - 8
    return [S(P().M(xr + 5, X - 120).C(xr - 15, ty - 20, MID + 95, ty, MID, ty)
                 .C(MID - (MID - xl) * Ov.K, ty, xl, yl + (ty - yl) * Ov.K, xl, yl)
                 .C(xl, yl - 75, MID - 120, cy + 30, MID, cy).C(MID + 120, cy - 30, xr, yr + 75, xr, yr)
                 .C(xr, yr - (yr - by) * Ov.K, MID + (xr - MID) * Ov.K, by, MID, by).C(MID - 100, by, xl - 5, by + 30, xl - 10, 120))]

@glyph('i')
def _(k): return [k.line(MID, 0, MID, X), k.line(140, X - k.h, MID, X - k.h), k.line(100, k.h, 500, k.h), k.dot(MID, X + 175)]

@glyph('ı')
def _(k): return G['i'](k)[:3]

@glyph('j')
def _(k):
    h, x = k.h, 380
    by = D - O + h
    return [S(P().M(x, X).L(x, -10).C(x, D + 70, x - 50, by, x - 150, by).L(L + 20, by)), k.line(170, X - h, x, X - h), k.dot(x, X + 175)]

@glyph('l')
def _(k):
    h, x = k.h, 270
    return [S(P().M(x, A).L(x, 200).C(x, 70, x + 50, h, x + 140, h).L(R, h)), k.line(100, A - h, x, A - h)]

@glyph('f')
def _(k):
    h, x = k.h, 250
    return [S(P().M(x, 0).L(x, A - 200).C(x, A - 70, x + 60, A - h, x + 160, A - h).L(R - 10, A - h)), k.line(L + 20, X - h, R - 40, X - h, .9)]

@glyph('t')
def _(k):
    h, x = k.h, 250
    return [S(P().M(x, X + 160).L(x, 200).C(x, 70, x + 60, h, x + 160, h).L(R - 10, h)), k.line(L + 20, X - h, R - 40, X - h, .9)]

@glyph('r')
def _(k):
    x = 175
    return [k.line(x, 0, x, X), rband(k, x - k.h, R - 15)]

@glyph('k')
def _(k):
    l = k.l
    return [k.line(l, 0, l, A), k.line(R + 15, X + 70, l, 170, clip=(0, -99, ADV, X)), k.line(230, 330, R + 25, -80, clip=(0, 0, ADV, 999))]

@glyph('v')
def _(k): return [S(P().M(L - 25, X + 60).L(MID, 12).L(R + 25, X + 60), clip=(0, 0, ADV, X))]

@glyph('w')
def _(k): return [S(P().M(L - 15, X + 50).L(170, 8).L(MID, X - 170).L(430, 8).L(R + 15, X + 50), .8, clip=(0, 0, ADV, X))]

@glyph('x')
def _(k):
    c = (0, 0, ADV, X)
    return [k.line(L - 15, X + 40, R + 15, -40, clip=c), k.line(R + 15, X + 40, L - 15, -40, clip=c)]

@glyph('y')
def _(k):
    h, (x0, y0), (x1, y1) = k.h, (R + 25, X + 60), (215, D + k.h)
    at = lambda y: x0 + (x1 - x0) * (y - y0) / (y1 - y0)  # right arm centerline x at height y
    return [k.line(L - 25, X + 60, at(30), 30, clip=(0, -99, ADV, X)), S(P().M(x0, y0).L(x1, y1).L(L + 15, y1), clip=(0, -999, ADV, X))]

@glyph('z')
def _(k):
    h = k.h
    return [k.line(L + 20, X - h, R - 15, X - h, .9), k.line(L + 10, h, R - 5, h, .9), k.line(R - 25, X - h, L + 25, h, clip=(L + 10, 0, R - 15, X))]
