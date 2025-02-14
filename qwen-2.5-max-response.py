import adsk.core
import adsk.fusion
import traceback

def convert_to_fusion_units(value):
    """Convert build123d units (mm) to Fusion 360 units (cm)."""
    return value / 10.0

def compare_volumes(ui, build_volume, fusion_volume):
    """Compare build123d and Fusion 360 volumes."""
    identical = "identical" if abs(build_volume - fusion_volume) < 1e-6 else "different"
    message = f"Build123d Volume: {build_volume:.2f} mm³\nFusion 360 Volume: {fusion_volume:.2f} mm³\nVolumes are {identical}."
    ui.messageBox(message)

def create_rectangular_plate(app, ui, length, width, thickness, build_volume):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        root_comp = design.rootComponent
        sketches = root_comp.sketches
        extrudes = root_comp.features.extrudeFeatures

        # Create sketch
        xy_plane = root_comp.xYConstructionPlane
        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(convert_to_fusion_units(length), convert_to_fusion_units(width), 0)
        )

        # Extrude
        profile = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(convert_to_fusion_units(thickness))
        extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrude_input.setSymmetricExtent(distance, False)
        extrude_feature = extrudes.add(extrude_input)

        # Calculate Fusion 360 volume
        fusion_volume = extrude_feature.bodies.item(0).volume * 1000  # Convert cm³ to mm³
        compare_volumes(ui, build_volume, fusion_volume)

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def create_plane_with_hole(app, ui, length, width, thickness, hole_dia, build_volume):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        root_comp = design.rootComponent
        sketches = root_comp.sketches
        extrudes = root_comp.features.extrudeFeatures

        # Create sketch
        xy_plane = root_comp.xYConstructionPlane
        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(convert_to_fusion_units(length), convert_to_fusion_units(width), 0)
        )
        circles = sketch.sketchCurves.sketchCircles
        center = adsk.core.Point3D.create(convert_to_fusion_units(length / 2), convert_to_fusion_units(width / 2), 0)
        circle = circles.addByCenterRadius(center, convert_to_fusion_units(hole_dia / 2))

        # Extrude
        profile = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(convert_to_fusion_units(thickness))
        extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrude_input.setSymmetricExtent(distance, False)
        extrude_feature = extrudes.add(extrude_input)

        # Calculate Fusion 360 volume
        fusion_volume = extrude_feature.bodies.item(0).volume * 1000  # Convert cm³ to mm³
        compare_volumes(ui, build_volume, fusion_volume)

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def create_extruded_prismatic_solid(app, ui, length, width, thickness, build_volume):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        root_comp = design.rootComponent
        sketches = root_comp.sketches
        extrudes = root_comp.features.extrudeFeatures

        # Create sketch
        xy_plane = root_comp.xYConstructionPlane
        sketch = sketches.add(xy_plane)
        circles = sketch.sketchCurves.sketchCircles
        circle = circles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), convert_to_fusion_units(width)
        )
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(convert_to_fusion_units(length / 2), convert_to_fusion_units(width / 2), 0)
        )

        # Extrude
        profile = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(convert_to_fusion_units(2 * thickness))
        extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrude_input.setSymmetricExtent(distance, False)
        extrude_feature = extrudes.add(extrude_input)

        # Calculate Fusion 360 volume
        fusion_volume = extrude_feature.bodies.item(0).volume * 1000  # Convert cm³ to mm³
        compare_volumes(ui, build_volume, fusion_volume)

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def create_profile_with_arcs(app, ui, length, width, thickness, build_volume):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        root_comp = design.rootComponent
        sketches = root_comp.sketches
        extrudes = root_comp.features.extrudeFeatures

        # Create sketch
        xy_plane = root_comp.xYConstructionPlane
        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs

        # Line 1
        l1_start = adsk.core.Point3D.create(0, 0, 0)
        l1_end = adsk.core.Point3D.create(convert_to_fusion_units(length), 0, 0)
        line1 = lines.addByTwoPoints(l1_start, l1_end)

        # Line 2
        l2_start = l1_end
        l2_end = adsk.core.Point3D.create(convert_to_fusion_units(length), convert_to_fusion_units(width), 0)
        line2 = lines.addByTwoPoints(l2_start, l2_end)

        # Arc
        arc_center = adsk.core.Point3D.create(convert_to_fusion_units(width), convert_to_fusion_units(width * 1.5), 0)
        arc_start = l2_end
        arc_end = adsk.core.Point3D.create(0, convert_to_fusion_units(width), 0)
        arc = arcs.addByThreePoints(arc_start, arc_center, arc_end)

        # Line 4
        line4 = lines.addByTwoPoints(arc_end, l1_start)

        # Extrude
        profile = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(convert_to_fusion_units(thickness))
        extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrude_input.setSymmetricExtent(distance, False)
        extrude_feature = extrudes.add(extrude_input)

        # Calculate Fusion 360 volume
        fusion_volume = extrude_feature.bodies.item(0).volume * 1000  # Convert cm³ to mm³
        compare_volumes(ui, build_volume, fusion_volume)

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def create_moving_working_point(app, ui, a, b, c, d, build_volume):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        root_comp = design.rootComponent
        sketches = root_comp.sketches
        extrudes = root_comp.features.extrudeFeatures

        # Create sketch
        xy_plane = root_comp.xYConstructionPlane
        sketch = sketches.add(xy_plane)
        circles = sketch.sketchCurves.sketchCircles
        circle = circles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), convert_to_fusion_units(a)
        )

        # Rectangle at (b, 0)
        lines = sketch.sketchCurves.sketchLines
        rect_start = adsk.core.Point3D.create(convert_to_fusion_units(b), 0, 0)
        rect_end = adsk.core.Point3D.create(
            convert_to_fusion_units(b + c), convert_to_fusion_units(c), 0
        )
        rect = lines.addTwoPointRectangle(rect_start, rect_end)

        # Circle at (0, b)
        small_circle = circles.addByCenterRadius(
            adsk.core.Point3D.create(0, convert_to_fusion_units(b), 0), convert_to_fusion_units(d)
        )

        # Extrude
        profile = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(convert_to_fusion_units(c))
        extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrude_input.setSymmetricExtent(distance, False)
        extrude_feature = extrudes.add(extrude_input)

        # Calculate Fusion 360 volume
        fusion_volume = extrude_feature.bodies.item(0).volume * 1000  # Convert cm³ to mm³
        compare_volumes(ui, build_volume, fusion_volume)

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Example 1: Rectangular Plate
        create_rectangular_plate(app, ui, 80.0, 60.0, 10.0, 48000.0)

        # Example 2: Plane with Hole
        create_plane_with_hole(app, ui, 80.0, 60.0, 10.0, 22.0, 44198.67288915635)

        # Example 3: Extruded Prismatic Solid
        create_extruded_prismatic_solid(app, ui, 80.0, 60.0, 10.0, 202194.6710584651)

        # Example 4: Profile with Arcs
        create_profile_with_arcs(app, ui, 80.0, 60.0, 10.0, 69504.6716490322)

        # Example 5: Moving Working Point
        create_moving_working_point(app, ui, 90.0, 45.0, 15.0, 7.5, 375677.7886096935)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))