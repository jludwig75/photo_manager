#!/usr/bin/env python3
import cherrypy
import os
from manager import PhotoManager
from mediaserver import FolderManager

def loadHtmlFile(pageName):
    with open(os.path.join('html', pageName)) as webPage:
        return webPage.read()

class Root(object):
    @cherrypy.expose
    def index(self):
        return loadHtmlFile('index.html')

    # def _uploadFile(self, fileToUpload):
    #     handle = self._fileManager.addImage(fileToUpload.filename)
    #     if handle == FileManager.FILE_EXISTS:
    #         return 'File {0} already exists'.format(fileToUpload.filename)
    #     elif handle == FileManager.FILE_NAME_INVALID:
    #         return 'File {0} is not a valid file name'.format(fileToUpload.filename)
    #     else:
    #         size = 0
    #         with handle:
    #             while True:
    #                 data = fileToUpload.file.read(8192)
    #                 if not data:
    #                     break
    #                 handle.write(data)
    #                 size += len(data)
    #         return 'Successfuly uploaded file {0}: size: {1} bytes, content type: {2}'.format(fileToUpload.filename, size, fileToUpload.content_type)

    # @cherrypy.expose
    # def upload(self, **kwargs):
    #     fileList = ''
    #     if cherrypy.request.method == 'GET':
    #         return loadHtmlFile('upload.html')
    #     elif cherrypy.request.method == 'POST':
    #         if 'fileToUpload' in kwargs:
    #             fileToUpload = kwargs['fileToUpload']
    #             if isinstance(fileToUpload, cherrypy._cpreqbody.Part):
    #                 message = self._uploadFile(fileToUpload)
    #                 fileList += '<p>{0}</p>'.format(message)
    #         elif 'filesToUpload' in kwargs:
    #             filesToUpload = kwargs['filesToUpload']
    #             for fileToUpload in filesToUpload:
    #                 if isinstance(fileToUpload, cherrypy._cpreqbody.Part):
    #                     message = self._uploadFile(fileToUpload)
    #                     fileList += '<p>{0}</p>\n'.format(message)
    #         else:
    #             raise cherrypy.HTTPError(status=400, message='You must provide either "fileToUpload" or "filesToUpload" argument')

    #         # return """<html>
    #         # <body>
    #         # {0}
    #         # </body>
    #         # </html>""".format(fileList)
    #         raise cherrypy.HTTPRedirect('/')
    #     else:
    #         raise cherrypy.HTTPError(status=405, message='Method %s not supported' % cherrypy.request.method)


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
    cherrypy.quickstart(Root(), '/', conf)
