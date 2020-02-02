import os
import bpy
import math
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup

class RenderSpriteSheet(bpy.types.Operator):
    """Operator used to render sprite sheets for an object"""
    bl_idname = "spritesheets.render"
    bl_label = "Render Sprite Sheets"
    bl_description = "Renders all actions to a single sprite sheet"

    def execute(self, context):
        scene = bpy.context.scene
        props = scene.SpriteSheetPropertyGroup
        progressProps = scene.ProgressPropertyGroup
        progressProps.rendering = True
        progressProps.success = False
        progressProps.actionTotal = len(bpy.data.actions)

        objectToRender = scene.objects.get("Cube")
        for index, action in enumerate(bpy.data.actions):
            progressProps.actionName = action.name
            progressProps.actionIndex = index
            # TODO: Configure which actions to render through UI for a given object
            objectToRender.animation_data.action = action
            self.processAction(action, scene, progressProps, objectToRender)

        # TODO: Call Rust function to combine temp images
        # TODO: Output JSON with metadata for importer

        progressProps.rendering = False
        progressProps.success = True
        os.remove(props.outputPath + "temp/")
        self.report({'INFO'}, "Finished Rendering Actions")
        return {'FINISHED'}

    def processAction(self, action, scene, progressProps, objectToRender):
        """Processes a single action by iterating through each frame and rendering tiles to a temp folder"""
        frameRange = action.frame_range
        frameMin = math.floor(frameRange[0])
        frameMax = math.ceil(frameRange[1])
        progressProps.tileTotal = frameMax - frameMin
        for index in range(frameMin, frameMax):
            progressProps.tileIndex = index
            scene.frame_set(index)
            # TODO: Unfortunately Blender's rendering happens on the same thread as the UI and freezes it while running,
            # eventually they may fix this and then we can leverage some of the progress information we track
            bpy.ops.spritesheets.render_tile('EXEC_DEFAULT')
        return
