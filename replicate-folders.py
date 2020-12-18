#!/usr/bin/env python3
from mediaclient import MediaClient
from photomanager import PhotoManager
from mimetypesdb import hasMediaFileExtension
import sys
import time


class Replicator:
    def __init__(self, source, destination):
        self._destination = destination
        self._manager = PhotoManager(source)
        self._client = MediaClient(destination)
        self._errors = []

    def replicate(self):
        self._replicateFolders()
        self._reportCompletion()

    def _replicateFolders(self):
        serverFolders = self._client.folders()
        if serverFolders is None:
            print(self._reportError(f'Failed to get folder list from {self._destination}'))
            return

        for folderName in self._manager.folders:
                self._replicateFolder(serverFolders, folderName)

    def _replicateFolder(self, serverFolders, folderName):
        print(f'Replicating folder {folderName}...')
        if not folderName in serverFolders:
            if self._client.createFolder(folderName):
                print(f'  Successfully created folder {folderName}')
            else:
                print('  ' + self._reportError(f'Failed to create folder {folderName}. Not uploading folder images'))
        else:
            print(f'  Folder {folderName} already exists')
        self._replicateFolderImages(folderName)
        print(f'Done replicating folder {folderName}')

    def _replicateFolderImages(self, folderName):
        serverImages = self._client.images(folderName)
        if serverImages is None:
            print('  ' + self._reportError(f'Failed to get images in {folderName}. Not uploading folder images'))
            return
        folder = self._manager.folder(folderName)
        for imageName in folder.images:
            self._replicateImage(serverImages, folder, folderName, imageName)

    def _replicateImage(self, serverImages, folder, folderName, imageName):
        print(f'  Replicating image {imageName}...')
        if not hasMediaFileExtension(imageName):
            print('    ' + self._reportWarning(f'Skipping non-media file {imageName}'))
            return
        if not imageName in serverImages:
            print(f'    Uploading image {imageName}...')
            self._uploadImage(folder, imageName)
        else:
            print(f'    Image {imageName} already exists')
        print(f'  Done replicating image {imageName}')

    def _uploadImage(self, folder, imageName):
        image = folder.image(imageName)
        with image.content:
            if self._client.uploadImage(folder.name, imageName, image.content):
                print(f'    Successfully uploading image {imageName}')
            else:
                print('    ' + self._reportError(f'Failed to upload image {imageName}'))

    def _reportCompletion(self):
        print(f'\nReplication completed with {len(self._errors)} errors')
        if len(self._errors) > 0:
            errorLog = 'Errors:\n'
            for error in self._errors:
                errorLog += f'  {error}\n'
            print(errorLog)
            errorLogFileName = f'error-{str(time.time())}.log'
            print(f'Writing errors to error log {errorLogFileName}')
            with open(errorLogFileName, 'wt') as out:
                out.write(errorLog)
    
    def _reportError(self, message):
        self._errors.append(f'Error: {message}')
        return message

    def _reportWarning(self, message):
        self._errors.append(f'Warning: {message}')
        return message


def main(args):
    if len(args) < 2:
        print('Not enought arguments. expect source folder and destination server')
        sys.exit(-1)
    if len(args) > 2:
        print('Too many arguments. expect source folder and destination server')
        sys.exit(-1)
    source, destination = args
    Replicator(source, destination).replicate()


if __name__ == "__main__":
    main(sys.argv[1:])