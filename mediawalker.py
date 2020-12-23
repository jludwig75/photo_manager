from mimetypesdb import hasMediaFileExtension
import os


class MediaFileWalker:
    def walk(self, mediaRoot, onMediaCallback):
        for path in os.listdir(mediaRoot):
            dirPath = os.path.join(mediaRoot, path)
            if not os.path.isdir(dirPath):
                continue
            for childPath in os.listdir(dirPath):
                filePath = os.path.join(dirPath, childPath)
                if not os.path.isfile(filePath):
                    continue
                if not hasMediaFileExtension(filePath):
                    continue
                onMediaCallback(filePath)