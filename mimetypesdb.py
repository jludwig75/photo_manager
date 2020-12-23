#!/usr/bin/env python3

import os

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
# https://help.intelligencebank.com/hc/en-us/articles/115005575806-Image-Annotations-Supported-Formats-Mime-Types-
# https://www.sitepoint.com/mime-types-complete-list/ # Not really complete
# https://stackoverflow.com/questions/43473056/which-mime-type-should-be-used-for-a-raw-image


def _parseMimeTypesFile(mimeTypesFile):
    mimeTypesMap = {}
    for line in mimeTypesFile:
        parts = line.split()
        if len(parts) != 2:
            continue
        parts = [part.strip() for part in parts]
        extension, mimeType = parts
        if extension[0] != '.':
            continue
        if len(mimeType.split('/')) != 2:
            continue
        extension = extension[1:].lower()
        if extension in mimeTypesMap:
            # always take the first entry for a given extension
            # the mime type files have duplicate entries for
            # extensions and the first is prefered
            continue
        mimeTypesMap[extension] = mimeType
    return mimeTypesMap

_image_mime_types_map = {}
_video_mime_types_map = {}

def loadMimeTypes():
    with open('mimetypes.image') as mimeTypesFile:
        map = _parseMimeTypesFile(mimeTypesFile)
        if map is not None:
            _image_mime_types_map.update(map)
    with open('mimetypes.video') as mimeTypesFile:
        map = _parseMimeTypesFile(mimeTypesFile)
        if map is not None:
            _video_mime_types_map.update(map)

def getMimeType(extension):
    extension = extension.lower()
    if extension in _image_mime_types_map:
        return _image_mime_types_map[extension]
    if not extension in _video_mime_types_map:
        return None
    return _video_mime_types_map[extension]

def getFileMimeType(fileName):
    extension = _fileExtension(fileName)
    if extension is None:
        return False
    return getMimeType(extension)

def _fileExtension(fileName):
    path, ext = os.path.splitext(fileName)
    if len(ext) == 0:
        return None
    return ext[1:].lower()

def isImageFile(fileName):
    extension = _fileExtension(fileName)
    if extension is None:
        return False
    return extension in _image_mime_types_map

def isVideoFile(fileName):
    # If there is an overlap, assume it is an image file
    if isImageFile(fileName):
        return False
    extension = _fileExtension(fileName)
    if extension is None:
        return False
    return extension in _video_mime_types_map

def hasMediaFileExtension(fileName):
    return isImageFile(fileName) or isVideoFile(fileName)

loadMimeTypes()

if __name__ == "__main__":
    mapList = [ (extension, mimeType) for extension, mimeType in  _image_mime_types_map.items()]
    mapList += [ (extension, mimeType) for extension, mimeType in  _video_mime_types_map.items()]
    mapList.sort(key=lambda x: x[0])
    for extension, mimeType in mapList:
        print('{0: <10} => {1}'.format(extension, mimeType))