# 3. An extruded prismatic solid

from build123d import *

length = 80.0
width = 60.0
thickness = 10.0

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        Circle(width)
        Rectangle(length / 2, width / 2, mode=Mode.SUBTRACT)
    extrude(amount=2 * thickness)

part = ex3.part