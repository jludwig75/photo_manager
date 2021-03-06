import os
from mimetypesdb import isImageFile
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

def fixImageOrientation(image, orientation):
    val = [orientation]
    if 5 in val:
        val += [4,8]
    if 7 in val:
        val += [4, 6]
    if 3 in val:
        image = image.transpose(Image.ROTATE_180)
    if 4 in val:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if 6 in val:
        image = image.transpose(Image.ROTATE_270)
    if 8 in val:
        image = image.transpose(Image.ROTATE_90)
    return image

def generateThumbNail(imagePath, destinationFolder):
    print(f'Generating thumbnail of {imagePath}...')
    if not isImageFile(imagePath):
        # TODO: Add video thumbnail support
        print(f'Not creating thumbnail of {imagePath}. It is not a known image file format')
        return False
    try:
        image = Image.open(imagePath)
        if not image:
            print(f'Unable to open image {imagePath} to create thumbnail')
            return False

        # Save off the original image orientation
        orientation = getOrientation(image)

        # Generate thumbnail image
        image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

        # Fix thumbnail image orientation, because the
        # orientation in the EXIF data is not in the thumbnail.
        image = fixImageOrientation(image, orientation)

        # Save the thumbnail
        imageFileName = imagePath
        if '/' in imageFileName:
            imageFileName = imageFileName[imageFileName.rfind('/')+1:]
        thumbnailPath = os.path.join(destinationFolder, imageFileName)
        image.save(thumbnailPath, quality=90)
        return True
    except Exception as e:
        print(f'Exception creating thumbnail for image {imagePath}: {e}')
        return False



if __name__ == "__main__":
    generateThumbNail(sys.argv[1], 'thumbnails')