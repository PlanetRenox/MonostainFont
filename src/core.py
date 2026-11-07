# Monostain draws every glyph as centerlines, then Skia strokes them at the weight's width and unions the result.
# So weights only differ in stroke width, and every glyph keeps the same outer edges, metrics and 600 unit advance.
import math, pathops
from pathops import LineCap, LineJoin, PathOp

UPM, ADV = 1000, 600
X, C, A, D, O = 550, 730, 770, -230, 10  # x-height, cap height, ascender, descender, overshoot of rounds
L, R, CL, CR, MID = 70, 530, 60, 540, 300  # outer edges: lowercase and figures, capitals, center

G = {}  # char -> glyph function taking a K and returning parts
def glyph(*cs):
    def d(f):
        for c in cs: G[c] = f
        return f
    return d

class P(list):
    """Chainable path: P().M(x, y).L(x, y).C(x1, y1, x2, y2, x, y).Z()"""
    def M(s, x, y): s.append(('M', x, y)); return s
    def L(s, x, y): s.append(('L', x, y)); return s
    def C(s, a, b, c, d, x, y): s.append(('C', a, b, c, d, x, y)); return s
    def Z(s): s.append(('Z',)); return s
    def cub(s, q): return s.C(*q[1], *q[2], *q[3])  # append a cubic given as 4 points, its start is the current point

class S:
    """Stroke a centerline: wf scales the weight's width, clip keeps only the part inside (x0, y0, x1, y1)"""
    def __init__(s, p, wf=1, clip=None, cap=LineCap.BUTT_CAP, join=LineJoin.MITER_JOIN): s.p, s.wf, s.clip, s.cap, s.join = p, wf, clip, cap, join

class F:
    """Fill a closed outline as is"""
    def __init__(s, p, clip=None): s.p, s.clip, s.wf = p, clip, 1

def tf(parts, f, wf=1):
    """Copy parts through a point transform f(x, y) -> (x, y), optionally scaling stroke width"""
    def mp(p):
        q = P()
        for c in p: q.append((c[0], *[v for i in range(1, len(c), 2) for v in f(c[i], c[i + 1])]))
        return q
    def cl(b):
        if not b: return b
        (x0, y0), (x1, y1) = f(b[0], b[1]), f(b[2], b[3])
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
    out = []
    for t in parts:
        n = S(mp(t.p), t.wf * wf, cl(t.clip), t.cap, t.join) if isinstance(t, S) else F(mp(t.p), cl(t.clip))
        out.append(n)
    return out

move = lambda parts, dx=0, dy=0: tf(parts, lambda x, y: (x + dx, y + dy))
mirror = lambda parts, cx=MID: tf(parts, lambda x, y: (2 * cx - x, y))
flip = lambda parts, cy: tf(parts, lambda x, y: (x, 2 * cy - y))
rot = lambda parts, cy, cx=MID: tf(parts, lambda x, y: (2 * cx - x, 2 * cy - y))
scale = lambda parts, s, ox=MID, oy=0, dx=0, dy=0, wf=1: tf(parts, lambda x, y: (ox + (x - ox) * s + dx, oy + (y - oy) * s + dy), wf)

def split(q, t):
    """Split cubic q (4 points) at t, returning both halves"""
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a, b, c = lerp(q[0], q[1]), lerp(q[1], q[2]), lerp(q[2], q[3])
    d, e = lerp(a, b), lerp(b, c)
    f = lerp(d, e)
    return (q[0], a, d, f), (f, e, c, q[3])

def sub(q, t0, t1):
    """Part of cubic q between t0 and t1"""
    if t1 < 1: q = split(q, t1)[0]
    return split(q, t0 / t1)[1] if t0 > 0 else q

class Ov:
    """Superellipse centerline inside outer bounds: straight sides, quarter curves q[0..3] counter-clockwise from the right"""
    K = .6  # handle length, .552 is a circle, higher is squarer
    def __init__(s, k, x0, y0, x1, y1, f=1.15):
        h = k.h
        s.cx, s.cy, s.rx, s.ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 - h, (y1 - y0) / 2 - h
        cr = min(s.ry, s.rx * f)  # vertical radius of the corners, the rest of the height is straight sides
        s.sy = s.ry - cr
        cx, cy, rx, ry, sy, K = s.cx, s.cy, s.rx, s.ry, s.sy, s.K
        s.q = [((cx + rx, cy + sy), (cx + rx, cy + sy + cr * K), (cx + rx * K, cy + ry), (cx, cy + ry)),
               ((cx, cy + ry), (cx - rx * K, cy + ry), (cx - rx, cy + sy + cr * K), (cx - rx, cy + sy)),
               ((cx - rx, cy - sy), (cx - rx, cy - sy - cr * K), (cx - rx * K, cy - ry), (cx, cy - ry)),
               ((cx, cy - ry), (cx + rx * K, cy - ry), (cx + rx, cy - sy - cr * K), (cx + rx, cy - sy))]
    def path(s):
        q = s.q
        return P().M(*q[3][3]).L(*q[0][0]).cub(q[0]).cub(q[1]).L(*q[2][0]).cub(q[2]).cub(q[3]).Z()

class K:
    """Drawing kit for one stroke width"""
    def __init__(s, w):
        s.w, s.h = w, w / 2
        s.l, s.r, s.cl, s.cr = L + s.h, R - s.h, CL + s.h, CR - s.h  # stem centerlines
        s.dr = 26 + w * .38  # dot radius, grows slower than the stroke so bold dots stay compact
    def ov(s, *b, f=1.15): return Ov(s, *b, f=f)
    def oval(s, *b, f=1.15): return S(Ov(s, *b, f=f).path())
    def dot(s, x, y, r=None):
        r, k = r or s.dr, .5523 * (r or s.dr)
        return F(P().M(x + r, y).C(x + r, y + k, x + k, y + r, x, y + r).C(x - k, y + r, x - r, y + k, x - r, y)
                 .C(x - r, y - k, x - k, y - r, x, y - r).C(x + k, y - r, x + r, y - k, x + r, y).Z())
    def pill(s, cx, cy, w, h):
        r = w / 2
        k = .5523 * r
        b, t = cy - h / 2 + r, cy + h / 2 - r
        return F(P().M(cx + r, b).L(cx + r, t).C(cx + r, t + k, cx + k, t + r, cx, t + r).C(cx - k, t + r, cx - r, t + k, cx - r, t)
                 .L(cx - r, b).C(cx - r, b - k, cx - k, b - r, cx, b - r).C(cx + k, b - r, cx + r, b - k, cx + r, b).Z())
    def line(s, x0, y0, x1, y1, wf=1, clip=None): return S(P().M(x0, y0).L(x1, y1), wf, clip)

def rev(p):
    """Reverse an open M/L/C path"""
    segs, cur = [], None
    for c in p:
        if c[0] == 'M': cur = c[1:]
        else: segs.append((cur, c)); cur = c[-2:]
    q = P().M(*cur)
    for st, c in reversed(segs): q.L(*st) if c[0] == 'L' else q.C(c[3], c[4], c[1], c[2], *st)
    return q

def band(outer, inner):
    """Fill between two paths drawn in the same direction, for joins a single stroke width can't draw"""
    p = P(outer); p.L(*inner[-1][-2:]); p.extend(rev(inner)[1:])
    return F(p.Z())

def rect(x0, y0, x1, y1):
    p = pathops.Path()
    p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
    return p

def skpath(cmds):
    p = pathops.Path()
    for c in cmds:
        if c[0] == 'M': p.moveTo(*c[1:])
        elif c[0] == 'L': p.lineTo(*c[1:])
        elif c[0] == 'C': p.cubicTo(*c[1:])
        else: p.close()
    return p

def outline(parts, k):
    """Union of all parts as one Skia path: each part is normalised first, so the direction it was drawn in doesn't matter"""
    acc = pathops.Path()
    for t in parts:
        g = skpath(t.p)
        if isinstance(t, S): g.stroke(k.w * t.wf, t.cap, t.join, 4)
        if t.clip: g = pathops.op(g, rect(*t.clip), PathOp.INTERSECTION)
        g.simplify(fix_winding=True)
        acc.addPath(g)
    acc.simplify(fix_winding=True)
    return acc
