from os import path
from PIL import Image, ImageStat


folder = path.dirname(__file__)
filename = 'xlgddaexman21.jpg'

image = Image.open(path.join(folder, filename))

stats = ImageStat.Stat(image)
print(stats.median)  # [89, 76,100]
target_color = (89, 150, 100)
for x in range(image.size[0]):
    for y in range(image.size[1]):
        pixel = image.getpixel((x, y))
        # modify pixel
        newcolor = ()
        image.putpixel((x, y), newcolor)
