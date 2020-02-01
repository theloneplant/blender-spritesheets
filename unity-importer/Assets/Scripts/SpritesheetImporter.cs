namespace Spritesheet
{
    using System.IO;
    using UnityEditor.Experimental.AssetImporters;
    using UnityEngine;

    // Docs: AssetPostprocessor should be in a DLL or 
    // imports cannot work when there are script compilation errors.

    // Blender sprite sheet
    [ScriptedImporter(1, "bss")]
    public class SpritesheetImporter : ScriptedImporter
    {
        public override void OnImportAsset(AssetImportContext ctx)
        {
            string text = File.ReadAllText(ctx.assetPath);
            JsonFormat info = JsonUtility.FromJson<JsonFormat>(text);
            /*
            Debug.Log(string.Format("Tile width:  {0}", info.tileWidth));
            Debug.Log(string.Format("Tile height: {0}", info.tileHeight));
            foreach (Animation anim in info.animations)
            {
                Debug.Log(string.Format("{0}: {1}", anim.name, anim.start));
            }
            */

            /*
            // 'cube' is a a GameObject and will be automatically converted into a prefab
            // (Only the 'Main Asset' is elligible to become a Prefab.)
            ctx.AddObjectToAsset("main obj", cube);
            ctx.SetMainObject(cube);
            */
        }
    }
}