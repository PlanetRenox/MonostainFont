from .core import *

def dbowl(k, x0, x1, y0, y1, rr=None):
    """D-shaped centerline from (x0, y1) right, round down the right side and back left to (x0, y0)"""
    r = min(rr or 1e9, (y1 - y0) / 2, x1 - x0)
    return P().M(x0, y1).L(x1 - r, y1).C(x1 - r + r * Ov.K, y1, x1, y1 - r + r * Ov.K, x1, y1 - r).L(x1, y0 + r) \
              .C(x1, y0 + r - r * Ov.K, x1 - r + r * Ov.K, y0, x1 - r, y0).L(x0, y0)

CAP = (0, 0, ADV, C)

@glyph('A')
def _(k):
    h, t = k.h, C + 120
    leg = lambda y: CL - 20 + (MID - CL + 20) * (y + 60) / (t + 60)  # left leg centerline x at height y
    return [S(P().M(CL - 20, -60).L(MID, t).L(CR + 20, -60), clip=CAP), k.line(leg(230), 230, 2 * MID - leg(230), 230, .9)]

@glyph('B')
def _(k):
    h, l, r, ym = k.h, k.cl, k.cr, 400
    return [k.line(l, 0, l, C), S(dbowl(k, l, r - 30, ym, C - h, 170)), S(dbowl(k, l, r, h, ym, 190))]

@glyph('C')
def _(k):
    q = k.ov(CL, -O, CR, C + O).q
    a = sub(q[0], .42, 1)
    return [S(P().M(*a[0]).cub(a).cub(q[1]).L(*q[2][0]).cub(q[2]).cub(sub(q[3], 0, .58)))]

@glyph('D')
def _(k): return [k.line(k.cl, 0, k.cl, C), S(dbowl(k, k.cl, k.cr, k.h, C - k.h, 230))]

@glyph('E')
def _(k):
    h, l = k.h, k.cl
    return [k.line(l, 0, l, C), k.line(l, C - h, CR - 15, C - h, .9), k.line(l, 395, CR - 45, 395, .9), k.line(l, h, CR, h, .9)]

@glyph('F')
def _(k): return G['E'](k)[:3]

@glyph('G')
def _(k):
    o = k.ov(CL, -O, CR, C + O)
    q, yb = o.q, 330
    a = sub(q[0], .42, 1)
    return [S(P().M(*a[0]).cub(a).cub(q[1]).L(*q[2][0]).cub(q[2]).cub(q[3]).L(k.cr, yb)), k.line(MID + 20, yb, k.cr, yb, .9)]

@glyph('H')
def _(k): return [k.line(k.cl, 0, k.cl, C), k.line(k.cr, 0, k.cr, C), k.line(k.cl, 390, k.cr, 390, .9)]

@glyph('I')
def _(k): return [k.line(MID, 0, MID, C), k.line(120, C - k.h, 480, C - k.h, .9), k.line(120, k.h, 480, k.h, .9)]

@glyph('J')
def _(k):
    h, x = k.h, k.cr - 15
    by = -O + h
    return [S(P().M(x, C).L(x, 230).C(x, 80, x - 80, by, MID - 20, by).C(MID - 130, by, CL + 30, by + 50, CL + 20, 170)), k.line(170, C - h, x, C - h, .9)]

@glyph('K')
def _(k):
    l = k.cl
    return [k.line(l, 0, l, C), k.line(CR + 20, C + 80, l, 250, clip=(0, -99, ADV, C)), k.line(225, 450, CR + 30, -90, clip=(0, 0, ADV, 999))]

@glyph('L')
def _(k): return [k.line(k.cl, 0, k.cl, C), k.line(k.cl, k.h, CR - 5, k.h, .9)]

@glyph('M')
def _(k):
    wf = .86
    a, b = CL + k.h * wf, CR - k.h * wf
    return [S(P().M(a, 0).L(a, C + 60).L(MID, 260).L(b, C + 60).L(b, 0), wf, clip=CAP)]

@glyph('N')
def _(k): return [S(P().M(k.cl, 0).L(k.cl, C + 99).L(k.cr, -99).L(k.cr, C), clip=CAP)]

@glyph('O')
def _(k): return [k.oval(CL, -O, CR, C + O)]

@glyph('P')
def _(k): return [k.line(k.cl, 0, k.cl, C), S(dbowl(k, k.cl, k.cr, 330, C - k.h, 200))]

@glyph('Q')
def _(k): return G['O'](k) + [k.line(MID + 15, 130, MID + 125, -180, 1, (0, -180, ADV, C))]

@glyph('R')
def _(k): return G['P'](k) + [k.line(270, 330, CR + 30, -100, clip=(0, 0, ADV, C))]

@glyph('S')
def _(k):
    h, xl, xr = k.h, k.cl, k.cr
    ty, by, cy = C + O - h, -O + h, C / 2 + 10
    yl, yr = (cy + ty) / 2 + 10, (cy + by) / 2 - 10
    return [S(P().M(xr + 5, C - 150).C(xr - 15, ty - 25, MID + 100, ty, MID, ty)
                 .C(MID - (MID - xl) * Ov.K, ty, xl, yl + (ty - yl) * Ov.K, xl, yl)
                 .C(xl, yl - 110, MID - 130, cy + 45, MID, cy).C(MID + 130, cy - 45, xr, yr + 110, xr, yr)
                 .C(xr, yr - (yr - by) * Ov.K, MID + (xr - MID) * Ov.K, by, MID, by).C(MID - 115, by, xl, by + 45, xl, 165))]

@glyph('T')
def _(k): return [k.line(MID, 0, MID, C), k.line(CL, C - k.h, CR, C - k.h, .9)]

@glyph('U')
def _(k):
    q = k.ov(CL, -O, CR, C + O, f=1).q
    return [S(P().M(k.cl, C).L(*q[2][0]).cub(q[2]).cub(q[3]).L(k.cr, C))]

@glyph('V')
def _(k): return [S(P().M(CL - 25, C + 80).L(MID, 15).L(CR + 25, C + 80), clip=CAP)]

@glyph('W')
def _(k): return [S(P().M(CL - 10, C + 60).L(165, 10).L(MID, C - 290).L(435, 10).L(CR + 10, C + 60), .82, clip=CAP)]

@glyph('X')
def _(k): return [k.line(CL - 15, C + 50, CR + 15, -50, clip=CAP), k.line(CR + 15, C + 50, CL - 15, -50, clip=CAP)]

@glyph('Y')
def _(k): return [S(P().M(CL - 25, C + 75).L(MID, 330).L(CR + 25, C + 75), clip=CAP), k.line(MID, 0, MID, 340)]

@glyph('Z')
def _(k):
    h = k.h
    return [k.line(CL + 15, C - h, CR - 10, C - h, .9), k.line(CL + 5, h, CR, h, .9), k.line(CR - 25, C - h, CL + 25, h, clip=(CL + 5, 0, CR - 10, C))]
