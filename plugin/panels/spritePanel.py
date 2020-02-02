import bpy
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup

class UI_PT_SpritePanel(bpy.types.Panel):
    """Panel for configuring and rendering sprite sheets"""
    bl_idname = "UI_PT_SpritePanel"
    bl_label = "Sprite Sheet Panel"
    bl_category = "Sprite Sheet"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        """Draw method that initializes the UI for the panel"""
        layout = self.layout

        props = context.scene.SpriteSheetPropertyGroup
        progressProps = context.scene.ProgressPropertyGroup

        row = layout.row()
        row.prop(props, "outputPath")
        #TODO: add support to select object
        row = layout.row()
        row.prop(props, "tileWidth")
        row.prop(props, "tileHeight")
        row = layout.row()
        row.prop(props, "fps")

        layout.separator()

        row = layout.row()
        row.operator("spritesheets.render", text="Render Sprite Sheet")
