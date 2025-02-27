# 17. Mirroring From Faces

from build123d import *

a = 30
b = 20

with BuildPart() as ex17:
    with BuildSketch() as ex17_sk:
        RegularPolygon(radius=a, side_count=5)
    extrude(amount=b)
    mirror(ex17.part, about=Plane(ex17.faces().group_by(Axis.Y)[0][0]))

part = ex17.part
# Volume: 85595.0864665638 mm^3
