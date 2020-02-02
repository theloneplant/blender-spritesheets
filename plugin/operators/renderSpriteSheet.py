import os
import sys
import bpy
import math
import shutil
import subprocess
import json
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSEMBLER_PATH = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "assembler.exe",
    )
)
print(ASSEMBLER_PATH)

class RenderSpriteSheet(bpy.types.Operator):
    """Operator used to render sprite sheets for an object"""
    bl_idname = "spritesheets.render"
    bl_label = "Render Sprite Sheets"
    bl_description = "Renders all actions to a single sprite sheet"

    def execute(self, context):
        scene = bpy.context.scene
        props = scene.SpriteSheetPropertyGroup
        progressProps = scene.ProgressPropertyGroup
        progressProps.rendering = True
        progressProps.success = False
        progressProps.actionTotal = len(bpy.data.actions)

        animation_descs = []
        frame_end = 0

        objectToRender = props.target
        for index, action in enumerate(bpy.data.actions):
            progressProps.actionName = action.name
            progressProps.actionIndex = index
            objectToRender.animation_data.action = action

            count, _, _ = frame_count(action.frame_range)
            frame_end += count
            animation_descs.append({
                "name": action.name,
                "end": frame_end,
            })

            self.processAction(action, scene, props,
                               progressProps, objectToRender)

        subprocess.run([ASSEMBLER_PATH, "--root", props.outputPath])

        json_info = {
            "tileWidth": props.tileSize[0],
            "tileHeight": props.tileSize[1],
            "frameRate": props.fps,
            "animations": animation_descs,
        }

        with open(os.path.join(props.outputPath, "out.bss"), "w") as f:
            json.dump(json_info, f, indent='\t')

        progressProps.rendering = False
        progressProps.success = True
        shutil.rmtree(os.path.join(
            props.outputPath.replace("//", "./"), "temp/"))
        return {'FINISHED'}


    def processAction(self, action, scene, props, progressProps, objectToRender):
        """Processes a single action by iterating through each frame and rendering tiles to a temp folder"""
        frameRange = action.frame_range
        frameCount, frameMin, frameMax = frame_count(frameRange)
        progressProps.tileTotal = frameCount
        actionPoseMarkers = action.pose_markers
        if props.onlyRenderMarkedFrames is True and actionPoseMarkers is not None and len(actionPoseMarkers.keys()) > 0:
            for marker in actionPoseMarkers.values():
                progressProps.tileIndex = marker.frame
                scene.frame_set(marker.frame)
                # TODO: Unfortunately Blender's rendering happens on the same thread as the UI and freezes it while running,
                # eventually they may fix this and then we can leverage some of the progress information we track
                bpy.ops.spritesheets.render_tile('EXEC_DEFAULT')
        else:
            for index in range(frameMin, frameMax):
                progressProps.tileIndex = index
                scene.frame_set(index)
                # TODO: Unfortunately Blender's rendering happens on the same thread as the UI and freezes it while running,
                # eventually they may fix this and then we can leverage some of the progress information we track
                bpy.ops.spritesheets.render_tile('EXEC_DEFAULT')


def frame_count(frame_range):
    frameMin = math.floor(frame_range[0])
    frameMax = math.ceil(frame_range[1])
    return (frameMax - frameMin, frameMin, frameMax)