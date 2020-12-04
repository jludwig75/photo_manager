from PIL import Image
from PIL.ExifTags import TAGS
import sys


def loadImageExifData(imageFileName):
    try:
        exifData = {}
        image = Image.open(imageFileName)
        if not image:
            return None
        exifdata = image.getexif()
        if not exifdata:
            return None
        for tag_id in exifdata:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                try:
                    data = data.decode('utf-8')
                except:
                    continue
            exifData[tag] = data
        return exifData
    except:
        return None



if __name__ == "__main__":
    for fileName in sys.argv[1:]:
        exifData = loadImageExifData(fileName)
        if exifData is None:
            print(f'Failed to get exif data for {fileName}')
            continue
        for tag, data in exifData.items():
            print(f"{tag:25}: {data}")