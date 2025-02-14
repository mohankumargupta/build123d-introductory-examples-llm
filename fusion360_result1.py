import adsk.core
import adsk.fusion
import traceback
from typing import Optional, Tuple

# Helper function to convert units from build123d (mm) to Fusion 360 (cm)
def mm_to_cm(value: float) -> float:
    return value / 10.0

# Parameters copied verbatim from build123d scripts
# From example-01.py
length_01 = 80.0
width_01 = 60.0
thickness_01 = 10.0
volume_01 = 48000.0

# From example-02.py
length_02 = 80.0
width_02 = 60.0
thickness_02 = 10.0
center_hole_dia_02 = 22.0
volume_02 = 44198.67288915635

# From example-03.py
length_03 = 80.0
width_03 = 60.0
thickness_03 = 10.0
volume_03 = 202194.6710584651

def create_rectangular_plate(component: adsk.fusion.Component) -> None:
    length = mm_to_cm(length_01)
    width = mm_to_cm(width_01)
    thickness = mm_to_cm(thickness_01)

    # Create a rectangular box
    sketches = component.sketches
    xy_plane = component.xYConstructionPlane
    sketch = sketches.add(xy_plane)
    lines = sketch.sketchCurves.sketchLines
    rectangle = lines.addTwoPointRectangle(adsk.core.Point3D.create(-length / 2, -width / 2, 0),
                                           adsk.core.Point3D.create(length / 2, width / 2, 0))

    extrudes = component.features.extrudeFeatures
    profile = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(thickness)
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    extrudes.add(extrude_input)

def create_plane_with_hole(component: adsk.fusion.Component) -> None:
    length = mm_to_cm(length_02)
    width = mm_to_cm(width_02)
    thickness = mm_to_cm(thickness_02)
    center_hole_dia = mm_to_cm(center_hole_dia_02)

    # Create a rectangular box
    sketches = component.sketches
    xy_plane = component.xYConstructionPlane
    sketch = sketches.add(xy_plane)
    lines = sketch.sketchCurves.sketchLines
    rectangle = lines.addTwoPointRectangle(adsk.core.Point3D.create(-length / 2, -width / 2, 0),
                                           adsk.core.Point3D.create(length / 2, width / 2, 0))

    extrudes = component.features.extrudeFeatures
    profile = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(thickness)
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    extrudes.add(extrude_input)

    # Create a hole in the center
    hole_sketch = sketches.add(xy_plane)
    circles = hole_sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), center_hole_dia / 2)

    hole_profile = hole_sketch.profiles.item(0)
    hole_distance = adsk.core.ValueInput.createByReal(thickness)
    hole_input = extrudes.createInput(hole_profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    hole_input.setDistanceExtent(False, hole_distance)
    extrudes.add(hole_input)

def create_extruded_prismatic_solid(component: adsk.fusion.Component) -> None:
    length = mm_to_cm(length_03)
    width = mm_to_cm(width_03)
    thickness = mm_to_cm(thickness_03)

    # Create a circle with a rectangle subtracted
    sketches = component.sketches
    xy_plane = component.xYConstructionPlane
    sketch = sketches.add(xy_plane)
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), width / 2)

    lines = sketch.sketchCurves.sketchLines
    rectangle = lines.addTwoPointRectangle(adsk.core.Point3D.create(-length / 4, -width / 4, 0),
                                           adsk.core.Point3D.create(length / 4, width / 4, 0))

    extrudes = component.features.extrudeFeatures
    profile = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(2 * thickness)
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    extrudes.add(extrude_input)

def calculate_volume(body: adsk.fusion.BRepBody) -> float:
    return body.volume * 1000  # Convert cm^3 to mm^3

def run(context):
    ui: Optional[adsk.core.UserInterface] = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # Create components for each example
        root_comp = design.rootComponent
        comp_01 = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        comp_02 = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        comp_03 = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component

        # Call functions for each example
        create_rectangular_plate(comp_01)
        create_plane_with_hole(comp_02)
        create_extruded_prismatic_solid(comp_03)

        # Compare volumes
        bodies_01 = comp_01.bRepBodies
        bodies_02 = comp_02.bRepBodies
        bodies_03 = comp_03.bRepBodies

        fusion_volume_01 = calculate_volume(bodies_01.item(0))
        fusion_volume_02 = calculate_volume(bodies_02.item(0))
        fusion_volume_03 = calculate_volume(bodies_03.item(0))

        if fusion_volume_01 != volume_01:
            ui.messageBox(f"Volume mismatch in example-01.py:\nBuild123d: {volume_01} mm^3\nFusion 360: {fusion_volume_01} mm^3")
        if fusion_volume_02 != volume_02:
            ui.messageBox(f"Volume mismatch in example-02.py:\nBuild123d: {volume_02} mm^3\nFusion 360: {fusion_volume_02} mm^3")
        if fusion_volume_03 != volume_03:
            ui.messageBox(f"Volume mismatch in example-03.py:\nBuild123d: {volume_03} mm^3\nFusion 360: {fusion_volume_03} mm^3")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))