import bpy

ProgressPropertyGroup = type(
    "ProgressPropertyGroup",
    (bpy.types.PropertyGroup,),
    {
        "__annotations__": {
          "actionName": bpy.props.StringProperty(name="actionName"),
          "actionIndex": bpy.props.IntProperty(name="actionIndex"),
          "actionTotal": bpy.props.IntProperty(name="actionTotal"),
          "tileIndex": bpy.props.IntProperty(name="tileIndex"),
          "tileTotal": bpy.props.IntProperty(name="tileTotal"),
          "rendering": bpy.props.BoolProperty(name="rendering"),
          "success": bpy.props.BoolProperty(name="success"),
        }
    },
)
