from lottie2vf.paintcompiler import compile_paints
from fontTools.ttLib import TTFont
from fontTools.fontBuilder import addFvar
from fontmake.font_project import FontProject

# Python version of `fontmake -o ttf -g Parallax.glyphs`
FontProject().run_from_glyphs("Parallax.glyphs", output=["ttf"])

font = TTFont("master_ttf/Parallax-Regular.ttf")

print("Adding axes...")
addFvar(font, [
	("XSEP", -50, 0, 50, "X separation"),
	("YSEP", -50, 0, 50, "Y separation"),
], [])


print("Adding paints...")
compile_paints(font, open("paints.py").read())

print("Saving...")
font.save("master_ttf/Parallax-VF.ttf")
print("master_ttf/Parallax-VF.ttf")
