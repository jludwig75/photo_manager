#!/usr/bin/env python3
from datetime import datetime
import exifread
import os
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import time


def loadImageExifData(imageFileName):
    try:
        exifData = {}
        image = Image.open(imageFileName)
        if not image:
            return None
        exifData['resolution'] = f'{image.width}x{image.height}'
        exifData['format'] = image.format_description
        exifData['format_mimetype'] = image.get_format_mimetype()
        exifdata = image.getexif()
        if os.path.isfile(imageFileName):
            with open(imageFileName, 'rb') as imageFile:
                tags = exifread.process_file(imageFile)
            if tags:
                for tag in tags:
                    tagValue = tags[tag]

                    if tag.lower() == 'image exifoffset':
                        continue

                    if tag.lower().startswith('image tag '):
                        continue

                    if 'padding' in tag.lower():
                        continue

                    parts = tag.split()
                    if len(parts) > 1 and parts[0].lower() == 'image':
                        tag = tag[6:]
                    exifData[tag] = tagValue.printable

        if not exifdata:
            return exifData
        for tag_id in exifdata:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'ExifOffset':
                continue
            data = exifdata.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                try:
                    data = data.decode('utf-8')
                except:
                    continue
            exifData[tag] = data
        for tag, value in exifData.items():
            if tag.lower() == 'datetime':
                dt = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                if dt is None:
                    continue
                exifData[tag] = time.mktime(dt.timetuple())
        if 'DateTime' in exifData:
            exifData['image_date'] = exifData['DateTime']
            del exifData['DateTime']
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