
import adsk.core
import adsk.fusion
import math

def convert_mm_to_cm(value_mm: float) -> float:
    """Converts a value from millimeters (mm) to centimeters (cm)."""
    return value_mm / 10.0

def calculate_volume(root_comp: adsk.fusion.Component) -> float:
    """Calculates the volume of the first B-Rep body in the component and converts it to mm^3."""
    return root_comp.bRepBodies.item(0).volume * 1000  # Convert cm^3 to mm^3

def example_01(root_comp: adsk.fusion.Component):
    """
    Creates a simple rectangular plate in Fusion 360.
    """
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)

    length = convert_mm_to_cm(80.0)
    width = convert_mm_to_cm(60.0)
    thickness = convert_mm_to_cm(10.0)

    # Get the root component of the active design.
    # root_comp = design.rootComponent

    # Create a new sketch on the xy plane.
    sketches = root_comp.sketches
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw a rectangle on the sketch.
    sketch_curves = sketch.sketchCurves
    sketch_lines = sketch_curves.sketchLines
    rect_width = width
    rect_height = length
    start_point = adsk.core.Point3D.create(-rect_width / 2, -rect_height / 2, 0)
    end_point = adsk.core.Point3D.create(rect_width / 2, -rect_height / 2, 0)
    line1 = sketch_lines.addByTwoPoints(start_point, end_point)

    start_point = adsk.core.Point3D.create(rect_width / 2, -rect_height / 2, 0)
    end_point = adsk.core.Point3D.create(rect_width / 2, rect_height / 2, 0)
    line2 = sketch_lines.addByTwoPoints(start_point, end_point)

    start_point = adsk.core.Point3D.create(rect_width / 2, rect_height / 2, 0)
    end_point = adsk.core.Point3D.create(-rect_width / 2, rect_height / 2, 0)
    line3 = sketch_lines.addByTwoPoints(start_point, end_point)

    start_point = adsk.core.Point3D.create(-rect_width / 2, rect_height / 2, 0)
    end_point = adsk.core.Point3D.create(-rect_width / 2, -rect_height / 2, 0)
    line4 = sketch_lines.addByTwoPoints(start_point, end_point)

    # Get the profile defined by the rectangle.
    profiles = sketch.profiles
    profile = profiles.item(0)

    # Create an extrusion input to define the features.
    extrudes = root_comp.features.extrudeFeatures
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Define the distance extent.
    distance = adsk.core.ValueInput.createByReal(thickness)
    extrude_input.setDistanceExtent(False, distance)

    # Create the extrusion.
    extrude = extrudes.add(extrude_input)

    return 48000.0 # build123d volume

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # Get the root component of the active design.
        root_comp = design.rootComponent

        # Function 1: Simple Rectangular Plate
        build123d_volume = example_01(root_comp)
        fusion360_volume = calculate_volume(root_comp)

        if not math.isclose(build123d_volume, fusion360_volume, rel_tol=1e-6):
            ui.messageBox(f"Example 01:\nBuild123d Volume: {build123d_volume} mm^3\nFusion 360 Volume: {fusion360_volume} mm^3\nVolumes are different.")

        # Delete all bodies and sketches
        for body in root_comp.bRepBodies:
            body.deleteMe()
        for sketch in root_comp.sketches:
            sketch.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
