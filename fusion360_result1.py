import adsk.core
import adsk.fusion
import traceback
from typing import Optional

# Helper function to convert build123d units to Fusion 360 units (mm -> cm)
def convert_units(value: float) -> float:
    return value / 10.0  # Convert mm to cm

# Function to calculate volume in mm^3
def calculate_volume(root_comp: adsk.fusion.Component) -> float:
    return root_comp.bRepBodies.item(0).volume * 1000  # Convert cm^3 to mm^3

# Parameters from build123d scripts
length_1 = 80.0
width_1 = 60.0
thickness_1 = 10.0
center_hole_dia_2 = 22.0

# Function for example-01.py: Simple Rectangular Plate
def create_simple_rectangular_plate(root_comp: adsk.fusion.Component) -> None:
    # Create a new sketch on the XY plane
    sketches = root_comp.sketches
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw a rectangle
    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(-convert_units(length_1) / 2, -convert_units(width_1) / 2, 0),
        adsk.core.Point3D.create(convert_units(length_1) / 2, convert_units(width_1) / 2, 0)
    )

    # Extrude the rectangle to create a box
    extrudes = root_comp.features.extrudeFeatures
    profile = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(convert_units(thickness_1))
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setSymmetricExtent(distance, False)
    extrudes.add(extrude_input)

# Function for example-02.py: Plane with Hole
def create_plane_with_hole(root_comp: adsk.fusion.Component) -> None:
    # Create a new sketch on the XY plane
    sketches = root_comp.sketches
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw a rectangle
    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(-convert_units(length_1) / 2, -convert_units(width_1) / 2, 0),
        adsk.core.Point3D.create(convert_units(length_1) / 2, convert_units(width_1) / 2, 0)
    )

    # Extrude the rectangle to create a box
    extrudes = root_comp.features.extrudeFeatures
    profile = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(convert_units(thickness_1))
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setSymmetricExtent(distance, False)
    extrudes.add(extrude_input)

    # Create a hole in the center
    hole_sketch = sketches.add(xy_plane)
    circles = hole_sketch.sketchCurves.sketchCircles
    center = adsk.core.Point3D.create(0, 0, 0)
    radius = convert_units(center_hole_dia_2) / 2
    circle = circles.addByCenterRadius(center, radius)

    # Extrude the hole
    hole_profile = hole_sketch.profiles.item(0)
    hole_distance = adsk.core.ValueInput.createByReal(convert_units(thickness_1))
    hole_extrude_input = extrudes.createInput(hole_profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    hole_extrude_input.setSymmetricExtent(hole_distance, False)
    extrudes.add(hole_extrude_input)

# Main run function
def run(context):
    ui: Optional[adsk.core.UserInterface] = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox("No active Fusion 360 document. Please open or create one.")
            return

        root_comp = design.rootComponent

        # Call each function and calculate volumes
        functions = [create_simple_rectangular_plate, create_plane_with_hole]
        expected_volumes = [48000.0, 44198.67288915635]

        for func, expected_volume in zip(functions, expected_volumes):
            func(root_comp)
            fusion_volume = calculate_volume(root_comp)

            if abs(fusion_volume - expected_volume) > 1e-3:  # Allow small floating-point tolerance
                ui.messageBox(
                    f"Volume mismatch for {func.__name__}:\n"
                    f"Build123d Volume: {expected_volume:.2f} mm^3\n"
                    f"Fusion 360 Volume: {fusion_volume:.2f} mm^3"
                )

            # Cleanup: Delete all bodies and sketches
            for body in root_comp.bRepBodies:
                body.deleteMe()
            for sketch in root_comp.sketches:
                sketch.deleteMe()

    except Exception as e:
        if ui:
            ui.messageBox(f"Failed:\n{traceback.format_exc()}")
