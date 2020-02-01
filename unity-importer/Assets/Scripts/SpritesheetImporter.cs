namespace Spritesheet
{
    using System.Collections.Generic;
    using System.IO;
    using UnityEditor;
    using UnityEngine;

    internal class SpritesheetImporter : AssetPostprocessor
    {
        // Where to let the user change this? 
        public SpriteAlignment alignment = SpriteAlignment.Center;

        // Maps SpriteAlignment to pivot
        private readonly Vector2[] pivots = new Vector2[]
        {
            // Center
            new Vector2(0.5f, 0.5f),
            // TopLeft
            new Vector2(0.0f, 1.0f),
            // TopCenter
            new Vector2(0.5f, 1.0f),
            // TopRight
            new Vector2(1.0f, 1.0f),
            // LeftCenter
            new Vector2(0.0f, 0.5f),
            // RightCenter
            new Vector2(1.0f, 0.5f),
            // BottomLeft
            new Vector2(0.0f, 0.0f),
            // BottomCenter
            new Vector2(0.5f, 0.0f),
            // BottomRight
            new Vector2(1.0f, 0.0f),

            // Custom is invalid, just default to center
            new Vector2(0.5f, 0.5f),
        };

        private void OnPreprocessTexture()
        {
            string parent = Directory.GetParent(assetPath).ToString();
            string name = Path.GetFileNameWithoutExtension(assetPath);
            string query = string.Format("{0} t:SpritesheetMetadata", name);
            string[] found = AssetDatabase.FindAssets(query, new string[] { parent });

            foreach (string guid in found)
            {
                string path = AssetDatabase.GUIDToAssetPath(guid);
                SpritesheetMetadata metadata = AssetDatabase.LoadAssetAtPath<SpritesheetMetadata>(path);
                if (metadata.name != name)
                {
                    continue;
                }

                var importer = assetImporter as TextureImporter;
                Vector2Int size = importer.TextureSize();

                int tilesX = size.x / metadata.tileSize.x;
                var tiles = new List<SpriteMetaData>();
                int previousStart = 0;
                foreach (KeyValuePair<string, int> pair in metadata.animations)
                {
                    int endFrame = pair.Value;
                    for (int i = previousStart; i < endFrame; i++)
                    {
                        int x = i % tilesX;
                        int y = i / tilesX;
                        var dims = new Vector2(metadata.tileSize.x, metadata.tileSize.y);
                        var rect = new Rect(new Vector2(x, y) * dims, dims);
                        tiles.Add(new SpriteMetaData
                        {
                            name = string.Format("{0}{1}", pair.Key, i - previousStart),
                            border = Vector4.zero,
                            alignment = (int)alignment,
                            pivot = pivots[(int)alignment],
                            rect = rect,
                        });
                    }
                    previousStart = endFrame;
                }

                importer.spriteImportMode = SpriteImportMode.Multiple;
                importer.spritesheet = tiles.ToArray();
            }
        }

        private void OnPostprocessTexture(Texture2D tex)
        {
            var binding = new EditorCurveBinding
            {
                type = typeof(SpriteRenderer),
                path = "",
                propertyName = "m_Sprite"
            };
            Object[] sprites = AssetDatabase.LoadAllAssetRepresentationsAtPath(assetPath);
            var keys = new ObjectReferenceKeyframe[sprites.Length];
            for (int i = 0; i < sprites.Length; i++)
            {
                keys[i] = new ObjectReferenceKeyframe
                {
                    time = i,
                    value = sprites[i],
                };
            }
            var clip = new AnimationClip
            {
                frameRate = 60
            };
            AnimationUtility.SetObjectReferenceCurve(clip, binding, keys);

            string path = Path.ChangeExtension(assetPath, "anim");
            AssetDatabase.CreateAsset(clip, path);
        }
    }
}
