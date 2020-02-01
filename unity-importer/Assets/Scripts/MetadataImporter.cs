namespace Spritesheet
{
    using System.IO;
    using UnityEditor.Experimental.AssetImporters;
    using UnityEditor;
    using UnityEngine;

    // Blender sprite sheet
    [ScriptedImporter(1, "bss")]
    public class MetadataImporter : ScriptedImporter
    {
        public override void OnImportAsset(AssetImportContext ctx)
        {
            string text = File.ReadAllText(ctx.assetPath);
            JsonMetadata parsed = JsonUtility.FromJson<JsonMetadata>(text);
            if (!parsed.Valid)
            {
                Debug.LogError("Invalid Blender spritesheet metadata");
                return;
            }
            SpritesheetMetadata metadata = ScriptableObject.CreateInstance<SpritesheetMetadata>();
            metadata.InitFromBss(parsed);

            ctx.AddObjectToAsset("metadata", metadata);
            ctx.SetMainObject(metadata);

            AssetDatabase.SaveAssets();
        }
    }
}