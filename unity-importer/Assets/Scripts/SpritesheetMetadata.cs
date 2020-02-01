using System;
using System.Collections.Generic;
using UnityEngine;

namespace Spritesheet
{
    public class SpritesheetMetadata : ScriptableObject
    {
        public Vector2Int tileSize;
        public int frameRate;
        public Dictionary<string, int> animations = new Dictionary<string, int>();

        internal void InitFromBss(JsonMetadata json)
        {
            tileSize = new Vector2Int(json.tileWidth, json.tileHeight);
            frameRate = json.frameRate;
            foreach (JsonAnimation anim in json.animations)
            {
                animations.Add(anim.name, anim.end);
            }
        }
    }

    [Serializable]
    internal class JsonMetadata
    {
        public int tileWidth = 0;
        public int tileHeight = 0;
        public int frameRate = 0;
        public List<JsonAnimation> animations = null;

        public bool Valid => animations != null &&
                    ValidAnimations &&
                    tileWidth > 0 &&
                    tileHeight > 0 &&
                    frameRate > 0;

        private bool ValidAnimations
        {
            get
            {
                bool valid = true;
                foreach (JsonAnimation anim in animations)
                {
                    valid &= anim.Valid;
                }
                return valid;
            }
        }
    }

    [Serializable]
    internal class JsonAnimation
    {
        public string name = null;
        public int end = 0;

        public bool Valid => name != null && end > -1;
    }
}
