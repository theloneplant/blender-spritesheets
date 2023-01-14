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
            foreach (Animation anim in metadata.animations)
            {
                for (int i = anim.start; i < anim.start + anim.count; i++)
                {
                    int x = i % tilesX;
                    int y = i / tilesX;
                    var dims = new Vector2(metadata.tileWidth, metadata.tileHeight);
                    var rect = new Rect(new Vector2(x, (tilesY - 1) - y) * dims, dims);
                    tiles.Add(new SpriteMetaData
                    {
                        name = string.Format("{0}-{1}", anim.name, i - anim.start),
                        border = Vector4.zero,
                        alignment = (int)SpriteAlignment.Center,
                        pivot = Vector2.one / 2f,
                        rect = rect,
                    });
                }
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
                Debug.Log("Asset being loaded:" + asset);
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

                Object[] sprites = AssetDatabase.LoadAllAssetRepresentationsAtPath(asset);
                // get sprite names in order
                Dictionary<string, int> names = new();
                int nameIndex = 0;
                foreach (Object sprite in sprites) {
                    string name = sprite.name.Split('-')[0];
                    if (!names.ContainsKey(name)) {
                        names.Add(name, nameIndex++);
                    }
                }
                Debug.Log("Ordered names found: " + names);

                // sort animations by sprite names
                metadata.animations.Sort((x, y) => names[x.name].CompareTo(names[y.name]));
                
                int previousStart = 0;
                foreach (Animation anim in metadata.animations)
                {
                    var binding = new EditorCurveBinding
                    {
                        type = typeof(SpriteRenderer),
                        path = "",
                        propertyName = "m_Sprite"
                    };
                    var keys = new ObjectReferenceKeyframe[anim.count];
                    for (int i = 0; i < anim.count; i++)
                    {
                        if (sprites.Length == 0) break;

                        keys[i] = new ObjectReferenceKeyframe
                        {
                            time = (float)i / metadata.frameRate,
                            value = sprites[i + previousStart],
                        };
                    }
                    Debug.Log("Found " + sprites.Length + " sprites to animate.");
                    var clip = new AnimationClip
                    {
                        frameRate = metadata.frameRate,
                    };
                    AnimationUtility.SetObjectReferenceCurve(clip, binding, keys);

                    DirectoryInfo parent = Directory.GetParent(asset);
                    Debug.Log("Application Datapath:" + Application.dataPath);
                    // Remove path to project
                    string pathFromProject = parent.ToString().Substring(Application.dataPath.Length - 6);
                    string path = Path.Combine(pathFromProject, string.Format("{0}.anim", anim.name));
                    Debug.Log("Creating at path:" + path);
                    AssetDatabase.CreateAsset(clip, path);
                    previousStart += anim.count;
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
