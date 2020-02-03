# Blender Sprite Sheets
## Overview
This addon allows you to export an animated 3D model to a sprite sheet and import it into Unity. It can be used for pixel art or pseudo-3D assets to improve performance in your game projects. Simply model, rig, and animate your assets in Blender as you would normally, and then export all animations to a texture sheet and metadata sidecar. These two files can be imported into Unity, creating animations automatically for each Blender action.

This tool is especially useful for complicated sprite sheets you don't want to manually update with each small change. Previously for pixel art sprite sheets, the artist had to meticulously change each frame of each animation for every direction that a sprite faced, especially hard in top down pixel art games.

## Installation
### Blender Add-on Installation
1. Clone or download this repository and extract it
2. Open Blender (this addon was made using __2.81__), and open the addon panel by going to `Edit > Preferences > Add-ons`
3. Click __Install__ and navigate to the repository you just downloaded and select __plugin.zip__
4. The add on should be installed now, but it's disabled by default. Check the box next to __Animation: Blender Sprite Sheets__ in the Add-ons menu in Blender and it will be enabled
5. In Blender's 3D Viewport you should now see a new tab on the right pop-out menu called Sprite Sheet
6. You've successfully installed the add on

### Unity Importer Installation
Use `Assets -> Import Package -> Custom Package` to browse for the Unity Importer package. 

## Usage
### Blender Add-on Usage
1. In Blender's 3D Viewport, open the panel on the right side (it may be hidden by default, look for a small arrow near the top-right corner of the 3D Viewport area)
2. Select the tab called __Sprite Sheet__
3. Select the __Target__, this is the object that will be animated and rendered to a sprite sheet
4. Configure your render settings
5. If you want to choose specific frames to render instead of every single one, you can specify '__Only render marked frames__' in the Rendering section. Note that this uses specifically __Action Pose Markers__ in Blender and not Timeline Markers. To edit Action Pose Markers, open the __Dope Sheet__, and make sure Marker > Show Pose Markers is selected. When this is selected you can use Marker > Add Marker and it will create an Action Pose Marker for that frame and action. This means you can use different Action Pose Markers for each action that you've created!
6. Select an output folder
7. Click on __Render Sprite Sheet__, note this may freeze Blender for a short time as the files are being rendered. Don't worry and let it do its thing. You should see the image generated in the output folder along with a JSON file that can be used for Unity importing.

### Unity Importer Usage
Import the texture and the `.bss` sidecar side-by-side anywhere in your assets folder. Sprites and animations should appear automatically in the same folder. 

## Examples
If you aren't familiar with how Blender's animation system works, you can try using a sample .blend file in the __examples__ folder of the repository.

You can see the animations for a Blender object through the __Dope Sheet__.
