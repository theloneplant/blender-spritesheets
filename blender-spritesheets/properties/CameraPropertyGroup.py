import bpy

CameraPropertyGroup = type(
    "CameraPropertyGroup",
    (bpy.types.PropertyGroup,),
    {
        "__annotations__": {
          "angleName": bpy.props.StringProperty(name="angleName"),
        }
    },
)
