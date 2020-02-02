import bpy
import math
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup

class RenderSpriteSheet(bpy.types.Operator):
    """Operator used to render sprite sheets for an object"""
    bl_idname = "spritesheets.render"
    bl_label = "Render Sprite Sheets"
    bl_description = "Renders all actions to a single sprite sheet"

    def execute(self, context):
        """Execute method called through the Blender panel UI"""
        scene = context.scene
        props = scene.SpriteSheetPropertyGroup
        objectToRender = scene.objects.get("Cube")
        for action in bpy.data.actions:
            # TODO: Configure which actions to render through UI for a given object
            objectToRender.animation_data.action = action
            self.processAction(action, scene, props, objectToRender)

        # TODO: Call Rust function to combine temp images
        # TODO: Output JSON with metadata for importer
        
        return {'FINISHED'}

    def processAction(self, action, scene, props, objectToRender):
        """Processes a single action by iterating through each frame and rendering tiles to a temp folder"""
        frameRange = action.frame_range
        name = action.name
        print("Action: ", name, " - Frame Range: ", frameRange)
        print("Range: ", math.floor(frameRange[0]), ", ", math.ceil(frameRange[1]))
        for index in range(math.floor(frameRange[0]), math.ceil(frameRange[1])):
            print(index)
            scene.frame_set(index)
            self.renderTile(name, index, scene, props)
        return

    def renderTile(self, name, index, scene, props):
        """Renders individual frames to a temp folder which will be combined after all of the frames have finished rendering"""
        print("Rendering ", name, " ", index)
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.film_transparent = True  # Transparent PNG
        scene.render.filter_size = 0  # Disable AA
        scene.render.bake_margin = 0
        scene.render.resolution_percentage = 100
        scene.render.resolution_x = props.tileWidth
        scene.render.resolution_y = props.tileHeight
        scene.render.filepath = props.outputPath + "temp/" + name + str(index)
        bpy.ops.render.render(write_still=1)
        return
