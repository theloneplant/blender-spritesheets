import bpy
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup


class UI_PT_SpritePanel(bpy.types.Panel):
    """Panel for configuring and rendering sprite sheets"""
    bl_idname = "UI_PT_SpritePanel"
    bl_label = "Create Sprite Sheet"
    bl_category = "Sprite Sheet"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        """Draw method that initializes the UI for the panel"""
        layout = self.layout

        props = context.scene.SpriteSheetPropertyGroup
        progressProps = context.scene.ProgressPropertyGroup

        row = layout.row()
        row.label(text="Selection", icon="CURSOR")
        row = layout.row()
        row.prop_search(props, "target", bpy.data, "objects")
        row = layout.row()
        row.label(text="This target will have all Actions in the Scene applied to it when rendering animations")

        layout.separator()

        row = layout.row()
        row.label(text="Rendering", icon="VIEW_CAMERA")
        row = layout.row()
        row.prop(props, "tileSize")
        row = layout.row()
        row.prop(props, "fps")
        row = layout.row()
        row.prop(props, "onlyRenderMarkedFrames")

        layout.separator()

        row = layout.row()
        row.label(text="Output", icon="FILE_FOLDER")
        row = layout.row()
        row.prop(props, "outputPath")

        layout.separator()

        row = layout.row()
        row.operator("spritesheets.render", text="Render Sprite Sheet")
        row = layout.row()
        row.label(text="Note: Blender will freeze briefly")
