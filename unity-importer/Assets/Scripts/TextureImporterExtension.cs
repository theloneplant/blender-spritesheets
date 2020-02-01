using System.Reflection;
using UnityEditor;
using UnityEngine;

namespace Spritesheet
{
    internal static class TextureImporterExtension
    {
        internal static Vector2Int TextureSize(this TextureImporter importer)
        {
            MethodInfo method = typeof(TextureImporter).GetMethod(
                "GetWidthAndHeight",
                BindingFlags.NonPublic | BindingFlags.Instance
            );
            object[] outputs = new object[] { 0, 0 };
            method.Invoke(importer, outputs);
            return new Vector2Int
            {
                x = (int)outputs[0],
                y = (int)outputs[1],
            };
        }
    }
}
