import cherrypy
import cherrypy.lib
from mimetypesdb import getMimeType, isImageFile, isVideoFile
import json
from photomanager import PhotoManager
import os
import urllib


def _getImageMimeType(imageName):
    parts = os.path.splitext(imageName)
    if len(parts) < 2:
        return ''
    extension = parts[-1][1:].lower()
    mimeType = getMimeType(extension)
    if mimeType is None:
        return 'image/unknown'
    return mimeType


class Image(object):
    def __init__(self, photoManager):
        self._photoManager = photoManager
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'DELETE']) # Post could be used for user comments/tags
    def index(self, folder_name, image_name, userContext=None):
        if cherrypy.request.method == 'GET':
            stats = self._getImage(folder_name, image_name).stats
            stats['media_type'] = 'unknown'
            if isImageFile(image_name):
                stats['media_type'] = 'image'
            elif isVideoFile(image_name):
                stats['media_type'] = 'video'
            if userContext is not None:
                stats['userContext'] = userContext
            stats['thumbnailPath'] = urllib.parse.quote(stats['thumbnailPath'])
            stats['path'] = urllib.parse.quote(stats['path'])
            return json.dumps(stats)
        elif cherrypy.request.method == 'DELETE':
            image = self._getImage(folder_name, image_name)
            image.delete()
    def _getImage(self, folderName, imageName):
        folder = self._photoManager.folder(folderName)
        if folder is None:
            raise cherrypy.HTTPError(status=404, message='Folder {0} not found'.format(folderName))
        image = folder.image(imageName)
        if image is None:
            raise cherrypy.HTTPError(status=404, message='Image {0} not found in folder {1}'.format(imageName, folderName))
        return image

class Folder(object):
    def __init__(self, photoManager):
        self._photoManager = photoManager

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST', 'DELETE'])
    def index(self, folder_name):
        if cherrypy.request.method == 'GET':
            return json.dumps(self._getFolder(folder_name).stats)
        elif cherrypy.request.method == 'POST':
            folder = self._photoManager.addFolder(folder_name)
            if folder is None:
                raise cherrypy.HTTPError(status=500, message=f'Error creating folder {folder_name}')
            return 'OK'
        elif cherrypy.request.method == 'DELETE':
            if not self._photoManager.deleteFolder(folder_name):
                raise cherrypy.HTTPError(status=500, message=f'Error deleting folder {folder_name}')

    def _uploadFile(self, folder, fileToUpload):
        uploadFolder = self._photoManager.folder(folder)
        if uploadFolder is None:
            self._photoManager.addFolder(folder)
            uploadFolder = self._photoManager.folder(folder)
            if uploadFolder is None:
                raise cherrypy.HTTPError(status=404, message=f'Upload folder {folder} not found')
        class ImageWriter:
            def __init__(self, fileToUpload):
                self.fileToUpload = fileToUpload
            def writeImage(self, handle):
                while True:
                    data = fileToUpload.file.read(8192)
                    if not data:
                        break
                    handle.write(data)
        writer = ImageWriter(fileToUpload)
        img = uploadFolder.addImage(fileToUpload.filename, writer.writeImage)
        if img is None:
            print(f'Image {fileToUpload.filename} already exists in {folder}')
            raise cherrypy.HTTPError(status=409, message=f'Image {fileToUpload.filename} is already in {folder}')
        uploadFolder.requestThumbNail(img)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST'])
    def images(self, folder_name, **kwargs):
        if cherrypy.request.method == 'GET':
            imageList = []
            folder = self._getFolder(folder_name)
            for imageName in folder.images:
                image = folder.image(imageName)
                imageList.append({
                                    'name': imageName,
                                    'path': urllib.parse.quote(image.path),
                                    'thumbnailPath': urllib.parse.quote(image.thumbnailPath)
                                 })
            return json.dumps(imageList)
        else: # POST
            if not 'fileToUpload' in kwargs:
                raise cherrypy.HTTPError(status=400, message='Missing argument "fileToUpload"')
            fileToUpload = kwargs['fileToUpload']
            self._uploadFile(folder_name, fileToUpload)
    
    def _getFolder(self, folderName):
        folder = self._photoManager.folder(folderName)
        if folder is None:
            raise cherrypy.HTTPError(status=404, message='Folder {0} not found'.format(folderName))
        return folder

class MediaServer(object):
    def __init__(self, photoRoot):
        self._photoManager = PhotoManager(photoRoot)
        self.folders = Folder(self._photoManager)
        self.images = Image(self._photoManager)

    def _cp_dispatch(self, vpath):
            if len(vpath) == 1:
                cherrypy.request.params['folder_name'] = vpath.pop()
                return self.folders

            if len(vpath) == 2:
                cherrypy.request.params['folder_name'] = vpath.pop(0)  # /band name/
                return self.folders

            if len(vpath) >= 3:
                cherrypy.request.params['folder_name'] = vpath.pop(0)  # /band name/
                vpath.pop(0) # /images/
                cherrypy.request.params['image_name'] = vpath.pop(0) # /album title/
                return self.images

            return vpath
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def index(self):
        return json.dumps(self._photoManager.folders)
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def suggest_folder_name(self):
        return self._photoManager.suggestNewFolderName()
