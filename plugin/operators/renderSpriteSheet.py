import bpy
import mathutils
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup

class RenderSpriteSheet(bpy.types.Operator):
    bl_idname = "spritesheets.render"
    bl_label = "Render Sprite Sheets"
    bl_description = "Renders all actions to a single sprite sheet"

    def execute(self, context):
        scene = context.scene
        props = context.scene.SpriteSheetPropertyGroup
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.film_transparent = True # Transparent PNG
        scene.render.filter_size = 0 # Disable AA
        scene.render.bake_margin = 0
        scene.render.resolution_percentage = 100
        scene.render.resolution_x = props.tileWidth
        scene.render.resolution_y = props.tileHeight
        scene.render.filepath = props.outputPath + "1"
        bpy.ops.render.render(write_still=1)
        return {'FINISHED'}
