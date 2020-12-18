import requests
import urllib


class MediaClient:
    def __init__(self, destinationServer):
        self._destinationServer = destinationServer
    def folderExists(self, folderName):
        r = requests.get(self._encodePath(folderName))
        return r.status_code == 200
    def createFolder(self, folderName):
        r = requests.post(self._encodePath(folderName))
        return r.status_code == 200
    def imageExists(self, folderName, imageName):
        r = requests.get(self._encodePath(folderName, imageName))
        return r.status_code == 200
    def uploadImage(self, folderName, imageName, fileHandle):
        r = requests.post(self._encodePath(folderName) + 'images/', files = { 'fileToUpload':  fileHandle} )
        return r.status_code == 200
    def _encodePath(self, folderName, imageName = None):
        path = f'http://{self._destinationServer}/folders/{urllib.parse.quote(folderName)}/'
        if imageName:
            path += f'images/{urllib.parse.quote(imageName)}/'
        return path
