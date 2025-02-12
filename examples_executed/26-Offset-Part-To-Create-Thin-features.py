from build123d import *

length = 80.0
width = 60.0
thickness = 10.0
wall = 2.0

with BuildPart() as ex26:
    Box(length, width, thickness)
    topf = ex26.faces().sort_by(Axis.Z)[-1]
    offset(amount=-wall, openings=topf)

part = ex26.part
# Volume: 13952.0 mm^3
