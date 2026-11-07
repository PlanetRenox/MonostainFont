# /// script
# dependencies = ["fonttools", "skia-pathops"]
# ///
# flags glyphs whose union left touching contours (visible seams) or tiny slivers
import sys, itertools; sys.path.insert(0, '.')
import pathops
from src.core import G, K, outline
from src import lower, upper, figures, symbols, marks
def cpath(c):
    p = pathops.Path(); pen = p.getPen()
    for verb, pts in c.segments: getattr(pen, verb)(*pts)
    return p
bad = 0
for w in (80, 128):
    k = K(w)
    for ch, f in sorted(G.items()):
        cs = list(outline(f(k), k).contours)
        for a in cs:
            if abs(a.area) < 400: print(f'{w} {ch!r}: tiny contour, area {a.area:.0f}'); bad += 1
        for i, a in enumerate(cs):
            rest = pathops.Path()
            for j, b in enumerate(cs):
                if j != i: rest.addPath(cpath(b))
            rest.addPath(cpath(a)); rest.simplify(fix_winding=True)
            if len(list(rest.contours)) < len(cs): print(f'{w} {ch!r}: contour merges with others {[round(v) for v in a.bounds]}'); bad += 1
print('issues:', bad)
