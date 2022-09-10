from PIL import Image, ImageFilter
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python kernaling.py image")

image = Image.open(sys.argv[1]).convert("RGB")

filteredimage = image.filter(ImageFilter.Kernel(
    kernel=[-1, -1, -1, -1, 8, -1, -1, -1, -1],
    size=(3, 3),
    scale=1
))

filteredimage.show()
