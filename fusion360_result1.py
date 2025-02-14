import adsk.core
import adsk.fusion
import math

# Helper function to convert build123d units to Fusion 360 units
def convert_units(value):
    # Assuming build123d uses mm and Fusion 360 uses cm
    return value / 10.0

# Function to calculate the volume of the first body in Fusion 360
def calculate_fusion360_volume(root_comp):
    bodies = root_comp.bRepBodies
    if bodies.count > 0:
        first_body = bodies.item(0)
        return first_body.volume * 1000  # Convert cm³ to mm³ for comparison
    return 0.0

# Function for example_01: Simple Rectangular Plate
def example_01(app, ui, design):
    length = 80.0
    width = 60.0
    thickness = 10.0

    # Convert parameters to Fusion 360 units
    length = convert_units(length)
    width = convert_units(width)
    thickness = convert_units(thickness)

    # Create a rectangular box
    root_comp = design.rootComponent
    sketches = root_comp.sketches
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw rectangle
    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(-length / 2, -width / 2, 0),
                                      adsk.core.Point3D.create(length / 2, width / 2, 0))

    # Extrude the rectangle
    extrudes = root_comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(thickness)
    extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    extrude = extrudes.add(extrude_input)

    # Calculate Fusion 360 volume
    fusion360_volume = calculate_fusion360_volume(root_comp)

    # Close Fusion 360 document
    app.activeDocument.close(False)

    return fusion360_volume

# Function for example_02: Plane with Hole
def example_02(app, ui, design):
    length = 80.0
    width = 60.0
    thickness = 10.0
    center_hole_dia = 22.0

    # Convert parameters to Fusion 360 units
    length = convert_units(length)
    width = convert_units(width)
    thickness = convert_units(thickness)
    center_hole_dia = convert_units(center_hole_dia)

    # Create a rectangular box
    root_comp = design.rootComponent
    sketches = root_comp.sketches
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw rectangle
    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(-length / 2, -width / 2, 0),
                                      adsk.core.Point3D.create(length / 2, width / 2, 0))

    # Extrude the rectangle
    extrudes = root_comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(thickness)
    extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    extrude = extrudes.add(extrude_input)

    # Add hole in the center
    center_point = adsk.core.Point3D.create(0, 0, 0)
    hole_input = root_comp.features.holeFeatures.createInput(
        adsk.core.ValueInput.createByReal(center_hole_dia / 2),
        adsk.core.ValueInput.createByReal(thickness),
        adsk.fusion.HoleTypes.Simple,
        None
    )
    hole_input.setToCenter(center_point)
    hole = root_comp.features.holeFeatures.add(hole_input)

    # Calculate Fusion 360 volume
    fusion360_volume = calculate_fusion360_volume(root_comp)

    # Close Fusion 360 document
    app.activeDocument.close(False)

    return fusion360_volume

# Function for example_03: Extruded Prismatic Solid
def example_03(app, ui, design):
    length = 80.0
    width = 60.0
    thickness = 10.0

    # Convert parameters to Fusion 360 units
    length = convert_units(length)
    width = convert_units(width)
    thickness = convert_units(thickness)

    # Create a circular base with a rectangular cutout
    root_comp = design.rootComponent
    sketches = root_comp.sketches
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw circle
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), width / 2)

    # Draw rectangle
    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(-length / 4, -width / 4, 0),
                                      adsk.core.Point3D.create(length / 4, width / 4, 0))

    # Extrude the profile
    extrudes = root_comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    distance = adsk.core.ValueInput.createByReal(2 * thickness)
    extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, distance)
    extrude = extrudes.add(extrude_input)

    # Calculate Fusion 360 volume
    fusion360_volume = calculate_fusion360_volume(root_comp)

    # Close Fusion 360 document
    app.activeDocument.close(False)

    return fusion360_volume

# Main run function
def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct

    # Precomputed build123d volumes
    build123d_volumes = [48000.0, 44198.67288915635, 202194.6710584651]

    # Call each example function and collect Fusion 360 volumes
    fusion360_volumes = []
    fusion360_volumes.append(example_01(app, ui, design))
    fusion360_volumes.append(example_02(app, ui, design))
    fusion360_volumes.append(example_03(app, ui, design))

    # Compare volumes and display message boxes for mismatches
    for i, (b_vol, f_vol) in enumerate(zip(build123d_volumes, fusion360_volumes)):
        if not math.isclose(b_vol, f_vol, rel_tol=1e-9):
            ui.messageBox(f"Volume mismatch in example_{i + 1}:\n"
                          f"Build123d Volume: {b_vol}\n"
                          f"Fusion 360 Volume: {f_vol}")