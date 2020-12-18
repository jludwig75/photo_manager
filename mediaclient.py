import json
import requests
import urllib


class MediaClient:
    def __init__(self, destinationServer):
        self._destinationServer = destinationServer
    def folders(self):
        r = requests.get(self._encodePath())
        if r.status_code != 200:
            return None
        return json.loads(r.text)
    def createFolder(self, folderName):
        r = requests.post(self._encodePath(folderName))
        return r.status_code == 200

    def images(self, folderName):
        r = requests.get(self._encodePath(folderName) + 'images/')
        if r.status_code != 200:
            return None
        return json.loads(r.text)
    def uploadImage(self, folderName, imageName, fileHandle):
        r = requests.post(self._encodePath(folderName) + 'images/', files = { 'fileToUpload':  fileHandle} )
        return r.status_code == 200

    def _encodePath(self, folderName = None, imageName = None):
        path = f'http://{self._destinationServer}/folders/'
        if folderName:
            path += f'{urllib.parse.quote(folderName)}/'
        if imageName:
            path += f'images/{urllib.parse.quote(imageName)}/'
        return path
