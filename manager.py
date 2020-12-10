from datetime import datetime
from dumpexif import loadImageExifData
from imgutils import generateThumbNail
import os

class FileSystemEntity:
    def __init__(self, name, containerPath):
        self._name = name
        self._path = os.path.join(containerPath, name)
    @property
    def name(self):
        return self._name
    @property
    def path(self):
        return self._path

class FileSytemContainer(FileSystemEntity):
    def __init__(self, name, containerPath):
        super().__init__(name, containerPath)
    def fullPath(self, itemName):
        return os.path.join(self.path, itemName)

class Image(FileSystemEntity):
    def __init__(self, name, folderPath):
        super().__init__(name, folderPath)
        self._folderPath = folderPath
    @property
    def stats(self):
        stat = os.stat(self.path)
        stats = {
                'name': self.name,
                'file_date': stat.st_ctime,
                'size_bytes': stat.st_size
               }
        exifData = loadImageExifData(self.path)
        if exifData is not None:
            stats.update(exifData)
        return stats
    @property
    def thumbnailPath(self):
        thumbnailDir = os.path.join(self._folderPath, 'thumbnails')
        if not os.path.exists(thumbnailDir):
            os.mkdir(thumbnailDir)
        thumbnailPath = os.path.join(thumbnailDir, self.name)
        if not os.path.exists(thumbnailPath):
            generateThumbNail(self.path, thumbnailDir)
            if not os.path.exists(thumbnailPath):
                return self.path
        return thumbnailPath
    @property
    def content(self):
        return open(self.path, 'rb')
    @property
    def thumbnail(self):
        return open(self.path, 'rb')

class Folder(FileSytemContainer):
    def __init__(self, name, rootPath):
        super().__init__(name, rootPath)
        self._name = name
    @property
    def stats(self):
        stat = os.stat(self.path)
        size_bytes = 0
        images = self.images
        for imageName in images:
            size_bytes += Image(imageName, self.path).stats['size_bytes']
        return {
                'name': self._name,
                "create_time": stat.st_ctime,
                'size_bytes': size_bytes,
                'image_count': len(images)
                }
    @property
    def images(self):
        paths = [path for path in os.listdir(self.path) if self._isImageFile(self.fullPath(path))]
        paths.sort()
        return paths
    def image(self, imageName):
        if not self._isImageFile(self.fullPath(imageName)):
            return None
        return Image(imageName, self.path)
    def addImage(self, imageName, writer):
        if os.path.exists(self.fullPath(imageName)):
            return Image(imageName, self.path)
        with open(self.fullPath(imageName), 'wb') as imageFile:
            writer(imageFile)
        return Image(imageName, self.path)
    def _isImageFile(self, fileName):
        if not os.path.isfile(fileName):
            return False
        # TODO: at least check the file extension too.
        return True
        

class PhotoManager(FileSytemContainer):
    def __init__(self, rootPath):
        super().__init__('', rootPath)
    @property
    def folders(self):
        folders = [path for path in os.listdir(self.path) if os.path.isdir(self.fullPath(path))]
        folders.sort()#key=lambda x: -Folder(x, self.path).stats['create_time'])
        return folders
    def folder(self, folderName):
        if not os.path.isdir(self.fullPath(folderName)):
            return None
        return Folder(folderName, self.path)
    def addFolder(self, folderName):
        if os.path.exists(self.fullPath(folderName)):
            return None
        os.mkdir(self.fullPath(folderName))
        return Folder(folderName, self.path)
    def suggestNewFolderName(self):
        now = datetime.now()
        dateString = now.strftime('%Y-%m-%d')
        newFolderName = f'New Folder {dateString}'
        if not os.path.exists(self.fullPath(newFolderName)):
            return newFolderName
        timeString = now.strftime('%H:%M:%S')
        newFolderName += f' {timeString}'
        if not os.path.exists(self.fullPath(newFolderName)):
            return newFolderName
        i = 0
        while os.path.exists(self.fullPath(f'{newFolderName} {i}')):
            i += 1
        return f'{newFolderName} {i}'
