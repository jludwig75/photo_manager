import cherrypy
import cherrypy.lib
from mimetypesdb import getMimeType
import json
from manager import PhotoManager
import os


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
    def index(self, folder_name, image_name, userContext=None):
        stats = self._getImage(folder_name, image_name).stats
        if userContext is not None:
            stats['userContext'] = userContext
        return json.dumps(stats)
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def content(self, folder_name, image_name):
        image = self._getImage(folder_name, image_name)
        return cherrypy.lib.static.serve_file(os.path.abspath(image.path), _getImageMimeType(image.name))
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def thumbnail(self, folder_name, image_name):
        image = self._getImage(folder_name, image_name)
        return cherrypy.lib.static.serve_file(os.path.abspath(image.thumbnailPath), _getImageMimeType(image.name))
    def _getImage(self, folderName, imageName):
        folder = self._photoManager.folder(folderName)
        if folder is None:
            raise cherrypy.HTTPError(status=400, message='Folder {0} not found'.format(folderName))
        image = folder.image(imageName)
        if image is None:
            raise cherrypy.HTTPError(status=400, message='Image {0} not found in folder {1}'.format(imageName, folderName))
        return image

class Folder(object):
    def __init__(self, photoManager):
        self._photoManager = photoManager

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST'])
    def index(self, folder_name):
        if cherrypy.request.method == 'GET':
            return json.dumps(self._getFolder(folder_name).stats)
        else: # POST
            folder = self._photoManager.addFolder(folder_name)
            if folder is None:
                raise cherrypy.HTTPError(status=500, message=f'Error creating folder {folder_name}')
            return 'OK'

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

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST'])
    def images(self, folder_name, **kwargs):
        if cherrypy.request.method == 'GET':
            return json.dumps(self._getFolder(folder_name).images)
        else: # POST
            if not 'fileToUpload' in kwargs:
                raise cherrypy.HTTPError(status=400, message='Missing argument "fileToUpload"')
            fileToUpload = kwargs['fileToUpload']
            self._uploadFile(folder_name, fileToUpload)
    
    def _getFolder(self, folderName):
        folder = self._photoManager.folder(folderName)
        if folder is None:
            raise cherrypy.HTTPError(status=400, message='Folder {0} not found'.format(folderName))
        return folder

class FolderManager(object):
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
