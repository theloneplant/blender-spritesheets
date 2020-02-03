namespace Spritesheet
{
    using System.Collections.Generic;
    using System.IO;
    using UnityEditor;
    using UnityEngine;

    internal class SpritesheetImporter : AssetPostprocessor
    {
        private void OnPreprocessTexture()
        {
            SpritesheetMetadata metadata = GetMetadata(assetPath);
            if (metadata == null)
            {
                Debug.Log("No spritesheet metadata at preprocess");
                return;
            }

            var importer = assetImporter as TextureImporter;
            Vector2Int size = importer.TextureSize();

            int tilesX = size.x / metadata.tileWidth;
            int tilesY = size.y / metadata.tileHeight;
            int tileCount = tilesX * tilesY;

            var tiles = new List<SpriteMetaData>();
            int previousStart = 0;
            foreach (Animation anim in metadata.animations)
            {
                for (int i = previousStart; i < anim.end; i++)
                {
                    int x = i % tilesX;
                    int y = i / tilesX;
                    var dims = new Vector2(metadata.tileWidth, metadata.tileHeight);
                    var rect = new Rect(new Vector2(x, y) * dims, dims);
                    tiles.Add(new SpriteMetaData
                    {
                        name = string.Format("{0}{1}", anim.name, i - previousStart),
                        border = Vector4.zero,
                        alignment = (int)SpriteAlignment.Center,
                        pivot = Vector2.one / 2f,
                        rect = rect,
                    });
                }
                previousStart = anim.end;
            }

            importer.spriteImportMode = SpriteImportMode.Multiple;
            importer.spritesheet = tiles.ToArray();
        }

        private static void OnPostprocessAllAssets(
            string[] importedAssets,
            string[] deletedAssets,
            string[] movedAssets,
            string[] movedFromAssetPaths)
        {
            foreach (string asset in importedAssets)
            {
                Texture2D tex = AssetDatabase.LoadAssetAtPath<Texture2D>(asset);
                if (tex == null)
                {
                    continue;
                }

                SpritesheetMetadata metadata = GetMetadata(asset);
                if (metadata == null)
                {
                    Debug.Log("No spritesheet metadata at postprocess");
                    return;
                }

                int previousStart = 0;
                foreach (Animation anim in metadata.animations)
                {
                    var binding = new EditorCurveBinding
                    {
                        type = typeof(SpriteRenderer),
                        path = "",
                        propertyName = "m_Sprite"
                    };
                    Object[] sprites = AssetDatabase.LoadAllAssetRepresentationsAtPath(asset);
                    int count = anim.end - previousStart;
                    var keys = new ObjectReferenceKeyframe[count];
                    for (int i = 0; i < count; i++)
                    {
                        keys[i] = new ObjectReferenceKeyframe
                        {
                            time = i,
                            value = sprites[i + previousStart],
                        };
                    }
                    var clip = new AnimationClip
                    {
                        frameRate = metadata.frameRate,
                    };
                    AnimationUtility.SetObjectReferenceCurve(clip, binding, keys);

                    DirectoryInfo parent = Directory.GetParent(asset);
                    string path = Path.Combine(parent.ToString(), string.Format("{0}.anim", anim.name));
                    AssetDatabase.CreateAsset(clip, path);

                    previousStart = anim.end;
                }
            }
        }

        private static SpritesheetMetadata GetMetadata(string path)
        {
            string metadataFilepath = Path.ChangeExtension(path, "bss");
            string text = File.ReadAllText(metadataFilepath);
            SpritesheetMetadata metadata = JsonUtility.FromJson<SpritesheetMetadata>(text);
            return metadata.Valid ? metadata : null;
        }
    }
}
