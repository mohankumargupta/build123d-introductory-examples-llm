# 21. Copying Workplanes

from build123d import *

width = 10.0
length = 60.0

with BuildPart() as ex21:
    with BuildSketch() as ex21_sk:
        Circle(width / 2)
    extrude(amount=length)
    with BuildSketch(Plane(origin=ex21.part.center(), z_dir=(-1, 0, 0))):
        Circle(width / 2)
    extrude(amount=length)

part = ex21.part
# Volume: 9091.44462742117 mm^3
