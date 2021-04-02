from hashlib import md5
from PIL import Image as pilImage
from wand.image import Image

reference = "39bcb3ef04696298430ca84b7ff2d6fa"
with open("test.svg") as _f:
    check = md5(_f.read().encode()).hexdigest()
if check != reference:
    print("test.svg failed integrity check.")
    raise RuntimeError

# Everything with ImageMagick
with Image(filename="./test.svg") as original:

    # Providing only ncolors
    with original.clone() as image:
        image.kmeans(number_colors=3, max_iterations=100, tolerance=0.1)
        image.save(filename="quantized-test.png")

    # Providing seed colors
    with original.clone() as image:
        image.artifacts["kmeans:seed-colors"] = "#f9cf02;#da2032;#ffd900"
        image.kmeans(number_colors=3, max_iterations=100, tolerance=0.1)
        image.save(filename="quantizedSeeded-test.png")

# Rasterize with ImageMagick, quantize with Pillow
