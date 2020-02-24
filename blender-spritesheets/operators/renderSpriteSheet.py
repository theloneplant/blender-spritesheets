import os
import sys
import bpy
import math
import shutil
import platform
import subprocess
import json
from properties.SpriteSheetPropertyGroup import SpriteSheetPropertyGroup
from properties.ProgressPropertyGroup import ProgressPropertyGroup

ASSEMBLER_FILENAME = "assembler.exe" if platform.system() is "Windows" else "assembler"

class RenderSpriteSheet(bpy.types.Operator):
    """Operator used to render sprite sheets for an object"""
    bl_idname = "spritesheets.render"
    bl_label = "Render Sprite Sheets"
    bl_description = "Renders all actions to a single sprite sheet"

    def execute(self, context):
        """
        Runs through one step of the rendering process. This will be called every frame and when the user starts rendering
        this will begin the workflow without completely blocking the Blender UI.
        """
        scene = bpy.context.scene
        props = scene.SpriteSheetPropertyGroup
        progress_props = scene.ProgressPropertyGroup
        # If not rendering, skip the function
        if not progress_props.rendering:
            self.prev_rendering = False
            return {'FINISHED'}
        # If rendering just started, initialize actions and start rendering the first tile
        if progress_props.rendering and not self.prev_rendering:
            self.prev_rendering = True
            self.action_iter = iter(bpy.data.actions)
            self.animation_descs = []
            self.frame_end = 0
            self.action = None
            progress_props.actionIndex = 0
            progress_props.actionTotal = len(bpy.data.actions)
        else:
            # Render normally
            return self.render_frame(scene, props, progress_props)

    def render_frame(self, scene, props, progress_props):
        """
        Checks if the current action is done rendering and renders the next frame. If it's done this will
        set up the next action to render during the next workflow cycle.
        """
        # Check if all actions are finished rendering, update status, and compile the sprite sheet
        if self.action is None and not self.next_action(scene, props, progress_props):
            self.compile_sprite_sheet(scene, props, progress_props)
        # Render the next frame of the workflow
        has_next = False
        if props.onlyRenderMarkedFrames is True and self.markers is not None and self.marker_length > 0:
            has_next = self.render_next_marked_frame(scene, props, progress_props)
        else:
            has_next = self.render_next_frame(scene, props, progress_props)
        # If the action is finished rendering, reset current action so another one will be fetched next workflow
        if not has_next:
            self.action = None
        return {'FINISHED'}

    def next_action(self, scene, props, progress_props):
        """Checks whether there is another action to render. If it exists, initialize next action for rendering"""
        self.action = next(self.action_iter, None)
        if self.action is None:
            return False
        progress_props.actionName = self.action.name
        progress_props.actionIndex += 1 # Action index will start at 1 for displaying in the UI
        # Initialize markers for only rendering marked frames
        self.markers = self.action.pose_markers.values()
        self.marker_iter = iter(self.markers, None)
        # Initialize frames for standard rendering, also used for rendering marked frames
        self.frame_length, self.frame_index, self.frame_max = self.frame_count(self.action.frame_range)
        # Update the target's action to the current action and reset frame position
        props.target.animation_data.action = self.action
        scene.frame_set(self.frame_index)
        # Update frame_end depending on whether to use marked frames or all frames
        if props.onlyRenderMarkedFrames is True and self.markers is not None and len(self.markers) > 0:
            self.marker_length = len(self.markers)
            self.marker_index = 0
            self.frame_end += self.marker_length
            progress_props.tileTotal = self.marker_length
        else:
            self.frame_end += self.frame_length
            progress_props.tileTotal = self.frame_length
        return True

    def render_next_marked_frame(self, scene, props, progress_props):
        """Renders the next marked frame, returns whether it was able to successfully render it"""
        self.marker = next(self.marker_iter, None)
        if self.marker is None or self.marker_index >= self.marker_length:
            return False
        progress_props.tileIndex = self.marker_index
        self.marker_index += 1
        scene.frame_set(self.marker.frame)
        bpy.ops.spritesheets.render_tile('EXEC_DEFAULT')
        return True

    def render_next_frame(self, scene, props, progress_props):
        """Renders the next frame, returns whether it was able to successfully render it"""
        if self.frame_index >= self.frame_length:
            return False
        progress_props.tileIndex = self.frame_index
        self.frame_index += 1
        scene.frame_set(self.frame_index)
        bpy.ops.spritesheets.render_tile('EXEC_DEFAULT')
        return True
    
    def compile_sprite_sheet(self, scene, props, progress_props):
        """Compiles sprite sheet images into a single image and bss sidecar and removes the temp directory"""
        progress_props.rendering = False
        progress_props.success = True
        assemblerPath = os.path.normpath(
            os.path.join(props.binPath, ASSEMBLER_FILENAME)
        )
        subprocess.run([assemblerPath, "--root", bpy.path.abspath(props.outputPath)])
        json_info = {
            "tileWidth": props.tileSize[0],
            "tileHeight": props.tileSize[1],
            "frameRate": props.fps,
            "animations": self.animation_descs,
        }
        with open(bpy.path.abspath(os.path.join(props.outputPath, "out.bss")), "w") as f:
            json.dump(json_info, f, indent='\t')
        shutil.rmtree(bpy.path.abspath(os.path.join(props.outputPath, "temp")))
        return {'FINISHED'}

    def frame_count(self, frame_range):
        frameMin = math.floor(frame_range[0])
        frameMax = math.ceil(frame_range[1])
        return (frameMax - frameMin, frameMin, frameMax)
