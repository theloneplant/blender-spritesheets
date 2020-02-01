namespace Spritesheet
{
    using System.IO;
    using UnityEditor.Experimental.AssetImporters;
    using UnityEngine;

    // Blender sprite sheet
    [ScriptedImporter(1, "bss")]
    public class MetadataImporter : ScriptedImporter
    {
        public override void OnImportAsset(AssetImportContext ctx)
        {
            SpritesheetMetadata metadata = ScriptableObject.CreateInstance<SpritesheetMetadata>();
            string text = File.ReadAllText(ctx.assetPath);
            JsonUtility.FromJsonOverwrite(text, metadata);
            if (!metadata.Valid)
            {
                Debug.LogError("Invalid Blender spritesheet metadata");
                return;
            }

            ctx.AddObjectToAsset("metadata", metadata);
            ctx.SetMainObject(metadata);
        }
    }
}