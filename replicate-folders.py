#!/usr/bin/env python3
from mediaclient import MediaClient
from photomanager import PhotoManager
from mimetypesdb import hasMediaFileExtension
import sys
import time


def replicateAlbum(source, destination):
    errors = []
    manager = PhotoManager(source)
    client = MediaClient(destination)
    for folderName in manager.folders:
        print(f'Replicating folder {folderName}...')
        if not client.folderExists(folderName):
            if client.createFolder(folderName):
                print(f'  Successfully created folder {folderName}')
            else:
                error = f'Failed to create folder {folderName}. Not uploading folder images'
                errors.append('Error: ' + error)
                print(f'  {error}')
                continue
        else:
            print('  Folder {folderName} already exists')
        folder = manager.folder(folderName)
        for imageName in folder.images:
            print(f'  Replicating image {imageName}...')
            if not hasMediaFileExtension(imageName):
                warning = f'Skipping non-media file {imageName}'
                errors.append('Warning: ' + warning)
                print(f'    {warning}')
            if not client.imageExists(folderName, imageName):
                print(f'    Uploading image {imageName}...')
                image = folder.image(imageName)
                if client.uploadImage(folderName, imageName, image.content):
                    print(f'    Successfully uploading image {imageName}')
                else:
                    error = f'Failed to upload image {imageName}'
                    errors.append('Error: ' + error)
                    print(f'    {error}')
            else:
                print(f'    Image {imageName} already exists')
            print(f'  Done replicating image {imageName}')
        print(f'Done replicating folder {folderName}')
    print(f'\nReplication completed with {len(errors)} errors')
    if len(errors) > 0:
        errorLog = 'Errors:\n'
        for error in errors:
            errorLog += f'  {error}\n'
        print(errorLog)
        errorLogFileName = f'error-{str(time.time())}.log'
        print(f'Writing errors to error log {errorLogFileName}')
        with open(errorLogFileName, 'wt') as out:
            out.write(errorLog)

def main(args):
    if len(args) < 2:
        print('Not enought arguments. expect source folder and destination server')
        sys.exit(-1)
    if len(args) > 2:
        print('Too many arguments. expect source folder and destination server')
        sys.exit(-1)
    source, destination = args
    replicateAlbum(source, destination)


if __name__ == "__main__":
    main(sys.argv[1:])