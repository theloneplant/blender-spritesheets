using System;
using System.Collections.Generic;

namespace Spritesheet
{
    [Serializable]
    public class SpritesheetMetadata
    {
        public string name;
        public int tileWidth;
        public int tileHeight;
        public int frameRate;
        public List<Animation> animations;

        public bool Valid => animations != null &&
                    ValidAnimations &&
                    tileWidth > 0 &&
                    tileHeight > 0 &&
                    frameRate > 0 &&
                    animations.Count > 0;

        private bool ValidAnimations
        {
            get
            {
                bool valid = true;
                foreach (Animation anim in animations)
                {
                    valid &= anim.Valid;
                }
                return valid;
            }
        }
    }

    [Serializable]
    public struct Animation
    {
        public string name;
        public int start;
        public int count;

        public bool Valid => name != null && start > -1;
    }
}
