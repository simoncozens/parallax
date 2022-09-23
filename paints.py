RED = "#FF141DFF"
ORANGE = "#FB7236FF"
LOW_GREEN = "#14FF1D22"
HIGH_GREEN = "#72FB3655"
LOW_BLUE = "#141DFF55"
HIGH_BLUE = "#7236FB55"


def grad(start, mid):
    return PaintLinearGradient(
        (512, 0), (512, 900), (0, 0), ColorLine({0: start, 0.25: mid, 1: start})
    )


def skew(paint):
    angle = "XSEP=-50:-15 XSEP=0:0 XSEP=50:15"
    return PaintVarSkewAroundCenter(0, angle, (512, 450), paint)


for gname in font.getGlyphOrder():
    base = PaintGlyph(gname, grad(RED, ORANGE))
    glyphs[gname] = PaintComposite(
        "screen",
        PaintVarTranslate(
            "XSEP=-50:100 XSEP=0:0 XSEP=50:-100",
            "YSEP=-50:100 YSEP=0:0 YSEP=50:-100",
            skew(
                PaintGlyph(gname, grad(LOW_BLUE, HIGH_BLUE)),
            ),
        ),
        PaintComposite(
            "screen",
            skew(base),
            PaintVarTranslate(
                "XSEP=-50:-100 XSEP=0:0 XSEP=50:100",
                "YSEP=-50:-100 YSEP=0:0 YSEP=50:100",
                skew(
                    PaintGlyph(gname, grad(LOW_GREEN, HIGH_GREEN)),
                ),
            ),
        ),
    )
