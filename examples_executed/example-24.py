# 24. Lofts

from build123d import *

length = 80.0
width = 60.0
thickness = 10.0

with BuildPart() as ex24:
    Box(length, length, thickness)
    with BuildSketch(ex24.faces().group_by(Axis.Z)[0][0]) as ex24_sk:
        Circle(length / 3)
    with BuildSketch(ex24_sk.faces()[0].offset(length / 2)) as ex24_sk2:
        Rectangle(length / 6, width / 6)
    loft()

part = ex24.part
# Volume: 89024.35585088223 mm^3
