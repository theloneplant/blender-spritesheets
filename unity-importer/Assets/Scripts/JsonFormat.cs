using System.Collections.Generic;
using System;

namespace Spritesheet
{
    [Serializable]
    internal class JsonFormat
    {
        public int tileWidth;
        public int tileHeight;
        public List<Animation> animations = new List<Animation>();
    }

    [Serializable]
    internal class Animation
    {
        public string name;
        public int start;
    }
}
