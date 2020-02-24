import os
import bpy
from properties.ProgressPropertyGroup import ProgressPropertyGroup

class StartRender(bpy.types.Operator):
    """Operator used to render sprite sheets for an object"""
    bl_idname = "spritesheets.start_render"
    bl_label = "Start Rendering"
    bl_description = "Begins rendering a sprite sheet"

    def execute(self, context):
        """Starts the rendering workflow"""
        scene = context.scene
        progressProps = scene.ProgressPropertyGroup
        progressProps.rendering = True
        progressProps.success = False
        return {'FINISHED'}