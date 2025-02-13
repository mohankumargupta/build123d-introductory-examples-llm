# 1. Simple Rectangular Plate

from build123d import *

length = 80.0
width = 60.0
thickness = 10.0

with BuildPart() as ex1:
    Box(length, width, thickness)

part = ex1.part
# Volume: 48000.0 mm^3
