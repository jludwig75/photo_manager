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
    def index(self, folder_name):
        return json.dumps(self._getFolder(folder_name).stats)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def images(self, folder_name):
        return json.dumps(self._getFolder(folder_name).images)
    
    def _getFolder(self, folderName):
        folder = self._photoManager.folder(folderName)
        if folder is None:
            raise cherrypy.HTTPError(status=400, message='Folder {0} not found'.format(folderName))
        return folder

class FolderManager(object):
    def __init__(self, photoManager):
        self._photoManager = photoManager
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
