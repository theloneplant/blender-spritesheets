import bpy
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup

class UI_PT_SpritePanel(bpy.types.Panel):
    bl_idname = "UI_PT_SpritePanel"
    bl_label = "Sprite Sheet Panel"
    bl_category = "Sprite Sheet"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        props = context.scene.SpriteSheetPropertyGroup
        row = layout.row()
        row.prop(props, "outputPath")
        row = layout.row()
        row.prop(props, "tileWidth")
        row.prop(props, "tileHeight")
        row = layout.row()
        row.prop(props, "fps")
        row = layout.row()
        row.operator("spritesheets.render", text="Render Sprite Sheets")
