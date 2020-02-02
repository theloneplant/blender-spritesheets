import bpy
import os
import sys

ADDON_FOLDER_NAME = "plugin"

# Add the addon's absolute path to the sys.path so we can reference custom modules
dir = os.path.join(bpy.utils.script_path_user(), "addons", ADDON_FOLDER_NAME)
if not dir in sys.path:
    sys.path.append(dir)
print(dir)

from panels.spritePanel import UI_PT_SpritePanel
from operators.renderTile import RenderTile
from operators.renderSpriteSheet import RenderSpriteSheet
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup

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

classes = (SpriteSheetPropertyGroup, ProgressPropertyGroup,
           RenderTile, RenderSpriteSheet, UI_PT_SpritePanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Create a reference to property groups so other classes can use it
    bpy.types.Scene.SpriteSheetPropertyGroup = bpy.props.PointerProperty(
        type=SpriteSheetPropertyGroup)
    bpy.types.Scene.ProgressPropertyGroup = bpy.props.PointerProperty(
        type=ProgressPropertyGroup)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.SpriteSheetPropertyGroup
    del bpy.types.Scene.ProgressPropertyGroup

if __name__ == "__main__":
    register()
