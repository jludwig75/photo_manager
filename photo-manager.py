#!/usr/bin/env python3
import cherrypy
import os
from manager import PhotoManager
from mediaserver import FolderManager

def loadHtmlFile(pageName):
    with open(os.path.join('html', pageName)) as webPage:
        return webPage.read()

class Root(object):
    def __init__(self, photoManager):
        self._photoManager = photoManager

    @cherrypy.expose
    def index(self):
        return loadHtmlFile('index.html')

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
    @cherrypy.tools.allow(methods=['POST'])
    def upload(self, **kwargs):
        if not 'fileToUpload' in kwargs:
            raise cherrypy.HTTPError(status=400, message='Missing argument "fileToUpload"')
        if not 'folder' in kwargs:
            raise cherrypy.HTTPError(status=400, message='Missing argument "folder"')
        fileToUpload = kwargs['fileToUpload']
        folder = kwargs['folder']
        self._uploadFile(folder, fileToUpload)


if __name__ == "__main__":
    photoManager = PhotoManager('photos')

    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./html')
        }
    }

    cherrypy.config.update({'server.socket_port': 8086})
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.tree.mount(FolderManager(photoManager), '/folders', conf)
    cherrypy.quickstart(Root(photoManager), '/', conf)
