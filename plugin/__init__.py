import bpy
import os
import sys

# Gets the cwd of the blend file, figure out a way to do this with absolute path
dir = os.getcwd()
if not dir in sys.path:
    sys.path.append(dir)
print(dir)

from panels.spritePanel import UI_PT_SpritePanel
from operators.renderSpriteSheet import RenderSpriteSheet
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup

bl_info = {
    "name": "blender-spritesheets",
    "author": "Michael LaPlante",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}

classes = (SpriteSheetPropertyGroup, RenderSpriteSheet, UI_PT_SpritePanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.SpriteSheetPropertyGroup = bpy.props.PointerProperty(
        type=SpriteSheetPropertyGroup)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.SpriteSheetPropertyGroup

if __name__ == "__main__":
    register()
