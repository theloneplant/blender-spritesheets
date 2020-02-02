import bpy
import os
import sys
import importlib

ADDON_FOLDER_NAME = "plugin"

ADDON_DIR = os.path.dirname(os.path.realpath(__file__))
if not ADDON_DIR in sys.path:
    sys.path.append(ADDON_DIR)

from panels import spritePanel
importlib.reload(spritePanel)
from operators import renderSpriteSheet
importlib.reload(renderSpriteSheet)
from operators import renderTile
importlib.reload(renderTile)
from properties import ProgressPropertyGroup
importlib.reload(ProgressPropertyGroup)
from properties import SpriteSheetPropertyGroup
importlib.reload(SpriteSheetPropertyGroup)

print(dir(bpy))

bl_info = {
    "name": "Blender Sprite Sheets",
    "author": "Michael LaPlante, Tim Harding",
    "description": "A Blender plugin that allows you to export 3D models and animations to spritesheets",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Animation"
}

classes = (
    SpriteSheetPropertyGroup.SpriteSheetPropertyGroup,
    ProgressPropertyGroup.ProgressPropertyGroup,
    renderTile.RenderTile, 
    renderSpriteSheet.RenderSpriteSheet, 
    spritePanel.UI_PT_SpritePanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Create a reference to property groups so other classes can use it
    bpy.types.Scene.SpriteSheetPropertyGroup = bpy.props.PointerProperty(
        type=SpriteSheetPropertyGroup.SpriteSheetPropertyGroup)
    bpy.types.Scene.ProgressPropertyGroup = bpy.props.PointerProperty(
        type=ProgressPropertyGroup.ProgressPropertyGroup)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.SpriteSheetPropertyGroup
    del bpy.types.Scene.ProgressPropertyGroup

if __name__ == "__main__":
    register()
