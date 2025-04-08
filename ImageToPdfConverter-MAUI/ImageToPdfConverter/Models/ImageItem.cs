using System;

namespace ImageToPdfConverter.Models
{
    public class ImageItem
    {
        public string Id { get; set; } = Guid.NewGuid().ToString();
        public string FilePath { get; set; }
        public string FileName { get; set; }
        public ImageSource ImageSource { get; set; }
    }
}
