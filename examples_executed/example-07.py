# 7. Polygons

from build123d import *

a = 60
b = 80
c = 5

with BuildPart() as ex7:
    with BuildSketch() as ex7_sk:
        Rectangle(a, b)
        with Locations((0, 3 * c), (0, -3 * c)):
            RegularPolygon(radius=2 * c, side_count=6, mode=Mode.SUBTRACT)
    extrude(amount=c)

part = ex7.part
# Volume: 21401.923788646673 mm^3
