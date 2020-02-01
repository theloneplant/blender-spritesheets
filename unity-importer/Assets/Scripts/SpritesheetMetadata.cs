using System;
using System.Collections.Generic;
using UnityEngine;

namespace Spritesheet
{
    // Probably better to deserialize to an intermediate format and 
    // then construct the final scriptable with support for
    // dictionaries and vector types and such
    [Serializable]
    public class SpritesheetMetadata : ScriptableObject
    {
        public int tileWidth;
        public int tileHeight;
        public List<Animation> animations = new List<Animation>();

        public bool Valid
        {
            get
            {
                bool valid = true;
                foreach (Animation anim in animations)
                {
                    valid &= anim.Valid;
                }
                return valid && tileWidth > 0 && tileHeight > 0 && animations.Count > 0;
            }
        }
    }

    [Serializable]
    public struct Animation
    {
        public string name;
        public int end;

        public bool Valid => name != null && end > -1;
    }
}
