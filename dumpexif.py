#!/usr/bin/env python3
from datetime import datetime
import exifread
import json
import os
from PIL import Image
from PIL.ExifTags import TAGS
import pprint
import sys
import time


def getImageAttributes(imageFileName):
    image = Image.open(imageFileName)
    if not image:
        return None
    return {
            'resolution': image.size,
            'format': image.format_description,
            'format_mimetype': image.get_format_mimetype()
           }

def getExitData(imageFileName):
    with open(imageFileName, 'rb') as imageFile:
        tags = exifread.process_file(imageFile, details=False)
    if not tags:
        return None

    categories = {}
    for tag in tags:
        parts = tag.split()
        if len(parts) == 1:
            category = ''
        else:
            strippedTag = ' '.join(parts[1:])
            category = parts[0]
        if category not in categories:
            categories[category] = {}
        originalValue = tags[tag]
        value = originalValue
        value = value.values if isinstance(value.values, str) else value.values[0] if len(value.values) == 1 else value.values
        if strippedTag.lower() in ['gpslatitude', 'gpslongitude']:
            locParts = [float(v) for v in value]
            pos = locParts[0]
            dec = 0
            for v in reversed(locParts[1:]):
                dec += v
                dec /= 60
            value = round(pos + dec, 8)
        elif 'version' in strippedTag.lower() and isinstance(value, list):
            versionStrings = [str(v) for v in value]
            value = '.'.join(versionStrings)
        elif strippedTag.lower() == 'gpstimestamp' and len(value) == 3:
            value = '%02d:%02d:%02d' % tuple(value)
        else:
            if hasattr(originalValue, 'printable') and str(value) != originalValue.printable:
                value = originalValue.printable
        categories[category][strippedTag] = value

    if 'GPS' in categories.keys():
        gpsData = categories['GPS']
        if 'GPSLatitude' in gpsData and 'GPSLatitudeRef' in gpsData and 'GPSLongitude' in gpsData and 'GPSLongitudeRef' in gpsData:
            gpsData['Location'] = f"{gpsData['GPSLatitude']}{gpsData['GPSLatitudeRef']},{gpsData['GPSLongitude']}{gpsData['GPSLongitudeRef']}"
            del gpsData['GPSLatitude']
            del gpsData['GPSLatitudeRef']
            del gpsData['GPSLongitude']
            del gpsData['GPSLongitudeRef']

    return categories


def loadImageExifData(imageFileName):
    if not os.path.isfile(imageFileName):
        return None
    exifData = getExitData(imageFileName)
    if not exifData:
        return None
    values = {}
    for category, entries in exifData.items():
        if category.lower() == 'image':
            category = None
        for key, value in entries.items():
            if category:
                key = ' '.join((category, key))
            if isinstance(value, exifread.utils.Ratio):
                value = str(value)
            values[key] = value
    return values


if __name__ == "__main__":
    for fileName in sys.argv[1:]:
        exifData = getExitData(fileName)
        if exifData is None:
            print(f'Failed to get exif data for {fileName}')
            continue
        pprint.pprint(exifData)
