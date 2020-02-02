import bpy

class SpriteSheetPropertyGroup(bpy.types.PropertyGroup):
    """Property group defining all of the configurable values for rendering sprite sheets"""
    outputPath = bpy.props.StringProperty(
        name="Output Path",
        subtype="DIR_PATH"
    )
    objectToRender = bpy.props.StringProperty(
        name="Object to Render"
    )
    tileWidth = bpy.props.IntProperty(
        name="tileWidth",
        description="Width of an individual sprite",
        default=50,
        min=1,
    )
    tileHeight = bpy.props.IntProperty(
        name="tileHeight",
        description="Height of an individual sprite",
        default=50,
        min=1,
    )
    fps = bpy.props.IntProperty(
        name="fps",
        description="Framerate of the output animation",
        default=24,
        min=1,
    )

