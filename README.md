# Blender Sprite Sheets
## Overview
This addon will allow you to export a 3D model with animations to a sprite sheet and import it into Unity for use in pixel art or pseudo 3D assets to improve performance in your games or other projects. The way to use this add on is to model, rig, and animate assets the same way you would normally in Blender, and afterwards you can export all animations to a single image and JSON file. These two files can then be used by the Unity importer to automatically create animations for each action that you used in Blender to animate the original model.

This tool is especially useful when you have complicated sprite sheets and don't want to update them by hand each time a small change is made to the original. For instance, previously for sprite sheets in pixel art, the artist would need to meticulously change each frame of each animation for every direction that a sprite faced (especially hard in top down pixel art games).

## Installation
### Blender Add-on Installation
1. Clone or download this repository and extract it
1. (Optional) Move the bin folder into another folder of your choosing. This will need to exist as long as you want to use the Blender add on.
1. Open __Blender__ (this addon was made using __2.81__), and open the addon panel by going to Edit > Preferences > Add-ons
1. Click __Install__ and navigate to the repository you just downloaded and select __blender-spritesheets.zip__
1. The add on should be installed now, but it's disabled by default. Check the box next to __Animation: Blender Sprite Sheets__ in the Add-ons menu in Blender and it will be enabled
1. In Blender's 3D Viewport you should now see a new tab on the right pop-out menu called Sprite Sheet
1. You've successfully installed the add on

### Unity Importer Installation
TODO

## Usage
### Blender Add-on Usage
1. In Blender's 3D Viewport, open the panel on the right side (it may be hidden by default, look for a small arrow near the top-right corner of the 3D Viewport area)
1. Select the tab called __Sprite Sheet__
1. Select the __Bin__ folder where the executables are in that you set up during installation
1. Select the __Target__, this is the object that will be animated and rendered to a sprite sheet
1. Configure your render settings
1. If you want to choose specific frames to render instead of every single one, you can specify '__Only render marked frames__' in the Rendering section. Note that this uses specifically __Action Pose Markers__ in Blender and not Timeline Markers. To edit Action Pose Markers, open the __Dope Sheet__, and make sure Marker > Show Pose Markers is selected. When this is selected you can use Marker > Add Marker and it will create an Action Pose Marker for that frame and action. This means you can use different Action Pose Markers for each action that you've created!
1. Select an output folder
1. Click on __Render Sprite Sheet__, note this may freeze Blender for a short time as the files are being rendered. Don't worry and let it do its thing. You should see the image generated in the output folder along with a JSON file that can be used for Unity importing.

### Unity Importer Usage
TODO

## Examples
If you aren't familiar with how Blender's animation system works, you can try using a sample .blend file in the __examples__ folder of the repository.

You can see the animations for a Blender object through the __Dope Sheet__.
