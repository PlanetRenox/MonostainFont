# /// script
# requires-python = ">=3.10"
# dependencies = ["fonttools[woff]>=4.50", "skia-pathops>=0.8"]
# ///
# uv run build.py  ->  dist/Monostain-{Regular,Bold,Italic,BoldItalic}.{otf,ttf,woff2}, dist/Monostain.zip,
#                      dist/chars.txt (every character, for the site) and favicon.svg
import math, os, zipfile
from functools import cache
from fontTools import agl
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from src.core import G, K, UPM, ADV, X, C, outline, rect
from src import lower, upper, figures, symbols, marks  # register glyphs

VERSION, RELEASED = '1.000', 1794009600  # release time, unix seconds, so rebuilds are byte identical
ASC, DESC = 1020, -300
SLANT = 10  # italic angle in degrees
STYLES = [('Regular', 80, 0), ('Bold', 128, 0), ('Italic', 80, SLANT), ('Bold Italic', 128, SLANT)]
URL = 'https://github.com/PlanetRenox/MonostainFont'
LICENSE = 'This font is dedicated to the public domain under CC0 1.0 Universal. You may use, modify and distribute it for any purpose without permission or attribution.'

name = lambda c: agl.UV2AGL.get(ord(c), f'uni{ord(c):04X}')

def notdef(k):
    """Hollow box for characters the font lacks"""
    inner = rect(70 + k.w, k.w, 530 - k.w, C - k.w); inner.reverse()
    out = rect(70, 0, 530, C); out.addPath(inner)
    return out

@cache
def drawings(w, slant):
    """Recorded outlines per glyph name, contours counter-clockwise (outer) as CFF wants"""
    k, t, out = K(w), math.tan(math.radians(slant)), {}
    for n, f in [('.notdef', notdef)] + [(name(c), (lambda k, c=c: outline(G[c](k), k))) for c in sorted(G, key=ord)]:
        p = f(k)
        if slant: p = p.transform(1, 0, t, 1, -t * X / 2, 0)  # shear around half the x-height so glyphs stay centered
        p.convertConicsToQuads()
        rec, a = RecordingPen(), AreaPen()
        p.draw(rec); rec.replay(a)
        if a.value < 0:
            r = RecordingPen(); rec.replay(ReverseContourPen(r)); rec = r
        out[n] = rec
    return out

def build(style, w, slant, ttf):
    ps = style.replace(' ', '')
    recs = drawings(w, slant)
    order = list(recs)
    cmap = {ord(c): name(c) for c in G}
    fb = FontBuilder(UPM, isTTF=ttf)
    fb.font.recalcTimestamp = False
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    full = f'Monostain {style}'
    if ttf:
        glyphs = {}
        for n, rec in recs.items():
            pen = TTGlyphPen(None)
            rec.replay(Cu2QuPen(ReverseContourPen(pen), max_err=1, reverse_direction=False))  # TrueType wants clockwise outers
            glyphs[n] = pen.glyph()
        fb.setupGlyf(glyphs)
        lsb = {n: fb.font['glyf'][n].xMin if hasattr(fb.font['glyf'][n], 'xMin') else 0 for n in order}
    else:
        cs = {}
        for n, rec in recs.items():
            pen = T2CharStringPen(ADV, None)
            rec.replay(pen)
            cs[n] = pen.getCharString()
        fb.setupCFF(f'Monostain-{ps}', {'FullName': full, 'FamilyName': 'Monostain', 'Weight': 'Bold' if w > 100 else 'Regular',
                                        'isFixedPitch': True, 'ItalicAngle': -slant, 'version': VERSION}, cs, {})
        lsb = {}
        for n, rec in recs.items():
            b = BoundsPen(None); rec.replay(b)
            lsb[n] = round(b.bounds[0]) if b.bounds else 0
    fb.setupHorizontalMetrics({n: (ADV, lsb[n]) for n in order})
    fb.setupHorizontalHeader(ascent=ASC, descent=DESC)
    fb.setupNameTable({
        'familyName': 'Monostain', 'styleName': style, 'uniqueFontIdentifier': f'Monostain-{ps} {VERSION}', 'fullName': full,
        'psName': f'Monostain-{ps}', 'version': f'Version {VERSION}', 'manufacturer': 'Planet Renox', 'designer': 'Planet Renox',
        'description': 'Monostain is a free, programmatic monospace font inspired by JetBrains Mono, from the Stain family.',
        'copyright': 'Dedicated to the public domain by Planet Renox under CC0 1.0 Universal.', 'vendorURL': URL, 'designerURL': URL,
        'licenseDescription': LICENSE, 'licenseInfoURL': 'https://creativecommons.org/publicdomain/zero/1.0/'})
    bold, italic = w > 100, slant != 0
    ys = []
    for rec in recs.values():
        b = BoundsPen(None); rec.replay(b)
        if b.bounds: ys += [b.bounds[1], b.bounds[3]]
    fb.setupOS2(version=4, usWeightClass=700 if bold else 400, xAvgCharWidth=ADV, achVendID='PLRX', sxHeight=X, sCapHeight=C,
                sTypoAscender=ASC, sTypoDescender=DESC, sTypoLineGap=0, usWinAscent=max(ASC, math.ceil(max(ys))),
                usWinDescent=max(-DESC, math.ceil(-min(ys))), fsType=0, ulCodePageRange1=1,
                fsSelection=(1 if italic else 0) | (32 if bold else 0) | (64 if not (bold or italic) else 0) | 128)
    os2 = fb.font['OS/2']
    os2.panose.bFamilyType, os2.panose.bProportion, os2.panose.bWeight = 2, 9, 8 if bold else 5
    os2.panose.bLetterForm = 9 if italic else 2
    fb.setupPost(isFixedPitch=1, italicAngle=-slant, underlinePosition=-150, underlineThickness=round(w * .75))
    head = fb.font['head']
    head.macStyle = (1 if bold else 0) | (2 if italic else 0)
    head.fontRevision = float(VERSION)
    head.created = head.modified = RELEASED + 2082844800  # head counts seconds from 1904
    os2.recalcUnicodeRanges(fb.font)
    return fb.font

def favicon():
    """Bold m from the font itself, centred white on a dark rounded square"""
    rec, pen, bp = drawings(128, 0)[name('m')], SVGPathPen(None, ntos=lambda v: f'{v:g}' if v == int(v) else f'{v:.1f}'), BoundsPen(None)
    rec.replay(TransformPen(pen, (1, 0, 0, -1, 0, 0)))  # font y points up, svg y down
    rec.replay(bp)
    x0, y0, x1, y1 = bp.bounds
    cx, cy, s = (x0 + x1) / 2, -(y0 + y1) / 2, max(x1 - x0, y1 - y0) * 1.5
    v = f'{cx - s / 2:.0f} {cy - s / 2:.0f} {s:.0f} {s:.0f}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{v}"><rect x="{cx - s / 2:.0f}" y="{cy - s / 2:.0f}" width="{s:.0f}" height="{s:.0f}" rx="{s * .21:.0f}" fill="#141414"/>'
            f'<path fill="#f7f7f5" d="{pen.getCommands()}"/></svg>\n')

def bundle(files):
    """Zip of the desktop fonts and license, timestamps pinned so the zip is reproducible too"""
    with zipfile.ZipFile('dist/Monostain.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            i = zipfile.ZipInfo(f'Monostain/{os.path.basename(f)}', (2026, 11, 7, 0, 0, 0))
            i.compress_type, i.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
            z.writestr(i, open(f, 'rb').read())

if __name__ == '__main__':
    os.makedirs('dist', exist_ok=True)
    desktop = []
    for style, w, slant in STYLES:
        ps = style.replace(' ', '')
        for ttf, ext in ((False, 'otf'), (True, 'ttf')):
            f = build(style, w, slant, ttf)
            f.save(path := f'dist/Monostain-{ps}.{ext}')
            desktop.append(path)
            if not ttf:
                f.flavor = 'woff2'
                f.save(f'dist/Monostain-{ps}.woff2')
        print(f'Built Monostain {style}: {len(G)} characters')
    bundle(sorted(desktop) + ['LICENSE'])
    open('dist/chars.txt', 'w').write(''.join(c for c in sorted(G, key=ord) if c.isprintable() and not c.isspace() and c != '\u00ad'))
    open('favicon.svg', 'w').write(favicon())
