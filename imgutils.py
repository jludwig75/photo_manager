import os
from PIL import Image
from PIL.ExifTags import TAGS
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

ORIENTATION_TAG = 274

def getOrientation(image):
    exif = image.getexif()
    if not exif:
        return None
    if not ORIENTATION_TAG in exif:
        return None
    return exif[ORIENTATION_TAG]

def generateThumbNail(imagePath, destinationFolder):
    image = Image.open(imagePath)
    if not image:
        return False
    orientation = getOrientation(image)
    if orientation:
        print(f'Image orientation: {orientation}')
    newSize = scaleSize(image.size)
    image = image.resize(newSize, Image.LANCZOS)
    imageFileName = imagePath
    if '/' in imageFileName:
        imageFileName = imageFileName[imageFileName.rfind('/')+1:]
    thumbnailPath = os.path.join(destinationFolder, imageFileName)
    val = [orientation]
    if 5 in val:
        val += [4,8]
    if 7 in val:
        val += [4, 6]
    if 3 in val:
        print("Rotating by 180 degrees.")
        image = image.transpose(Image.ROTATE_180)
    if 4 in val:
        print("Mirroring horizontally.")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if 6 in val:
        print("Rotating by 270 degrees.")
        image = image.transpose(Image.ROTATE_270)
    if 8 in val:
        print("Rotating by 90 degrees.")
        image = image.transpose(Image.ROTATE_90)
    image.save(thumbnailPath)


if __name__ == "__main__":
    generateThumbNail(sys.argv[1], 'thumbnails')