import os
import bpy
import math
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup

class RenderTile(bpy.types.Operator):
    """Operator used to render sprite sheets for an object"""
    bl_idname = "spritesheets.render_tile"
    bl_label = "Render Tile"
    bl_description = "Renders a single tile for a sprite sheet"

    def execute(self, context):
        """Renders individual frames to a temp folder which will be combined after all of the frames have finished rendering"""
        scene = context.scene
        props = scene.SpriteSheetPropertyGroup
        progressProps = scene.ProgressPropertyGroup

        progress = float(progressProps.tileIndex + 1) / progressProps.tileTotal * 100

        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.film_transparent = True  # Transparent PNG
        scene.render.bake_margin = 0
        scene.render.resolution_percentage = 100
        scene.render.resolution_x = props.tileSize[0]
        scene.render.resolution_y = props.tileSize[1]
        scene.render.filepath = os.path.join(
            props.outputPath, "temp/") + progressProps.actionName + index_to_string(progressProps.tileIndex, progressProps.tileTotal)
        bpy.context.scene.eevee.taa_render_samples = 1
        bpy.ops.render.render(write_still=1)
        return {'FINISHED'}

def index_to_string(tile_index, tile_total):
    empty_digits = count_digits(tile_total) - count_digits(tile_index)
    return ("0" * empty_digits) + str(tile_index)

def count_digits(n):
    count=0
    while(n>0):
        count=count+1
        n=n//10
    return count