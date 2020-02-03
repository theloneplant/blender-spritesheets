import bpy

class ProgressPropertyGroup(bpy.types.PropertyGroup):
    """Property group defining all of the configurable values for displaying rendering progress"""
    actionName = bpy.props.StringProperty(name="actionName")
    actionIndex = bpy.props.IntProperty(name="actionIndex")
    actionTotal = bpy.props.IntProperty(name="actionTotal")
    tileIndex = bpy.props.IntProperty(name="tileIndex")
    tileTotal = bpy.props.IntProperty(name="tileTotal")
    rendering = bpy.props.BoolProperty(name="rendering")
    success = bpy.props.BoolProperty(name="success")
