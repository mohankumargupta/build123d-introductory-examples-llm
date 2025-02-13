# 27. Splitting an Object

from build123d import *

length = 80.0
width = 60.0
thickness = 10.0

with BuildPart() as ex27:
    Box(length, width, thickness)
    with BuildSketch(ex27.faces().sort_by(Axis.Z)[0]) as ex27_sk:
        Circle(width / 4)
    extrude(amount=-thickness, mode=Mode.SUBTRACT)
    split(bisect_by=Plane(ex27.faces().sort_by(Axis.Y)[-1]).offset(-width / 2))

part = ex27.part
# Volume: 20465.708264711477 mm^3
