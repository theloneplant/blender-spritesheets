import bpy

SpriteSheetPropertyGroup = type(
    "SpriteSheetPropertyGroup",
    (bpy.types.PropertyGroup,),
    {
        "__annotations__": {
            "binPath": bpy.props.StringProperty(
                name="Bin",
                subtype="DIR_PATH",
                description="Folder containing the executables for combining tiles",
                default="./"
            ),
            "target": bpy.props.PointerProperty(
                name="Target",
                description="Object to render with each animation",
                type=bpy.types.Object
            ),
            "tileSize": bpy.props.IntVectorProperty(
                name="Tile Size",
                description="Size of an individual sprite",
                default=(50,50),
                min=1,
                size=2
            ),
            "fps": bpy.props.IntProperty(
                name="FPS",
                description="Framerate of the output animation",
                default=24,
                min=1
            ),
            "onlyRenderMarkedFrames": bpy.props.BoolProperty(
                name="Only render marked frames",
                description="Only renders frames that have an Action Pose Marker, allowing you to choose which frames to include with a sprite sheet. To add marked frames make sure 'Show Pose Markers' is selected in the Action Editor.\n\nNote: If no markers are specified this will render the action normally.",
                default=False
            ),
            "outputPath": bpy.props.StringProperty(
                name="Path",
                subtype="DIR_PATH",
                description="Output path of the final spritesheet and metadata JSON",
                default="./"
            ),
        }
    },
)
