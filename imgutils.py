import os
from PIL import Image
import sys


MAX_WIDTH=150
MAX_HEIGHT=100


def scaleSize(size):
    width, height = size
    if height > MAX_HEIGHT:
        height = MAX_HEIGHT
        width = (size[0] * MAX_HEIGHT) / size[1]
    if width > MAX_WIDTH:
        width = MAX_WIDTH
        height = (size[1] * MAX_WIDTH) / size[0]
    return (int(width), int(height))

def generateThumbNail(imagePath, destinationFolder):
    image = Image.open(imagePath)
    if not image:
        return False
    newSize = scaleSize(image.size)
    image = image.resize(newSize, Image.LANCZOS)
    imageFileName = imagePath
    if '/' in imageFileName:
        imageFileName = imageFileName[imageFileName.rfind('/')+1:]
    thumbnailPath = os.path.join(destinationFolder, imageFileName)
    image.save(thumbnailPath)


if __name__ == "__main__":
    generateThumbNail(sys.argv[1], 'thumbnails')