# This is a little Python program which runs inside the font builder.
# We get access to a number of functions, starting in "Paint...",
# which create the paint tables, and the font builder expects us
# to set up a dictionary called `glyphs` which maps glyph names to
# paint definitions.

# To understand what paint tables are available and their parameters,
# you need to read https://github.com/googlefonts/colr-gradients-spec/blob/main/OFF_AMD2_WD.md

# The paint builder will automatically set up the palettes for us;
# we can just call "PaintSolid" and "PaintLinearGradient" etc.
# with colour strings and it'll sort it out. We define constants here
# to make the code tidier.
RED = "#FF141DFF"
ORANGE = "#FB7236FF"
LOW_GREEN = "#14FF1D22"
HIGH_GREEN = "#72FB3655"
LOW_BLUE = "#141DFF55"
HIGH_BLUE = "#7236FB55"

# A little wrapper to make defining our three gradients easier
def grad(start, mid):
    return PaintLinearGradient(
        (512, 0),  # Start gradient at middle, baseline
        (512, 900),  # End gradient at middle, top
        (0, 0),  # Rotate gradient 90 degrees
        ColorLine({0: start, 0.25: mid, 1: start})
        # Go from the start colour to the mid colour at 25% and
        # back to the start again
    )


# And another wrapper encoding our skew constants
def skew(paint):
    return PaintVarSkewAroundCenter(
        0,  # X axis skew
        "XSEP=-50:-4 XSEP=0:0 XSEP=50:4",  # Y axis skew
        # "At XSEP=-50, skew the Y axis -4 degrees; at XSEP=50, skew
        # it 4 degrees"
        (512, 450),  # skew around the center of the glyph
        paint,  # dispatch to the next paint table
    )


# We also have access to the font object, so we can get all the glyph
# names
for gname in font.getGlyphOrder():
    # Now we are going to compose three copies of the base glyph
    # together using the "screen" composition mode.

    # The frontmost copy is the base glyph painted in a
    # blue gradient, skewed a few degrees, and then translated
    # according to the values of the XSEP and YSEP axes.
    foreground = PaintVarTranslate(
        "XSEP=-50:100 XSEP=0:0 XSEP=50:-100",
        "YSEP=-50:110 YSEP=0:0 YSEP=50:-110",
        skew(
            PaintGlyph(gname, grad(LOW_BLUE, HIGH_BLUE)),
        ),
    )

    # The second copy is the base glyph itself painted in a
    # red-orange-red gradient, skewed a few degrees, but
    # not translated.
    middle = skew(PaintGlyph(gname, grad(RED, ORANGE)))

    # And the back layer, the background of our inner
    # composition, is the base glyph again painted in a
    # green gradient, skewed, and moved in the opposite
    # direction on the XSEP/YSEP axes.
    background = PaintVarTranslate(
        "XSEP=-50:-110 XSEP=0:0 XSEP=50:110",
        "YSEP=-50:-100 YSEP=0:0 YSEP=50:100",
        skew(
            PaintGlyph(gname, grad(LOW_GREEN, HIGH_GREEN)),
        ),
    )

    # Now we create the composition. Since we have three layers
    # and "PaintComposite" takes a foreground and a background,
    # we do two compositing operations and feed the second as
    # the background to the first.
    glyphs[gname] = PaintComposite(
        "screen", foreground, PaintComposite("screen", middle, background)
    )
